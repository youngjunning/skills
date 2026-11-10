# Joyally Design

统一的跨平台设计 Skill：从产品与品牌建立视觉语言，覆盖原生平台适配、React 组件契约、可移植 HTML 报告、演示与交互图表。保留湖色命名、湖景层次与季节光影要求，预设不使用具体景区名称。

```bash
npx skills add youngjunning/skills --skill joyally-design -g
```

使用 `$joyally-design`，说明产品、目标平台和要完成的任务。入口与按需参考见 [SKILL.md](SKILL.md)。Joyally Design 以[完整设计流程](DESIGN_PROCESS.md)与[融合方法](references/fused-method.md)把方向探索、各类页面方法、存量改造、素材、动效、对比页、截图、评审和规范工具落到同一套[江南山水视觉语言](references/visual-language.md)、语义变量、组件状态与验收契约。全部方法、工具和素材位于本目录，按[能力路由](references/capability-routing.md)读取。更新源包时运行 `python3 scripts/sync-upstream.py <压缩包> --check`，确认后用 `--apply` 导入；已有本地修改会报告冲突，不会被覆盖。

## 配色与使用

报告、原生示例与图表遵循 [token 契约](references/token-contract.md)。交互图表的四种样式 共用语义颜色，保留构图、线条与动效特点。旧项目已复制的源码不自动重写；原生 CSS 统一使用 `joyally-` 前缀。

默认本地交付，托管使用调用项目已授权的服务。公开包不依赖内部上传工具。Joyally Design 自身源码采用 [PolyForm Noncommercial 1.0.0](LICENSE)，允许非商业使用、修改和分发；商业使用需另行授权。从 `node scripts/design-engine.mjs --help` 查看报告、演示和图表命令。
