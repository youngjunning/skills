# CLI Architecture

Use this reference when a CLI is a product interface, automation boundary, or cross-platform delivery tool. The goal is not a fashionable terminal UI. The goal is a small command contract that people can learn, scripts can trust, and maintainers can evolve without duplicating business logic.

When the task explicitly asks to align with named open-source CLIs or frameworks, also use [cli-source-benchmarks.md](cli-source-benchmarks.md). Pin upstream revisions and compare source ownership; matching dependencies or terminal styling does not establish architectural alignment.

## Start from journeys and contracts

Identify the primary journeys before selecting libraries:

- first-time setup and discovery;
- routine success path;
- diagnosis and repair;
- CI or scripted execution;
- long-running child processes;
- cancellation, retry, and recovery;
- supported shells and operating systems.

For each journey, state required input, safe defaults, observable progress, success evidence, failure evidence, exit code, and next action. Command names, aliases, flags, environment variables, stdin, stdout, stderr, exit codes, and machine-readable schemas are public interfaces.

Compare at least two credible structures when the command surface is consequential. Usually compare a flat command set with task-oriented groups, or an imperative parser with a declarative command schema. Choose the smallest structure that makes discovery and compatibility testable.

## Three boundaries

Keep three responsibilities distinct even if they remain in one package:

1. **Command definition** declares commands, arguments, options, aliases, validation, examples, and help. Building or printing help must not install dependencies, inspect a project, access the network, or start a child process.
2. **Execution and orchestration** resolves project context and calls domain operations. It owns sequencing, cancellation propagation, retries, and the mapping from known failures to stable exit codes. Domain operations should also be callable from tests or another interface without constructing a terminal.
3. **Presentation and interaction** owns color, prompts, progress, summaries, terminal-width adaptation, and human-readable errors. It consumes structured events or results rather than parsing prose emitted by the domain layer.

This separation is a testability and compatibility boundary, not an invitation to create a framework. A thin composition root is enough.

## Interactive and non-interactive modes

Interactive prompts are progressive assistance, never the only way to express input.

- Prompt only when stdin and stdout are terminals and CI mode is not active.
- In CI, pipes, redirected output, or an explicit non-interactive mode, fail immediately when required input is missing. Print the exact command shape needed to continue.
- Every prompt must map to a documented argument, option, config field, or environment variable.
- Cancellation should stop child work, restore terminal state, and normally exit with `130` for an interrupt.
- Do not ask twice for authorization. If a user already supplied an explicit destructive flag, another confirmation adds friction without resolving ambiguity.
- If a destructive action can be reached interactively without explicit authorization, summarize the exact target and consequence before confirming. Define a non-interactive policy such as a required flag; do not silently assume yes.

## Command and help design

- Group commands by user task, not by internal module ownership.
- Keep the common path short. Derive conventional root, config, target, phase, and strictness values when the derivation is deterministic.
- Reserve options for real overrides. Avoid examples that repeat defaults and create false cognitive load.
- Prefer verbs that describe outcomes. Use nested groups when they reduce ambiguity, not merely to mirror folders.
- Name the routine orchestration command after the user-visible result. Keep implementation terms such as `pipeline`, `workflow`, or `orchestrate` internal; expose a narrower verb such as `compile`, `stage`, or `package` only when users need to run that phase independently for diagnosis or recovery.
- Generate help from the command schema. Show a concise overview, per-command help, useful defaults, valid choices, and one or two copyable examples.
- Detect likely command typos and point to the nearest command plus the relevant help entry.
- Hide internal maintenance commands from primary help while retaining an explicit, documented debugging path if operators still need them.
- Deprecation needs a warning, replacement command, removal condition, and test. Do not maintain a second implementation behind an old binary.

## Progress, errors, and child processes

Use a spinner only for a quiet phase owned by the parent CLI. When a compiler, package manager, browser, or deployment tool streams meaningful logs, forward them directly and add a concise phase boundary or final summary.

