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
- **No production-grade MCP transport yet.** The three MCP servers are
  intended for local / controlled use. There is no built-in
  authentication, authorisation, multi-tenant isolation, or hardened
  network transport. Treat them as you would any local development
  service.
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
