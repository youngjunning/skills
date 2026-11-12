import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { mkdtemp, readFile, readdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const engine = join(root, 'scripts/design-engine.mjs');
const run = (args) => spawnSync(process.execPath, [engine, ...args], { encoding: 'utf8' });

test('social card builds a portable image and escapes supplied copy', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'joyally-social-test-'));
  const output = join(dir, 'card');
  const created = run(['social-card', output, '--style', 'poster', '--layout', 'insight',
    '--title', '结论 <A>', '--subtitle', '依据 & 下一步', '--highlight', '39 分钟',
    '--credit', '作者 & 来源', '--page', '02', '--total', '03']);
  assert.equal(created.status, 0, created.stderr);
  const html = await readFile(join(output, 'index.html'), 'utf8');
  assert.match(html, /结论 &lt;A&gt;/);
  assert.match(html, /依据 &amp; 下一步/);
  assert.match(html, /作者 &amp; 来源/);
  assert.match(html, /social-card--poster social-card--insight/);
  assert.deepEqual(await readdir(join(output, 'joyally-design')), ['social-card.css']);
  assert.notEqual(run(['social-card', output, '--title', 'x', '--subtitle', 'y', '--credit', 'z']).status, 0);
  assert.notEqual(run(['social-card', join(dir, 'bad'), '--style', 'unknown', '--title', 'x', '--subtitle', 'y', '--credit', 'z']).status, 0);
  assert.notEqual(run(['social-card', join(dir, 'no-credit'), '--title', 'x', '--subtitle', 'y']).status, 0);

  const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  if (!existsSync(chrome)) return;
  const rendered = run(['social-render', join(output, 'index.html'), '--scale', '1']);
  assert.equal(rendered.status, 0, rendered.stderr);
  const png = await readFile(join(output, 'card.png'));
  assert.equal(png.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
  assert.equal(png.readUInt32BE(16), 1080);
  assert.equal(png.readUInt32BE(20), 1440);
});
