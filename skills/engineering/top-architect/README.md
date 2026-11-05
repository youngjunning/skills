# top-architect

**English** | [简体中文](README.zh-CN.md)

An engineering decision skill for Codex that connects business judgment, product choices, technical architecture, and reliable delivery.

Its working loop is:

> Industry reality → valuable problem → product behavior → system boundaries → delivered outcome → feedback

Use it to understand an industry workflow, assess a product bet, prioritize a first useful slice, compare build/buy options, review architecture, evolve systems, or diagnose runtime performance. It covers users versus buyers/sponsors, incentives, economics per accepted outcome, adoption, trustworthy failure behavior, technical contracts, and operating accountability. Discussion keeps facts, estimates, hypotheses, and preferences visible. Narrow technical work stays narrow; a small internal tool does not require a market study.

## Use

Invoke it explicitly:

```text
$top-architect Review this system architecture, focusing on boundaries, data consistency, capacity, and evolution risks.
$top-architect Discuss the execution boundaries of this Agent with me before reaching a conclusion. Surface the key assumptions and alternatives step by step.
$top-architect Assess this AI product opportunity: who benefits and pays, what users will adopt, which first slice is worth building, and how to verify its economics and delivery.
```

Install it globally in Codex:

```bash
npx skills add youngjunning/skills --skill top-architect -g
```

For a shared source checkout and local links, see the repository [installation guide](../../../README.md#安装).

## Design

- `SKILL.md`: invocation, depth selection, and the business → product → system → evidence → delivery workflow.
- `references/business-product.md`: industry workflows, incentives, product promise, prioritization, adoption, economics, and bounded validation.
- `references/systems-delivery.md`: domain invariants, data/distributed systems, AI/Agent control, rollout, and operation.
- `references/decision-template.md`: business/product/architecture decision memo and ADR template.
- `references/review-checklist.md`: evidence-led business, product, technical, and delivery review.
- `references/discussion-guide.md`: provisional judgments, productive disagreement, and convergence.
- `references/web-architecture-patterns.md`: Web architecture decision gates, evidence contracts, and a complete coverage map distilled from the 58 JavaScript, React, and Vue skills in PatternsDev.
- `references/cli-architecture.md`: CLI contract, interaction, automation, and cross-platform architecture guidance.
- `references/javascript-runtime-performance.md`: comparable profiling, memory ownership, lifecycle cleanup, bounded caches, hot-path allocation, and evidence rules for JavaScript runtimes.
- `references/framework-source-benchmarks.md`: framework engineering decisions, including pnpm workspace and Changesets release ownership.
- `references/behavior-checks.md`: independent replay scenarios and the limits of the observed evaluation.

## Source note

This project is an original operational synthesis inspired by [“99 Things a Top Architect Should Know”](https://hangzhouhot.com/arch99/) and informed by the decision signals in the 58 Web skills and the JavaScript Performance Patterns skill from [PatternsDev/skills](https://github.com/PatternsDev/skills). It reorganizes and distills those sources into a decision framework without reproducing their numbered lists, long-form tutorials, or code examples.

## License

MIT
