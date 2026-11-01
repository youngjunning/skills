#!/usr/bin/env python3
"""Validate the bundled Qingshan token file and declared contrast pairs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKEN_FILE = ROOT / "assets" / "qingshan.tokens.json"
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
REFERENCE = re.compile(r"^\{([a-zA-Z0-9_.]+)\}$")
REQUIRED_SEMANTIC = {
    "background",
    "surface",
    "text",
    "textSecondary",
    "primaryAction",
    "onPrimaryAction",
    "success",
    "warning",
    "error",
    "focus",
    "darkBackground",
    "onDark",
}


def resolve_path(document: dict, dotted: str) -> object:
    current: object = document
    for key in dotted.split("."):
        if not isinstance(current, dict) or key not in current:
            raise KeyError(dotted)
        current = current[key]
    return current


def resolve_color(document: dict, dotted: str) -> str:
    value = resolve_path(document, dotted)
    seen = {dotted}
    while isinstance(value, str) and (match := REFERENCE.fullmatch(value)):
        target = match.group(1)
        if target in seen:
            raise ValueError(f"cyclic token reference: {target}")
        seen.add(target)
        value = resolve_path(document, target)
    if not isinstance(value, str) or not HEX.fullmatch(value):
        raise ValueError(f"{dotted} does not resolve to a six-digit hex color")
    return value.upper()


def relative_luminance(hex_color: str) -> float:
    channels = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(left: str, right: str) -> float:
    high, low = sorted((relative_luminance(left), relative_luminance(right)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def main() -> int:
    document = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
    errors: list[str] = []

    semantic = document.get("semantic")
    if not isinstance(semantic, dict):
        errors.append("semantic must be an object")
    else:
        missing = sorted(REQUIRED_SEMANTIC - semantic.keys())
        if missing:
            errors.append(f"missing semantic roles: {', '.join(missing)}")

    for group_name in ("color", "semantic"):
        group = document.get(group_name, {})
        if not isinstance(group, dict):
            errors.append(f"{group_name} must be an object")
            continue
        for key in group:
            try:
                resolve_color(document, f"{group_name}.{key}")
            except (KeyError, ValueError) as error:
                errors.append(str(error))

    passed_pairs = 0
    for index, pair in enumerate(document.get("contrastPairs", []), start=1):
        try:
            foreground_name = pair["foreground"]
            background_name = pair["background"]
            minimum = float(pair["minimum"])
            foreground = resolve_color(document, foreground_name)
            background = resolve_color(document, background_name)
            ratio = contrast(foreground, background)
            if ratio + 1e-9 < minimum:
                errors.append(
                    f"contrast pair {index} fails: {foreground_name} on {background_name} "
                    f"is {ratio:.2f}:1, expected {minimum:.2f}:1"
                )
            else:
                passed_pairs += 1
        except (KeyError, TypeError, ValueError) as error:
            errors.append(f"invalid contrast pair {index}: {error}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"validated {len(document['color'])} colors, {len(document['semantic'])} semantic roles, {passed_pairs} contrast pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
