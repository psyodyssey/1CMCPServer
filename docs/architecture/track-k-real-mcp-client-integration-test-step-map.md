# Track K — Real MCP Client Integration Test (Step Map)

> **Companion to** `track-k-real-mcp-client-integration-test-plan.md`.
> This document fixes the six-step trajectory for
> Track K, with per-step Goal / What changes / What
> does NOT change / Result. It also pins the track
> invariants that **MUST** carry through every step.
>
> **Status.** Track K / Step 1 — planning-only. Step 2
> is the next opening and **NOT** opened in this
> commit.

---

## Track invariants (carried through every step)

These invariants are **hard constraints** that every
Track K step (1 / 2 / 3 / 4 / 5 / 6) **MUST**
preserve:

1. **Registry counts** `read = 15 / write = 25 /
   intelligence = 16` carried through byte-identical.
   No new MCP tools at any step.
2. **Track G stdio runtime byte-identical.**
   `packages/mcp-common/src/mcp_common/_stdio_transport.py`
   untouched at every step.
3. **Track H HTTP runtime byte-identical.**
   `packages/mcp-common/src/mcp_common/_network_transport.py`
   untouched at every step.
4. **Track I installer auth round-trip integrity
   byte-identical.**
   `apps/platform/src/onec_platform/installer.py`
   untouched at every step.
5. **Three `__main__.py` entrypoints byte-identical.**
   `apps/mcp-{read,write,intelligence}-server/src/mcp_{read,write,intelligence}_server/__main__.py`
   untouched at every step.
6. **Track J §13 / §6 / §7 / §8 carry-forward.**
   No in-process TLS introduced; no mTLS introduced;
   Forwarded-header MUST-NOT-consume policy preserved;
   per-scenario MUST/SHOULD/MAY matrix preserved;
   `/healthz` not shipped.
7. **No `pyproject.toml` change** in Steps 1 / 2 / 3
   / Step 5. Step 4 **MUST NOT** change
   `pyproject.toml` (the harness, if shipped, is
   stdlib-only and does not add `[project.dependencies]`).
   Step 6 **MAY** bump per Q7 (default = NO-BUMP).
8. **No `scripts/*` modification.** Existing scripts
   stay byte-identical at every step. Step 4 **MAY**
   add at most one new file under `scripts/dev/`
   **OR** `examples/mcp-client-smoke/` (Step 3
   contract chooses location), but **MUST NOT**
   modify any existing `scripts/*` file.
9. **No new MCP tools at any step.**
10. **No registry drift at any step.** Selfcheck
    `selfcheck_status=ok` and registry counts at
    every step.
11. **No `1cv8.exe` runs at any step.** Track K
    operates on MCP client / transport layer; not on
    1cv8 binary surface.
12. **No remote push at any step.** Operator action;
    not part of Track K.
13. **No real credentials at any step.** No real
    bearer tokens, env-var values, hostnames,
    certificates, internal IPs in committed text.
    All examples / harness placeholders use abstract
    placeholders (`<BEARER_TOKEN>` or
    `<TOKEN_ENV_VARNAME>`, `<HOST>:<PORT>`, etc.).
14. **No premature Track K closure language** in
    Step 1 / 2 / 3 / 4 / 5 commits.
15. **No false implementation claims** in any step's
    deliverables. If Step 4 ships a runnable harness,
    it **MUST** demonstrably run; if Step 4 is
    docs-only, the deliverable **MUST NOT** describe
    behaviour as shipped.

---

## Hard out-of-scope list (carried through every step)

Track K **MUST NOT** widen into any of these at any
step:

- New transport family (WebSocket / SSE / TCP /
  Unix-socket / named-pipe / TLS-in-process / mTLS).
- New auth scheme (JWT / OAuth 2.0 / OIDC / SAML /
  SCIM / token rotation / refresh tokens / session
  cookies).
- RBAC / ABAC / per-tool ACL / per-tenant isolation
  / multi-tenant.
- Rate limiting / WAF / IDS / DDoS protection /
  anomaly detection.
- Service supervision (systemd / Windows Service /
  launchd / hot reload / restart watcher / auto-
  update).
- Packaging ecosystem (`.msi` / `.deb` / signed
  distribution / GUI installer / wizard / PyPI
  publication / wheel publication beyond
  `[project.scripts]`).
- Web UI / dashboard frontend.
- Observability stack (OpenTelemetry / Jaeger /
  Prometheus / OpenMetrics / log aggregation /
  distributed tracing / metric emission).
- Standalone `apps/platform` entrypoint.
- `/healthz` / `/readyz` / `/livez` endpoint.
- Reverse-proxy redesign (Track J §13 carry-forward).
- `1cv8` work.
- Multi-version 1С matrix expansion (orthogonal —
  Track E follow-up).
- Rollback whitelist expansion / AST work
  (orthogonal — Track F / Track A follow-ups).
- New MCP tools / registry change.

---

## Step 1 — planning real MCP client integration test (THIS STEP)

