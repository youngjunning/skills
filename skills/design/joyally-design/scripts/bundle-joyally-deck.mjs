#!/usr/bin/env node

import { readFile, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';

const input = process.argv[2];
const outIndex = process.argv.indexOf('--out');
if (!input || input === '--help' || outIndex < 0 || !process.argv[outIndex + 1]) {
  console.log('Usage: deck-bundle <deck/index.html> --out <standalone.html>');
  process.exit(input === '--help' ? 0 : 2);
}

const indexPath = resolve(input);
const outputPath = resolve(process.argv[outIndex + 1]);
if (outputPath === indexPath) throw new Error('Choose a separate output file to preserve the editable deck.');
const outputDir = dirname(indexPath);
const assetDir = join(outputDir, 'joyally-design');
let html = await readFile(indexPath, 'utf8');
if (!/<body\b[^>]*class=["'][^"']*\bjoyally-deck\b/.test(html)) throw new Error('Expected a Joyally Design presentation.');
const imageTypes = { png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', webp: 'image/webp', gif: 'image/gif', svg: 'image/svg+xml' };
for (const match of [...html.matchAll(/src="\.\/media\/([0-9]+\.([a-z0-9]+))"/g)]) {
  const [, name, extension] = match;
  const mime = imageTypes[extension];
  if (!mime) throw new Error(`Unsupported embedded image type: ${extension}`);
  const data = await readFile(join(outputDir, 'media', name));
  html = html.replace(`src="./media/${name}"`, `src="data:${mime};base64,${data.toString('base64')}"`);
}

const css = async (name) => `<style>\n${await readFile(join(assetDir, name), 'utf8')}\n</style>`;
for (const name of ['base.css', 'animations.css', 'deck.css']) {
  const link = `<link rel="stylesheet" href="./joyally-design/${name}">`;
  if (!html.includes(link)) throw new Error(`Missing ${name} link.`);
  html = html.replace(link, await css(name));
}

const themes = html.match(/data-themes=["']([^"']+)["']/)?.[1]?.split(',') ?? [];
if (!themes.length || themes.some((name) => !/^[a-z][a-z-]*$/.test(name))) throw new Error('Invalid theme list.');
const themeCss = [];
for (const name of themes) {
  const source = await readFile(join(assetDir, 'themes', `${name}.css`), 'utf8');
  if (!/^:root\s*\{/m.test(source)) throw new Error(`Theme ${name} has no token root.`);
  themeCss.push(source.replace(/^:root\s*\{/m, `html[data-theme="${name}"] {`));
}
if (!/<link id="theme-link"[^>]+>/.test(html)) throw new Error('Theme link is missing.');
html = html.replace(/<link id="theme-link"[^>]+>/, `<style>\n${themeCss.join('\n')}\n</style>`);
html = html.replace('<html ', '<html data-embedded-themes="true" ');

const scriptTag = async (name) => `<script>\n${await readFile(join(assetDir, name), 'utf8')}\n</script>`;
if (!html.includes('<script src="./joyally-design/runtime.js"></script>') || !html.includes('<script src="./joyally-design/fx-runtime.js"></script>')) throw new Error('Presentation scripts are missing.');
html = html.replace('<script src="./joyally-design/runtime.js"></script>', await scriptTag('runtime.js'));
const fxNames = ['_util', 'particle-burst', 'confetti-cannon', 'firework', 'starfield', 'matrix-rain', 'knowledge-graph', 'neural-net', 'constellation', 'orbit-ring', 'galaxy-swirl', 'word-cascade', 'letter-explode', 'chain-react', 'magnetic-field', 'data-stream', 'gradient-blob', 'sparkle-trail', 'shockwave', 'typewriter-multi', 'counter-explosion'];
const fxScripts = ['<script>window.__joyallyFxEmbedded = true;</script>'];
for (const name of fxNames) fxScripts.push(await scriptTag(`fx/${name}.js`));
fxScripts.push(await scriptTag('fx-runtime.js'));
html = html.replace('<script src="./joyally-design/fx-runtime.js"></script>', fxScripts.join('\n'));
const license = await readFile(join(assetDir, 'LICENSE'), 'utf8');
html = html.replace('</body>', `<!--\n${license}\n--></body>`);
await writeFile(outputPath, html);
console.log(JSON.stringify({ mode: 'deck-bundle', output: outputPath, slides: (html.match(/<section\b[^>]*class=["'][^"']*\bslide\b/g) || []).length, themes: themes.length }, null, 2));
