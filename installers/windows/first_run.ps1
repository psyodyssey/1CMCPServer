# ============================================================================
# first_run.ps1 - 1C Agent Platform first-run configurator
# Track Q / Step 4. Single user-facing surface after install per contract
# sec.8 / sec.9. Runs in Windows PowerShell 5.1+ (no PowerShell 7 required).
#
# Behaviour (locked by contract sec.8):
#   First run  - prompt for two paths (1cv8 executable + file-based 1C
#                infobase folder), validate, synthesise the input-config JSON,
#                call the existing fast-path helper through the bundled
#                python.exe, display + clipboard the Claude MCP snippet.
#   Later run  - display the existing config summary + the Claude MCP
#                snippet; offer Reconfigure.
#   Never      - spawn the MCP server, install autostart, install tray icon,
#                modify Claude's MCP config, modify PATH, modify production
#                code, write to anywhere other than %LOCALAPPDATA%\1C Agent
#                Platform\.
# ============================================================================

$ErrorActionPreference = 'Stop'

# --- Paths and constants -----------------------------------------------------

$InstallDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe  = Join-Path $InstallDir 'python\python.exe'
$StateDir   = Join-Path $env:LOCALAPPDATA '1C Agent Platform'
$ConfigPath = Join-Path $StateDir 'config.json'
$DumpsDir   = Join-Path $StateDir 'dumps'
$WorkDir    = Join-Path $StateDir '.runtime'
$ProductName = '1C Agent Platform'

Add-Type -AssemblyName System.Windows.Forms

# --- UI helpers --------------------------------------------------------------

function Show-Info {
    param([string]$Text, [string]$Title = $ProductName)
    [System.Windows.Forms.MessageBox]::Show(
        $Text, $Title,
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    ) | Out-Null
}

function Show-Error {
    param([string]$Text)
    [System.Windows.Forms.MessageBox]::Show(
        $Text, "$ProductName - Error",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    ) | Out-Null
}

