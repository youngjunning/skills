#!/usr/bin/env python3
"""Validate a local distillation receipt; never writes targets or infers meaning."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

KINDS = {'record', 'reference', 'concept', 'research', 'excerpt'}
STATES = {'created', 'updated', 'duplicate', 'candidate', 'skipped', 'failed'}


def audit(data):
    errors = []

    def need(condition, message):
        if not condition:
            errors.append(message)
        return condition

    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())

    def ids(value, name, allow_empty=False):
        if not isinstance(value, list) or not all(nonempty(x) for x in value):
            errors.append(f'{name}: string list required')
            return []
        need(allow_empty or bool(value), f'{name}: empty list')
        need(len(set(value)) == len(value), f'{name}: duplicate identifier')
        return value

    def rows(name):
        value = data.get(name)
        if not isinstance(value, list) or not all(isinstance(x, dict) for x in value):
            errors.append(f'{name}: object list required')
            return []
        return value

    if not isinstance(data, dict):
        return {'ok': False, 'errors': ['receipt object required']}
    need(data.get('version') == 1, 'version must be 1')
    need(data.get('scope_complete') is True, 'input scope must be complete before reporting')
    expected = ids(data.get('expected_inputs'), 'expected_inputs')
    reviewed = ids(data.get('reviewed_kinds'), 'reviewed_kinds')
    need(set(reviewed) == KINDS, 'all five content kinds must be reviewed')
    inputs, candidates, results = rows('inputs'), rows('candidates'), rows('results')

    def index(items, name):
        found = {}
        for item in items:
            key = item.get('id')
            if not need(nonempty(key), f'{name}: id required'):
                continue
            need(key not in found, f'{name}: duplicate id {key}')
            found[key] = item
        return found

    input_by_id, candidate_by_id = index(inputs, 'inputs'), index(candidates, 'candidates')
    need(set(input_by_id) == set(expected), 'input inventory must match expected_inputs')
    input_links = {}
    for key, item in input_by_id.items():
        links = ids(item.get('candidate_ids'), f'input {key} candidate_ids', allow_empty=True)
        input_links[key] = set(links)
        need(bool(links) or nonempty(item.get('reason')), f'input {key}: exclusion reason required')
        need(set(links) <= set(candidate_by_id), f'input {key}: unknown candidate')

    expected_pairs = set()
    for key, candidate in candidate_by_id.items():
        need(candidate.get('kind') in KINDS if isinstance(candidate.get('kind'), str) else False,
             f'candidate {key}: invalid kind')
        sources = ids(candidate.get('source_ids'), f'candidate {key} source_ids')
        targets = ids(candidate.get('targets'), f'candidate {key} targets')
        need(set(sources) <= set(input_by_id), f'candidate {key}: unknown input')
        linked = {source for source, links in input_links.items() if key in links}
        need(set(sources) == linked, f'candidate {key}: input references must agree in both directions')
        expected_pairs.update((key, target) for target in targets)

    actual_pairs, identities, counts = set(), set(), Counter()
    for item in results:
        key, target, status = item.get('candidate_id'), item.get('target'), item.get('status')
        if not need(nonempty(key) and nonempty(target), 'result candidate_id and target required'):
            continue
        pair = (key, target)
        need(pair in expected_pairs, 'unexpected candidate/target result')
        need(pair not in actual_pairs, 'duplicate candidate/target result')
        actual_pairs.add(pair)
        if not need(isinstance(status, str) and status in STATES, 'invalid or unfinished result state'):
            continue
        need(nonempty(item.get('reason')), 'result reason required')
        if status in {'created', 'updated', 'duplicate'}:
            record_id = item.get('record_id')
            if need(nonempty(record_id), 'target record identity required'):
                kind = candidate_by_id.get(key, {}).get('kind')
                if isinstance(kind, str):
                    identity = (target, kind, record_id)
                    need(identity not in identities, 'same target content counted more than once')
                    identities.add(identity)
            if status == 'duplicate':
                need(nonempty(item.get('existing_ref')), 'duplicate requires existing target reference')
            else:
                need(nonempty(item.get('validation')), 'saved result requires validation evidence')
                need(nonempty(item.get('readback')), 'saved result requires readback evidence')
        kind = candidate_by_id.get(key, {}).get('kind')
        if isinstance(kind, str):
            counts[(target, kind, status)] += 1
    need(actual_pairs == expected_pairs, 'every candidate/target requires a final result')
    if errors:
        return {'ok': False, 'errors': errors}
    summary = [{'target': target, 'kind': kind, 'status': status, 'count': count}
               for (target, kind, status), count in sorted(counts.items())]
    statuses = {row['status'] for row in summary}
    completion = ('attention' if statuses & {'candidate', 'failed', 'skipped'} else
                  'changed' if statuses & {'created', 'updated'} else 'no_new')
    return {'ok': True, 'completion': completion, 'summary': summary}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    args = parser.parse_args()
    try:
        result = audit(json.loads(args.receipt.read_text(encoding='utf-8')))
    except (OSError, ValueError) as error:
        result = {'ok': False, 'errors': [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
