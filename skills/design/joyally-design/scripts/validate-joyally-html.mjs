#!/usr/bin/env node

import { access, readFile } from 'node:fs/promises';
import { constants } from 'node:fs';
import { dirname, resolve } from 'node:path';

const input = process.argv[2];
if (!input) {
  console.error('Usage: validate-joyally-html.mjs <report/index.html>');
  process.exit(1);
}

const indexPath = resolve(process.cwd(), input);
const html = await readFile(indexPath, 'utf8');
const assetDir = resolve(dirname(indexPath), 'joyally-design');
const errors = [];
const warnings = [];
const requireText = (pattern, message) => {
  if (!pattern.test(html)) errors.push(message);
};

requireText(/class=["'][^"']*joyally-report/, 'body must use joyally-report');
requireText(/href=["'](?:\.\/)?joyally-design\/report-base\.css["']/, 'Joyally report base is not linked');
requireText(/href=["'](?:\.\/)?joyally-design\/joyally-theme\.css["']/, 'Joyally report theme is not linked');
requireText(
  /<meta\b(?=[^>]*\bname=["']viewport["'])(?=[^>]*\bcontent=["'][^"']*width=device-width)[^>]*>/i,
  'report viewport meta with width=device-width is missing',
);
requireText(/<main\b/, 'report main region is missing');
requireText(/class=["'][^"']*report-summary/, 'report summary is missing');
requireText(/class=["'][^"']*report-finding/, 'at least one report finding is required');
requireText(/class=["'][^"']*report-evidence/, 'report evidence region is missing');

for (const name of ['report-base.css', 'joyally-theme.css']) {
  try {
    await access(resolve(assetDir, name), constants.R_OK);
  } catch {
    errors.push(`missing readable file: joyally-design/${name}`);
  }
}

if (/joyally-design\/(?:base\.css|runtime\.js|deck\.css|animations\.css|fx-runtime\.js)/.test(html)) {
  errors.push('report must not load presentation assets');
}
if (/style=["'][^"']*(?:#[0-9a-f]{3,8}|rgb\()/i.test(html)) {
  warnings.push('inline literal colors found; prefer semantic theme tokens');
}
if (/{{[A-Z_]+}}/.test(html)) errors.push('unresolved template placeholder found');

const result = { indexPath, mode: 'report', errors, warnings };
console.log(JSON.stringify(result, null, 2));
if (errors.length) process.exit(2);
