#!/usr/bin/env python3
"""Keep private, searchable evidence screenshots from automated UI work."""

import argparse
from datetime import date, datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import urlsplit
from uuid import uuid4

from PIL import Image


DEFAULT_ROOT = Path.home() / ".joyally" / "spotlight"
FORMATS = {"PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp"}


def private_directory(path: Path) -> None:
    if path.is_symlink():
        raise ValueError(f"archive directory must not be a symlink: {path}")
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not path.is_dir():
        raise ValueError(f"archive path is not a directory: {path}")
    path.chmod(0o700)


def slug(value: str) -> str:
    return re.sub(r"[_\W]+", "-", value.lower(), flags=re.UNICODE).strip("-")[:40] or "capture"


def image_format(path: Path) -> tuple[str, int, int]:
    with Image.open(path) as image:
        fmt = image.format
        size = image.size
        image.verify()
    if fmt not in FORMATS:
        raise ValueError("screenshot must be PNG, JPEG, or WebP")
    return FORMATS[fmt], *size


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def save(args: argparse.Namespace) -> dict:
    source = args.input.expanduser().resolve(strict=True)
    if not source.is_file():
        raise ValueError("input must be a screenshot file")
    extension, width, height = image_format(source)
    if args.url and (urlsplit(args.url).query or urlsplit(args.url).fragment):
        raise ValueError("source URL must omit query and fragment")
    root = args.root.expanduser()
    if root == DEFAULT_ROOT:
        private_directory(root.parent)
    private_directory(root)
    now = datetime.now().astimezone()
    captured_at = args.captured_at.strip() or now.isoformat(timespec="microseconds")
    try:
        date.fromisoformat(captured_at[:10])
        if len(captured_at) > 10:
            datetime.fromisoformat(captured_at)
    except ValueError as error:
        raise ValueError("captured-at must be an ISO date or date-time") from error
    folder = root / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d")
    for directory in (folder.parent.parent, folder.parent, folder):
        private_directory(directory)
    name = f"{now.strftime('%Y%m%dT%H%M%S%f')}-{slug(args.project)}-{slug(args.step)}-{uuid4().hex[:8]}"
    target = folder / f"{name}{extension}"
    sidecar = folder / f"{name}.json"
    sha256 = digest(source)
    record = {
        "version": 1,
        "captured_at": captured_at,
        "archived_at": now.isoformat(timespec="microseconds"),
        "project": args.project.strip(),
        "task": args.task.strip(),
        "step": args.step.strip(),
        "environment": args.environment.strip(),
        "outcome": args.outcome,
        "source_url": args.url.strip(),
        "note": args.note.strip(),
        "privacy": "private; review before sharing",
        "image": str(target),
        "width": width,
        "height": height,
        "sha256": sha256,
    }
    try:
        with os.fdopen(os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as output:
            with source.open("rb") as original:
                shutil.copyfileobj(original, output)
        with os.fdopen(os.open(sidecar, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w", encoding="utf-8") as output:
            json.dump(record, output, ensure_ascii=False, indent=2)
            output.write("\n")
    except BaseException:
        target.unlink(missing_ok=True)
        sidecar.unlink(missing_ok=True)
        raise
    return record


def find(args: argparse.Namespace) -> list[dict]:
    root = args.root.expanduser()
    if not root.exists():
        return []
    if root.is_symlink() or not root.is_dir():
        raise ValueError("archive root must be a directory, not a symlink")
    since = date.fromisoformat(args.since) if args.since else None
    matches = []
    for sidecar in root.glob("[0-9][0-9][0-9][0-9]/*/*/*.json"):
        try:
            record = json.loads(sidecar.read_text(encoding="utf-8"))
            image = Path(record["image"])
            if not image.is_file() or image.parent != sidecar.parent or image.stem != sidecar.stem:
                continue
            if args.project and args.project.casefold() not in record["project"].casefold():
                continue
            if args.task and args.task.casefold() not in record["task"].casefold():
                continue
            if since and date.fromisoformat(record["captured_at"][:10]) < since:
                continue
            if args.query and args.query.casefold() not in " ".join(str(record.get(field, "")) for field in ("project", "task", "step", "environment", "outcome", "note", "source_url")).casefold():
                continue
            if args.verify and digest(image) != record["sha256"]:
                print(f"hash mismatch: {image}", file=sys.stderr)
                continue
            matches.append(record)
        except (OSError, ValueError, KeyError, TypeError) as error:
            print(f"skipping invalid screenshot record {sidecar}: {error}", file=sys.stderr)
    matches.sort(key=lambda record: record.get("archived_at", record["captured_at"]), reverse=True)
    return matches[: args.limit]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="private archive root")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("save", help="archive one observed screenshot")
    add.add_argument("--input", required=True, type=Path)
    add.add_argument("--project", required=True)
    add.add_argument("--task", required=True)
    add.add_argument("--step", required=True)
    add.add_argument("--environment", default="")
    add.add_argument("--captured-at", default="", help="original ISO capture date/time for older images")
    add.add_argument("--outcome", choices=("before", "success", "failure", "pending"), required=True)
    add.add_argument("--url", default="")
    add.add_argument("--note", default="")
    search = sub.add_parser("find", help="find screenshots for a future article")
    search.add_argument("--project", default="")
    search.add_argument("--task", default="")
    search.add_argument("--query", default="")
    search.add_argument("--since", default="", help="YYYY-MM-DD")
    search.add_argument("--limit", type=int, default=20)
    search.add_argument("--verify", action="store_true", help="check stored SHA-256")
    search.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "save":
            if not all((args.project.strip(), args.task.strip(), args.step.strip())):
                raise ValueError("project, task, and step must be nonempty")
            print(json.dumps(save(args), ensure_ascii=False, indent=2))
        else:
            if args.limit < 1:
                raise ValueError("limit must be positive")
            records = find(args)
            if args.json:
                print(json.dumps(records, ensure_ascii=False, indent=2))
            else:
                for record in records:
                    print(f"{record['captured_at']}  {record['project']}  {record['task']}  {record['step']}  {record['outcome']}\n  {record['image']}")
        return 0
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
