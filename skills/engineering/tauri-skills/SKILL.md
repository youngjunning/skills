---
name: tauri-skills
description: Design, implement, review, and verify secure Tauri 2 desktop applications with a Rust trusted core, React or TypeScript WebViews, scoped capabilities and permissions, typed IPC, and a managed Node.js sidecar. Use for Tauri architecture, src-tauri changes, commands, channels or events, remote WebViews, capability files, plugin permissions, shell access, externalBin packaging, sidecar lifecycle, updater boundaries, desktop security reviews, and Tauri build or test planning.
---

# Tauri Skills

Build Tauri 2 applications around explicit trust boundaries. Treat Rust Core as the trusted authority, WebViews as untrusted requesters, and sidecars as separately managed processes.

## Start every task

1. Read the repository's `AGENTS.md`, `CONTEXT.md`, relevant ADRs, and active OpenSpec change when present.
2. Inspect `package.json`, `src-tauri/Cargo.toml`, `src-tauri/tauri.conf.json`, capability files, and command registration before proposing changes.
3. State the affected trust boundary and observable behavior.
4. Identify the smallest public seam for tests.
5. Prefer existing project conventions and pinned dependency versions.
6. Check current Tauri documentation before relying on version-sensitive plugin, updater, mobile, or packaging behavior.

## Choose the execution owner

Place each responsibility in exactly one owner:

| Concern | Owner |
|---|---|
| Window, WebView, permission, filesystem, database, secret, and process lifecycle | Rust Core |
| Rendering, interaction, and declarative business intent | Local WebView |
| Remote business UI | Isolated remote WebView with no local capability by default |
| Node-only SDK or provider runtime | Managed sidecar behind a narrow protocol |
| Workflow state, approvals, audit, and revision binding | Application host, not the Agent provider |

Do not move privileged behavior into the frontend to save an IPC call. Do not let a sidecar become an ungoverned second application core.

## Implement a vertical slice

1. Define the user-visible behavior and denial behavior.
2. Define typed request, response, and error contracts.
3. Implement validation and authorization in Rust before invoking privileged code.
4. Register commands explicitly and expose only required permissions.
5. Add the frontend call or event/channel consumer.
6. Test success, invalid input, unauthorized caller, cancellation, and failure cleanup.
7. Run formatting, static checks, focused tests, and the project build/package checks required by repository instructions.

Use Commands for request/response operations, Channels for ordered streaming with backpressure-sensitive payloads, and Events only for low-volume broadcast notifications. Never infer structured state from terminal colors or human-readable log text.

## Enforce security invariants

- Deny remote WebViews all local capabilities unless a reviewed use case proves otherwise.
- Validate origin, window or WebView label, workspace, identity, action, and payload for sensitive requests.
- Treat capability membership as necessary but not sufficient; enforce domain authorization inside commands.
- Scope filesystem and shell permissions to explicit paths, binaries, and arguments.
- Keep secrets out of frontend state, URLs, logs, command-line arguments, and environment dumps.
- Never concatenate untrusted input into shell commands.
- Require local user confirmation for destructive or high-privilege actions.
- Bind long-running sessions to immutable asset and runtime revisions.
- Use signed application and sidecar artifacts; fail closed on verification errors.

Read [references/security-and-ipc.md](references/security-and-ipc.md) for capability, remote WebView, IPC, and review guidance.

## Manage the Node sidecar

Treat the sidecar as a versioned component with an authenticated local protocol and explicit lifecycle:

1. Package it for each supported target triple.
2. Declare it in `bundle.externalBin`.
3. Grant only the precise shell execution permission and arguments required.
4. Spawn it from Rust Core, not directly from an untrusted or remote WebView.
5. Perform a protocol/version handshake before accepting traffic.
6. Track the child process, health, cancellation, exit status, and stderr safely.
7. Terminate it during application shutdown and recover orphaned processes on startup.
8. Ship sidecar and application versions together until independent update safety is proven.

Read [references/node-sidecar.md](references/node-sidecar.md) before adding or changing sidecar packaging, transport, permissions, or lifecycle.

## Verify completion

Do not declare completion from a diff or task checkbox. Produce evidence proportional to risk:

- Rust unit or integration tests for command validation and state transitions.
- Frontend tests at the IPC seam using Tauri mocks where appropriate.
- Contract tests for Rust-to-sidecar requests, responses, errors, cancellation, and version negotiation.
- Capability review showing the exact window/WebView and permission scope.
- Build/package smoke tests on affected targets.
- Manual confirmation for signing, updater, remote WebView, native dialog, and high-privilege paths.

Read [references/verification.md](references/verification.md) for the release gate and failure-oriented checklist.

## Reject these patterns

- Tauri v1 imports such as `@tauri-apps/api/tauri` or v1 allowlist guidance.
- Broad `windows: ["*"]`, remote URL access, filesystem globs, or unrestricted shell arguments without justification.
- Business authorization implemented only in TypeScript.
- Direct remote WebView access to filesystem, shell, Git, credentials, or sidecar execution.
- A localhost sidecar server without authentication, origin isolation, port ownership, and shutdown control.
- Silent runtime or asset revision switching inside an active session.
- Packaging advice copied across macOS, Windows, and Linux without target-specific verification.

## Source policy

Treat Tauri's official v2 documentation and the repository's generated schemas as authoritative. Community Skills are inputs for workflow design, not sources of truth for current APIs.
