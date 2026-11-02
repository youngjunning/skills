---
name: joyally-design
description: 使用 Joyally Design（青山湖视觉语言）设计、实现或审查 macOS、iOS、Android、React Native 和 Web 界面，生成或改造 HTML 报告，并通过内置 Archify 绘制可探索图表。
---

# Joyally Design

将层级、材质、颜色、间距与证据呈现用于用户的实际主题。保留事实、链接、标题、数据与交互，不植入来源产品的角色、术语或业务流程。

Joyally Design 是统一的开源设计语言，合并原 Qingshan Design 与 Joyally Design Design。青山湖是自然视觉来源，不是另一套设计系统，也不代表景区官方。唯一维护源为本目录；产品服务、角色素材和上传配置由使用项目管理。

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

移动端保留原生触控热区与字体缩放；桌面保持专业密度。先布局与层级，再语义颜色、表面、组件状态，最后加入氛围与动效。原生示例和默认湖色预设见 [平台视觉参考](references/native-visual-system.md)。

## 选择路径

1. 新建报告：明确读者、决策与证据结构，读取 [设计系统](references/design-system.md)、[报告语言](references/report-language.md)、[布局](references/layout.md) 与 [Pakco 集成](references/pakco-html-integration.md)。
2. 改造已有 HTML：先读 [改造约定](references/adapting-existing-html.md)，保留 DOM、锚点、事件与导出功能，优先增加 scoped theme。
3. React 设计系统：读 [React 约定](references/react-design-system.md)，依次核对 tokens、共享 primitives、组件状态和页面组合。
4. 动态图表：读 [Archify 集成](references/archify-integration.md)，使用内置 wrapper 验证 typed JSON IR，再生成自包含 HTML。

## 设计契约

内容和可读性先于氛围。正文、表格、日志与证据使用不透明表面；湖色、雾白、克制的中国材质线索用于页面外围与必要强调。保持紧凑的专业密度，避免嵌套玻璃卡片、持续装饰动画与颜色单独表示状态。

语义 tokens 分为 seed、map、alias、component。Ant Design 提供分层与密度参考，Material 3 提供语义状态角色，Radix 提供无障碍行为，shadcn 提供开放组合方式，Tailwind 用于表达已有 tokens，Magic UI 动效只作为可降级增强；不要求安装全部参考库。

页面按任务组织上下文、局部工具、主要内容与支持信息。只保留一个稳定标题层；selected、focus、loading 不推动布局。组件覆盖 default、hover、pressed、selected、focus、disabled、loading、empty、error、success，以及窄屏、reduced motion 和打印状态。

## 生成与校验

以下 `<skill-dir>` 是当前技能目录，输出使用用户指定位置或临时目录：

```bash
node <skill-dir>/scripts/new-joyally-html.mjs report <output-dir> --title "报告标题" --subtitle "证据与下一步"
python3 <skill-dir>/scripts/validate-joyally-tokens.py
python3 <skill-dir>/scripts/validate-native-tokens.py
node <skill-dir>/scripts/validate-joyally-html.mjs <output-dir>/index.html
```

用户明确要求演示文稿时将 `report` 换成 `deck`。阅读报告保持自然滚动，不自动改成幻灯片。

静态通过后检查桌面、窄屏、键盘、长文本、空状态、错误与打印输出。动态图表运行 `joyally-archify.mjs validate` 和 `deliver`；正文保留文字摘要或静态 fallback，分别报告确定性校验与视觉证据。

## 交付与来源

默认交付可用的本地产物。用户明确要求托管时，使用其已配置且获授权的上传方式，上传后读回最终 URL 比较 SHA-256；没有托管配置时直接交付本地文件，不推断上传目标或调用私有服务。保留用户要求的源文件。

内置 Pakco HTML 与 Archify 仅作为 MIT 运行时依赖，署名及许可见 [第三方声明](THIRD_PARTY_NOTICES.md)。第三方 runtime 不作为本人原创技能单独发现。公开包不包含角色素材、内部上传代码、账号、真实报告或安装证据。
