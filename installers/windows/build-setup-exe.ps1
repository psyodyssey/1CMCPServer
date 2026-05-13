# ============================================================================
# build-setup-exe.ps1 - Build helper for the 1C Agent Platform Windows
# installer (Track Q / Step 4).
#
# Locked by contract sec.12.2 file 4. Fetches the python.org embeddable
# CPython 3.11 distribution at build time, prepares the build directory the
# Inno Setup compiler consumes, rewrites python311._pth per contract sec.6.3,
# and invokes iscc.exe against installers\windows\setup.iss.
#
# CRITICAL: the embeddable CPython zip is fetched fresh at build time. It is
# NOT committed to the repository (forbidden by contract sec.3.9, sec.4.4,
# and step-map invariant sec.1.30). The build/ and dist/ directories are
# already in .gitignore (lines 13-14).
#
# Usage:
#   pwsh installers\windows\build-setup-exe.ps1
#   pwsh installers\windows\build-setup-exe.ps1 -PythonEmbedVersion 3.11.9
#   pwsh installers\windows\build-setup-exe.ps1 -IsccPath 'C:\Tools\InnoSetup6\ISCC.exe'
#   pwsh installers\windows\build-setup-exe.ps1 -SkipFetch  # reuse build/python
# ============================================================================

[CmdletBinding()]
param(
    [string] $PythonEmbedVersion = '3.11.9',
    [string] $PythonEmbedUrl     = '',
    [string] $IsccPath           = '',
    [string] $OutputDir          = '',
    [switch] $SkipFetch
)

$ErrorActionPreference = 'Stop'

$Root          = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$BuildRoot     = Join-Path $Root 'build'
$BuildPython   = Join-Path $BuildRoot 'python'
$BuildPkgs     = Join-Path $BuildRoot 'packages'
$BuildLauncher = Join-Path $BuildRoot 'first_run.ps1'
$IssFile       = Join-Path $PSScriptRoot 'setup.iss'
$LauncherSrc   = Join-Path $PSScriptRoot 'first_run.ps1'
if (-not $OutputDir) { $OutputDir = Join-Path $Root 'dist\installer' }

# Mirror of pyproject.toml [tool.hatch.build.targets.wheel] packages array
# (lines 51-63). Source paths are repo-relative; Module names are the
# importable package names locked by contract sec.6.1 / sec.6.3.
$Packages = @(
    @{ Module = 'mcp_read_server';         Source = 'apps\mcp-read-server\src\mcp_read_server' },
    @{ Module = 'mcp_write_server';        Source = 'apps\mcp-write-server\src\mcp_write_server' },
    @{ Module = 'mcp_intelligence_server'; Source = 'apps\mcp-intelligence-server\src\mcp_intelligence_server' },
    @{ Module = 'onec_platform';           Source = 'apps\platform\src\onec_platform' },
    @{ Module = 'mcp_common';              Source = 'packages\mcp-common\src\mcp_common' },
    @{ Module = 'onec_process_runner';     Source = 'packages\onec-process-runner\src\onec_process_runner' },
    @{ Module = 'onec_policy_engine';      Source = 'packages\onec-policy-engine\src\onec_policy_engine' },
    @{ Module = 'onec_audit';              Source = 'packages\onec-audit\src\onec_audit' },
    @{ Module = 'onec_health';             Source = 'packages\onec-health\src\onec_health' },
    @{ Module = 'onec_troubleshooting';    Source = 'packages\onec-troubleshooting\src\onec_troubleshooting' },
    @{ Module = 'onec_config';             Source = 'packages\onec-config\src\onec_config' }
)

# --- Helpers -----------------------------------------------------------------

function Resolve-Iscc {
    if ($IsccPath -and (Test-Path -LiteralPath $IsccPath -PathType Leaf)) { return $IsccPath }
    $candidates = @(
        "$env:ProgramFiles\Inno Setup 6\ISCC.exe",
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles\Inno Setup 5\ISCC.exe",
        "${env:ProgramFiles(x86)}\Inno Setup 5\ISCC.exe"
    )
    foreach ($c in $candidates) {
        if ($c -and (Test-Path -LiteralPath $c -PathType Leaf)) { return $c }
    }
    $iscc = Get-Command iscc.exe -ErrorAction SilentlyContinue
    if ($iscc) { return $iscc.Source }
    throw 'iscc.exe not found. Install Inno Setup 6 from https://jrsoftware.org/isdl.php or pass -IsccPath <full path>.'
}

function Reset-Directory {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) { Remove-Item -LiteralPath $Path -Recurse -Force }
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
}

