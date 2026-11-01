---
name: polyglot-service-deploy
description: Develop and diagnose a Node.js service that packages or supervises Python, Rust or Bun runtimes, with explicit process ownership, locked dependencies, prebuilt artifact verification and separate liveness/readiness evidence; uses the owning repository's deployment commands.
---

# Polyglot Service Deploy

Read the owning repository's instructions, manifests, lockfiles, build scripts, startup configuration and health probes. Establish the actual topology before proposing changes. This skill contains no platform SDK, private deployment template or production target.

## Establish ownership

Map each process to its runtime, entrypoint, supervisor, working directory, port or IPC transport, environment, readiness condition and shutdown owner. Preserve those boundaries. A child service becoming ready does not prove the main application or reverse proxy is ready.

Use the repository's pinned toolchains and package managers. Keep separate locks for each language; assemble production-only dependencies at build time. Avoid network installation or compilation at container startup unless that is an explicit existing contract.

When decorator-based dependency injection relies on runtime type metadata, retain value imports for provider classes. A type-only import or a test that directly constructs the class may miss container-resolution failures. Verify the actual metadata or exercise a route that resolves the full dependency chain with the installed framework version.

## Build and package

1. Distinguish source compilation from verification of a committed prebuilt binary. Follow the established route rather than adding a compiler to every deployment environment.
2. Bind a prebuilt binary to its target OS/architecture, byte hash and source identity. Reject mismatches; a file existing on disk is insufficient evidence.
3. Stage the declared binaries, child-service source, locked production dependencies and configuration. Inspect the resulting archive rather than inferring it from a successful build command.
4. Verify executable modes, working directories, dynamic libraries and runtime versions on the target host. Preserve platform-specific paths in project configuration, not this skill.

## Startup and diagnosis

Read logs as a timeline: extraction/bootstrap, main service, supervised children, direct application probe, proxy probe, platform probe, termination decision. Keep an early connection refusal separate from a later successful readiness check.

Confirm the real application port and bind address. A public proxy URL is not a substitute for a direct local probe. Liveness checks the main process; readiness may additionally require child services, IPC and dependent resources. Use repository-defined bounded startup deadlines and retries rather than hiding failures behind permanent retries.

Spawn children with an explicit executable, cwd and argument list. Forward termination, reap exits, release ports and temporary files, and record the failed layer. Unexpected child failure must propagate to the owner; do not return a successful health state because another process is still alive.

During remediation, change the smallest owning layer. Do not disable global response middleware to repair one raw protocol endpoint, expose private diagnostics, or merge independently owned runtimes merely to simplify a startup script.

## Delivery evidence

Report source revision, package/archive identity, artifact hashes and target runtime evidence separately from deployment, readiness and application acceptance. Preserve unknown outcomes. Use actual repository commands, and state missing permissions, host evidence or runtime capabilities precisely without inventing platform APIs.
