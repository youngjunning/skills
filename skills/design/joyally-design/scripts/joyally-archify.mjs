#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const skillRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const cli = join(skillRoot, 'runtime/diagram/bin/archify.mjs');
const args = process.argv.slice(2);

if (args.length === 0) {
  console.error('Usage: joyally-archify.mjs <validate|deliver|visual-check|doctor|demo|...> [Archify arguments]');
  process.exit(1);
}

const result = spawnSync(process.execPath, [cli, ...args], {
  cwd: process.cwd(),
  env: {
    ...process.env,
    ARCHIFY_UPDATE_CHECK_DISABLED: '1',
  },
  stdio: 'inherit',
});

if (result.error) {
  console.error(`Unable to run bundled Archify: ${result.error.message}`);
  process.exit(1);
}

process.exit(result.status ?? 1);
