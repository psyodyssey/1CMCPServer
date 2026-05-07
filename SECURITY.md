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
- **Operator credentials are out-of-band.** DESIGNER user / password for
  live 1С infobases must be supplied by the operator at run time
  (e.g. environment variables, OS keychain, or local-only config files
  excluded from the repository via `.gitignore`). The platform does
  **not** ship a secrets manager.
- **No production-grade MCP transport yet.** The three MCP servers are
  intended for local / controlled use. There is no built-in
  authentication, authorisation, multi-tenant isolation, or hardened
  network transport. Treat them as you would any local development
  service.
- **Single-version 1С evidence.** Real binary-backed round-trip has been
  exercised on `8.3.27.1859`. Other versions are not yet covered.
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
