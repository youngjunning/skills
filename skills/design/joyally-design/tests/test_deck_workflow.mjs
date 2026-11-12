import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtemp, readFile, readdir, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const engine = join(root, 'scripts/design-engine.mjs');
const validator = join(root, 'scripts/validate-joyally-html.mjs');
const run = (script, args) => spawnSync(process.execPath, [script, ...args], { encoding: 'utf8' });

test('a sourced presentation keeps its media, theme, notes and playback assets together', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'joyally-deck-test-'));
  const image = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=', 'base64');
  await writeFile(join(dir, 'photo.png'), image);
  const source = join(dir, 'source.json');
  await writeFile(source, JSON.stringify({ title: '验证 <演示>', theme: 'lake', slides: [
    { type: 'cover', title: '验证 <演示>', subtitle: '内容', notes: '开场讲稿' },
    { type: 'image', title: '图片', image: 'photo.png', alt: '证据图片', fx: 'constellation', notes: '图片讲稿' },
    { type: 'comparison', title: '取舍', headers: ['维度', 'A', 'B'], rows: [['收益', '高', '低']], notes: '比较讲稿' },
  ] }));
  const output = join(dir, 'deck');
  const built = run(engine, ['deck', output, '--source', source, '--theme', 'xiaoxiang']);
  assert.equal(built.status, 0, built.stderr);
  const html = await readFile(join(output, 'index.html'), 'utf8');
  assert.match(html, /验证 &lt;演示&gt;/);
  assert.match(html, /data-theme="xiaoxiang"/);
  assert.match(html, /data-fx="constellation"/);
  assert.match(html, /\.\/media\/2\.png/);
  assert.deepEqual(await readFile(join(output, 'media/2.png')), image);
  assert.equal(JSON.parse(await readFile(join(output, 'deck.json'))).theme, 'xiaoxiang');
  for (const name of ['base.css', 'runtime.js', 'fx-runtime.js', 'fx/constellation.js', 'deck.css', 'themes/xiaoxiang.css', 'LICENSE']) {
    assert.ok((await stat(join(output, 'joyally-design', name))).size > 0, name);
  }
  assert.equal((await readdir(join(output, 'joyally-design'))).includes('report-base.css'), false);
  const checked = run(validator, [join(output, 'index.html')]);
  assert.equal(checked.status, 0, checked.stdout);
  assert.equal(JSON.parse(checked.stdout).warnings.length, 0);
  const standalone = join(dir, 'standalone.html');
  const bundled = run(engine, ['deck-bundle', join(output, 'index.html'), '--out', standalone]);
  assert.equal(bundled.status, 0, bundled.stderr);
  const singleHtml = await readFile(standalone, 'utf8');
  assert.match(singleHtml, /src="data:image\/png;base64,/);
  assert.match(singleHtml, /data-embedded-themes="true"/);
  assert.match(singleHtml, /MIT License/);
  assert.doesNotMatch(singleHtml, /(?:src|href)="\.\/joyally-design\//);
});

test('presentation source rejects remote images and invalid layouts', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'joyally-deck-invalid-'));
  const source = join(dir, 'source.json');
  await writeFile(source, JSON.stringify({ slides: [{ type: 'image', title: '图片', image: 'https://example.com/image.png' }] }));
  assert.notEqual(run(engine, ['deck', join(dir, 'remote'), '--source', source]).status, 0);
  await writeFile(source, JSON.stringify({ slides: [{ type: 'nonexistent', title: '未知' }] }));
  assert.notEqual(run(engine, ['deck', join(dir, 'invalid'), '--source', source]).status, 0);
});
