import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from codex_skill_usage import candidates, connect, manifest_names, project_for, read_paths, scan


def row(kind, payload, timestamp='2026-01-01T00:00:00Z'):
    return {'type': kind, 'timestamp': timestamp, 'payload': payload}


def start(turn='t1', prompt='Build a page', timestamp='2026-01-01T00:00:00Z'):
    return [row('event_msg', {'type': 'task_started', 'turn_id': turn}),
            row('turn_context', {'turn_id': turn}),
            row('response_item', {'type': 'message', 'role': 'user',
                                 'content': [{'type': 'input_text', 'text': prompt}]}, timestamp)]


def read(call='c1', skill='example', wrapper=False, success=True):
    command = f'cat /fixture/skills/{skill}/SKILL.md'
    payload = {'type': 'function_call', 'name': 'exec_command', 'call_id': call,
               'arguments': json.dumps({'cmd': command})}
    manifest = f'---\nname: {skill}\ndescription: Example workflow.\n---\n# Instructions\n'
    output = {'exit_code': 0 if success else 1, 'output': manifest if success else 'No such file'}
    if wrapper:
        payload = {'type': 'custom_tool_call', 'name': 'exec', 'call_id': call,
                   'input': 'text(await tools.exec_command({cmd:' + json.dumps(command) + '}));'}
        output = [{'type': 'input_text', 'text': 'Script completed'},
                  {'type': 'input_text', 'text': json.dumps({'i': 0, 'value': output})}]
    return [row('response_item', payload), row('response_item', {
        'type': 'custom_tool_call_output' if wrapper else 'function_call_output',
        'call_id': call, 'output': output})]


class UsageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'sessions').mkdir()
        (self.root / 'archived_sessions').mkdir()
        self.db = connect(self.root / 'state.sqlite3')

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def write(self, name, rows, append=False):
        path = self.root / name
        with path.open('a' if append else 'w') as stream:
            for item in rows:
                stream.write(json.dumps(item) + '\n')
        return path

    def test_duplicate_reads_fork_and_archive(self):
        data = start() + read() + read('c2', wrapper=True)
        self.write('sessions/rollout-a.jsonl', data)
        self.write('sessions/rollout-fork.jsonl', data)
        self.write('archived_sessions/rollout-copy.jsonl', data)
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 1)
        self.assertEqual(result['duplicateReads'], 5)
        self.assertEqual(result['scan']['addedTriggers'], 1)
        again = scan(self.db, self.root)
        self.assertEqual(again['triggerCount'], 1)
        self.assertEqual(again['scan']['unchanged'], 3)
        self.assertEqual(again['scan']['addedTriggers'], 0)

    def test_incremental_pending_result_and_new_turn(self):
        call, output = read(wrapper=True)
        self.write('sessions/rollout-a.jsonl', start() + [call])
        self.assertEqual(scan(self.db, self.root)['triggerCount'], 0)
        self.write('sessions/rollout-a.jsonl', [output], append=True)
        self.assertEqual(scan(self.db, self.root)['triggerCount'], 1)
        self.write('sessions/rollout-a.jsonl', [row('event_msg', {'type': 'task_complete'})]
                   + start('t2') + read('c3'), append=True)
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 2)
        self.assertEqual(result['scan']['appended'], 1)

    def test_copied_call_ids_deduplicate_even_if_turn_ids_change(self):
        self.write('sessions/rollout-a.jsonl', start('original') + read('same-call'))
        self.write('sessions/rollout-fork.jsonl', start('fork') + read('same-call'))
        self.assertEqual(scan(self.db, self.root)['triggerCount'], 1)
        self.write('sessions/rollout-fork.jsonl', start('fork', 'Inspect the example skill') + read('same-call'))
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 0)
        self.assertEqual(result['maintenanceReads'], 2)
        self.assertEqual(result['duplicateReads'], 0)

    def test_partial_final_line_retried(self):
        call, output = read()
        path = self.write('sessions/rollout-a.jsonl', start() + [call])
        encoded = json.dumps(output)
        with path.open('a') as stream:
            stream.write(encoded[:70])
        self.assertEqual(scan(self.db, self.root)['triggerCount'], 0)
        with path.open('a') as stream:
            stream.write(encoded[70:] + '\n')
        self.assertEqual(scan(self.db, self.root)['triggerCount'], 1)

    def test_maintenance_failure_search_and_mentions(self):
        data = start(prompt='Update the example skill') + read()
        data += start('t2', '更新蒸馏技能，统计 skill 触发次数') + read('c2', wrapper=True)
        data += start('t3') + read('c3', success=False)
        data += read('c4')
        data[-2]['payload']['arguments'] = json.dumps({'cmd': 'rg example /fixture/skills/example/SKILL.md'})
        self.write('sessions/rollout-a.jsonl', data)
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 0)
        self.assertEqual(result['maintenanceReads'], 2)
        self.assertEqual(result['unconfirmedReads'], 1)

    def test_source_edit_retroactively_excludes_turn(self):
        self.write('sessions/rollout-a.jsonl', start() + read())
        self.assertEqual(scan(self.db, self.root)['triggerCount'], 1)
        self.write('sessions/rollout-a.jsonl', [row('response_item', {
            'type': 'custom_tool_call', 'name': 'apply_patch', 'call_id': 'patch1',
            'input': '*** Begin Patch\n*** Update File: /fixture/skills/example/SKILL.md\n@@\n-x\n+y\n*** End Patch'})], append=True)
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 0)
        self.assertEqual(result['maintenanceReads'], 1)
        self.assertEqual(result['scan']['removedTriggers'], 1)

    def test_rewrite_replaces_observations_and_error_preserves_old(self):
        path = self.write('sessions/rollout-a.jsonl', start() + read())
        self.assertEqual(scan(self.db, self.root)['triggerCount'], 1)
        path.write_text('{"type":"response_item","payload":{"type":"function_call",broken}}\n')
        result = scan(self.db, self.root)
        self.assertEqual(len(result['scan']['errors']), 1)
        self.assertEqual(result['triggerCount'], 1)
        self.write('sessions/rollout-a.jsonl', start() + read(success=False))
        self.assertEqual(scan(self.db, self.root)['triggerCount'], 0)

    def test_legacy_turns_and_missing_turn(self):
        messages = [x for x in start() if x['type'] == 'response_item']
        self.write('sessions/rollout-a.jsonl', messages + read())
        self.write('sessions/rollout-fork.jsonl', messages + read())
        self.write('sessions/rollout-missing.jsonl', read('missing'))
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 1)
        self.assertEqual(result['unconfirmedReads'], 1)

    def test_no_raw_prompt_or_output_in_state(self):
        self.write('sessions/rollout-a.jsonl', start(prompt='PRIVATE PROMPT SENTINEL') + read())
        scan(self.db, self.root)
        dump = '\n'.join(self.db.iterdump())
        self.assertNotIn('PRIVATE PROMPT SENTINEL', dump)
        self.assertNotIn('Example workflow', dump)

    def test_user_before_context_keeps_maintenance_exclusion(self):
        data = start(prompt='修改 example 技能')
        self.write('sessions/rollout-a.jsonl', [data[2], data[1]] + read())
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 0)
        self.assertEqual(result['maintenanceReads'], 1)

    def test_frontmatter_alone_is_not_a_workflow_read(self):
        self.assertEqual(manifest_names('---\nname: example\ndescription: Test.\n---\n'), set())

    def test_same_size_rewrite_with_identical_tail_replaces_old_turn(self):
        data = start() + read()
        data.append(row('response_item', {'type': 'message', 'role': 'assistant',
                    'content': [{'type': 'output_text', 'text': 'x' * 900}]}))
        path = self.write('sessions/rollout-a.jsonl', data)
        scan(self.db, self.root)
        before = path.read_text()
        path.write_text(before.replace('"t1"', '"t2"'))
        scan(self.db, self.root)
        turns = self.db.execute('SELECT DISTINCT turn_key FROM observations').fetchall()
        self.assertEqual(turns, [('turn:t2',)])

    def test_wrapper_source_edit_and_repeated_context(self):
        data = start() + read()
        data += [row('turn_context', {'turn_id': 't1'})]
        patch = '*** Begin Patch\n*** Update File: /fixture/skills/example/SKILL.md\n@@\n-x\n+y\n*** End Patch'
        data += [row('response_item', {'type': 'custom_tool_call', 'name': 'exec', 'call_id': 'patch',
                 'input': 'text(await tools.apply_patch(' + json.dumps(patch) + '));'})]
        self.write('sessions/rollout-a.jsonl', data)
        self.assertEqual(scan(self.db, self.root)['maintenanceReads'], 1)

    @unittest.skipUnless(shutil.which('zstd'), 'zstd unavailable')
    def test_compressed_archive_and_repeated_scan(self):
        plain = self.write('sessions/rollout-a.jsonl', start() + read())
        compressed = self.root / 'archived_sessions/rollout-a.jsonl.zst'
        subprocess.run(['zstd', '-q', str(plain), '-o', str(compressed)], check=True)
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 1)
        self.assertEqual(scan(self.db, self.root)['scan']['unchanged'], 2)

    def test_literal_reads_only(self):
        path = '/fixture/skills/example/SKILL.md'
        self.assertEqual(read_paths(f"sed -n '1,100p' {path} && cat '{path}'"), [path])
        for cmd in [f'rg name {path}', f'echo {path}', f'python3 - <<\'PY\'\nprint("{path}")\nPY',
                    f'cat $(echo {path})', f'sed -i s/a/b/ {path}', f'/usr/bin/sed -i s/a/b/ {path}']:
            self.assertEqual(read_paths(cmd), [])
        payload = read(wrapper=True)[0]['payload']
        self.assertEqual(candidates(payload), [path])
        self.assertEqual(candidates({'name': 'exec', 'input': f'const path="{path}";'}), [])

    def git_repo(self, directory):
        subprocess.run(['git', 'init', '-q', str(directory)], check=True)
        return directory

    def project_start(self, turn, cwd, prompt='Build a page'):
        data = start(turn, prompt)
        data[1]['payload']['cwd'] = str(cwd)
        return data

    def test_project_attribution_and_skill_cross_totals(self):
        a = self.git_repo(self.root / 'a')
        b = self.git_repo(self.root / 'b')
        nested = a / 'src'
        nested.mkdir()
        data = self.project_start('p1', a) + read('p1-read') + read('p1-repeat')
        data += self.project_start('p2', nested) + read('p2-read')
        data += self.project_start('p3', b) + read('p3-read')
        self.write('sessions/rollout-a.jsonl', data)
        result = scan(self.db, self.root)
        projects = result['projectAttribution']
        self.assertEqual(result['triggerCount'], 3)
        self.assertEqual(projects['projectCount'], 2)
        self.assertEqual(projects['attributedTriggers'], 3)
        self.assertEqual(sorted(p['triggerCount'] for p in projects['projects']), [1, 2])
        self.assertEqual(sum(p['triggerCount'] for p in result['skills'][0]['projects']), 3)
        self.assertEqual(scan(self.db, self.root)['scan']['addedTriggers'], 0)

    def test_first_load_project_wins_inside_one_turn_and_fork(self):
        a, b = self.git_repo(self.root / 'a'), self.git_repo(self.root / 'b')
        data = self.project_start('p1', a) + read('original')
        data += [row('turn_context', {'turn_id': 'p1', 'cwd': str(b)})] + read('later')
        self.write('sessions/rollout-a.jsonl', data)
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 1)
        self.assertEqual(len(result['projectAttribution']['projects']), 1)
        self.assertEqual(result['projectAttribution']['projects'][0]['root'], str(a.resolve()))
        self.write('sessions/rollout-fork.jsonl', self.project_start('copied', b) + read('original'))
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 1)
        self.assertEqual(result['projectAttribution']['ambiguousTriggers'], 1)
        self.assertEqual(result['projectAttribution']['attributedTriggers'], 0)

    def test_missing_directory_unknown_cwd_and_same_name_repos(self):
        missing = self.root / 'deleted'
        data = self.project_start('p1', missing) + read('p1-read')
        second = start('p2')
        # Remove an inherited cwd explicitly; an absent cwd retains session context.
        second[1]['payload']['cwd'] = ''
        data += second + read('p2-read')
        self.write('sessions/rollout-a.jsonl', data)
        projects = scan(self.db, self.root)['projectAttribution']
        self.assertEqual(projects['projectCount'], 0)
        self.assertEqual(projects['unattributedTriggers'], 2)
        self.assertEqual({p['kind'] for p in projects['projects']}, {'directory', 'unknown'})
        a = self.git_repo(self.root / 'left' / 'same')
        b = self.git_repo(self.root / 'right' / 'same')
        self.assertNotEqual(project_for(str(a))[0], project_for(str(b))[0])

    def test_schema_migration_backfills_metadata_without_recounting(self):
        repo = self.git_repo(self.root / 'project')
        data = [row('session_meta', {'cwd': str(repo)})] + start() + read()
        self.write('sessions/rollout-a.jsonl', data)
        self.assertEqual(scan(self.db, self.root)['triggerCount'], 1)
        self.db.execute('ALTER TABLE observations DROP COLUMN cwd')
        self.db.execute("UPDATE meta SET value='1' WHERE key='version'")
        for filename, raw in self.db.execute('SELECT path,context FROM files').fetchall():
            context = json.loads(raw)
            context.pop('cwd', None)
            self.db.execute('UPDATE files SET context=? WHERE path=?', (json.dumps(context), filename))
        self.db.commit()
        self.db.close()
        self.db = connect(self.root / 'state.sqlite3')
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 1)
        self.assertEqual(result['scan']['addedTriggers'], 0)
        self.assertEqual(result['scan']['removedTriggers'], 0)
        self.assertFalse(result['scan']['reindexed'])
        self.assertEqual(result['scan']['project_backfilled'], 1)
        self.assertEqual(result['projectAttribution']['projectCount'], 1)
        self.assertEqual(result['projectAttribution']['pendingBackfillObservations'], 0)

    @unittest.skipUnless(shutil.which('zstd'), 'zstd unavailable')
    def test_compressed_metadata_backfill(self):
        repo = self.git_repo(self.root / 'project')
        plain = self.write('sessions/rollout-a.jsonl', self.project_start('t1', repo) + read())
        compressed = self.root / 'archived_sessions/rollout-a.jsonl.zst'
        subprocess.run(['zstd', '-q', str(plain), '-o', str(compressed)], check=True)
        plain.unlink()
        scan(self.db, self.root)
        self.db.execute('UPDATE observations SET cwd=NULL')
        self.db.execute('DELETE FROM projects')
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 1)
        self.assertEqual(result['scan']['project_backfilled'], 1)
        self.assertEqual(result['projectAttribution']['projectCount'], 1)

    def test_worktrees_share_project_identity(self):
        repo = self.git_repo(self.root / 'project')
        subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Fixture', '-c',
                        'user.email=fixture@example.test', 'commit', '-q', '--allow-empty', '-m', 'seed'], check=True)
        tree = self.root / 'tree'
        subprocess.run(['git', '-C', str(repo), 'worktree', 'add', '-q', '--detach', str(tree)], check=True)
        self.assertEqual(project_for(str(repo)), project_for(str(tree)))

    def test_compact_cli_preserves_totals_and_reports_project_coverage(self):
        self.write('sessions/rollout-a.jsonl', start() + read())
        script = Path(__file__).with_name('codex_skill_usage.py')
        result = subprocess.run([sys.executable, str(script), 'scan', '--compact',
                                 '--codex-home', str(self.root), '--state', str(self.root / 'state.sqlite3')],
                                capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        self.assertEqual(data['triggerCount'], 1)
        self.assertEqual(data['projectAttribution']['unattributedTriggers'], 1)
        self.assertEqual(data['scan']['errors'], [])
        self.assertNotIn('skills', data)
        self.assertNotIn('projects', data['projectAttribution'])

    def test_removed_source_recovers_location_from_copied_call(self):
        repo = self.git_repo(self.root / 'project')
        data = self.project_start('t1', repo) + read()
        old = self.write('sessions/rollout-a.jsonl', data)
        self.write('archived_sessions/rollout-copy.jsonl', data)
        scan(self.db, self.root)
        self.db.execute('UPDATE observations SET cwd=NULL WHERE file=?', (str(old),))
        old.unlink()
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 1)
        self.assertEqual(result['scan']['projectLocationsRecovered'], 1)
        self.assertEqual(result['projectAttribution']['pendingBackfillObservations'], 0)

    def test_removed_source_without_copy_is_explicitly_unattributed(self):
        old = self.write('sessions/rollout-a.jsonl', start() + read())
        self.write('sessions/rollout-empty.jsonl', start('empty'))
        scan(self.db, self.root)
        self.db.execute('UPDATE observations SET cwd=NULL WHERE file=?', (str(old),))
        old.unlink()
        result = scan(self.db, self.root)
        self.assertEqual(result['triggerCount'], 1)
        self.assertEqual(result['scan']['projectLocationsUnavailable'], 1)
        self.assertEqual(result['scan']['retainedMissingFiles'], 1)
        self.assertEqual(result['projectAttribution']['unattributedTriggers'], 1)
        self.assertEqual(result['projectAttribution']['pendingBackfillObservations'], 0)


if __name__ == '__main__':
    unittest.main()
