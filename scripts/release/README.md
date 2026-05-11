# scripts/release

Operator-facing release / install scripts for **1C Agent Platform**.

This directory holds two thin wrappers:

- **`install.ps1`** — operator-facing entry to the install fast
  path (Track B / Step 3).
- **`verify-release.ps1`** — pre-handoff release sanity check
  (Track C / Step 2).

Neither introduces a new install ecosystem — no `.msi`, no `.deb`,
no GUI wizard, no signed distribution — they only make existing
capabilities operator-discoverable and verify release-facing
invariants.

## install.ps1

Thin PowerShell wrapper around the install fast path helper
`onec_platform.run_install_fast_path_from_json_file` (defined in
`apps/platform/src/onec_platform/installer.py`, originally shipped
in Phase 6 / Step 3).

The wrapper bootstraps `PYTHONPATH` for the monorepo (via
`scripts/dev/bootstrap_paths.ps1`) and forwards the call to the
fast-path helper through `_install_runner.py`. No production code
is touched.

### Usage

Preview (no file is written):

```powershell
.\scripts\release\install.ps1 `
    -ConfigPath examples\demo-infobase\infobase6.config.json `
    -OutputConfigPath C:\path\to\target\product.config.json
```

Execute (actually writes the JSON config):

```powershell
.\scripts\release\install.ps1 `
    -ConfigPath examples\demo-infobase\infobase6.config.json `
    -OutputConfigPath C:\path\to\target\product.config.json `
    -Confirm
