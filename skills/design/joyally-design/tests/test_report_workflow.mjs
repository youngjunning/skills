import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtemp, readFile, readdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const engine = join(root, 'scripts/design-engine.mjs');
const validator = join(root, 'scripts/validate-joyally-html.mjs');
const run = (script, args) => spawnSync(process.execPath, [script, ...args], { encoding: 'utf8' });

test('report packages only Joyally report CSS and rejects deck overwrite', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'joyally-report-test-'));
  const output = join(dir, 'report');
  const built = run(engine, ['report', output, '--title', '独立报告']);
  assert.equal(built.status, 0, built.stderr);
  const html = await readFile(join(output, 'index.html'), 'utf8');
  assert.match(html, /<body class="joyally-report">/);
  assert.match(html, /独立报告/);
  assert.deepEqual((await readdir(join(output, 'joyally-design'))).sort(), ['joyally-theme.css', 'report-base.css']);
  const theme = await readFile(join(output, 'joyally-design/joyally-theme.css'), 'utf8');
  assert.doesNotMatch(theme, /joyally-deck|pakco|html-ppt/);
  assert.equal(run(validator, [join(output, 'index.html')]).status, 0);
  assert.equal(run(engine, ['deck', output]).status, 3);
});
