# Parallel Track L — Service Supervision and OS Service Registration — Step Map

Companion to
[track-l-service-supervision-and-os-service-registration-plan.md](track-l-service-supervision-and-os-service-registration-plan.md).
This document defines the six steps of Track L in the
standard format used by Tracks A–K (Goal / What changes /
What does NOT change / Result), plus the track invariants
block and the hard out-of-scope block.

Companion plan locks the directional Q1–Q7 defaults; this
step-map locks the per-step boundary so each step ships
narrowly and verifiably.

---

## Track L invariants

These invariants must hold at every step. They are
verifiable from repo state (grep / `git diff` / `selfcheck.py`
/ `verify-release.ps1`) at every commit:

1. **Tracks A–K production code byte-identical.**
   `apps/*/src/`, `packages/*/src/`,
   `packages/mcp-common/src/mcp_common/_stdio_transport.py`,
   `packages/mcp-common/src/mcp_common/_network_transport.py`,
   `apps/platform/src/onec_platform/installer.py` not
   modified by Steps 1 / 2 / 3 / 5 / 6. Step 4 default
   expectation = also not modified; only Step 3 contract
   may explicitly authorize a narrow modification, and
   only if defended as a defect-class fix (which the
   default expectation per Q6 is **not** needed).
2. **Track K diagnostic harness byte-identical.**
   `scripts/dev/mcp_client_smoke.py` not modified at any
   step.
3. **Track J operator recipe byte-identical.**
   `docs/operators/deployment-boundary.md` not modified at
   any step. Track L may add a sibling document at
   `docs/operators/service-supervision.md` (or similar —
   path locked by Step 3 contract) but does not edit the
   deployment-boundary recipe.
4. **`pyproject.toml`** byte-identical at Steps 1 / 2 / 3 /
   4 / 5. Step 6 may bump `version` if Q7 = PATCH or MINOR;
   default expectation = NO-BUMP (Track J / Track K
   precedent).
5. **Registries `read = 15 / write = 25 / intelligence =
   16`** unchanged across all six steps. `selfcheck.py`
   `status=ok` at every step.
6. **`scripts/dev/selfcheck.py`** byte-identical at every
   step.
7. **`scripts/release/install.ps1`**,
   **`scripts/release/verify-release.ps1`**,
   **`scripts/dev/bootstrap_paths.ps1`**,
   **`scripts/dev/launch.ps1`**,
   **`scripts/dev/README.md`** byte-identical at Steps 1 /
   2 / 3 / 5 / 6. Step 4 may add a new sibling script under
   `scripts/release/` (only if Step 3 contract pins PATH C
   and only under the Step 3 LOC cap).
8. **SECURITY.md** byte-identical at Steps 1 / 2 / 3 / 4.
   Step 5 may add at most one narrow cross-link bullet if
   Step 4 ships an artefact that meaningfully interacts
   with the security claim (default: not the case —
   service supervision does not change the security claim).
9. **`docs/release-handoff.md`** byte-identical at Steps
   1 / 2 / 3 / 4. Step 5 may add one bullet under "What is
   in this handoff" + one bullet under "Where to read
   deeper" if Step 4 shipped a recipe operators must read
   before installing.
10. **`apps/platform/README.md`** byte-identical at Steps
    1 / 2 / 3 / 4. Step 5 may add one narrow cross-link
    only if the Step 4 artefact references a Phase-6
    boundary that platform's README mentions; default
    expectation = no edit.
11. **README.md "Closed parallel tracks" list** byte-
    identical at Steps 1 / 2 / 3 / 4 / 5 (still ends at
    Track K). Only Step 6 extends it to twelve entries
    (A through L).
12. **No new MCP tools** at any step. No additions to
    `mcp_read_server` / `mcp_write_server` /
    `mcp_intelligence_server` tool registries.
13. **No `1cv8.exe` runs** at any step. Track L is
    orthogonal to the 1C binary surface.
14. **No real credentials** in any committed text.
    Examples must use abstract placeholders.
15. **No remote push** at any step. GitHub push remains
    an explicit operator action outside the track.
16. **No premature closure language.** Phrases that frame
    Track L as "закрыт" / "closed" / "fully solved" /
    "production-ready service supervision" / "all OS
    families supported" / "service supervision solved"
    may appear in Steps 1–5 only as explicit DENIALS.
    Only Step 6 introduces closure language for Track L
    itself.

---

