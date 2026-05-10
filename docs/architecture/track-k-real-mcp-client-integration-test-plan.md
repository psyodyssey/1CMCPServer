# Track K — Real MCP Client Integration Test (Plan)

> **Status.** Track K / Step 1 — **planning, docs-only**.
> No code changes; no `pyproject.toml` change; no
> `scripts/*` change; no operator-facing doc edits; no
> registry change; no new MCP tools; no `1cv8.exe` runs;
> no remote push. This document opens the eleventh
> post-phase parallel track and pins its scope, guard-
> rails, acceptance criteria, and Q1–Q7 directional
> defaults. Step 2 (baseline audit) is the next opening
> and is **NOT** opened in this commit.

> **Authoritative version pin (read-time grounding).**
> `pyproject.toml` `version = 0.5.1` (preserved through
> Track J closure at commit `dd86261`). Registry
> invariants `read = 15 / write = 25 / intelligence =
> 16` carried through into Track K opening. HEAD before
> this commit = `dd86261`.

---

## 1. Purpose / why the track exists

Track K formalizes one specific honest gap that
remained explicitly flagged after the closure of every
prior MCP-transport track (Tracks G / H / I) and was
restated in Track J's final closure recommendations:

> The project has stdlib-level smoke and internal
> verification, but **no real MCP-client-facing
> end-to-end proof**. No closure of any prior track
> demonstrated that an unmodified, third-party (or
> minimum-viable real-client-compatible) MCP client
> could (a) connect to one of the three MCP servers via
> either supported transport (`stdio` or `http`),
> (b) negotiate `initialize`, (c) list tools, and
> (d) invoke at least one read-only tool, observing
> well-formed responses end-to-end.

Track G / Step 6 closure narrative, Track H / Step 6
closure narrative, and Track J Step 4 recipe §6 all
explicitly acknowledge this gap as honest constraint —
not a hidden defect, but a known unverified surface.

Track K's mandate is to convert that honest gap into a
disciplined six-step deliverable: planning → audit →
contract → narrow implementation (only if needed) →
docs alignment → closure. Track K does **not** add new
MCP tools, redesign existing transports, change
registries, or expand into adjacent territories.

## 2. Current post-Track-J baseline

The platform after Track J closure (commit `dd86261`)
ships:

- **Three MCP servers** with stable registries: `read =
  15 / write = 25 / intelligence = 16`. Tool surface
  byte-identical from Phase 4 closure onward.
- **Two transports** per server (Track G / Track H):
  - `--transport stdio` (default; line-delimited JSON-
    RPC 2.0 over stdin/stdout; trusted-local-subprocess
    threat model; no auth).
  - `--transport http` (HTTP/1.1 `/mcp` POST-only;
    bearer auth with failure-equivalence + redaction
    discipline; 1 MiB body cap; non-`/mcp` returns 404;
    trusted-internal-network behind operator-owned
    reverse proxy threat model).
- **CLI surface per server.** `--config-path`,
  `--transport {stdio,http}`, `--log-level`, `--bind`
  (HTTP), `--auth-token-env` (HTTP). Three
  `[project.scripts]` console entries
  (`mcp-read-server`, `mcp-write-server`,
  `mcp-intelligence-server`).
- **Install fast path** via `scripts/release/install.ps1`
  with auth round-trip integrity (Track I / Step 4).
- **Operator-facing deployment-boundary recipe** at
  [`docs/operators/deployment-boundary.md`](../operators/deployment-boundary.md)
  (Track J / Step 4).
- **Selfcheck** at `scripts/dev/selfcheck.py` exercises
  every internal package import + prints registry
  counts and `selfcheck_status`. This is **not** an MCP
  client.
- **Release verify** at `scripts/release/verify-release.ps1`
  exercises eight repo-level invariants. This is also
  **not** an MCP client.

What the platform does **not** ship today:

- Any real-MCP-client harness exercising `--transport
  stdio` end-to-end.
