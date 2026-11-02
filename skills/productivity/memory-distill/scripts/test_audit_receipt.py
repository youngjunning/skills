import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from audit_receipt import audit


def receipt():
    return {
        'version': 1, 'scope_complete': True, 'expected_inputs': ['m1', 'm2'],
        'inputs': [{'id': 'm1', 'candidate_ids': ['c1'], 'reason': ''},
                   {'id': 'm2', 'candidate_ids': [], 'reason': '仅请求查看执行进度'}],
        'reviewed_kinds': ['record', 'vibe', 'reference', 'concept', 'research', 'excerpt'],
        'candidates': [{'id': 'c1', 'kind': 'record', 'source_ids': ['m1'], 'targets': ['personal']}],
        'results': [{'candidate_id': 'c1', 'target': 'personal', 'status': 'created',
                     'record_id': 'item-1', 'reason': '本人明确选择',
                     'validation': 'validation-result', 'readback': 'readback-result'}],
    }


class AuditTests(unittest.TestCase):
    def test_complete_created_item_counts_once(self):
        result = audit(receipt())
        self.assertTrue(result['ok'])
        self.assertEqual(result['completion'], 'changed')
        self.assertEqual(result['summary'], [{'target': 'personal', 'kind': 'record',
                                             'status': 'created', 'count': 1}])

    def test_missing_input_cannot_report_no_new(self):
        data = receipt()
        data['inputs'].pop()
        self.assertFalse(audit(data)['ok'])

    def test_truncated_scope_rejected(self):
        data = receipt()
        data['scope_complete'] = False
        self.assertFalse(audit(data)['ok'])

    def test_excluded_input_needs_reason(self):
        data = receipt()
        data['inputs'][1]['reason'] = ''
        self.assertFalse(audit(data)['ok'])

    def test_each_kind_is_reviewed_independently(self):
        data = receipt()
        data['reviewed_kinds'].remove('reference')
        self.assertFalse(audit(data)['ok'])

    def test_unhandled_target_rejected(self):
        data = receipt()
        data['candidates'][0]['targets'].append('public')
        self.assertFalse(audit(data)['ok'])

    def test_source_links_must_match(self):
        data = receipt()
        data['candidates'][0]['source_ids'] = ['m2']
        self.assertFalse(audit(data)['ok'])

    def test_duplicate_needs_identity_and_existing_reference(self):
        for missing in ['record_id', 'existing_ref', 'reason']:
            with self.subTest(missing=missing):
                data = receipt()
                data['results'][0].update(status='duplicate', existing_ref='target/records#item-1')
                data['results'][0].pop(missing)
                self.assertFalse(audit(data)['ok'])
        data = receipt()
        data['results'][0].update(status='duplicate', existing_ref='target/records#item-1')
        self.assertEqual(audit(data)['completion'], 'no_new')

    def test_saved_requires_both_validation_and_readback(self):
        for missing in ['validation', 'readback']:
            data = receipt()
            data['results'][0].pop(missing)
            self.assertFalse(audit(data)['ok'])

    def test_failure_on_one_target_does_not_erase_other_success(self):
        data = receipt()
        data['candidates'][0]['targets'].append('public')
        data['results'].append({'candidate_id': 'c1', 'target': 'public',
                                'status': 'failed', 'reason': '目标验证失败'})
        result = audit(data)
        self.assertTrue(result['ok'])
        self.assertEqual(result['completion'], 'attention')
        self.assertEqual(len(result['summary']), 2)

    def test_unsupported_research_is_candidate_not_saved(self):
        data = receipt()
        data['candidates'][0]['kind'] = 'research'
        data['results'][0] = {'candidate_id': 'c1', 'target': 'personal',
                              'status': 'candidate', 'reason': '目标没有待办存储映射'}
        result = audit(data)
        self.assertEqual(result['completion'], 'attention')
        self.assertEqual(result['summary'][0]['status'], 'candidate')

    def test_vibe_observation_uses_its_own_kind(self):
        data = receipt()
        data['candidates'][0]['kind'] = 'vibe'
        result = audit(data)
        self.assertTrue(result['ok'])
        self.assertEqual(result['summary'][0]['kind'], 'vibe')

    def test_duplicate_target_identity_is_not_double_counted(self):
        data = receipt()
        second = copy.deepcopy(data['candidates'][0])
        second['id'] = 'c2'
        data['candidates'].append(second)
        data['inputs'][0]['candidate_ids'].append('c2')
        second_result = copy.deepcopy(data['results'][0])
        second_result['candidate_id'] = 'c2'
        second_result['status'] = 'updated'
        data['results'].append(second_result)
        self.assertFalse(audit(data)['ok'])

    def test_same_identity_across_targets_counted_separately(self):
        data = receipt()
        data['candidates'][0]['targets'].append('public')
        second = copy.deepcopy(data['results'][0])
        second['target'] = 'public'
        data['results'].append(second)
        self.assertEqual(len(audit(data)['summary']), 2)

    def test_no_candidate_requires_all_inputs_accounted_for(self):
        data = receipt()
        data['inputs'][0].update(candidate_ids=[], reason='重复确认当前操作')
        data['candidates'] = []
        data['results'] = []
        self.assertEqual(audit(data)['completion'], 'no_new')

    def test_invalid_types_report_errors(self):
        for value in [None, [], {}, {'version': 1, 'inputs': 'wrong'},
                      {**receipt(), 'results': [{'candidate_id': []}]}]:
            with self.subTest(value=value):
                self.assertFalse(audit(value)['ok'])

    def test_cli_read_only_and_failure_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'receipt.json'
            data = receipt()
            data['results'] = []
            original = json.dumps(data)
            path.write_text(original)
            result = subprocess.run([sys.executable, str(Path(__file__).with_name('audit_receipt.py')), str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(json.loads(result.stdout)['ok'])
            self.assertEqual(path.read_text(), original)


if __name__ == '__main__':
    unittest.main()
