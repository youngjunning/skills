---
name: joyally-design
description: 使用 Joyally Design 为 macOS、iOS、Android、React Native 和 Web 建立可适配品牌的设计系统，设计或审查界面、HTML 报告与交互图表。静态架构图片默认由 better-imagegen 主导；用户明确指定 Skill 时优先遵从。
---

# Joyally Design

将层级、材质、颜色、间距与证据呈现用于用户的实际主题。保留事实、链接、标题、数据与交互，不植入来源产品的角色、术语或业务流程。

Joyally Design 是跨平台的设计方法与实现契约：从产品目标、读者、品牌和使用情境出发，形成语义 tokens、组件行为、内容层级和可验证的交付。随包保留湖色命名、湖景层次、雾气、水杉、四季与光影的视觉约定；它们是一套可适配品牌的预设，不以具体景区命名。唯一维护源为本目录；产品服务、角色素材和上传配置由使用项目管理。

## 跨平台路径

先盘点产品任务、既有 tokens、共享组件、输入方式和信息密度，保留平台原生导航。所有平台先读 [统一 token 契约](references/token-contract.md) 与 [验收](references/validation.md)，再选择对应参考：

| 目标 | 参考 |
| --- | --- |
| macOS / SwiftUI / AppKit | [macOS](references/macos.md) |
| iPhone / iPad | [iOS](references/ios.md) |
| Android / Compose | [Android](references/android.md) |
| React Native / Expo | [React Native](references/react-native.md) |
| Web 工作台 | [工作台](references/web-dashboard.md) 与 [React](references/react-design-system.md) |
| 营销页 | [Landing page](references/web-landing-page.md) |

移动端保留原生触控热区与字体缩放；桌面根据任务选择信息密度。先布局与层级，再语义颜色、表面、组件状态，最后加入品牌氛围与动效。原生示例和随包湖色预设见 [平台视觉参考](references/native-visual-system.md)。

## 选择路径

先按交付物确定主导 Skill，再选择视觉风格。用户明确指定 Skill 时优先遵从；未指定时按下表路由：

| 交付物 | 主导 Skill |
| --- | --- |
| 文章、PPT 或分享使用的静态架构图、知识图谱、流程图片 | `better-imagegen` |
| 可点击、缩放、聚焦节点或探索路径的交互图表 | `joyally-design` → Archify |
| 网页、工作台、报告整体设计或跨平台设计系统 | `joyally-design`；其中的静态插图交给 `better-imagegen` |

仅说“画架构图”且现有交付上下文未要求交互时，默认按静态图片处理。Joyally Design 可提供配色、字体、层级与材质参考；采用这些视觉规范不改变主导 Skill，也不自动增加交互页面。生成工具、绘制方式与视觉风格分别确定；`better-imagegen` 的结构图仍按其知识图谱流程完成精确文字和箭头排版。

1. 新建报告：明确读者、决策与证据结构，读取 [设计系统](references/design-system.md)、[报告语言](references/report-language.md)、[布局](references/layout.md) 与 [Pakco 集成](references/pakco-html-integration.md)。
2. 改造已有 HTML：先读 [改造约定](references/adapting-existing-html.md)，保留 DOM、锚点、事件与导出功能，优先增加 scoped theme。
3. React 设计系统：读 [React 约定](references/react-design-system.md)，依次核对 tokens、共享 primitives、组件状态和页面组合。
4. 交互图表：读 [Archify 集成](references/archify-integration.md)，使用内置 wrapper 验证 typed JSON IR，再生成自包含 HTML。既有交互图表的静态导出沿用其源文件。
5. 界面评审或精修：读 [设计质量工作流](references/design-quality.md)。区分 critique（视觉与任务判断）、audit（可核验缺陷）、polish（保留方向的精修）；排版、文案、响应式、动效或风格强弱调整按该文的任务表选择范围。

新建界面也先使用该工作流的「确定方向」：区分阅读、操作与展示场景，再落实到上述平台路径。已有品牌和设计系统是依据，默认配色与第三方审美建议均不覆盖它们。

## 设计契约

内容和可读性先于氛围。正文、表格、日志与证据使用足够清晰的表面；品牌色、材质、字体与图像由具体项目确定。湖景预设用于自然、克制的场景；保留湖色种子名称与景观要求，其他项目从自身品牌素材派生视觉语言。图表与报告共用语义配色。避免嵌套玻璃卡片、持续装饰动画与颜色单独表示状态。

语义 tokens 分为 seed、map、alias、component。Ant Design 提供分层与密度参考，Material 3 提供语义状态角色，Radix 提供无障碍行为，shadcn 提供开放组合方式，Tailwind 用于表达已有 tokens，Magic UI 动效只作为可降级增强；不要求安装全部参考库。

页面按任务组织上下文、局部工具、主要内容与支持信息。只保留一个稳定标题层；selected、focus、loading 不推动布局。组件覆盖 default、hover、pressed、selected、focus、disabled、loading、empty、error、success，以及窄屏、reduced motion 和打印状态。

## 生成与校验

以下 `<skill-dir>` 是当前技能目录，输出使用用户指定位置或临时目录：

```bash
node <skill-dir>/scripts/new-joyally-html.mjs report <output-dir> --title "报告标题" --subtitle "证据与下一步"
python3 <skill-dir>/scripts/validate-joyally-tokens.py
python3 <skill-dir>/scripts/validate-native-tokens.py
python3 <skill-dir>/scripts/validate-archify-theme.py
node <skill-dir>/scripts/validate-joyally-html.mjs <output-dir>/index.html
```

用户明确要求演示文稿时将 `report` 换成 `deck`。阅读报告保持自然滚动，不自动改成幻灯片。

静态通过后检查桌面、窄屏、键盘、长文本、空状态、错误与打印输出。动态图表运行 `joyally-archify.mjs validate` 和 `deliver`；正文保留文字摘要或静态 fallback，分别报告确定性校验与视觉证据。

## 交付与来源

默认交付可用的本地产物。用户明确要求托管时，使用其已配置且获授权的上传方式，上传后读回最终 URL 比较 SHA-256；没有托管配置时直接交付本地文件，不推断上传目标或调用私有服务。保留用户要求的源文件。

内置 Pakco HTML 与 Archify 作为第三方运行时依赖；设计质量工作流改编自 Impeccable，直接融入本技能，未安装其 CLI、hooks 或独立技能。署名、改编范围及各自许可见 [第三方声明](THIRD_PARTY_NOTICES.md)。第三方 runtime 不作为本人原创技能单独发现。公开包不包含角色素材、内部上传代码、账号、真实报告或安装证据。
