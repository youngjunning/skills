import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { run } from '../scripts/read.mjs';

const id = '0123456789abcdef';
const text = '# Example\nA verified article.';
const doc = { id, title: 'Example article', sha256: createHash('sha256').update(text).digest('hex') };
const json = value => new Response(JSON.stringify(value), { headers: { 'content-type': 'application/json' } });
function options(overrides = {}) {
  const requests = [];
  return {
    env: { RECORDS_BASE_URL: 'https://records.example' }, requests,
    fetchImpl: async (url, init) => {
      requests.push({ url, init });
      const path = new URL(url).pathname;
      if (path in overrides) return overrides[path]();
      if (path === '/api/catalog') return json({ documents: [doc] });
      if (path === '/api/search') return json([{ id, text }]);
      if (path === '/api/records') return json({ records: [{ id, title: 'Example', text: 'A real choice', visibility: 'shared' }, { id: 'ffffffffffffffff', title: 'Example secret', visibility: 'private' }] });
      if (path === `/api/records/${id}`) return json({ record: { id, visibility: 'shared' } });
      if (path === `/raw/${id}`) return new Response(text, { headers: { 'content-type': 'text/markdown' } });
      if (path === '/api/favorites') return json({ favorites: [{ title: 'Example', visibility: 'shared' }, { title: 'Hidden', visibility: 'private' }] });
      return new Response('', { status: 404 });
    },
  };
}

test('missing target and credential-bearing roots fail before any request', async () => {
  let called = false;
  const fetchImpl = () => { called = true; throw Error('must not fetch'); };
  await assert.rejects(run(['persona'], { env: {}, fetchImpl }), /HTTP/);
  await assert.rejects(run(['--base-url', 'https://user:pass@records.example', 'persona'], { fetchImpl }), /凭证/);
  assert.equal(called, false);
});

test('search filters non-shared records and constructs same-origin source links', async () => {
  const result = await run(['search', 'Example'], options());
  assert.equal(result.records.length, 1);
  assert.equal(result.articles[0].url, `https://records.example/blog/${id}`);
});

test('article validates raw bytes before slicing and exposes continuation', async () => {
  const result = await run(['article', id, '--chars', '10'], options());
  assert.equal(result.content, text.slice(0, 10));
  assert.equal(result.nextOffset, 10);
  assert.equal(result.truncated, true);
  await assert.rejects(run(['article', id], options({ [`/raw/${id}`]: () => new Response('changed', { headers: { 'content-type': 'text/markdown' } }) })), /SHA-256/);
});

test('cross-origin redirects are refused before contacting the second host', async () => {
  const opts = options({ '/api/records': () => new Response('', { status: 302, headers: { location: 'https://login.example' } }) });
  await assert.rejects(run(['record', id], { ...opts, fetchImpl: async (url, init) => {
    opts.requests.push({ url, init });
    return new Response('', { status: 302, headers: { location: 'https://login.example' } });
  } }), /其他站点/);
  assert.equal(opts.requests.length, 1);
});

test('wrong content types, forbidden responses, private records and oversize bodies fail', async () => {
  for (const response of [() => new Response('<html>login</html>', { headers: { 'content-type': 'text/html' } }), () => new Response('', { status: 403 }), () => json({ record: { id, visibility: 'private' } }), () => new Response('x'.repeat(8 * 1024 * 1024 + 1), { headers: { 'content-type': 'application/json' } })]) {
    await assert.rejects(run(['record', id], options({ [`/api/records/${id}`]: response })));
  }
});

test('favorites keep a bounded shared projection', async () => {
  const result = await run(['favorites'], options());
  assert.deepEqual(result.favorites.map(x => x.title), ['Example']);
});