```

### Parameters

- `-ConfigPath` (mandatory) — path to the input product config
  JSON. This is the operator-authored product config that should be
  validated and (optionally) materialised at the target location.
- `-OutputConfigPath` (mandatory) — where the materialised JSON
  should be written. The underlying helper refuses to overwrite an
  existing file (`mode=rejected`).
- `-Confirm` (switch, default off) — when present, the wrapper
  calls the helper with `confirm_write=True` and the file is
  actually written. When absent, the wrapper runs in preview mode
  and writes nothing.

### Output and exit codes

The wrapper prints a banner with the resolved paths, dot-sources
`bootstrap_paths.ps1`, runs the helper, and then prints the result
fields:

- `ok`, `mode`, `product_name`, `profile_name`,
  `default_environment`, `output_config_path`, `config_written`;
- any `confirmed findings` and `presumed findings` with their
  severity and code;
- any `recommended actions`.

Exit codes:

| Code | Meaning |
|------|---------|
| `0`  | `ok=True` and `mode in {"preview", "executed"}` |
| `2`  | `mode="rejected"` (target path exists, bad config, layout problem) |
| `3`  | any other failure (`ok=False` outside the rejected path) |
| `64` | wrapper invoked with bad arguments |

### What this wrapper deliberately does NOT do

- Does **not** start MCP servers.
- Does **not** invoke any `mcp_write_server` tool.
- Does **not** touch a 1С infobase.
- Does **not** use `shell=True`.
- Does **not** ship a packaging ecosystem (`.msi` / `.deb` / GUI
  wizard / signed distribution).
- Does **not** replace operator launch ergonomics for the three
  MCP servers — that is planned separately as Track B / Step 4
  and out of Step 3 scope.

### Files (install)

- `install.ps1` — operator entry point.
- `_install_runner.py` — small Python helper called by the
  wrapper. Not meant to be imported. Underscore-prefixed by
  convention.

### Related (install)

- `apps/platform/src/onec_platform/installer.py` — the boundary
  helper this wrapper calls. The wrapper has no logic of its own
  beyond argument forwarding and exit-code mapping.
- `scripts/dev/bootstrap_paths.ps1` — PYTHONPATH bootstrap that
  the wrapper dot-sources.
- `apps/platform/README.md` — bigger picture of the product layer.


## verify-release.ps1

Thin PowerShell wrapper that runs a **pre-handoff release sanity
check**. The script is read-only and never executes production
code. Its purpose is to give an operator confidence that the
repository is ready to be handed off to another operator: the
required files are present, the working tree is clean, the git
baseline matches expectations, the registry invariant has not
drifted, and no obvious credential markers leaked into tracked
files.

`verify-release.ps1` and `install.ps1` are deliberately a parallel
pair: `install.ps1` materialises a product config, `verify-release.ps1`
asserts that the repo itself is fit to ship.

### Usage

```powershell
.\scripts\release\verify-release.ps1
```

With switches:

```powershell
.\scripts\release\verify-release.ps1 -AllowDirtyTree    # tolerate uncommitted work
.\scripts\release\verify-release.ps1 -SkipSelfcheck     # skip the Python invocation
.\scripts\release\verify-release.ps1 -AllowDirtyTree -SkipSelfcheck
```

### Parameters

- `-AllowDirtyTree` (switch, default off) — when present, the
  "Working tree" check passes even if `git status --porcelain`
  reports uncommitted changes. Useful for CI runs that verify
  release-facing invariants before the closing commit. Default
  is to fail on a dirty tree.
- `-SkipSelfcheck` (switch, default off) — when present, skips
  the Python self-check sub-call (Check 6). Useful for very
  fast verification or when the Python toolchain is intentionally
  unavailable. The skipped check appears as `[SKIP]` in the
  summary; it does NOT count as a pass.

### What `verify-release.ps1` checks

| # | Check | What it asserts |
|---|---|---|
| 1 | Repo layout | `LICENSE`, `CHANGELOG.md`, `SECURITY.md`, `README.md`, `PROJECT-STATUS.md`, `pyproject.toml`, `.gitignore` are present in repo root. |
| 2 | Release entrypoints | `scripts/release/{install.ps1, _install_runner.py, README.md}` and `scripts/dev/{launch.ps1, bootstrap_paths.ps1, run_dev_check.ps1, selfcheck.py}` are present. |
| 3 | Important docs | Operator / administrator / developer manuals, runbooks index, Track A reference-stand round-trip runbook, plan + step-map for Track A / B / C are present under `docs/`. |
| 4 | Working tree | `git status --porcelain` is empty (or `-AllowDirtyTree` is set). |
| 5 | Git baseline | Current branch is `main` and history is non-empty. |
| 6 | Selfcheck | `python scripts/dev/selfcheck.py` returns exit 0; output contains `imports_ok = true` and `selfcheck_status = ok`; registry counts are exactly `read=15 / write=25 / intelligence=16`. Skipped with `-SkipSelfcheck`. |
| 7 | Credential leak guard | `git grep` over tracked files finds none of: `BEGIN PRIVATE KEY`, `BEGIN RSA PRIVATE KEY`, `BEGIN OPENSSH PRIVATE KEY`, `aws_secret_access_key`. |
| 8 | Credential template hygiene | Tracked `*.config.json` files (via `git ls-files`) are scanned for argv elements immediately following `"/P"` or `"/Pwd"` (case-insensitive) inside 1С command-template arrays. The two documented safe forms are the env-substitution token `"${ENV:NAME}"` (Track D / Step 3) and the abstract placeholder `"<password>"`; either form is a PASS. Literal cleartext values trigger **WARN** (not FAIL), naming the offending file and line. Empty values are not flagged. The check is deliberately narrow: only tracked `*.config.json`, only the `/P` / `/Pwd` adjacency, no scanning of runbooks or other documentation. |

### Exit codes

| Code | Meaning |
|------|---------|
| `0`  | All checks PASS or SKIP. |
| `2`  | At least one release-facing check FAILED. The summary lists which one. |
| `64` | Wrapper invoked with bad arguments (PowerShell native handling). |

### What `verify-release.ps1` deliberately does NOT do

- It does **not** start MCP servers.
- It does **not** call any `mcp_write_server` tool.
- It does **not** touch a 1С infobase. It does not run `1cv8.exe`.
- It does **not** validate runtime behaviour, schema migrations,
  or write-flow correctness — those are responsibilities of the
  product layer and Track A artifacts, not of release-side
  scaffolding.
- It does **not** validate publication to package managers
  (PyPI / Chocolatey / winget / apt). No publication is in scope.
- It does **not** perform a full security audit. The credential
  leak guard catches the most obvious markers (private key
  headers and one well-known cloud credential token); it is
  belt-and-suspenders, not a substitute for a real secrets scan.
- Check 8 (credential template hygiene) is a narrow heuristic
  over tracked `*.config.json` files; it is **not a full DLP
  scan**. It does not parse 1С template semantics, does not
  scan runbooks or other documentation, does not understand
  templating macros beyond the documented `${ENV:NAME}`
  substitution form, and emits WARN (not FAIL) so legacy
  cleartext templates do not block release verify.
- It does **not** modify the working tree. It is strictly
  read-only.

### Files (verify)

- `verify-release.ps1` — operator entry point. Pure PowerShell,
  no Python helper required (Check 6 invokes the existing
  `scripts/dev/selfcheck.py` directly through the existing
  `bootstrap_paths.ps1` mechanism).

### Related (verify)

- `scripts/dev/bootstrap_paths.ps1` — PYTHONPATH bootstrap that
  the wrapper dot-sources for the selfcheck step.
- `scripts/dev/selfcheck.py` — the script invoked by Check 6.
- `docs/architecture/track-c-packaging-installer-delivery-plan.md`
  — Track C plan that introduced this wrapper.


## Packaging-facing install flow (post-Track-M reality)

The long-standing Track C / Step 3 honest constraint — that
`[tool.hatch.build.targets.wheel] packages = []` was deliberately
empty and `python -m build` produced no usable artefact — was
closed by **Track M / Step 4** (commit `31313db`). The flip and
the operator-facing recipe ship two complementary pieces:

- a buildable `py3-none-any` Python wheel (filename pattern
  `1c_agent_platform-<VERSION>-py3-none-any.whl`) containing the
  eleven src-layout packages spread across `apps/*/src/` and
  `packages/*/src/`, plus the three locked `[project.scripts]`
  console entries — and **nothing else** (no credentials, no
  `.env`, no `examples/`, no `docs/`, no `scripts/`);
- a single operator recipe at
  [`docs/operators/packaging/distribution-boundary.md`](../../docs/operators/packaging/distribution-boundary.md)
  covering all five lifecycle verbs (`build` / `install` /
  `uninstall` / `upgrade` / `verify`) end-to-end with
  placeholder-only examples.

`install.ps1` (this directory) and the Track M wheel are
**orthogonal-but-complementary** axes, not replacements:

| Axis | Provided by |
|---|---|
| Python code delivery (11 packages + 3 console scripts) | the wheel (Track M / Step 4) |
| Operator `ProductConfig` JSON materialisation | `install.ps1` (this directory, Track B / Track I) |
| Reverse-proxy / TLS-termination deployment posture | `docs/operators/deployment-boundary.md` (Track J) |
| Cross-OS service supervision | `docs/operators/service/service-supervision.md` (Track L) |

To work with the platform locally without building the wheel,
the development / verification entrypoints remain:

| Action | Entrypoint |
|--------|-----------|
| Set PYTHONPATH from a repository checkout | `scripts/dev/bootstrap_paths.ps1` |
| Materialise a product config | `scripts/release/install.ps1` |
| Verify release readiness | `scripts/release/verify-release.ps1` |
| Run selfcheck / REPL / ad-hoc Python | `scripts/dev/launch.ps1` |

The build front-end (`build`) is an **operator-side
prerequisite** (`pip install build` on a control host), **not**
a project dependency. The wheel is delivered out-of-band from
the control host to a deployment host the operator owns;
**no publication** to PyPI, Chocolatey, Homebrew, apt,
conda-forge, NuGet, or any other package index is in scope.
No `.msi`, `.deb`, `.rpm`, `.dmg`, `.pkg`, `.snap`, `.flatpak`,
GUI installer, wizard, or signed binary distribution is in
scope. The Track M / Step 3 contract (the normative source-of-
truth for these boundaries) lives at
[`docs/architecture/track-m-packaging-ecosystem-and-distribution-boundary-contract.md`](../../docs/architecture/track-m-packaging-ecosystem-and-distribution-boundary-contract.md).
