#!/usr/bin/env python3
"""Validate Qingshan Lake Light/Dark image tokens and text contrast."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKEN_FILE = ROOT / "assets" / "qingshan-lake-image.tokens.json"
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
REQUIRED = {
    "canvas",
    "surface",
    "surfaceMuted",
    "text",
    "textSecondary",
    "primary",
    "primaryStrong",
    "primaryContainer",
    "success",
    "warning",
    "error",
    "border",
}


def luminance(color: str) -> float:
    channels = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
        for value in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(left: str, right: str) -> float:
    high, low = sorted((luminance(left), luminance(right)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def main() -> int:
    document = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
    modes = document.get("mode")
    if not isinstance(modes, dict) or set(modes) != {"light", "dark"}:
        raise ValueError("mode must define exactly light and dark")
    if document.get("defaultMode") != "light":
        raise ValueError("defaultMode must remain light")

    checked_pairs = 0
    for mode_name, tokens in modes.items():
        missing = REQUIRED - tokens.keys()
        if missing:
            raise ValueError(f"{mode_name} missing tokens: {', '.join(sorted(missing))}")
        invalid = [name for name, value in tokens.items() if not HEX.fullmatch(value)]
        if invalid:
            raise ValueError(f"{mode_name} invalid colors: {', '.join(sorted(invalid))}")
        if tokens["canvas"].upper() in {"#FFFFFF", "#000000"}:
            raise ValueError(f"{mode_name} canvas must not be pure white or pure black")

        for foreground in ("text", "textSecondary"):
            for background in ("canvas", "surface"):
                ratio = contrast(tokens[foreground], tokens[background])
                if ratio < 4.5:
                    raise ValueError(
                        f"{mode_name} {foreground}/{background} contrast is {ratio:.2f}:1"
                    )
                checked_pairs += 1

    print(f"validated Light/Dark modes, {len(REQUIRED)} tokens each, {checked_pairs} contrast pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
