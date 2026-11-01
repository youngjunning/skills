#!/usr/bin/env python3
"""Check exported picture-book geometry and evidence; never infer visual approval."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image


def rectangle(value):
    return (isinstance(value, list) and len(value) == 4
            and all(type(v) in (int, float) and math.isfinite(v) for v in value)
            and 0 <= value[0] < value[2] <= 1
            and 0 <= value[1] < value[3] <= 1)


def inside(a, b):
    return b[0] <= a[0] and b[1] <= a[1] and a[2] <= b[2] and a[3] <= b[3]


def overlap(a, b):
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])


def validate(book, root):
    errors, warnings = [], []
    pages = book['pages']
    count = book['page_count']
    if type(count) is not int or count < 1 or len(pages) != count:
        errors.append('page count does not match edition')
    if [p['page'] for p in pages] != list(range(1, len(pages) + 1)):
        errors.append('page numbers must be ordered, contiguous, and unique')
    width, height = book['size_cm']
    dpi = book['dpi']
    if not all(type(v) in (int, float) and math.isfinite(v) and v > 0
               for v in (width, height, dpi)):
        raise ValueError('size_cm and dpi must be finite and positive')
    expected = (round(width / 2.54 * dpi), round(height / 2.54 * dpi))
    safe = book['safe_box']
    if not rectangle(safe):
        raise ValueError('invalid normalized safe_box')
    if book['layout'] not in ('integrated', 'split'):
        raise ValueError('layout must be integrated or split')
    seen_art, seen_outputs = {}, set()
    signatures = []
    for p in pages:
        label = f"page {p['page']}"
        for field in ('purpose', 'scene', 'focal_subject', 'shot', 'angle', 'composition', 'evidence'):
            if not isinstance(p.get(field), str) or not p[field].strip():
                errors.append(f'{label}: missing storyboard field {field}')
        signatures.append(tuple(p.get(k) for k in ('shot', 'angle', 'composition')))
        if len(signatures) >= 3 and signatures[-1] == signatures[-2] == signatures[-3]:
            if not p.get('repetition_reason'):
                warnings.append(f'{label}: three repeated shot/angle/composition plans; inspect rhythm')
        if p.get('layout') != book['layout']:
            errors.append(f'{label}: page layout differs from edition')
        output = (root / p['image']).resolve()
        if output in seen_outputs:
            errors.append(f'{label}: reused output path')
        seen_outputs.add(output)
        try:
            with Image.open(output) as im:
                im.load()
                if im.size != expected:
                    errors.append(f'{label}: pixels {im.size}, expected {expected}')
            with Image.open(root / p['art']) as im:
                pixels = im.convert('RGBA')
                digest = hashlib.sha256(str(pixels.size).encode() + pixels.tobytes()).hexdigest()
            if digest in seen_art and not p.get('reuse_reason'):
                errors.append(f'{label}: source art duplicates page {seen_art[digest]}')
            seen_art[digest] = p['page']
            final_hash = hashlib.sha256(output.read_bytes()).hexdigest()
        except (OSError, ValueError) as exc:
            errors.append(f'{label}: unreadable image: {exc}')
            final_hash = None
        copy = p['text']
        blocks = p['text_blocks']
        if not isinstance(copy, str) or copy != ''.join(b['text'] for b in blocks):
            errors.append(f'{label}: rendered copy differs from authoritative text')
        region = p['text_region']
        protected = p['protected_boxes']
        if not rectangle(region) or not isinstance(protected, list) or not all(rectangle(b) for b in protected):
            errors.append(f'{label}: invalid text/protected geometry')
            continue
        measured = []
        for block in blocks:
            box = block['box']
            if not rectangle(box):
                errors.append(f'{label}: invalid measured text bounds')
                continue
            if not inside(box, region) or not inside(box, safe):
                errors.append(f'{label}: text outside region or safe area')
            if any(overlap(box, target) for target in protected):
                errors.append(f'{label}: text overlaps protected subject')
            if any(overlap(box, other) for other in measured):
                errors.append(f'{label}: text blocks overlap')
            measured.append(box)
        review = p.get('review', {})
        checks = ('identity', 'anatomy', 'story_evidence', 'copy', 'readability', 'composition')
        if (not final_hash or review.get('image_sha256') != final_hash
                or not review.get('note') or any(review.get(k) != 'pass' for k in checks)):
            errors.append(f'{label}: missing, stale, or failed visual review')
    return {'errors': errors, 'warnings': warnings, 'pages': len(pages),
            'expected_pixels': expected, 'scope': 'geometry/files/review records; not visual recognition'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.manifest.read_text()), args.manifest.resolve().parent)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        result = {'errors': [f'invalid manifest: {exc}'], 'warnings': []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