- Any real-MCP-client harness exercising `--transport
  http` end-to-end (the bearer-auth path, the
  `/mcp` POST endpoint, the JSON-RPC 2.0 envelope, the
  `tools/list` + `tools/call` round-trip).
- Any documented "what counts as MCP client end-to-end
  proof" closure-gate definition.
- Any runbook for a third-party operator to verify on
  their own machine that the platform speaks the MCP
  protocol correctly.

## 3. Honest gap statement

The gap is **not** "the runtime is broken" — the
runtime has been exercised through stdlib-level smoke
(import every package; iterate registry; invoke
tool callables in-process) at every track closure, and
the HTTP transport has been exercised through unit-test
shape (status-code paths, JSON envelope shapes,
failure-equivalence). The gap is that **no MCP-protocol-
compliant client** has been demonstrated to interoperate
with the platform end-to-end at any closure gate.

This matters because:

- **Protocol-shape drift is invisible to stdlib smoke.**
  The platform's `_handle_request` switch on `method`
  ("initialize" / "tools/list" / "tools/call" / etc.) is
  written against the MCP specification, but no
  client-side conformance check has been demonstrated.
  A real MCP client may negotiate fields the platform
  silently ignores, or expect response shapes the
  platform returns differently.
- **Operator confidence is incomplete.** An operator
  installing the platform today can run `selfcheck` and
  `verify-release` and confirm the project's internal
  invariants. They cannot today run a documented "point
  Claude Desktop / mcp-cli / equivalent at this and
  watch tools/list succeed" smoke that proves the MCP
  half of the contract.
- **The "MCP" in "1C Agent Platform MCP" is
  unverified end-to-end.** Track G / Step 4 (commit
  message) and Track H / Step 4 closure explicitly
  acknowledge this. Track J Step 2 audit confirmed the
  carry-forward.

The gap is therefore **real, honest, and well-scoped**.
Track K addresses it without expanding into adjacent
territories.

## 4. Why this is not redundant with existing smoke

The platform's existing smoke surfaces are:

- **`scripts/dev/selfcheck.py`** — imports every
  internal package, iterates registries, prints
  `selfcheck_status=ok`. **Not an MCP client.** Does
  not exercise `_stdio_transport._serve_stdio` or
  `_network_transport._serve_http`. Does not speak
  JSON-RPC 2.0 over any wire. Does not validate
  `initialize` / `tools/list` / `tools/call` envelope
  shapes against an external client.
- **`scripts/release/verify-release.ps1`** — eight
  repo-level invariants (layout, entrypoints,
  important docs, working tree, git baseline,
  selfcheck, credential leak guard, credential
  template hygiene). **Not an MCP client.** Does not
  start the MCP servers.
- **Internal unit-shape paths** in
  `_stdio_transport.py` and `_network_transport.py`
  (e.g., `_handle_request`, `_auth_header_passes`,
  `_make_error`). Exercised only indirectly via
  Phase 1–6 + Track G/H/I development; no test suite
  ships with the project (see Track C / Step 3 honest
  constraint).

None of these would catch the class of failure Track K
targets: real-client protocol-shape interoperability.
The runtime might be locally consistent but spec-
divergent in ways only a real client would observe.

## 5. Goal of the track

**Primary goal.** Produce a single end-to-end-runnable
artefact (operator-runnable, abstract-placeholder-
compatible, no real credentials, no real hostnames)
that demonstrates a real MCP client connecting to one
of the three MCP servers, completing `initialize`,
`tools/list`, and at least one `tools/call` (read-only
tool from `mcp-read-server`), observing well-formed
JSON-RPC 2.0 responses.

**Secondary goal.** Document in a Track K closure-gate
contract what counts as "real MCP client end-to-end
proof" so that future tracks (or operator-driven
verification on their own machine) have a fixed
target rather than a moving expectation.

