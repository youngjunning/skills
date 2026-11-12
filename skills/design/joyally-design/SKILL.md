---
name: joyally-design
description: 所有 UI 设计相关任务使用 Joyally Design，包括 Web/React、macOS、iOS、Android 和 React Native 的新界面、现有页面调整、交互与组件设计、视觉精修、响应式、无障碍和截图评审；混合功能修复时参与界面方案与验收。提供完整的设计方法、工具、设计系统、HTML 报告与交互图表能力。静态架构图片由 joyally-imagegen 主导。
---

# Joyally Design

将层级、材质、颜色、间距与证据呈现用于用户的实际主题。保留事实、链接、标题、数据与交互，不植入来源产品的角色、术语或业务流程。

先由用户任务、现有产品和品牌决定界面，再选领域设计方法、组件基础与视觉方向。Oil UI Pro 的任务路径、视觉构思、存量改造和真实画面走查用于形成与检验方案；Joyally Design 的语义 tokens、跨平台组件状态、主题资产、报告与交互图表能力按任务使用。两者都不是所有页面的默认外观或无条件流程：逐项说明采用什么、保留什么，以及依据。

Joyally Design 是跨平台的设计方法与实现契约：从产品目标、读者、品牌和使用情境出发，形成语义 tokens、组件行为、内容层级和可验证的交付。当前六套并列主题为「青山湖」「西湖」「苏州园林」「马尔代夫」「阿尔卑斯雪山」与[小香风](references/fashion-xiaoxiang.md)。青山湖正在按四季各 5 张授权实拍重建参考画册，已核实数量和缺口见[参考目录](assets/references/qingshan-lake/README.md)；其余五套各有 20 张真实参考画面。前五套按[景观视觉规则](references/visual-language.md)观察地点，小香风观察服装造型、滚边、纽扣、织纹与编辑呈现；粗花呢是材质线索，不是主题身份。六套共用操作语义、组件状态与可读性契约。参考画面位于[青山湖](assets/references/qingshan-lake/README.md)、[西湖](assets/references/west-lake/README.md)、[苏州园林](assets/references/suzhou-gardens/README.md)、[马尔代夫](assets/references/maldives/README.md)、[阿尔卑斯雪山](assets/references/alpine-snow-mountains/README.md)与[小香风](assets/references/xiaoxiang/README.md)；苏州园林同时包含[留园画面](assets/references/lingering-garden/README.md)。服务其他品牌时保留设计方法和语义契约，视觉按该品牌派生。唯一维护源为本目录；产品服务、角色素材和上传配置由使用项目管理。

设计任务先按[完整设计流程](DESIGN_PROCESS.md)选择领域与阶段，再按[融合方法](references/fused-method.md)组织事实、结构、组件、状态与验收；按[能力路由](references/capability-routing.md)读取本目录的领域参考并调用工具。领域、方向、存量改造、组件、素材、动效、截图、评审与规范构成主流程；[专项质量检查](references/design-quality.md)仅在文字本地化、健壮性或技术审计等实际问题出现时加入。Joyally 的视觉语言、语义 tokens、跨平台行为与验收把这些方法连成同一套输出。明确改法的小改动直接完成，任务范围和交付物仍由用户决定。

## 现有界面精修

所有涉及界面设计决策的任务都从本 Skill 进入；用户给出截图并要求调整页面、指出操作拥挤或视觉不协调时尤其如此。先读取实际界面、目标任务路径和项目现有组件与 tokens；按[能力路由](references/capability-routing.md)进入精修、回改或存量项目路径。交互缺陷与视觉问题同在一个操作区时，与工程排障一起处理：先确认状态和下一步动作，再调整布局与层级，最后检查颜色与细节。文字、本地化、健壮性或技术审计问题再读[专项质量检查](references/design-quality.md)。不要只改装饰而保留难以发现、无法继续或语义相反的操作。

交付前在目标页面核对主要操作、恢复路径、加载与禁用状态，以及实际支持的窄屏；源码、构建和截图各自只证明对应范围。纯业务逻辑或 API 改动没有界面决策时，不因同属前端仓库而触发本流程。

## 跨平台路径

