---
name: lake-report-design
description: 使用湖色、雾白与专业信息密度生成或改造可移植 HTML 报告，为 React 页面建立语义 tokens 和组件状态，并通过内置 Archify 绘制可探索图表；不包含业务品牌素材或托管服务。
---

# Lake Report Design

将层级、材质、颜色、间距与证据呈现用于用户的实际主题。保留事实、链接、标题、数据与交互，不植入来源产品的角色、术语或业务流程。

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
node <skill-dir>/scripts/new-lake-html.mjs report <output-dir> --title "报告标题" --subtitle "证据与下一步"
python3 <skill-dir>/scripts/validate-lake-tokens.py
node <skill-dir>/scripts/validate-lake-html.mjs <output-dir>/index.html
```

用户明确要求演示文稿时将 `report` 换成 `deck`。阅读报告保持自然滚动，不自动改成幻灯片。

静态通过后检查桌面、窄屏、键盘、长文本、空状态、错误与打印输出。动态图表运行 `lake-archify.mjs validate` 和 `deliver`；正文保留文字摘要或静态 fallback，分别报告确定性校验与视觉证据。

## 交付与来源

默认交付可用的本地产物。用户明确要求托管时，使用其已配置且获授权的上传方式，上传后读回最终 URL 比较 SHA-256；没有托管配置时直接交付本地文件，不推断上传目标或调用私有服务。保留用户要求的源文件。

内置 Pakco HTML 与 Archify 仅作为 MIT 运行时依赖，署名及许可见 [第三方声明](THIRD_PARTY_NOTICES.md)。第三方 runtime 不作为本人原创技能单独发现。公开包不包含角色素材、内部上传代码、账号、真实报告或安装证据。
