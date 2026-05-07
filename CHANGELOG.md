# Changelog

All notable changes to **1C Agent Platform** are documented in this file.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and the project adheres to [Semantic Versioning](https://semver.org/) starting
from `0.1.0`.

## 0.1.0 — initial public snapshot

The first publicly trackable snapshot of the project. The version
matches `pyproject.toml`.

### Closed before 0.1.0

- **Phases 1–6** — read MVP, write MVP, metadata changes, intelligence
  layer, product layer, industrialization & completion track.
  See `PROJECT-STATUS.md` for per-phase detail.
- **Parallel Track A — Full Real 1cv8-backed Write Path** — closed on
  Step 7. Real binary-backed write path
  (`/DumpConfigToFiles` / `/LoadConfigFromFiles` / `/UpdateDBCfg`) is
  proven on a reference stand. See
  `docs/runbooks/track-a-reference-stand-round-trip.md`.
- **Parallel Track B — Productization & Delivery Polish** — closed on
  Step 6 (final integration pass and Track B closure). Six steps
  total; production code untouched throughout the track. Per-step
  outcomes:
  - Step 1 (planning) — two planning documents under
    `docs/architecture/track-b-*`.
  - Step 2 (repo hygiene + legal layer) — `git init` on `main`,
    extended `.gitignore`, this `CHANGELOG.md`, `LICENSE`
    (Apache-2.0, full standard text), `SECURITY.md`, first
    meaningful commit.
  - Step 3 (operator-discoverable install fast path) — thin
    PowerShell wrapper `scripts/release/install.ps1` over the
    existing `run_install_fast_path` helper, plus
    `_install_runner.py` and `scripts/release/README.md`.
  - Step 4 (operator/dev local launch umbrella) —
    `scripts/dev/launch.ps1` with `selfcheck` / `repl` / `run` /
    `help` subcommands; updated `scripts/dev/README.md`.
  - Step 5 (root README quickstart and docs polish) — top-level
    `## Quickstart` block in this README with install / check /
    launch commands and a deeper-docs map.
  - Step 6 (final integration pass and Track B closure) — this
    closure: README + PROJECT-STATUS + CHANGELOG aligned with
    Track B closed status.

### Registry invariant carried into 0.1.0

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track A or Track B.

### Honest constraints carried into 0.1.0

- DESIGNER credentials remain operator-managed and out-of-band; never
  stored in repository.
- Multi-version 1С smoke matrix not yet exercised — single-version
  evidence on `8.3.27.1859`.
- No production-grade MCP transport, no installer ecosystem
  (`.msi` / `.deb` / GUI wizard / signed distribution), no web-UI,
  no full enterprise super-set (SSO/RBAC, multi-tenant, secrets vault
  as a service, federated audit storage, policy-as-code DSL,
  multi-instance HA).
- No hot reload, no OS-level service supervision, no full AST parser,
  no full rollback/delete coverage.

These are honest constraints, not hidden gaps.

### Active work

None. No parallel track is currently open. Phase 7 as a linear phase
is not planned. Opening the next parallel track is an explicit
operator decision.
