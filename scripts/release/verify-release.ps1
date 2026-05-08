# verify-release.ps1
# Pre-handoff release sanity check for 1C Agent Platform.
#
# Track C / Step 2. Release-facing only: this script verifies that
# the repository looks ready to be handed off to another operator.
# It does NOT exercise production code, does NOT start MCP servers,
# does NOT touch a 1C infobase, does NOT publish anything.
#
# Checks (all read-only):
#   1. Required root files present (LICENSE, CHANGELOG, SECURITY,
#      README, PROJECT-STATUS, pyproject.toml, .gitignore).
#   2. Release entrypoints present (install.ps1 + helper + README,
#      scripts/dev launch / bootstrap / run_dev_check / selfcheck).
#   3. Important docs present (operator / admin / developer manuals,
#      runbooks index + Track A round-trip runbook, architecture
#      plans + step maps for Track A / B / C).
#   4. Working tree clean (unless -AllowDirtyTree).
#   5. Git baseline OK (branch == main, history non-empty).
#   6. Selfcheck green (imports_ok = true; registry counts
#      read=15 / write=25 / intelligence=16; selfcheck_status = ok).
#      Skipped with -SkipSelfcheck.
#   7. Credential leak guard (no PRIVATE KEY / AWS secret access
#      key markers in tracked files).
#   8. Credential template hygiene (Track D / Step 5). Narrow
#      heuristic over tracked *.config.json files: scans for argv
#      elements immediately following /P or /Pwd in 1C command
#      templates. The documented safe forms are the env-substitution
#      token ${ENV:NAME} (Track D / Step 3) and the abstract
#      <password> placeholder. Literal cleartext values trigger
#      WARN (not FAIL) so legacy templates do not block the
#      receive-side verify flow.
#
# Exit codes:
#   0  — all checks PASS / SKIP / WARN (WARN does not block)
#   2  — one or more release-facing assertions FAILED
#   64 — wrapper invoked with bad arguments (PS native handling)

param(
    [switch] $AllowDirtyTree,
    [switch] $SkipSelfcheck
)

$ErrorActionPreference = "Stop"

$root      = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$bootstrap = Join-Path $root "scripts\dev\bootstrap_paths.ps1"
$selfcheck = Join-Path $root "scripts\dev\selfcheck.py"

$checks = New-Object System.Collections.Generic.List[object]
$script:failed = 0

function Add-Check {
    param(
        [string] $Name,
        [string] $Status,
        [string] $Detail = ""
    )
    $checks.Add([pscustomobject]@{
        Name = $Name; Status = $Status; Detail = $Detail
    })
    if ($Status -eq "FAIL") { $script:failed++ }
}

function Test-FilesPresent {
    param(
        [string]   $Name,
        [string[]] $Paths
    )
    $missing = New-Object System.Collections.Generic.List[string]
    foreach ($p in $Paths) {
        $full = Join-Path $root $p
        if (-not (Test-Path -LiteralPath $full)) { $missing.Add($p) }
    }
    if ($missing.Count -eq 0) {
        Add-Check $Name "PASS" "$($Paths.Count) file(s) present"
    } else {
        Add-Check $Name "FAIL" "missing: $($missing -join ', ')"
    }
}


Write-Host "1C Agent Platform - release verify"
Write-Host "  project root      : $root"
Write-Host "  allow dirty tree  : $($AllowDirtyTree.IsPresent)"
Write-Host "  skip selfcheck    : $($SkipSelfcheck.IsPresent)"
Write-Host


# 1. Required root files
Test-FilesPresent "Repo layout (root files)" @(
    "LICENSE",
    "CHANGELOG.md",
    "SECURITY.md",
    "README.md",
    "PROJECT-STATUS.md",
    "pyproject.toml",
    ".gitignore"
)


