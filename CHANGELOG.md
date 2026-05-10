# Changelog

All notable changes to **1C Agent Platform** are documented in this file.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and the project adheres to [Semantic Versioning](https://semver.org/) starting
from `0.1.0`.

## 0.5.0 — Parallel Track H — Network-Grade MCP Transport and Authentication Boundary

This release closes **Parallel Track H — Network-Grade MCP
Transport and Authentication Boundary**, the eighth post-
phase parallel track. Track H shipped the **second maturity
layer** on top of Track G: a single HTTP/1.1 `/mcp` endpoint
with static bearer authentication, additive over the existing
local stdio transport. The same `list_tools()` /
`get_tool(name)` boundary serves both transports; the
existing `--transport stdio` path is preserved byte-
identically. **No new MCP tools.** **No changes to tool
registries, `mcp_common` public API, audit row `details`
shape, or `run_write_flow` discipline.** Six steps plus one
Step 2 follow-up; production code was touched in only one
step (Step 4) and only on the explicit allowed surfaces.

The version bump `0.4.0` → `0.5.0` (Q7 resolved YES) reflects
that Track H / Step 4 shipped a real production code change
with observable runtime capability delta:
`python -m mcp_<server> --transport http --bind ...
--auth-token-env ...` now actually starts an HTTP/1.1
listener with bearer authentication, whereas before Track H
the existing `_stdio_transport._build_arg_parser` had
`ALLOWED_TRANSPORTS=("stdio",)` and rejected `http` at
argparse level. This is backward-compatible new functionality
classifying as a classic MINOR bump per SemVer (existing
`--transport stdio` byte-identical via delegation to
`_stdio_transport._serve_stdio`; `mcp_common/__init__.py`
`__all__` byte-identical; `_stdio_transport.py` byte-
identical; `[project.scripts]` byte-identical; registries
`15/25/16` invariant; audit `details` shape preserved; new
`ProductConfig.auth` is an optional field with
`default_factory=ProductAuthSettings`, so pre-Track-H
configs continue to load unchanged).

### Per-step outcomes

- **Step 1 (planning network-grade MCP transport and
  authentication boundary)** — two planning documents under
  `docs/architecture/track-h-*` (plan + step-map). 7 open
  questions Q1–Q7. No code changes. Commit `563b27b`.
- **Step 2 (transport / auth baseline audit)** — one new
  descriptive documentation-only document
  (`track-h-transport-and-auth-baseline-audit.md`,
  1085 lines, 11 sections). Per-server / per-package /
  per-pyproject inventory + 4-class breakdown (11 reusable
  / 8 adjacent / 11 missing / 12 out-of-scope) + read-only
  evidence (zero hits across 8 grep categories: HTTP server
  libs, SSE, WebSocket, TCP, TLS, auth, sessions, rate-
  limit). Resolved Q1 (HTTP-based MCP transport), Q2
  (exactly one transport family), Q3 (static bearer token
  via `Authorization` header, constant-time compare, fail-
  closed), Q4 (`ProductConfig.auth.tokens` + Track D
  `${ENV:NAME}` pattern + `--auth-token-env` CLI override).
  Commit `3c74564`.
- **Step 2 follow-up (credential leak guard self-reference
  fix)** — narrow one-file fix removing four literal
  credential-leak-guard pattern strings from the audit doc
  that started self-matching against `verify-release.ps1`
  Check 7 once the file became tracked (the same self-
  reference hazard the script already handles for itself
  and its README via the `$excludes` list). Paraphrased
  without weakening the audit's meaning; touching
  `scripts/release/verify-release.ps1` deliberately
  avoided. Commit `0628f4c`.
- **Step 3 (network transport / auth contract)** — one new
  prescriptive normative document
  (`track-h-network-transport-and-auth-contract.md`, 1650
  lines) using RFC 2119-style MUST / MUST NOT / SHALL /
  SHOULD / MAY wording (293 normative keyword usages: 199
  MUST, 74 MUST NOT, 17 MAY, 2 SHOULD, 1 SHALL). 18
  sections pinning the exact transport family, framing,
  endpoint, MCP method coverage, JSON-RPC ↔ HTTP boundary
  (per-failure-mode HTTP status + envelope shape pinned),
  concurrency, auth contract (`Authorization: <case-
  insensitive-Bearer> <token>`, `hmac.compare_digest`,
  failure-equivalence rule, complete redaction discipline,
  exhaustive forbidden auth-shape list), config schema, CLI
  surface, integration boundary, backward compatibility,
  TLS posture (in-process TLS forbidden; operator-reverse-
  proxy responsibility), `pyproject.toml` posture, exact
  Step 4 implementation surface (allowed/forbidden file
  lists), verification protocol. Commit `2e76061`.
- **Step 4 (narrow HTTP transport and bearer auth boundary)**
  — the only step with production code change.
  Implementation PATH A. Five files changed (+877 / -35,
  1 new + 4 modified):
  - `packages/mcp-common/src/mcp_common/_network_transport.py`
    — new, 549 LOC; underscore-prefixed internal helper,
    NOT exported from `mcp_common.__init__`; pure stdlib
    (`http.server.ThreadingHTTPServer`, `hmac`, `os`, `re`,
    `json`, `argparse`, `logging`, `sys`, `email.message`).
    Implements the `/mcp` POST handler (GET → 405+
    `Allow:POST`; non-`/mcp` → 404; wrong Content-Type →
    415+`-32600`; body > 1 MiB → 413+`-32600`; multiple
    Authorization headers → 400+`-32600`; case-insensitive
    Bearer scheme; constant-time token compare; failure-
    equivalence 401+`WWW-Authenticate: Bearer realm="mcp"`+
    JSON-RPC `-32001` for missing/empty/malformed/invalid
    tokens; notifications → 204; complete token-redaction
    discipline) and a unified `run_main_http(...)` that
    handles both `--transport stdio` and `--transport http`
    via a single argparser (stdio path delegates to
    existing `_stdio_transport._serve_stdio` byte-
    identically).
  - Three `__main__.py` (modified) — switched import
    `_stdio_transport.run_main` → `_network_transport.run_main_http`;
    `SERVER_VERSION` bumped 0.3.0→0.4.0; module docstrings
    describe both transports; `main() -> int` signature
    preserved.
  - `apps/platform/src/onec_platform/models.py` (modified)
    — added `ProductAuthSettings` dataclass with
    `tokens: list[str]` + `auth: ProductAuthSettings`
    field on `ProductConfig` with `default_factory`.
  - `apps/platform/src/onec_platform/loader.py` (modified)
    — added `_AUTH_ENV_TOKEN_RE` regex byte-identical to
    Track D pattern; added `_parse_auth(auth_raw)` with
    unknown-keys reject, list-of-strings validation,
    env-substitution regex enforce per entry, literal
    cleartext fail-closed at config-load time. Wired into
    `load_product_config`. Commit `5814041`.
- **Step 5 (operator docs and security alignment)** — six
  docs aligned with the actual Step 4 surface (+410 / -173
  lines): `README.md` Quickstart + "Что Quickstart не
  обещает" + full rewrite of "Active parallel track"
  section enumerating Steps 1–4 closure summary;
  `SECURITY.md` "Local stdio MCP transport only" bullet
  replaced with structured per-transport block (stdio
  threat model + http threat model) plus exhaustive
  still-NOT list and the installer auth-round-trip gap;
  `docs/release-handoff.md` four locations updated;
  `apps/platform/README.md` four locations updated;
  `scripts/dev/launch.ps1` header comment + Show-Usage
  help text point operators at both transports;
  `scripts/dev/README.md` `launch.ps1` parenthetical
  rewritten. `PROJECT-STATUS.md` and `CHANGELOG.md`
  deliberately not touched (closure territory). Commit
  `407a2f2`.
- **Step 6 (final integration pass and Track H closure)** —
  this closure: `pyproject.toml` version bumped 0.4.0 →
  0.5.0 (Q7 = YES); `README.md`, `PROJECT-STATUS.md`, and
  `CHANGELOG.md` aligned with Track H closed status. Read-
  only final integration check green: linear Step 1 → 6
  history, all Step 1–5 deliverables present on disk,
  registries without drift, `verify-release.ps1` GREEN on
  8 checks, no real credentials anywhere in the seven
  Track H commits, no 1cv8.exe runs at any Track H step.

### Actual launch surface after Track H closure

```
python -m mcp_read_server --transport stdio --help
python -m mcp_read_server --transport http \
    --bind 127.0.0.1:8765 --auth-token-env MCP_TOKEN --help
```

(and analogously for `mcp_write_server` and
`mcp_intelligence_server`). The CLI flag set is identical
across all three servers: `--help`, `--config-path`,
`--transport {stdio,http}`, `--log-level
{DEBUG,INFO,WARNING,ERROR}`, `--bind <HOST>:<PORT>`,
`--auth-token-env <VARNAME>`. `--bind` and a token source
(either `--auth-token-env <VARNAME>` or non-empty
`auth.tokens` in product config) are required when
`--transport http`; both are silently ignored when
`--transport stdio`.

The HTTP `/mcp` endpoint accepts only POST with
`Content-Type: application/json` and a single JSON-RPC
2.0 message per body up to 1 MiB. The `Authorization`
header is required (`<case-insensitive-Bearer> <token>`);
missing, empty, malformed, mismatched, or duplicate
header all map to a deterministic shape (401 +
`WWW-Authenticate: Bearer realm="mcp"` + JSON-RPC
`-32001` envelope, except multiple-Authorization which
maps to 400+`-32600`). Token validation is constant-time
via `hmac.compare_digest`. Token values, lengths, prefixes,
suffixes, hashes, and fingerprints never appear in stderr
logs, response bodies, error messages, or audit `details`.

Tool dispatch goes through the existing `server.py`
boundary (`list_tools()` / `get_tool(name)`); the
`run_write_flow` discipline for write tools and the
read-only-by-construction discipline of the intelligence
server are preserved unchanged on both transports.

### Registry invariant carried through Track H

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track H.

### Honest constraints update under Track H closure

- **Local trusted-stdio + trusted-network HTTP+bearer
  baseline only.** Threat model = local trusted stdio
  boundary for `--transport stdio`, trusted-network
  deployment behind operator-owned reverse proxy for
  `--transport http`. The platform does not claim
  production readiness for adversarial-internet
  deployment.
- **No in-process TLS / HTTPS termination.** Operator
  is responsible for TLS termination at the reverse
  proxy layer; the Track H listener binds plain HTTP/1.1
  and SHOULD be bound to a loopback or private interface.
- **No mTLS / client certificate authentication.**
- **No JWT / OAuth 2.0 / OIDC / SAML / SCIM**, no token
  introspection / refresh / rotation endpoints, no
  session cookies.
- **No RBAC / ABAC / per-token permissioning / per-tool
  ACL / per-tenant isolation / multi-tenant policy
  engine.** Single-tier auth: a valid token grants access
  to the full tool registry.
- **No rate limiting / quotas / throttling.**
- **No WebSocket / Server-Sent Events / TCP / Unix-socket
  / named-pipe transports.**
- **No supervisor daemon / systemd unit / Windows Service
  registration / `launchd` plist / hot reload / restart
  watcher.** Each server is a single-shot process; the
  operator (or the existing `apps/platform/runtime.py`
  boundary, which Track H did not extend) is responsible
  for lifecycle.
- **No web UI / dashboard frontend.**
- **No standalone `apps/platform` entrypoint** (Q6
  carry-over from Track G).
- **No packaging ecosystem beyond `[project.scripts]`
  declarations.** No `.msi` / `.deb` / GUI installer /
  signed binary distribution / PyPI / wheel publication.
  Track C wheel-build empty constraint preserved.
- **No new MCP tools.** Registry counts unchanged.
- **No 1cv8.exe runs at any Track H step.** Track H
  operates at the process / transport / auth layer; the
  1cv8 binary surface is not engaged.
- **Known install fast path round-trip limitation.**
  `apps/platform/src/onec_platform/installer.py:_config_to_dict`
  does not yet emit the new `auth` section, so a config
  round-tripped through `scripts/release/install.ps1
  ... -Confirm` silently loses its `auth.tokens`
  declarations. Operators using `--transport http`
  against a round-tripped config get a clean fail-
  closed startup ("`--transport http requires
  --auth-token-env or auth.tokens in product config`")
  and can either re-add the section by hand or use
  `--auth-token-env <VARNAME>` to bypass the config.
  Future post-Track-H fix to `_config_to_dict` is
  analogous to the Phase 6 / Step 9 service-level +
  enterprise round-trip fix.
- **No real MCP client integration test as a closure
  gate.** Real client testing (Claude Desktop, MCP CLI
  launching the server) is recommended but not blocking
  (Track G precedent carry-over).
- **All other 0.4.0 honest constraints carry forward
  unchanged** (local stdio baseline; rollback whitelist
  6 of 25 mutating registry tools; no `delete_*` family;
  no multi-file restore; no DB schema rollback; no AST
  semantic inversion; no transactional rollback).
- **All earlier 0.3.0 / 0.2.0 / 0.1.0 honest constraints
  carry forward unchanged** (DESIGNER credentials via
  `${ENV:NAME}` substitution; 8th hygiene check in
  `verify-release.ps1`; no installer ecosystem; no full
  enterprise super-set; no full AST parser; no full
  rollback / delete coverage).

### Active work

None. No parallel track is currently open after Track H
closure. Phase 7 as a linear phase is not planned. Opening
the next parallel track is an explicit operator decision.

## 0.4.0 — Parallel Track G — Production-Grade MCP Transport and CLI

This release closes **Parallel Track G — Production-Grade MCP
Transport and CLI**, the seventh post-phase parallel track.
Track G shipped the **first production-grade operational
layer** for the three MCP servers: canonical `__main__.py`
entrypoints (`mcp_read_server` / `mcp_write_server` /
`mcp_intelligence_server`), a minimum-viable line-delimited
stdio JSON-RPC 2.0 transport (stdlib-only, no third-party
SDK), a minimal CLI surface (`--help`, `--config-path`,
`--transport`, `--log-level`), and `[project.scripts]`
console entries in `pyproject.toml`. **No new MCP tools.**
**No changes to tool registries, `mcp_common` public API,
audit row `details` shape, or `run_write_flow` discipline.**
Six steps total; production code was touched in only one
step (Step 4); all other steps were
documentation/status/version-only.

The version bump `0.3.0` → `0.4.0` (Q7 resolved YES) reflects
that Track G / Step 4 shipped a real production code change
with observable runtime capability delta:
`python -m mcp_read_server` (and the two siblings) now
actually start a stdio JSON-RPC server, whereas before
Track G the modules were not runnable as scripts at all.
This is backward-compatible new functionality classifying as
a classic MINOR bump per SemVer (existing `list_tools()` /
`get_tool(name)` API preserved byte-identical; the new helper
`mcp_common._stdio_transport` is underscore-prefixed and is
NOT exported from `mcp_common.__init__`, so the public API
surface of `mcp_common` is preserved byte-identical).

### Per-step outcomes

- **Step 1 (planning production-grade MCP transport and CLI)** —
  two planning documents under `docs/architecture/track-g-*`
  (plan + step-map). 7 open questions Q1–Q7. No code
  changes. Commit `7a39454`.
- **Step 2 (transport baseline audit)** — one new
  descriptive documentation-only document
  (`track-g-transport-baseline-audit.md`, 587 lines). Per-
  server inventory of the current state with a 4-class
  breakdown (already useful baseline / adjacent insufficient
  / clearly missing / out-of-scope). Critical findings:
  zero declared runtime dependencies in `pyproject.toml`,
  zero MCP SDK imports anywhere in repo, all three MCP
  server packages identical in structure and lacking
  `__main__.py`. **Q1 resolved** (stdio only). **Q2
  resolved** (custom stdlib only, no new pyproject deps).
  **Q6 resolved** (`apps/platform` standalone entrypoint
  out-of-scope). Commit `6f3ad73`.
- **Step 3 (runtime CLI / entrypoint contract)** — one new
  prescriptive normative document
  (`track-g-runtime-cli-entrypoint-contract.md`, 879 lines)
  using RFC 2119-style MUST / MUST NOT / SHALL / SHOULD /
  MAY wording (85 normative keyword usages). 15 sections
  pinning down the exact `__main__.py` shape, exact CLI
  surface, exact transport scope (stdio JSON-RPC 2.0 only,
  forbidden libraries, stdout/stderr discipline,
  minimum-viable MCP method set), server binding /
  dispatch contract via existing `list_tools()` /
  `get_tool(name)` boundary, no-auth / no-supervisor
  posture, exact `[project.scripts]` block content,
  backward compatibility statement, exact Step 4
  implementation surface (allowed files + forbidden
  surfaces + scope creep markers), verification protocol.
  Commit `8bb3883`.
- **Step 4 (narrow stdio transport and CLI entrypoints)** —
  the only step with production code change. Implementation
  PATH B (3 entrypoints + pyproject scripts + 1 private
  `mcp_common` helper); PATH A pure inline rejected because
  each `__main__.py` would have carried ~140 LOC of
  identical argparse / JSON-RPC framing / dispatch logic
  (~280 LOC of pure copy-paste across 3 servers),
  qualifying as "duplication otherwise unreasonable" under
  Step 3 contract §12.1.4. Five files changed (+361
  lines):
  - `packages/mcp-common/src/mcp_common/_stdio_transport.py`
    — new, 245 LOC; underscore-prefixed internal helper,
    NOT exported from `mcp_common.__init__`; pure stdlib
    (`argparse`, `json`, `logging`, `inspect`, `sys`);
    implements line-delimited JSON-RPC 2.0 loop, the four
    required CLI flags, handlers for `initialize` /
    `ping` / `tools/list` / `tools/call` /
    `notifications/initialized` /
    `notifications/cancelled`, `ToolResult` → MCP
    envelope serialization (`content` +
    `structuredContent` + `isError`), top-of-`run_main`
    exception boundary; `sys.stdout` reserved for
    JSON-RPC envelopes, all diagnostic output routed to
    `sys.stderr` via `logging`.
  - `apps/mcp-read-server/src/mcp_read_server/__main__.py`,
    `apps/mcp-write-server/src/mcp_write_server/__main__.py`,
    `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
    — new, ~30 LOC each; each defines `main() -> int`
    that calls `run_main` with the package's existing
    `list_tools` / `get_tool` boundary and a per-server
    name + version. No `__init__.py` edits, no
    `server.py` edits, no `tools.py` / `models.py` /
    `runtime/` / `apps/platform/` touches.
  - `pyproject.toml` — `[project.scripts]` block added
    with exactly three console entries (`mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`). No
    new dependencies; the
    `[tool.hatch.build.targets.wheel] packages = []`
    block (Track C / Step 3 honest constraint) is
    preserved unchanged. Commit `370c5a8`.
- **Step 5 (operator docs and transport alignment)** —
  six docs aligned with the actual Step 4 surface
  (+229 / -81 lines): `README.md` Quickstart paragraph +
  "Что Quickstart не обещает" + full rewrite of "Active
  parallel track" section enumerating closed Steps 1–4
  with artifacts and the actual launch surface;
  `SECURITY.md` "No production-grade MCP transport yet"
  bullet replaced with "Local stdio MCP transport only"
  block (explicit threat model, explicit still-NOT list);
  `docs/release-handoff.md` new "What is in this
  handoff" bullet for the three `python -m` entrypoints,
  reworded "What is NOT in this handoff", launch-section
  parenthetical fix, "Known limitations" alignment;
  `apps/platform/README.md` four "transport / `__main__`
  / CLI does not exist" locations rewritten under the
  Step 4 baseline while preserving network / auth /
  supervisor out-of-scope; `scripts/dev/launch.ps1`
  header comment + `Show-Usage` help text point operators
  at `python -m <server> --help`; `scripts/dev/README.md`
  two operator-facing parentheticals + CI workflow note
  aligned. `PROJECT-STATUS.md` and `CHANGELOG.md`
  deliberately not touched (closure territory). Commit
  `5890ba5`.
- **Step 6 (final integration pass and Track G closure)** —
  this closure: `pyproject.toml` version bumped 0.3.0 →
  0.4.0 (Q7 = YES); `README.md`, `PROJECT-STATUS.md`, and
  `CHANGELOG.md` aligned with Track G closed status. Read-
  only final integration check green: linear Step 1 → 6
  history, all Step 1–5 deliverables present on disk,
  registries without drift, `verify-release.ps1` GREEN on
  8 checks, no real credentials anywhere in the six
  Track G commits, no 1cv8.exe runs at any Track G step.

### Actual launch surface after Track G closure

```
python -m mcp_read_server --help
python -m mcp_write_server --help
python -m mcp_intelligence_server --help
```

Each server starts a line-delimited stdio JSON-RPC 2.0 loop
with handlers for `initialize`, `ping`, `tools/list`,
`tools/call`, `notifications/initialized`, and
`notifications/cancelled`. `sys.stdout` is reserved for
JSON-RPC envelopes; diagnostic output (logs) is routed to
`sys.stderr`. Tool dispatch goes through the existing
`server.py` boundary (`list_tools()` / `get_tool(name)`); the
`run_write_flow` discipline for write tools and the read-
only-by-construction discipline of the intelligence server
are preserved unchanged. CLI flags: `--help`, `--config-path
<path>`, `--transport stdio`, `--log-level
{DEBUG,INFO,WARNING,ERROR}`. The same three names are also
declared as `[project.scripts]` console entries in
`pyproject.toml`; the wheel build remains empty
(`[tool.hatch.build.targets.wheel] packages = []`), so these
console entries become installable binaries only when a
future packaging track ships an actual wheel — meanwhile the
documented invocation is `python -m <server>`.

### Registry invariant carried through Track G

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track G.

### Honest constraints update under Track G closure

- **Local trusted-stdio transport only.** No HTTP, no
  WebSocket, no SSE, no TCP, no Unix domain socket, no
  named pipe / Windows IPC. Network exposure remains
  out-of-scope; threat model = local trusted stdio
  boundary (operator-owned process). A future post-
  Track-G network transport track is the right place
  for any of those.
- **No authentication / authorisation.** No token / Bearer
  / JWT / API key validation; no mutual TLS; no OAuth /
  OpenID Connect / SAML; no RBAC / ABAC; no multi-tenant
  isolation; no rate limiting. The platform does not
  claim production readiness for adversarial network
  deployment.
- **No supervisor / service registration.** No systemd
  unit, no Windows Service, no `launchd` plist, no Docker
  / Kubernetes deployment configuration, no
  `supervisor` / `runit` / `s6` recipes, no automatic
  restart watcher, no log aggregation
  (`journald` / `syslog` / ELK), no distributed tracing
  / observability stack.
- **No hot reload, no background config watcher.** Each
  server is a single-shot process; lifecycle is the
  operator's responsibility (or the existing
  `apps/platform/runtime.py` boundary, which Track G did
  not extend).
- **No web UI / dashboard frontend.**
- **No standalone `apps/platform` entrypoint** (Q6
  explicit out-of-scope; Track G ships entrypoints for
  the three MCP servers only, not for `onec_platform`).
- **No packaging ecosystem beyond `[project.scripts]`
  declarations.** No `.msi` / `.deb` / GUI installer /
  signed binary distribution / PyPI / wheel publication.
  Track C wheel-build empty constraint is preserved.
- **No new MCP tools.** Registry counts unchanged
  (`read=15 / write=25 / intelligence=16`).
- **No 1cv8.exe runs at any Track G step.** Track G
  operates at the process / transport layer; the 1cv8
  binary surface is not engaged.
- **No real MCP client integration test as a closure
  gate.** Real client testing (Claude Desktop, MCP CLI
  launching the server) requires operator infrastructure
  and is recommended but not blocking.
- **All other 0.3.0 honest constraints carry forward
  unchanged** (rollback whitelist 6 of 25 mutating
  registry tools, no public `delete_*`, no multi-file
  restore, no DB schema rollback, no AST semantic
  inversion, no transactional rollback).
- **All earlier 0.2.0 / 0.1.0 honest constraints carry
  forward unchanged** (DESIGNER credentials via
  `${ENV:NAME}` substitution; 8th hygiene check in
  `verify-release.ps1`; no installer ecosystem; no full
  enterprise super-set; no full AST parser; no full
  rollback / delete coverage).

### Active work

None. No parallel track is currently open after Track G
closure. Phase 7 as a linear phase is not planned. Opening
the next parallel track is an explicit operator decision.

## 0.3.0 — Parallel Track F — Rollback Whitelist Expansion

This release closes **Parallel Track F — Rollback Whitelist
Expansion**, the sixth post-phase parallel track. Track F
narrowly extended the existing `_AUTOMATIC_RECOVERY_SUPPORTED`
whitelist (and its mirror `_ROLLBACK_SUPPORTED_OPERATIONS` in
the write-server runtime) from 2 to 6 entries, strictly inside
the existing snapshot-restore-based rollback model. **No new
MCP tools.** **No changes to recovery API, audit row details
shape, or registries.** Six steps total; production code was
touched in only one step (Step 4) and only in two files
(`recovery.py` + `flow.py`); all other steps were
documentation-only.

The version bump `0.2.0` → `0.3.0` (Q5 resolved YES) reflects
that Track F / Step 4 shipped a real production code change
with observable runtime behaviour delta:
`automatic_recovery_supported=True` is now runtime-reachable
for 4 additional tool families through `run_rollback_assistant`.
This is backward-compatible new functionality classifying as a
classic MINOR bump per SemVer.

### Per-step outcomes

- **Step 1 (planning rollback whitelist expansion)** — two
  planning documents under `docs/architecture/track-f-*` (plan
  + step-map). 10 acceptance criteria; 7 open questions Q1–Q7.
  No code changes. Commit `351278b`.
- **Step 2 (rollback baseline audit and candidate selection)** —
  one new descriptive documentation-only document
  (`track-f-rollback-baseline-audit.md`, 637 lines). Manual
  code review of full mcp-write-server registry (25 tools)
  with per-tool tier breakdown: **Tier 4** (already, 2 tools);
  **Tier 1** (strong candidates, 4 tools — `add_form_attribute`,
  `add_form_element`, `append_module_method`,
  `replace_module_method_body` — verified payload-key match
  against `flow.py:_RELATIVE_PATH_KEYS`); **Tier 2** (deferred,
  1 tool — `update_module_code` payload key naming mismatch);
  **Tier 3** (categorically excluded, 5 tools — `create_*`
  family + `apply_config_from_files` +
  `update_database_configuration` with per-criterion violation
  citation). Q2 resolved: Step 4 target set fixed at the four
  Tier 1 tools. Critical finding documented: whitelist lives in
  TWO mirror frozensets that must stay synchronized
  (`recovery.py:_AUTOMATIC_RECOVERY_SUPPORTED` +
  `flow.py:_ROLLBACK_SUPPORTED_OPERATIONS`). Commit `e9725b2`.
- **Step 3 (rollback eligibility contract)** — one new
  prescriptive normative document
  (`track-f-rollback-eligibility-contract.md`, 633 lines)
  using RFC 2119-style MUST / MUST NOT / SHALL / MAY wording
  (64 normative keyword usages). Six eligibility criteria
  4.A–4.F (payload shape, restore semantics, verification,
  sync discipline, non-expansion, implementation surface);
  9 categorical exclusions; exact Step 4 implementation
  boundary with per-tool sanity check anchors and escape
  clause; backward compatibility statement. Q3 (no
  `restore_dump_file_from_snapshot` API change) and Q4 (no
  audit `details` shape change) resolved YES. Commit
  `45ad2b2`.
- **Step 4 (narrow rollback whitelist expansion)** — the only
  step with production code change. Two-file narrow expansion
  2 → 6 entries: `apps/platform/src/onec_platform/recovery.py`
  `_AUTOMATIC_RECOVERY_SUPPORTED` extended; mirror
  `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py`
  `_ROLLBACK_SUPPORTED_OPERATIONS` extended with identical
  6-entry content; minor sync-comment wording update in
  `flow.py:97-103` (allowed per Step 3 contract Section 6.3.1).
  Per-tool sanity check anchors cited in commit message with
  `tools.py` line numbers (3512-3520 / 2680-2687 / 2833-2838 /
  2994-2999) and payload keys for each. No changes to
  `tools.py`, `_RELATIVE_PATH_KEYS`, `_extract_relative_path`,
  audit `details` shape, public API signatures, or registries.
  Diff: 2 files, +17 / -7. Commit `cd95627`.
- **Step 5 (operator docs and rollback coverage alignment)** —
  eight point-edits across three operator-facing docs
  realigning wording with the actual post-Step-4 state:
  `apps/platform/README.md` (5 edits in RECOVERY_MODES /
  «Почему пуст» / «Что не делает» / Phase 6 historical /
  «Что Phase 6 / Step 4 НЕ делал» sections + new «Track F /
  Step 4 — расширение whitelist до 6 tools» subsection),
  `README.md` (2 edits: Quickstart Track F open + Track A
  detail honest constraints bullet), `docs/release-handoff.md`
  (1 edit: Known limitations rollback bullet). Unified support
  statement now consistent across the three modified docs:
  whitelist 2 → 6, broader but still narrow, no blanket
  reversibility claim. SECURITY.md untouched (qualitative
  «small, deliberate set» wording remains accurate). Commit
  `60f1761`.
- **Step 6 (final integration pass and Track F closure)** —
  this closure: `pyproject.toml` version bumped 0.2.0 → 0.3.0
  (Q5 = YES); `README.md`, `PROJECT-STATUS.md`, and
  `CHANGELOG.md` aligned with Track F closed status. Read-only
  final integration check green: linear Step 1 → 6 history,
  all Step 1–5 deliverables present on disk, identical 6-entry
  sets in both mirror frozensets verified, registries without
  drift, `verify-release.ps1` GREEN on 8 checks, no real
  credentials anywhere in the six Track F commits, no
  1cv8.exe runs at any Track F step.

### Final whitelist after Track F closure

Both `_AUTOMATIC_RECOVERY_SUPPORTED` (in `recovery.py`) and
`_ROLLBACK_SUPPORTED_OPERATIONS` (mirror in `flow.py`) contain
exactly six identical entries:

```
add_catalog_attribute        # already (Phase 6 / Step 4)
add_document_attribute       # already (Phase 6 / Step 4)
add_form_attribute           # added (Track F / Step 4)
add_form_element             # added (Track F / Step 4)
append_module_method         # added (Track F / Step 4)
replace_module_method_body   # added (Track F / Step 4)
```

Coverage: 6 of 25 mutating registry tools = 24% mutating
surface. 19 mutating tools remain manual snapshot-restore
territory by design (Tier 3 categorical exclusions:
`create_*` family — inverse = delete with no public `delete_*`
semantics; `apply_config_from_files` — multi-file impact;
`update_database_configuration` — DB schema migration;
multi-file ops in general).

### Registry invariant carried through Track F

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track F.

### Honest constraints update under Track F closure

- **No universal rollback.** Whitelist remains a narrow
  6-entry list; everything outside falls back to manual
  snapshot-restore via operator-side discipline.
- **No public `delete_*` write-tools.** Semantics of deletion
  in 1С remains undecided; Track F deliberately did not
  introduce them. `create_*` family inverse semantics
  therefore stays unimplemented (Tier 3 categorical
  exclusion).
- **No multi-file restore.** `restore_dump_file_from_snapshot`
  remains the exclusive single-file mutating mechanism for
  rollback.
- **No DB schema rollback.** `update_database_configuration`
  inverse remains operator-side external-DB-backup territory.
- **No AST semantic inversion.** File-byte-restore only; no
  BSL / XML semantic understanding for inverse computation.
- **No transactional rollback.** Multi-step chains
  (apply + updatedb sequence) have no atomic rollback.
- **All other 0.2.0 honest constraints carry forward
  unchanged** (DESIGNER credentials via `${ENV:NAME}`
  substitution; 8th hygiene check in `verify-release.ps1`).
- **All 0.1.0 honest constraints carry forward unchanged**
  (no production-grade MCP transport, no installer ecosystem,
  no full enterprise super-set, no hot reload, no full AST
  parser, no full rollback / delete coverage — Track F
  expanded coverage but not to full).

### Active work

None. No parallel track is currently open after Track F
closure. Phase 7 as a linear phase is not planned. Opening
the next parallel track is an explicit operator decision.

## 0.2.0 — Parallel Track D — Operator Credentials Hardening

This release closes **Parallel Track D — Operator Credentials
Hardening**, the fourth post-phase parallel track. Track D made the
operator credentials path less brittle by introducing a documented
`${ENV:NAME}` substitution form for argv elements inside
`onec_*_command_template`, render-time fail-closed semantics on
missing or malformed env tokens, password-position redaction in
`command_preview` and audit excerpts, operator-facing docs migrated
to the env-substitution default with literal cleartext kept as a
legacy fallback, and a narrow credential-template-hygiene heuristic
in `scripts/release/verify-release.ps1`. This is **not** an
enterprise security platform: no vault, no KMS, no SSO/RBAC, no OS
keychain, no encrypted-at-rest secrets file format. Six steps
total; production code was touched only at one boundary file
(`apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`)
and one release-side script (`scripts/release/verify-release.ps1`);
all other steps were documentation-only or aligned existing
operator-facing docs.

### Per-step outcomes

- **Step 1 (planning operator credentials hardening)** — two
  planning documents under `docs/architecture/track-d-*` (plan +
  step-map). No code changes.
- **Step 2 (credentials-flow audit and contract)** — two new
  documentation-only documents under `docs/architecture/`:
  `track-d-credentials-flow-audit.md` (where `/P "<password>"` is
  surfaced today, which payload fields see rendered argv, what
  "out-of-band" meant before Track D), and
  `track-d-credentials-contract.md` (formal contract for the
  `${ENV:NAME}` substitution syntax, render-time resolution
  order, fail-closed semantics, redaction discipline, backward
  compatibility with literal cleartext templates). No code
  changes.
- **Step 3 (env substitution and preview redaction)** —
  implementation in
  `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`:
  `_resolve_env_token(...)` resolves the full-element token
  `${ENV:NAME}` from the process environment at render time
  (after structural placeholder substitution); fail-closed on
  missing, empty, or partial / mixed forms (`ok=False`,
  `command_preview=None`, no subprocess started);
  `_redact_password_args(...)` replaces the argv element
  following `/P` or `/Pwd` (case-insensitive) with the sentinel
  `<redacted>` in `command_preview` and trimmed payload
  excerpts. The actual subprocess argv stays unredacted because
  the binary must authenticate. Literal cleartext templates
  remain supported as a legacy fallback. Registry invariant
  preserved: `read=15 / write=25 / intelligence=16`.
- **Step 4 (operator docs and migration alignment)** —
  operator-facing documentation migrated to the `${ENV:NAME}`
  form as the recommended default, with literal cleartext kept
  as a clearly marked legacy fallback. Three documents aligned:
  `docs/runbooks/track-a-reference-stand-round-trip.md` (product
  config example, env-substitution callout, failure mode F2
  extended to env-token failures, credentials-in-logs note
  updated), `SECURITY.md` (Honest constraints block rewritten
  under env-substitution), `docs/release-handoff.md` (Known
  limitations DESIGNER credentials bullet rewritten). No code
  changes.
- **Step 5 (release verify credential hygiene heuristic)** —
  eighth release-facing check **Credential template hygiene**
  added to `scripts/release/verify-release.ps1`. The check
  scans tracked `*.config.json` files (via `git ls-files`) for
  argv elements immediately following `"/P"` or `"/Pwd"`
  (case-insensitive) inside command-template arrays. Documented
  safe forms (`"${ENV:NAME}"`, `"<password>"`) pass; literal
  cleartext values emit `WARN` (not `FAIL`), naming file and
  line; empty values are not flagged. WARN does not change
  exit-code semantics, so legacy templates do not block the
  receive-side flow. `scripts/release/README.md` and
  `docs/release-handoff.md` updated to describe the eighth
  check and its narrow heuristic-not-DLP scope.
- **Step 6 (final integration pass and Track D closure)** —
  this closure: `pyproject.toml` version bumped 0.1.0 → 0.2.0;
  `README.md`, `PROJECT-STATUS.md`, and `CHANGELOG.md` aligned
  with Track D closed status. Read-only final integration
  check green: linear Step 1 → 6 history, all Step 1–5
  deliverables present on disk, registries `read=15 / write=25
  / intelligence=16` without drift, `verify-release.ps1` GREEN
  with eight checks, no real credentials anywhere in the
  diffs of the six Track D commits.

### Registry invariant carried into 0.2.0

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track D.

### Honest constraints update

- DESIGNER credentials remain operator-managed. The new
  **recommended path** is the `${ENV:NAME}` substitution form
  resolved at render time. Literal cleartext templates remain
  supported as a legacy fallback. The platform still does
  **not** ship a secrets manager, vault, KMS, OS keychain
  integration, or encrypted-at-rest secrets file format —
  operators feed env vars from their own secrets infrastructure
  if they need that.
- Check 8 is a narrow heuristic over tracked `*.config.json`
  files, not a full DLP scan. It does not parse 1С template
  semantics, does not scan runbooks or other documentation,
  and emits `WARN` (not `FAIL`).
- All other 0.1.0 honest constraints carry forward unchanged
  (single-version 1С smoke evidence on `8.3.27.1859`, no
  production-grade MCP transport, no installer ecosystem,
  no full enterprise super-set, no hot reload, no full AST
  parser, no full rollback / delete coverage).

### Parallel Track E follow-up — Multi-Version 1C Smoke Matrix (closure under 0.2.0)

After Track D closure, **Parallel Track E — Multi-Version 1C
Smoke Matrix** was opened as the fifth post-phase parallel
track and closed within the same `0.2.0` release line as a
documentation / scaffolding follow-up, **without** a minor
version bump (Q5 resolved: NO bump). Track E shipped no
functional delta — production code untouched throughout the
track, registries `read=15 / write=25 / intelligence=16`
without drift, no new MCP tools, no `1cv8.exe` runs at any
step. Six steps total.

#### Per-step outcomes

- **Step 1 (planning multi-version 1C smoke matrix)** — two
  planning documents under `docs/architecture/track-e-*` (plan
  + step-map). No code changes. Commit `1b233ce`.
- **Step 2 (current evidence audit and smoke scenario freeze)** —
  two new documentation-only documents:
  `track-e-current-evidence-audit.md` (descriptive — what is
  proven on reference `8.3.27.1859`, physical artifacts on
  disk, what is not yet evidenced, why single-version is
  insufficient; strict separation proven / inferred /
  not-yet-run / operator-supplied future inputs) and
  `track-e-smoke-scenario.md` (prescriptive **frozen** —
  scenario name `frozen-smoke-v1`, cut-down
  `create_dump_snapshot` via `/DumpConfigToFiles` only,
  principle-based version selection criteria,
  12-column matrix shape, PASS / FAIL / NOT RUN semantics,
  required evidence fields, Step 4 execution boundary).
  Commit `630f837`.
- **Step 3 (matrix scaffolding and operator runbook)** — two
  new operator-facing documents:
  `docs/runbooks/track-e-multi-version-smoke-matrix.md`
  (operator runbook for running `frozen-smoke-v1` on an
  operator-supplied 1С version) and
  `docs/version-support-matrix.md` (top-level evidence
  table with frozen 12-column shape; reference Row 1 for
  `8.3.27.1859` filled copy-only from existing Track A /
  Step 6 evidence, scenario field explicitly marked as
  `stronger-than-frozen-smoke-v1`; no fabricated additional
  rows). No `1cv8.exe` run. Commit `7c08cae`.
- **Step 4 (operator-driven smoke execution and matrix update)** —
  closed via **PATH B (honest operator-supplied gap)**. No
  `1cv8.exe` runs were executed; no additional evidence rows
  were added. Operator-side inventory found only the `8.3.27`
  minor family installed locally (builds `1859/x64` reference
  + `1936/x86` same-family disqualified per Step 2 §2.2);
  no `8.3.<other minor>` family was available; ENV-substitution
  credentials were not set in the work session. Per Track E
  plan Q4 + step-map Step 4, this is honest closure, not
  track failure. `docs/version-support-matrix.md` gained a
  closure note subsection enumerating the actual operator-side
  inventory and an explicit list of what Step 4 deliberately
  did not do (no run on same-family x86 build, no rerun of
  reference, no scenario expansion, no matrix contract
  changes, no fabricated rows, no real credentials).
  Commit `f962d78`.
- **Step 5 (support statement and docs alignment)** — five
  point-edits across three operator-facing docs to align
  wording with the actual Step 4 PATH B outcome: `SECURITY.md`
  (single-version evidence bullet renamed to "Single-version
  1С evidence (with multi-version scaffolding)" with pointer
  to matrix doc + Track E PATH B context + "no blanket
  multi-version support claim"), `docs/release-handoff.md`
  ("No multi-version 1С smoke matrix" Known limitations
  bullet rewritten as "Multi-version 1С smoke matrix —
  scaffolding only" with pointers and PATH B context;
  Single-version coverage bullet extended with matrix-doc
  pointer), `README.md` (Quickstart paragraph rewritten to
  remove stale "planning-only, Step 1" and broad
  "matrix из нескольких 1С версий" implication; "Куда идти
  дальше" navigation enriched with Track E runbook + matrix
  doc + Track E architecture mentions). Unified support
  statement now consistent across all three docs. Commit
  `78d5956`.
- **Step 6 (final integration pass and Track E closure)** —
  this closure: `README.md`, `PROJECT-STATUS.md`, and
  `CHANGELOG.md` aligned with Track E closed status. No
  `pyproject.toml` change (Q5 = NO; Track E without
  functional delta does not warrant a minor bump). Read-only
  final integration check green: linear Step 1 → 6 history,
  all Step 1–5 deliverables present on disk, registries
  without drift, `verify-release.ps1` GREEN on 8 checks, no
  real credentials anywhere in the six Track E commits.

#### Registry invariant carried through Track E

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track E.

#### Honest constraints update under Track E closure

- **Reference single-version evidence remains
  single-version.** Track E shipped scaffolding (frozen
  scenario + operator runbook + matrix-table doc) but did
  not extend the actual evidence breadth. The reference
  row in `docs/version-support-matrix.md` covers
  `8.3.27.1859` only; no additional version evidence rows
  were added.
- **No blanket multi-version support claim.** The platform
  remains multi-version-friendly architecturally (operator
  selects the binary path), but evidence-level claims are
  bounded by the reference row and the honest
  operator-supplied gap notation in the matrix doc.
- **`docs/version-support-matrix.md` is the single source
  of truth** for the actual evidence level. Post-closure
  additional evidence rows can be added through
  documentation-only updates against the matrix doc by
  following
  `docs/runbooks/track-e-multi-version-smoke-matrix.md`,
  without re-opening Track E.
- All other 0.2.0 honest constraints (DESIGNER credentials
  remain operator-managed via `${ENV:NAME}` substitution;
  Check 8 is a narrow heuristic, not full DLP) carry
  forward unchanged.
- All 0.1.0 honest constraints (no production-grade MCP
  transport, no installer ecosystem, no full enterprise
  super-set, no hot reload, no full AST parser, no full
  rollback / delete coverage) also carry forward
  unchanged.

### Active work (at the end of 0.2.0)

At the end of the 0.2.0 release line: Track E was opened and
closed within 0.2.0 as a documentation / scaffolding follow-up
without a minor version bump (Q5 = NO; no functional delta).
**Parallel Track F — Rollback Whitelist Expansion** was opened
afterwards and closed in 0.3.0 with a minor bump (Q5 = YES;
real production code change with functional delta — see
0.3.0 release notes above). Phase 7 as a linear phase remains
not planned. Opening the next parallel track is an explicit
operator decision.

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
- **Parallel Track C — Packaging & Installer Delivery** — closed on
  Step 6 (final integration pass and Track C closure). Six steps
  total; production code untouched throughout the track. Per-step
  outcomes:
  - Step 1 (planning) — two planning documents under
    `docs/architecture/track-c-*`.
  - Step 2 (release-facing verify path and layout polish) —
    `scripts/release/verify-release.ps1` as a read-only
    pre-handoff sanity check; updated `scripts/release/README.md`
    for the three-entrypoint surface (`install` / `verify` /
    `launch`).
  - Step 3 (packaging-facing install flow honest review) —
    inline block comment in `pyproject.toml` documenting why
    `[tool.hatch.build.targets.wheel] packages = []` is an
    intentional no-op (multi-app monorepo shape; install via
    `scripts/release/install.ps1`, not `pip install`); short
    "Packaging story" section in `scripts/release/README.md`.
  - Step 4 (release handoff documentation) — new
    `docs/release-handoff.md` for the receive-side operator:
    what you received, system prerequisites, reproducible
    install sequence, verify sequence, honest known
    limitations table.
  - Step 5 (integration and handoff polish) — minimal pointer
    to `docs/release-handoff.md` from the Quickstart "Куда
    идти дальше" navigation in this README.
  - Step 6 (final integration pass and Track C closure) — this
    closure: README + PROJECT-STATUS + CHANGELOG aligned with
    Track C closed status.

### Registry invariant carried into 0.1.0

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track A, Track B, or Track C.

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

### Active work (at the time of 0.1.0)

None. No parallel track was open at the time of the 0.1.0 release.
**Parallel Track D — Operator Credentials Hardening** was opened
afterwards and closed in 0.2.0; see the 0.2.0 release notes above.
