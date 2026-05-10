# launch.ps1
# Operator / dev umbrella entry point for typical local actions on
# the 1C Agent Platform monorepo.
#
# Track B / Step 4 — this is a *thin scripts-only* wrapper around
# already-existing helpers (`scripts/dev/bootstrap_paths.ps1` and
# `scripts/dev/run_dev_check.ps1`). It removes the manual PYTHONPATH
# ritual for the common local actions and gives one discoverable
# command surface. No production code is touched.
#
# What this wrapper deliberately does NOT do:
#   - it does NOT start MCP read / write / intelligence servers.
#     Each server is launched separately via `python -m <pkg>`
#     (also declared as [project.scripts] console entries).
#     Two transports are supported on each server:
#       * --transport stdio (default; Track G / Step 4) - local
#         JSON-RPC 2.0 over stdin/stdout; trusted local
#         subprocess only; no auth (the channel is not network-
#         exposed);
#       * --transport http (Track H / Step 4) - HTTP/1.1 /mcp
#         endpoint with static bearer authentication; requires
#         --bind <HOST>:<PORT> and --auth-token-env <VARNAME>
#         (or auth.tokens in product config); trusted-network
#         deployment behind operator's reverse proxy; in-
#         process TLS is not provided.
#     Launching the servers from this wrapper is a deliberate
#     scope choice that this umbrella does NOT take;
#   - it does NOT run pytest (there is no test suite yet);
#   - it does NOT run the install fast path
#     (use scripts\release\install.ps1 for that);
#   - it does NOT touch a 1C infobase.

param(
    [Parameter(Position = 0)]
    [string] $Command = '',

    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]] $Rest = @()
)

$ErrorActionPreference = "Stop"

$root        = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$bootstrap   = Join-Path $PSScriptRoot "bootstrap_paths.ps1"
$runDevCheck = Join-Path $PSScriptRoot "run_dev_check.ps1"


function Show-Usage {
    $text = @'
1C Agent Platform - local launch wrapper

Usage:

  scripts\dev\launch.ps1 selfcheck
      Run the skeleton self-check (imports, registries, health
      summary). Equivalent to scripts\dev\run_dev_check.ps1.

  scripts\dev\launch.ps1 repl
      Start an interactive Python REPL with the monorepo
      PYTHONPATH already set. Useful for ad-hoc exploration of
      mcp_read_server / mcp_write_server / onec_platform.

  scripts\dev\launch.ps1 run <script.py> [args...]
      Run an arbitrary Python script under the monorepo
      PYTHONPATH. The script path can be absolute or relative to
      the current working directory. Remaining arguments are
      forwarded to Python.

  scripts\dev\launch.ps1 help
      Print this usage message.

What this wrapper deliberately does NOT do:

  - It does NOT start the MCP read / write / intelligence servers.
    Launch them separately, e.g.:
        python -m mcp_read_server --help
        python -m mcp_write_server --help
        python -m mcp_intelligence_server --help
    Each accepts --transport stdio (default; Track G / Step 4
    local subprocess use, no auth) or --transport http
    (Track H / Step 4 HTTP/1.1 /mcp endpoint with static
    bearer authentication; requires --bind HOST:PORT and
    a token source via --auth-token-env VARNAME or
    auth.tokens in product config; trusted-network
    deployment, no in-process TLS).
  - It does NOT run pytest (no test suite yet).
  - It does NOT run the install fast path. Use
    scripts\release\install.ps1 for that (Track B / Step 3).
  - It does NOT touch a 1C infobase. It is a local-dev helper.
'@
    Write-Host $text
    Write-Host
    Write-Host "Project root: $root"
}


# Sanity: bootstrap script must exist (it is a hard dependency of
# repl / run, and a soft dependency of selfcheck via run_dev_check).
if (-not (Test-Path $bootstrap)) {
    Write-Error "Missing bootstrap script: $bootstrap"
    exit 1
}

switch -Regex ($Command) {
    '^(|help|-help|--help|-\?)$' {
        Show-Usage
        exit 0
    }

    '^selfcheck$' {
        if (-not (Test-Path $runDevCheck)) {
            Write-Error "Missing run_dev_check.ps1 at $runDevCheck"
            exit 1
        }
        & $runDevCheck
        exit $LASTEXITCODE
    }

    '^repl$' {
        Write-Host "Starting Python REPL with monorepo PYTHONPATH..."
        Write-Host "  Press Ctrl-Z then Enter (Windows) to exit."
        Write-Host
        . $bootstrap
        python
        exit $LASTEXITCODE
    }

    '^run$' {
        if ($Rest.Count -lt 1) {
            # Use Console.Error directly: Write-Error combined with
            # $ErrorActionPreference = "Stop" would short-circuit the
            # script before `exit 64` runs.
            [Console]::Error.WriteLine("Usage: launch.ps1 run <script.py> [args...]")
            exit 64
        }
        . $bootstrap
        python @Rest
        exit $LASTEXITCODE
    }

    default {
        [Console]::Error.WriteLine("Unknown command: '$Command'")
        Show-Usage
        exit 64
    }
}
