import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { copyFileSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { run } from '../scripts/read.mjs';

test('主题与本周更新命令有界读取，保留时间语义和整周计数', async () => {
  const env = { RECORDS_BASE_URL: 'https://example.test' };
  const fetchImpl = async url => {
    const path = new URL(url).pathname;
    return new Response(JSON.stringify(path === '/api/subjects' ? { version: 1, subjects: [{ id: 'business', label: '产品与业务' }] } : { version: 1, start: '2026-11-02', end: '2026-11-08', today: '2026-11-07', counts: { favorite: 2 }, entries: [1, 2].map(i => ({ title: '业务方法 ' + i, summary: '运营流程', time: '2026-11-07', timeLabel: '收藏入库', href: '/favorites#' + i })), weekly: { url: '/docs/1111111111111111' } }), { headers: { 'content-type': 'application/json' } });
  };
  const subjects = await run(['subjects'], { env, fetchImpl });
  assert.equal(subjects.subjects[0].siteUrl, 'https://example.test/topics?subject=business');
  const activity = await run(['activity', '--limit', '1'], { env, fetchImpl });
  assert.equal(activity.entries.length, 1);
  assert.equal(activity.totalEntries, 2);
  assert.equal(activity.counts.favorite, 2);
  assert.equal(activity.entries[0].timeLabel, '收藏入库');
  assert.equal(activity.weekly.url, 'https://example.test/docs/1111111111111111');
});

const recordId = '1111111111111111';
const articleId = '2222222222222222';
const otherId = '3333333333333333';
const base = 'https://example.test';
const body = '# ExampleAgent\n这是设计提案，尚未实现。\n';
const sha256 = createHash('sha256').update(body).digest('hex');
const record = { id: recordId, kind: 'judgment', title: 'ExampleAgent 架构', text: '覆盖多端与执行环境管理', visibility: 'shared', date: null, recordedAt: '2026-10-30', relatedIds: [] };
const doc = { id: articleId, title: 'ExampleAgent 架构', date: '2026-11-02T09:12+08:00', updatedAt: '2026-11-02T10:34+08:00', tags: ['Agent'], summary: '设计提案', sha256, kind: 'markdown' };
const research = { id: recordId, title: 'ExampleAgent 执行验证', question: '如何确认任务完成', context: '验证执行结果', nextStep: '观察页面变化', nextStepSource: 'suggested', status: 'todo', result: null, visibility: 'shared', sources: [{ label: '本人问题' }] };
const excerpt = { id: recordId, title: 'ExampleAgent 操作讨论', context: '一次判断纠正', selection: 'discovered', format: 'verbatim', date: null, savedAt: '2026-11-07', visibility: 'shared', messages: [{ role: 'user', text: '先观察业务流程再讨论合作' }, { role: 'assistant', text: '把观察与建议分开' }], source: { label: '会话来源' } };
const objective = { id: 'O1', title: 'Agent 目标', description: '阶段目标而非已完成结果', weight: 60, keyResults: [{ id: 'O1-KR1', title: 'ExampleAgent 执行通道', description: '目标任务量', openQuestions: ['如何衡量效果'] }] };
const material = { id: 'material-1', keyResultId: 'O1-KR1', title: '月报证据', summary: '阶段观察', evidenceNote: '静态记录不代表目标完成' };
const skill = { name: 'example-agent-reader', group: 'self', category: '个人维护', summary: '读取 ExampleAgent 记录', source: '资料主体维护', sourceUrl: '', scope: '全局' };
const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json' } });

test('Skill CLI 从独立安装目录运行，并为非法输入返回非零状态', t => {
  const dir = mkdtempSync(join(tmpdir(), 'personal-records-reader-cli-test-'));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  const script = join(dir, 'read.mjs');
  copyFileSync(new URL('../scripts/read.mjs', import.meta.url), script);
  const help = JSON.parse(execFileSync(process.execPath, [script, '--help'], { cwd: dir, encoding: 'utf8' }));
  assert.ok(help.commands.includes('search QUERY'));
  assert.throws(() => execFileSync(process.execPath, [script, '--base-url', 'https://example.test', 'record', 'invalid'], { cwd: dir, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }), error => error.status === 1 && /16 位/.test(JSON.parse(error.stderr).error));
});

function fixture(overrides = {}) {
  const calls = [];
  const routes = {
    '/api/records': () => json({ version: 2, records: [record, { ...record, id: otherId, visibility: 'private' }, { ...record, id: '4444444444444444', title: '前端架构', text: '其他项目' }] }),
    [`/api/records/${recordId}`]: () => json({ record }),
    '/api/catalog': () => json({ schemaVersion: 1, generatedAt: '2026-10-30', source: { revision: 'abc123', dirty: false }, documents: [doc] }),
    '/api/search': () => json([{ id: articleId, text: body }]),
    [`/raw/${articleId}`]: () => new Response(body, { headers: { 'content-type': 'text/markdown; charset=utf-8' } }),
    '/api/persona': () => json({ recordsUrl: '/api/records', evidence: [] }),
    '/api/favorites': () => json({ version: 1, favorites: [ { id: recordId, kind: 'knowledge', title: '外部 ExampleAgent 资料', url: 'https://example.test/example-agent', savedAt: '2026-11-02T10:34+08:00', visibility: 'shared', selection: 'discovered' }, { id: articleId, kind: 'card', title: '页面观察裁剪', url: null, savedAt: '2026-11-02', card: { understanding: '保留业务信息与页面语义', example: '库存文字', distinction: '裁剪的是观察' }, visibility: 'shared', selection: 'discovered' }, { id: otherId, title: '私人收藏', visibility: 'private' } ] }),
    '/api/research': () => json({ version: 1, items: [research, { ...research, id: otherId, visibility: 'private' }] }),
    '/api/excerpts': () => json({ version: 1, items: [excerpt, { ...excerpt, id: otherId, visibility: 'private' }] }),
    '/api/okr': () => json({ version: 1, period: 'FY27 S2', owner: '资料主体', recordedAt: '2026-11-07', principle: '目标保留依据', source: '本人目标原文', objectives: [objective], materials: [material] }),
    '/api/skills': () => json({ version: 1, updatedAt: '2026-11-07', skills: [skill] }),
    '/api/graph': () => json({ nodes: [{ id: articleId, type: 'document' }, { id: otherId, type: 'document' }, { id: 'topic:architecture', type: 'topic' }], edges: [{ source: articleId, target: otherId, type: 'references', evidence: { line: 12 } }, { source: articleId, target: 'topic:architecture', type: 'belongs_to', evidence: { basis: 'frontmatter' } }] }),
    ...overrides,
  };
  return { calls, fetchImpl: async (url, options) => {
    calls.push(url);
    assert.equal(options.method, 'GET');
    assert.equal(options.redirect, 'manual');
    return (routes[new URL(url).pathname] || (() => json({ error: 'not found' }, 404)))();
  }, env: { RECORDS_BASE_URL: base } };
}

test('Skill 检索排除私人记录和只匹配泛词的其他项目，返回可回查链接', async () => {
  const result = await run(['search', 'ExampleAgent 架构'], fixture());
  assert.deepEqual(result.records.map(hit => hit.id), [recordId]);
  assert.equal(result.articles[0].id, articleId);
  assert.equal(result.articles[0].updatedAt, '2026-11-02T10:34+08:00');
  assert.equal('publication' in result.articles[0], false);
  assert.equal(result.records[0].url, `${base}/records/${recordId}`);
  assert.equal(result.snapshot.revision, 'abc123');
  const empty = await run(['search', 'unrecorded-topic-xyz123'], fixture());
  assert.equal(empty.records.length + empty.articles.length, 0);
});

test('Skill 校验原文后分页，能完整还原中文正文', async () => {
  const first = await run(['article', articleId, '--chars', '12'], fixture());
  const rest = await run(['article', articleId, '--offset', String(first.nextOffset)], fixture());
  assert.equal(first.content + rest.content, body);
  assert.equal(first.truncated, true);
  assert.equal(rest.truncated, false);
  assert.equal(rest.nextOffset, null);
  assert.equal(first.sha256, sha256);
  assert.equal(first.date, '2026-11-02T09:12+08:00');
  assert.equal(first.updatedAt, '2026-11-02T10:34+08:00');
});

test('Skill 不把快照不一致或不可见文章当作已读取的证据', async () => {
  await assert.rejects(run(['article', articleId], fixture({ [`/raw/${articleId}`]: () => new Response('另一版', { headers: { 'content-type': 'text/plain' } }) })), /SHA-256/);
  const source = fixture();
  await assert.rejects(run(['article', otherId], source), /不在当前可见目录/);
  assert.equal(source.calls.length, 1);
});

test('Skill 在 SSO 跳转、登录 HTML 和无权限时明确失败，不访问其他站点', async () => {
  for (const response of [
    () => new Response(null, { status: 302, headers: { location: 'https://login.example.test/sso' } }),
    () => new Response('<html>Login</html>', { headers: { 'content-type': 'text/html' } }),
    () => json({ error: 'forbidden' }, 403),
  ]) {
    const source = fixture({ '/api/persona': response });
    await assert.rejects(run(['persona'], source), /登录|权限/);
    assert.deepEqual(source.calls, [`${base}/api/persona`]);
  }
});

test('Skill 参数覆盖环境地址，拒绝含凭证地址及非法记录 ID', async () => {
  const source = fixture();
  const result = await run(['persona', '--base-url', 'https://other.example.test'], source);
  assert.equal(result.url, 'https://other.example.test/');
  assert.equal(source.calls[0], 'https://other.example.test/api/persona');
  for (const url of ['https://user:secret@example.test', 'file:///tmp/test', 'https://example.test/path', 'https://example.test/?key=secret']) {
    await assert.rejects(run(['persona', '--base-url', url], fixture()), /根地址|凭证/);
  }
  await assert.rejects(run(['record', '../../etc/passwd'], fixture()), /16 位/);
});

test('Skill 图谱保留真实引用证据，并单独输出主题归属', async () => {
  const result = await run(['graph', articleId], fixture());
  assert.equal(result.references.length, 1);
  assert.equal(result.references[0].evidence.line, 12);
  assert.equal(result.topicMemberships.length, 1);
  assert.equal(result.nodes.find(node => node.id === otherId).url, `${base}/blog/${otherId}`);
});

test('Skill 收藏保留会话发现标记并排除私人收藏', async () => {
  const result = await run(['favorites', 'ExampleAgent'], fixture());
  assert.equal(result.favorites.length, 1);
  assert.equal(result.favorites[0].selection, 'discovered');
  assert.equal(result.favorites[0].siteUrl, `${base}/favorites#${recordId}`);
  assert.equal(result.favorites[0].savedAt, '2026-11-02T10:34+08:00');
  const card = await run(['favorites', '库存文字'], fixture());
  assert.equal(card.favorites[0].kind, 'card');
  assert.equal(card.favorites[0].url, null);
  assert.equal(card.favorites[0].siteUrl, `${base}/favorites#${articleId}`);
  assert.equal((await run(['favorites'], fixture())).favorites.some(item => item.visibility === 'private'), false);
});

test('Skill 不把 HTTP 失败、错误结构或读取超限当作无搜索结果', async () => {
  await assert.rejects(run(['record', otherId], fixture()), /HTTP 404/);
  await assert.rejects(run(['search', 'ExampleAgent'], fixture({ '/api/search': () => json({ wrong: true }) })), /格式不匹配/);
  await assert.rejects(run(['persona'], fixture({ '/api/persona': () => new Response('x'.repeat(8 * 1024 * 1024 + 1), { headers: { 'content-type': 'application/json' } }) })), /8 MiB/);
});

test('统一检索覆盖七类内容，保留角色、目标、采用边界并只调用读取接口', async () => {
  const source = fixture();
  const result = await run(['search', 'ExampleAgent'], source);
  for (const key of ['records', 'articles', 'favorites', 'research', 'excerpts', 'okr', 'skills']) assert.equal(result[key].length, 1, key);
  assert.equal(result.research[0].nextStepSource, 'suggested');
  assert.equal(result.research[0].siteUrl, `${base}/research#${recordId}`);
  assert.equal(result.excerpts[0].selection, 'discovered');
  assert.deepEqual(result.excerpts[0].messages.map(item => item.role), ['user', 'assistant']);
  assert.equal(result.excerpts[0].siteUrl, `${base}/excerpts#${recordId}`);
  assert.equal(result.okr[0].period, 'FY27 S2');
  assert.deepEqual(result.okr[0].materials, [material]);
  assert.equal(result.okr[0].siteUrl, `${base}/okr#O1`);
  assert.equal(result.skills[0].siteUrl, `${base}/skills`);
  assert.equal(result.skills[0].source, '资料主体维护');
  assert.ok(source.calls.every(url => new URL(url).origin === base && !url.includes('/api/chat')));
});

test('各类读取使用真实响应结构，检索嵌套消息、关键结果及月报素材', async () => {
  const questions = await run(['research', '页面变化'], fixture());
  assert.equal(questions.research[0].status, 'todo');
  assert.equal(questions.research.length, 1);
  const quotes = await run(['excerpts', '业务流程'], fixture());
  assert.equal(quotes.excerpts[0].format, 'verbatim');
  assert.equal(quotes.excerpts[0].source.label, '会话来源');
  const goals = await run(['okr', '月报证据'], fixture());
  assert.equal(goals.period, 'FY27 S2');
  assert.equal(goals.source, '本人目标原文');
  assert.equal(goals.objectives[0].keyResults[0].openQuestions[0], '如何衡量效果');
  const catalog = await run(['skills', '读取'], fixture());
  assert.equal(catalog.updatedAt, '2026-11-07');
  assert.equal(catalog.skills[0].name, 'example-agent-reader');
});

test('清单与统一检索均遵守每类数量上限，空命中不使用其他内容补齐', async () => {
  const repeated = fixture({
    '/api/research': () => json({ items: [research, { ...research, id: articleId }] }),
    '/api/excerpts': () => json({ items: [excerpt, { ...excerpt, id: articleId }] }),
    '/api/okr': () => json({ period: 'FY27 S2', objectives: [objective, { ...objective, id: 'O2' }], materials: [material] }),
    '/api/skills': () => json({ version: 1, updatedAt: '2026-11-07', skills: [skill, { ...skill, name: 'example-agent-other' }] }),
  });
  for (const [command, key] of [['research', 'research'], ['excerpts', 'excerpts'], ['okr', 'objectives'], ['skills', 'skills']]) {
    assert.equal((await run([command, '--limit', '1'], repeated))[key].length, 1);
    assert.deepEqual((await run([command, 'unrecorded-topic-xyz123'], repeated))[key], []);
  }
  const result = await run(['search', 'ExampleAgent', '--limit', '1'], repeated);
  for (const key of ['records', 'articles', 'favorites', 'research', 'excerpts', 'okr', 'skills']) assert.ok(result[key].length <= 1);
  const empty = await run(['search', 'unrecorded-topic-xyz123'], repeated);
  for (const key of ['records', 'articles', 'favorites', 'research', 'excerpts', 'okr', 'skills']) assert.deepEqual(empty[key], []);
  await assert.rejects(run(['skills', '--limit', '21'], repeated), /1–20/);
});

test('新增接口不存在或结构不匹配时明确失败，不能伪装成空结果', async () => {
  for (const [command, path, data] of [
    ['research', '/api/research', { research: [] }],
    ['excerpts', '/api/excerpts', { items: [null] }],
    ['okr', '/api/okr', { objectives: [], materials: null, period: 'FY27 S2' }],
    ['skills', '/api/skills', { version: 1, skills: [] }],
  ]) await assert.rejects(run([command], fixture({ [path]: () => json(data) })), /格式不匹配/);
  const failed = fixture({ '/api/research': () => json({ error: 'missing' }, 404) });
  await assert.rejects(run(['research'], failed), /HTTP 404/);
  await assert.rejects(run(['search', 'ExampleAgent'], failed), /HTTP 404/);
});

const methodNote = { id: recordId, kind: 'note', type: 'method', title: '从实际场景寻找合作切入点', url: null,
  summary: '先观察实际流程，再讨论合作', reason: '本人学习收获', tags: ['业务调研'], subjects: ['business'],
  attribution: 'user', selection: 'discovered', visibility: 'shared', savedAt: '2026-11-07',
  note: { body: '讨论合作前先观察运营的实际流程；这是方法收获，尚未陈述执行结果。', date: null, recordedAt: '2026-11-07' },
  sources: [{ label: '本人表达' }] };
const conceptNote = { ...methodNote, id: articleId, type: 'concept', title: 'ExampleVision Noul 与 Box', attribution: 'ai',
  subjects: ['grounding', 'agents'], tags: ['ExampleVision'], note: { body: 'Noul 判断存在性，Box 返回目标位置；资料整理不证明本人已验证。', date: null, recordedAt: '2026-11-07' }, sources: [{ label: '官方文档', url: 'https://example.test/docs' }] };
const usedDesign = { ...methodNote, id: otherId, kind: 'resource', type: 'tool', title: '设计工具', attribution: 'source',
  url: 'https://example.test/design', note: undefined, subjects: ['design'], tags: ['界面设计'],
  usages: [{ project: '项目 A', projectUrl: 'https://example.test/project-a', stage: 'trial', purpose: '参考交互', evidence: '原型中已试用选定交互' }, { project: '项目 B', projectUrl: 'https://example.test/project-b', stage: 'adopted', purpose: '主题来源', evidence: '主题已引用选定资源' }] };
const v2 = () => ({ version: 2, favorites: [methodNote, conceptNote, usedDesign] });

test('百宝箱 v2 按知识正文、主题和真实使用查找，保留归属与项目差异', async () => {
  const source = fixture({ '/api/favorites': () => json(v2()) });
  const method = await run(['favorites', '实际流程', '--type', 'method', '--subject', 'business'], source);
  assert.deepEqual(method.favorites.map(item => item.id), [recordId]);
  assert.equal(method.favorites[0].attribution, 'user');
  assert.equal(method.favorites[0].note.example, undefined);
  const concept = await run(['search', 'ExampleVision'], source);
  assert.equal(concept.favorites[0].attribution, 'ai');
  assert.equal(concept.favorites[0].siteUrl, `${base}/favorites#${articleId}`);
  const tools = await run(['favorites', '--subject', 'design', '--used'], source);
  assert.deepEqual(tools.favorites.map(item => item.id), [otherId]);
  assert.deepEqual(tools.favorites[0].usages.map(usage => usage.stage), ['trial', 'adopted']);
  assert.equal((await run(['favorites', '--type', 'concept', '--used'], source)).favorites.length, 0);
  await assert.rejects(run(['favorites', '--type', 'card'], source), /--type/);
  await assert.rejects(run(['favorites', '--subject', 'unconfigured'], source), /主题/);
});

test('单条知识笔记读取核对身份，旧站点只对 v1 回退集合', async () => {
  const source = fixture({ '/api/favorites': () => json(v2()), [`/api/favorites/${recordId}`]: () => json({ favorite: methodNote }) });
  const result = await run(['favorite', recordId], source);
  assert.equal(result.favorite.note.body, methodNote.note.body);
  assert.equal(result.favorite.attribution, 'user');
  assert.deepEqual(source.calls, [`${base}/api/favorites/${recordId}`]);
  const legacy = await run(['favorite', recordId], fixture());
  assert.equal(legacy.favorite.kind, 'knowledge');
  await assert.rejects(run(['favorite', recordId], fixture({ '/api/favorites': () => json(v2()) })), /HTTP 404/);
  await assert.rejects(run(['favorite', recordId], fixture({ [`/api/favorites/${recordId}`]: () => json({ favorite: conceptNote }) })), /不同的身份/);
  await assert.rejects(run(['favorite', recordId], fixture({ [`/api/favorites/${recordId}`]: () => json({ favorite: { ...methodNote, visibility: 'private' } }) })), /共享/);
});

test('百宝箱 v2 非法归属及未知版本明确失败，笔记图谱保留关系证据', async () => {
  await assert.rejects(run(['favorites'], fixture({ '/api/favorites': () => json({ version: 2, favorites: [{ ...methodNote, attribution: 'adopted' }] }) })), /v2/);
  await assert.rejects(run(['favorites'], fixture({ '/api/favorites': () => json({ version: 3, favorites: [] }) })), /版本/);
  const id = 'favorite:' + recordId;
  const edge = { source: id, target: 'subject:business', type: 'tagged', evidence: { basis: '已审核主题' } };
  const data = await run(['graph', id], fixture({ '/api/graph': () => json({ nodes: [{ id, type: 'favorite' }, { id: 'subject:business', type: 'topic' }], edges: [edge] }) }));
  assert.equal(data.url, `${base}/favorites#${recordId}`);
  assert.deepEqual(data.relations, [edge]);
  assert.equal(data.references.length, 0);
});


test('catalog article links take precedence, preserve publication metadata, and remain same-origin', async () => {
  const catalog = value => fixture({ '/api/catalog': () => json({ documents: [{ ...doc, ...value }] }) });
  const result = await run(['article', articleId], catalog({ url: '/docs/' + articleId, publication: { status: 'published' } }));
  assert.equal(result.url, base + '/docs/' + articleId);
  assert.deepEqual(result.publication, { status: 'published' });
  await assert.rejects(run(['article', articleId], catalog({ url: 'https://other.example/article' })), /同源/);
  const graph = await run(['graph', articleId], fixture());
  assert.equal(graph.url, base + '/blog/' + articleId);
});
