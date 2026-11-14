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

if (mode !== 'report' || !outputArg || outputArg.startsWith('--')) {
  const help = mode === '--help' || outputArg === '--help';
  const stream = help ? process.stdout : process.stderr;
  stream.write('Joyally Design\nUsage: design-engine.mjs report <output-dir> [--title <title>] [--subtitle <subtitle>]\n');
  process.exit(help ? 0 : 1);
}

const title = option('--title', 'Joyally Design HTML 报告');
const subtitle = option('--subtitle', '结论、依据与行动建议');
const outputDir = resolve(process.cwd(), outputArg);
const outputIndex = join(outputDir, 'index.html');

const artifactAssets = join(outputDir, 'joyally-design');

try {
  await access(outputDir, constants.F_OK);
  console.error(`Refusing to overwrite existing directory: ${outputDir}`);
  process.exit(3);
} catch {
  await mkdir(artifactAssets, { recursive: true });
}

await Promise.all([
  cp(join(skillRoot, 'assets/report-base.css'), join(artifactAssets, 'report-base.css')),
  cp(join(skillRoot, 'assets/joyally-report-theme.css'), join(artifactAssets, 'joyally-theme.css')),
  cp(join(skillRoot, 'LICENSE'), join(artifactAssets, 'LICENSE')),
]);

const template = await readFile(join(skillRoot, 'assets/starter-report.html'), 'utf8');
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
