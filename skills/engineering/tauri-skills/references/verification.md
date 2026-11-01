# Verification and delivery gate

## Contents

1. Test layers
2. Security assertions
3. Build and packaging
4. Evidence receipt
5. Official references

## Test layers

### Rust unit tests

Test policy, parsers, state transitions, path validation, authorization, protocol framing, compatibility, and error normalization without a real WebView.

### Tauri integration tests

Use Tauri's mock runtime for command wiring and managed state where it represents the behavior accurately. Keep application construction testable outside the production entry point.

### Frontend seam tests

Mock IPC at the Tauri API boundary. Assert observable behavior and typed contracts, not private component structure. Test command rejection, channel terminal states, and cancellation.

### Sidecar contract tests

Run a deterministic fake sidecar to test handshake, request correlation, streaming order, invalid messages, timeout, crash, cancellation, and version mismatch. Maintain fixtures for at least the current and previous supported protocol versions.

### End-to-end tests

Use WebDriver or platform-appropriate automation for critical user paths. Account for platform limitations instead of assuming one driver behaves identically everywhere.

## Security assertions

Add negative tests for:

- Unlisted window or WebView labels.
- Remote or unexpected origins.
- Cross-workspace and cross-session access.
- Path traversal and symlink escape.
- Disallowed sidecar arguments and executable names.
- Oversized, malformed, reordered, duplicated, or unknown protocol messages.
- Missing approval, revoked permission, and stale revision.

Review generated capability schemas and built artifacts, not only source configuration.

## Build and packaging

For each affected target:

1. Run formatter, linter, TypeScript check, Rust check, and focused tests.
2. Build the frontend and Tauri application according to repository policy.
3. Confirm the correct target-specific sidecar exists in the package.
4. Inspect signing, entitlements, permissions, checksums, and updater metadata.
5. Launch the installed artifact, complete the sidecar handshake, and exercise one privileged denial path.
6. Verify graceful quit, crash recovery, and update-safe shutdown.

Do not claim cross-platform support from a single-host build.

## Evidence receipt

Record:

```text
change/spec:
commit:
target platforms:
commands run:
tests passed:
capabilities changed:
sidecar protocol/version:
artifacts inspected:
manual checks:
known limitations:
reviewer/date:
```

Block archive or release when a required field lacks evidence. A task checkbox is not evidence.

## Official references

- Tauri tests: https://v2.tauri.app/develop/tests/
- WebDriver: https://v2.tauri.app/develop/tests/webdriver/
- Distribute: https://v2.tauri.app/distribute/
- Updater plugin: https://v2.tauri.app/plugin/updater/
