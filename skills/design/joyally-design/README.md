# Joyally Design

统一的跨平台设计 Skill：青山湖视觉语言、原生平台适配、React 组件契约、可移植 HTML 报告与 Archify 图表。

```bash
npx skills add youngjunning/skills --skill joyally-design -g
```

使用 `$joyally-design`，说明产品、目标平台和要完成的任务。入口与按需参考见 [SKILL.md](SKILL.md)。

## 从旧技能迁移

`qingshan-design` 与 `lake-report-design` 合并为 `joyally-design`；更新项目中的调用名并移除旧安装，避免重复发现。旧项目已经复制的样式和源码不自动重写。

报告脚本前缀从 `lake-` 改为 `joyally-`；原生示例采用 `JoyallyPalette`、`JoyallyTheme` 与 `joyallyTheme`。两种预设的语义关系见 [token 契约](references/token-contract.md)。

默认本地交付，托管使用调用项目已授权的服务。公开包不依赖内部上传工具。MIT；第三方运行时的许可证与署名见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
