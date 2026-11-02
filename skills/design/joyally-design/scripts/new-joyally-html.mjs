#!/usr/bin/env node

import { access, cp, mkdir, readFile, writeFile } from 'node:fs/promises';
import { constants } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const skillRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const mode = args[0];
const outputArg = args[1];

const option = (name, fallback) => {
  const index = args.indexOf(name);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
};

if (!['deck', 'report'].includes(mode) || !outputArg || outputArg.startsWith('--')) {
  console.error('Usage: new-joyally-html.mjs <deck|report> <output-dir> [--title <title>] [--subtitle <subtitle>]');
  process.exit(1);
}

const title = option('--title', mode === 'report' ? 'Joyally Design HTML 报告' : 'Joyally Design HTML 演示');
const subtitle = option('--subtitle', mode === 'report' ? '结论、依据与行动建议' : '用清晰层级与可靠证据讲明核心信息');
const outputDir = resolve(process.cwd(), outputArg);
const outputIndex = join(outputDir, 'index.html');

const pakcoHome = join(skillRoot, 'vendor/pakco-html');

const required = [
  'assets/base.css',
  'assets/runtime.js',
  'assets/animations/animations.css',
  'LICENSE',
];

try {
  await Promise.all(required.map((entry) => access(join(pakcoHome, entry), constants.R_OK)));
} catch {
  console.error(`Bundled pakco-html is incomplete: ${pakcoHome}`);
  process.exit(2);
}

try {
  await access(outputDir, constants.F_OK);
  console.error(`Refusing to overwrite existing directory: ${outputDir}`);
  process.exit(3);
} catch {
  await mkdir(join(outputDir, 'pakco'), { recursive: true });
}

const copies = [
  ['assets/base.css', 'pakco/base.css'],
  ['LICENSE', 'pakco/LICENSE'],
];

if (mode === 'deck') {
  copies.push(
    ['assets/runtime.js', 'pakco/runtime.js'],
    ['assets/animations/animations.css', 'pakco/animations.css'],
  );
}

await Promise.all(copies.map(([source, target]) => cp(join(pakcoHome, source), join(outputDir, target))));
await cp(join(skillRoot, 'assets/joyally-pakco-theme.css'), join(outputDir, 'pakco/joyally-theme.css'));

const templateName = mode === 'report' ? 'starter-report.html' : 'starter-deck.html';
const template = await readFile(join(skillRoot, `assets/${templateName}`), 'utf8');
const escapeHtml = (value) => value
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#39;');

const html = template
  .replaceAll('{{TITLE}}', escapeHtml(title))
  .replaceAll('{{SUBTITLE}}', escapeHtml(subtitle));

await writeFile(outputIndex, html);
console.log(JSON.stringify({ mode, output: outputIndex }, null, 2));
