#!/usr/bin/env python3
"""Regression tests for deterministic SVG connector and divider geometry."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_svg_layout.py")


def svg(*, shaft_end: int = 290, approach_y: int = 130, penultimate_y: int = 130, arrow_y: int = 130, arrow_fill: str = "#468b84", divider_y: int = 250) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300">
  <rect x="10" y="100" width="100" height="60" data-layout-node="source"/>
  <rect x="330" y="100" width="100" height="60" data-layout-node="target"/>
  <rect x="10" y="{divider_y}" width="420" height="1" data-layout-divider="footer-divider"/>
  <path d="M 120 130 L 270 {approach_y} L 280 {penultimate_y} L {shaft_end} 130" stroke="#468b84" stroke-width="4" stroke-linecap="butt"
    data-layout-edge="source-target" data-from="source" data-to="target" data-flow="right"/>
  <path d="M 290 {arrow_y - 8} L 300 {arrow_y} L 290 {arrow_y + 8} Z" fill="{arrow_fill}"
    data-arrow-for="source-target"/>
</svg>"""


class ValidateSvgLayoutTests(unittest.TestCase):
    def run_case(self, source: str) -> tuple[int, dict[str, object]]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "diagram.svg"
            path.write_text(source, encoding="utf-8")
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    str(path),
                    "--edge-clearance",
                    "0",
                    "--divider-node-clearance",
                    "16",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            return result.returncode, json.loads(result.stdout)

    def assert_error(self, report: dict[str, object], expected: str) -> None:
        errors = report["errors"]
        self.assertIn(expected, {error["type"] for error in errors})

    def test_valid_arrow_join_and_divider_clearance(self) -> None:
        code, report = self.run_case(svg())
        self.assertEqual(0, code, report)

    def test_arrow_shaft_overlap_is_rejected(self) -> None:
        code, report = self.run_case(svg(shaft_end=300))
        self.assertEqual(1, code)
        self.assert_error(report, "arrow-shaft-overlap")

    def test_arrow_centerline_misalignment_is_rejected(self) -> None:
        code, report = self.run_case(svg(arrow_y=136))
        self.assertEqual(1, code)
        self.assert_error(report, "arrow-shaft-misaligned")

    def test_arrow_terminal_tangent_misalignment_is_rejected(self) -> None:
        code, report = self.run_case(svg(penultimate_y=120))
        self.assertEqual(1, code)
        self.assert_error(report, "arrow-tangent-misaligned")

    def test_arrow_hidden_kink_before_short_tail_is_rejected(self) -> None:
        code, report = self.run_case(svg(approach_y=120))
        self.assertEqual(1, code)
        self.assert_error(report, "arrow-tangent-misaligned")

    def test_orthogonal_elbow_with_long_straight_tail_is_valid(self) -> None:
        source = svg().replace(
            'M 120 130 L 270 130 L 280 130 L 290 130',
            'M 120 130 H 170 V 65 H 220 V 130 H 290',
        )
        code, report = self.run_case(source)
        self.assertEqual(0, code, report)

    def test_arrow_color_mismatch_is_rejected(self) -> None:
        code, report = self.run_case(svg(arrow_fill="#ad6a61"))
        self.assertEqual(1, code)
        self.assert_error(report, "arrow-color-mismatch")

    def test_divider_crossing_node_is_rejected(self) -> None:
        code, report = self.run_case(svg(divider_y=155))
        self.assertEqual(1, code)
        self.assert_error(report, "divider-node-clearance")


if __name__ == "__main__":
    unittest.main()
