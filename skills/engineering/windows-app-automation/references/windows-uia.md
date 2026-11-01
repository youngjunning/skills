# Windows UI Automation helper

Use `scripts/windows-ui.ps1` when an interactive PowerShell process runs in the same Windows desktop session and at a compatible integrity level as the target app. The helper uses the Windows UI Automation API included with Windows; it does not install a driver or background service.

## Start with discovery

List visible top-level windows:

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 -Action ListWindows
```

Inspect one app's accessibility tree:

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action DumpTree `
  -ProcessName notepad `
  -WindowTitle '*Notepad*' `
  -MaxDepth 4
```

The helper emits JSON. Record the useful `processId`, `name`, `automationId`, `controlType`, `className`, `enabled`, `offscreen`, and `bounds` fields. Prefer an `automationId` that remains stable across runs.

## Resolve one control

Selectors are combined with AND. The helper searches descendants of the selected top-level window.

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action GetState `
  -ProcessName MyApp `
  -WindowTitle 'Settings*' `
  -AutomationId SaveButton `
  -ControlType Button
```

If several elements match, discovery actions return all candidates. Mutating actions fail unless `-Index` is supplied. Inspect the candidate list before choosing an index; do not guess.

Selector stability, strongest first:

1. `ProcessName + WindowTitle + AutomationId`
2. `ProcessName + WindowTitle + Name + ControlType`
3. `ClassName` combined with another property
4. explicit `Index` after inspecting current candidates
5. coordinate fallback from a new screenshot

`WindowTitle`, `Name`, `AutomationId`, and `ClassName` accept PowerShell wildcard patterns such as `Save*`. Wildcards require an in-memory filter, so use an exact value when possible.

## Supported actions

### Wait for a control

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action WaitFor `
  -ProcessName MyApp `
  -AutomationId ReadyIndicator `
  -TimeoutSeconds 30
```

### Invoke a button or menu item

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action Invoke `
  -ProcessName MyApp `
  -AutomationId SaveButton
```

Use `Invoke` before coordinate clicking when the control supports `InvokePattern`.

### Set a text value

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action SetValue `
  -ProcessName MyApp `
  -AutomationId ProjectName `
  -Value 'Quarterly review'
```

This requires `ValuePattern` and an enabled, non-read-only element. Use visual typing only when the app does not expose the pattern, and verify focus first.

### Toggle or select

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action Toggle `
  -ProcessName MyApp `
  -AutomationId EnableNotifications

pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action Select `
  -ProcessName MyApp `
  -Name 'Stable channel' `
  -ControlType RadioButton
```

Read the returned state, then call `GetState` again if the surrounding UI should also change.

### Focus and send keys

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action SendKeys `
  -ProcessName MyApp `
  -AutomationId SearchBox `
  -Keys 'release notes{ENTER}'
```

`SendKeys` uses .NET `SendWait` syntax. Characters such as `+`, `^`, `%`, `~`, `(`, `)`, `{`, and `}` have special meanings. Prefer `SetValue` for literal text.

### Click a custom control

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action Click `
  -ProcessName MyApp `
  -Name 'Apply' `
  -ControlType Button
```

`Click` uses the UIA clickable point or the center of the current bounding rectangle. It is a fallback for controls that do not expose an action pattern. It moves the real pointer and affects the foreground desktop.

### Capture evidence

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action Screenshot `
  -ProcessName MyApp `
  -WindowTitle '*My App*' `
  -OutFile "$PWD\artifacts\my-app-after.png"
```

The parent directory is created when needed. A screenshot proves only what is visibly present; pair it with application state or output evidence when a visual look alone is insufficient.

## Pattern failures

An element can be visible yet expose no useful UIA patterns. Common causes include custom canvases, games, Chromium/Electron accessibility being disabled, owner-drawn controls, and cross-integrity boundaries.

When a pattern is missing:

1. inspect the tree again at a larger `MaxDepth`;
2. check whether a parent or child exposes the action;
3. verify the app and helper have compatible elevation;
4. use keyboard navigation if focus is observable;
5. use Computer Use or one verified coordinate click as the final fallback.

Do not loop the same unsupported pattern call.

## Session boundary

`Environment.UserInteractive = true` is necessary but not sufficient. The helper cannot make a WinRM, SSH, service, CI, or disconnected RDP session control another user's visible desktop. Run it through an approved execution surface attached to the same interactive session, or use Computer Use directly.
