[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('ListWindows', 'DumpTree', 'WaitFor', 'GetState', 'Focus', 'Invoke', 'SetValue', 'Toggle', 'Select', 'Click', 'SendKeys', 'Screenshot')]
    [string]$Action,

    [string]$ProcessName,
    [int]$TargetProcessId,
    [string]$WindowTitle,
    [string]$Name,
    [string]$AutomationId,
    [string]$ControlType,
    [string]$ClassName,
    [int]$Index = -1,
    [string]$Value,
    [string]$Keys,
    [string]$OutFile,
    [ValidateRange(1, 3600)]
    [int]$TimeoutSeconds = 15,
    [ValidateRange(0, 20)]
    [int]$MaxDepth = 5
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Write-JsonResult {
    param(
        [bool]$Ok,
        [string]$Operation,
        [object]$Data,
        [string]$Message
    )

    [ordered]@{
        ok        = $Ok
        action    = $Operation
        message   = $Message
        data      = $Data
        timestamp = [DateTimeOffset]::Now.ToString('o')
    } | ConvertTo-Json -Depth 12
}

function Assert-WindowsInteractiveSession {
    if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
        throw 'windows-ui.ps1 can only run on Windows.'
    }
    if (-not [Environment]::UserInteractive) {
        throw 'UI Automation requires an interactive Windows user session.'
    }
}

function Import-DesktopAssemblies {
    Add-Type -AssemblyName UIAutomationClient
    Add-Type -AssemblyName UIAutomationTypes
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    if (-not ('WindowsAppAutomation.NativeMethods' -as [type])) {
        Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;

namespace WindowsAppAutomation {
    public static class NativeMethods {
        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetForegroundWindow(IntPtr hWnd);

        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetCursorPos(int x, int y);

        [DllImport("user32.dll")]
        public static extern void mouse_event(uint flags, uint dx, uint dy, uint data, UIntPtr extraInfo);
    }
}
'@
    }
}

function Test-WildcardValue {
    param([string]$Actual, [string]$Expected)
    if ([string]::IsNullOrWhiteSpace($Expected)) { return $true }
    return $Actual -like $Expected
}

function Get-ControlTypeValue {
    param([string]$RequestedControlType)
    if ([string]::IsNullOrWhiteSpace($RequestedControlType)) { return $null }

    $property = [System.Windows.Automation.ControlType].GetProperty(
        $RequestedControlType,
        [Reflection.BindingFlags]'Public,Static,IgnoreCase'
    )
    if ($null -eq $property) {
        throw "Unknown ControlType '$RequestedControlType'. Examples: Button, Edit, CheckBox, RadioButton, MenuItem, ListItem, Text."
    }
    return $property.GetValue($null, $null)
}

function Get-BoundsObject {
    param([System.Windows.Rect]$Rectangle)
    [ordered]@{
        x      = $Rectangle.X
        y      = $Rectangle.Y
        width  = $Rectangle.Width
        height = $Rectangle.Height
    }
}

function Get-ElementDescriptor {
    param([System.Windows.Automation.AutomationElement]$Element)

    $patterns = @()
    try {
        $patterns = @($Element.GetSupportedPatterns() | ForEach-Object { $_.ProgrammaticName })
    } catch {
        $patterns = @()
    }

    $bounds = $Element.Current.BoundingRectangle
    [ordered]@{
        processId    = $Element.Current.ProcessId
        name         = $Element.Current.Name
        automationId = $Element.Current.AutomationId
        controlType  = $Element.Current.ControlType.ProgrammaticName -replace '^ControlType\.', ''
        className    = $Element.Current.ClassName
        enabled      = $Element.Current.IsEnabled
        offscreen    = $Element.Current.IsOffscreen
        hasFocus     = $Element.Current.HasKeyboardFocus
        bounds       = Get-BoundsObject -Rectangle $bounds
        patterns     = $patterns
    }
}

