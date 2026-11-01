#!/usr/bin/env python3
"""Link this checkout into one explicitly selected Agent skill directory."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def install(sources, dest, *, replace=False, dry_run=False, backup_root=None):
    dest = Path(dest).expanduser().resolve()
    if dest == ROOT or ROOT in dest.parents:
        raise ValueError('The destination must be outside the source checkout.')
    actions = []
    for name, source in sources:
        source = Path(source).resolve()
        if not (source / 'SKILL.md').is_file():
            raise ValueError(f'Missing skill entry: {source}')
        target = dest / name
        if target.is_symlink() and target.resolve() == source:
            actions.append((name, source, target, 'unchanged'))
        elif target.exists() or target.is_symlink():
            if not replace:
                raise ValueError(f'Existing install: {target}; use --replace to back it up first.')
            actions.append((name, source, target, 'backup + link'))
        else:
            actions.append((name, source, target, 'link'))
    # Finish every preflight check before changing any installation.
    if dry_run:
        return [(name, action) for name, _, _, action in actions]
    backup = None
    for name, source, target, action in actions:
        if action == 'unchanged':
            continue
        dest.mkdir(parents=True, exist_ok=True)
        if action == 'backup + link':
            if backup is None:
                base = Path(backup_root or Path.home() / '.local/share/youngjunning-skills/backups')
                base.mkdir(parents=True, exist_ok=True)
                import tempfile
                stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-')
                backup = Path(tempfile.mkdtemp(prefix=stamp, dir=base))
            shutil.move(str(target), str(backup / name))
        try:
            target.symlink_to(source, target_is_directory=True)
        except OSError:
            if action == 'backup + link' and not target.exists() and not target.is_symlink():
                shutil.move(str(backup / name), str(target))
            raise
    if backup:
        print(f'Backup: {backup}')
    return [(name, action) for name, _, _, action in actions]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, required=True)
    parser.add_argument('--replace', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    sources = [(item['name'], ROOT / item['path']) for item in catalog]
    try:
        for name, action in install(sources, args.dest, replace=args.replace, dry_run=args.dry_run):
            print(f'{name}: {action}')
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
