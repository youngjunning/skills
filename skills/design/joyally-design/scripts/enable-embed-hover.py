#!/usr/bin/env python3
"""Enable Archify intent trace on node hover in a clean embedded viewer."""

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Verified Archify HTML")
    parser.add_argument("output", type=Path, help="Derived self-contained HTML")
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error("source and output must differ")

    content = args.source.read_text(encoding="utf-8")
    before = """      function blocked() {
        return html.getAttribute('data-embed') === 'true' ||
          html.getAttribute('data-guide-open') === 'true' ||"""
    after = """      function blocked() {
        // Keep semantic node hover available in the clean embedded canvas.
        return html.getAttribute('data-guide-open') === 'true' ||"""
    if content.count(before) != 1:
        parser.error("expected exactly one Archify intentTrace embed guard; inspect this viewer version")
    args.output.write_text(content.replace(before, after, 1), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