function Get-TopLevelWindows {
    $root = [System.Windows.Automation.AutomationElement]::RootElement
    $elements = $root.FindAll(
        [System.Windows.Automation.TreeScope]::Children,
        [System.Windows.Automation.Condition]::TrueCondition
    )

    $matches = @()
    foreach ($element in $elements) {
        if ($TargetProcessId -gt 0 -and $element.Current.ProcessId -ne $TargetProcessId) { continue }

        if (-not [string]::IsNullOrWhiteSpace($ProcessName)) {
            try {
                $process = Get-Process -Id $element.Current.ProcessId -ErrorAction Stop
                if ($process.ProcessName -notlike $ProcessName) { continue }
            } catch {
                continue
            }
        }

        if (-not (Test-WildcardValue -Actual $element.Current.Name -Expected $WindowTitle)) { continue }
        $matches += $element
    }
    return @($matches)
}

function Select-TopLevelWindow {
    $windows = @(Get-TopLevelWindows)
    if ($windows.Count -eq 0) {
        throw 'No top-level window matched the process and window selectors.'
    }
    if ($windows.Count -gt 1) {
        $candidates = @($windows | ForEach-Object { Get-ElementDescriptor -Element $_ })
        throw "Multiple top-level windows matched. Narrow ProcessName, TargetProcessId, or WindowTitle. Candidates: $($candidates | ConvertTo-Json -Compress -Depth 8)"
    }
    return $windows[0]
}

function Get-DescendantMatches {
    param([System.Windows.Automation.AutomationElement]$Window)

    $requestedType = Get-ControlTypeValue -RequestedControlType $ControlType
    $elements = $Window.FindAll(
        [System.Windows.Automation.TreeScope]::Descendants,
        [System.Windows.Automation.Condition]::TrueCondition
    )

    $matches = @()
    foreach ($element in $elements) {
        if (-not (Test-WildcardValue -Actual $element.Current.Name -Expected $Name)) { continue }
        if (-not (Test-WildcardValue -Actual $element.Current.AutomationId -Expected $AutomationId)) { continue }
        if (-not (Test-WildcardValue -Actual $element.Current.ClassName -Expected $ClassName)) { continue }
        if ($null -ne $requestedType -and $element.Current.ControlType -ne $requestedType) { continue }
        $matches += $element
    }
    return @($matches)
}

function Test-ControlSelectorPresent {
    return -not (
        [string]::IsNullOrWhiteSpace($Name) -and
        [string]::IsNullOrWhiteSpace($AutomationId) -and
        [string]::IsNullOrWhiteSpace($ControlType) -and
        [string]::IsNullOrWhiteSpace($ClassName)
    )
}

function Resolve-Control {
    param([System.Windows.Automation.AutomationElement]$Window)

    if (-not (Test-ControlSelectorPresent)) {
        return $Window
    }

    $matches = @(Get-DescendantMatches -Window $Window)
    if ($matches.Count -eq 0) {
        throw 'No control matched the supplied selectors.'
    }
    if ($Index -ge 0) {
        if ($Index -ge $matches.Count) {
            throw "Index $Index is outside the $($matches.Count) matched controls."
        }
        return $matches[$Index]
    }
    if ($matches.Count -gt 1) {
        $candidates = @($matches | ForEach-Object { Get-ElementDescriptor -Element $_ })
        throw "Multiple controls matched. Narrow the selector or pass an inspected zero-based Index. Candidates: $($candidates | ConvertTo-Json -Compress -Depth 8)"
    }
    return $matches[0]
}

function Get-TreeNode {
    param(
        [System.Windows.Automation.AutomationElement]$Element,
        [int]$Depth,
        [int]$DepthLimit
    )

    $node = Get-ElementDescriptor -Element $Element
    if ($Depth -ge $DepthLimit) {
        $node.children = @()
        return $node
    }

    $children = @()
    $walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
    $child = $walker.GetFirstChild($Element)
    while ($null -ne $child) {
        $children += Get-TreeNode -Element $child -Depth ($Depth + 1) -DepthLimit $DepthLimit
        $child = $walker.GetNextSibling($child)
    }
    $node.children = $children
    return $node
}