**Tertiary goal (non-commitment).** If the Step 4
implementation lands a runnable harness that operators
can replay, document its operator-facing invocation
in a Step 5 alignment. The harness must remain
abstract-placeholder-compatible and **not** include
any real bearer token / hostname / certificate /
internal IP.

## 6. What is in scope

- **Planning** (Step 1, this document + step-map).
- **Baseline audit of current client-integration gap**
  (Step 2) — descriptive inventory of what exists
  today (stdlib smoke, unit-shape paths, recipe doc,
  manuals) vs what real-MCP-client end-to-end proof
  would require; categorical breakdown (already
  covered / adjacent insufficient / clearly missing /
  explicitly out-of-scope).
- **Normative closure-gate contract** (Step 3) — what
  counts as honest end-to-end MCP-client proof
  (acceptance criteria, allowed client classes,
  required round-trip envelope, transport coverage,
  honesty rules: no real credentials, no real
  hostnames, abstract placeholders only).
- **Narrow implementation / harness slice** (Step 4,
  only if Step 3 contract requires it) — the only
  possible code or runnable-script step. Step 3
  decides whether Step 4 is docs-only, narrow runnable
  harness (e.g., a single new script under
  `scripts/dev/` or a single new `examples/mcp-client-
  smoke/` directory), or hybrid.
- **Docs / operator / release alignment** (Step 5) —
  narrow update of operator-facing surfaces to point
  at the Step 4 deliverable (if Step 4 shipped a
  runnable harness, document its invocation; if
  docs-only, point at the Step 3 contract from the
  appropriate operator-facing locations).
- **Final integration pass + closure** (Step 6) — Q7
  versioning decision, README / PROJECT-STATUS /
  CHANGELOG closure narrative, Track K full closure.
- **Exercise of current `stdio` and/or `http` surfaces**
  through a real MCP client or minimum-viable
  real-client-compatible harness. **Compatibility
  preserved** with existing Track G / H / I / J
  truths: no new MCP tools, no registry change, no
  transport redesign, no auth-scheme change, no
  deployment-boundary redesign.

## 7. What is out of scope

Track K **MUST NOT** widen into the following
adjacent territories, **even if** they would help
the Step 4 harness:

- **No new MCP tools.** Registry invariant `read = 15 /
  write = 25 / intelligence = 16` carried through
  byte-identical.
- **No registry counts change.**
- **No redesign of `_stdio_transport.py`,
  `_network_transport.py`, `installer.py`, or any
  Phase 1–6 / Track A–J production-code surface.**
  Track K exercises existing surfaces; it does not
  redesign them.
- **No new transport family** (no WebSocket / SSE /
  TCP / Unix-socket / named-pipe / TLS-in-process /
  mTLS / OAuth / OIDC / SAML / JWT / SCIM).
- **No auth-scheme change.** Bearer + failure-
  equivalence + redaction discipline preserved
  byte-identical.
- **No deployment-boundary redesign** (Track J §13
  carry-forward unchanged).
- **No service-supervisor work** (systemd / Windows
  Service / launchd / hot reload / restart watcher /
  auto-update).
- **No packaging ecosystem work** (`.msi` / `.deb` /
  signed distribution / GUI installer / wizard /
  PyPI publication / wheel publication beyond
  `[project.scripts]`).
- **No enterprise identity stack** (SSO / SAML / OIDC
  / SCIM / RBAC / ABAC / per-tool ACL / per-tenant
  isolation / multi-tenant identity / token rotation
  endpoint / refresh tokens / session cookies).
- **No observability stack** (OpenTelemetry / Jaeger
  / Prometheus / OpenMetrics / log aggregation /
  distributed tracing / metric emission).
- **No web UI / dashboard frontend.**
- **No `1cv8.exe` work.** Track K operates on MCP
  client / transport layer, not on 1cv8 binary
  surface. Real-stand round-trips remain Track A
  / Track E territory.
- **No multi-version 1C matrix expansion** (Track E
  follow-up; orthogonal).
