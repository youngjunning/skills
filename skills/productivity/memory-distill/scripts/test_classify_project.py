import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from classify_project import classify, host_of, inspect


class ClassificationTests(unittest.TestCase):
    def test_private_hosts_require_explicit_policy(self):
        urls = ['https://git.corp.example/team/repo', 'git@code.corp.example:team/repo']
        self.assertEqual(classify(urls)['route'], 'candidate_only')
        self.assertEqual(classify(urls, ['git.corp.example', 'code.corp.example'])['route'], 'internal_then_sanitized_public')

    def test_external_does_not_claim_public_visibility(self):
        result = classify(['https://github.com/owner/private-repo'])
        self.assertEqual(result['route'], 'public')
        self.assertNotIn('visibility', result)

    def test_mixed_and_suffix_spoofing_do_not_auto_publish(self):
        for urls in [[], ['git@alias:repo'], ['file:///tmp/repo'], ['https://github.com/a/b', 'https://git.corp.example/a/b'], ['https://git.corp.example.attacker.test/a/b']]:
            self.assertFalse(classify(urls, ['git.corp.example'])['automatic_distillation'])

    def test_url_credentials_are_never_echoed(self):
        result = classify(['https://user:example-password@github.com/a/b'])
        self.assertEqual(result['hosts'], ['github.com'])
        self.assertNotIn('example-password', str(result))
        self.assertEqual(host_of('ssh://git@GITHUB.COM./a/b'), 'github.com')

    def test_local_repository_checks_fetch_and_push_hosts(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(['git', 'init', directory], capture_output=True, check=True)
            subprocess.run(['git', '-C', directory, 'remote', 'add', 'origin', 'https://git.corp.example/a/b'], check=True)
            self.assertEqual(inspect(directory, ['git.corp.example'])['classification'], 'internal')
            subprocess.run(['git', '-C', directory, 'remote', 'set-url', '--push', 'origin', 'https://github.com/a/b'], check=True)
            self.assertEqual(inspect(directory, ['git.corp.example'])['classification'], 'unknown')


if __name__ == '__main__':
    unittest.main()
