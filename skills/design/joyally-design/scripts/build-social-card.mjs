#!/usr/bin/env node

import { access, cp, mkdir, writeFile } from 'node:fs/promises';
import { constants } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const skillRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const outputArg = args[0];
const option = (name, fallback = '') => {
  const index = args.indexOf(name);
  return index >= 0 ? args[index + 1] : fallback;
};
if (!outputArg || outputArg === '--help' || outputArg.startsWith('--')) {
  process.stdout.write('Usage: social-card <output-dir> --title <text> --subtitle <text> --credit <source> [--style editorial|swiss|poster] [--layout cover|insight] [--eyebrow <text>] [--highlight <text>] [--page <n>] [--total <n>] [--brand <text>]\n');
  process.exit(outputArg === '--help' ? 0 : 2);
}
const title = option('--title');
const subtitle = option('--subtitle');
const credit = option('--credit');
const style = option('--style', 'editorial');
const layout = option('--layout', 'cover');
if (!title?.trim() || !subtitle?.trim() || !credit?.trim()) throw new Error('A title, subtitle, and source credit are required.');
if (!['editorial', 'swiss', 'poster'].includes(style)) throw new Error(`Unsupported style: ${style}`);
if (!['cover', 'insight'].includes(layout)) throw new Error(`Unsupported layout: ${layout}`);
const outputDir = resolve(outputArg);
try {
  await access(outputDir, constants.F_OK);
  throw new Error(`Refusing to overwrite existing directory: ${outputDir}`);
} catch (error) {
  if (error.code !== 'ENOENT') throw error;
}
await mkdir(join(outputDir, 'joyally-design'), { recursive: true });
await cp(join(skillRoot, 'assets/social-card.css'), join(outputDir, 'joyally-design/social-card.css'));
const escapeHtml = (value) => String(value)
  .replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;').replaceAll("'", '&#39;');
const eyebrow = option('--eyebrow', layout === 'cover' ? 'JOYALLY / 观点' : 'JOYALLY / 发现');
const highlight = option('--highlight');
const page = option('--page', '01');
const total = option('--total', '01');
const brand = option('--brand', 'Joyally Design');
const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="generator" content="Joyally Design">
  <title>${escapeHtml(title)} · Joyally Design</title>
  <link rel="stylesheet" href="./joyally-design/social-card.css">
</head>
<body>
  <article class="social-card social-card--${style} social-card--${layout}" aria-label="${escapeHtml(title)}">
    <header class="social-card__top"><span>${escapeHtml(brand)}</span><span>${escapeHtml(page)} / ${escapeHtml(total)}</span></header>
    <div class="social-card__main">
      <p class="social-card__eyebrow">${escapeHtml(eyebrow)}</p>
      <h1 class="social-card__title">${escapeHtml(title)}</h1>
      <div class="social-card__rule" aria-hidden="true"></div>
      <p class="social-card__subtitle">${escapeHtml(subtitle)}</p>
      ${highlight ? `<p class="social-card__highlight">${escapeHtml(highlight)}</p>` : ''}
    </div>
    <footer class="social-card__bottom"><span>${escapeHtml(credit)}</span><span>${escapeHtml(page)} / ${escapeHtml(total)}</span></footer>
  </article>
</body>
</html>
`;
await writeFile(join(outputDir, 'index.html'), html);
console.log(JSON.stringify({ style, layout, output: join(outputDir, 'index.html') }, null, 2));