- **No rollback whitelist expansion / AST work**
  (Track F / Track A follow-ups; orthogonal).
- **No `pyproject.toml` change** unless Step 3
  contract pins a SemVer bump in Step 6 (default
  expectation = NO-BUMP or PATCH; never MINOR /
  MAJOR unless Step 4 ships net-new external
  capability, which §9 / §10 below should not
  authorize).
- **No `SECURITY.md` / `docs/release-handoff.md` /
  `apps/platform/README.md` / `CHANGELOG.md` /
  `manuals` rewrite.** Step 5 alignment is narrow
  CLASS-1 only.
- **No real credentials anywhere.** No real bearer
  tokens, real env-var values, real hostnames, real
  certificates, real internal IPs in any Track K
  step's commits.
- **No remote push.** GitHub push is operator action;
  not part of any Track K step.

## 8. Guardrails

Hard invariants Track K **MUST** carry through every
step:

1. Registry invariant `read = 15 / write = 25 /
   intelligence = 16` carried through unchanged.
2. No new MCP tools.
3. Track G stdio runtime byte-identical
   (`_stdio_transport.py` untouched).
4. Track H HTTP runtime byte-identical
   (`_network_transport.py` untouched at Step 4 unless
   Step 3 contract justifies a ≤15 LOC narrow
   addition; default expectation = untouched).
5. Track I installer auth round-trip integrity byte-
   identical (`installer.py` untouched).
6. Track J §13 / §6 / §7 carry-forward unchanged
   (in-process TLS forbidden; mTLS forbidden;
   Forwarded-header MUST-NOT-consume policy;
   per-scenario MUST/SHOULD/MAY matrix; `/healthz`
   not shipped).
7. No `pyproject.toml` change in Step 1 / 2 / 3 /
   Step 4 (if docs-only) / Step 5. Step 6 may bump
   per Q7 default (NO-BUMP preferred; PATCH
   `0.5.1 → 0.5.2` only if Step 4 shipped a defect-
   class fix; never MINOR / MAJOR).
8. No `scripts/*` change in Step 1 / 2 / 3 / Step 5 /
   Step 6. Step 4 may add a single new runnable
   harness file under `scripts/dev/` **or** under
   `examples/mcp-client-smoke/` (Step 3 decides
   location) — but only if Step 3 contract
   explicitly authorizes it.
9. No `1cv8.exe` runs in any Track K step.
10. No real credentials in any committed text.
11. No remote push in any Track K step.
12. No premature Track K closure language in any
    Step 1–5 commit.
13. No false implementation claims. Step 4 deliverable
    (if it ships runnable harness) **MUST** be
    demonstrably runnable, not aspirational.

## 9. Acceptance criteria for eventual closure

Track K is considered honestly closed when **all** of
the following hold simultaneously:

1. Plan + step-map + audit + contract on disk as
   separate commits (Steps 1 / 2 / 3).
2. Step 4 deliverable on disk: either explicit
   docs-only operationalization, or one narrow new
   harness file (location pinned by Step 3 contract).
3. Real-MCP-client end-to-end proof has been
   demonstrated against at least one of the three
   MCP servers (read / write / intelligence) on at
   least one transport (`stdio` or `http`). Demonstrated
   = the harness runs locally and produces well-formed
   JSON-RPC 2.0 responses for `initialize`,
   `tools/list`, and at least one read-only
   `tools/call`. Demonstration may be operator-side
   (commit message records the evidence) or harness-
   side (Step 4 deliverable is itself the runnable
   evidence).
4. Step 3 contract explicitly decides whether
   "demonstrated against one server on one transport"
   is the closure gate, or whether two transports /
   two servers / two clients are required. (Default
   recommendation: one server + one transport is
   sufficient for honest closure; broader matrices
   are recommended-only, not closure-gate. Subject to
   Step 3 review.)
