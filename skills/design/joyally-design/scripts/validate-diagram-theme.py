#!/usr/bin/env python3
"""Validate the Joyally Design diagram palettes and print mappings."""
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('tokens', Path(__file__).with_name('validate-joyally-tokens.py'))
tokens = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tokens)


def validate():
    document = json.loads((ROOT / 'assets/joyally-design.tokens.json').read_text())
    template = (ROOT / 'runtime/diagram/assets/template.html').read_text()
    count = 0
    for mode in ('light', 'dark'):
        expected = {key: tokens.resolve_color(document, f'diagram.{mode}.{key}')
                    for key in document['diagram'][mode]}
        for preset in ('classic', 'signal-flow', 'blueprint', 'editorial'):
            selector = ('' if preset == 'classic' else f'[data-preset="{preset}"]') + f'[data-theme="{mode}"]'
            matches = re.findall(r'^    ' + re.escape(selector) + r' \{(.*?)\n    \}', template, re.M | re.S)
            assert len(matches) == 1, f'Missing or duplicated palette: {preset}/{mode}'
            actual = dict(re.findall(r'--([\w-]+):\s*([^;]+);', matches[0]))
            assert {k: v.upper() for k, v in actual.items()} == expected, f'Palette drift: {preset}/{mode}'
            count += 1
        # Text and category strokes also serve labels, so verify normal-text contrast.
        pairs = [(text, bg, 4.5) for text in ('text', 'text-muted', 'text-dim', 'text-faint')
                 for bg in ('bg', 'panel', 'lane-fill')]
        pairs += [('toolbar-text', 'toolbar-bg', 4.5), ('arrow', 'bg', 3), ('arrow-emphasis', 'bg', 3)]
        for category in ('frontend', 'backend', 'database', 'cloud', 'security', 'messagebus', 'external'):
            pairs += [(category + '-stroke', category + '-fill', 4.5),
                      ('text', category + '-fill', 4.5),
                      (category + '-stroke', 'bg', 3)]
        for foreground, background, minimum in pairs:
            ratio = tokens.contrast(expected[foreground], expected[background])
            assert ratio >= minimum, f'{mode} {foreground}/{background}: {ratio:.2f} < {minimum}'
    print_block = re.search(r'@media print.*?\[data-theme\]\[data-preset\].*?\{(.*?)\n      \}', template, re.S)
    assert print_block, 'Print palette must override preset specificity'
    printed = dict(re.findall(r'--([\w-]+):\s*([^;]+);', print_block[1]))
    expected_print = {k: tokens.resolve_color(document, f'diagram.light.{k}') for k in document['diagram']['light']}
    expected_print.update(bg='#FFFFFF', panel='#FFFFFF', mask='#FFFFFF', grid='TRANSPARENT')
    assert {k: v.upper() for k, v in printed.items()} == expected_print, 'Print palette drift'
    reader = (ROOT / 'runtime/diagram/explainer/reader.css').read_text()
    reader_count = 0
    for line in reader.splitlines():
        if '--paper:' not in line:
            continue
        mode = 'dark' if '[data-theme=dark]' in line or ':not([data-theme])' in line else 'light'
        printing = line.startswith(':root,:root[data-style][data-theme]')
        if printing:
            mode = 'light'
        expected = {key: tokens.resolve_color(document, f'diagram.{mode}.{role}')
                    for key, role in document['readerMapping'].items()}
        if printing:
            expected.update(paper='#FFFFFF', panel='#FFFFFF', surface='#FFFFFF')
        actual = dict(re.findall(r'--([\w-]+):([^;}]+)', line))
        assert all(actual.get(key, '').upper() == value for key, value in expected.items()), 'Explainer palette drift'
        reader_count += 1
    assert reader_count == 13, f'Expected 12 explainer theme blocks and print, got {reader_count}'
    print(f'Validated {count} viewer palettes, 13 explainer palettes, print mappings and 72 contrast pairs')


if __name__ == '__main__':
    validate()