# 2. Release entrypoints
Test-FilesPresent "Release entrypoints" @(
    "scripts/release/install.ps1",
    "scripts/release/_install_runner.py",
    "scripts/release/README.md",
    "scripts/dev/launch.ps1",
    "scripts/dev/bootstrap_paths.ps1",
    "scripts/dev/run_dev_check.ps1",
    "scripts/dev/selfcheck.py"
)


# 3. Important docs
Test-FilesPresent "Important docs" @(
    "docs/operator-manual.md",
    "docs/administrator-manual.md",
    "docs/developer-manual.md",
    "docs/runbooks.md",
    "docs/runbooks/track-a-reference-stand-round-trip.md",
    "docs/architecture/track-a-real-write-path-plan.md",
    "docs/architecture/track-a-real-write-path-step-map.md",
    "docs/architecture/track-b-productization-polish-plan.md",
    "docs/architecture/track-b-productization-polish-step-map.md",
    "docs/architecture/track-c-packaging-installer-delivery-plan.md",
    "docs/architecture/track-c-packaging-installer-delivery-step-map.md"
)


# 4. Working tree
Push-Location $root
try {
    $porcelain = git status --porcelain
    if ($null -eq $porcelain -or @($porcelain).Count -eq 0) {
        Add-Check "Working tree" "PASS" "clean"
    } else {
        $count = @($porcelain).Count
        if ($AllowDirtyTree.IsPresent) {
            Add-Check "Working tree" "PASS" "$count uncommitted change(s) - accepted (-AllowDirtyTree)"
        } else {
            Add-Check "Working tree" "FAIL" "$count uncommitted change(s); use -AllowDirtyTree to bypass"
        }
    }
} finally { Pop-Location }


# 5. Git baseline
Push-Location $root
try {
    $branchRaw = git branch --show-current
    $branch = if ($branchRaw) { ($branchRaw | Out-String).Trim() } else { "" }
    $log = git log --oneline
    $logCount = if ($null -eq $log) { 0 } else { @($log).Count }
    if ($branch -eq "main" -and $logCount -ge 1) {
        Add-Check "Git baseline" "PASS" "branch=$branch, $logCount commit(s)"
    } else {
        Add-Check "Git baseline" "FAIL" "branch='$branch', $logCount commit(s) (expected branch=main, >=1 commit)"
    }
} finally { Pop-Location }


# 6. Selfcheck
if ($SkipSelfcheck.IsPresent) {
    Add-Check "Selfcheck" "SKIP" "skipped via -SkipSelfcheck"
} else {
    Push-Location $root
    try {
        . $bootstrap | Out-Null
        $output = python $selfcheck | Out-String
        $exit = $LASTEXITCODE

        $importsOk = $output -match "imports_ok = true"
        $statusOk  = $output -match "selfcheck_status = ok"

        $rRead  = if ($output -match "read_server_tools = \[(.+?)\]")         { ($matches[1] -split ',').Count } else { 0 }
        $rWrite = if ($output -match "write_server_tools = \[(.+?)\]")        { ($matches[1] -split ',').Count } else { 0 }
        $rIntel = if ($output -match "intelligence_server_tools = \[(.+?)\]") { ($matches[1] -split ',').Count } else { 0 }

        if ($exit -eq 0 -and $importsOk -and $statusOk -and $rRead -eq 15 -and $rWrite -eq 25 -and $rIntel -eq 16) {
            Add-Check "Selfcheck" "PASS" "registries read=$rRead / write=$rWrite / intelligence=$rIntel; status=ok"
        } else {
            Add-Check "Selfcheck" "FAIL" "exit=$exit imports_ok=$importsOk status_ok=$statusOk read=$rRead write=$rWrite intel=$rIntel"
        }
    } finally { Pop-Location }
}