function Set-WindowForeground {
    param([System.Windows.Automation.AutomationElement]$Window)
    $handle = [IntPtr]$Window.Current.NativeWindowHandle
    if ($handle -eq [IntPtr]::Zero) {
        throw 'The selected window has no native window handle.'
    }
    $null = [WindowsAppAutomation.NativeMethods]::SetForegroundWindow($handle)
    Start-Sleep -Milliseconds 200
}

function Get-Pattern {
    param(
        [System.Windows.Automation.AutomationElement]$Element,
        [System.Windows.Automation.AutomationPattern]$Pattern,
        [string]$PatternName
    )
    try {
        return $Element.GetCurrentPattern($Pattern)
    } catch {
        throw "The selected element does not support $PatternName."
    }
}

function Save-ElementScreenshot {
    param(
        [System.Windows.Automation.AutomationElement]$Element,
        [string]$Path
    )
    if ([string]::IsNullOrWhiteSpace($Path)) {
        throw 'Screenshot requires -OutFile.'
    }

    $bounds = $Element.Current.BoundingRectangle
    if ($bounds.IsEmpty -or $bounds.Width -le 0 -or $bounds.Height -le 0) {
        throw 'The selected element has empty or invalid screen bounds.'
    }

    $resolvedPath = [IO.Path]::GetFullPath($Path)
    $parent = Split-Path -Parent $resolvedPath
    if (-not [string]::IsNullOrWhiteSpace($parent)) {
        $null = New-Item -ItemType Directory -Path $parent -Force
    }

    $bitmap = New-Object Drawing.Bitmap ([int][Math]::Ceiling($bounds.Width)), ([int][Math]::Ceiling($bounds.Height))
    $graphics = [Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.CopyFromScreen(
            [int][Math]::Floor($bounds.X),
            [int][Math]::Floor($bounds.Y),
            0,
            0,
            $bitmap.Size,
            [Drawing.CopyPixelOperation]::SourceCopy
        )
        $bitmap.Save($resolvedPath, [Drawing.Imaging.ImageFormat]::Png)
    } finally {
        $graphics.Dispose()
        $bitmap.Dispose()
    }
    return $resolvedPath
}

