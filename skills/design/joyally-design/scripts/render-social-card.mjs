#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { access, mkdtemp, mkdir, rm } from 'node:fs/promises';
import { constants } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const indexArg = args[0];
const option = (name, fallback) => {
  const index = args.indexOf(name);
  return index >= 0 ? args[index + 1] : fallback;
};
if (!indexArg || indexArg === '--help') {
  process.stdout.write('Usage: social-render <index.html> [--out <image.png>] [--scale 1|2] [--chrome <executable>]\n');
  process.exit(indexArg === '--help' ? 0 : 2);
}
const indexPath = resolve(indexArg);
const out = resolve(option('--out', join(dirname(indexPath), 'card.png')));
const scale = Number(option('--scale', '2'));
if (![1, 2].includes(scale)) throw new Error('Scale must be 1 or 2.');
const chrome = option('--chrome', process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');
await access(chrome, constants.X_OK);
await mkdir(dirname(out), { recursive: true });
const profile = await mkdtemp(join(tmpdir(), 'joyally-social-chrome-'));
try {
  const result = spawnSync(chrome, [
    '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check',
    `--user-data-dir=${profile}`, '--allow-file-access-from-files', '--window-size=1080,1440',
    `--force-device-scale-factor=${scale}`, '--virtual-time-budget=3000', `--screenshot=${out}`,
    pathToFileURL(indexPath).href,
  ], { encoding: 'utf8' });
  if (result.error || result.status !== 0) throw new Error(result.error?.message || result.stderr || `Chrome exited ${result.status}`);
} finally {
  await rm(profile, { recursive: true, force: true });
}
console.log(JSON.stringify({ output: out, width: 1080 * scale, height: 1440 * scale }, null, 2));
