#!/usr/bin/env python3
"""Read bounded conversation excerpts; never modifies sessions or personal records."""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import re
import sys


def clean_user(text):
    text = re.sub(r'<in-app-browser-context\b[^>]*>[\s\S]*?</in-app-browser-context>', '', text)
    text = re.sub(r'<external_codex_apps_open_page>[\s\S]*?</external_codex_apps_open_page>', '', text)
    text = text.strip()
    if not text or text.startswith(('# AGENTS.md instructions', '<environment_context>', '<permissions instructions>')):
        return ''
    if text.startswith('<send_user_message_question_reply>'):
        try:
            rows = json.loads(re.sub(r'</?send_user_message_question_reply>', '', text).strip())
            return '\n'.join(f"问题：{row['question']}\n本人回复：{row['answer']}" for row in rows)
        except (ValueError, TypeError, KeyError):
            return text
    if '## My request:' in text:
        text = text.split('## My request:', 1)[1].strip()
    return text


def excerpt(filename, match=None, before=2, after=2, tail=12, max_hits=5):
    metadata = {}
    selected = {}
    previous = deque(maxlen=before)
    recent = deque(maxlen=tail)
    remaining = 0
    total = hits = matches_seen = 0
    with Path(filename).open(encoding='utf-8') as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = row.get('payload', {})
            if row.get('type') == 'session_meta':
                metadata = {key: payload.get(key) for key in ['id', 'cwd', 'timestamp']}
                continue
            if row.get('type') != 'response_item' or payload.get('type') != 'message':
                continue
            role = payload.get('role')
            if role not in ['user', 'assistant']:
                continue
            if role == 'assistant' and payload.get('channel') in ['analysis', 'summary']:
                continue
            text = '\n'.join(part.get('text', '') for part in payload.get('content', [])
                             if part.get('type') in ['input_text', 'output_text'])
            text = clean_user(text) if role == 'user' else text.strip()
            if not text:
                continue
            total += 1
            message = {'line': line_number, 'timestamp': row.get('timestamp'), 'role': role,
                       'text': text, 'sha256': hashlib.sha256(text.encode()).hexdigest()}
            recent.append(message)
            hit = match is not None and match in text
            if hit:
                matches_seen += 1
            if hit and hits < max_hits:
                hits += 1
                for old in previous:
                    selected[old['line']] = old
                selected[line_number] = message
                remaining = after
            elif remaining:
                selected[line_number] = message
                remaining -= 1
            previous.append(message)
    messages = sorted(selected.values(), key=lambda row: row['line']) if match is not None else list(recent)
    return {'session_file': str(Path(filename).resolve()), 'session': metadata,
            'matching_messages': matches_seen, 'selected_matches': hits,
            'truncated': matches_seen > max_hits,
            'eligible_messages': total, 'messages': messages}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', required=True, type=Path)
    parser.add_argument('--match')
    parser.add_argument('--before', type=int, default=2)
    parser.add_argument('--after', type=int, default=2)
    parser.add_argument('--tail', type=int, default=12)
    parser.add_argument('--max-hits', type=int, default=5)
    args = parser.parse_args()
    if any(value < 0 or value > 50 for value in [args.before, args.after, args.tail]):
        parser.error('before, after and tail must be between 0 and 50')
    if args.max_hits < 1 or args.max_hits > 20:
        parser.error('max-hits must be between 1 and 20')
    result = excerpt(args.session, args.match, args.before, args.after, args.tail, args.max_hits)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if args.match is not None and result['matching_messages'] == 0 else 0


if __name__ == '__main__':
    sys.exit(main())
