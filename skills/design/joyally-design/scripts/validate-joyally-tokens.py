#!/usr/bin/env python3
"""Validate the self-contained Joyally Design tokens and bundled HTML theme."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TOKEN_FILE = SKILL_ROOT / "assets" / "joyally-design.tokens.json"
THEME_FILE = SKILL_ROOT / "assets" / "joyally-report-theme.css"
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
REFERENCE = re.compile(r"^\{([a-zA-Z0-9_.]+)\}$")
CSS_TOKEN = re.compile(r"(--[a-zA-Z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{6})\s*;")
REQUIRED_SEMANTIC = {
    "background",
    "surface",
    "surfaceStrong",
    "surfaceMuted",
    "text",
    "textSecondary",
    "primary",
    "primaryAction",
    "onPrimaryAction",
    "success",
    "warning",
    "error",
    "focus",
    "darkBackground",
    "onDark",
}
REQUIRED_THEME_ROLES = {
    "background",
    "surface",
    "surfaceMuted",
    "primary",
    "primaryHover",
    "primaryAction",
    "accent",
    "text",
    "textSecondary",
    "border",
    "success",
    "warning",
    "error",
    "focus",
}
REQUIRED_MATERIAL_FIELDS = {
    "surfaceAlpha",
    "surfaceStrongAlpha",
    "surfaceMutedAlpha",
    "borderAlpha",
    "quietBorderAlpha",
    "blur",
    "fallback",
    "atmosphere",
}
THEME_MAPPING = {
    "--bg": "semantic.background",
    "--surface": "semantic.surface",
    "--surface-2": "semantic.primarySubtle",
    "--text-1": "semantic.text",
    "--text-2": "semantic.textSecondary",
    "--text-3": "semantic.textTertiary",
    "--accent": "semantic.primaryAction",
    "--accent-2": "semantic.primary",
    "--accent-3": "color.lakeMist",
    "--good": "semantic.success",
    "--warn": "semantic.warning",
    "--bad": "semantic.error",
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
    linear = [
        value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
        for value in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(left: str, right: str) -> float:
    high, low = sorted((relative_luminance(left), relative_luminance(right)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def parse_css_tokens(path: Path) -> dict[str, str]:
    return {name: value.upper() for name, value in CSS_TOKEN.findall(path.read_text(encoding="utf-8"))}


def check_mapping(
    actual: dict[str, str],
    mapping: dict[str, str],
    document: dict,
    label: str,
    errors: list[str],
) -> int:
    passed = 0
    for css_name, token_name in mapping.items():
        expected = resolve_color(document, token_name)
        value = actual.get(css_name)
        if value is None:
            errors.append(f"{label} is missing {css_name}")
        elif value != expected:
            errors.append(f"{label} {css_name} is {value}, expected {expected} from {token_name}")
        else:
            passed += 1
    return passed


def check_appearance_contract(document: dict, errors: list[str]) -> tuple[int, int]:
    contract = document.get("appearanceContract")
    if not isinstance(contract, dict):
        errors.append("appearanceContract must be an object")
        return 0, 0

    theme_tokens = contract.get("themeTokens")
    if not isinstance(theme_tokens, dict) or not theme_tokens:
        errors.append("appearanceContract.themeTokens must be a non-empty object")
    else:
        missing = sorted(REQUIRED_THEME_ROLES - theme_tokens.keys())
        if missing:
            errors.append(f"themeTokens is missing roles: {', '.join(missing)}")
        for role in theme_tokens:
            try:
                resolve_color(document, f"appearanceContract.themeTokens.{role}")
            except (KeyError, ValueError) as error:
                errors.append(str(error))

    materials = contract.get("materialTokens")
    if not isinstance(materials, dict) or not materials:
        errors.append("appearanceContract.materialTokens must be a non-empty object")
        material_count = 0
    else:
        material_count = len(materials)
        for material_name, values in materials.items():
            if not isinstance(values, dict):
                errors.append(f"material {material_name} must be an object")
                continue
            missing = sorted(REQUIRED_MATERIAL_FIELDS - values.keys())
            if missing:
                errors.append(f"material {material_name} is missing fields: {', '.join(missing)}")
            for field in ("surfaceAlpha", "surfaceStrongAlpha", "surfaceMutedAlpha", "borderAlpha", "quietBorderAlpha"):
                value = values.get(field)
                if not isinstance(value, (int, float)) or not 0 <= value <= 1:
                    errors.append(f"material {material_name}.{field} must be a number between 0 and 1")
            blur = values.get("blur")
            if not isinstance(blur, str) or not re.fullmatch(r"\d+(?:\.\d+)?px", blur):
                errors.append(f"material {material_name}.blur must be a pixel value")

    rules = contract.get("materialRules")
    required_rules = {
        "contentSurface",
        "transparentAllowed",
        "transparentForbidden",
        "surfaceRoles",
        "reducedTransparencyFallback",
        "semanticColorsUnaffected",
    }
    if not isinstance(rules, dict):
        errors.append("appearanceContract.materialRules must be an object")
    else:
        missing = sorted(required_rules - rules.keys())
        if missing:
            errors.append(f"appearanceContract.materialRules is missing: {', '.join(missing)}")
        if rules.get("semanticColorsUnaffected") is not True:
            errors.append("appearanceContract.materialRules.semanticColorsUnaffected must be true")
        surface_roles = rules.get("surfaceRoles")
        if not isinstance(surface_roles, dict):
            errors.append("appearanceContract.materialRules.surfaceRoles must be an object")
        else:
            chrome = surface_roles.get("materialChrome")
            reading = surface_roles.get("opaqueReading")
            for role_name, elements in (("materialChrome", chrome), ("opaqueReading", reading)):
                if not isinstance(elements, list) or not elements or not all(isinstance(item, str) and item for item in elements):
                    errors.append(f"appearanceContract.materialRules.surfaceRoles.{role_name} must be a non-empty string list")
            if isinstance(chrome, list) and isinstance(reading, list) and set(chrome) & set(reading):
                errors.append("appearanceContract.materialRules.surfaceRoles cannot assign an element to both roles")

    return len(theme_tokens) if isinstance(theme_tokens, dict) else 0, material_count


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

    for group_name in ("color", "semantic", "component"):
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

    theme_passed = check_mapping(
        parse_css_tokens(THEME_FILE), THEME_MAPPING, document, "HTML theme", errors
    )
    theme_role_count, material_count = check_appearance_contract(document, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"validated {len(document['color'])} colors, {len(document['semantic'])} semantic roles, "
        f"{passed_pairs} contrast pairs, {theme_passed} HTML theme mappings, "
        f"{theme_role_count} theme roles, {material_count} material presets"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