5. Step 5 alignment of operator-facing surfaces
   updates the recipe / handoff / README to point at
   the Step 4 deliverable.
6. Step 6 final integration pass: Q7 decision (NO-BUMP
   / PATCH) explicitly defended; README / PROJECT-
   STATUS / CHANGELOG closure narrative; track moved
   to Closed parallel tracks list.
7. Registries `read = 15 / write = 25 / intelligence
   = 16` invariant carried through all six Track K
   steps.
8. No new MCP tools added in any step.
9. No production code surface changed in any step
   beyond the narrow Step 4 harness file (if Step 3
   contract authorizes it).
10. No `1cv8.exe` runs in any step.
11. No real credentials in any committed text.

## 10. Honest constraints after closure

Even after Track K closure, the following remain
honest constraints (carry-forward from prior tracks):

- **No hostile-internet readiness.** Real-MCP-client
  proof exercises the supported deployment shape
  only (trusted-local-stdio or trusted-internal-
  network-behind-reverse-proxy). Track K does not
  validate hostile-internet exposure.
- **No enterprise identity stack.** Bearer auth
  remains the only authentication signal; Track K
  exercises bearer auth from a real client's
  perspective, but does not add JWT / OAuth / OIDC /
  SAML / SCIM / RBAC / ABAC / per-tenant.
- **No multi-tenant.** One bearer-token list per
  process; Track K does not change this.
- **No `/healthz` endpoint.** Track J §8 defer
  carried forward.
- **No in-process TLS / mTLS.** Track H §13.1 / §13.3
  / Track J §5 carried forward.
- **No service supervision.** Track K does not
  daemonize, supervise, or auto-restart the MCP
  servers; harness invocations are foreground
  operator commands.
- **No packaging ecosystem.** Wheel build stays empty
  (Track C honest constraint); harness, if shipped,
  remains runnable via documented
  `python -m mcp_<server>` or equivalent.
- **No web UI.**
- **No observability stack.**
- **Honest threat model carried forward** from
  Track J §4: trusted-internal-network HTTP MCP
  listener with static bearer authentication,
  fronted by an operator-owned reverse proxy that
  terminates TLS. Not hostile-internet ready. Not
  enterprise-identity ready. Not multi-tenant. Not
  load-balanced. Not observed. Not supervised.

## 11. Relationship to Tracks G / H / I / J

| Track | Closed at | What Track K assumes from it (byte-identical carry-forward) |
|---|---|---|
| Track G — Production-Grade MCP Transport and CLI | `0.4.0` MINOR bump | `_stdio_transport.py` runtime; three `__main__.py` entrypoints; `--config-path` / `--transport` / `--log-level` flags; `[project.scripts]` block. |
| Track H — Network-Grade MCP Transport and Authentication Boundary | `0.5.0` MINOR bump | `_network_transport.py` runtime; HTTP `/mcp` POST endpoint; bearer auth + failure-equivalence + redaction; `--bind` + `--auth-token-env` flags; §10 / §13 contract. |
| Track I — Installer Auth Round-Trip Integrity | `0.5.1` PATCH bump | `installer.py:_config_to_dict` auth emit branch; round-trip preservation byte-identical. |
| Track J — TLS and Reverse-Proxy Deployment Boundary | NO-BUMP under `0.5.1` | Deployment-boundary contract (§4 / §5 / §6 / §7 / §8); operator-facing recipe at `docs/operators/deployment-boundary.md`; per-scenario MUST/SHOULD/MAY matrix; Forwarded-header MUST-NOT-consume policy; `/healthz` defer; PATH A docs-only precedent. |

Track K builds **on top of** these — it does not
modify any of them. The Step 4 harness (if shipped)
exercises the surfaces Tracks G / H / I / J already
ship; it does not invent new transports, auth schemes,
or deployment surfaces.

## 12. Open questions Q1–Q7 (directional defaults only)

