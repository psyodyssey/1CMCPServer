# Release Handoff — 1C Agent Platform

This document is the **canonical entry point for someone receiving
the project**. If you have just been given a clone of this
repository (or a snapshot tarball) and you need to verify what
you got, install it locally, and pass it on cleanly, read this
end to end.

It is intentionally separate from `README.md` (which introduces
the project) and from `scripts/release/README.md` (which
documents individual release-facing wrappers). This file collects
the **handoff sequence** in one place.


## Audience

You are reading this if you are a receive-side **operator** or
**developer**:

- Operator — you want to bring the platform up locally, verify
  it, and possibly materialise a product config without altering
  any source code.
- Developer — you also want a reproducible local environment for
  exploring or extending the platform.

You are **not** the target audience if you are looking for a
production deployment guide, a GUI installer, or instructions for
publishing to a package manager. Those are out of scope (see
"What is NOT in this handoff" below).


## What is already closed in the project

At the time of this handoff:

- **Phases 1–6** (read MVP, write MVP, metadata changes,
  intelligence layer, product layer, industrialization &
  completion track) — closed. Three MCP servers are present
  with stable public registries: `mcp-read-server` (15 tools),
  `mcp-write-server` (25 tools),
  `mcp-intelligence-server` (16 tools). See `PROJECT-STATUS.md`
  for per-phase detail.
- **Parallel Track A — Full Real 1cv8-backed Write Path** —
  closed on Step 7. A real binary-backed
  `DumpConfigToFiles` → `LoadConfigFromFiles` → `UpdateDBCfg`
  round-trip has been exercised on a reference stand. See
  `docs/runbooks/track-a-reference-stand-round-trip.md`.
- **Parallel Track B — Productization & Delivery Polish** —
  closed on Step 6. Repository hygiene baseline, install fast
  path wrapper, local launch umbrella, root README quickstart.
- **Parallel Track C — Packaging & Installer Delivery** —
  in progress. The release-facing verify path
  (`scripts/release/verify-release.ps1`) and the packaging-facing
  honest review (`pyproject.toml` + `scripts/release/README.md`)
  are already in. This handoff document is the Track C / Step 4
  deliverable.


## What is in this handoff

The operator-facing surface you are receiving:

- A scripts-based **install path** (`scripts/release/install.ps1`).
- A scripts-based **release verify path**
  (`scripts/release/verify-release.ps1`) covering seven
  release-facing invariants.
- A **local dev launch umbrella** (`scripts/dev/launch.ps1`)
  with `selfcheck`, `repl`, `run` subcommands.
- A documented **PYTHONPATH bootstrap**
  (`scripts/dev/bootstrap_paths.ps1`) that the rest of the
  scripts dot-source.
- A **selfcheck tool** (`scripts/dev/selfcheck.py`) that imports
  every internal package and prints registry counts plus a
  health summary.
- One **reference-stand runbook** for the real binary-backed
  write round-trip
  (`docs/runbooks/track-a-reference-stand-round-trip.md`).
- **Per-track planning documents** under `docs/architecture/`
  for Track A, Track B, Track C.
- **Standalone manuals** under `docs/`:
  `operator-manual.md`, `administrator-manual.md`,
  `developer-manual.md`, `runbooks.md`.
- **Legal / security baseline**: `LICENSE` (Apache-2.0),
  `CHANGELOG.md`, `SECURITY.md`.


## What is NOT in this handoff

These are **honest constraints**. They are not hidden gaps —
they are intentional limits of the current scaffolding.

- **No wheel-based install.** `pyproject.toml` declares
  `[tool.hatch.build.targets.wheel] packages = []` deliberately.
  The build toolchain (`build` / `hatch` / `hatchling`) is not
  part of the documented dev prerequisites; `python -m build`
  produces no usable artifact. See the comment in
  `pyproject.toml` and the "Packaging-facing install flow"
  section of `scripts/release/README.md`.
- **No GUI installer / `.msi` / `.deb` / signed binary
  distribution.**
- **No publication to package managers** (PyPI / Chocolatey /
  winget / apt).
- **No production-grade MCP transport.** No authentication,
  authorisation, multi-tenant isolation, or hardened network
  transport. The three MCP servers are intended for local /
  controlled use, not as exposed network endpoints.
- **No web UI / dashboard frontend.**
- **No enterprise super-set** (SSO/RBAC, multi-tenant, secrets
  vault as a service, federated audit storage, policy-as-code
  DSL, multi-instance HA).
- **No hot reload or OS-level service supervision** (Windows
  Service / systemd unit registration, automatic restart
  supervisor).
- **No multi-version 1С smoke matrix.** Real-stand evidence
  exists for `8.3.27.1859`; other 1С platform versions are not
  covered.
- **No live 1С execution as part of this handoff.** The default
  receive-side flow does NOT call `1cv8.exe`. The reference-stand
  runbook is available if you have a stand and want to exercise
  the binary-backed write path, but that is a separate, explicit
  operator action — not something the install / verify wrappers
  perform automatically.
