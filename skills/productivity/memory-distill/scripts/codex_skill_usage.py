#!/usr/bin/env python3
"""Incrementally count evidenced Codex skill reads; never execute log contents."""
import argparse
import ast
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import sqlite3
import subprocess
import sys

from session_excerpt import clean_user

VERSION = 2
PARSER_REVISION = '3'
LITERAL = r'''("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`[^`]*`)'''
MAINTENANCE = re.compile(
    r'(?is)(?:skill|技能).{0,45}(?:维护|修改|更新|迁移|重命名|审查|统计|触发次数|回填|清单|指纹|怎么写|怎么用|是什么)'
    r'|(?:维护|修改|更新|迁移|重命名|审查|回填|统计|同步|检查|查看|读取|创建|新增|安装|卸载|删除|加到).{0,45}(?:skill|技能)'
    r'|(?:edit|update|inspect|review|migrate|rename|install|remove|create|audit|count|list|read)\b.{0,60}\bskills?\b')
MANIFEST = re.compile(r'''(?m)^\s*name:\s*["']?([\w:.-]+)["']?\s*$''')


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def literal_value(value):
    try:
        if value.startswith('`'):
            return value[1:-1] if '${' not in value else None
        return json.loads(value) if value.startswith('"') else ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return None


def read_paths(command):
    """Only literal cat/head/sed reads; exclude searches, loops and script sources."""
    if not isinstance(command, str) or any(s in command for s in ('<<', '$(', '`')):
        return []
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=';&|()<>')
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return []
    segments, segment = [], []
    for token in tokens:
        if token and all(c in ';&|()<>\n' for c in token):
            if segment:
                segments.append(segment)
            segment = []
        else:
            segment.append(token)
    if segment:
        segments.append(segment)
    paths = []
    for words in segments:
        if not words or Path(words[0]).name not in ('cat', 'head', 'sed'):
            continue
        if Path(words[0]).name == 'sed' and any(w in ('-i', '--in-place') or w.startswith('-i') for w in words[1:]):
            continue
        for word in words[1:]:
            if word.endswith('/SKILL.md') and not any(c in word for c in '$*?{}\n'):
                paths.append(word)
    return sorted(set(paths))


def candidates(payload):
    name = payload.get('name', '').split('.')[-1]
    raw = payload.get('arguments', payload.get('input', ''))
    if isinstance(raw, str):
        try:
            args = json.loads(raw)
        except ValueError:
            args = None
    else:
        args = raw
    commands = []
    if isinstance(args, dict):
        cmd = args.get('cmd', args.get('command'))
        if isinstance(cmd, list):
            cmd = cmd[-1] if len(cmd) >= 3 and cmd[-2] in ('-c', '-lc') else ''
        if isinstance(cmd, str):
            commands.append(cmd)
    if name == 'exec' and isinstance(raw, str):
        # Match only literal exec_command calls, not paths quoted in generic scripts.
        for match in re.finditer(r'\b(?:tools\.)?exec_command\s*\(\s*\{\s*["\']?cmd["\']?\s*:\s*' + LITERAL, raw):
            value = literal_value(match[1])
            if value is not None:
                commands.append(value)
    return sorted({p for cmd in commands for p in read_paths(cmd)})


def output_strings(value):
    """Unwrap tool envelopes and JSON stdout without interpreting their contents."""
    if isinstance(value, list):
        for item in value:
            yield from output_strings(item)
    elif isinstance(value, dict):
        for key in ('text', 'output', 'content', 'value', 'result', 'results'):
            if key in value:
                yield from output_strings(value[key])
    elif isinstance(value, str):
        try:
            decoded = json.loads(value)
        except ValueError:
            decoded = None
        if isinstance(decoded, (dict, list)):
            yield from output_strings(decoded)
        else:
            # Batched exec calls often print one JSON envelope per line.
            for line in value.splitlines():
                if line.startswith('{'):
                    try:
                        item = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(item, dict):
                        yield from output_strings(item)
            yield value


