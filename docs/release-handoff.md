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
  (`scripts/release/verify-release.ps1`) covering eight
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
- A **two-transport MCP baseline** for the three MCP servers:
  - **`--transport stdio`** (default; Track G / Step 4) —
    `python -m mcp_read_server`, `python -m mcp_write_server`,
    `python -m mcp_intelligence_server` start a line-delimited
    JSON-RPC 2.0 stdio loop. Trusted local subprocess use only;
    no network listener; no auth (the channel is not network-
    exposed).
  - **`--transport http`** (Track H / Step 4) — single `/mcp`
    HTTP/1.1 endpoint, POST only, `application/json`, 1 MiB
    body cap, static bearer authentication
    (`Authorization: <case-insensitive-Bearer> <token>`,
    constant-time compare). Required CLI flags when http:
    `--bind <HOST>:<PORT>` (no default; binding must be
    explicit) and a token source — either
    `--auth-token-env <VARNAME>` (CLI flag wins over config)
    or `auth.tokens` in product config (each entry MUST be
    `${ENV:NAME}` env-substitution; literal cleartext
    rejected). Trusted-network deployment behind an operator-
    owned reverse proxy that terminates TLS; the listener
    itself binds plain HTTP/1.1.
  - The three names are also declared as `[project.scripts]`
    console entries in `pyproject.toml`. The CLI flag set
    (`--help`, `--config-path`, `--transport {stdio,http}`,
    `--log-level`, `--bind`, `--auth-token-env`) is identical
    across all three servers.
- **Per-track planning documents** under `docs/architecture/`
  for Track A, Track B, Track C.
- **Operator-facing deployment-boundary recipe** (Track J /
  Step 4 deliverable, PATH A docs-only) at
  [`docs/operators/deployment-boundary.md`](operators/deployment-boundary.md):
  single-source-of-truth ten-section recipe for the
  `--transport http` deployment shape — per-scenario
  MUST/SHOULD/MAY matrix (loopback / trusted private
  subnet / public-facing-through-reverse-proxy),
  per-scenario walkthroughs, explicit Forwarded-header
  MUST-NOT-consume policy (listener does not consume
  `X-Forwarded-*` / `Forwarded` / `X-Real-IP` /
  `True-Client-IP` / `CF-Connecting-IP` for any
  trust / authz / routing / audit decision), `/healthz`
  non-shipping with strict-2xx-only-prober workarounds,
  two abstract reverse-proxy snippets (nginx + Caddy),
  eight operator decision-point Q&A, honest non-goals.
  This is the document to read **before** standing up
  the HTTP listener anywhere off-loopback. The Track J
  Step 3 contract that pinned PATH A and the
  per-scenario matrix lives at
  [`docs/architecture/track-j-deployment-boundary-contract.md`](architecture/track-j-deployment-boundary-contract.md).
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
- **Stdio + narrow HTTP+bearer transport baseline; no
  hostile-network / enterprise-identity story.** Two
  transports are shipped (Track G / Step 4 stdio, Track H /
  Step 4 HTTP+bearer; see "What is in this handoff" above).
  Threat model = trusted-local-stdio for stdio, trusted-
  network behind an operator-owned reverse proxy for HTTP.
  Specifically NOT in this handoff: TLS / HTTPS termination
  in process; mTLS / client certificate authentication; JWT
  / OAuth 2.0 / OIDC / SAML / SCIM; RBAC / ABAC / per-tool
  ACL / per-tenant isolation; token rotation endpoint /
  refresh tokens / session cookies; rate limiting; WebSocket
  / SSE / TCP / Unix-socket / named-pipe transports;
  supervisor daemon / systemd unit / Windows Service
  registration / hot reload; multi-tenant identity stack.
  The wheel build remains empty
  (`[tool.hatch.build.targets.wheel] packages = []`), so
  the `[project.scripts]` console entries materialise as
  installable binaries only when a future packaging track
  ships an actual wheel — meanwhile the documented
  invocation is `python -m <server>`. **Install fast path
  auth round-trip preserved (Track I / Step 4):**
  `installer.py:_config_to_dict` now emits the operator's
  `auth.tokens` declarations symmetric to the existing
  Phase 6 / Step 8 enterprise-block emit-only-when-divergent
  pattern. A config round-tripped through
  `scripts/release/install.ps1 ... -Confirm` preserves
  `auth.tokens` byte-identical to the source list (raw
  `${ENV:NAME}` strings remain raw configuration data; env
  resolution happens at server startup, not at install
  time). Pre-Track-H configs without an `auth` section
  continue to round-trip byte-identical (no implicit
  `"auth": {}` injection). Operators using
  `--transport http` against a round-tripped config no
  longer have to re-add the section by hand; the
  `--auth-token-env <VARNAME>` CLI override remains
  available for operators who prefer not to declare tokens
  in the config file at all.
- **No web UI / dashboard frontend.**
- **No enterprise super-set** (SSO/RBAC, multi-tenant, secrets
  vault as a service, federated audit storage, policy-as-code
  DSL, multi-instance HA).
- **No hot reload or OS-level service supervision** (Windows
  Service / systemd unit registration, automatic restart
  supervisor).
