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

VERSION = 1
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
        CREATE INDEX IF NOT EXISTS observation_turn ON observations(turn_key, skill);
        CREATE INDEX IF NOT EXISTS observation_call ON observations(call_id, skill);
        CREATE INDEX IF NOT EXISTS excluded_turn ON excluded_turns(turn_key);
    ''')
    old = db.execute("SELECT value FROM meta WHERE key='version'").fetchone()
    if old and old[0] != str(VERSION):
        raise ValueError('Unsupported state version; use a separate state database for a rebuild.')
    db.execute("INSERT OR IGNORE INTO meta VALUES ('version', ?)", (str(VERSION),))
    db.commit()
    return db


@contextmanager
def source(path):
    if path.name.endswith('.zst'):
        if not shutil.which('zstd'):
            raise RuntimeError('zstd is required for compressed rollouts')
        process = subprocess.Popen(['zstd', '-q', '-d', '-c', '--', str(path)], stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL)
        try:
            yield process.stdout
            if process.wait() != 0:
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
                                'timestamp': row.get('timestamp'), 'line': line}
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
            db.execute('INSERT OR REPLACE INTO observations VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (filename, call_id, skill, call.get('turn'), call['timestamp'], call['line'], status))


def scan_file(db, path):
    filename = str(path)
    stat = path.stat()
    old = db.execute('SELECT size, mtime, offset, line, boundary, context FROM files WHERE path=?',
                     (filename,)).fetchone()
    if old and old[:2] == (stat.st_size, stat.st_mtime_ns):
        return 'unchanged'
    compressed = path.name.endswith('.zst')
    resume = bool(old and not compressed and (stat.st_size > old[2] or old[0] == -1)
                  and boundary(path, old[2]) == old[4])
    offset, line = (old[2], old[3]) if resume else (0, 0)
    context = json.loads(old[5]) if resume else {}
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


ACCEPTED = '''SELECT turn_key, skill, timestamp FROM (
        SELECT o.turn_key, o.skill, o.timestamp,
               ROW_NUMBER() OVER (PARTITION BY o.call_id, o.skill ORDER BY o.timestamp, o.turn_key) AS occurrence
        FROM observations o WHERE o.status='verified' AND NOT EXISTS
        (SELECT 1 FROM observations copy JOIN excluded_turns e ON e.turn_key=copy.turn_key
         WHERE copy.call_id=o.call_id AND copy.skill=o.skill)) WHERE occurrence=1'''


def summary(db):
    rows = db.execute('''SELECT skill, COUNT(*), MIN(first_seen), MAX(last_seen) FROM
        (SELECT skill, turn_key, MIN(timestamp) first_seen, MAX(timestamp) last_seen
         FROM (''' + ACCEPTED + ''') GROUP BY skill, turn_key)
        GROUP BY skill ORDER BY COUNT(*) DESC, skill''').fetchall()
    total_reads = db.execute('SELECT COUNT(*) FROM observations').fetchone()[0]
    unconfirmed = db.execute("SELECT COUNT(*) FROM observations WHERE status!='verified'").fetchone()[0]
    excluded = db.execute('''SELECT COUNT(*) FROM observations o WHERE status='verified' AND EXISTS
        (SELECT 1 FROM observations copy JOIN excluded_turns e ON e.turn_key=copy.turn_key
         WHERE copy.call_id=o.call_id AND copy.skill=o.skill)''').fetchone()[0]
    total = sum(row[1] for row in rows)
    return {'version': VERSION, 'metric': 'verified_skill_read_turns', 'complete': False,
            'coverage': 'Locally retained rollouts only; verified loads are not workflow successes.',
            'files': db.execute('SELECT COUNT(*) FROM files').fetchone()[0],
            'triggerCount': total, 'skillCount': len(rows), 'observedReads': total_reads,
            'unconfirmedReads': unconfirmed, 'maintenanceReads': excluded,
            'duplicateReads': total_reads - unconfirmed - excluded - total,
            'skills': [{'name': r[0], 'triggerCount': r[1], 'firstSeen': r[2], 'lastSeen': r[3]}
                       for r in rows]}


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
    result = summary(db)
    after = 'SELECT DISTINCT turn_key, skill FROM (' + ACCEPTED + ')'
    added = db.execute('SELECT COUNT(*) FROM (' + after + ' EXCEPT SELECT * FROM before_scan)').fetchone()[0]
    removed = db.execute('SELECT COUNT(*) FROM (SELECT * FROM before_scan EXCEPT ' + after + ')').fetchone()[0]
    result['scan'] = {**counts, 'discoveredFiles': len(paths), 'addedTriggers': added,
                      'removedTriggers': removed, 'reindexed': reindex,
                      'scanComplete': not errors, 'errors': errors}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['scan', 'summary'])
    parser.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', '~/.codex')).expanduser())
    parser.add_argument('--state', type=Path, required=True, help='Local private SQLite state, outside Git repositories')
    parser.add_argument('--progress', action='store_true')
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
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1 if result.get('scan', {}).get('errors') else 0
        finally:
            db.close()


if __name__ == '__main__':
    sys.exit(main())
