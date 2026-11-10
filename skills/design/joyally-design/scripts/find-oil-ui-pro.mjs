#!/usr/bin/env node

import { existsSync, readFileSync, realpathSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, resolve } from 'node:path';

const candidates = [
  process.env.OIL_UI_PRO_DIR,
  join(homedir(), '.codex', 'skills', 'oil-ui-pro'),
  join(homedir(), '.agents', 'skills', 'oil-ui-pro'),
].filter(Boolean);

const required = [
  'SKILL.md',
  'references/tools.md',
  'references/direction-workspace.md',
  'references/direction-persuasion.md',
  'references/direction-content.md',
  'references/play.md',
  'references/design-spec.md',
  'references/style-explorer.md',
  'scripts/build_explorer.py',
  'scripts/shoot.mjs',
];

for (const candidate of candidates) {
  const root = resolve(candidate);
  const entry = join(root, 'SKILL.md');
  if (!existsSync(entry)) continue;

  const source = readFileSync(entry, 'utf8');
  if (!/^name:\s*oil-ui-pro\s*$/m.test(source)) {
    process.stderr.write(`Unexpected package at ${root}: SKILL.md does not identify oil-ui-pro.\n`);
    process.exit(1);
  }

  const missing = required.filter((file) => !existsSync(join(root, file)));
  if (missing.length) {
    process.stderr.write(`Incomplete oil-ui-pro package at ${root}: ${missing.join(', ')}\n`);
    process.exit(1);
  }

  const version = source.match(/^\s+version:\s*["']?([^"'\s]+)["']?\s*$/m)?.[1] ?? 'unknown';
  process.stdout.write(`${JSON.stringify({ root: realpathSync(root), version, bridgeVersion: '0.33.3' })}\n`);
  process.exit(0);
}

process.stderr.write('oil-ui-pro is not installed in the configured or standard skill locations.\n');
process.exit(2);
