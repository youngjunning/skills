# Windows App Automation

A Codex Skill for operating Windows desktop applications with an evidence-driven automation loop.

It supports three practical control surfaces:

- native Windows Computer Use;
- Microsoft Windows App, Windows App Beta, Remote Desktop, or VM viewers controlled from another desktop;
- Windows UI Automation through the bundled PowerShell helper.

When a task needs command execution, the Skill opens PowerShell in the target Windows desktop, verifies the prompt and working directory, compares spaces and quoting character-for-character, executes one logical command at a time, and reads the output plus exit status. It does not silently move command execution to `cmd.exe`, WSL, SSH, WinRM, or the controller machine.

The Skill prefers stable accessibility selectors, uses visual clicks only as a fallback, and treats every action as incomplete until the resulting application state is verified.

On macOS it recognizes `Windows App Beta` as `com.microsoft.rdc.osx.beta`. It can reuse an already-authorized session, but it still verifies the visible connection and target Windows desktop instead of inferring a host from the app name.

## What it is for

Use it to:

- operate settings, forms, file dialogs, installers, and ordinary Win32/WPF/WinUI applications;
- inspect a Windows application's UI Automation tree;
- reproduce and verify desktop UI bugs;
- control an already-authorized remote Windows session;
- monitor long-running GUI work without mistaking progress for completion;
- capture screenshots and machine-readable control state as evidence.

It is not a remote-access server, a credential manager, or a security-prompt bypass. You still need a supported Computer Use surface or an existing way to reach the Windows device.

## Install

Ask Codex to install the public repository:

```text
$skill-installer install https://github.com/youngjunning/skills/tree/main/skills/engineering/windows-app-automation
```

Or use the shared repository installer:

```bash
npx skills add youngjunning/skills --skill windows-app-automation -g
```

Codex detects Skill changes automatically. Restart Codex if it does not appear in `/skills`.

## Use

Invoke it explicitly with `$windows-app-automation`, or describe a Windows desktop task that matches the Skill description.

```text
$windows-app-automation 打开 Windows 设置，把默认浏览器改成指定应用，重开页面确认设置已持久化。
```

```text
$windows-app-automation 复用已经登录的 Microsoft Windows App 会话，打开目标应用，导出报告到指定路径，并核对文件确实生成。
```

```text
$windows-app-automation 在远程 Windows 桌面打开 PowerShell，进入 C:\work\my-app，执行测试命令，读取完整输出和退出码。
```

```text
$windows-app-automation inspect MyApp's UI Automation tree, select the Stable channel, save it, and verify the value after reopening Settings.
```

For sensitive flows, enter passwords, MFA codes, administrator credentials, certificate decisions, and payment data yourself. The Skill tells Codex to pause and re-observe the application after handoff.

## PowerShell helper

[`scripts/windows-ui.ps1`](scripts/windows-ui.ps1) uses Windows' built-in UI Automation assemblies. It requires no Appium server, WinAppDriver, or third-party PowerShell module.

Discover top-level windows:

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 -Action ListWindows
```

Inspect an accessibility tree:

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action DumpTree `
  -ProcessName notepad `
  -WindowTitle '*Notepad*' `
  -MaxDepth 4
```

Invoke a control by stable selector:

```powershell
pwsh -NoProfile -File .\scripts\windows-ui.ps1 `
  -Action Invoke `
  -ProcessName MyApp `
  -AutomationId SaveButton `
  -ControlType Button
```

The helper emits JSON and supports:

`ListWindows`, `DumpTree`, `WaitFor`, `GetState`, `Focus`, `Invoke`, `SetValue`, `Toggle`, `Select`, `Click`, `SendKeys`, and `Screenshot`.

Read [the UI Automation guide](references/windows-uia.md) for selector rules and complete examples.

## Reliability model

The workflow is intentionally strict:

```text
observe -> target -> act -> verify -> record
```

- `AutomationId` and UIA patterns come before coordinates.
- Every navigation or reconnect invalidates cached visual assumptions.
- A click, process start, closed dialog, or full progress bar is not completion evidence.
- Remote connection, app action, save, submission, and target-host readback are separate states.
- Repeated unchanged failures stop with the last observed state instead of looping blindly.

## Windows session constraints

UI Automation must run in the same interactive Windows session as the target application. A shell opened through SSH, WinRM, CI, a service, or a disconnected RDP session may run successfully while seeing no visible UI. A non-elevated helper also cannot reliably control an elevated application.

When those boundaries apply, use Computer Use for visible UI and use the shell only for process, file, and log evidence. Do not auto-elevate or bypass UAC.

## Repository layout

```text
.
├── SKILL.md
├── agents/openai.yaml
├── scripts/windows-ui.ps1
├── references/
│   ├── windows-uia.md
│   ├── remote-sessions.md
│   ├── playbooks.md
│   ├── powershell-execution.md
│   └── verification-and-recovery.md
└── tests/
```

## Validation

```bash
python3 tests/validate_structure.py
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

GitHub Actions also parses the PowerShell script and runs a `ListWindows` JSON-contract smoke test on `windows-latest`.

## License

[MIT](LICENSE)