try {
    Assert-WindowsInteractiveSession
    Import-DesktopAssemblies

    if ($Action -eq 'ListWindows') {
        $windows = @(Get-TopLevelWindows | ForEach-Object { Get-ElementDescriptor -Element $_ })
        Write-JsonResult -Ok $true -Operation $Action -Data $windows -Message "Found $($windows.Count) matching top-level window(s)."
        exit 0
    }

    if ($Action -eq 'WaitFor') {
        $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
        $element = $null
        $lastWaitError = $null
        do {
            try {
                $window = Select-TopLevelWindow
                $element = Resolve-Control -Window $window
            } catch {
                $element = $null
                $lastWaitError = $_.Exception.Message
            }
            if ($null -ne $element) { break }
            Start-Sleep -Milliseconds 250
        } while ([DateTime]::UtcNow -lt $deadline)

        if ($null -eq $element) {
            throw "Timed out after $TimeoutSeconds second(s) waiting for the requested window or control. Last observation: $lastWaitError"
        }
        Write-JsonResult -Ok $true -Operation $Action -Data (Get-ElementDescriptor -Element $element) -Message 'Requested element is present.'
        exit 0
    }

    $window = Select-TopLevelWindow

    if ($Action -eq 'DumpTree') {
        $tree = Get-TreeNode -Element $window -Depth 0 -DepthLimit $MaxDepth
        Write-JsonResult -Ok $true -Operation $Action -Data $tree -Message "Captured UI Automation tree to depth $MaxDepth."
        exit 0
    }

    $element = Resolve-Control -Window $window

    switch ($Action) {
        'GetState' {
            Write-JsonResult -Ok $true -Operation $Action -Data (Get-ElementDescriptor -Element $element) -Message 'Read current element state.'
        }
        'Focus' {
            Set-WindowForeground -Window $window
            $element.SetFocus()
            Write-JsonResult -Ok $true -Operation $Action -Data (Get-ElementDescriptor -Element $element) -Message 'Focused the selected element.'
        }
        'Invoke' {
            $pattern = Get-Pattern -Element $element -Pattern ([System.Windows.Automation.InvokePattern]::Pattern) -PatternName 'InvokePattern'
            $pattern.Invoke()
            Write-JsonResult -Ok $true -Operation $Action -Data (Get-ElementDescriptor -Element $element) -Message 'Invoked the selected element; verify the resulting application state.'
        }
        'SetValue' {
            if ($null -eq $Value) { throw 'SetValue requires -Value.' }
            $pattern = Get-Pattern -Element $element -Pattern ([System.Windows.Automation.ValuePattern]::Pattern) -PatternName 'ValuePattern'
            if ($pattern.Current.IsReadOnly) { throw 'The selected value element is read-only.' }
            $pattern.SetValue($Value)
            Write-JsonResult -Ok $true -Operation $Action -Data (Get-ElementDescriptor -Element $element) -Message 'Set the value; verify persistence in the application.'
        }
        'Toggle' {
            $pattern = Get-Pattern -Element $element -Pattern ([System.Windows.Automation.TogglePattern]::Pattern) -PatternName 'TogglePattern'
            $before = $pattern.Current.ToggleState.ToString()
            $pattern.Toggle()
            $afterPattern = Get-Pattern -Element $element -Pattern ([System.Windows.Automation.TogglePattern]::Pattern) -PatternName 'TogglePattern'
            $data = [ordered]@{ before = $before; after = $afterPattern.Current.ToggleState.ToString(); element = (Get-ElementDescriptor -Element $element) }
            Write-JsonResult -Ok $true -Operation $Action -Data $data -Message 'Toggled the selected element.'
        }
        'Select' {
            $pattern = Get-Pattern -Element $element -Pattern ([System.Windows.Automation.SelectionItemPattern]::Pattern) -PatternName 'SelectionItemPattern'
            $pattern.Select()
            Write-JsonResult -Ok $true -Operation $Action -Data (Get-ElementDescriptor -Element $element) -Message 'Selected the requested item.'
        }
        'Click' {
            Set-WindowForeground -Window $window
            $point = New-Object System.Windows.Point
            if (-not $element.TryGetClickablePoint([ref]$point)) {
                $bounds = $element.Current.BoundingRectangle
                if ($bounds.IsEmpty -or $bounds.Width -le 0 -or $bounds.Height -le 0) {
                    throw 'The selected element has no clickable point or usable bounds.'
                }
                $point = New-Object System.Windows.Point ($bounds.X + ($bounds.Width / 2)), ($bounds.Y + ($bounds.Height / 2))
            }
            $null = [WindowsAppAutomation.NativeMethods]::SetCursorPos([int][Math]::Round($point.X), [int][Math]::Round($point.Y))
            [WindowsAppAutomation.NativeMethods]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
            [WindowsAppAutomation.NativeMethods]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
            $data = [ordered]@{ x = $point.X; y = $point.Y; element = (Get-ElementDescriptor -Element $element) }
            Write-JsonResult -Ok $true -Operation $Action -Data $data -Message 'Clicked the selected element; verify the resulting application state.'
        }
        'SendKeys' {
            if ([string]::IsNullOrEmpty($Keys)) { throw 'SendKeys requires -Keys.' }
            Set-WindowForeground -Window $window
            $element.SetFocus()
            [System.Windows.Forms.SendKeys]::SendWait($Keys)
            Write-JsonResult -Ok $true -Operation $Action -Data (Get-ElementDescriptor -Element $element) -Message 'Sent keys to the selected element; read back the resulting state.'
        }
        'Screenshot' {
            $path = Save-ElementScreenshot -Element $element -Path $OutFile
            $data = [ordered]@{ path = $path; element = (Get-ElementDescriptor -Element $element) }
            Write-JsonResult -Ok $true -Operation $Action -Data $data -Message 'Captured a PNG screenshot.'
        }
        default {
            throw "Unsupported action '$Action'."
        }
    }
} catch {
    Write-JsonResult -Ok $false -Operation $Action -Data $null -Message $_.Exception.Message
    exit 1
}