# 7. Credential leak guard
# Exclude self-references: this script and its README necessarily
# contain the literal pattern names (in the $patterns array and in
# documentation listing what is checked). Excluding them avoids
# false positives without weakening coverage of the real risk
# (someone committing an actual key file or AWS credential).
Push-Location $root
try {
    $patterns = @(
        "BEGIN PRIVATE KEY",
        "BEGIN RSA PRIVATE KEY",
        "BEGIN OPENSSH PRIVATE KEY",
        "aws_secret_access_key"
    )
    $excludes = @(
        ":!scripts/release/verify-release.ps1",
        ":!scripts/release/README.md"
    )
    $hits = New-Object System.Collections.Generic.List[string]
    foreach ($pat in $patterns) {
        $found = git grep -l --no-color "$pat" -- @excludes
        if ($found) {
            $hits.Add("$pat -> $(@($found) -join ', ')")
        }
    }
    if ($hits.Count -eq 0) {
        Add-Check "Credential leak guard" "PASS" "no obvious markers found in tracked files (excluding self-references)"
    } else {
        Add-Check "Credential leak guard" "FAIL" ($hits -join '; ')
    }
} finally { Pop-Location }


# 8. Credential template hygiene (Track D / Step 5)
# Narrow heuristic over tracked *.config.json files. Looks for argv
# elements immediately following the 1C "/P" or "/Pwd" flag inside
# command-template arrays. The two documented safe forms are the
# env-substitution token "${ENV:NAME}" (resolved at render time by
# the write server, see Track D / Step 3) and the abstract
# placeholder "<password>". Literal cleartext values trigger WARN
# with the file:line offender, not FAIL — by design, so legacy
# templates do not block the receive-side flow. The check is
# deliberately scoped: only tracked *.config.json files, only the
# /P and /Pwd adjacency, no scanning of runbooks or other docs.
Push-Location $root
try {
    $configFilesRaw = git ls-files -- '*.config.json'
    if ($null -eq $configFilesRaw) { $configFilesRaw = @() }
    $configFiles = @($configFilesRaw)

    $warns   = New-Object System.Collections.Generic.List[string]
    $scanned = 0

    $pattern        = '(?i)"/P(?:wd)?"\s*,\s*"([^"]*)"'
    $envFormPattern = '^\$\{ENV:[A-Z_][A-Z0-9_]*\}$'

    foreach ($f in $configFiles) {
        $full = Join-Path $root $f
        if (-not (Test-Path -LiteralPath $full)) { continue }
        $scanned++
        $text = Get-Content -LiteralPath $full -Raw -Encoding UTF8
        if ([string]::IsNullOrEmpty($text)) { continue }

        $found = [regex]::Matches($text, $pattern)
        foreach ($m in $found) {
            $value = $m.Groups[1].Value
            if ($value -match $envFormPattern)  { continue }
            if ($value -eq '<password>')        { continue }
            if ([string]::IsNullOrEmpty($value)) { continue }

            $prefix = $text.Substring(0, $m.Index)
            $line   = ([regex]::Matches($prefix, "`n")).Count + 1
            $warns.Add(('{0}:{1} - literal /P value; expected ${{ENV:NAME}} or <password>' -f $f, $line))
        }
    }

    if ($warns.Count -eq 0) {
        Add-Check "Credential template hygiene" "PASS" "scanned $scanned tracked *.config.json file(s); no literal /P values"
    } else {
        Add-Check "Credential template hygiene" "WARN" ($warns -join '; ')
    }
} finally { Pop-Location }


# Summary
Write-Host
Write-Host "Summary:"
foreach ($c in $checks) {
    $marker = switch ($c.Status) {
        "PASS" { "[PASS]" }
        "FAIL" { "[FAIL]" }
        "SKIP" { "[SKIP]" }
        "WARN" { "[WARN]" }
        default { "[?]" }
    }
    Write-Host ("  {0} {1} - {2}" -f $marker, $c.Name, $c.Detail)
}

Write-Host
if ($script:failed -eq 0) {
    Write-Host "Release verify: GREEN (all checks passed or skipped)"
    exit 0
} else {
    Write-Host "Release verify: RED ($($script:failed) check(s) failed)"
    exit 2
}
