# top-architect

**English** | [简体中文](README.zh-CN.md)

An architecture skill for Codex that helps teams discuss and review systems, then turn ambiguous goals into executable, verifiable, and evolvable architecture decisions.

It reorganizes the ideas behind “99 Things a Top Architect Should Know” into a practical loop:

> Value → constraints → boundaries → options → evidence → evolution → ownership

Use it for architecture discussions, decisions, design reviews, system evolution, runtime performance, and architecture communication across software systems, Web frontends, AI applications, Agents, and AI Infra. It supports discussion before decision: facts, assumptions, disagreements, and open questions stay explicit instead of being turned into conclusions too early. Its primary output is not a catalogue of design patterns, but a clear recommendation with tradeoffs, validation evidence, a migration path, operational boundaries, and review triggers.

## Use

Invoke it explicitly:

```text
$top-architect Review this system architecture, focusing on boundaries, data consistency, capacity, and evolution risks.
$top-architect Discuss the execution boundaries of this Agent with me before reaching a conclusion. Surface the key assumptions and alternatives step by step.
```

Install it globally in Codex:

```bash
npx skills add youngjunning/skills --skill top-architect -g
```

For a shared source checkout and local links, see the repository [installation guide](../../../README.md#安装).

## Design

- `SKILL.md`: invocation boundaries, architecture decision workflow, AI/Agent-specific checks, and the response contract.
- `references/decision-template.md`: ADR and decision memo template.
- `references/review-checklist.md`: architecture review checklist.
- `references/discussion-guide.md`: turn-by-turn protocol and convergence signals for sustained architecture discussions.
- `references/web-architecture-patterns.md`: Web architecture decision gates, evidence contracts, and a complete coverage map distilled from the 58 JavaScript, React, and Vue skills in PatternsDev.
- `references/cli-architecture.md`: CLI contract, interaction, automation, and cross-platform architecture guidance.
- `references/javascript-runtime-performance.md`: comparable profiling, memory ownership, lifecycle cleanup, bounded caches, hot-path allocation, and evidence rules for JavaScript runtimes.
- `references/framework-source-benchmarks.md`: framework engineering decisions, including pnpm workspace and Changesets release ownership.

## Source note

This project is an original operational synthesis inspired by [“99 Things a Top Architect Should Know”](https://hangzhouhot.com/arch99/) and informed by the decision signals in the 58 Web skills and the JavaScript Performance Patterns skill from [PatternsDev/skills](https://github.com/PatternsDev/skills). It reorganizes and distills those sources into a decision framework without reproducing their numbered lists, long-form tutorials, or code examples.

## License

MIT
