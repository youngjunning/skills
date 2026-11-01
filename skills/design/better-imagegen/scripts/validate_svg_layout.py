#!/usr/bin/env python3
"""Validate straight-line deterministic SVG diagrams without launching a browser."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rect:
    left: float
    top: float
    right: float
    bottom: float


def number(element: ET.Element, name: str) -> float:
    return float(element.attrib.get(name, "0"))


def rect_of(element: ET.Element) -> Rect:
    x, y = number(element, "x"), number(element, "y")
    return Rect(x, y, x + number(element, "width"), y + number(element, "height"))


def path_points(data: str) -> list[tuple[float, float]]:
    tokens = re.findall(r"[MLHVZmlhvz]|-?(?:\d+(?:\.\d*)?|\.\d+)", data)
    points: list[tuple[float, float]] = []
    x = y = 0.0
    index = 0
    command = ""
    while index < len(tokens):
        token = tokens[index]
        if token.isalpha():
            command = token.upper()
            index += 1
            if command == "Z":
                continue
        if command in {"M", "L"}:
            x, y = float(tokens[index]), float(tokens[index + 1])
            index += 2
        elif command == "H":
            x = float(tokens[index])
            index += 1
        elif command == "V":
            y = float(tokens[index])
            index += 1
        else:
            raise ValueError(f"unsupported SVG path command in {data!r}")
        points.append((x, y))
    if len(points) < 2:
        raise ValueError(f"path needs at least two points: {data!r}")
    return points


def point_distance_to_rect(point: tuple[float, float], rect: Rect) -> float:
    x, y = point
    dx = max(rect.left - x, 0, x - rect.right)
    dy = max(rect.top - y, 0, y - rect.bottom)
    return math.hypot(dx, dy)


def intersects(a: Rect, b: Rect) -> bool:
    return min(a.right, b.right) > max(a.left, b.left) and min(a.bottom, b.bottom) > max(a.top, b.top)


def expanded(rect: Rect, amount: float) -> Rect:
    return Rect(rect.left - amount, rect.top - amount, rect.right + amount, rect.bottom + amount)


def style_value(element: ET.Element, name: str, default: str) -> str:
    if name in element.attrib:
        return element.attrib[name]
    style = dict(
        part.split(":", 1) for part in element.attrib.get("style", "").split(";") if ":" in part
    )
    return style.get(name, default).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("svg")
    parser.add_argument("--min-gap", type=float, default=24)
    parser.add_argument("--edge-clearance", type=float, default=12)
    parser.add_argument("--arrow-clearance", type=float, default=12)
    parser.add_argument("--arrow-join-tolerance", type=float, default=2)
    parser.add_argument("--arrow-tangent-tolerance", type=float, default=8)
    parser.add_argument("--arrow-shaft-tolerance", type=float, default=0.25)
    parser.add_argument("--label-clearance", type=float, default=8)
    parser.add_argument("--divider-node-clearance", type=float, default=16)
    args = parser.parse_args()

    root = ET.parse(args.svg).getroot()
    viewbox = [float(value) for value in root.attrib.get("viewBox", "0 0 0 0").split()]
    if len(viewbox) != 4 or viewbox[2] <= 0 or viewbox[3] <= 0:
        raise SystemExit("invalid or missing viewBox")
    _, _, width, height = viewbox
    errors: list[dict[str, object]] = []
    nodes = {element.attrib["data-layout-node"]: rect_of(element) for element in root.iter() if "data-layout-node" in element.attrib}
    labels = {element.attrib["data-layout-label"]: rect_of(element) for element in root.iter() if "data-layout-label" in element.attrib}
    dividers = {element.attrib["data-layout-divider"]: rect_of(element) for element in root.iter() if "data-layout-divider" in element.attrib}
    edges = [element for element in root.iter() if "data-layout-edge" in element.attrib]
    arrows = {element.attrib["data-arrow-for"]: (element, path_points(element.attrib.get("d", ""))) for element in root.iter() if "data-arrow-for" in element.attrib}

    for name, rect in {**nodes, **labels}.items():
        if rect.left < 0 or rect.top < 0 or rect.right > width or rect.bottom > height:
            errors.append({"type": "canvas-overflow", "element": name})

    node_items = list(nodes.items())
    for index, (name_a, a) in enumerate(node_items):
        for name_b, b in node_items[index + 1 :]:
            if intersects(a, b):
                errors.append({"type": "node-overlap", "elements": [name_a, name_b]})
                continue
            x_overlap = min(a.right, b.right) - max(a.left, b.left)
            y_overlap = min(a.bottom, b.bottom) - max(a.top, b.top)
            horizontal_gap = max(b.left - a.right, a.left - b.right, 0)
            vertical_gap = max(b.top - a.bottom, a.top - b.bottom, 0)
            if y_overlap > 0 and horizontal_gap < args.min_gap:
                errors.append({"type": "node-gap", "elements": [name_a, name_b], "actual": horizontal_gap})
            elif x_overlap > 0 and vertical_gap < args.min_gap:
                errors.append({"type": "node-gap", "elements": [name_a, name_b], "actual": vertical_gap})

    for label_name, label in labels.items():
        for node_name, node in nodes.items():
            if intersects(expanded(label, args.label_clearance), node):
                errors.append({"type": "label-node-clearance", "elements": [label_name, node_name]})

    for divider_name, divider in dividers.items():
        for node_name, node in nodes.items():
            dx = max(divider.left - node.right, node.left - divider.right, 0)
            dy = max(divider.top - node.bottom, node.top - divider.bottom, 0)
            clearance = math.hypot(dx, dy)
            if clearance < args.divider_node_clearance:
                errors.append({
                    "type": "divider-node-clearance",
                    "divider": divider_name,
                    "node": node_name,
                    "actual": clearance,
                    "required": args.divider_node_clearance,
                })

    for edge in edges:
        name = edge.attrib["data-layout-edge"]
        source_name, target_name = edge.attrib.get("data-from"), edge.attrib.get("data-to")
        flow = edge.attrib.get("data-flow")
        source, target = nodes.get(source_name or ""), nodes.get(target_name or "")
        if not source or not target:
            errors.append({"type": "edge-missing-endpoint", "edge": name})
            continue
        try:
            points = path_points(edge.attrib.get("d", ""))
        except ValueError as exc:
            errors.append({"type": "edge-path", "edge": name, "message": str(exc)})
            continue
        start, end = points[0], points[-1]
        arrow_entry = arrows.get(name)
        if not arrow_entry:
            errors.append({"type": "edge-arrow-target", "edge": name})
            continue
        arrow_element, arrow = arrow_entry
        arrow_x = [point[0] for point in arrow]
        arrow_y = [point[1] for point in arrow]
        ordered = {"down": end[1] > start[1], "up": end[1] < start[1], "right": end[0] > start[0], "left": end[0] < start[0]}.get(flow or "", False)
        if not ordered:
            errors.append({"type": "edge-direction", "edge": name, "flow": flow})
        nonzero_segments = [
            (first, second)
            for first, second in zip(points, points[1:])
            if first != second
        ]
        # Inspect a fixed terminal approach span, rather than the last two commands.
        # A long straight tail after a legal elbow is valid; a tiny tail must not
        # conceal a kink immediately before the arrowhead.
        remaining = max(16.0, 2 * float(style_value(edge, "stroke-width", "1")))
        approach_segments = []
        for segment in reversed(nonzero_segments):
            approach_segments.append(segment)
            remaining -= math.dist(*segment)
            if remaining <= 0:
                break
        tangent_angles: list[float] = []
        for first, second in approach_segments:
            dx, dy = second[0] - first[0], second[1] - first[1]
            primary = dx if flow == "right" else -dx if flow == "left" else dy if flow == "down" else -dy
            cross = abs(dy) if flow in {"right", "left"} else abs(dx)
            tangent_angles.append(math.degrees(math.atan2(cross, primary)) if primary > 0 else 180.0)
        tangent_angle = max(tangent_angles, default=180.0)
        if tangent_angle > args.arrow_tangent_tolerance:
            errors.append({
                "type": "arrow-tangent-misaligned",
                "edge": name,
                "flow": flow,
                "actual": tangent_angle,
                "allowed": args.arrow_tangent_tolerance,
            })
        if flow in {"down", "up"}:
            anchored = source.left <= start[0] <= source.right and target.left <= end[0] <= target.right
            arrow_tip = max(arrow_y) if flow == "down" else min(arrow_y)
            target_clearance = target.top - arrow_tip if flow == "down" else arrow_tip - target.bottom
        else:
            anchored = source.top <= start[1] <= source.bottom and target.top <= end[1] <= target.bottom
            arrow_tip = max(arrow_x) if flow == "right" else min(arrow_x)
            target_clearance = target.left - arrow_tip if flow == "right" else arrow_tip - target.right
        if not anchored:
            errors.append({"type": "edge-anchor", "edge": name})
        stroke_width = float(style_value(edge, "stroke-width", "1").removesuffix("px"))
        linecap = style_value(edge, "stroke-linecap", "butt")
        cap_extension = stroke_width / 2 if linecap in {"round", "square"} else 0
        if flow == "right":
            shaft_tip, overrun = end[0] + cap_extension, end[0] + cap_extension - arrow_tip
        elif flow == "left":
            shaft_tip, overrun = end[0] - cap_extension, arrow_tip - (end[0] - cap_extension)
        elif flow == "down":
            shaft_tip, overrun = end[1] + cap_extension, end[1] + cap_extension - arrow_tip
        else:
            shaft_tip, overrun = end[1] - cap_extension, arrow_tip - (end[1] - cap_extension)
        if overrun > args.arrow_shaft_tolerance:
            errors.append({
                "type": "marker-shaft-overrun",
                "edge": name,
                "flow": flow,
                "lineCap": linecap,
                "actual": overrun,
                "allowed": args.arrow_shaft_tolerance,
                "shaftTip": shaft_tip,
                "arrowTip": arrow_tip,
            })
        arrow_base = min(arrow_x) if flow == "right" else max(arrow_x) if flow == "left" else min(arrow_y) if flow == "down" else max(arrow_y)
        join_offset = shaft_tip - arrow_base if flow in {"right", "down"} else arrow_base - shaft_tip
        if join_offset < -args.arrow_join_tolerance:
            errors.append({
                "type": "arrow-shaft-gap",
                "edge": name,
                "actual": -join_offset,
                "allowed": args.arrow_join_tolerance,
            })
        elif join_offset > args.arrow_join_tolerance:
            errors.append({
                "type": "arrow-shaft-overlap",
                "edge": name,
                "actual": join_offset,
                "allowed": args.arrow_join_tolerance,
            })
        shaft_center = end[1] if flow in {"right", "left"} else end[0]
        arrow_center = (min(arrow_y) + max(arrow_y)) / 2 if flow in {"right", "left"} else (min(arrow_x) + max(arrow_x)) / 2
        center_offset = abs(shaft_center - arrow_center)
        if center_offset > args.arrow_join_tolerance:
            errors.append({
                "type": "arrow-shaft-misaligned",
                "edge": name,
                "actual": center_offset,
                "allowed": args.arrow_join_tolerance,
            })
        edge_stroke = style_value(edge, "stroke", "none")
        arrow_fill = style_value(arrow_element, "fill", "none")
        if edge_stroke != arrow_fill:
            errors.append({
                "type": "arrow-color-mismatch",
                "edge": name,
                "edgeStroke": edge_stroke,
                "arrowFill": arrow_fill,
            })
        if point_distance_to_rect(start, source) < args.edge_clearance:
            errors.append({"type": "edge-source-clearance", "edge": name})
        if target_clearance < args.arrow_clearance:
            errors.append({"type": "arrow-target-clearance", "edge": name, "actual": target_clearance})

    report = {
        "file": str(Path(args.svg).resolve()),
        "ok": not errors,
        "viewport": {"width": width, "height": height},
        "counts": {"nodes": len(nodes), "labels": len(labels), "dividers": len(dividers), "edges": len(edges), "arrows": len(arrows)},
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
