# Windows application playbooks

Use only the playbook that matches the requested operation. These are decision guides, not permission to expand scope.

## Execute a command in PowerShell

1. Open PowerShell inside the target Windows desktop.
2. Confirm the remote session, PowerShell title, prompt, and current directory.
3. Use `Set-Location -LiteralPath 'C:\exact\path'` when the command has a required working directory.
4. Type or paste one logical command, compare it character-for-character for spaces, quoting, escaping, truncation, and line wrapping, then submit it.
5. Wait for the command to finish. Do not infer completion from silence or a temporarily idle cursor.
6. Read the full output. For native programs, run or inspect `$LASTEXITCODE`; for PowerShell commands, inspect `$?` and terminating errors.
7. Verify any claimed file, process, service, build, or application result through an independent readback.

Prefer `-LiteralPath` for user-provided paths. Avoid command strings assembled from untrusted UI text. Do not place passwords, tokens, private keys, recovery material, or payment data on the command line or clipboard.

Load `powershell-execution.md` for exact path, argument, native-executable, and exit-code rules.

For a long or reusable script, invoke a verified `.ps1` file by exact path instead of typing many lines into the terminal. If the current Computer Use implementation refuses terminal control, preserve the intended command and report the restriction; do not switch to an unrelated remote session or attempt a bypass.

## Launch and identify an application

1. Discover whether the app is already running.
2. If launch is required, use an approved app launcher or open PowerShell in the target desktop; stop if the active host disallows terminal automation.
3. Match the executable, process ID, product name, and top-level window. Do not rely on a generic title such as `Settings` or `Login` alone.
4. Wait for the app's real ready state, not merely for the process to exist.
5. Record the app version when version-specific behavior matters.

If multiple versions or profiles are present, stop before changing state until the intended one is identifiable.

## Change an application setting

1. Capture the current value.
2. Navigate to the exact settings page and verify its heading.
3. Change one setting.
4. Observe whether the app requires `Apply`, `Save`, restart, sign-out, or elevated approval.
5. Reopen or revisit the settings page and read the persisted value.

A toggled visual switch before save is not persistence evidence.

## Work with a file picker

1. Confirm whether the dialog is `Open`, `Save`, `Save As`, folder selection, or export.
2. Prefer entering an absolute path into the filename/location field over navigating a long folder tree.
3. Verify the final path and file type before confirmation.
4. For overwrite prompts, compare the exact existing target and stop if overwrite was not authorized.
5. After the dialog closes, verify both application state and the file on disk.

Do not treat the dialog closing as proof that the file was saved successfully.

## Fill and submit a form

1. Map required fields and identify validation messages.
2. Fill fields with `SetValue` when supported; otherwise focus and type one field at a time.
3. Read back critical values, especially destination, account, quantity, path, and environment.
4. Treat `Submit`, `Send`, `Publish`, `Purchase`, and destructive confirmations as consequential actions.
5. After submission, verify a confirmation identifier or authoritative resulting state. Avoid resubmission until duplicate risk is ruled out.

## Install, update, or uninstall

1. Confirm the exact product, publisher, source, version, architecture, and target device.
2. Inspect signature or publisher information when available. Do not bypass SmartScreen or certificate warnings.
3. Record the pre-operation version and whether the app is running.
4. Follow the installer one state at a time. Do not accept unrelated bundled software or change system-wide defaults without authorization.
5. Stop for UAC or administrator authentication.
6. Verify completion through installed version, executable path, launch behavior, and requested feature—not only an installer's final page.
7. For uninstall, identify user data retention separately from binary removal.

## Operate a long-running task

1. Establish the start evidence: task identifier, input, output path, start time, and initial status.
2. Choose a polling interval proportional to expected duration; avoid rapid visual polling.
3. At each poll, inspect progress text, activity, elapsed time, errors, and whether the same task is still active.
4. Distinguish progress, stalled, failed, canceled, and completed.
5. Verify final output independently. A full progress bar or missing spinner is not sufficient.

If the session disconnects, use the reconnect procedure in `remote-sessions.md` before deciding whether to restart.

## Reproduce a UI bug

1. Record app version, Windows version, display scale, window size, theme, locale, and input method when relevant.
2. Capture the clean starting state.
3. Perform the minimal deterministic action sequence.
4. Capture the first incorrect state before taking recovery actions.
5. Repeat only when repetition is safe and needed to establish reproducibility.
6. Separate visual evidence from suspected root cause. Do not diagnose source code from appearance alone.

## Recover from an unexpected dialog

1. Stop sending input.
2. Read the dialog title, body, buttons, origin process, and whether it is modal.
3. Classify it: expected confirmation, validation, authentication, security, crash, update, conflict, or unrelated interruption.
4. Preserve error text and screenshots.
5. Continue only when one option clearly preserves the user's goal and authorization. Otherwise request a decision.

Never dismiss a dialog merely to unblock the automation; it may contain the actual result or safety boundary.
