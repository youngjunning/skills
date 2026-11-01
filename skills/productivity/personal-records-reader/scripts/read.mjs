#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { existsSync, realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const DEFAULT_BASE = undefined;
const ID = /^[a-f0-9]{16}$/;
const MAX_BYTES = 8 * 1024 * 1024;
const STOP = new Set(['什么', '如何', '怎么', '哪些', '是否', '关于', '一下', '介绍', '记录', '问题', '他的', '看法', 'what', 'is', 'a', 'the', 'of', 'and', 'or', 'for', 'with', 'how', 'does', 'about', 'show', 'me']);

function parseArgs(args) {
  const options = {};
  const positional = [];
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--help' || arg === '-h') return { help: true };
    if (!arg.startsWith('--')) { positional.push(arg); continue; }
    if (!['--base-url', '--limit', '--offset', '--chars'].includes(arg)) throw new Error(`未知参数：${arg}`);
    const value = args[++i];
    if (!value || value.startsWith('--')) throw new Error(`${arg} 缺少参数值`);
    options[arg.slice(2)] = value;
  }
  return { ...options, command: positional.shift(), values: positional };
}

function integer(value, fallback, min, max, label) {
  const n = value === undefined ? fallback : Number(value);
  if (!Number.isSafeInteger(n) || n < min || n > max) throw new Error(`${label} 必须为 ${min}–${max} 的整数`);
  return n;
}

function baseUrl(value) {
  let url;
  try { url = new URL(value); } catch { throw new Error('站点地址必须是完整的 HTTP(S) 根地址'); }
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash || url.pathname !== '/') {
    throw new Error('站点地址只接受 HTTP(S) 根地址，不接受凭证、子路径、查询参数或片段');
  }
  return url;
}

async function bodyBytes(response) {
  const chunks = [];
  let size = 0;
  const reader = response.body?.getReader();
  if (!reader) return Buffer.alloc(0);
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > MAX_BYTES) throw new Error('接口内容超过 8 MiB 读取上限');
      chunks.push(Buffer.from(value));
    }
  } finally { await reader.cancel().catch(() => {}); reader.releaseLock(); }
  return Buffer.concat(chunks);
}

function termsFor(query) {
  const words = query.normalize('NFKC').toLowerCase().match(/[a-z0-9][a-z0-9_.+-]*|[\p{Script=Han}]+/gu) || [];
  return [...new Set(words.flatMap(word => /\p{Script=Han}/u.test(word) && word.length > 2
    ? [word, ...Array.from({ length: word.length - 1 }, (_, i) => word.slice(i, i + 2))]
    : [word]).filter(word => !STOP.has(word)))];
}

function rank(items, query, fields, limit) {
  const terms = termsFor(query);
  const latinTerms = terms.filter(term => /^[a-z0-9]/.test(term));
  const candidates = latinTerms.length ? items.filter(item => {
    const text = fields.map(([key]) => Array.isArray(item[key]) ? item[key].join(' ') : item[key] || '').join(' ').normalize('NFKC').toLowerCase();
    return latinTerms.some(term => text.includes(term));
  }) : items;
  return candidates.map(item => ({ item, score: fields.reduce((score, [key, weight]) => {
    const text = String(Array.isArray(item[key]) ? item[key].join(' ') : item[key] || '').normalize('NFKC').toLowerCase();
    return score + terms.filter(term => text.includes(term)).length * weight;
  }, 0) })).filter(hit => hit.score > 0).sort((a, b) => b.score - a.score).slice(0, limit).map(hit => hit.item);
}

function snippet(value, query, chars = 320) {
  const text = String(value || '');
  const lower = text.toLowerCase();
  const positions = termsFor(query).map(term => lower.indexOf(term)).filter(pos => pos >= 0);
  const start = Math.max(0, (positions.length ? Math.min(...positions) : 0) - 70);
  return (start ? '…' : '') + text.slice(start, start + chars) + (start + chars < text.length ? '…' : '');
}