function Build-McpSnippet {
    $jsonPython = $PythonExe.Replace('\', '\\')
    return @"
{
  "mcpServers": {
    "1c-agent-platform-read": {
      "command": "$jsonPython",
      "args": ["-m", "mcp_read_server"]
    }
  }
}
"@
}

function Show-McpSnippet {
    param([string]$Preamble)
    $snippet = Build-McpSnippet
    $clipboardOk = $true
    try { Set-Clipboard -Value $snippet -ErrorAction Stop } catch { $clipboardOk = $false }
    $clipNote = if ($clipboardOk) {
        'The snippet above has been copied to your clipboard.'
    } else {
        'Clipboard copy failed - copy the snippet above manually.'
    }
    Show-Info -Text @"
$Preamble

Paste this Claude MCP configuration snippet into your Claude client's MCP config:

$snippet

$clipNote

Claude will spawn the bundled python.exe as a stdio subprocess and route MCP read tools to your configured 1C infobase. The MCP server is not running right now - Claude starts it on its next session.
"@
}

# --- Pickers -----------------------------------------------------------------

function Pick-1CV8Executable {
    param([string]$Default = '')
    $dlg = New-Object System.Windows.Forms.OpenFileDialog
    $dlg.Title = 'Select 1cv8 executable'
    $dlg.Filter = '1cv8 binaries (1cv8.exe;1cestart.exe)|1cv8.exe;1cestart.exe|All files (*.*)|*.*'
    $dlg.CheckFileExists = $true
    $dlg.Multiselect = $false
    if ($Default -and (Test-Path -LiteralPath $Default)) {
        $dlg.InitialDirectory = Split-Path -Parent $Default
        $dlg.FileName = Split-Path -Leaf $Default
    }
    if ($dlg.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { return $null }
    return $dlg.FileName
}

function Pick-FileBasedInfobase {
    param([string]$Default = '')
    $dlg = New-Object System.Windows.Forms.FolderBrowserDialog
    $dlg.Description = 'Select file-based 1C infobase folder (must contain a .1cd file at top level). Server-based bases are not supported in this version.'
    $dlg.ShowNewFolderButton = $false
    if ($Default -and (Test-Path -LiteralPath $Default -PathType Container)) {
        $dlg.SelectedPath = $Default
    }
    if ($dlg.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { return $null }
    return $dlg.SelectedPath
}

function Test-IsFileBasedInfobase {
    param([string]$Folder)
    if (-not (Test-Path -LiteralPath $Folder -PathType Container)) { return $false }
    $found = Get-ChildItem -LiteralPath $Folder -Filter '*.1cd' -File -ErrorAction SilentlyContinue
    return ($null -ne $found -and @($found).Count -ge 1)
}

# --- Input-config synthesis (locked by contract sec.8.4) ---------------------

function Build-InputConfig {
    param([string]$OnecBinary, [string]$BasePath)
    return [ordered]@{
        product_name        = $ProductName
        profile_name        = 'default'
        default_environment = 'main'
        project = [ordered]@{
            environments = [ordered]@{
                main = [ordered]@{
                    name              = 'main'
                    base_id           = 'main'
                    base_path         = $BasePath
                    publication_name  = ''
                    http_base_url     = ''
                    dump_path         = $DumpsDir
                    timeout_seconds   = 600
                    allow_write       = $false
                    onec_binary_path  = $OnecBinary
                }
            }
        }
        servers   = [ordered]@{ read = $true; write = $false; intelligence = $false }
        bootstrap = [ordered]@{ work_dir = $WorkDir }
    }
}

# --- Fast-path invocation (locked by contract sec.8.5) ----------------------

function Invoke-FastPath {
    param([System.Collections.IDictionary]$InputObj)
    if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
        Show-Error "Bundled python.exe not found at:`n$PythonExe`n`nReinstall $ProductName."
        return $false
    }
    $tempDir = Join-Path $env:TEMP "$ProductName first run"
    if (-not (Test-Path -LiteralPath $tempDir)) {
        New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    }
    $tempInput = Join-Path $tempDir ("input-" + [Guid]::NewGuid().ToString() + ".json")
    try {
        if (-not (Test-Path -LiteralPath $StateDir)) {
            New-Item -ItemType Directory -Path $StateDir -Force | Out-Null
        }
        if (Test-Path -LiteralPath $ConfigPath) {
            Remove-Item -LiteralPath $ConfigPath -Force
        }
        # PowerShell 5.1 Set-Content -Encoding UTF8 emits a BOM, which Python
        # json.load rejects. Use .NET WriteAllText with explicit BOM-less UTF-8.
        [System.IO.File]::WriteAllText($tempInput, ($InputObj | ConvertTo-Json -Depth 8), [System.Text.UTF8Encoding]::new($false))
        $py = @"
from onec_platform.installer import run_install_fast_path_from_json_file
r = run_install_fast_path_from_json_file(r'''$tempInput''', output_config_path=r'''$ConfigPath''', confirm_write=True)
print('ok=' + str(r.ok))
print('mode=' + str(r.mode))
for f in (r.confirmed_findings or []):
    print('finding=' + getattr(f, 'severity', '?') + ':' + getattr(f, 'code', '?') + ':' + getattr(f, 'detail', '?'))
import sys
sys.exit(0 if r.ok else 3)
"@
        $output = & $PythonExe -c $py 2>&1
        $code = $LASTEXITCODE
        if ($code -ne 0) {
            $detail = ($output -join "`n")
            Show-Error "Fast-path helper returned non-zero (exit=$code).`n`n$detail"
            return $false
        }
        if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
            Show-Error "Fast-path returned ok but $ConfigPath was not created."
            return $false
        }
        return $true
    } finally {
        try { Remove-Item -LiteralPath $tempInput -Force -ErrorAction SilentlyContinue } catch {}
        try { Remove-Item -LiteralPath $tempDir -Force -ErrorAction SilentlyContinue } catch {}
    }
}

# --- Configuration flow ------------------------------------------------------

function Invoke-Configure {
    param([string]$DefaultOnec = '', [string]$DefaultBase = '')

    $onec = Pick-1CV8Executable -Default $DefaultOnec
    if (-not $onec) { Show-Error '1cv8 executable selection cancelled. No changes made.'; return $false }
    if (-not (Test-Path -LiteralPath $onec -PathType Leaf)) {
        Show-Error "Selected 1cv8 path does not exist:`n$onec"
        return $false
    }

    $base = Pick-FileBasedInfobase -Default $DefaultBase
    if (-not $base) { Show-Error 'Infobase folder selection cancelled. No changes made.'; return $false }
    if (-not (Test-Path -LiteralPath $base -PathType Container)) {
        Show-Error "Selected infobase folder does not exist:`n$base"
        return $false
    }

    if (-not (Test-IsFileBasedInfobase $base)) {
        Show-Error @"
The selected folder is not a file-based 1C infobase (no .1cd file found at its top level).

Server-based / client-server 1C infobases are not supported in this version of $ProductName.

See the operator recipe at docs/operators/installer/windows-setup-exe.md for the existing engineering path (scripts/release/install.ps1 + hand-authored input JSON) for server-based bases.

Selected folder:
$base
"@
        return $false
    }

    $inputObj = Build-InputConfig -OnecBinary $onec -BasePath $base
    if (-not (Invoke-FastPath -InputObj $inputObj)) { return $false }

    Show-McpSnippet -Preamble "Configuration saved to:`n$ConfigPath`n`n  1cv8 executable: $onec`n  Infobase folder: $base"
    return $true
}

function Invoke-SubsequentLaunch {
    try {
        $existing = Get-Content -LiteralPath $ConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $envMain = $existing.project.environments.main
        $existingOnec = $envMain.onec_binary_path
        $existingBase = $envMain.base_path
    } catch {
        Show-Error "Failed to read existing config at:`n$ConfigPath`n`n$($_.Exception.Message)`n`nDelete the file manually to start over."
        return
    }

    $summary = @"
Existing $ProductName configuration:
  1cv8 executable : $existingOnec
  Infobase folder : $existingBase
  Config file     : $ConfigPath
"@

    $choice = [System.Windows.Forms.MessageBox]::Show(
        "$summary`n`nClick OK to view the Claude MCP snippet (also copied to clipboard).`nClick Cancel to reconfigure with new paths.",
        "$ProductName - Existing configuration",
        [System.Windows.Forms.MessageBoxButtons]::OKCancel,
        [System.Windows.Forms.MessageBoxIcon]::Information
    )

    if ($choice -eq [System.Windows.Forms.DialogResult]::Cancel) {
        Invoke-Configure -DefaultOnec $existingOnec -DefaultBase $existingBase | Out-Null
    } else {
        Show-McpSnippet -Preamble $summary
    }
}

# --- Entry point -------------------------------------------------------------

if (Test-Path -LiteralPath $ConfigPath -PathType Leaf) {
    Invoke-SubsequentLaunch
} else {
    Show-Info -Text @"
Welcome to $ProductName.

This is a one-time setup. You will be asked to:
  1. Select your 1cv8 executable (1cv8.exe or 1cestart.exe).
  2. Select your file-based 1C infobase folder (must contain a .1cd file).

Server-based / client-server 1C bases are not supported in this version - see the operator recipe for the existing engineering path.
"@ -Title "$ProductName - First-run configuration"
    Invoke-Configure | Out-Null
}
