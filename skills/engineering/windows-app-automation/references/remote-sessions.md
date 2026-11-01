# Microsoft Windows App and remote desktop sessions

Use this guide when Codex controls a Windows desktop through Microsoft Windows App, Remote Desktop, a VM viewer, or another nested display.

## Windows App clients on macOS

Microsoft Windows App may be exposed as either `Windows App` or `Windows App Beta`. The beta client's bundle identifier is `com.microsoft.rdc.osx.beta`.

- Discover the installed client name instead of assuming the stable name also matches the beta application.
- Use the bundle identifier to discover or inspect the beta client when Computer Use cannot resolve a display name.
- Prefer the exact discovered display name for click, key, typing, and paste actions. If bundle-ID actions return `noWindowsAvailable` while state inspection still shows a window, re-read state and retry once with the exact display name.
- The macOS accessibility tree may expose only the outer Windows App window and menu bar, not controls inside the rendered Windows desktop. In that case, use a fresh screenshot, verify the remote window geometry, perform one coordinate action, and immediately re-observe.
- If Computer Use reports that the user changed the app, discard the pending action and re-query the full state before continuing.

An app name or bundle identifier proves only which controller client is open, not which Windows host or account is connected.

## Connection boundary

Treat these as distinct layers:

1. the controller device and its app permissions;
2. the remote desktop client window;
3. the selected saved connection or workspace;
4. the authenticated Windows session;
5. the target application inside that session;
6. the requested application outcome.

Reaching an earlier layer does not prove a later one. An open Windows App window is not proof that the intended host is connected. A connected desktop is not proof that the target app is ready. A progress indicator is not proof that a job finished.

## Connect safely

- Prefer an already-open, already-authenticated session explicitly identified by the user or by visible connection metadata.
- Do not infer an IP address, hostname, username, environment, or privilege level from a friendly tile or window title.
- Do not enumerate unrelated saved desktops or workspaces when one target is already in scope.
- Stop for password, MFA, smart-card, certificate trust, privacy consent, or administrator prompts. The user completes these steps.
- After the user returns control, inspect the full remote desktop again before continuing.

## Nested-desktop coordinate model

Coordinates from the controller refer to the remote desktop client's rendered surface, not directly to Windows screen coordinates. They become stale when any of these changes:

- the client window moves or resizes;
- full-screen mode changes;
- the remote resolution or DPI scale changes;
- a toolbar appears or auto-hides;
- multiple monitors are enabled or reordered;
- the remote session reconnects;
- display scaling or dynamic resolution updates.

After any such change, discard old coordinates and take a fresh screenshot. Prefer accessibility/UIA selectors on the Windows side when available.

## Focus and keyboard ownership

Before typing:

1. confirm the remote client is the active controller window;
2. confirm the expected Windows app is foreground inside it;
3. confirm the intended field has focus or a caret;
4. type the smallest meaningful unit;
5. verify the resulting text or state.

Do not send global shortcuts until you know whether the controller OS, remote client, or Windows guest will consume them. Clipboard sharing is also a cross-system boundary: avoid copying secrets, and clear sensitive clipboard content if the user explicitly used it during a handoff.

## Disconnect, lock, and reconnect

UI state may stop updating when the controller sleeps, the remote client disconnects, Windows locks, or the RDP session is minimized by some clients. Long-running non-UI work may continue, but visual automation and UIA evidence are no longer trustworthy.

On reconnect:

1. identify the actual Windows session and target app;
2. inspect for lock screens, reconnect banners, error dialogs, or changed resolution;
3. re-resolve the target window and controls;
4. determine whether the last action completed, partially completed, or did not run;
5. resume from an observed checkpoint, not from the last attempted click.

Avoid duplicate submissions after a reconnect. Check output files, status text, history, or server-side state before repeating a consequential action.

## Remote shell is not the visible desktop

SSH and WinRM commonly create a different logon session from the visible RDP desktop. A process started there can successfully run while seeing no target UI. Likewise, a service or scheduled task may run in session 0.

Before using the PowerShell UIA helper remotely, verify all of the following:

- the command runs under the same user as the visible app;
- the process is in the same interactive session ID;
- the desktop is unlocked and connected;
- helper and target app have compatible integrity levels.

If these conditions cannot be established, use the visual controller for UI actions and reserve the remote shell for file, process, and log evidence.

## Evidence from the target host

For completion, prefer evidence produced inside Windows:

- visible final state plus a screenshot;
- target process and version;
- UIA control state;
- created or changed file with path, size, and timestamp;
- application log or exit code;
- installer/package/signature state;
- a successful reopen or readback of the saved result.

State explicitly when evidence comes only from the controller view. It may prove visible behavior without proving file integrity, remote service acceptance, installation, signing, or persistence after restart.