## Track L hard out-of-scope (carry through every step)

These categories must not be addressed by Track L at any
step. Each is named explicitly to prevent silent expansion:

- No new transport family (no WebSocket, no SSE, no TCP,
  no Unix-socket, no named-pipe, no in-process TLS, no
  mTLS).
- No auth-scheme redesign (no JWT, no OAuth, no OIDC, no
  SAML, no SCIM, no RBAC, no ABAC, no per-tool ACL, no
  per-tenant isolation, no multi-tenant).
- No deployment-boundary redesign (Track J §13 / §6 / §7 /
  §8 invariants preserved unchanged).
- No packaging ecosystem (no `.msi`, no `.deb`, no signed
  distribution, no GUI installer, no wizard, no PyPI
  publication, no wheel publication beyond existing
  `[project.scripts]` declarations).
- No enterprise identity stack.
- No clustering / HA / load balancing / orchestration
  platforms (no Kubernetes, no Compose-with-replicas, no
  Nomad, no Consul, no etcd, no Zookeeper).
- No web UI / dashboard frontend.
- No full observability stack (no OpenTelemetry, no
  Jaeger, no Prometheus exporter, no OpenMetrics endpoint,
  no log-aggregation forwarder, no distributed tracing
  instrumentation).
- No `/healthz` / `/readyz` / `/livez` endpoint (Track J
  §8 defer preserved).
- No standalone `apps/platform` daemon entrypoint.
- No hot reload / zero-downtime restart guarantee.
- No automatic-update / OTA / self-upgrade mechanism.
- No rollback expansion / AST work / 1C matrix expansion.
- No new MCP tools / registry change.
- No `1cv8.exe` runs.
- No remote push.
- No "service supervision solved" / "production-ready
  service supervision" / "all OS families supported" /
  "clustered HA" / "zero-downtime restart" claim.

---

## Step 1 — planning service supervision and OS service registration

**Goal.** Open Track L formally with a single planning
document and a single step-map document, plus the narrative
flip on README.md and PROJECT-STATUS.md required to mark
Track L as the active parallel track. Establish the Q1–Q7
directional defaults without locking final answers.

**What changes.**
- NEW: `docs/architecture/track-l-service-supervision-and-os-service-registration-plan.md`
  (14-section planning document; Q1–Q7 directional
  recommendations only; honest gap statement; in-scope /
  out-of-scope; guardrails; acceptance criteria;
  relationship table to Tracks G/H/I/J/K; step trajectory).
- NEW: `docs/architecture/track-l-service-supervision-and-os-service-registration-step-map.md`
  (this document — six steps + track invariants block +
  hard out-of-scope block).
- MODIFIED: `README.md` — Quickstart paragraph appended
  with Track L active wording; "Active parallel track"
  section reopened describing Track L at Step 1 planning-
  only; Closed parallel tracks list **unchanged**
  (Track L not moved there yet).
