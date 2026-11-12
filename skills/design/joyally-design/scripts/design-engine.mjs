#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const skillDir = dirname(dirname(fileURLToPath(import.meta.url)));
const commands = {
  explore: 'build_explorer.py',
  shoot: 'shoot.mjs',
  media: 'curate-media.mjs',
  'prep-image': 'prep-image.mjs',
  measure: 'measure_reference.py',
  'design-check': 'check_design_md.py',
  cards: 'build_cards.py',
  report: 'new-joyally-html.mjs',
  'social-card': 'build-social-card.mjs',
  'social-render': 'render-social-card.mjs',
  deck: 'build-joyally-deck.mjs',
  'deck-gallery': 'build-deck-gallery.mjs',
  'deck-render': 'render-joyally-deck.mjs',
  'deck-bundle': 'bundle-joyally-deck.mjs',
  diagram: 'joyally-diagram.mjs',
};
const [command, ...args] = process.argv.slice(2);
if (!command || command === '--help') {
  process.stdout.write(`Joyally Design
Usage: node <joyally-dir>/scripts/design-engine.mjs <${Object.keys(commands).join('|')}|path|run> [tool arguments]
report <output-dir>: generate a scrolling HTML report
social-card <output-dir> --title <text> --subtitle <text> --credit <source>: generate a 3:4 social card
social-render <index.html> [--out <image.png>]: export a social card as PNG
deck <output-dir> [--scenario <name>|--source <deck.json>]: generate a Joyally presentation
deck-gallery <output-dir>: preview Joyally presentation themes and layouts
deck-render <index.html> --format png|pdf: export slides
deck-bundle <index.html> --out <standalone.html>: bundle a deck into one HTML file
diagram --help: list diagram commands and formats
image generation and editing: use the joyally-image skill
path <relative-file>: show a bundled reference, asset or script path
run <script-name> [...arguments]: run a bundled script
`);
  process.exit(command ? 0 : 2);
}
if (!Object.hasOwn(commands, command) && command !== 'path' && command !== 'run') {
  process.stderr.write(command === 'image'
    ? 'Image generation and editing now use joyally-image.\n'
    : `Unknown tool: ${command}. Run --help for available tools.\n`);
  process.exit(2);
}
const [name, ...scriptArgs] = command === 'path' || command === 'run'
  ? args : [commands[command], ...args];
if (!name) {
  process.stderr.write(`Missing ${command === 'run' ? 'script name' : 'relative file path'}.\n`);
  process.exit(2);
}
const base = command === 'run' || Object.hasOwn(commands, command)
  ? resolve(skillDir, 'scripts') : resolve(skillDir);
const target = resolve(base, name);
if (!target.startsWith(base + sep) || !existsSync(target)) {
  process.stderr.write('File is outside the Joyally Design directory or does not exist.\n');
  process.exit(2);
}
if (command === 'path') {
  process.stdout.write(`${target}\n`);
  process.exit(0);
}
const runtime = target.endsWith('.py') ? 'python3'
  : target.endsWith('.mjs') ? process.execPath
  : target.endsWith('.sh') ? 'sh' : null;
if (!runtime) {
  process.stderr.write('Only bundled Python, JavaScript and shell scripts can be run.\n');
  process.exit(2);
}
const forwardedArgs = command === 'report' ? [command, ...scriptArgs] : scriptArgs;
const result = spawnSync(runtime, [target, ...forwardedArgs], {
  cwd: process.cwd(), env: process.env, stdio: 'inherit',
});
if (result.error) {
  process.stderr.write(`${result.error.message}\n`);
  process.exit(1);
}
process.exit(result.status ?? 1);
