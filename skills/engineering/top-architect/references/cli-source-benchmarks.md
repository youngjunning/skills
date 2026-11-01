# CLI Source Benchmarks

Use this reference when “align with a leading CLI” needs source-level evidence. Dependency parity and similar screenshots are insufficient. Pin a reviewed revision, identify the ownership boundaries in source, and record what is adopted, adapted, or rejected.

## Benchmark method

For each project, inspect:

1. the executable composition root and command schema;
2. command/action ownership and domain-service boundaries;
3. prompts, progress, errors, debug output, and cancellation;
4. CI/non-interactive equivalents for prompted input;
5. help and integration tests;
6. package, build, release, and compatibility boundaries.

The output is a decision matrix, not a feature checklist. Record the exact revision and source paths so later reviews can distinguish a durable architectural choice from upstream drift.

## Reference matrix

| Project | Source areas to inspect | Strong signal | Common misuse |
| --- | --- | --- | --- |
| React | `packages/*/package.json`, `scripts/rollup/`, `scripts/release/` | Monorepo package ownership, build/release separation, explicit test and artifact boundaries | Calling React a CLI UX reference when the relevant code is build and release infrastructure |
| React Native Community CLI | `packages/cli/src/index.ts`, `packages/cli/src/commands/`, `packages/cli-types/`, `packages/cli-doctor/` | Declarative command descriptors, independently owned actions, plugin/platform loading, verbose diagnostics, doctor boundary | Copying dynamic plugin discovery into a product with a fixed command contract |
| create-vue | `index.ts`, `package.json`, `scripts/test.mjs` | Grouped prompts, flag equivalence, cancellation, compact completion and next steps | Copying project-specific questions or overwrite behavior without matching safety constraints |
| Mastra | `packages/cli/src/index.ts`, `packages/cli/src/commands/`, `packages/cli/src/services/`, command-local `utils.ts` | Commander composition root, command/action/service separation, Clack flows, debug mode, task presentation | Treating dependency parity as architectural parity or hiding child logs behind spinners |
| Vite+ | `packages/cli/src/bin.ts`, `packages/cli/src/utils/{terminal,command,spinner}.ts`, `crates/vp_global_cli/src/{cli,help,main}.rs`, `crates/vp_cli_snapshots/` | Global-to-local toolchain delegation, leading `-C`, help before project discovery, TTY-gated headers and correction prompts, inherited child streams, signal-aware exit codes, and CLI snapshots | Copying its Rust/NAPI topology into a Node CLI, or copying colors and banners without its process and automation contracts |

These projects are lenses, not a combined template. React supplies package and delivery lessons; create-vue supplies a focused generator interaction; Mastra supplies a larger product CLI composition; React Native Community CLI supplies extensible command and diagnostic boundaries.

Vite+ supplies the strongest unified-toolchain CLI comparison when the local product also owns project-version delegation, environment preparation, package-manager execution, build orchestration, and long-running child processes. Review an exact upstream commit: its CLI is evolving quickly, and a screenshot or dependency list cannot establish parity.

## Required comparison output

Document each conclusion in this shape:

| Field | Required evidence |
| --- | --- |
| Baseline | repository, branch or tag, exact commit, review date |
| Upstream boundary | exact source paths and their responsibilities |
| Local boundary | exact source paths that implement the adapted decision |
| Adopted | behavior or ownership rule retained locally |
| Adapted | difference required by local product, runtime, or safety constraints |
| Rejected | tempting upstream pattern not used, with a concrete reason |
| Verification | parser/help/unit/PTY/CI/process/platform evidence and its limits |

## Review gates

- A shared library version is dependency alignment, not interaction alignment.
- A command folder is not an action boundary if orchestration remains in one central conditional.
- Prompts are incomplete until every value has a non-interactive representation.
- Pretty progress is a regression if it hides child stderr or delays failure evidence.
- A macOS pseudo-terminal test does not establish PowerShell, CMD, Windows PATH, process-tree cancellation, privilege handling, or Unicode behavior.
- An upstream pattern should be rejected when it expands the current product boundary without solving a demonstrated problem.