export async function run(args, { fetchImpl = globalThis.fetch, env = process.env } = {}) {
  const options = parseArgs(args);
  if (options.help || !options.command) return { commands: ['persona', 'search QUERY', 'record ID', 'article ID', 'graph ID', 'favorites [QUERY]'], options: ['--base-url URL', '--limit 1..20', '--offset N', '--chars 1..40000'] };
  const base = baseUrl(options['base-url'] || env.RECORDS_BASE_URL || DEFAULT_BASE);
  const urlFor = path => new URL(path, base).href;
  const limit = integer(options.limit, 6, 1, 20, '--limit');
  const offset = integer(options.offset, 0, 0, Number.MAX_SAFE_INTEGER, '--offset');
  const chars = integer(options.chars, 12000, 1, 40000, '--chars');
  const [id] = options.values;
  const query = options.values.join(' ').trim();
  if (query.length > 512) throw new Error('查询内容不能超过 512 个字符');
  if (['record', 'article', 'graph'].includes(options.command) && (options.values.length !== 1 || !ID.test(id))) throw new Error('请提供一个 16 位小写十六进制 ID');

  async function get(path, raw = false) {
    let url = new URL(path, base);
    const signal = AbortSignal.timeout(15000);
    for (let redirects = 0; redirects <= 4; redirects++) {
      if (url.origin !== base.origin) throw new Error('接口跳转到其他站点；请使用已登录浏览器检查站点访问权限');
      const response = await fetchImpl(url.href, { method: 'GET', redirect: 'manual', signal, headers: { Accept: raw ? 'text/markdown, text/plain' : 'application/json' } });
      if (response.status >= 300 && response.status < 400 && response.headers.get('location')) {
        await response.body?.cancel();
        url = new URL(response.headers.get('location'), url);
        continue;
      }
      if ([401, 403].includes(response.status)) { await response.body?.cancel(); throw new Error(`HTTP ${response.status}：需要站点访问权限，请在已登录浏览器中检查`); }
      if (!response.ok) { await response.body?.cancel(); throw new Error(`读取 ${path} 失败：HTTP ${response.status}`); }
      const type = response.headers.get('content-type') || '';
      if ((!raw && !type.includes('application/json')) || (raw && !/^text\/(plain|markdown)\b/i.test(type))) {
        await response.body?.cancel();
        throw new Error(`读取 ${path} 时返回了非预期内容，可能是登录页；请通过已登录浏览器检查`);
      }
      const bytes = await bodyBytes(response);
      if (raw) return bytes;
      try { return JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/, '')); } catch { throw new Error(`读取 ${path} 时返回的 JSON 无效`); }
    }
    throw new Error('接口重定向次数过多；请检查站点地址和访问权限');
  }

  const getRecords = async () => {
    const data = await get('/api/records');
    if (!Array.isArray(data.records)) throw new Error('个人记录接口格式不匹配');
    return data.records.filter(record => record.visibility === 'shared');
  };
  const getCatalog = async () => {
    const data = await get('/api/catalog');
    if (!Array.isArray(data.documents)) throw new Error('文章目录接口格式不匹配');
    return data;
  };
  const snapshot = catalog => ({ generatedAt: catalog.generatedAt, revision: catalog.source?.revision, dirty: catalog.source?.dirty });
  const articleLink = doc => ({ id: doc.id, title: doc.title, date: doc.date, url: urlFor(`/blog/${doc.id}`), rawUrl: urlFor(`/raw/${doc.id}`), publication: doc.publication });

  switch (options.command) {
    case 'persona': {
      const data = await get('/api/persona');
      if (!data.recordsUrl || !Array.isArray(data.evidence)) throw new Error('个人介绍接口格式不匹配');
      return { url: urlFor('/'), ...data };
    }
    case 'search': {
      if (!query) throw new Error('search 需要提供关键词');
      const [records, catalog, search] = await Promise.all([getRecords(), getCatalog(), get('/api/search')]);
      if (!Array.isArray(search)) throw new Error('全文索引接口格式不匹配');
      const textById = new Map(search.map(row => [row.id, row.text]));
      const documents = catalog.documents.filter(doc => ID.test(doc.id)).map(doc => ({ ...doc, text: textById.get(doc.id) || '' }));
      return { query, snapshot: snapshot(catalog), records: rank(records, query, [['title', 8], ['text', 3], ['context', 1]], limit).map(record => ({ id: record.id, kind: record.kind, title: record.title, date: record.date, recordedAt: record.recordedAt, snippet: snippet(record.text, query), url: urlFor(`/records/${record.id}`), relatedIds: record.relatedIds, articleId: record.articleId })), articles: rank(documents, query, [['title', 8], ['tags', 5], ['summary', 3], ['text', 1]], limit).map(doc => ({ ...articleLink(doc), snippet: snippet(doc.text || doc.summary, query) })) };
    }
    case 'record': {
      const data = await get(`/api/records/${id}`);
      if (data.record?.id !== id || data.record.visibility !== 'shared') throw new Error('未获得对应的共享记录');
      return { url: urlFor(`/records/${id}`), ...data };
    }
    case 'article': {
      const catalog = await getCatalog();
      const doc = catalog.documents.find(row => row.id === id);
      if (!doc) throw new Error('文章不在当前可见目录中');
      const bytes = await get(`/raw/${id}`, true);
      const sha256 = createHash('sha256').update(bytes).digest('hex');
      if (doc.sha256 !== sha256) throw new Error('原文与目录 SHA-256 不一致，请重新检索后读取');
      const content = bytes.toString('utf8');
      if (offset > content.length) throw new Error('--offset 超出文章长度');
      const end = Math.min(offset + chars, content.length);
      return { ...articleLink(doc), snapshot: snapshot(catalog), kind: doc.kind, sha256, offset, totalChars: content.length, truncated: end < content.length, nextOffset: end < content.length ? end : null, content: content.slice(offset, end) };
    }
    case 'graph': {
      const graph = await get('/api/graph');
      if (!Array.isArray(graph.nodes) || !Array.isArray(graph.edges)) throw new Error('图谱接口格式不匹配');
      if (!graph.nodes.some(node => node.id === id && node.type === 'document')) throw new Error('文章不在当前可见图谱中');
      const edges = graph.edges.filter(edge => edge.source === id || edge.target === id);
      const ids = new Set(edges.flatMap(edge => [edge.source, edge.target]));
      return { id, url: urlFor(`/blog/${id}`), snapshot: snapshot(graph), nodes: graph.nodes.filter(node => node.id === id || ids.has(node.id)).map(node => ({ ...node, ...(node.type === 'document' && ID.test(node.id) ? { url: urlFor(`/blog/${node.id}`) } : {}) })), references: edges.filter(edge => edge.type === 'references'), topicMemberships: edges.filter(edge => edge.type === 'belongs_to') };
    }
    case 'favorites': {
      const data = await get('/api/favorites');
      if (!Array.isArray(data.favorites)) throw new Error('收藏接口格式不匹配');
      const items = data.favorites.filter(item => item.visibility === 'shared');
      const hits = query ? rank(items, query, [['title', 8], ['tags', 5], ['summary', 3], ['reason', 1]], limit) : items.slice(0, limit);
      return { query, siteUrl: urlFor('/favorites'), favorites: hits };
    }
    default: throw new Error(`未知命令：${options.command}`);
  }
}

if (process.argv[1] && existsSync(process.argv[1]) && realpathSync(process.argv[1]) === realpathSync(fileURLToPath(import.meta.url))) {
  run(process.argv.slice(2)).then(result => process.stdout.write(JSON.stringify(result, null, 2) + '\n')).catch(error => {
    const message = error.name === 'TimeoutError' || error.name === 'AbortError' ? '读取超时，请检查网络与站点地址' : error.message;
    process.stderr.write(JSON.stringify({ error: message }) + '\n');
    process.exitCode = 1;
  });
}