def manifest_names(output):
    names = set()
    for text in output_strings(output):
        # An echoed path/command or a name in the skills catalog is insufficient.
        for block in re.finditer(r'(?m)^---\s*\n([\s\S]*?)\n---(?:\s*\n|$)', text):
            match = MANIFEST.search(block[1])
            if match and re.search(r'(?m)^description:\s*\S', block[1]) and text[block.end():].strip():
                names.add(match[1])
    return names


def connect(path):
    db = sqlite3.connect(path)
    db.execute('PRAGMA journal_mode=WAL')
    db.executescript('''
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY, size INTEGER, mtime INTEGER, offset INTEGER,
            line INTEGER, boundary TEXT, context TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS observations (
            file TEXT, call_id TEXT, skill TEXT, turn_key TEXT, timestamp TEXT,
            line INTEGER, status TEXT, PRIMARY KEY(file, call_id, skill));
        CREATE TABLE IF NOT EXISTS excluded_turns (
            file TEXT, turn_key TEXT, reason TEXT, PRIMARY KEY(file, turn_key));
        CREATE TABLE IF NOT EXISTS projects (
            cwd TEXT PRIMARY KEY, project_id TEXT, name TEXT, root TEXT, kind TEXT);
        CREATE TABLE IF NOT EXISTS turn_aliases (turn_key TEXT PRIMARY KEY, canonical_turn TEXT);
        CREATE INDEX IF NOT EXISTS observation_turn ON observations(turn_key, skill);
        CREATE INDEX IF NOT EXISTS observation_call ON observations(call_id, skill);
        CREATE INDEX IF NOT EXISTS excluded_turn ON excluded_turns(turn_key);
    ''')
    old = db.execute("SELECT value FROM meta WHERE key='version'").fetchone()
    if old and old[0] not in ('1', str(VERSION)):
        raise ValueError('Unsupported state version; use a separate state database for a rebuild.')
    if 'cwd' not in {r[1] for r in db.execute('PRAGMA table_info(observations)')}:
        db.execute('ALTER TABLE observations ADD COLUMN cwd TEXT')
    db.execute("INSERT OR REPLACE INTO meta VALUES ('version', ?)", (str(VERSION),))
    db.commit()
    return db


@contextmanager
def source(path, partial=False):
    if path.name.endswith('.zst'):
        if not shutil.which('zstd'):
            raise RuntimeError('zstd is required for compressed rollouts')
        process = subprocess.Popen(['zstd', '-q', '-d', '-c', '--', str(path)], stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL)
        try:
            yield process.stdout
            if not partial and process.wait() != 0:
                raise RuntimeError('zstd could not decode rollout')
        finally:
            process.stdout.close()
            if process.poll() is None:
                process.terminate()
                process.wait()
    else:
        with path.open('rb') as stream:
            yield stream


def boundary(path, offset):
    with path.open('rb') as stream:
        head = stream.read(min(offset, 256))
        stream.seek(max(0, offset - 256))
        return hashlib.sha256(head + stream.read(min(offset, 256))).hexdigest()


def message_text(payload):
    return '\n'.join(p.get('text', '') for p in payload.get('content', [])
                     if p.get('type') in ('input_text', 'output_text'))


def skill_edit(payload):
    name = payload.get('name', '').split('.')[-1]
    raw = payload.get('arguments', payload.get('input', ''))
    patches = [raw] if name == 'apply_patch' and isinstance(raw, str) else []
    if name == 'exec' and isinstance(raw, str):
        patches += [literal_value(m[1]) for m in re.finditer(r'\b(?:tools\.)?apply_patch\s*\(\s*' + LITERAL, raw)]
    return any(re.search(r'(?m)^\*\*\* (?:Add|Update|Delete) File: (?:[^\n]*/)?SKILL\.md\s*$', p)
               for p in patches if isinstance(p, str))


