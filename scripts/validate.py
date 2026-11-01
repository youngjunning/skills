#!/usr/bin/env python3
"""Check the public skill catalog, local references, and disclosure boundaries."""
import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '__pycache__', '.venv', 'node_modules'}
PATTERNS = {
    'personal absolute path': re.compile('/' + r'Users/[^/\s]+/'),
    'internal host': re.compile(r'\b(?:[\w-]+\.)*(?:alibaba-inc|aliway|fliggy)\.com\b'),
    'credential': re.compile(r'\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]{30,})\b'),
    'private key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'live ad account': re.compile(r'ca-pub-\d{10,}|div-gpt-ad-\d{10,}'),
    'live pixel config': re.compile(r"(?:fbq\(['\"]init['\"],\s*['\"]|Pixel\s+[`'\"]?)\d{12,}"),
}


def validate(root=ROOT):
    errors = []
    catalog = json.loads((root / 'catalog.json').read_text())
    names, paths = set(), set()
    for item in catalog:
        name, path = item['name'], item['path']
        if name in names or path in paths:
            errors.append(f'duplicate catalog entry: {name}')
        names.add(name)
        paths.add(path)
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            errors.append(f'invalid skill name: {name}')
        if path != f"skills/{item['category']}/{name}":
            errors.append(f'category/path mismatch: {path}')
        entry = root / path / 'SKILL.md'
        if not entry.is_file():
            errors.append(f'missing entry: {entry}')
            continue
        text = entry.read_text()
        front = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
        if not front or not re.search(r'^name:\s*' + re.escape(name) + r'\s*$', front[1], re.M):
            errors.append(f'frontmatter name mismatch: {path}')
        if not front or not re.search(r'^description:\s*\S', front[1], re.M):
            errors.append(f'missing description: {path}')
        for target in re.findall(r'\]\(([^\s)]+)\)', text):
            if target.startswith(('#', '~', '/')) or '://' in target or '<' in target:
                continue
            local = (entry.parent / unquote(target.split('#')[0])).resolve()
            if not local.exists():
                errors.append(f'broken entry link: {path}: {target}')
    found = {str(p.parent.relative_to(root)) for p in (root / 'skills').glob('*/*/SKILL.md')}
    if paths != found:
        errors.append(f'catalog differs from skill tree: {sorted(paths ^ found)}')
    readme = (root / 'README.md').read_text()
    for path in paths:
        if path + '/SKILL.md' not in readme:
            errors.append(f'missing README catalog link: {path}')
    for p in root.rglob('*'):
        rel = p.relative_to(root)
        if any(part in SKIP for part in rel.parts):
            continue
        if p.is_symlink():
            errors.append(f'public source contains symlink: {rel}')
            continue
        if not p.is_file():
            continue
        if p.name == '.env' or p.name.startswith('.env.') and p.name != '.env.example':
            errors.append(f'environment file in source: {rel}')
        if '.bak' in p.name:
            errors.append(f'backup in source: {rel}')
        try:
            text = p.read_text()
        except UnicodeError:
            continue
        for label, pattern in PATTERNS.items():
            match = pattern.search(text)
            if match:
                line = text.count('\n', 0, match.start()) + 1
                errors.append(f'{label}: {rel}:{line}')
        if re.search(r'git (?:clone|submodule add) https://github\.com/[^/\s]+/[^/\s]+/tree/', text):
            errors.append(f'Git command uses a web directory URL: {rel}')
        if p.suffix == '.json':
            try:
                json.loads(text)
            except ValueError as error:
                errors.append(f'invalid JSON: {rel}: {error}')
        if p.suffix == '.py':
            try:
                ast.parse(text, filename=str(rel))
            except SyntaxError as error:
                errors.append(f'invalid Python: {rel}: {error}')
    return errors


if __name__ == '__main__':
    problems = validate()
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        sys.exit(1)
    count = len(json.loads((ROOT / 'catalog.json').read_text()))
    print(f'Validated {count} public skills, catalog, entry links, Python/JSON, and disclosure patterns.')
