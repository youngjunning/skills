#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { access, mkdir, writeFile } from 'node:fs/promises';
import { constants } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const outputArg = process.argv[2];
if (!outputArg || outputArg === '--help') {
  process.stdout.write('Usage: deck-gallery <output-dir>\n');
  process.exit(outputArg === '--help' ? 0 : 2);
}
const output = resolve(outputArg);
try { await access(output, constants.F_OK); console.error(`Refusing to overwrite existing directory: ${output}`); process.exit(3); } catch (error) { if (error.code !== 'ENOENT') throw error; }
await mkdir(output, { recursive: true });
const builder = join(dirname(fileURLToPath(import.meta.url)), 'build-joyally-deck.mjs');
const themes = [
  ['lake', '青山湖'], ['west-lake', '西湖'], ['suzhou', '苏州园林'],
  ['maldives', '马尔代夫'], ['alpine', '阿尔卑斯雪山'], ['xiaoxiang', '小香风'], ['space', '太空'],
];
const scenarios = [
  ['tech-sharing', '技术分享'], ['project-report', '项目汇报'],
  ['product-launch', '产品发布'], ['pitch-deck', '提案演示'],
];
const layoutSamples = [
  ['cover', '封面', { subtitle: '用一句话交代演示主题' }],
  ['agenda', '目录', { items: ['背景', '判断', '证据', '下一步'] }],
  ['section', '章节页', { number: '01', subtitle: '给观众清楚的转场' }],
  ['statement', '核心判断', { body: '这一页只讲一个观点。' }],
  ['cards', '并列要点', { items: [{ title: '要点一', body: '说明内容' }, { title: '要点二', body: '说明内容' }, { title: '要点三', body: '说明内容' }] }],
  ['columns', '双栏', { left: { title: '现状', body: '已有事实' }, right: { title: '目标', body: '预期结果' } }],
  ['metrics', '指标', { items: [{ value: '92%', label: '完成率' }, { value: '18', label: '已验证项' }] }],
  ['comparison', '对比表', { headers: ['维度', '方案 A', '方案 B'], rows: [['收益', '较高', '适中'], ['成本', '适中', '较低']] }],
  ['timeline', '时间线', { items: [{ label: '第一步', title: '验证', body: '建立证据' }, { label: '第二步', title: '实施', body: '完成交付' }] }],
  ['chart', '条形图', { chartType: 'bar', items: [{ label: '当前', value: 42 }, { label: '目标', value: 78 }], caption: '示例数据' }],
  ['chart', '折线图', { chartType: 'line', items: [{ label: '一月', value: 22 }, { label: '二月', value: 46 }, { label: '三月', value: 78 }], caption: '示例数据' }],
  ['chart', '环形图', { chartType: 'donut', items: [{ label: '第一类', value: 42 }, { label: '第二类', value: 35 }, { label: '其他', value: 23 }], caption: '示例数据' }],
  ['chart', '雷达图', { chartType: 'radar', items: [{ label: '质量', value: 82 }, { label: '速度', value: 68 }, { label: '成本', value: 45 }, { label: '体验', value: 75 }], caption: '示例数据' }],
  ['code', '代码', { code: 'const result = await run();\nconsole.log(result);' }],
  ['image', '图片', { alt: '图片占位', caption: '加入真实截图与来源' }],
  ['quote', '引述', { quote: '把重要的原话放在这里。', attribution: '出处' }],
  ['closing', '结语', { subtitle: '留下具体的下一步' }],
];
for (const [name] of themes) {
  const result = spawnSync(process.execPath, [builder, join(output, `theme-${name}`), '--scenario', 'tech-sharing', '--theme', name], { encoding: 'utf8' });
  if (result.status !== 0) throw new Error(result.stderr || `Cannot build ${name}`);
}
for (const [name] of scenarios) {
  const result = spawnSync(process.execPath, [builder, join(output, `scenario-${name}`), '--scenario', name, '--theme', 'lake'], { encoding: 'utf8' });
  if (result.status !== 0) throw new Error(result.stderr || `Cannot build ${name}`);
}
const layoutSource = join(output, 'layout-source.json');
await writeFile(layoutSource, JSON.stringify({ title: '版式展示', theme: 'lake', slides: layoutSamples.map(([type, title, fields]) => ({ type, title, ...fields })) }));
const layoutResult = spawnSync(process.execPath, [builder, join(output, 'layouts'), '--source', layoutSource], { encoding: 'utf8' });
if (layoutResult.status !== 0) throw new Error(layoutResult.stderr || 'Cannot build layout gallery');
const cards = (entries, prefix) => entries.map(([name, label]) => `<a class="card" href="./${prefix}-${name}/index.html"><iframe title="${label}预览" src="./${prefix}-${name}/index.html?preview=1" loading="lazy" tabindex="-1"></iframe><span>${label}</span></a>`).join('');
const layoutCards = layoutSamples.map(([, label], index) => `<a class="card" href="./layouts/index.html#/${index + 1}"><iframe title="${label}预览" src="./layouts/index.html?preview=${index + 1}" loading="lazy" tabindex="-1"></iframe><span>${label}</span></a>`).join('');
const html = `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Joyally Design · 演示文稿画廊</title><style>
:root{color-scheme:light;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif;color:#253c2d;background:#f7f5f0}
body{max-width:1280px;margin:auto;padding:48px 24px 80px}h1{font-size:clamp(32px,4vw,54px);margin:0 0 8px}h2{margin:52px 0 18px;font-size:25px}p{color:#526a56}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:20px}.card{display:block;overflow:hidden;color:inherit;text-decoration:none;background:white;border:1px solid #c8d9ca;border-radius:16px;box-shadow:0 12px 30px #1b362010}.card:hover,.card:focus-visible{outline:3px solid #397a46;outline-offset:3px}.card iframe{width:100%;height:205px;border:0;pointer-events:none}.card span{display:block;padding:12px 18px;font-weight:700}
</style></head><body><h1>Joyally Design 演示文稿</h1><p>选择视觉方向、内容结构和页面版式。点击预览进入可翻页的示例，按 S 打开演讲者窗口。</p><h2>主题</h2><div class="grid">${cards(themes, 'theme')}</div><h2>演示结构</h2><div class="grid">${cards(scenarios, 'scenario')}</div><h2>页面版式</h2><div class="grid">${layoutCards}</div></body></html>\n`;
await writeFile(join(output, 'index.html'), html);
console.log(JSON.stringify({ output: join(output, 'index.html'), themes: themes.length, scenarios: scenarios.length, layouts: layoutSamples.length }, null, 2));