These are **directional recommendations** for Step 2
(audit) and Step 3 (contract) to resolve. They are
**not** normative; they capture the planning view at
Step 1 opening.

### Q1 — What counts as "real MCP client"?

**Directional default.** A real MCP client is any
process that speaks the MCP protocol (JSON-RPC 2.0
envelope + the MCP method set including `initialize`,
`tools/list`, `tools/call`, etc.) externally to the
server process. Three candidate classes:

- **Class A — Third-party real client** (e.g., Claude
  Desktop, MCP CLI, `mcp-cli` tool, equivalents). Most
  authentic; cannot be redistributed inside this repo;
  operator-side demonstration. Commit messages would
  record evidence.
- **Class B — Minimum-viable real-client-compatible
  harness** shipped as a single new script in the repo
  (e.g., `scripts/dev/mcp_client_smoke.py` or
  `examples/mcp-client-smoke/run.py`). Operator-runnable;
  byte-replayable; serves as Track K's closure
  evidence.
- **Class C — Both A and B.** Step 4 ships harness
  (B); Step 6 closure records optional third-party
  verification (A) as recommended-only.

**Step 1 directional recommendation.** Class B (or
Class C with Class B as closure gate and Class A as
recommended). Class A alone is not honest closure
because operator-side verification is not byte-
replayable from the repo.

### Q2 — Stdio only, or HTTP also?

**Directional default.** Stdio is the easier-and-
default transport (no bind, no auth, no reverse
proxy). HTTP exercises the bearer-auth path and is
where most operator deployment risk lives.

- **Q2 option A — stdio only.** Cheapest. Honest
  closure gate. HTTP remains documented-but-
  unverified-by-Track-K. Closure narrative
  acknowledges this carry-forward.
- **Q2 option B — stdio + HTTP.** Best coverage.
  HTTP harness needs bearer token (env-var
  placeholder; no real credential committed).
  Cost: doubled harness scope.
- **Q2 option C — HTTP only.** Strange — leaves
  stdio (the default!) unverified.

**Step 1 directional recommendation.** Option B
(stdio + HTTP). Both surfaces matter; the cost of
covering both is small once a working harness for
either exists. Subject to Step 3 contract review:
if Step 2 audit reveals one surface is materially
harder to exercise honestly without operator-side
infrastructure, Step 3 may downgrade to Option A.

### Q3 — Claude Desktop / `mcp-cli` / minimum-viable harness?

**Directional default.** Minimum-viable real-client-
compatible harness (Q1 Class B). Claude Desktop /
`mcp-cli` are valid recommended-only options to
document in Step 5, but not the closure gate.
Reasoning: third-party tools introduce external
dependency on the operator's machine; the harness in
the repo is byte-replayable and survives third-party
client changes.

### Q4 — One client or two for closure gate?

**Directional default.** One client (the minimum-
viable harness from Q1 / Q3). Multiple clients are
recommended-only. Closure gate at one is the narrowest
honest framing; broader matrices are scope creep.

### Q5 — Does this track likely need code, or is harness possible as docs-only?

**Directional default.** This track most likely
needs a small amount of code — but the code is a new
script file, not a modification to existing
production code. Specifically:

- **Most likely Step 4 outcome.** One new file:
  `scripts/dev/mcp_client_smoke.py` **OR**
  `examples/mcp-client-smoke/run.py`. Stdlib-only
  (`socket`, `json`, `urllib.parse`, `subprocess`,
  `argparse`, `os`, `sys`). No new runtime
  dependency. ≤300 LOC soft cap.
- **Less likely.** Docs-only Step 4 with operator-
  side verification recorded in the commit message.
- **Even less likely / forbidden.** Modifying
  `_stdio_transport.py` / `_network_transport.py`
  / `installer.py` / any other production code.
  Track K **MUST NOT** do this.

Final decision = Step 3 contract.

### Q6 — Should `pyproject` / `scripts/*` stay out of scope?

