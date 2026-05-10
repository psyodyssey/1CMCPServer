# Security

## Reporting a vulnerability

If you discover a security issue in **1C Agent Platform**, please report it
**privately** to the project owner. Do not open a public issue or pull
request for security-sensitive findings until the report has been reviewed
and a remediation path has been agreed upon.

The platform is currently maintained by a small team. Expect a
human-paced response, not 24/7 SLA coverage.

## Honest constraints (current state)

These constraints are intentional and documented openly. They are **not**
hidden gaps.

- **Pre-1.0 software.** No backwards-compatibility guarantees across
  versions yet.
- **Operator credentials are operator-managed.** DESIGNER user /
  password for live 1С infobases are supplied by the operator at
  run time. The recommended path (Track D / Step 3) is the
  full-element token `${ENV:NAME}` inside any
  `onec_*_command_template` argv element, e.g.
  `"/P", "${ENV:ONEC_DESIGNER_PASSWORD}"`. The render layer
  resolves the token from the process environment; missing,
  empty, or partial / mixed forms are fail-closed
  (`ok=False`, `command_preview=None`, no subprocess started).
  Literal cleartext templates remain supported as a legacy
  fallback for backward compatibility but are **not** the
  recommended baseline. The `command_preview` field surfaced in
  payload data and the audit row's `details` redacts the argv
  element following `/P` / `/Pwd` (case-insensitive) to the
  sentinel `<redacted>`; the actual subprocess argv stays
  unredacted because the binary must authenticate. The platform
  does **not** ship a secrets manager / vault / KMS / OS keychain
  integration / encrypted-at-rest secrets file format. Operators
  who need any of those pull values into env vars from their own
  secrets infrastructure before invoking the platform.
- **Local stdio plus narrow HTTP+bearer transport baseline.** Two
  transports are now supported on each of the three MCP servers:
  - **`--transport stdio`** (default; Track G / Step 4) — line-
    delimited JSON-RPC 2.0 over stdin/stdout. Threat model =
    local trusted stdio boundary (operator-owned subprocess);
    auth is intentionally absent because the channel is not
    network-exposed.
  - **`--transport http`** (Track H / Step 4) — HTTP/1.1 single
    `/mcp` endpoint, POST only, `application/json`, 1 MiB body
    cap, line-delimited single JSON-RPC message per body, no
    SSE / batch / streaming. Authentication is **static bearer
    token** in the `Authorization` header (scheme accepted
    case-insensitively per RFC 6750; token compared byte-exactly
    via `hmac.compare_digest`). Tokens are declared either
    through `ProductConfig.auth.tokens` (each entry MUST be
    `${ENV:NAME}` env-substitution; literal cleartext rejected
    at config-load) or through the `--auth-token-env <VARNAME>`
    CLI flag (CLI wins, replace not merge). Missing `--bind`,
    missing token source, or unresolvable env var → fail-closed
    startup with a single operator-readable stderr line and no
    Python traceback. Token values are never logged in any form
    (no value, no length, no prefix, no suffix, no hash, no
    fingerprint).
  - Threat model for HTTP = **trusted-network deployment** behind
    an operator-owned reverse proxy that terminates TLS. The
    listener itself binds plain HTTP/1.1; in-process TLS is not
    provided. Operator SHOULD bind the listener to a loopback or
    private interface and front-proxy it. The single
    operator-facing single-source-of-truth recipe for this
    deployment shape — per-scenario MUST/SHOULD/MAY matrix
    (loopback / trusted private subnet / public-facing-through-
    reverse-proxy), explicit Forwarded-header MUST-NOT-consume
    policy, `/healthz` non-shipping, abstract nginx / Caddy
    snippets, and operator decision-point Q&A — is
    [`docs/operators/deployment-boundary.md`](docs/operators/deployment-boundary.md)
    (Track J / Step 4 deliverable; PATH A docs-only per Track J
    Step 3 contract).
  - **Still NOT shipped:** TLS / HTTPS termination in process,
    mTLS / client certificate authentication, JWT / OAuth 2.0 /
    OIDC / SAML / SCIM, RBAC / ABAC / per-tool ACL / per-tenant
    isolation, token rotation endpoint or refresh tokens, session
    cookies, rate limiting, WebSocket / Server-Sent Events / TCP
    / Unix domain socket / named pipe transports, supervisor
    daemon / systemd unit / Windows Service registration / hot
    reload, web UI / dashboard / observability stack. These are
    explicit Track H non-goals; subsequent post-Track-H tracks
    can address them. Track H does not claim production
    readiness for adversarial-internet deployment.
  - **Install fast path auth round-trip preserved (Track I /
    Step 4).** `apps/platform/src/onec_platform/installer.py:_config_to_dict`
    now emits the operator's `auth.tokens` declarations through
    the install fast path round-trip, symmetric to the existing
    Phase 6 / Step 8 enterprise-block emit-only-when-divergent
    pattern. Configs round-tripped through
    `scripts/release/install.ps1 ... -Confirm` preserve
    `auth.tokens` byte-identical to the source list (raw
    `${ENV:NAME}` strings remain raw configuration data, not
    resolved env values). Pre-Track-H configs without an `auth`
    section continue to round-trip byte-identical (no implicit
    `"auth": {}` injection). Resolution of `${ENV:NAME}` happens
    at server startup in `_network_transport._resolve_env_token`,
    not at install time. Broader installer / packaging /
    deployment ecosystem limitations remain (no `.msi` / `.deb`
    / signed distribution / GUI installer / wizard / PyPI
    publication / wheel publication beyond `[project.scripts]`;
    no service / supervisor registration; no enterprise-ready
    or hostile-network claim) — see "What is NOT in this
    handoff" / "Known limitations" sections in
    `docs/release-handoff.md` for the full carry-forward list.