- **Multi-version 1С smoke matrix — scaffolding only.** Real-stand
  binary-backed evidence exists for `8.3.27.1859` (Windows x64,
  file-based reference stand) — represented as the reference row
  in [`docs/version-support-matrix.md`](version-support-matrix.md).
  Track E (Multi-Version 1C Smoke Matrix) ship'ит **scaffolding**
  для extension этой базы: frozen smoke scenario (`frozen-smoke-v1`),
  operator runbook
  ([`docs/runbooks/track-e-multi-version-smoke-matrix.md`](runbooks/track-e-multi-version-smoke-matrix.md)),
  и matrix-table doc. **Additional version evidence rows пока не
  добавлены** — Track E / Step 4 закрыт через honest operator-supplied
  gap (отсутствие 1С minor families помимо `8.3.27` на operator
  machine). Other 1С platform versions therefore are not yet
  evidenced. Additional rows возможны post-closure через
  operator-driven runs.
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
| Verify release readiness | `scripts/release/verify-release.ps1 [-AllowDirtyTree] [-SkipSelfcheck]` | Runs eight release-facing checks (layout, entrypoints, docs, working tree, git baseline, selfcheck, credential leak guard, credential template hygiene). |
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

   Expected: eight check lines, mostly `[PASS]` (or `[SKIP]`
   for selfcheck if you supplied `-SkipSelfcheck`; check 8 may
   report `[WARN]` on legacy templates without failing the run),
   and the final
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

`scripts/release/verify-release.ps1` runs eight read-only
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
| 8 | Credential template hygiene | Scans tracked `*.config.json` files for argv elements following `"/P"` or `"/Pwd"` (case-insensitive) inside 1С command-template arrays. Documented safe forms — `"${ENV:NAME}"` (Track D / Step 3 substitution) and the abstract `"<password>"` placeholder — pass; literal cleartext values emit `[WARN]` (not `[FAIL]`) and are reported with `file:line`. Empty values are not flagged. Heuristic only — narrow by design (only `*.config.json`, only the `/P` adjacency). |

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

It deliberately does NOT start the MCP servers — those are
launched separately via `python -m mcp_read_server` /
`python -m mcp_write_server` /
`python -m mcp_intelligence_server`. Each server accepts
`--transport stdio` (default; Track G / Step 4) or
`--transport http` (Track H / Step 4, additionally requires
`--bind <HOST>:<PORT>` and a bearer-token source —
`--auth-token-env <VARNAME>` or `auth.tokens` in product
config). Threat model = trusted-local-stdio for stdio,
trusted-network behind an operator-owned reverse proxy for
HTTP; in-process TLS is not provided. It also does NOT run
pytest (no test suite yet), does NOT touch a 1С infobase,
does NOT replace the install fast path.


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
  are not yet exercised. Multi-version smoke matrix scaffolding
  (frozen scenario + operator runbook + matrix table) ship'нута
  Track E / Steps 1–3 и закрыта Step 4 через honest
  operator-supplied gap; single source of truth для актуального
  evidence-уровня —
  [`docs/version-support-matrix.md`](version-support-matrix.md).
- **Limited rollback coverage** — the automatic rollback
  whitelist remains narrow and intentional. After Track F /
  Step 4 (post-Phase-6 parallel track) it contains exactly
  6 entries: `add_catalog_attribute`,
  `add_document_attribute`, `add_form_attribute`,
  `add_form_element`, `append_module_method`,
  `replace_module_method_body`. That covers 6 of 25 mutating
  registry tools = 24% mutating surface; the remaining
  19 tools (incl. `create_*` family,
  `apply_config_from_files`,
  `update_database_configuration`, multi-file ops) stay
  outside the rollback whitelist by design — there is no
  blanket reversibility claim. See `apps/platform/README.md`,
  `docs/architecture/track-f-rollback-whitelist-expansion-plan.md`,
  `docs/architecture/track-f-rollback-baseline-audit.md`,
  and `docs/architecture/track-f-rollback-eligibility-contract.md`
  for full rationale and per-tool tier breakdown.
- **Stdio + narrow HTTP+bearer transport baseline.** Track G
  / Step 4 ship'нул the local stdio JSON-RPC 2.0 transport;
  Track H / Step 4 added a single HTTP/1.1 `/mcp` endpoint
  with static bearer authentication on top of the existing
  `list_tools()` / `get_tool(name)` boundary. Threat model =
  trusted-local-stdio for stdio, trusted-network behind an
  operator-owned reverse proxy for HTTP. No in-process TLS;
  no mTLS / OAuth / JWT / SAML / SCIM / RBAC / multi-tenant;
  no WebSocket / SSE / TCP / pipe transports; no supervisor /
  systemd / Windows Service registration; no hot reload; no
  web UI; no token rotation endpoint. After Track I / Step 4,
  `installer.py:_config_to_dict` preserves operator
  `auth.tokens` declarations byte-identical through install
  fast path round-trip; raw `${ENV:NAME}` strings remain
  raw configuration data (no env resolution at install
  time). See `SECURITY.md` "Honest constraints" for the
  full per-transport statement including the post-Track-I
  install fast path auth-round-trip preservation behaviour.
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
- **Operator-facing deployment-boundary recipe (HTTP transport)** —
  [`docs/operators/deployment-boundary.md`](operators/deployment-boundary.md).
  The single recipe for deploying `--transport http` safely
  behind an operator-owned reverse proxy. Required reading
  before any non-loopback HTTP exposure.
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
