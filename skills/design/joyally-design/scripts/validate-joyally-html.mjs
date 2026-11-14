#!/usr/bin/env node

import { access, readFile } from 'node:fs/promises';
import { constants } from 'node:fs';
import { dirname, resolve } from 'node:path';

const input = process.argv[2];
if (!input) {
  console.error('Usage: validate-joyally-html.mjs <report-or-deck/index.html>');
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

const isDeck = /<body\b[^>]*class=["'][^"']*\bjoyally-deck\b/.test(html);
const isReport = /<body\b[^>]*class=["'][^"']*\bjoyally-report\b/.test(html);
if (!isDeck && !isReport) errors.push('body must use joyally-report or joyally-deck');

if (isReport) {
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

for (const name of ['report-base.css', 'joyally-theme.css', 'LICENSE']) {
  try {
    await access(resolve(assetDir, name), constants.R_OK);
  } catch {
    errors.push(`missing readable file: joyally-design/${name}`);
  }
}

if (/joyally-design\/(?:base\.css|runtime\.js|deck\.css|animations\.css|fx-runtime\.js)/.test(html)) {
  errors.push('report must not load presentation assets');
}
}

let slideCount = 0;
let notesCount = 0;
if (isDeck) {
  requireText(/href=["'](?:\.\/)?joyally-design\/base\.css["']/, 'presentation base is not linked');
  requireText(/href=["'](?:\.\/)?joyally-design\/deck\.css["']/, 'Joyally deck layout is not linked');
  requireText(/src=["'](?:\.\/)?joyally-design\/runtime\.js["']/, 'presentation runtime is not linked');
  requireText(/class=["'][^"']*\bdeck\b/, 'deck root is missing');
  slideCount = (html.match(/<section\b[^>]*class=["'][^"']*\bslide\b/g) || []).length;
  notesCount = (html.match(/<aside\b[^>]*class=["'][^"']*\bnotes\b/g) || []).length;
  if (!slideCount) errors.push('at least one slide is required');
  if (notesCount < slideCount) warnings.push(`${slideCount - notesCount} slide(s) have no speaker notes`);
  const themes = html.match(/data-themes=["']([^"']+)["']/)?.[1]?.split(',') ?? [];
  const required = ['base.css', 'deck.css', 'runtime.js', 'animations.css', 'fx-runtime.js', 'fx/_util.js', 'LICENSE'];
  for (const name of themes) {
    if (!/^[a-z][a-z-]*$/.test(name)) errors.push(`invalid theme name: ${name}`);
    else required.push(`themes/${name}.css`);
  }
  if (html.includes('data-fx=')) {
    for (const name of [...html.matchAll(/data-fx=["']([a-z-]+)["']/g)].map((match) => match[1])) required.push(`fx/${name}.js`);
  }
  for (const name of required) {
    try { await access(resolve(assetDir, name), constants.R_OK); }
    catch { errors.push(`missing readable file: joyally-design/${name}`); }
  }
}
if (/style=["'][^"']*(?:#[0-9a-f]{3,8}|rgb\()/i.test(html)) {
  warnings.push('inline literal colors found; prefer semantic theme tokens');
}
if (/{{[A-Z_]+}}/.test(html)) errors.push('unresolved template placeholder found');

const result = { indexPath, mode: isDeck ? 'deck' : isReport ? 'report' : 'unknown', slideCount, notesCount, errors, warnings };
console.log(JSON.stringify(result, null, 2));
if (errors.length) process.exit(2);
