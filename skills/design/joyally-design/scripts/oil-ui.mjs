#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const skillDir = dirname(dirname(fileURLToPath(import.meta.url)));
const commands = {
  explore: ['python3', 'scripts/build_explorer.py'],
  shoot: [process.execPath, 'scripts/shoot.mjs'],
  media: [process.execPath, 'scripts/curate-media.mjs'],
  'prep-image': [process.execPath, 'scripts/prep-image.mjs'],
  measure: ['python3', 'scripts/measure_reference.py'],
  'design-check': ['python3', 'scripts/check_design_md.py'],
  image: [process.execPath, 'scripts/oiloil-image.mjs'],
};

const [command, ...args] = process.argv.slice(2);
if (!command || command === '--help') {
  process.stdout.write(`Usage: node <joyally-dir>/scripts/oil-ui.mjs <${Object.keys(commands).join('|')}> [original tool arguments]\n`);
  process.exit(command ? 0 : 2);
}
if (!Object.hasOwn(commands, command)) {
  process.stderr.write(`Unknown tool: ${command}. Run --help for available tools.\n`);
  process.exit(2);
}

const found = spawnSync(process.execPath, [join(skillDir, 'scripts', 'find-oil-ui-pro.mjs')], {
  encoding: 'utf8',
});
if (found.status !== 0) {
  process.stderr.write(found.stderr || 'Unable to locate oil-ui-pro.\n');
  process.exit(found.status ?? 1);
}

const { root, version, bridgeVersion } = JSON.parse(found.stdout);
if (version !== bridgeVersion) {
  process.stderr.write(`oil-ui-pro ${version} differs from the reviewed ${bridgeVersion} integration. Read its current SKILL.md and verify tool arguments before running it.\n`);
  process.exit(3);
}

const [runtime, relativePath] = commands[command];
const result = spawnSync(runtime, [join(root, relativePath), ...args], {
  cwd: process.cwd(),
  env: process.env,
  stdio: 'inherit',
});
if (result.error) {
  process.stderr.write(`${result.error.message}\n`);
  process.exit(1);
}
process.exit(result.status ?? 1);
