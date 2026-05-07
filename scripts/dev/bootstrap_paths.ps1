# bootstrap_paths.ps1
# Sets PYTHONPATH for the 1C Agent Platform monorepo in the current session only.
# Does not touch the system PATH or the registry.

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

$srcPaths = @(
    "apps\mcp-read-server\src",
    "apps\mcp-write-server\src",
    "apps\mcp-intelligence-server\src",
    "apps\platform\src",
    "packages\mcp-common\src",
    "packages\onec-process-runner\src",
    "packages\onec-policy-engine\src",
    "packages\onec-audit\src",
    "packages\onec-health\src",
    "packages\onec-troubleshooting\src",
    "packages\onec-config\src"
)

$absolute = $srcPaths | ForEach-Object { Join-Path $root $_ }
$env:PYTHONPATH = ($absolute -join ";")

Write-Host "PYTHONPATH set for this PowerShell session."
Write-Host "Project root: $root"
Write-Host "Included src paths:"
foreach ($path in $absolute) {
    Write-Host "  - $path"
}