**Directional default.** `pyproject.toml` stays
untouched in Step 1 / 2 / 3 / Step 5. Step 6 may
bump per Q7 below. `scripts/*` stays untouched in
Step 1 / 2 / 3 / Step 5 / Step 6; the **only**
permitted change is Step 4 adding one new file
under `scripts/dev/` (if Step 3 contract chooses
that location). Existing `scripts/*` content stays
byte-identical.

### Q7 — Likely SemVer bump at Step 6 closure?

**Directional default.** NO-BUMP preferred. PATCH
`0.5.1 → 0.5.2` only if Step 4 ships a defect-class
fix observable by end-users (which it is not
expected to). MINOR `0.5.1 → 0.6.0` only if Step 4
ships net-new external capability that consumers of
`pyproject.toml`-version-pinning would observe — and
the track's stated scope discipline argues against
this.

| Step 4 outcome | Q7 default |
|---|---|
| Docs-only operationalization | **NO-BUMP** |
| New stdlib-only harness script under `scripts/dev/` or `examples/` | **NO-BUMP** (a runnable diagnostic tool that exercises existing surfaces is not consumer-visible capability) |
| Modification to existing production code | **PATCH** if defect-class; otherwise rethink track scope |
| Net-new external capability (new transport / new auth / new endpoint) | Forbidden by §7; track scope error |

Final decision = Step 6 closure.

## 13. Step trajectory preview

| Step | Type | Default expectation |
|---|---|---|
| **Step 1** (this commit) | planning | 2 new architecture docs + README / PROJECT-STATUS active-track flip. No code. No registry change. |
| **Step 2** | descriptive baseline audit (docs-only) | 1 new architecture doc inventorying current client-integration gap surfaces; Q1–Q7 directional resolutions. No code. |
| **Step 3** | normative contract (docs-only) | 1 new architecture doc pinning closure-gate definition, allowed client class, transport coverage, Step 4 file surface. PATH A vs PATH B selection. |
| **Step 4** | narrow harness implementation **or** docs-only operationalization | Either 1 new harness file (default: `scripts/dev/mcp_client_smoke.py` or `examples/mcp-client-smoke/run.py`) or 1 new operator-facing demonstration doc. No modification to existing production code. |
| **Step 5** | docs / operator / release alignment | Narrow CLASS-1 edits to README / SECURITY / release-handoff / recipe to point at Step 4 deliverable. Track K still active at Step 5. |
| **Step 6** | closure | README Closed-tracks list extended десять → одиннадцать; PROJECT-STATUS Track K closure section; CHANGELOG Track K subsection; Q7 SemVer decision (default = NO-BUMP). |

No step (1 / 2 / 3 / 4 / 5 / 6) touches production
code in `apps/*/src/` or `packages/*/src/` beyond
adding one possible new stand-alone harness file at
Step 4 (Step 3 decides).

---

## 14. Honest summary

Track K opens a narrow, documentation-first track to
close the "no real MCP client integration proof"
honest gap that has been carried forward through every
prior MCP-transport-track closure (Tracks G / H / I /
J). Step 1 ships only two planning documents (this
file + step-map). Step 2 (descriptive baseline audit)
is the next opening and is **NOT** opened in this
commit. Track K's scope is deliberately narrow: no new
MCP tools; no registry change; no transport redesign;
no auth-scheme change; no deployment-boundary
redesign; no `1cv8` work; no `pyproject.toml` change
until Step 6 Q7 (default NO-BUMP); no
`SECURITY.md` / `docs/release-handoff.md` /
`apps/platform/README.md` / `CHANGELOG.md` rewrite
until Step 5 (narrow CLASS-1 only); no real
credentials anywhere; no remote push.

The Step 4 design question — docs-only vs narrow
new-harness-file vs both — remains **explicitly open**
and is resolved by Step 3 contract on the basis of
Step 2 audit evidence. Step 1 directional
recommendation is harness-shipped (PATH B), but
Step 1 does **not** lock this.
