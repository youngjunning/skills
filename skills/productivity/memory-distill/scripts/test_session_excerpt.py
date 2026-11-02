import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from session_excerpt import excerpt


def message(role, text, channel=None):
    payload = {'type': 'message', 'role': role,
               'content': [{'type': 'input_text' if role == 'user' else 'output_text', 'text': text}]}
    if channel:
        payload['channel'] = channel
    return {'type': 'response_item', 'timestamp': '2026-10-29T04:50:32Z', 'payload': payload}


class ExcerptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.file = Path(self.temp.name) / 'session.jsonl'

    def tearDown(self):
        self.temp.cleanup()

    def write(self, rows):
        self.file.write_text('\n'.join(json.dumps(row, ensure_ascii=False) for row in rows) + '\n')

    def test_role_and_metadata_boundaries(self):
        self.write([
            {'type': 'session_meta', 'payload': {'id': 'session-example', 'cwd': '/project'}},
            message('user', '# AGENTS.md instructions\n不要将此段当作本人观点'),
            message('assistant', 'PRIVATE_REASONING', 'analysis'),
            {'type': 'response_item', 'payload': {'type': 'function_call_output', 'output': 'TOOL_SENTINEL'}},
            message('user', '<in-app-browser-context>AMBIENT_SENTINEL</in-app-browser-context>\n## My request:\n先复用当前链路'),
            message('assistant', '建议另外创建服务', 'final'),
        ])
        data = excerpt(self.file)
        self.assertEqual(data['session']['id'], 'session-example')
        self.assertEqual([(x['role'], x['text']) for x in data['messages']],
                         [('user', '先复用当前链路'), ('assistant', '建议另外创建服务')])
        self.assertEqual(data['messages'][0]['line'], 5)

    def test_structured_reply_preserves_question_and_actual_answer(self):
        rows = [{'question': '先做哪项？', 'answer': '先建立个人记忆'}]
        self.write([message('user', '<send_user_message_question_reply>' + json.dumps(rows) + '</send_user_message_question_reply>')])
        result = excerpt(self.file)['messages'][0]
        self.assertEqual(result['text'], '问题：先做哪项？\n本人回复：先建立个人记忆')

    def test_match_keeps_context_roles_and_deduplicates_overlapping_windows(self):
        self.write([message('assistant', '候选是 A、B、C'), message('user', '三个都做'),
                    message('assistant', '确认三个都做的范围'), message('user', '先建记录模型'),
                    message('assistant', '无关尾部')])
        result = excerpt(self.file, '三个都做', before=1, after=1)
        self.assertEqual([x['line'] for x in result['messages']], [1, 2, 3, 4])
        self.assertEqual(result['messages'][0]['role'], 'assistant')
        self.assertEqual(result['messages'][1]['role'], 'user')

    def test_match_budget_and_read_only(self):
        self.write([message('user', f'选择对象 {n}') for n in range(20)])
        before = hashlib.sha256(self.file.read_bytes()).hexdigest()
        result = excerpt(self.file, '选择对象', before=0, after=0, max_hits=3)
        self.assertEqual(len(result['messages']), 3)
        self.assertEqual(result['matching_messages'], 20)
        self.assertEqual(result['selected_matches'], 3)
        self.assertTrue(result['truncated'])
        self.assertEqual(hashlib.sha256(self.file.read_bytes()).hexdigest(), before)
        tail = excerpt(self.file, tail=2)
        self.assertEqual([x['line'] for x in tail['messages']], [19, 20])

    def test_no_match_cli_exits_without_fabricating_excerpt(self):
        self.write([message('user', '别的内容')])
        command = [sys.executable, str(Path(__file__).with_name('session_excerpt.py')),
                   '--session', str(self.file), '--match', '不存在的原话']
        result = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)['messages'], [])

    def test_tail_discloses_omitted_earlier_judgment(self):
        self.write([message('user', '我认为内置脚本足够了'),
                    message('assistant', '开始检查'), message('assistant', '检查结束')])
        result = excerpt(self.file, tail=2)
        self.assertTrue(result['truncated'])
        self.assertEqual(result['selection_mode'], 'tail')
        self.assertEqual(result['omitted_messages'], 1)
        recovered = excerpt(self.file, '内置脚本', before=0, after=0)
        self.assertEqual(recovered['messages'][0]['line'], 1)
        self.assertEqual(recovered['selection_mode'], 'match')

    def test_context_block_followed_by_real_request_is_preserved(self):
        self.write([message('user', '<environment_context>ambient</environment_context>\n我改选方案 B'),
                    message('user', '<environment_context>ambient only</environment_context>')])
        result = excerpt(self.file)
        self.assertEqual([x['text'] for x in result['messages']], ['我改选方案 B'])


if __name__ == '__main__':
    unittest.main()