- MODIFIED: `PROJECT-STATUS.md` — header flipped from
  "no active step" to "Track L / Step 1 active planning";
  Track K closure block preserved beneath byte-identical;
  one new per-step section "Parallel Track L / Step 1 —
  planning service supervision and OS service registration
  (завершён)" inserted between the Track K Step 6 section
  and `## Phase 6 закрыта`.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`,
  `_stdio_transport.py`, `_network_transport.py`,
  `installer.py`).
- `pyproject.toml` (`version=0.5.1` preserved).
- `scripts/*` — all existing files byte-identical.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `docs/operators/
  deployment-boundary.md`, `CHANGELOG.md` — byte-identical.
- All Track K / Track J / Track I / Track H / Track G
  architecture docs — byte-identical.
- Registries `read=15 / write=25 / intelligence=16`.
- README Closed parallel tracks list (still ends at
  Track K).
- No `1cv8.exe` runs.
- No real credentials.
- No remote push.
- No Step 2 opening.

**Result.** Track L is formally open at Step 1. The plan
document fixes Q1–Q7 as defaults / directional
recommendations. The step-map document (this file) fixes
the six-step boundary. Operator can read the plan and
step-map and know exactly what Track L will and will not
do. README and PROJECT-STATUS reflect the active-track
flip. No code change anywhere; no `pyproject` change;
registry invariant carried through; selfcheck green;
`verify-release.ps1` green on 8 checks.

---

## Step 2 — baseline audit of current long-running-process / service gap

**Goal.** Produce a single descriptive (not prescriptive)
audit document inventorying the current state of long-
running-process / service / supervision surfaces in the
repo and in the runtime; classify the inventory into the
standard 4-class breakdown (already-reusable / adjacent-
but-insufficient / clearly-missing / explicitly-out-of-
scope); produce Q1–Q6 directional resolutions grounded in
evidence; produce a handoff list for Step 3 contract
consumption.

**What changes.**
- NEW: `docs/architecture/track-l-service-supervision-and-os-service-registration-baseline-audit.md`
  — single descriptive audit document. Default expectation
  = 8–12 sections, ≤ 1500 lines. Sections must cover:
  inventory of foreground-blocking server entrypoints
  (`__main__.py` shape for all three servers); inventory
  of supervision-adjacent files (`launch.ps1`,
  `install.ps1`); whole-repo grep results for `systemd`,
  `launchd`, `Restart=`, `sc.exe`, `nssm`, `New-Service`,
  `pywin32`, `supervisor`, `daemon`, `PIDFile`, `pidfile`,
  `--background`, `--fork`, `--daemonize`; inventory of
  signal-handling shape in `_serve_stdio` and
  `_serve_http`; 4-class breakdown; Q1–Q6 directional
  resolutions; Step 3 handoff list (≥ 10 items).

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  `docs/operators/deployment-boundary.md`.
- README and PROJECT-STATUS — Step 2 is the audit step;
  active-track narrative flips occur at Steps 1 and 6
  only. (Step 2 may at most touch README's "Active
  parallel track" wording to say "Step 2 active" instead
  of "Step 1 active" — but if so, the touch is the
  narrowest single-paragraph CLASS-1 drift fix, not a
  rewrite.)
- Registries.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 2 produces a single descriptive audit
document. No prescriptive language; no MUST / MUST NOT /
SHOULD lock. All "decisions" stay as directional
recommendations to be locked by Step 3 contract. Operator
can read the audit and see exactly what the repo currently
has, what it lacks, and what Step 3 must resolve.

---

## Step 3 — service-supervision contract

**Goal.** Produce a single normative (prescriptive)
contract document using RFC 2119 MUST / MUST NOT / SHOULD /
SHOULD NOT / MAY language. Lock Q1–Q7 final answers (Q7
deferred to Step 6 but framed). Lock Step 4 PATH (A docs-
only / B docs + template / C docs + template + wrapper
script). Lock Step 4 file-surface cap (default ≤ 2 new
files). Lock Step 4 LOC cap for any code-bearing artefact
(default ≤ 150 LOC stdlib-only, no new dependencies). Lock
Step 4 forbidden-files list. Lock Step 5 forbidden-files
list. Lock the closure-gate scenario (which OS family, which
lifecycle verbs, which artefacts).

**What changes.**
- NEW: `docs/architecture/track-l-service-supervision-and-os-service-registration-contract.md`
  — single normative contract document with RFC 2119
  language. Default expectation = 10–15 sections, ≤ 1700
  lines. Sections must cover: definition of supervised-
  service for this repo (§1); OS-family target lock (§2);
  PATH selection lock (§3); lifecycle-verb closure scope
  (§4); file surface lock (§5); LOC cap and dependency
  cap (§6); forbidden-files list for Step 4 (§7);
  forbidden-files list for Step 5 / Step 6 (§8); Track
  G / H / I / J / K carry-forward invariants (§9);
  verification protocol for Step 4 (§10); placeholder
  / credential discipline (§11); honest non-goals (§12);
  closure criteria (§13); Q7 framing for Step 6 (§14);
  Step 4 handoff note (§15).

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  `docs/operators/deployment-boundary.md`.
- README / PROJECT-STATUS narrative beyond at most a
  single CLASS-1 wording update to reflect "Step 3
  active" (same discipline as Step 2).
- Registries.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 3 closes with the prescriptive contract
in place. Step 4 has a closure-gate scenario, a file
surface, a LOC cap, a forbidden-files list, and a
verification protocol — all locked. Step 4 cannot
silently expand scope.

---

## Step 4 — narrow implementation slice

**Goal.** Operationalize the Step 3 contract by shipping
the locked Step 4 artefact(s) under the locked path and
cap. Default expectation = PATH B (one operator-facing
recipe + one template artefact). PATH A or PATH C only if
Step 3 contract explicitly authorizes them.

**What changes (default expectation, PATH B).**
- NEW: `docs/operators/service-supervision.md` (or
  whichever path Step 3 contract locks) — operator-
  facing recipe document. Default expectation = 8–12
  sections, ≤ 1200 lines. Sections must cover: purpose;
  scope statement (which OS family is implementation-
  covered, which OS families are prose-only); prerequisite
  list; service-account / permissions discipline using
  abstract placeholders only; install / register
  walkthrough; uninstall / deregister walkthrough; full
  lifecycle-verb table (start / stop / restart / status /
  logs) per OS family; troubleshooting bullets; cross-
  references to Track G entrypoints, Track H bind
  policy, Track J deployment-boundary recipe, Track K
  smoke harness; honest non-goals.
- NEW: one template artefact at the Step-3-locked path
  (default: `docs/operators/service/mcp-server.service`
  for the systemd path, with placeholders only — no real
  user, host, port, token, or service name). Or, if
  Step 3 contract locks PATH C: one additional script at
  `scripts/release/register-mcp-service.{ps1,sh}` under
  the LOC cap.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`,
  `_stdio_transport.py`, `_network_transport.py`,
  `installer.py`).
- `pyproject.toml` (`version=0.5.1` preserved).
- Existing `scripts/dev/*`, `scripts/release/*`
  byte-identical (Step 4 may add **new** script files
  under `scripts/release/` only if PATH C is locked by
  Step 3 contract; existing files in those directories
  are not modified).
- `scripts/dev/mcp_client_smoke.py` byte-identical.
- `docs/operators/deployment-boundary.md` byte-identical.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  `README.md`, `PROJECT-STATUS.md` — Step 4 is the
  implementation step; closure-doc updates belong to
  Step 5 / Step 6.
- Track L Step 1 / Step 2 / Step 3 docs byte-identical
  (frozen anchors).
- Registries.
- No new MCP tools.
- No 1cv8.exe runs.
- No real credentials (template uses placeholders only).
- No remote push.

**Result.** Step 4 ships the locked Step 3 artefact(s).
Verification protocol from Step 3 §10 must pass: each
template artefact uses placeholders only; each lifecycle
verb described works as specified on the implementation-
covered OS family; cross-references resolve. The artefact
is operator-runnable in the sense of "operator can follow
the recipe from beginning to end without further repo
modifications and end up with a supervised MCP server".

---

## Step 5 — docs / operator / release alignment

**Goal.** Narrow CLASS-1 docs-alignment only. Update the
operator / security / release-facing docs that have
direct factual drift after Step 4. No Track L closure
narrative; Track L remains framed as **active** through
Step 5 (closure narrative is Step 6 territory).

**What changes (default expectation, CLASS 1 only).**
- MODIFIED: `README.md` — Quickstart paragraph + "Active
  parallel track" section refreshed to reflect Steps 1–4
  closed and Step 5 active. Track L still framed as
  **active**; not moved to Closed parallel tracks list.
- MODIFIED: `docs/release-handoff.md` — one new bullet
  in "What is in this handoff" + one new bullet in
  "Where to read deeper" pointing at the Step 4
  recipe / template.
- POSSIBLY MODIFIED: `apps/platform/README.md` — only if
  Step 4 introduces a service-supervision boundary that
  the platform README's existing boundary inventory
  reasonably mentions; default expectation = no edit.
- POSSIBLY MODIFIED: `SECURITY.md` — only if Step 4 ships
  a service-account / permissions section that meaningfully
  intersects the existing security claim; default
  expectation = no edit.

**What does NOT change.**
- Production code.
- `pyproject.toml`.
- `scripts/*`.
- `PROJECT-STATUS.md`, `CHANGELOG.md`, README Closed
  parallel tracks list / Track L detail (закрыт)
  section, `pyproject.toml` version — all Step 6
  territory.
- Track L Step 1 / Step 2 / Step 3 / Step 4 deliverables
  byte-identical.
- Registries.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 5 closes with operator-facing docs in
sync with the Step 4 artefact(s). CLASS-2 cross-links
(narrow optional pointers) may be added if and only if
they fix a factual drift, not as cosmetic enhancement.
CLASS-3 (closure-narrative) edits are explicitly **not**
done at Step 5.

---

## Step 6 — final integration pass and track closure

**Goal.** Honest closure of Track L. Q7 decision recorded
explicitly. Active tracks remaining = none afterwards.
Eleven post-phase parallel tracks become twelve (A
through L).

**What changes.**
- MODIFIED: `README.md` — Quickstart paragraph flipped
  from active → no-active-track wording; "Active parallel
  track" section compressed back to "no active track";
  new "Track L detail (закрыт)" section added above
  "Track K detail (закрыт)"; Closed parallel tracks list
  extended from одиннадцать → двенадцать with Track L
  entry.
- MODIFIED: `PROJECT-STATUS.md` — header rewritten from
  "Track L / Step 1 active planning" to "no active step
  + Track L fully closed"; new `closed` status block for
  Track L with six commit hashes; per-step closure
  sections for Track L Step 2 / Step 3 / Step 4 / Step 5 /
  Step 6 inserted; historical-edit annotation on the tail
  of the Track K Step 6 section updated to reflect
  Track L closure.
- MODIFIED: `CHANGELOG.md` — Track L subsection inserted.
  If Q7 = NO-BUMP: subsection under existing `## 0.5.1`
  heading (mirroring Track J / Track K pattern). If Q7 =
  PATCH: new top-level `## 0.5.2 — Parallel Track L —
  Service Supervision and OS Service Registration`
  heading.
- POSSIBLY MODIFIED: `pyproject.toml` — `version` bumped
  only if Q7 = PATCH (`0.5.1 → 0.5.2`) or MINOR
  (`0.5.1 → 0.6.0`); not touched if Q7 = NO-BUMP.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`,
  `_stdio_transport.py`, `_network_transport.py`,
  `installer.py`).
- All `scripts/*` files (no Step-4 wrapper script
  modification at Step 6; Step-4 deliverables immutable).
- Track L Step 1 / Step 2 / Step 3 / Step 4 / Step 5
  deliverables byte-identical (frozen anchors).
- `SECURITY.md` (Step 5 already aligned; Step 6 closure-
  narrative does not re-touch).
- `docs/release-handoff.md` (Step 5 already aligned;
  Step 6 does not re-touch).
- `apps/platform/README.md` (Step 5 already aligned or
  not touched; Step 6 does not re-touch).
- `docs/operators/deployment-boundary.md` byte-identical
  (Track J artefact, not in Track L scope at any step).
- Registries `read=15 / write=25 / intelligence=16`.
- No new MCP tools.
- No 1cv8.exe runs.
- No real credentials.
- No remote push.

**Result.** Track L closed. Twelve post-phase parallel
tracks closed sequentially (A / B / C / D / E / F / G / H /
I / J / K / L). Phase 7 as a linear phase still not
planned. Q7 outcome recorded explicitly with defended
reasoning. Active parallel track = none.

---

## Q7 framing for Step 6

The Q7 decision is locked at Step 6 only. Defaults from
the plan §12.Q7:

- **NO-BUMP default** if Step 4 = PATH A (docs-only) or
  PATH B (docs + declarative template, no production
  code change). Both Track J and Track K closed under
  NO-BUMP after shipping a docs-and-one-artefact slice;
  Track L is structurally identical under PATH B.
- **PATCH considered** only if Step 4 = PATH C and the
  wrapper script is honestly framed as a defect-class
  fix. Default expectation: not the case — Track L is
  ergonomic, not defect-fixing.
- **MINOR considered** only if Step 4 introduces net-new
  external capability for ordinary product consumers
  (e.g., a new CLI flag on existing server entrypoints).
  Default expectation: not the case — Track L explicitly
  rejects new CLI flags (Q6 = NO production code
  change).
- **MAJOR forbidden** by track scope.

Step 6 must defend its Q7 choice with concrete repo facts
(diff stat, byte-identical inventories, public API
inventory, SemVer §6 / §7 applicability), not by inertia.

---

## Closure summary

By Step 6 commit:

- Twelve post-phase parallel tracks (A through L) closed.
- Track L closed with an explicit Q7 decision.
- Production code byte-identical to Track K closure
  state (`0e40056`).
- Registries unchanged.
- One new operator-facing recipe + at most one new
  template artefact (default PATH B).
- README / PROJECT-STATUS / CHANGELOG updated honestly,
  with explicit denial of "service supervision solved" /
  "production-ready service" / "all OS families
  supported" / "clustered HA" / "zero-downtime restart"
  claims.
- `verify-release.ps1` GREEN on 8 checks at every step.
- `selfcheck.py` `status=ok` at every step.
- No new MCP tools / registry drift / `1cv8.exe` runs /
  real credentials / remote push at any step.
