#!/usr/bin/env python3
"""Check and merge a newer Joyally Design source archive without losing local edits."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "UPSTREAM_SYNC.json"
TEXT_SUFFIXES = {".md", ".html", ".css", ".js", ".mjs", ".json", ".py", ".sh", ".txt"}
MANUAL = {"DESIGN_PROCESS.md", "assets/style-explorer.html",
          "references/media.md", "references/image-ideation.md",
          "references/scroll-narrative.md", "references/tools.md"}
MANUAL_PREFIXES = ("assets/cards/", "scripts/", "tests/")
SKIPPED = {"README.md", "README.en.md", ".gitignore",
           "scripts/check_update.py", "scripts/check_update.sh",
           "tests/test_check_update.py", "scripts/oiloil-image.mjs",
           "tests/test_oiloil_image.py"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def destination(relative: str) -> str | None:
    if relative in SKIPPED or relative.startswith("adapters/dsh/"):
        return None
    if relative == "SKILL.md":
        return "DESIGN_PROCESS.md"
    if relative == "references/visual-language.md":
        return "references/visual-craft.md"
    if relative.startswith(("references/", "scripts/", "assets/", "tests/", "adapters/")):
        return relative
    return None


def transformed(relative: str, raw: bytes, source_name: str) -> bytes:
    if PurePosixPath(relative).suffix not in TEXT_SUFFIXES:
        return raw
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw
    parts = source_name.split("-")
    provider = parts[0]
    short = "-".join(parts[:2])
    display = f"{parts[0].capitalize()} {parts[1].upper()}" if len(parts) > 1 else provider.capitalize()
    replacements = (
        (display + " " + parts[2].capitalize(), "Joyally Design") if len(parts) > 2 else ("", ""),
        (source_name, "joyally-design"),
        (provider + "-" + provider, "youngjunning"),
        (display, "Joyally Design"),
        (short, "joyally-design"),
        ((provider * 2).capitalize(), "Joyally"),
        (provider * 2, "joyally"),
        (short.replace("-", "_").upper(), "JOYALLY"),
        (short.replace("-", "_"), "joyally"),
        (provider.upper() + "_", "JOYALLY_"),
    )
    for before, after in replacements:
        if not before:
            continue
        content = content.replace(before, after)
    return content.encode("utf-8")


def entries(archive: Path) -> dict[str, tuple[str, bytes]]:
    result: dict[str, tuple[str, bytes]] = {}
    with ZipFile(archive) as bundle:
        files = [item for item in bundle.infolist() if not item.is_dir()]
        roots = {PurePosixPath(item.filename).parts[0] for item in files}
        if len(roots) != 1:
            raise ValueError("Archive must have one top-level directory")
        source_name = next(iter(roots))
        for item in files:
            parts = PurePosixPath(item.filename).parts
            if len(parts) < 2 or ".." in parts or item.filename.startswith("/"):
                raise ValueError("Archive contains an unsafe path")
            relative = PurePosixPath(*parts[1:]).as_posix()
            dest = destination(relative)
            if dest is None:
                continue
            if dest in result:
                raise ValueError(f"Archive maps more than one file to {dest}")
            result[dest] = (digest(bundle.read(item)), transformed(relative, bundle.read(item), source_name))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report source changes and local conflicts")
    mode.add_argument("--apply", action="store_true", help="merge safe changes and update the manifest")
    mode.add_argument("--manifest", action="store_true", help="print initial manifest for reviewed import")
    args = parser.parse_args()
    try:
        current = entries(args.archive)
        previous = json.loads(MANIFEST.read_text("utf-8"))["files"] if MANIFEST.exists() else {}
    except (OSError, ValueError, KeyError) as error:
        print(f"Cannot read source archive or manifest: {error}", file=sys.stderr)
        return 2
    if args.manifest:
        files = {}
        for dest, (source_hash, _) in sorted(current.items()):
            target = ROOT / dest
            if not target.is_file():
                print(f"Missing imported file: {dest}", file=sys.stderr)
                return 2
            files[dest] = {"source_sha256": source_hash,
                           "local_sha256": digest(target.read_bytes())}
        print(json.dumps({"format": 1, "files": files}, ensure_ascii=False, indent=2))
        return 0

    changed = conflicts = 0
    next_files = dict(previous)
    for dest, (source_hash, content) in sorted(current.items()):
        target = ROOT / dest
        prior = previous.get(dest)
        source_changed = prior is None or prior["source_sha256"] != source_hash
        if not source_changed:
            continue
        changed += 1
        local_hash = digest(target.read_bytes()) if target.is_file() else None
        local_changed = prior is not None and local_hash != prior["local_sha256"]
        if (dest in MANUAL or dest.startswith(MANUAL_PREFIXES)
                or local_changed or (prior is None and target.exists())):
            conflicts += 1
            print(f"REVIEW {dest}: source changed; keep local version")
            continue
        print(f"UPDATE {dest}")
        if args.apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            next_files[dest] = {"source_sha256": source_hash,
                                "local_sha256": digest(content)}
    removed = sorted(set(previous) - set(current))
    for dest in removed:
        print(f"REVIEW {dest}: no longer in source archive; keep local version")
        conflicts += 1
    if args.apply:
        MANIFEST.write_text(json.dumps({"format": 1, "files": next_files},
                                       ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(f"Checked {len(current)} mapped files; {changed} changed, {conflicts} need review.")
    return 1 if conflicts else 0


if __name__ == "__main__":
    raise SystemExit(main())