function Fetch-Embeddable {
    param([string]$Version, [string]$Url, [string]$Destination)
    Reset-Directory -Path $Destination
    if (-not $Url) {
        $Url = "https://www.python.org/ftp/python/$Version/python-$Version-embed-amd64.zip"
    }
    $zipPath = Join-Path $BuildRoot ("python-$Version-embed-amd64.zip")
    if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
    Write-Host "Fetching embeddable CPython from: $Url"
    $oldPP = $ProgressPreference
    $ProgressPreference = 'SilentlyContinue'
    try { Invoke-WebRequest -Uri $Url -OutFile $zipPath } finally { $ProgressPreference = $oldPP }
    Write-Host "Extracting to: $Destination"
    Expand-Archive -LiteralPath $zipPath -DestinationPath $Destination -Force
    Remove-Item -LiteralPath $zipPath -Force
}

function Edit-PathConfig {
    param([string]$EmbeddableDir)
    # Rewrite python*._pth so the eleven src-layout package directories
    # (extracted one level UP from python/) are importable. Layout locked
    # by contract sec.6.3.
    $pth = Get-ChildItem -LiteralPath $EmbeddableDir -Filter 'python*._pth' -File | Select-Object -First 1
    if (-not $pth) { throw "Could not locate python*._pth under $EmbeddableDir." }
    $stdlibZip = ($pth.Name -replace '\._pth$', '.zip')
    $lines = @(
        $stdlibZip,
        '.',
        '..',
        '..\mcp_read_server',
        '..\mcp_write_server',
        '..\mcp_intelligence_server',
        '..\onec_platform',
        '..\mcp_common',
        '..\onec_process_runner',
        '..\onec_policy_engine',
        '..\onec_audit',
        '..\onec_health',
        '..\onec_troubleshooting',
        '..\onec_config',
        '',
        '# Uncomment to run site.main() automatically',
        '#import site'
    )
    Set-Content -LiteralPath $pth.FullName -Value $lines -Encoding ASCII
    Write-Host "Rewrote $($pth.Name) with eleven src-layout package entries."
}

function Copy-Packages {
    Reset-Directory -Path $BuildPkgs
    foreach ($p in $Packages) {
        $src = Join-Path $Root $p.Source
        $dst = Join-Path $BuildPkgs $p.Module
        if (-not (Test-Path -LiteralPath $src -PathType Container)) {
            throw "Source package directory missing: $src"
        }
        Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
        # Strip cached bytecode to keep the installed payload clean
        # (matches the no-binary spirit of contract sec.3.9).
        Get-ChildItem -LiteralPath $dst -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Get-ChildItem -LiteralPath $dst -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Extension -in '.pyc','.pyo' } | Remove-Item -Force -ErrorAction SilentlyContinue
    }
    Write-Host "Copied $($Packages.Count) src-layout packages into: $BuildPkgs"
}

function Copy-Launcher {
    if (-not (Test-Path -LiteralPath $LauncherSrc -PathType Leaf)) {
        throw "first_run.ps1 missing at: $LauncherSrc"
    }
    Copy-Item -LiteralPath $LauncherSrc -Destination $BuildLauncher -Force
    Write-Host 'Copied first_run.ps1 into build root.'
}

function Invoke-Iscc {
    param([string]$Iscc)
    if (-not (Test-Path -LiteralPath $OutputDir)) {
        New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    }
    Write-Host "Invoking $Iscc against $IssFile"
    Write-Host "  Output directory: $OutputDir"
    & $Iscc "/O$OutputDir" $IssFile
    if ($LASTEXITCODE -ne 0) { throw "iscc.exe exited with code $LASTEXITCODE." }
}

# --- Main --------------------------------------------------------------------

Write-Host '1C Agent Platform - build setup.exe'
Write-Host "  project root      : $Root"
Write-Host "  build root        : $BuildRoot"
Write-Host "  python embed pin  : $PythonEmbedVersion"
Write-Host "  output directory  : $OutputDir"
Write-Host ''

if (-not (Test-Path -LiteralPath $BuildRoot)) {
    New-Item -ItemType Directory -Path $BuildRoot -Force | Out-Null
}

$Iscc = Resolve-Iscc
Write-Host "Found iscc.exe at: $Iscc"

if ($SkipFetch -and (Test-Path -LiteralPath (Join-Path $BuildPython 'python.exe'))) {
    Write-Host 'Skipping embeddable fetch (-SkipFetch and existing build/python preserved).'
} else {
    Fetch-Embeddable -Version $PythonEmbedVersion -Url $PythonEmbedUrl -Destination $BuildPython
}

Edit-PathConfig -EmbeddableDir $BuildPython
Copy-Packages
Copy-Launcher
Invoke-Iscc -Iscc $Iscc

Write-Host ''
Write-Host "Build complete. setup.exe is under: $OutputDir"
Write-Host ''
Write-Host 'Reminder: build/ and dist/ are gitignored. Do not commit the'
Write-Host 'embeddable CPython zip, the build directory, or setup.exe.'
