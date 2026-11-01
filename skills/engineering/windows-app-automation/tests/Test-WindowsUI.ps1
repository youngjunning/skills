$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$scriptPath = Join-Path (Split-Path -Parent $PSScriptRoot) 'scripts\windows-ui.ps1'
$tokens = $null
$errors = $null
$null = [System.Management.Automation.Language.Parser]::ParseFile(
    $scriptPath,
    [ref]$tokens,
    [ref]$errors
)

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_.Message }
    exit 1
}

$output = & pwsh -NoProfile -File $scriptPath -Action ListWindows
$scriptExitCode = $LASTEXITCODE

$result = $output | ConvertFrom-Json
if ($result.action -ne 'ListWindows') {
    throw 'ListWindows did not return the expected JSON contract.'
}

if ($scriptExitCode -eq 0 -and -not $result.ok) {
    throw 'ListWindows exited successfully but returned ok=false.'
}

if ($scriptExitCode -ne 0) {
    if ($result.ok -or $result.message -notmatch 'interactive Windows user session') {
        throw "ListWindows failed unexpectedly: $output"
    }
    Write-Output 'PowerShell parser passed; UI smoke test correctly reported the non-interactive runner boundary.'
    exit 0
}

Write-Output 'PowerShell parser and ListWindows smoke test passed.'