- **No remote `git push`.** The repository is ready for
  publication, but pushing to a git remote is your own decision
  and step.


## Prerequisites

This handoff is **Windows-first**. Other platforms are not yet
covered by the scripts.

| Requirement | How to verify |
|---|---|
| Windows 10/11 with PowerShell 5.1 or PowerShell 7+ | `$PSVersionTable.PSVersion` |
| Python 3.11 or compatible (the project pin lives in `.python-version`; `pyproject.toml` requires `>=3.11`) | `python --version` |
| Git (used by `verify-release.ps1` for `git status` / `git log` / `git grep`) | `git --version` |
| (optional) `1cv8.exe` for the real binary-backed write round-trip on a reference stand | `Test-Path "C:\Program Files\1cv8\<version>\bin\1cv8.exe"`. Only needed if you intend to follow `docs/runbooks/track-a-reference-stand-round-trip.md`. |

If `Get-ExecutionPolicy` returns `Restricted`, invoke scripts
with `powershell -NoProfile -ExecutionPolicy Bypass -File <path>`
or adjust your local policy.


## Release entrypoint map

| Action | Entrypoint | What it does |
|---|---|---|
| Bootstrap `PYTHONPATH` | `scripts/dev/bootstrap_paths.ps1` (dot-source) | Adds the 11 internal `src/` directories to `PYTHONPATH` for the current PowerShell session. The other scripts dot-source it; you rarely call it directly. |
| Local selfcheck | `scripts/dev/launch.ps1 selfcheck` | Imports every internal package and prints registry counts, health summary, `selfcheck_status`. |
| Materialise a product config | `scripts/release/install.ps1 -ConfigPath <in> -OutputConfigPath <out> [-Confirm]` | Runs the install fast path. Default is `preview` (no file written); pass `-Confirm` to actually write. |
| Verify release readiness | `scripts/release/verify-release.ps1 [-AllowDirtyTree] [-SkipSelfcheck]` | Runs seven release-facing checks (layout, entrypoints, docs, working tree, git baseline, selfcheck, credential leak guard). |
| Interactive Python REPL | `scripts/dev/launch.ps1 repl` | Starts `python` interactively with `PYTHONPATH` already set. |
| Run an ad-hoc Python script | `scripts/dev/launch.ps1 run <script.py> [args...]` | Bootstraps `PYTHONPATH`, then `python <script>`. |


## Reproducible install sequence

Follow these steps in order. Each step has an expected success
signal. If a step does not produce the expected signal, stop and
read the corresponding section of `docs/operator-manual.md` or
re-run `verify-release.ps1` with `-AllowDirtyTree -SkipSelfcheck`
to narrow the failure surface.

1. **Open a PowerShell session at the project root.**

   ```powershell
   cd C:\path\to\1c-agent-platform
   ```

   Expected: `Get-Location` shows the project root and
   `Test-Path .git` returns `True`.

2. **Verify prerequisites.**

   ```powershell
   $PSVersionTable.PSVersion
   python --version
   git --version
   ```

   Expected: each command prints a version, no errors.

3. **Run the local selfcheck.**

   ```powershell
   .\scripts\dev\launch.ps1 selfcheck
   ```

   Expected output contains:

   ```
   imports_ok = true
   read_server_tools = [...]                 # 15 names
   write_server_tools = [...]                # 25 names
   intelligence_server_tools = [...]         # 16 names
   selfcheck_status = ok
   ```

   Exit code `0`. If any internal package fails to import,
   stop here.

4. **Run the release-readiness verify.**

   ```powershell
   .\scripts\release\verify-release.ps1
   ```

   Expected: seven check lines, all `[PASS]` (or `[SKIP]` if
   you supplied `-SkipSelfcheck`), and the final
   `Release verify: GREEN (all checks passed or skipped)`.
   Exit code `0`. If any check fails, the summary names the
   offender; address it before proceeding.

5. **(Optional) Materialise a product config in preview mode.**

   ```powershell
   .\scripts\release\install.ps1 `
       -ConfigPath examples\demo-infobase\infobase6.config.json `
       -OutputConfigPath C:\path\to\target\product.config.json
   ```

   Expected: `mode=preview`, `config_written=False`,
   `Preview completed`. **No file is written.**

6. **(Optional) Materialise the config for real.**

   Re-run the same command with `-Confirm`. Expected:
   `mode=executed`, `config_written=True`, `Install fast path
   completed`. Inspect the output file at `-OutputConfigPath`.

After step 4 you have a working local install. Steps 5 and 6
are only needed if you intend to actually configure the platform
against a target environment.


## Verify sequence in detail

`scripts/release/verify-release.ps1` runs seven read-only
checks:

