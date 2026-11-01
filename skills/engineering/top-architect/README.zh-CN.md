# top-architect

[English](README.md) | **简体中文**

一个面向 Codex 的架构师 skill：讨论、评审并把模糊目标变成可执行、可验证、可演进的架构决策。

它把“顶级架构师应该知道的 99 件事”重新组织成一个工作闭环：

> 价值 → 约束 → 边界 → 方案 → 证据 → 演进 → 负责到底

适用于软件系统、Web 前端、AI 应用、Agent、AI Infra 的架构讨论、决策、设计评审、系统演进、运行时性能和架构沟通。它支持先讨论后决策：显式区分事实、假设、分歧和待验证问题，不会过早把探索写成结论。核心输出不是堆砌设计模式，而是明确推荐、权衡、验证证据、迁移路径、运维边界和复盘触发器。

## 使用

显式调用：

```text
$top-architect 帮我评审这个系统架构，重点看边界、数据一致性、容量和演进风险。
$top-architect 先和我讨论 Agent 的执行边界，不急着下结论，逐步暴露关键假设和替代方案。
```

全局安装到 Codex：

```bash
npx skills add youngjunning/skills --skill top-architect -g
```

需要共享源目录与本地软链接时，使用[仓库安装说明](../../../README.md#安装)。安装副本的更新方式以安装工具为准。

## 设计

- `SKILL.md`：触发边界、架构决策工作流、AI/Agent 专项检查和响应契约。
- `references/decision-template.md`：ADR / decision memo 模板。
- `references/review-checklist.md`：架构评审清单。
- `references/discussion-guide.md`：持续架构讨论的回合协议和收敛信号。
- `references/web-architecture-patterns.md`：从 PatternsDev 的 58 个 JavaScript、React、Vue Skills 蒸馏出的 Web 架构决策门、证据契约和完整覆盖映射。
- `references/cli-architecture.md`：CLI 契约、交互、自动化和跨平台架构指南。
- `references/javascript-runtime-performance.md`：JavaScript runtime 的同口径 profiling、内存所有权、生命周期清理、有界缓存、热路径分配和证据规则。
- `references/framework-source-benchmarks.md`：框架工程决策参考，包含 pnpm workspace 与 Changesets 的发布职责边界。

## 来源说明

本项目是原创的操作化总结，灵感来源于[《顶级架构师应该知道的 99 件事》](https://hangzhouhot.com/arch99/)，并融合了 [PatternsDev/skills](https://github.com/PatternsDev/skills) 中 58 个 Web Skills 与 JavaScript Performance Patterns Skill 的决策信号。内容采用重新组织和蒸馏后的决策框架，不复制原文编号、长篇教程或代码示例。

## License

MIT
