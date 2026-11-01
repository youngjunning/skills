# Managed Node.js sidecar reference

## Contents

1. Ownership boundary
2. Packaging
3. Permission model
4. Transport and handshake
5. Lifecycle
6. Security checklist
7. Official references

## Ownership boundary

Use a Node sidecar only for a Node-only SDK, provider runtime, or workload whose process isolation is valuable. Keep window management, permissions, secrets, local database authority, update control, and child-process ownership in Rust Core.

Expose a narrow domain protocol instead of mirroring arbitrary Node APIs. The sidecar must not write Provider projections, project files, or credentials outside paths and operations authorized by Rust Core.

## Packaging

Choose one explicit distribution model:

- Self-contained Node application binary.
- Bundled Node runtime plus packaged application resources.
- Native executable implemented without Node when dependency constraints permit.

For Tauri `externalBin`, produce the target-specific filename expected by the CLI, such as `name-aarch64-apple-darwin` or `name-x86_64-pc-windows-msvc.exe`. Generate the host tuple from the Rust toolchain where possible; do not hardcode the developer machine target into release scripts.

Declare the logical path in `bundle.externalBin`. Ensure CI builds every supported architecture and verifies that the exact binary is included, executable, signed where required, and covered by release checksums.

## Permission model

Initialize `tauri-plugin-shell` in Rust and scope `shell:allow-execute` to the declared sidecar. Restrict allowed arguments. Prefer Rust-side spawning so the frontend never receives a general process-execution primitive.

Never pass secrets through command-line arguments. Use an inherited pipe or another protected local channel. Avoid broad shell permissions even if frontend invocation is not currently implemented; future code can accidentally expose them.

## Transport and handshake

Prefer stdin/stdout framed messages or local sockets with OS-level ownership controls. If using localhost HTTP:

- Bind loopback only.
- Use an unguessable per-launch credential.
- Authenticate every connection or request.
- Reserve and communicate the port without a race.
- Reject browser origins and cross-site requests.
- Bound request bodies, concurrency, and timeouts.

Perform a handshake before normal traffic:

```json
{
  "protocolVersion": 1,
  "desktopVersion": "x.y.z",
  "sidecarVersion": "x.y.z",
  "provider": "codex-or-qoder",
  "capabilities": ["stream", "approve", "cancel", "resume"]
}
```

Fail closed on incompatible protocol versions. Capability negotiation may disable optional features but must not weaken required authorization or evidence behavior.

## Lifecycle

Rust Core must own this state machine:

```text
stopped -> starting -> handshaking -> ready -> draining -> stopped
                      |              |
                      v              v
                    failed <---------+
```

Required behavior:

- Single-flight startup per runtime profile.
- Startup deadline and bounded retry with backoff.
- Health determined from protocol messages, not process existence alone.
- Request cancellation propagated to the sidecar and underlying provider.
- Child exit mapped to structured in-flight request failures.
- Graceful drain before forced termination.
- Shutdown on application exit, update, logout, or workspace revocation.
- Startup cleanup for orphaned sockets, locks, and partial revisions.
- Redacted stdout/stderr with bounded retention.

Keep sidecar and desktop versions in one signed release until independent component updates have rollback, compatibility, signature, boot-health, and kill-switch mechanisms.

## Security checklist

- Is the artifact signed and verified before execution?
- Can an untrusted path select a different executable?
- Are executable and resource directories non-user-writable after installation?
- Are arguments constrained and free of secrets?
- Is the protocol authenticated, framed, size-limited, and versioned?
- Can another local process impersonate the sidecar?
- Are workspace and session scopes checked for every operation?
- Do crash, cancellation, and update paths terminate children reliably?
- Are logs redacted and protected from injection?

## Official references

- Node.js as a sidecar: https://v2.tauri.app/learn/sidecar-nodejs/
- Embedding external binaries: https://v2.tauri.app/develop/sidecar/
- Shell plugin: https://v2.tauri.app/plugin/shell/