**Goal.** Open Track K with planning documents only.
Pin scope, guardrails, acceptance criteria, Q1–Q7
directional defaults. Flip README / PROJECT-STATUS
active-track state from "no active track" to
"Track K / Step 1 active planning-only". Do **not**
open Step 2 in the same commit.

**What changes.** Exactly four files:

1. `docs/architecture/track-k-real-mcp-client-integration-test-plan.md`
   (new — the companion plan doc).
2. `docs/architecture/track-k-real-mcp-client-integration-test-step-map.md`
   (this file, new).
3. `README.md` (modified — Quickstart paragraph
   flipped from "Активного трека сейчас нет" to
   "Активный трек сейчас — Parallel Track K"; Active
   parallel track section reopened describing
   Track K at Step 1 only).
4. `PROJECT-STATUS.md` (modified — header flipped
   from "Активного шага нет" to "Parallel Track K /
   Step 1 — planning ... (in progress)"; new per-
   step "Parallel Track K / Step 1 — planning real
   MCP client integration test (завершён)" section
   added below the Track J Step 6 closure section).

**What does NOT change.** Production code; `pyproject.toml`;
`scripts/*`; `SECURITY.md`; `docs/release-handoff.md`;
`apps/platform/README.md`; manuals; `CHANGELOG.md`;
Closed parallel tracks list (still ends at Track J);
`docs/operators/deployment-boundary.md`; Track A–J
architecture docs; `examples/*`; registries; new MCP
tools; `1cv8.exe`. No remote push.

**Result.** Track K open at Step 1; planning surface
on disk; active-track state reflects Step 1 in
progress. Tracks A–J still listed as closed. Step 2
is the canonical next step and is **NOT** opened in
this commit.

---

## Step 2 — baseline audit of current client-integration gap

**Goal.** Produce a descriptive baseline audit that
inventories what surfaces currently approximate
MCP-client end-to-end coverage, what surfaces are
adjacent but insufficient, what surfaces are clearly
missing, and what surfaces are explicitly out of
scope. Resolve Q1–Q6 directionally on the basis of
evidence. Produce a handoff list for Step 3 contract.

**What changes.** Exactly one new file:

- `docs/architecture/track-k-real-mcp-client-integration-test-baseline-audit.md`
  (new — descriptive audit, similar in shape to
  Track J Step 2 audit).

**What does NOT change.** Same invariant list as
Step 1. README / PROJECT-STATUS may receive narrow
"next step" narrative updates if needed but should
remain mostly untouched. Production code; `pyproject.toml`;
`scripts/*`; operator-facing surfaces beyond active-
track narrative.

**Result.** Step 2 closed with one new audit
document; directional Q1–Q6 resolutions on disk;
Step 3 handoff list pinned (N items).

---

## Step 3 — exact client-integration contract / closure gate definition

**Goal.** Promote Step 2 directional findings into a
normative contract that pins the closure-gate
definition, allowed client classes, required round-
trip envelope, transport coverage (one transport vs
two), Step 4 file surface, Step 4 verification
harness, Step 6 SemVer expectation.

**What changes.** Exactly one new file:

- `docs/architecture/track-k-real-mcp-client-integration-test-contract.md`
  (new — normative contract, RFC 2119 MUST / MUST
  NOT / SHOULD / MAY language, similar in shape to
  Track J Step 3 contract).

**What does NOT change.** Same invariant list.

**Result.** Step 3 closed with one normative
contract document; PATH selection (PATH A docs-only
vs PATH B narrow harness) pinned; Step 4 file
surface, allowed content, forbidden content, and
verification harness all locked.

---

## Step 4 — narrow harness implementation **or** docs-only operationalization

**Goal.** Operationalize the Step 3 contract.
Either ship a narrow runnable harness (Step 3
PATH B) or a single new operator-facing
demonstration document (Step 3 PATH A). The harness,
if shipped, exercises one MCP server over one
transport end-to-end (`initialize` + `tools/list` +
at least one read-only `tools/call`) and produces
well-formed JSON-RPC 2.0 responses.

**What changes.** Exactly one new file, location
chosen by Step 3 contract:

- **PATH A (docs-only).** New operator-facing
  document at `docs/operators/mcp-client-smoke.md`
  (or equivalent under `docs/`) describing how an
  operator would point a real MCP client (Claude
  Desktop / `mcp-cli` / equivalent) at one of the
  servers, plus the expected envelope shapes.
  No code.
- **PATH B (narrow harness).** New runnable file at
  `scripts/dev/mcp_client_smoke.py` **OR**
  `examples/mcp-client-smoke/run.py` (Step 3
  decides). Stdlib-only (`socket`, `json`,
  `urllib`, `subprocess`, `argparse`, `os`, `sys`).
  No new runtime dependency. ≤300 LOC soft cap.
  Abstract placeholders only; no real credentials.

**What does NOT change.** Same invariant list:
production code (`apps/*/src/`, `packages/*/src/`)
byte-identical; `pyproject.toml` byte-identical;
existing `scripts/*` byte-identical; existing
`examples/*` byte-identical; registries
`15/25/16`; no new MCP tools; no `1cv8.exe`.