先盘点产品任务、既有 tokens、共享组件、输入方式和信息密度，保留平台原生导航。交付界面先确定组件来源：已有项目使用现行组件库和样式体系；没有组件基础时按目标平台选定并记录，不把逐页手写原生控件样式当作默认方案。Joyally Design 管理语义 tokens、共享组件变体、交互状态和页面组合，具体控件由所选平台组件基础承载。所有平台先读 [统一 token 契约](references/token-contract.md) 与 [验收](references/validation.md)，再选择对应参考：

| 目标 | 参考 |
| --- | --- |
| macOS / SwiftUI / AppKit | [macOS](references/macos.md) |
| iPhone / iPad | [iOS](references/ios.md) |
| Android 原生 App / Compose | [Android](references/android.md)；使用 Jetpack Compose Material 3 |
| React Native / Expo | [React Native](references/react-native.md) |
| H5 页面 | [H5 界面](references/h5-ui.md)；Joyally 自有新界面使用 daisyUI，其他项目沿用现有组件基础 |
| React Web 页面与工作台 | [React](references/react-design-system.md)；工作台另读[工作台](references/web-dashboard.md)；Joyally 自有中后台以完整 shadcn/ui 为基础，其他项目沿用现有组件，Magic UI 用于适合的展示动效 |
| 营销页 | [Landing page](references/web-landing-page.md) |
| Chrome 扩展界面 | [扩展界面](references/chrome-extension-ui.md)；Joyally 自有新界面使用 daisyUI，其他项目沿用现有组件基础 |
| Chrome 扩展图标 | [扩展图标](references/chrome-extension-icon.md) |

按交付场景选组件基础：React 实现的 H5 页面仍按 H5 路径使用 daisyUI，React 实现的 Chrome 扩展仍按扩展路径使用 daisyUI；React Native 使用原生移动端路径。其他项目已有组件体系先沿用并按获准范围升级。

移动端保留原生触控热区与字体缩放；桌面根据任务选择信息密度。先布局与层级，再语义颜色、表面、组件状态，最后加入品牌氛围与动效。原生示例和随包湖色预设见 [平台视觉参考](references/native-visual-system.md)。

## 选择路径

先按交付物确定主导 Skill，再选择视觉风格。用户明确指定 Skill 时优先遵从；未指定时按下表路由：

| 交付物 | 主导 Skill |
| --- | --- |
| 文章、PPT 或分享使用的静态架构图、知识图谱、流程图片 | `joyally-imagegen` |
| 可点击、缩放、聚焦节点或探索路径的交互图表 | `joyally-design` |
| 网页或工作台的新建与局部精修、报告整体设计、跨平台设计系统 | `joyally-design`；其中的静态插图交给 `joyally-imagegen` |
| Chrome 扩展图标的设计、尺寸适配和真实工具栏验收 | `joyally-design` 主导小尺寸识别与使用情境；需要生成源图时调用 `joyally-imagegen` |

仅说“画架构图”且现有交付上下文未要求交互时，默认按静态图片处理。Joyally Design 可提供配色、字体、层级与材质参考；采用这些视觉规范不改变主导 Skill，也不自动增加交互页面。生成工具、绘制方式与视觉风格分别确定；`joyally-imagegen` 的结构图仍按其知识图谱流程完成精确文字和箭头排版。

1. 新建报告：明确读者、决策与证据结构，读取 [设计系统](references/design-system.md)、[报告语言](references/report-language.md)、[布局](references/layout.md) 与 [HTML 报告与演示](references/html-reports.md)。
2. 改造已有 HTML：先读 [改造约定](references/adapting-existing-html.md)，保留 DOM、锚点、事件与导出功能，优先增加 scoped theme。
3. React 设计系统：读 [React 约定](references/react-design-system.md)，依次核对 tokens、共享 primitives、组件状态和页面组合。
   编码 Agent 需要选用、安装或组合中后台组件时，再读 [React 组件工作流](references/component-workflow.md)，从目标项目或 shadcn/ui 官方 CLI 取得真实源码，并逐项验收预览。
4. 交互图表：读 [交互图表](references/interactive-diagrams.md)，使用统一入口 验证 typed JSON IR，再生成自包含 HTML。既有交互图表的静态导出沿用其源文件。
5. 界面评审或精修：按[能力路由](references/capability-routing.md)读取评审、精修、回改或存量路径。技术审计再读[专项质量检查](references/design-quality.md)，结论需可复现条件与证据。

