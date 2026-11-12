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
  const help = mode === '--help' || outputArg === '--help';
  const stream = help ? process.stdout : process.stderr;
  stream.write('Joyally Design\nUsage: design-engine.mjs <report|deck> <output-dir> [--title <title>] [--subtitle <subtitle>]\n');
  process.exit(help ? 0 : 1);
}

const title = option('--title', mode === 'report' ? 'Joyally Design HTML 报告' : 'Joyally Design HTML 演示');
const subtitle = option('--subtitle', mode === 'report' ? '结论、依据与行动建议' : '用清晰层级与可靠证据讲明核心信息');
const outputDir = resolve(process.cwd(), outputArg);
const outputIndex = join(outputDir, 'index.html');

const runtimeDir = join(skillRoot, 'runtime/html');
const artifactAssets = join(outputDir, 'joyally-design');

const required = [
  'assets/base.css',
  'assets/runtime.js',
  'assets/animations/animations.css',
  'LICENSE',
];

try {
  await Promise.all(required.map((entry) => access(join(runtimeDir, entry), constants.R_OK)));
} catch {
  console.error(`Joyally Design HTML runtime is incomplete: ${runtimeDir}`);
  process.exit(2);
}

try {
  await access(outputDir, constants.F_OK);
  console.error(`Refusing to overwrite existing directory: ${outputDir}`);
  process.exit(3);
} catch {
  await mkdir(artifactAssets, { recursive: true });
}

const copies = [
  ['assets/base.css', 'base.css'],
  ['LICENSE', 'LICENSE'],
];

if (mode === 'deck') {
  copies.push(
    ['assets/runtime.js', 'runtime.js'],
    ['assets/animations/animations.css', 'animations.css'],
  );
}

await Promise.all(copies.map(([source, target]) => cp(join(runtimeDir, source), join(artifactAssets, target))));
await cp(join(skillRoot, 'assets/joyally-html-theme.css'), join(artifactAssets, 'joyally-theme.css'));
if (mode === 'deck') {
  await cp(join(skillRoot, 'assets/deck.css'), join(artifactAssets, 'deck.css'));
  await cp(join(skillRoot, 'assets/deck-themes'), join(artifactAssets, 'themes'), { recursive: true });
  await cp(join(runtimeDir, 'assets/animations/fx-runtime.js'), join(artifactAssets, 'fx-runtime.js'));
  await cp(join(runtimeDir, 'assets/animations/fx'), join(artifactAssets, 'fx'), { recursive: true });
}

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
