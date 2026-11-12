#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { access, mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { constants } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const indexArg = args[0];
const option = (name) => {
  const index = args.indexOf(name);
  return index < 0 ? undefined : args[index + 1];
};
if (!indexArg || indexArg === '--help') {
  process.stdout.write('Usage: deck-render <index.html> [--format png|pdf] [--out <path>] [--chrome <executable>]\nPNG exports every slide; PDF uses the deck print layout.\n');
  process.exit(indexArg === '--help' ? 0 : 2);
}
const indexPath = resolve(indexArg);
const format = option('--format') || 'png';
if (!['png', 'pdf'].includes(format)) throw new Error(`Unsupported format: ${format}`);
const chrome = option('--chrome') || process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
await access(chrome, constants.X_OK);
const html = await readFile(indexPath, 'utf8');
const count = (html.match(/<section\b[^>]*class=["'][^"']*\bslide\b/g) || []).length;
if (!count) throw new Error('No slides found.');
const out = resolve(option('--out') || (format === 'pdf' ? join(dirname(indexPath), 'deck.pdf') : join(dirname(indexPath), 'slides-png')));
if (format === 'png') await mkdir(out, { recursive: true });
else await mkdir(dirname(out), { recursive: true });
const profile = await mkdtemp(join(tmpdir(), 'joyally-deck-chrome-'));
const baseArgs = ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', `--user-data-dir=${profile}`, '--virtual-time-budget=3000', '--window-size=1920,1080'];
const fileUrl = pathToFileURL(indexPath).href;
const run = (commandArgs) => {
  const result = spawnSync(chrome, [...baseArgs, ...commandArgs], { encoding: 'utf8' });
  if (result.error || result.status !== 0) throw new Error(result.error?.message || result.stderr || `Chrome exited ${result.status}`);
};
try {
  // The first fresh headless Chrome process can capture before the deck's
  // runtime and font cache settle. Warm the same profile before exporting.
  run([`--screenshot=${join(profile, 'warmup.png')}`, `${fileUrl}?preview=1`]);
  if (format === 'pdf') {
    run(['--no-pdf-header-footer', `--print-to-pdf=${out}`, fileUrl]);
  } else {
    for (let index = 1; index <= count; index += 1) {
      const name = `slide-${String(index).padStart(2, '0')}.png`;
      run([`--screenshot=${join(out, name)}`, `${fileUrl}?preview=${index}`]);
    }
  }
} finally {
  await rm(profile, { recursive: true, force: true });
}
console.log(JSON.stringify({ format, slides: count, output: out }, null, 2));