- **Single-version 1С evidence (with multi-version scaffolding).** Real
  binary-backed round-trip evidence has been exercised on `8.3.27.1859`
  (Windows x64, file-based reference stand) — see Track A / Step 6 in
  `PROJECT-STATUS.md`. Track E (Multi-Version 1C Smoke Matrix) ship'ит
  scaffolding для extension этой базы: frozen smoke scenario
  (`frozen-smoke-v1`), operator runbook, и matrix-table doc
  ([`docs/version-support-matrix.md`](docs/version-support-matrix.md)).
  На момент Track E / Step 4 closure additional version evidence rows
  не были добавлены — Step 4 закрыт через honest operator-supplied gap
  (отсутствие на operator machine 1С minor families помимо `8.3.27`).
  Additional rows могут быть добавлены post-closure через operator-driven
  runs по `docs/runbooks/track-e-multi-version-smoke-matrix.md`. Никакого
  blanket multi-version support claim не делается.
- **No installer ecosystem.** No `.msi` / `.deb` / GUI wizard / signed
  binary distribution. The install fast path operates on a declarative
  product config and a Python entry point.
- **Limited rollback coverage.** Automatic rollback is whitelisted to a
  small, deliberate set of write tools. See
  `docs/architecture/track-a-real-write-path-plan.md` and
  `PROJECT-STATUS.md` for the full list of honest constraints.

## Safety guarantees the platform DOES carry

These are invariants enforced by code and reviewed every time the
relevant area is touched.

- **Single mutating path.** All write operations go through
  `run_write_flow` (preflight → snapshot → operation → verify → audit).
  No back-door write channel from the product layer.
- **Read-only intelligence layer.** `mcp-intelligence-server` does not
  import `onec_policy_engine`, does not call `run_write_flow`, does not
  write to disk.
- **No `shell=True`.** All subprocess invocations use argv-list form.
- **Append-only audit log.** Audit records are never rewritten.
- **Fail-closed defaults.** Unknown placeholders, missing prerequisites,
  or unhealthy environments cause honest `ok=False` results, not silent
  fallbacks.

## What to include in a security report

- A short description of the issue.
- Reproduction steps, or a minimal example.
- The version (`pyproject.toml`) and 1С platform version (if relevant)
  on which it was observed.
- Whether you intend to disclose publicly, and on what timeline.

Thank you for taking the time to report responsibly.
