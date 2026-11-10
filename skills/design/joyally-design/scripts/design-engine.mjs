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
  image: 'joyally-image.mjs',
  cards: 'build_cards.py',
};
const [command, ...args] = process.argv.slice(2);
if (!command || command === '--help') {
  process.stdout.write(`Usage: node <joyally-dir>/scripts/design-engine.mjs <${Object.keys(commands).join('|')}|path|run> [tool arguments]
path <relative-file>: show a bundled reference, asset or script path
run <script-name> [...arguments]: run a bundled script
`);
  process.exit(command ? 0 : 2);
}
if (!Object.hasOwn(commands, command) && command !== 'path' && command !== 'run') {
  process.stderr.write(`Unknown tool: ${command}. Run --help for available tools.\n`);
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
const result = spawnSync(runtime, [target, ...scriptArgs], {
  cwd: process.cwd(), env: process.env, stdio: 'inherit',
});
if (result.error) {
  process.stderr.write(`${result.error.message}\n`);
  process.exit(1);
}
process.exit(result.status ?? 1);