| # | Check | Asserts |
|---|---|---|
| 1 | Repo layout | seven required root files (`LICENSE`, `CHANGELOG.md`, `SECURITY.md`, `README.md`, `PROJECT-STATUS.md`, `pyproject.toml`, `.gitignore`) are present. |
| 2 | Release entrypoints | seven scripts under `scripts/release/` and `scripts/dev/`. |
| 3 | Important docs | eleven documents (manuals, runbooks index, Track A round-trip runbook, plan + step-map for Track A / B / C). |
| 4 | Working tree | clean (or `-AllowDirtyTree`). |
| 5 | Git baseline | branch `main`, non-empty history. |
| 6 | Selfcheck | `imports_ok=true`; registry counts `15 / 25 / 16`; `selfcheck_status=ok`. Skipped with `-SkipSelfcheck`. |
| 7 | Credential leak guard | `git grep` finds none of three PEM private-key header variants (generic, RSA, OpenSSH) and the well-known AWS secret-access-key token in tracked files (excluding self-references). The exact pattern list lives in `scripts/release/verify-release.ps1`; this document avoids quoting the literals to stay outside the scan's match set. |

Exit codes:

- `0` — all checks pass or skip.
- `2` — at least one check failed.
- `64` — wrapper invoked with bad arguments.

When to use which switch:

- Default (no switches) — full release verify before handing off
  the repository to another operator.
- `-AllowDirtyTree` — when you have intentional uncommitted work
  and want to confirm the rest of the release surface is sane.
- `-SkipSelfcheck` — when the Python toolchain is intentionally
  unavailable and you want a fast path/git-only verification.


## Local check / launch sequence

`scripts/dev/launch.ps1` is the operator/dev umbrella:

```powershell
.\scripts\dev\launch.ps1 help                    # usage
.\scripts\dev\launch.ps1 selfcheck               # equivalent to scripts\dev\run_dev_check.ps1
.\scripts\dev\launch.ps1 repl                    # interactive Python with PYTHONPATH
.\scripts\dev\launch.ps1 run <script.py> [args]  # ad-hoc Python script
```

It deliberately does NOT start the MCP servers (no production
transport yet), does NOT run pytest (no test suite yet), does
NOT touch a 1С infobase, does NOT replace the install fast path.


## Known limitations

Some of these have been called out above; they are repeated here
as a single checklist so the receiver does not miss them.

- **DESIGNER credentials are operator-managed.** Track D /
  Step 3 added a documented safer input path: any argv element
  inside `onec_*_command_template` may be the full-element token
  `${ENV:NAME}`, which is resolved at render time from the
  process environment (e.g.
  `"/P", "${ENV:ONEC_DESIGNER_PASSWORD}"`). Missing or empty
  env, and partial / mixed token forms, are fail-closed before
  the subprocess starts. Literal cleartext templates remain
  supported as a legacy fallback. `command_preview` in
  write-tool payloads and the audit row's `details` redacts the
  argv position following `/P` / `/Pwd` (case-insensitive) to
  `<redacted>`; the actual subprocess argv is not redacted
  (the 1С binary must authenticate). The platform still does
  not ship a secrets manager, vault, KMS, OS keychain
  integration, or encrypted-at-rest secrets file format —
  operators feed env vars from their own secrets infrastructure
  if they need that.
- **Pre-1.0 software.** Backwards-compatibility guarantees
  across versions are not yet in place.
- **Single-version 1С coverage** — `8.3.27.1859`. Other versions
  are not yet exercised.
- **Limited rollback coverage** — the automatic rollback
  whitelist is small and intentional. See
  `apps/platform/README.md` and the Phase 6 / Step 4 history in
  `PROJECT-STATUS.md`.
- **No production-grade MCP transport.** Treat the servers as
  local development services, not as exposed network endpoints.
- **No installer ecosystem.** See "What is NOT in this handoff"
  above.

For the security report flow, see `SECURITY.md`.


## Where to read deeper

- **Project entry** — `README.md` (project intro + Quickstart).
- **Per-step status across all tracks** — `PROJECT-STATUS.md`.
- **Release wrappers detail** — `scripts/release/README.md`.
- **Local dev wrappers detail** — `scripts/dev/README.md`.
- **Product layer surface** — `apps/platform/README.md`.
- **Operator-facing reference** — `docs/operator-manual.md`.
- **Administrator-facing reference** — `docs/administrator-manual.md`.
- **Developer-facing reference** — `docs/developer-manual.md`.
- **Reproducible scenarios** — `docs/runbooks/`, including the
  Track A reference-stand round-trip.
- **Phase / track plans + step maps** — `docs/architecture/`.
- **Version notes** — `CHANGELOG.md`.
- **Security reporting + safety guarantees** — `SECURITY.md`.

If something in this handoff document does not match what you
see in the repository, the discrepancy itself is a signal worth
reporting back to the previous custodian — silent drift between
this document and the rest of the repo is exactly what
`scripts/release/verify-release.ps1` is designed to catch.