Errors should answer four questions:

1. What operation failed?
2. What is the likely user-actionable cause?
3. What evidence identifies the stage or underlying child failure?
4. What exact command or input should the user try next?

Write normal results to stdout and diagnostics to stderr. Preserve child stderr and exit status, redact credentials and tokens, and avoid converting every failure into the same generic code. Stabilize exit codes for usage error, validation failure, unavailable dependency, operation failure, and cancellation when callers need to distinguish them. Add structured output only for a demonstrated automation consumer; version its schema.

## Runtime and dependency choices

Choose dependencies for the repository runtime and distribution constraints; do not copy another project's stack mechanically.

For a project-scoped CLI, make the dependency declared by the project and resolved by its lockfile the executable authority. The normal bootstrap is package-manager install followed by the local binary (`pnpm exec`, `npm exec`, a package script, or the ecosystem equivalent). A global binary may remain as an optional convenience when it only discovers the project and delegates to the exact local version. Avoid requiring an independently versioned global implementation: it weakens reproducibility, makes fresh clones depend on hidden machine state, and creates ambiguity about which contract actually ran. A machine-global install remains appropriate when the tool's primary responsibility is machine-wide rather than project-owned.

Treat this as a default with an explicit exception test, not a slogan. Record why the ecosystem norm does or does not fit the product, what compatibility or operational cost the choice creates, and which evidence would trigger revisiting it.

For Node.js, credible options include Commander or the built-in argument parser for command schemas, Clack or another prompt library for TTY interaction, picocolors for color, and native `child_process` or `execa` according to process-control needs. For Rust, analogous choices include clap, dialoguer, indicatif, and owo-colors. Evaluate package size, module format, supported runtime versions, Windows behavior, maintenance, and whether the feature is useful in non-interactive mode.

Avoid adding a spinner library when child logs already provide progress. Avoid replacing a working process layer solely for aesthetic API consistency.

## Cross-platform boundary

Verify the actual supported environment matrix:

- PowerShell, CMD, and POSIX shell quoting;
- executable shims, PATH updates, and process re-entry after installation;
- drive letters, separators, spaces, long paths, and case behavior;
- Ctrl+C and signal propagation to process trees;
- TTY detection under terminals, IDEs, CI runners, pipes, and redirection;
- terminal width, Unicode capability, color support, and `NO_COLOR`;
- administrator or sudo transitions and restoration of the original command context.

Give copyable commands for each supported shell where syntax differs. A cross-platform library does not replace native acceptance.

## Verification matrix

Use proportional checks:

| Boundary | Minimum evidence |
| --- | --- |
| Command schema | parser tests for commands, aliases, defaults, choices, and invalid input |
| Help | stable top-level and per-command snapshots with no operational side effects |
| Interaction | pseudo-terminal tests for prompts, defaults, cancellation, and terminal cleanup |
| Automation | non-TTY and CI tests proving no prompt and deterministic errors/output |
| Processes | child stdout/stderr, exit-code, interrupt, and cleanup tests |
| Compatibility | deprecated command/flag warning and forwarding tests until removal |
| Platforms | native smoke or acceptance on every claimed OS and shell |

Record what each check proves. Unit tests prove the command contract; they do not prove package installation, shell shims, privilege changes, native tooling, or the complete target workflow.

## Review checklist

- Can a new user discover the common path from top-level help?
- Can CI express every required input without prompts?
- Are defaults deterministic and omitted from routine examples?
- Are destructive targets explicit, and is authorization asked exactly once?
- Are stdout, stderr, exit codes, cancellation, and structured output intentional contracts?
- Does help run without project, network, install, or build side effects?
- Are child logs preserved where they are the best diagnostic evidence?
- Is the implementation split at command, execution, and presentation boundaries without duplicating domain logic?
- Are deprecated entrypoints facades with a removal path rather than parallel implementations?
- Has each claimed operating system been accepted natively?
