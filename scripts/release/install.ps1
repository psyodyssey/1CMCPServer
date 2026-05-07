# install.ps1
# Operator-facing wrapper around the install fast path
# (`onec_platform.run_install_fast_path_from_json_file`, defined in
# `apps/platform/src/onec_platform/installer.py`).
#
# Track B / Step 3 — this is a *thin scripts-only* wrapper. It
# bootstraps PYTHONPATH for the monorepo and forwards the call to the
# existing Phase 6 / Step 3 install fast path through a small Python
# helper (`_install_runner.py`). It does NOT introduce a new install
# ecosystem. No `.msi`, no `.deb`, no GUI wizard, no signed
# distribution.
#
# Default invocation runs in preview mode and writes nothing to disk.
# Pass -Confirm to actually materialise the JSON product config.

param(
    [Parameter(Mandatory = $true,
               HelpMessage = "Path to the input product config JSON.")]
    [string] $ConfigPath,

    [Parameter(Mandatory = $true,
               HelpMessage = "Where the materialised product config JSON should be written.")]
    [string] $OutputConfigPath,

    [switch] $Confirm
)

$ErrorActionPreference = "Stop"

$root      = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$bootstrap = Join-Path $root "scripts\dev\bootstrap_paths.ps1"
$runner    = Join-Path $PSScriptRoot "_install_runner.py"

Write-Host "1C Agent Platform - install fast path wrapper"
Write-Host "  project root      : $root"
Write-Host "  input config      : $ConfigPath"
Write-Host "  output config     : $OutputConfigPath"
if ($Confirm.IsPresent) {
    Write-Host "  mode              : EXECUTE (will write the JSON)"
} else {
    Write-Host "  mode              : PREVIEW (no file will be written)"
}
Write-Host

# Bootstrap PYTHONPATH for this PowerShell session.
. $bootstrap

# Translate the switch into a plain string the Python runner consumes.
$confirmFlag = if ($Confirm.IsPresent) { "true" } else { "false" }

python $runner $ConfigPath $OutputConfigPath $confirmFlag
$exitCode = $LASTEXITCODE

Write-Host
switch ($exitCode) {
    0 {
        if ($Confirm.IsPresent) {
            Write-Host "Install fast path completed: mode=executed."
            Write-Host "Inspect the result at: $OutputConfigPath"
        } else {
            Write-Host "Preview completed: mode=preview."
            Write-Host "No file was written. Re-run with -Confirm to actually write the config."
        }
    }
    2 {
        Write-Host "Install fast path REJECTED. Inspect findings above."
    }
    default {
        Write-Host "Install fast path FAILED with exit code $exitCode."
    }
}

exit $exitCode
