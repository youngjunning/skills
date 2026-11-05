# top-architect

[English](README.md) | **简体中文**

一个面向 Codex 的工程决策技能，把业务判断、产品取舍、技术架构与稳定交付连成同一条推理链。

工作闭环：

> 行业真实流程 → 有价值的问题 → 产品行为 → 系统边界 → 交付结果 → 反馈

适用于行业流程分析、产品机会与优先级、首个完整场景、自建或采购、Skill / Agent / 数字员工设计与交付、架构评审、系统演进和运行时性能。覆盖使用者与付费者或内部发起者、各方激励、完整结果成本、采用阻力，以及模型与上下文、数据工具、能力资产生命周期、执行协作、业务职责运营、评测和发布。讨论时保留事实、估计、假设和偏好的区别；窄技术问题直接处理，不强制小型内部工具做市场研究。

## 使用

显式调用：

```text
$top-architect 帮我评审这个系统架构，重点看边界、数据一致性、容量和演进风险。
$top-architect 先和我讨论 Agent 的执行边界，不急着下结论，逐步暴露关键假设和替代方案。
$top-architect 判断这个 AI 产品机会：谁受益和付费、用户为何采用、第一片做什么，以及如何验证经济性与稳定交付。
$top-architect 为这项业务职责设计数字员工：哪些方法沉淀为 Skill，Agent 如何运行，人如何接管，以及用什么证据验收持续服务。
```

全局安装到 Codex：

```bash
npx skills add youngjunning/skills --skill top-architect -g
```

需要共享源目录与本地软链接时，使用[仓库安装说明](../../../README.md#安装)。安装副本的更新方式以安装工具为准。

## 设计

- `SKILL.md`：触发边界、分析深度与业务 → 产品 → 系统 → 证据 → 交付流程。
- `references/business-product.md`：行业流程、激励、产品承诺、优先级、采用、经济性与有界验证。
- `references/systems-delivery.md`：领域约束、数据与分布式系统、AI/Agent 控制、上线和运维。
- `references/ai-engineering.md`：模型、上下文、数据与工具选择，Skill 生命周期，Agent 执行协作，数字员工运营，分层评测与 AI 发布。
- `references/decision-template.md`：业务、产品与技术决策备忘录及 ADR 模板。
- `references/review-checklist.md`：有证据的业务、产品、技术与交付评审。
- `references/discussion-guide.md`：暂定判断、建设性分歧与收敛。
- `references/web-architecture-patterns.md`：从 PatternsDev 的 58 个 JavaScript、React、Vue Skills 蒸馏出的 Web 架构决策门、证据契约和完整覆盖映射。
- `references/cli-architecture.md`：CLI 契约、交互、自动化和跨平台架构指南。
- `references/javascript-runtime-performance.md`：JavaScript runtime 的同口径 profiling、内存所有权、生命周期清理、有界缓存、热路径分配和证据规则。
- `references/framework-source-benchmarks.md`：框架工程决策参考，包含 pnpm workspace 与 Changesets 的发布职责边界。
- `references/behavior-checks.md`：独立行为回放场景与已执行评估的证据边界。

## 来源说明

本项目是原创的操作化总结，灵感来源于[《顶级架构师应该知道的 99 件事》](https://hangzhouhot.com/arch99/)，并融合了 [PatternsDev/skills](https://github.com/PatternsDev/skills) 中 58 个 Web Skills 与 JavaScript Performance Patterns Skill 的决策信号。内容采用重新组织和蒸馏后的决策框架，不复制原文编号、长篇教程或代码示例。

## License

MIT
