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
requireText(/pakco\/joyally-theme\.css/, 'Joyally Design theme is not linked');

if (isDeck) {
  requireText(/class=["'][^"']*deck(?:\s|["'])/, 'deck root is missing');
  requireText(/class=["'][^"']*slide(?:\s|["'])/, 'at least one slide is required');
  requireText(/pakco\/runtime\.js/, 'Pakco runtime is not linked');
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

const requiredFiles = [
  'pakco/base.css',
  'pakco/joyally-theme.css',
  'pakco/LICENSE',
];

if (isDeck) requiredFiles.push('pakco/runtime.js', 'pakco/animations.css');

for (const relativePath of requiredFiles) {
  try {
    await access(resolve(deckDir, relativePath), constants.R_OK);
  } catch {
    errors.push(`missing readable file: ${relativePath}`);
  }
}

if (/style=["'][^"']*(?:#[0-9a-f]{3,8}|rgb\()/i.test(html)) {
  warnings.push('inline literal colors found; prefer semantic theme tokens');
}

if (/{{[A-Z_]+}}/.test(html)) errors.push('unresolved template placeholder found');

if (isReport && /<script[^>]+pakco\/runtime\.js/.test(html)) {
  warnings.push('reports should use native scrolling and normally do not need the Pakco slide runtime');
}

const result = { indexPath, mode: isDeck ? 'deck' : isReport ? 'report' : 'unknown', slideCount, notesCount, errors, warnings };
console.log(JSON.stringify(result, null, 2));
if (errors.length) process.exit(2);
