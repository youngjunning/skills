#!/usr/bin/env node

import { access, cp, mkdir, readFile, writeFile } from 'node:fs/promises';
import { constants } from 'node:fs';
import { dirname, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const skillRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const themes = ['lake', 'west-lake', 'suzhou', 'maldives', 'alpine', 'xiaoxiang'];
const types = ['cover', 'agenda', 'section', 'statement', 'cards', 'columns', 'metrics', 'comparison', 'timeline', 'chart', 'code', 'image', 'quote', 'closing'];
const fxTypes = ['particle-burst', 'confetti-cannon', 'firework', 'starfield', 'matrix-rain', 'knowledge-graph', 'neural-net', 'constellation', 'orbit-ring', 'galaxy-swirl', 'word-cascade', 'letter-explode', 'chain-react', 'magnetic-field', 'data-stream', 'gradient-blob', 'sparkle-trail', 'shockwave', 'typewriter-multi', 'counter-explosion'];
const animations = ['fade-up', 'fade-down', 'fade-left', 'fade-right', 'rise-in', 'drop-in', 'zoom-pop', 'blur-in', 'glitch-in', 'typewriter', 'neon-glow', 'shimmer-sweep', 'gradient-flow', 'stagger-list', 'counter-up', 'path-draw', 'parallax-tilt', 'card-flip-3d', 'cube-rotate-3d', 'page-turn-3d', 'perspective-zoom', 'marquee-scroll', 'kenburns', 'confetti-burst', 'spotlight', 'morph-shape', 'ripple-reveal'];
const scenarios = ['tech-sharing', 'project-report', 'product-launch', 'pitch-deck'];
const args = process.argv.slice(2);
const outputArg = args[0];
const option = (name) => {
  const index = args.indexOf(name);
  return index < 0 ? undefined : args[index + 1];
};

if (!outputArg || outputArg === '--help' || !['--source', '--scenario'].some((name) => args.includes(name))) {
  process.stdout.write(`Joyally Design deck builder\nUsage: deck <output-dir> --source <deck.json> [--theme <${themes.join('|')}>]\n       deck <output-dir> --scenario <${scenarios.join('|')}> [--theme <name>]\n       deck <output-dir>\nLayouts: ${types.join(', ')}\n`);
  process.exit(outputArg === '--help' ? 0 : 2);
}

const sourcePath = option('--source');
const scenario = option('--scenario');
if (Boolean(sourcePath) === Boolean(scenario)) {
  console.error('Choose exactly one of --source or --scenario.');
  process.exit(2);
}
if (scenario && !scenarios.includes(scenario)) {
  console.error(`Unknown scenario: ${scenario}`);
  process.exit(2);
}

const samples = {
  'tech-sharing': {
    title: '技术分享', subtitle: '问题、判断、实现与验证',
    slides: [
      { type: 'cover', title: '技术分享', subtitle: '讲清问题与关键判断' },
      { type: 'agenda', title: '今天讲什么', items: ['问题与约束', '方案与取舍', '实现与验证', '结论与下一步'] },
      { type: 'section', title: '问题与约束', number: '01', subtitle: '先说明为什么需要改变' },
      { type: 'columns', title: '现状与目标', left: { title: '现状', body: '填入可验证的现状与影响。' }, right: { title: '目标', body: '填入目标与验收口径。' } },
      { type: 'comparison', title: '方案取舍', headers: ['维度', '方案 A', '方案 B'], rows: [['收益', '填入依据', '填入依据'], ['代价', '填入依据', '填入依据']] },
      { type: 'code', title: '关键实现', code: '// 放入最能说明机制的代码\nconst result = await run();', caption: '只展示观众需要理解的部分。' },
      { type: 'metrics', title: '验证结果', items: [{ value: '待填', label: '核心指标', detail: '注明样本和时间范围' }, { value: '待填', label: '稳定性', detail: '注明验证方法' }] },
      { type: 'closing', title: '我的判断', subtitle: '结论、适用边界、下一步' },
    ],
  },
  'project-report': {
    title: '项目汇报', subtitle: '进度、证据与决策',
    slides: [
      { type: 'cover', title: '项目汇报', subtitle: '截至目前的真实状态' },
      { type: 'statement', title: '一句话结论', body: '写出本次汇报最重要的判断。' },
      { type: 'metrics', title: '关键进展', items: [{ value: '待填', label: '已完成', detail: '附证据' }, { value: '待填', label: '待处理', detail: '附负责人' }] },
      { type: 'timeline', title: '里程碑', items: [{ label: '已完成', title: '阶段一', body: '填写验收结果' }, { label: '进行中', title: '阶段二', body: '填写当前进展' }, { label: '下一步', title: '阶段三', body: '填写可执行动作' }] },
      { type: 'cards', title: '需要关注', items: [{ title: '风险', body: '说明实际风险与影响。' }, { title: '依赖', body: '说明尚需的输入。' }, { title: '决策', body: '说明需要确定的事项。' }] },
      { type: 'closing', title: '下一步', subtitle: '责任、时间与验收口径' },
    ],
  },
  'product-launch': {
    title: '产品发布', subtitle: '价值、体验与行动',
    slides: [
      { type: 'cover', title: '产品发布', subtitle: '用一句话说清用户价值' },
      { type: 'statement', title: '用户遇到的问题', body: '填写真实场景与原有成本。' },
      { type: 'section', title: '新的体验', number: '01', subtitle: '聚焦一条主路径' },
      { type: 'cards', title: '核心能力', items: [{ title: '能力一', body: '对应用户收益。' }, { title: '能力二', body: '对应用户收益。' }, { title: '能力三', body: '对应用户收益。' }] },
      { type: 'image', title: '产品画面', image: '', alt: '待加入产品截图', caption: '用真实截图替换占位画面。' },
      { type: 'comparison', title: '体验变化', headers: ['场景', '过去', '现在'], rows: [['任务一', '原有步骤', '新路径'], ['任务二', '原有步骤', '新路径']] },
      { type: 'closing', title: '开始使用', subtitle: '填写真实入口与下一步' },
    ],
  },
  'pitch-deck': {
    title: '提案演示', subtitle: '机会、方案与可验证计划',
    slides: [
      { type: 'cover', title: '提案演示', subtitle: '写出清楚的价值主张' },
      { type: 'statement', title: '问题', body: '谁在什么场景下付出什么成本？' },
      { type: 'chart', title: '机会规模', items: [{ label: '当前', value: 35 }, { label: '目标', value: 70 }], caption: '示例数据，交付前替换并注明来源。' },
      { type: 'cards', title: '解决方案', items: [{ title: '价值一', body: '说明机制和收益。' }, { title: '价值二', body: '说明机制和收益。' }, { title: '价值三', body: '说明机制和收益。' }] },
      { type: 'timeline', title: '推进计划', items: [{ label: '第一步', title: '验证', body: '写明验证方法' }, { label: '第二步', title: '交付', body: '写明交付范围' }, { label: '第三步', title: '扩展', body: '写明前置条件' }] },
      { type: 'closing', title: '需要的决定', subtitle: '把具体请求和验收条件写清楚' },
    ],
  },
};

const escape = (value) => String(value ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
const paragraph = (value) => escape(value).replaceAll('\n', '<br>');
const text = (value, tag = 'p', className = '') => value ? `<${tag}${className ? ` class="${className}"` : ''}>${paragraph(value)}</${tag}>` : '';
const items = (value) => Array.isArray(value) ? value : [];
const source = (slide) => {
  if (!slide.source) return '';
  const label = escape(typeof slide.source === 'string' ? slide.source : slide.source.label);
  const url = typeof slide.source === 'object' ? slide.source.url : undefined;
  return `<p class="deck-source">来源：${url && /^https?:\/\//.test(url) ? `<a href="${escape(url)}">${label}</a>` : label}</p>`;
};
const heading = (slide) => `<p class="deck-eyebrow">${escape(slide.eyebrow || slide.section || 'Joyally Design')}</p><h2 class="h2">${escape(slide.title)}</h2>${text(slide.subtitle, 'p', 'deck-lead')}`;
const chartMarkup = (slide) => {
  const data = items(slide.items).map((item) => ({ label: String(item.label ?? ''), value: Math.max(0, Math.min(100, Number(item.value) || 0)) }));
  if (slide.chartType === 'line') {
    const points = data.map((item, index) => [40 + index * 920 / Math.max(1, data.length - 1), 320 - item.value * 2.8]);
    return `<svg class="deck-chart-svg" viewBox="0 0 1000 360" role="img" aria-label="${escape(data.map((item) => `${item.label} ${item.value}%`).join('、'))}"><path class="axis" d="M40 40 V320 H960"/><polyline class="plot" points="${points.map((point) => point.join(',')).join(' ')}"/>${points.map(([x, y]) => `<circle class="dot" cx="${x}" cy="${y}" r="7"/>`).join('')}</svg><div class="deck-chart-labels">${data.map((item) => `<span>${escape(item.label)}<br>${item.value}%</span>`).join('')}</div>`;
  }
  if (slide.chartType === 'donut') {
    const colors = ['var(--accent)', 'var(--accent-2)', 'var(--accent-3)', 'var(--good)', 'var(--warn)', 'var(--bad)'];
    const total = data.reduce((sum, item) => sum + item.value, 0) || 1;
    let cursor = 0;
    const segments = data.map((item, index) => { const start = cursor; cursor += item.value / total * 100; return `${colors[index % colors.length]} ${start}% ${cursor}%`; });
    return `<div class="deck-donut-row"><div class="deck-donut" role="img" aria-label="${escape(data.map((item) => `${item.label} ${item.value}`).join('、'))}" style="background:conic-gradient(${segments.join(',')})"></div><div class="deck-legend">${data.map((item, index) => `<span><i style="--legend-color:${colors[index % colors.length]}"></i>${escape(item.label)}：${item.value}</span>`).join('')}</div></div>`;
  }
  if (slide.chartType === 'radar') {
    const point = (radius, index) => { const angle = -Math.PI / 2 + index * 2 * Math.PI / data.length; return [500 + Math.cos(angle) * radius, 180 + Math.sin(angle) * radius]; };
    const area = data.map((item, index) => point(item.value * 1.4, index).join(',')).join(' ');
    return `<svg class="deck-chart-svg" viewBox="0 0 1000 360" role="img" aria-label="${escape(data.map((item) => `${item.label} ${item.value}%`).join('、'))}">${data.map((_, index) => { const [x, y] = point(150, index); return `<line class="axis" x1="500" y1="180" x2="${x}" y2="${y}"/>`; }).join('')}<polygon class="plot-area" points="${area}"/><polygon class="plot" points="${area}"/>${data.map((item, index) => { const [x, y] = point(170, index); return `<text x="${x}" y="${y}" text-anchor="middle" fill="var(--text-2)" font-size="17">${escape(item.label)}</text>`; }).join('')}</svg>`;
  }
  return `<div class="deck-bars">${data.map((item) => `<div class="deck-bar"><span>${escape(item.label)}</span><div class="deck-bar-track"><div class="deck-bar-fill" style="--value:${item.value}%"></div></div><strong>${item.value}%</strong></div>`).join('')}</div>`;
};

const layouts = {
  cover: (s) => `<p class="deck-eyebrow">${escape(s.eyebrow || 'Joyally Design')}</p><h1 class="deck-hero">${escape(s.title)}</h1>${text(s.subtitle, 'p', 'deck-lead')}`,
  agenda: (s) => `${heading(s)}<ol class="deck-list">${items(s.items).map((item) => `<li>${escape(item)}</li>`).join('')}</ol>`,
  section: (s) => `<span class="deck-section-number">${escape(s.number || '01')}</span>${heading(s)}`,
  statement: (s) => `${heading(s)}<p class="deck-quote">${paragraph(s.body)}</p>`,
  cards: (s) => `${heading(s)}<div class="deck-cards mt-l" style="--deck-columns:${Math.min(4, Math.max(1, items(s.items).length))}">${items(s.items).map((item) => `<div class="deck-card"><h3>${escape(item.title)}</h3>${text(item.body)}</div>`).join('')}</div>`,
  columns: (s) => `${heading(s)}<div class="deck-columns mt-l">${[s.left, s.right].map((item) => `<div class="deck-card"><h3>${escape(item?.title)}</h3>${text(item?.body)}</div>`).join('')}</div>`,
  metrics: (s) => `${heading(s)}<div class="deck-cards mt-l" style="--deck-columns:${Math.min(4, Math.max(1, items(s.items).length))}">${items(s.items).map((item) => `<div class="deck-card"><div class="deck-metric">${escape(item.value)}</div><h3>${escape(item.label)}</h3>${text(item.detail)}</div>`).join('')}</div>`,
  comparison: (s) => `${heading(s)}<table class="deck-table mt-l"><thead><tr>${items(s.headers).map((cell) => `<th scope="col">${escape(cell)}</th>`).join('')}</tr></thead><tbody>${items(s.rows).map((row) => `<tr>${items(row).map((cell) => `<td>${escape(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table>`,
  timeline: (s) => `${heading(s)}<div class="deck-timeline mt-l" style="--deck-columns:${Math.min(4, Math.max(1, items(s.items).length))}">${items(s.items).map((item) => `<div><strong>${escape(item.label)}</strong><h3>${escape(item.title)}</h3>${text(item.body)}</div>`).join('')}</div>`,
  chart: (s) => `${heading(s)}<div class="mt-l">${chartMarkup(s)}</div>${text(s.caption, 'p', 'deck-image-caption')}`,
  code: (s) => `${heading(s)}<pre class="deck-code"><code>${escape(s.code)}</code></pre>${text(s.caption, 'p', 'deck-image-caption')}`,
  image: (s) => `${heading(s)}${s.image ? `<img class="deck-image mt-l" src="${escape(s.image)}" alt="${escape(s.alt || '')}">` : `<div class="deck-card mt-l" role="img" aria-label="${escape(s.alt || '待添加图片')}">${escape(s.alt || '待添加图片')}</div>`}${text(s.caption, 'p', 'deck-image-caption')}`,
  quote: (s) => `${heading(s)}<blockquote class="deck-quote">“${paragraph(s.quote)}”</blockquote>${text(s.attribution, 'p', 'deck-lead')}`,
  closing: (s) => `<p class="deck-eyebrow">${escape(s.eyebrow || '结语')}</p><h2 class="deck-hero">${escape(s.title)}</h2>${text(s.subtitle, 'p', 'deck-lead')}`,
};

const outputDir = resolve(process.cwd(), outputArg);
try { await access(outputDir, constants.F_OK); console.error(`Refusing to overwrite existing directory: ${outputDir}`); process.exit(3); } catch (error) { if (error.code !== 'ENOENT') throw error; }
const spec = sourcePath ? JSON.parse(await readFile(resolve(sourcePath), 'utf8')) : structuredClone(samples[scenario]);
const theme = option('--theme') || spec.theme || 'lake';
if (!themes.includes(theme)) throw new Error(`Unknown Joyally Design deck theme: ${theme}`);
if (!Array.isArray(spec.slides) || !spec.slides.length) throw new Error('A deck needs at least one slide.');
if (spec.slides.some((slide) => !types.includes(slide.type) || !slide.title)) throw new Error(`Every slide needs a title and one of: ${types.join(', ')}`);
if (spec.slides.some((slide) => slide.fx && !fxTypes.includes(slide.fx))) throw new Error(`Unknown canvas effect. Choose one of: ${fxTypes.join(', ')}`);
if (spec.slides.some((slide) => slide.animation && !animations.includes(slide.animation))) throw new Error(`Unknown CSS animation. Choose one of: ${animations.join(', ')}`);
for (const slide of spec.slides) {
  if (['agenda', 'cards', 'metrics', 'timeline', 'chart'].includes(slide.type) && !items(slide.items).length) throw new Error(`${slide.type} slide needs items.`);
  if (slide.type === 'comparison' && (!items(slide.headers).length || !items(slide.rows).length)) throw new Error('comparison slide needs headers and rows.');
  if (slide.type === 'columns' && (!slide.left || !slide.right)) throw new Error('columns slide needs left and right.');
  if (slide.type === 'code' && !slide.code) throw new Error('code slide needs code.');
  if (slide.type === 'quote' && !slide.quote) throw new Error('quote slide needs quote.');
  if (slide.type === 'statement' && !slide.body) throw new Error('statement slide needs body.');
  if (slide.type === 'chart' && slide.chartType && !['bar', 'line', 'donut', 'radar'].includes(slide.chartType)) throw new Error('chartType must be bar, line, donut or radar.');
  if (slide.type === 'image' && slide.image && /^[a-z][a-z0-9+.-]*:/i.test(slide.image)) throw new Error('Use a local image path so the deck remains portable.');
}
const mediaCopies = [];
if (sourcePath) {
  for (const [index, slide] of spec.slides.entries()) {
    if (slide.type !== 'image' || !slide.image) continue;
    const imagePath = resolve(dirname(resolve(sourcePath)), slide.image);
    await access(imagePath, constants.R_OK);
    const name = `${index + 1}${extname(imagePath).toLowerCase()}`;
    mediaCopies.push([imagePath, name]);
    slide.image = `./media/${name}`;
  }
}

const assetDir = join(outputDir, 'joyally-design');
await mkdir(join(assetDir, 'themes'), { recursive: true });
await Promise.all([
  cp(join(skillRoot, 'runtime/html/assets/base.css'), join(assetDir, 'base.css')),
  cp(join(skillRoot, 'runtime/html/assets/runtime.js'), join(assetDir, 'runtime.js')),
  cp(join(skillRoot, 'runtime/html/assets/animations/animations.css'), join(assetDir, 'animations.css')),
  cp(join(skillRoot, 'runtime/html/assets/animations/fx-runtime.js'), join(assetDir, 'fx-runtime.js')),
  cp(join(skillRoot, 'runtime/html/assets/animations/fx'), join(assetDir, 'fx'), { recursive: true }),
  cp(join(skillRoot, 'runtime/html/LICENSE'), join(assetDir, 'LICENSE')),
  cp(join(skillRoot, 'assets/joyally-html-theme.css'), join(assetDir, 'joyally-theme.css')),
  cp(join(skillRoot, 'assets/deck.css'), join(assetDir, 'deck.css')),
  ...themes.map((name) => cp(join(skillRoot, `assets/deck-themes/${name}.css`), join(assetDir, `themes/${name}.css`))),
]);

if (mediaCopies.length) await mkdir(join(outputDir, 'media'), { recursive: true });
await Promise.all(mediaCopies.map(([source, name]) => cp(source, join(outputDir, 'media', name))));

const slideHtml = spec.slides.map((slide, index) => `<section class="slide" data-title="${escape(slide.title)}">
  ${slide.fx ? `<div class="deck-fx-host" data-fx="${escape(slide.fx)}" aria-hidden="true"></div>` : ''}
  <div class="deck-safe" data-anim="${escape(slide.animation || 'fade-up')}">${layouts[slide.type](slide)}</div>
  ${source(slide)}
  <div class="deck-footer"><span>${escape(spec.footer || 'Joyally Design')}</span><span class="slide-number" data-current="${index + 1}" data-total="${spec.slides.length}"></span></div>
  <aside class="notes">${text(slide.notes || '补充本页讲述要点和过渡句。')}</aside>
</section>`).join('\n');
const html = `<!doctype html>
<html lang="${escape(spec.lang || 'zh-CN')}" data-theme="${theme}" data-themes="${themes.join(',')}" data-theme-base="./joyally-design/themes/">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="generator" content="Joyally Design"><title>${escape(spec.title || spec.slides[0].title)} · Joyally Design</title>
<link rel="stylesheet" href="./joyally-design/base.css"><link rel="stylesheet" href="./joyally-design/animations.css"><link rel="stylesheet" href="./joyally-design/joyally-theme.css"><link rel="stylesheet" href="./joyally-design/deck.css"><link id="theme-link" rel="stylesheet" href="./joyally-design/themes/${theme}.css"></head>
<body class="joyally-deck"><main class="deck">${slideHtml}</main><script src="./joyally-design/runtime.js"></script><script src="./joyally-design/fx-runtime.js"></script></body></html>\n`;
await writeFile(join(outputDir, 'index.html'), html);
await writeFile(join(outputDir, 'deck.json'), `${JSON.stringify({ ...spec, theme }, null, 2)}\n`);
console.log(JSON.stringify({ mode: 'deck', output: join(outputDir, 'index.html'), theme, slides: spec.slides.length, scenario: scenario || null }, null, 2));
