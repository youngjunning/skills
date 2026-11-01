# Exact PowerShell command execution

Use this guide whenever Codex must type or paste a command into PowerShell on the target Windows desktop.

## Build the command as tokens

Identify each token before typing:

1. command, function, script, or executable;
2. parameter names;
3. parameter values;
4. positional arguments;
5. operators such as `|`, `>`, `2>&1`, `;`, or `&&` when intentionally required.

Put a normal space between separate tokens. Preserve spaces that belong inside a quoted argument. Do not treat visual line wrapping as an actual newline.

Example:

```powershell
pnpm run test -- --filter 'Windows App'
```

The spaces around `run`, `test`, `--`, `--filter`, and the quoted value are token separators. The space inside `'Windows App'` belongs to one argument.

## Paths and quoting

Use literal single-quoted paths by default:

```powershell
Set-Location -LiteralPath 'D:\work\My App'
Get-Item -LiteralPath 'D:\output\result file.json'
```

Use PowerShell's call operator when an executable or script path is quoted:

```powershell
& 'C:\Program Files\My App\app.exe' --config 'D:\configs\release.json'
& 'D:\work\scripts\verify.ps1' -TargetPath 'D:\output\My Build'
```

Without `&`, a quoted executable path is only a string and will not execute.

Use double quotes only when PowerShell variable or expression expansion is intentional:

```powershell
Get-Item -LiteralPath "$env:TEMP\report.json"
```

Do not convert single quotes to double quotes casually. `$`, `$()`, and backticks change meaning inside double-quoted strings.

## Native executable arguments

Keep the executable separate from its arguments:

```powershell
& 'C:\Tools\tool.exe' --input 'D:\input file.txt' --output 'D:\out file.txt'
```

Do not wrap the entire command in one string:

```powershell
# Wrong: PowerShell treats this as one string.
'C:\Tools\tool.exe --input D:\input file.txt'
```

Do not insert shell operators unless they are part of the intended command. A semicolon, pipe, redirection, `&&`, or `||` can change ordering, output, and failure behavior.

## Submission gate

Before pressing Enter:

1. confirm the correct PowerShell window and prompt;
2. confirm the working directory;
3. compare the visible command with the prepared command from left to right;
4. check every space between tokens;
5. check paired single quotes, double quotes, parentheses, braces, and brackets;
6. check hyphens in parameter names and leading `--` for native CLI flags;
7. check backslashes, drive letters, filename extensions, and trailing slashes;
8. check that visual wrapping did not create or hide a newline;
9. submit exactly once.

If the command is truncated, malformed, or entered in the wrong prompt, do not press Enter. Clear the current line with `Ctrl+C`, re-observe the prompt, and enter the corrected command.

When typing through Windows App or Windows App Beta, treat the keyboard bridge as an additional verification boundary:

- Check the Windows input-language indicator before composing the command. Prefer an English keyboard layout for shell input.
- If shared paste times out, opens an IME candidate window, or inserts only a paste shortcut character such as `v`, treat the paste as failed and do not submit.
- Dismiss the IME state and clear the editable PowerShell line before retrying. If `Ctrl+C` is visibly swallowed by the IME or client, use `Escape` only after confirming the active surface is an ordinary PSReadLine prompt where it safely reverts the current line.
- Visual typing may lose capitalization or shifted symbols across the macOS-to-Windows boundary. Characters such as `?`, `(`, and `)` can arrive as their unshifted keys even when a modifier was requested.
- Prefer an equivalent command syntax that avoids an unreliable character when one exists. Otherwise stop after a bounded alternate-key attempt instead of submitting a command that differs from the reviewed text.

Always compare the rendered terminal line with the prepared command after the keyboard bridge, not only with the controller-side string that was sent.

## Multiline and long commands

Do not visually type a large script or a command whose correctness is hard to inspect in one terminal line. Put it in a reviewed `.ps1` file, then run:

```powershell
& 'D:\work\scripts\operation.ps1'
```

For a multi-line command that must remain inline, use PowerShell syntax deliberately. Do not add backticks merely to match visual wrapping; trailing whitespace after a backtick breaks continuation.

## Read the result accurately

For native executables:

```powershell
$LASTEXITCODE
```

For PowerShell commands and scripts:

```powershell
$?
```

When a command's success matters, print an explicit structured checkpoint:

```powershell
& 'C:\Tools\tool.exe' --verify
$exitCode = $LASTEXITCODE
[pscustomobject]@{
  exitCode = $exitCode
  succeeded = ($exitCode -eq 0)
  location = (Get-Location).Path
} | ConvertTo-Json
```

Do not run another native executable before reading `$LASTEXITCODE`, because the value would then refer to the later program.

An exit code of zero proves only the command's own success contract. Verify the requested app, file, service, build, or remote outcome separately.