**Result.** Step 4 closed with exactly one new
file; demonstrably-runnable evidence (PATH B) or
explicit operator-facing recipe (PATH A); no
production code modified.

---

## Step 5 — docs / operator / release alignment

**Goal.** Narrow CLASS-1 alignment of operator-
facing surfaces to point at the Step 4 deliverable.
Track K remains **active** at Step 5; closure
narrative deferred to Step 6.

**What changes.** Narrow edits to existing
operator-facing docs, only where they have direct
factual drift after Step 4:

- `README.md` Quickstart paragraph (Track K state
  reflects Step 4 closed; Step 5 active).
- `README.md` Active parallel track section
  (Step 4 closed; Step 5 active; Step 6 closure
  next).
- `SECURITY.md` (only if Step 4 introduced a new
  user-visible surface — likely no).
- `docs/release-handoff.md` (only if Step 4
  introduced a new operator-runnable artefact —
  likely yes for PATH B; likely a one-bullet
  addition under "What is in this handoff" + one
  bullet under "Where to read deeper").
- `docs/operators/deployment-boundary.md` (only if
  Step 4 cross-references it; likely no
  modification needed).

**What does NOT change.** `PROJECT-STATUS.md`
(Step 5 narrative deferred to Step 6 — analogous
to Track J Step 5 / Step 6 split); `CHANGELOG.md`
(Step 6 territory); `pyproject.toml` (Step 6
territory); closed-tracks list (Step 6
territory); Track K Step 1 / 2 / 3 / 4
deliverables (immutable post-step); production
code; `scripts/*` (existing files);
`apps/platform/README.md`; manuals.

**Result.** Step 5 closed with narrow CLASS-1
alignment; operator-facing surfaces consistent
with Step 4 deliverable; Track K still framed as
active in README + PROJECT-STATUS.

---

## Step 6 — final integration pass and Track K closure

**Goal.** Final integration verification across
Track K Steps 1–5; Q7 SemVer decision (NO-BUMP /
PATCH); closure-facing docs/status/version
updates; Track K full closure. No active track
remaining after Step 6.

**What changes.**

- `README.md` (Quickstart flipped active → no-
  active-track; Active parallel track section
  compressed; new "Track K detail (закрыт)"
  section above "Track J detail (закрыт)";
  Closed parallel tracks list extended from
  десять → одиннадцать with Track K entry;
  intro line updated to "одиннадцать post-phase
  completion track'ов").
- `PROJECT-STATUS.md` (header rewritten from
  active Track K / Step 5 → "Активного шага
  нет" + Track K closure narrative + commit
  trail across all six steps + Q7 decision;
  status block flipped to `closed` for Track K
  (Track J `closed` block preserved beneath);
  per-step closure sections for Step 2 / 3 / 4 /
  5 / 6 inserted between existing Step 1 section
  and `## Phase 6 закрыта` delimiter).
- `CHANGELOG.md` (if Q7 = PATCH: new
  `## 0.5.2 — Parallel Track K — Real MCP
  Client Integration Test` heading at top; if
  Q7 = NO-BUMP: Track K subsection added under
  existing `## 0.5.1` heading mirroring the
  Track J NO-BUMP closure pattern).
- `pyproject.toml` (touched **only** if Q7 =
  PATCH `0.5.1 → 0.5.2`; untouched if Q7 =
  NO-BUMP).

**What does NOT change.** Same invariant list.
Track K Step 1 / 2 / 3 / 4 / 5 deliverables
byte-identical. Production code; existing
`scripts/*`; `SECURITY.md`; `docs/release-
handoff.md`; `apps/platform/README.md`;
`docs/operators/deployment-boundary.md`;
manuals.

**Q7 decision rule.** Per plan §12 (Q7
directional default): **NO-BUMP** preferred.
PATCH `0.5.1 → 0.5.2` only if Step 4 shipped a
defect-class fix observable by end-users (which
this track is not expected to ship). MINOR /
MAJOR forbidden by track scope.

**Result.** Track K fully closed; eleven post-
phase parallel tracks (A / B / C / D / E / F / G
/ H / I / J / K) closed sequentially; active
parallel track = none; Phase 7 still not
planned.

---

## Summary

Track K is a narrow six-step track to close the
"no real MCP client integration proof" honest gap.
Step 1 (this opening) ships only two planning
documents + narrow README / PROJECT-STATUS
active-track flip. Steps 2 / 3 are docs-only;
Step 4 is the **only** possible code step and
even there is bounded to one new file under
`scripts/dev/` or `examples/mcp-client-smoke/`
(Step 3 decides). Steps 5 / 6 are docs-only.
Production code in `apps/*/src/` and
`packages/*/src/` remains byte-identical
throughout. Registries `read = 15 / write = 25 /
intelligence = 16` carry through. No new MCP
tools. No `1cv8.exe` runs. No real credentials.
No remote push.
