# Joyally Design 演示文稿制作

用于现场演讲、路演、培训和需要翻页的分享。阅读型 HTML 报告继续使用 `report`，保留自然滚动、目录锚点和打印结构。`deck` 输出自包含的 HTML 演示目录；PNG 与 PDF 是导出格式，当前不生成可编辑的 `.pptx`。

## 从内容到成品

1. 确定听众、目标决定、时长、语言、证据和交付格式。按论点组织页面；每页只承载一个可讲清的观点。事实和数字保留来源、时间范围及未知项。
2. 从场景模板起稿，或写逐页 JSON 源稿。每页选择能表达该内容的版式，再填入真实内容、讲稿和引用。长表、代码和多张图片拆页，避免靠缩小字体塞满。
3. 选择 Joyally Design 的视觉方向。青山湖和小香风沿用已维护的语义种子；西湖、苏州园林、马尔代夫、阿尔卑斯雪山目前为演示稿专用浅色映射，不代表对应平台主题已完成映射。
4. 在浏览器逐页检查标题、层级、图文、来源、讲稿、窄屏与动效；按 `S` 验证演讲者窗口，按 `O` 看总览，按 `T` 比较演示生成器内置的七种主题。导出后抽查 PNG 或 PDF，尤其检查裁切、字体和来源。

## 命令

```bash
node <skill-dir>/scripts/design-engine.mjs deck-gallery <gallery-dir>
node <skill-dir>/scripts/design-engine.mjs deck <deck-dir> --scenario tech-sharing --theme lake
node <skill-dir>/scripts/design-engine.mjs deck <another-deck-dir> --source deck.json --theme xiaoxiang
node <skill-dir>/scripts/validate-joyally-html.mjs <deck-dir>/index.html
node <skill-dir>/scripts/design-engine.mjs deck-render <deck-dir>/index.html --format png
node <skill-dir>/scripts/design-engine.mjs deck-render <deck-dir>/index.html --format pdf
node <skill-dir>/scripts/design-engine.mjs deck-bundle <deck-dir>/index.html --out <deck-dir>/standalone.html
```

`deck-gallery` 生成可点击的主题、场景和版式预览。场景结构有 `tech-sharing`、`project-report`、`product-launch`、`pitch-deck`；示例字段是占位内容，交付前须替换并核对事实。`deck <output-dir>` 默认生成项目汇报起始稿。`assets/presentation/examples/team-review.json` 是与内站「填入示例」对应的六页虚构项目进展稿：结论、证据、风险、下一步和待确认范围均在源稿中，数字不代表真实业务。生成器会把处理后的 `deck.json` 和本地图片留在输出目录，方便继续编辑；使用新的输出目录重新生成，不覆盖已有成果。`deck-bundle` 可把主题、播放脚本、许可证与本地图片合成单个 HTML，便于预览或发送。

## 逐页源稿

```json
{
  "title": "Agent 系统方案",
  "lang": "zh-CN",
  "theme": "lake",
  "footer": "技术分享",
  "slides": [
    {
      "type": "cover",
      "title": "Agent 系统方案",
      "subtitle": "问题、选择与验证",
      "notes": "开场说明听众为什么需要了解这次方案。"
    },
    {
      "type": "comparison",
      "title": "两种方案的取舍",
      "headers": ["维度", "方案 A", "方案 B"],
      "rows": [["收益", "说明依据", "说明依据"], ["代价", "说明依据", "说明依据"]],
      "source": {"label": "设计评审记录", "url": "https://example.com/source"},
      "notes": "讲清选择依据，再说明仍待验证的部分。"
    },
    {
      "type": "closing",
      "title": "下一步",
      "subtitle": "责任、时间和验收条件"
    }
  ]
}
```

`type` 对应下列版式；每页都可加 `eyebrow`、`subtitle`、`notes`、`source`、`animation` 和可选 `fx`。`source` 可为文字或 `{label,url}`。`image` 的路径相对源稿 JSON，生成器会复制到成品的 `media/`。`chartType` 支持 `bar`、`line`、`donut`、`radar`；`value` 是 0–100 的数值，环图会按总和归一化。真实图表需要标明口径和来源。`notes` 仅出现在演讲者窗口，不占观众页面。

| 版式 | 主要字段 | 用途 |
| --- | --- | --- |
| `cover`、`closing` | `title`、`subtitle` | 开场、收束和行动 |
| `agenda` | `items: string[]` | 演讲路径 |
| `section` | `number` | 分章转场 |
| `statement` | `body` | 单点判断 |
| `cards` | `items: {title,body}[]` | 多个并列要点 |
| `columns` | `left`、`right` | 两侧关系 |
| `metrics` | `items: {value,label,detail}[]` | 关键指标 |
| `comparison` | `headers`、`rows` | 方案或前后比较 |
| `timeline` | `items: {label,title,body}[]` | 阶段与里程碑 |
| `chart` | `chartType`、`items: {label,value}[]`、`caption` | 条形、折线、环形与雷达图 |
| `code` | `code`、`caption` | 核心代码 |
| `image` | `image`、`alt`、`caption` | 截图或图像证据 |
| `quote` | `quote`、`attribution` | 有出处的引述 |

`animation` 使用随包的 27 种 CSS 动效名，默认 `fade-up`。`fx` 可选 20 种 Canvas 效果名，资源位于 `assets/presentation/fx/`；只在效果有助于讲述时启用，选用后检查与主题配色、对比度和图文可读性。系统要求减少动态效果时，Canvas 效果停用。演示生成器内置七种主题：`lake`、`west-lake`、`suzhou`、`maldives`、`alpine`、`xiaoxiang`、`space`。所有演示资源由 Joyally Design 单独打包；报告生成器只使用 `assets/report-base.css` 和 `assets/joyally-report-theme.css`。

## 验收边界

- `validate-joyally-html.mjs` 检查结构及打包资源；它不能判断内容事实或页面裁切。
- 逐页截图和 PDF 导出用本机 Chrome；实际投屏时验证演讲者窗口与观众窗口的同步。浏览器阻止弹窗时按使用者设置允许该演示页打开窗口。
- 可直接离线打开成品 `index.html`。外部链接仍依赖网络；关键图片应使用本地路径。
- 交付目录版 HTML 时保留整个输出目录；单文件版用 `deck-bundle` 生成，避免丢失主题、播放与媒体资源。