新建界面先区分阅读、操作与展示场景，再落实到上述平台路径。按[能力路由](references/capability-routing.md)选择任务与领域参考，处理方向比较、代表性页面、多页扩展、回改和项目设计规范。已有品牌和设计系统是依据，默认配色与第三方审美建议均不覆盖它们。

## 设计契约

内容和可读性先于氛围。正文、表格、日志与证据使用足够清晰的表面；品牌色、材质、字体与图像由具体项目确定。Joyally 品牌先按任务和已有品牌环境选择视觉主题；选用前五套景观主题时读[景观视觉规则](references/visual-language.md)，选用小香风时读[小香风主题](references/fashion-xiaoxiang.md)和[参考画面](assets/references/xiaoxiang/README.md)。选用阿尔卑斯雪山时读[雪山主题细则](references/alpine-snow-mountains.md)，[平台视觉参考](references/native-visual-system.md)提供现有青山湖预设的具体映射。青山湖从四季画面提炼一套主题，不按季节切换；随包青瓷釉和玻璃 token 是该主题的材质样本。小香风提供独立的浅色与深色[语义 token 样本](assets/xiaoxiang-theme.tokens.json)。其他主题进入产品时要完整映射相同语义 token 并验证。其他项目从自身品牌素材派生视觉语言。图表与报告共用语义配色。避免嵌套玻璃卡片、持续装饰动画与颜色单独表示状态。

新建或精修界面交付前，按[反模板感检查](references/anti-ai-taste.md)核对任务焦点、内容顺序、容器职责、装饰语义、示例数据与状态反馈。把“AI 味”当作需要定位的可观察问题，不用颜色、圆角或渐变推断界面来源；具体问题和改法对照同一内容与视口验证。

语义 tokens 分为 seed、map、alias、component。Ant Design 提供分层与密度参考，Material 3 提供语义状态角色，Radix 提供无障碍行为，shadcn/ui 提供开放组件基础。Joyally 自有新建 React 中后台以完整 shadcn/ui 基础组件集建立组件库；其他项目先沿用现有组件并按任务补齐。Data Table、Date Picker 等可由基础组件组合，保留升级路径。展示类页面可按需要选用 Magic UI 的动效组件。动效按任务选择并提供可降级状态。H5 与 Chrome 扩展使用 daisyUI 时，可按项目构建条件选择 Tailwind CSS 4 插件或本地打包独立 CSS。

页面按任务组织上下文、局部工具、主要内容与支持信息。只保留一个稳定标题层；selected、focus、loading 不推动布局。组件覆盖 default、hover、pressed、selected、focus、disabled、loading、empty、error、success，以及窄屏、reduced motion 和打印状态。

## 生成与校验

以下 `<skill-dir>` 是当前技能目录，输出使用用户指定位置或临时目录。工具直接位于 `scripts/`，使用方法见[能力路由](references/capability-routing.md)：

```bash
node <skill-dir>/scripts/design-engine.mjs report <output-dir> --title "报告标题" --subtitle "证据与下一步"
node <skill-dir>/scripts/design-engine.mjs --help
python3 <skill-dir>/scripts/validate-joyally-tokens.py
python3 <skill-dir>/scripts/validate-native-tokens.py
python3 <skill-dir>/scripts/validate-diagram-theme.py
node <skill-dir>/scripts/validate-joyally-html.mjs <output-dir>/index.html
```

用户明确要求演示文稿时将 `report` 换成 `deck`。阅读报告保持自然滚动，不自动改成幻灯片。

静态通过后检查桌面、窄屏、键盘、长文本、空状态、错误与打印输出。动态图表运行 `design-engine.mjs diagram validate` 和 `diagram deliver`；正文保留文字摘要或静态 fallback，分别报告确定性校验与视觉证据。

## 交付与来源

默认交付可用的本地产物。用户明确要求托管时，使用其已配置且获授权的上传方式，上传后读回最终 URL 比较 SHA-256；没有托管配置时直接交付本地文件，不推断上传目标或调用私有服务。保留用户要求的源文件。

Joyally Design 自身源码按 [非商业许可](LICENSE)提供。公开包不包含角色素材、内部上传代码、账号、真实报告或安装证据。
