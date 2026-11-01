# Security, capability, and IPC reference

## Contents

1. Trust model
2. Capability design
3. Remote WebViews
4. IPC selection
5. Command implementation
6. Review checklist
7. Official references

## Trust model

Model these principals separately:

- Rust Core: full operating-system authority; every bug can cross the application boundary.
- Bundled local WebView: application code, but still exposed to frontend and dependency compromise.
- Remote WebView: network-controlled content; grant zero local capability by default.
- Node sidecar: native process with its own dependency and protocol attack surface.
- Agent provider: replaceable executor; do not give it ownership of application policy or workflow state.

Document every data flow that crosses between principals. Validate at the receiving boundary even when the sender also validates.

## Capability design

Store capabilities in `src-tauri/capabilities/`. Prefer one capability per privilege domain or window role.

For each capability:

1. Name the intended window or WebView labels explicitly.
2. Restrict platforms when the permission is platform-specific.
3. Include only required plugin commands.
4. Add scopes for paths, URLs, binaries, and arguments.
5. Explain why each high-risk permission exists.
6. Test that excluded windows and inputs are denied.

Avoid overlapping capabilities for the same window: permissions merge, which can silently widen the boundary. Remember that application commands registered through `invoke_handler` require their own authorization strategy; generated plugin permissions do not replace command-level checks.

Use generated schemas under `src-tauri/gen/schemas/` to validate identifiers against the exact dependency set.

## Remote WebViews

Prefer a separate `WebviewWindow` for remote content. Enforce all of the following:

- Dedicated label and navigation policy.
- No local capabilities by default.
- Strict allowlist for origins and redirects.
- Declarative intent messages only.
- Rust-side checks for origin, label, authenticated user, workspace, action, and payload.
- Local trusted UI for permission prompts and destructive confirmations.

Do not assume an iframe creates a security boundary. Platform WebView behavior differs, and some platforms cannot reliably distinguish iframe-originated requests from the containing window.

## IPC selection

### Commands

Use for request/response operations with bounded payloads. Define serializable request and response types. Return stable error codes plus safe messages instead of leaking internal paths or stack traces.

### Channels

Use for ordered streaming such as Agent output, progress, or process events. Include sequence, run/session identifiers, terminal state, and cancellation semantics. Bound queues and payload sizes.

### Events

Use for low-volume notification or broadcast. Do not use events for privileged request/response operations or guaranteed delivery.

### Sidecar protocol

Prefer framed structured messages over parsing console text. Include protocol version, request ID, operation, workspace scope, deadline, and structured error. Reject unknown fields or operations according to the compatibility policy.

## Command implementation

For every sensitive command:

1. Deserialize into a typed request.
2. Enforce size and format limits.
3. Resolve caller context from trusted application state.
4. Authorize identity, workspace, session, capability, and action.
5. Canonicalize paths and prevent traversal or symlink escape.
6. Execute without shell interpolation.
7. Record a redacted audit event.
8. Return a stable typed result.

Keep `main.rs` thin and place testable application construction and command logic in library modules.

## Review checklist

- Can compromised frontend code reach a new OS resource?
- Can one window exercise another window's permission?
- Can remote content navigate into a privileged origin?
- Are path and shell scopes narrower than the command's validation?
- Are custom commands authorized beyond simple registration?
- Can payload size or event rate cause memory or CPU exhaustion?
- Are secrets present in logs, URLs, CLI arguments, or errors?
- Are cancellation and partial failure safe and idempotent?

## Official references

- Tauri security: https://v2.tauri.app/security/
- Capabilities: https://v2.tauri.app/security/capabilities/
- Core permissions: https://v2.tauri.app/reference/acl/core-permissions/
- Plugin permissions: https://v2.tauri.app/learn/security/using-plugin-permissions/
- IPC concepts: https://v2.tauri.app/concept/inter-process-communication/
- Tauri 1 to 2 migration: https://v2.tauri.app/start/migrate/from-tauri-1/
