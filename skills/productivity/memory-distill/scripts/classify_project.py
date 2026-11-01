#!/usr/bin/env python3
"""Classify local Git remote hosts; private host policy comes from the caller."""
import argparse
import json
import os
import re
import subprocess
from urllib.parse import urlsplit

EXTERNAL_HOSTS = {'github.com', 'gitlab.com', 'bitbucket.org'}


def host_of(url):
    try:
        if '://' in url:
            parsed = urlsplit(url)
            if parsed.scheme not in {'http', 'https', 'ssh', 'git'}:
                return None
            return (parsed.hostname or '').lower().rstrip('.') or None
        match = re.fullmatch(r'(?:[^/@:\s]+@)?([^/:\s]+):.+', url)
        return match.group(1).lower().rstrip('.') if match else None
    except ValueError:
        return None


def classify(urls, internal_hosts=()):
    hosts = [host_of(url) for url in urls]
    allowed = {host.lower().rstrip('.') for host in internal_hosts}
    if hosts and all(host in allowed for host in hosts):
        classification, reason = 'internal', 'all_remotes_internal'
    elif hosts and all(host in EXTERNAL_HOSTS for host in hosts):
        classification, reason = 'external', 'external_hosting_only'
    else:
        classification, reason = 'unknown', 'missing_mixed_or_unrecognized_remotes'
    return {'classification': classification, 'reason': reason,
            'hosts': sorted({host for host in hosts if host}),
            'automatic_distillation': classification in {'internal', 'external'},
            'route': {'internal': 'internal_then_sanitized_public', 'external': 'public', 'unknown': 'candidate_only'}[classification]}


def inspect(path, internal_hosts=()):
    def git(*args):
        return subprocess.run(['git', '-C', path, *args], capture_output=True, text=True, timeout=10)
    try:
        root = git('rev-parse', '--show-toplevel')
        if root.returncode:
            return {'classification': 'unknown', 'reason': 'not_git_repository', 'automatic_distillation': False}
        remotes = git('remote')
        if remotes.returncode:
            raise RuntimeError('remote read failed')
        urls = []
        for remote in remotes.stdout.splitlines():
            for extra in [[], ['--push']]:
                result = git('remote', 'get-url', '--all', *extra, remote)
                if result.returncode:
                    raise RuntimeError('remote URL read failed')
                urls.extend(result.stdout.splitlines())
        return {**classify(urls, internal_hosts), 'repository': root.stdout.strip()}
    except (OSError, subprocess.TimeoutExpired, RuntimeError):
        return {'classification': 'unknown', 'reason': 'git_read_failed', 'automatic_distillation': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--path', default='.')
    parser.add_argument('--internal-host', action='append', default=[])
    args = parser.parse_args()
    configured = args.internal_host + [x.strip() for x in os.environ.get('MEMORY_DISTILL_INTERNAL_HOSTS', '').split(',') if x.strip()]
    if any(not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.?', x) or '..' in x for x in configured):
        parser.error('internal hosts must be exact DNS hostnames, without schemes, paths, ports or wildcards')
    print(json.dumps(inspect(args.path, configured), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
