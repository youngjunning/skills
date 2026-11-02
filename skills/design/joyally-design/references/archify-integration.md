# Archify 集成

Joyally Design 将官方 [Archify](https://github.com/tt-a1i/archify) 核心作为报告图表层内置。这是技能包的内部能力，不是路由、远程服务或第二套设计系统。

## 使用场景

报告需要可探索的架构图、工作流图、时序图、数据流图、生命周期图、ERD、树图、类图、时间线、瀑布图或解释型图文时使用 Archify。根据要表达的关系选择图表类型，不让预设风格决定内容。图表仍然是可选增强：省略、阻塞、打印或启用 reduced motion 时，报告必须仍然可理解。

## 交付契约

1. 使用匹配的 schema 编写 typed JSON IR，并保持主路径小而清晰。
2. 交付前验证候选图表：

   ```bash
   node .codex/skills/joyally-design/scripts/joyally-archify.mjs validate architecture input.json --quality showcase --json
   ```

3. 只有验证通过后才交付自包含 HTML/SVG 产物：

   ```bash
   node .codex/skills/joyally-design/scripts/joyally-archify.mjs deliver architecture input.json output.html --quality showcase --json
   ```

4. 需要浏览器证据时运行 `visual-check`。确定性产物、浏览器证据和感知层视觉审查必须分别陈述。
5. 默认交付已验证的本地 HTML；用户要求托管时，按 [分享约定](sharing.md) 使用已有授权的上传方式并读回校验。

wrapper 会设置 `ARCHIFY_UPDATE_CHECK_DISABLED=1`，保证报告生成离线且可复现。更新 vendored core 时要明确从上游仓库同步；运行时不要安装全局 Archify 副本。

## 集成边界（vendor + wrapper）

Archify 的唯一运行时来源是 `vendor/archify/`。报告和 React 代码不应直接 import renderer、viewer template 或 Archify 的内部模块；统一通过 `scripts/joyally-archify.mjs` 调用本地 CLI。这个 wrapper 只负责三件事：解析技能包内的 vendored CLI、透传 Archify 命令参数、关闭联网更新检查。它不负责业务数据、页面路由或视觉主题。

图表输入、产物和验证文件放在用户指定位置或系统临时目录，交付前保留最终结果：

```text
<temp-dir>/
  search-flow.workflow.json   # typed Archify IR
  search-flow.html             # deliver 产物，不依赖外部资源
```

独立图表的生成链路为 `typed JSON IR → validate → deliver → optional visual-check → 本地交付或授权托管及读回`。`validate` 失败不得继续生成或嵌入；`deliver` 失败不得拿旧 HTML 冒充当前结果。报告正文必须同时提供一段文字摘要或静态/export fallback，这样禁用脚本、打印、reduced motion 或图表生成失败时，读者仍能理解主路径和结论。

HTML 报告嵌入时使用有边界的 frame，不让图表改变正文布局：

```html
<figure class="joyally-diagram" aria-labelledby="search-flow-title">
  <iframe
    src="https://reports.example/artifacts/{sha256-prefix}.html"
    title="搜索推荐工作流"
    loading="lazy"
    sandbox="allow-scripts"
  ></iframe>
  <figcaption id="search-flow-title">
    搜索请求经过检索、分析与报告生成；正文提供同一流程的文字摘要。
  </figcaption>
</figure>
```

将示例中的 `{sha256-prefix}` 替换为上传脚本返回的已验证对象 key。

在 Markdown 或 HTML 文档中嵌入 Archify 图表时，默认使用不带参数的原始 URL，保留完整查看器、章节导航和节点悬停反馈。用户明确要求纯画布时才加 `embed=1`：它隐藏标题、工具栏、说明卡和导航，也关闭普通 trace 入场动画。明确要求纯画布内自动播放首段引导故事一次时才加 `embed=1&play=1`；如需重播，可由宿主页面重新加载 iframe。已有查询参数时追加参数，保留片段标识且不重复添加。三种方式都保留独立打开链接与正文摘要，无需另生成或裁剪 HTML。

原始 URL 已支持悬停节点时高亮关联路径。只有用户同时要求纯画布和悬停反馈时才使用派生版：对已验证的自包含 HTML 运行 `python3 scripts/enable-embed-hover.py 原图.html hover版.html`，再在浏览器验证 `?embed=1` 中悬停节点后 SVG 出现 `data-intent-trace-active` 和关联路径，需要托管时再上传并替换 iframe URL。该脚本只移除 `intentTrace` 的 embed guard；其他 viewer 控件与 click 行为仍遵守原模式。Archify 模板更新后若脚本报 guard 不匹配，先检查新版逻辑再改脚本，不做盲目字符串替换。

Markdown 文档直接使用原生 HTML 块，前后留空行。独立打开链接放在 HTML 块外，使用普通 Markdown 链接，以便过滤原生 HTML 的预览器仍能显示；正文仍须概述图表主路径。下面是默认嵌入示例；明确要求纯画布时才在 iframe URL 后加 `?embed=1`，要求自动播放时用 `?embed=1&amp;play=1`：

```html
<figure>
  <iframe
    src="https://reports.example/artifacts/{sha256-prefix}.html"
    title="工作流图"
    loading="lazy"
    sandbox="allow-scripts"
    style="display: block; width: 100%; max-width: 100%; height: 70vh; min-height: 560px; max-height: 680px; border: 0;"
  ></iframe>
  <figcaption>工作流图；主要步骤见正文。</figcaption>
</figure>

[单独打开工作流图](https://reports.example/artifacts/{sha256-prefix}.html)
```

将占位对象 key 换成已验证的 CDN URL。交付前核对目标 Markdown 渲染器：Zed 内置 Markdown Preview 不使用浏览器 WebView，不能显示交互式 iframe；GitLab Markdown 的嵌入内容受实例设置和允许的 provider 限制。若目标渲染器过滤 iframe，明确说明该限制，保留独立链接，并在需要页内交互展示时改用可嵌入的 HTML 页面。不要把 `embed=1` 加到独立打开链接。

容器必须设置 `aspect-ratio` 或明确的最小高度、`max-width: 100%` 和窄屏纵向降级；不要用 `overflow: hidden` 掩盖 Archify 自身的溢出诊断。`sandbox`、`title` 和 `figcaption` 是默认可访问性边界，若需要导出或交互桥接，必须在具体报告中说明扩展权限。

升级 vendored core 时只改 `UPSTREAM.json`、vendor 文件和对应校验记录；不要把上游 Archify 的颜色、preset 或主题选择直接写入 Joyally Design tokens。Archify 负责图表语义和自身 viewer，Joyally Design 负责报告外围的层级、材质、间距和降级策略。

## Joyally Design 视觉映射

- 默认使用 Archify light mode 与 `classic` preset，优先保证报告可读性。
- 只有当主题确实受益于对应视觉语法时才使用 `signal-flow` 或 `blueprint`；不要为了让技术图表显得复古而选择 `editorial`。
- Joyally Design 的气质应落在外围报告的 tokens、间距、标题处理和克制的墨色/青瓷釉强调上。不要修改 Archify 核心 renderer，也不要给图表添加仿古装饰。
- 嵌入产物时提供明确的 `title`、`loading="lazy"` 和有边界的响应式 frame；为 print 与 reduced-motion 提供文字摘要或静态/export fallback。

## 范围与来源

bundled directory 是官方 Archify `archify/` core 的运行时子集，包含 CLI、schemas、renderers、viewer template、references 和 doctor 所需的最小示例。来源与 Apache-2.0 license、历史 MIT 声明记录在 `vendor/archify/UPSTREAM.json`、`vendor/archify/LICENSE`、`LICENSE-MIT`、`NOTICE` 和 `THIRD_PARTY_NOTICES.md`。
