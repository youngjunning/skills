#!/usr/bin/env node

import { access, readFile } from 'node:fs/promises';
import { constants } from 'node:fs';
import { dirname, resolve } from 'node:path';

const input = process.argv[2];
if (!input) {
  console.error('Usage: validate-joyally-html.mjs <index.html>');
  process.exit(1);
}

const indexPath = resolve(process.cwd(), input);
const deckDir = dirname(indexPath);
const html = await readFile(indexPath, 'utf8');
const errors = [];
const warnings = [];

const requireText = (pattern, message) => {
  if (!pattern.test(html)) errors.push(message);
};

const isDeck = /class=["'][^"']*joyally-deck/.test(html);
const isReport = /class=["'][^"']*joyally-report/.test(html);
if (!isDeck && !isReport) errors.push('body must use joyally-deck or joyally-report');
const themeLink = html.match(/(?:href=["'](?:\.\/)?)(joyally-design|pakco)\/joyally-theme\.css["']/);
const assetDir = themeLink?.[1] ?? 'joyally-design';
if (!themeLink) errors.push('Joyally Design theme is not linked');
const runtimeLinked = html.includes(`${assetDir}/runtime.js`);

if (isDeck) {
  requireText(/class=["'][^"']*deck(?:\s|["'])/, 'deck root is missing');
  requireText(/class=["'][^"']*slide(?:\s|["'])/, 'at least one slide is required');
  if (!runtimeLinked) errors.push('Joyally Design presentation runtime is not linked');
}

if (isReport) {
  requireText(
    /<meta\b(?=[^>]*\bname=["']viewport["'])(?=[^>]*\bcontent=["'][^"']*width=device-width)[^>]*>/i,
    'report viewport meta with width=device-width is missing',
  );
  requireText(/<main\b/, 'report main region is missing');
  requireText(/class=["'][^"']*report-summary/, 'report summary is missing');
  requireText(/class=["'][^"']*report-finding/, 'at least one report finding is required');
  requireText(/class=["'][^"']*report-evidence/, 'report evidence region is missing');
}

const slideCount = (html.match(/<section\b[^>]*class=["'][^"']*\bslide\b/g) || []).length;
const notesCount = (html.match(/<(?:aside|div)\b[^>]*class=["'][^"']*\bnotes\b/g) || []).length;
if (notesCount < slideCount) warnings.push(`${slideCount - notesCount} slide(s) do not contain speaker notes`);
if (isDeck && html.includes('补充本页讲述要点和过渡句')) warnings.push('speaker notes still contain starter placeholders');

const requiredFiles = [
  'base.css',
  'joyally-theme.css',
  'LICENSE',
];

if (isDeck) requiredFiles.push('runtime.js', 'animations.css');
if (isDeck && html.includes(`${assetDir}/deck.css`)) requiredFiles.push('deck.css');
if (isDeck && html.includes(`${assetDir}/fx-runtime.js`)) requiredFiles.push('fx-runtime.js', 'fx/_util.js');
if (isDeck && html.includes('data-theme-base=')) {
  const themeNames = html.match(/data-themes=["']([^"']+)["']/)?.[1]?.split(',') || [];
  for (const name of themeNames) {
    if (!/^[a-z][a-z-]*$/.test(name)) errors.push(`invalid theme name: ${name}`);
    else requiredFiles.push(`themes/${name}.css`);
  }
}

for (const relativePath of requiredFiles) {
  try {
    await access(resolve(deckDir, assetDir, relativePath), constants.R_OK);
  } catch {
    errors.push(`missing readable file: ${assetDir}/${relativePath}`);
  }
}

if (/style=["'][^"']*(?:#[0-9a-f]{3,8}|rgb\()/i.test(html)) {
  warnings.push('inline literal colors found; prefer semantic theme tokens');
}

if (/{{[A-Z_]+}}/.test(html)) errors.push('unresolved template placeholder found');

if (isReport && runtimeLinked) {
  warnings.push('reports should use native scrolling and normally do not need the presentation runtime');
}

const result = { indexPath, mode: isDeck ? 'deck' : isReport ? 'report' : 'unknown', slideCount, notesCount, errors, warnings };
console.log(JSON.stringify(result, null, 2));
if (errors.length) process.exit(2);