def process_row(db, filename, row, line, context):
    payload = row.get('payload', {})
    if not isinstance(payload, dict):
        return
    kind, subtype = row.get('type'), payload.get('type')
    if kind == 'session_meta':
        context['session'] = payload.get('id', payload.get('session_id', ''))
        context['cwd'] = payload.get('cwd') or ''
    if kind == 'turn_context' and 'cwd' in payload:
        context['cwd'] = payload.get('cwd') or ''
    if kind == 'turn_context' or (kind == 'event_msg' and subtype == 'task_started'):
        turn = payload.get('turn_id')
        if turn:
            previous = context.get('turn')
            if kind == 'turn_context' and context.get('awaiting_context'):
                # Some versions write user messages before their turn_context.
                db.execute('''INSERT OR IGNORE INTO excluded_turns SELECT file, ?, reason
                    FROM excluded_turns WHERE file=? AND turn_key=?''',
                           ('turn:' + turn, filename, previous))
                db.execute('UPDATE observations SET turn_key=? WHERE file=? AND turn_key=?',
                           ('turn:' + turn, filename, previous))
                context['awaiting_context'] = False
                context['fresh_turn'] = False
            elif previous != 'turn:' + turn or subtype == 'task_started':
                context['fresh_turn'] = True
            context['turn'] = 'turn:' + turn
    if kind == 'response_item' and subtype == 'message' and payload.get('role') == 'user':
        text = clean_user(message_text(payload))
        if text:
            # Fallback independent of filename/session, so a fork's copied history deduplicates.
            if not context.get('fresh_turn'):
                context['turn'] = ('user:' + digest(row['timestamp'] + '\n' + text)
                                   if row.get('timestamp') else None)
                context['awaiting_context'] = True
            context['fresh_turn'] = False
            if context.get('turn') and MAINTENANCE.search(text):
                db.execute('INSERT OR REPLACE INTO excluded_turns VALUES (?, ?, ?)',
                           (filename, context['turn'], 'maintenance_or_inspection'))
    if kind == 'event_msg' and subtype == 'task_complete':
        context['fresh_turn'] = False
    if kind != 'response_item':
        return
    pending = context.setdefault('pending', {})
    if subtype in ('function_call', 'custom_tool_call'):
        if skill_edit(payload) and context.get('turn'):
            db.execute('INSERT OR REPLACE INTO excluded_turns VALUES (?, ?, ?)',
                       (filename, context['turn'], 'skill_source_edit'))
        paths = candidates(payload)
        call_id = payload.get('call_id')
        if paths and call_id:
            pending[call_id] = {'paths': paths, 'turn': context.get('turn'),
                                'timestamp': row.get('timestamp'), 'line': line,
                                'cwd': context.get('cwd') or ''}
    elif subtype in ('function_call_output', 'custom_tool_call_output'):
        call_id = payload.get('call_id')
        call = pending.pop(call_id, None)
        if not call:
            return
        names = manifest_names(payload.get('output'))
        for path in call['paths']:
            skill = Path(path).parent.name
            status = 'verified' if skill in names else 'unconfirmed_read'
            if not call.get('turn'):
                status = 'missing_turn'
            db.execute('''INSERT OR REPLACE INTO observations
                       (file, call_id, skill, turn_key, timestamp, line, status, cwd)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (filename, call_id, skill, call.get('turn'), call['timestamp'], call['line'],
                        status, call.get('cwd') or ''))


def backfill_locations(db, path, checkpoint):
    """Enrich old evidence from metadata only; keep trigger decisions unchanged."""
    context = json.loads(checkpoint[5])
    targets = {r[0] for r in db.execute('SELECT DISTINCT line FROM observations WHERE file=?', (str(path),))}
    targets.update(c['line'] for c in context.get('pending', {}).values())
    cwd, locations = '', {}
    if targets:
        with source(path, partial=True) as stream:
            for line in range(1, checkpoint[3] + 1):
                raw = stream.readline()
                if not raw:
                    raise ValueError('Rollout ended before its saved checkpoint during project backfill')
                if any(k in raw[:180] for k in (b'"session_meta"', b'"turn_context"')):
                    row = json.loads(raw)
                    if row.get('type') in ('session_meta', 'turn_context'):
                        payload = row.get('payload', {})
                        if 'cwd' in payload:
                            cwd = payload.get('cwd') or ''
                if line in targets:
                    locations[line] = cwd
        db.executemany('UPDATE observations SET cwd=? WHERE file=? AND line=?',
                       [(value, str(path), line) for line, value in locations.items()])
    context['cwd'] = cwd
    for call in context.get('pending', {}).values():
        call['cwd'] = locations.get(call['line'], '')
    db.execute('UPDATE files SET context=? WHERE path=?',
               (json.dumps(context, ensure_ascii=False), str(path)))
    return context


def project_for(cwd):
    """Resolve a logged directory against current Git metadata; no network/remotes."""
    if not cwd or not Path(cwd).is_absolute():
        return ('unknown', '未识别项目', None, 'unknown')
    directory = Path(cwd)
    if directory.is_dir():
        try:
            env = {k: v for k, v in os.environ.items()
                   if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE')}
            result = subprocess.run(['git', '-C', cwd, 'rev-parse', '--path-format=absolute',
                                     '--show-toplevel', '--git-common-dir'],
                                    capture_output=True, text=True, timeout=5, env=env)
            if result.returncode == 0:
                root, common = result.stdout.strip().splitlines()[:2]
                common = str(Path(common).resolve())
                canonical = str(Path(common).parent) if Path(common).name == '.git' else root
                return ('git:' + digest(common)[:16], Path(canonical).name, canonical, 'git')
        except (OSError, ValueError, subprocess.TimeoutExpired):
            pass
    return ('directory:' + digest(cwd)[:16], directory.name or cwd, cwd, 'directory')


def index_projects(db):
    missing = db.execute('''SELECT DISTINCT COALESCE(o.cwd, '') FROM observations o
        LEFT JOIN projects p ON p.cwd=COALESCE(o.cwd, '') WHERE p.cwd IS NULL''').fetchall()
    for (cwd,) in missing:
        db.execute('INSERT OR REPLACE INTO projects VALUES (?, ?, ?, ?, ?)', (cwd, *project_for(cwd)))


def reconcile_turns(db):
    """Copied call IDs connect original and rewritten fork turn identifiers."""
    parents, calls = {}, {}

    def find(turn):
        parents.setdefault(turn, turn)
        if parents[turn] != turn:
            parents[turn] = find(parents[turn])
        return parents[turn]

    for call, skill, turn in db.execute('SELECT call_id, skill, turn_key FROM observations WHERE turn_key IS NOT NULL'):
        key = (call, skill)
        left = find(turn)
        right = find(calls.setdefault(key, turn))
        if left != right:
            parents[max(left, right)] = min(left, right)
    db.execute('DELETE FROM turn_aliases')
    db.executemany('INSERT INTO turn_aliases VALUES (?, ?)', [(turn, find(turn)) for turn in parents])


def recover_archived_locations(db, paths):
    retained = {str(path) for path in paths}
    recovered = unavailable = 0
    pending = db.execute('SELECT file, call_id, skill FROM observations WHERE cwd IS NULL').fetchall()
    for filename, call, skill in pending:
        variants = {r[0] for r in db.execute('''SELECT DISTINCT cwd FROM observations
            WHERE call_id=? AND skill=? AND cwd IS NOT NULL AND cwd!='' ''', (call, skill))}
        if len(variants) == 1:
            cwd = next(iter(variants))
            recovered += 1
        elif filename not in retained:
            cwd = ''
            unavailable += 1
        else:
            continue  # A readable source with a failed backfill must remain pending for retry.
        db.execute('UPDATE observations SET cwd=? WHERE file=? AND call_id=? AND skill=?',
                   (cwd, filename, call, skill))
    return recovered, unavailable


def scan_file(db, path):
    filename = str(path)
    stat = path.stat()
    old = db.execute('SELECT size, mtime, offset, line, boundary, context FROM files WHERE path=?',
                     (filename,)).fetchone()
    unchanged = bool(old and old[:2] == (stat.st_size, stat.st_mtime_ns))
    compressed = path.name.endswith('.zst')
    resume = bool(old and not compressed and (stat.st_size > old[2] or old[0] == -1)
                  and boundary(path, old[2]) == old[4])
    enriched = False
    if old and (unchanged or resume) and ('cwd' not in json.loads(old[5]) or db.execute(
            'SELECT 1 FROM observations WHERE file=? AND cwd IS NULL LIMIT 1', (filename,)).fetchone()):
        backfill_locations(db, path, old)
        old = db.execute('SELECT size, mtime, offset, line, boundary, context FROM files WHERE path=?',
                         (filename,)).fetchone()
        enriched = True
    if unchanged:
        return 'project_backfilled' if enriched else 'unchanged'
    offset, line = (old[2], old[3]) if resume else (0, 0)
    context = json.loads(old[5]) if resume else {}
    context.setdefault('cwd', '')
    if not resume:
        db.execute('DELETE FROM observations WHERE file=?', (filename,))
        db.execute('DELETE FROM excluded_turns WHERE file=?', (filename,))
    with source(path) as stream:
        if offset:
            stream.seek(offset)
        while True:
            raw = stream.readline()
            if not raw:
                break
            if not raw.endswith(b'\n'):
                # Concurrent writer: retry this partial line next time.
                if compressed:
                    raise ValueError('Incomplete compressed rollout line')
                break
            offset += len(raw)
            line += 1
            # Skip bulky tool output unless there is a literal skill read awaiting a result.
            is_output = b'function_call_output' in raw[:250] or b'custom_tool_call_output' in raw[:250]
            if is_output and not context.get('pending'):
                continue
            if not is_output and not any(k in raw[:600] for k in
                    (b'session_meta', b'turn_context', b'task_started', b'task_complete',
                     b'"message"', b'function_call', b'custom_tool_call')):
                continue
            try:
                row = json.loads(raw)
            except (ValueError, UnicodeError):
                raise ValueError('Malformed complete JSON line at ' + str(line)) from None
            process_row(db, filename, row, line, context)
    saved_boundary = '' if compressed else boundary(path, offset)
    # A partial trailing line must not become an unchanged checkpoint.
    saved_size = stat.st_size if compressed or offset == stat.st_size else -1
    db.execute('INSERT OR REPLACE INTO files VALUES (?, ?, ?, ?, ?, ?, ?)',
               (filename, saved_size, stat.st_mtime_ns, offset, line, saved_boundary,
                json.dumps(context, ensure_ascii=False)))
    return 'appended' if resume else 'scanned'


TURN_FILTER = '''COALESCE(a.canonical_turn, o.turn_key) NOT IN
        (SELECT COALESCE(ea.canonical_turn, e.turn_key) FROM excluded_turns e
         LEFT JOIN turn_aliases ea ON ea.turn_key=e.turn_key WHERE e.turn_key IS NOT NULL)'''
ACCEPTED = '''SELECT turn_key, skill, timestamp, file, line, cwd, call_id FROM (
        SELECT COALESCE(a.canonical_turn, o.turn_key) AS turn_key, o.skill, o.timestamp,
               o.file, o.line, o.cwd, o.call_id,
               ROW_NUMBER() OVER (PARTITION BY o.call_id, o.skill ORDER BY o.timestamp, o.file, o.turn_key) AS occurrence
        FROM observations o LEFT JOIN turn_aliases a ON a.turn_key=o.turn_key
        WHERE o.status='verified' AND ''' + TURN_FILTER + ''') WHERE occurrence=1'''


def project_summary(db):
    triggers = db.execute('''SELECT skill, timestamp, COALESCE(cwd, ''), call_id FROM (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY turn_key, skill ORDER BY timestamp, line, file) AS first_load
        FROM (''' + ACCEPTED + ''')) WHERE first_load=1''').fetchall()
    lookup = {r[0]: r[1:] for r in db.execute('SELECT cwd, project_id, name, root, kind FROM projects')}
    evidence = {}
    for call, skill, cwd in db.execute("SELECT call_id, skill, COALESCE(cwd, '') FROM observations WHERE status='verified'"):
        project = lookup.get(cwd)
        if project and project[3] != 'unknown':
            evidence.setdefault((call, skill), {})[project[0]] = project
    groups, ambiguous = {}, 0
    for skill, timestamp, cwd, call in triggers:
        identity, name, root, kind = lookup.get(cwd, ('unknown', '未识别项目', None, 'unknown'))
        variants = evidence.get((call, skill), {})
        if len(variants) > 1:
            identity, name, root, kind = ('unknown', '未识别项目', None, 'unknown')
            ambiguous += 1
        elif len(variants) == 1:
            identity, name, root, kind = next(iter(variants.values()))
        group = groups.setdefault(identity, {'id': identity, 'name': name, 'root': root, 'kind': kind,
                                             'paths': set(), 'triggerCount': 0, 'skills': {},
                                             'firstSeen': None, 'lastSeen': None})
        if cwd:
            group['paths'].add(cwd)
        group['triggerCount'] += 1
        group['skills'][skill] = group['skills'].get(skill, 0) + 1
        if timestamp:
            group['firstSeen'] = min(group['firstSeen'] or timestamp, timestamp)
            group['lastSeen'] = max(group['lastSeen'] or timestamp, timestamp)
    projects = []
    for group in groups.values():
        group['paths'] = sorted(group['paths'])
        group['skillCount'] = len(group['skills'])
        group['skills'] = [{'name': n, 'triggerCount': c} for n, c in
                           sorted(group['skills'].items(), key=lambda p: (-p[1], p[0]))]
        projects.append(group)
    projects.sort(key=lambda p: (-p['triggerCount'], p['id']))
    attributed = sum(p['triggerCount'] for p in projects if p['kind'] == 'git')
    return {'projectCount': sum(p['kind'] == 'git' for p in projects),
            'directoryGroupCount': sum(p['kind'] == 'directory' for p in projects),
            'attributedTriggers': attributed, 'unattributedTriggers': len(triggers) - attributed,
            'ambiguousTriggers': ambiguous,
            'pendingBackfillObservations': db.execute('SELECT COUNT(*) FROM observations WHERE cwd IS NULL').fetchone()[0],
            'basis': 'Logged turn cwd; Git roots resolved locally at indexing time.', 'projects': projects}


def summary(db):
    rows = db.execute('''SELECT skill, COUNT(*), MIN(first_seen), MAX(last_seen) FROM
        (SELECT skill, turn_key, MIN(timestamp) first_seen, MAX(timestamp) last_seen
         FROM (''' + ACCEPTED + ''') GROUP BY skill, turn_key)
        GROUP BY skill ORDER BY COUNT(*) DESC, skill''').fetchall()
    total_reads = db.execute('SELECT COUNT(*) FROM observations').fetchone()[0]
    unconfirmed = db.execute("SELECT COUNT(*) FROM observations WHERE status!='verified'").fetchone()[0]
    excluded = db.execute('''SELECT COUNT(*) FROM observations o
        LEFT JOIN turn_aliases a ON a.turn_key=o.turn_key
        WHERE status='verified' AND NOT (''' + TURN_FILTER + ')').fetchone()[0]
    total = sum(row[1] for row in rows)
    projects = project_summary(db)
    skills = [{'name': r[0], 'triggerCount': r[1], 'firstSeen': r[2], 'lastSeen': r[3],
               'projects': [{'projectId': p['id'], 'name': p['name'], 'kind': p['kind'],
                             'triggerCount': s['triggerCount']}
                            for p in projects['projects'] for s in p['skills'] if s['name'] == r[0]]}
              for r in rows]
    if (projects['attributedTriggers'] + projects['unattributedTriggers'] != total or
            any(sum(p['triggerCount'] for p in s['projects']) != s['triggerCount'] for s in skills)):
        raise ValueError('Project and skill cross totals do not reconcile with global trigger counts')
    return {'version': VERSION, 'metric': 'verified_skill_read_turns', 'complete': False,
            'coverage': 'Locally retained rollouts only; verified loads are not workflow successes.',
            'files': db.execute('SELECT COUNT(*) FROM files').fetchone()[0],
            'triggerCount': total, 'skillCount': len(rows), 'observedReads': total_reads,
            'unconfirmedReads': unconfirmed, 'maintenanceReads': excluded,
            'duplicateReads': total_reads - unconfirmed - excluded - total,
            'skills': skills, 'projectAttribution': projects}


def scan(db, codex_home, progress=False):
    paths = sorted({p for folder in ('sessions', 'archived_sessions')
                    for p in (codex_home / folder).rglob('rollout-*.jsonl*')
                    if p.name.endswith(('.jsonl', '.jsonl.zst'))})
    if not paths:
        raise ValueError('No rollout files found; existing statistics were preserved.')
    revision = db.execute("SELECT value FROM meta WHERE key='parser_revision'").fetchone()
    reindex = revision is None or revision[0] != PARSER_REVISION
    if reindex:
        # Retain observations until each replacement succeeds, including unreadable files.
        db.execute('DELETE FROM files')
        db.execute("INSERT OR REPLACE INTO meta VALUES ('parser_revision', ?)", (PARSER_REVISION,))
        db.commit()
    reconcile_turns(db)
    db.execute('DROP TABLE IF EXISTS temp.before_scan')
    db.execute('CREATE TEMP TABLE before_scan AS SELECT DISTINCT turn_key, skill FROM (' + ACCEPTED + ')')
    counts, errors = {}, []
    for index, path in enumerate(paths, 1):
        db.execute('SAVEPOINT one_file')
        try:
            status = scan_file(db, path)
            db.execute('RELEASE one_file')
            db.commit()
            counts[status] = counts.get(status, 0) + 1
        except (OSError, ValueError, RuntimeError) as error:
            db.execute('ROLLBACK TO one_file')
            db.execute('RELEASE one_file')
            errors.append({'file': str(path), 'error': str(error)})
        if progress and (index % 50 == 0 or index == len(paths)):
            print(f'Scanned {index}/{len(paths)} files; errors={len(errors)}', file=sys.stderr, flush=True)
    reconcile_turns(db)
    recovered, unavailable = recover_archived_locations(db, paths)
    index_projects(db)
    db.commit()
    result = summary(db)
    after = 'SELECT DISTINCT turn_key, skill FROM (' + ACCEPTED + ')'
    added = db.execute('SELECT COUNT(*) FROM (' + after + ' EXCEPT SELECT * FROM before_scan)').fetchone()[0]
    removed = db.execute('SELECT COUNT(*) FROM (SELECT * FROM before_scan EXCEPT ' + after + ')').fetchone()[0]
    result['scan'] = {**counts, 'discoveredFiles': len(paths), 'addedTriggers': added,
                      'removedTriggers': removed, 'reindexed': reindex,
                      'projectLocationsRecovered': recovered, 'projectLocationsUnavailable': unavailable,
                      'retainedMissingFiles': len({r[0] for r in db.execute('SELECT path FROM files')} - {str(p) for p in paths}),
                      'scanComplete': not errors, 'errors': errors}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['scan', 'summary'])
    parser.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', '~/.codex')).expanduser())
    parser.add_argument('--state', type=Path, required=True, help='Local private SQLite state, outside Git repositories')
    parser.add_argument('--progress', action='store_true')
    parser.add_argument('--compact', action='store_true', help='Omit detailed skill/project matrices from stdout')
    args = parser.parse_args()
    state = args.state.expanduser().resolve()
    state.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    # Serialize scans from concurrent chats, including their checkpoint updates.
    with state.with_suffix(state.suffix + '.lock').open('a') as lock:
        os.chmod(lock.name, 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX)
        db = connect(state)
        os.chmod(state, 0o600)
        try:
            result = scan(db, args.codex_home.expanduser().resolve(), args.progress) if args.action == 'scan' else summary(db)
            if args.compact:
                result.pop('skills', None)
                result['projectAttribution'].pop('projects', None)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1 if result.get('scan', {}).get('errors') else 0
        finally:
            db.close()


if __name__ == '__main__':
    sys.exit(main())
