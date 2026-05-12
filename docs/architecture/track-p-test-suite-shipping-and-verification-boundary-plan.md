# Parallel Track P — Test Suite Shipping and Verification Boundary — Plan

**Track status at the time of this document.** Parallel
Track P opens as the sixteenth post-phase parallel track
after Track O closure (commit `720ac54`, project version
`0.5.2`). Step 1 — planning only; documentation-only. No
production code change. No `pyproject.toml` change. No
`scripts/*` change. No registry change. No `1cv8.exe`
runs. No remote push.

**Track P positioning relative to Tracks A–O.** Fifteen
post-phase parallel tracks have closed sequentially:
A real-write-path, B productization, C packaging, D
credentials hardening, E version-matrix scaffolding, F
rollback expansion, G stdio transport + CLI, H HTTP
transport + bearer auth, I installer auth round-trip
integrity, J TLS and reverse-proxy deployment boundary,
K real MCP client integration test, L service supervision
and OS service registration, M packaging ecosystem and
distribution boundary, N observability and diagnostics
boundary, O dev-time editable install and workspace
discovery. After Track O closure the platform has:

- a stdio MCP transport (Track G);
- a narrow HTTP `/mcp` endpoint with static bearer auth
  (Track H);
- `ProductConfig.auth.tokens` with `${ENV:NAME}` env-
  substitution and `--auth-token-env` CLI override
  (Tracks D + H);
- an install fast-path with auth round-trip integrity
  (Track I);
- an operator-facing deployment-boundary recipe
  (Track J);
- a real MCP client smoke harness (Track K);
- an operator-facing service-supervision recipe and a
  declarative systemd unit-file template (Track L);
- a single buildable pure-Python wheel
  (`1c_agent_platform-0.5.2-py3-none-any.whl`) and an
  operator-facing distribution-boundary recipe (Track M);
- an operator-facing observability/diagnostics recipe
  with FC1–FC7 first-class signals and a triage recipe
  (Track N);
- a contributor-facing dev-time editable install /
  workspace discovery recipe with first-class
  `pip install -e .` and recommended-only
  `bootstrap_paths.ps1` (Track O).

What it still does **not** have is a first-class
**shipped automated test suite** as an in-repo surface.
That gap is the subject of Track P.

---

## §1. Purpose — why this track exists

Track P exists to convert the current honest gap

> "the platform now has every operationally-relevant
> boundary documented (transport / auth / installer /
> deployment / service / packaging / observability /
> dev-time editable install), and three working
> verification gates (`selfcheck.py` pre-flight,
> `verify-release.ps1` release-side 8-check,
> `mcp_client_smoke.py` transport-boundary smoke), but
> it does not have a **shipped automated test suite** —
> no `tests/` directory exists at HEAD `720ac54`, even
> though `pyproject.toml` already declares
> `[tool.pytest.ini_options] testpaths = [\"tests\"]`
> aspirationally"

into a disciplined six-step closure track using the same
shape as Tracks A–O (planning → audit → contract →
narrow implementation → docs alignment → final
integration pass).

The gap is **explicitly acknowledged** in the repo at
HEAD `720ac54`. Two repo anchors point at it:

- `pyproject.toml:31-32` declares `[tool.pytest.ini_options]`
  with `testpaths = ["tests"]`. The declaration is
  aspirational; the directory does not exist.
- `scripts/dev/launch.ps1:28` (in the umbrella usage
  prose) states verbatim: "It does NOT run pytest
  (there is no test suite yet)."

Track O / Step 2 baseline audit (§3.4 and §3.18) noted
both anchors. Track O explicitly chose to leave the
test-suite gap out of its scope (contributor-facing
dev-time install boundary only). Track P is the
dedicated narrow track that closes the test-suite gap.

The track is **not** justified by a defect — there is no
broken behaviour. It is justified by a **verification-
surface-completeness gap**: today the project verifies
itself through three pre-flight / release / smoke
gates, but `pytest`-style automated unit / integration
tests for the existing repo behaviour are absent. The
existing gates are valuable and not duplicated by tests;
they cover different verification axes (import-time
pre-flight, release-side invariants, transport-boundary
round-trip). What is missing is the **behavioural
unit / integration verification layer** that a test
suite typically provides.

---

## §2. Current post-Track-O baseline

The relevant baseline for Track P (as of `720ac54`):

### §2.1 Existing verification surfaces

- **`scripts/dev/selfcheck.py`** — 110-LOC pre-flight
  gate. Imports all 11 src-layout packages, calls
  base functions on safe data, prints 11 key=value
  lines, exits 0 on success. Track N FC4 first-class
  diagnostic signal.
- **`scripts/release/verify-release.ps1`** — 8-check
  release-side gate (Repo layout / Release entrypoints
  / Important docs / Working tree / Git baseline /
  Selfcheck / Credential leak guard / Credential
  template hygiene). Track N FC5 first-class
  diagnostic signal.
- **`scripts/dev/mcp_client_smoke.py`** — Track K
  transport-boundary smoke harness; 341-LOC stdlib-
  only stand-alone diagnostic file. Exercises
  `initialize` + `tools/list` + read-only
  `tools/call` round-trip over both stdio and HTTP
  transports against `mcp-read-server` plus an HTTP
  missing-`Authorization` probe. Track N R1
  recommended-only diagnostic signal.
- **`scripts/release/_install_runner.py`** — install
  fast-path runner; emits structured findings on each
  install attempt. Track N FC6 first-class signal.
- **`.github/workflows/dev-check.yml`** — CI workflow
  running only `bootstrap_paths.ps1` + `selfcheck.py`
  on `windows-latest`. The only CI gate today.

### §2.2 Existing pyproject test declaration

`pyproject.toml:31-32`:

```
[tool.pytest.ini_options]
testpaths = ["tests"]
```

This declaration is **aspirational**. It is configured
as if pytest will be invoked against a `tests/`
directory, but:

- The `tests/` directory **does not exist** at HEAD
  `720ac54`.
- `pytest` is **not** declared in `[project.dependencies]`
  (which is implicitly empty).
- `pytest` is **not** declared in `[project.optional-
  dependencies]` (which does not exist as a TOML
  block at all).
- No `.github/workflows/*.yml` file invokes `pytest`.
- No `scripts/*.ps1` or `scripts/*.py` invokes
  `pytest`.

The declaration was kept across all Tracks A–O as a
future-aspirational marker; Track P is the track that
finally closes (or honestly re-frames) it.

### §2.3 Existing hand-off anchors

- `scripts/dev/launch.ps1:28-30` (in the umbrella
  comment block): "It does NOT run pytest (there is
  no test suite yet)."
- `scripts/dev/launch.ps1:86` (in the usage text):
  "It does NOT run pytest (no test suite yet)."
- Both anchors were committed during Track B / Step 4
  (`launch.ps1` introduction) and have carried
  forward across Tracks C–O byte-identically.
- Track O / Step 2 baseline audit (§3.4) explicitly
  noted the `pyproject.toml:32` declaration is
  aspirational and `tests/` does not exist; Track O
  scope did not address this.

### §2.4 What is **not** in the repo today

- **No `tests/` directory.** Verified via
  `ls tests/` returning "does not exist".
- **No `conftest.py` file** anywhere in the repo.
- **No `pytest.ini` file** (the configuration is
  embedded in `pyproject.toml`).
- **No CI invocation of pytest.**
- **No coverage measurement** (`coverage.py`,
  `pytest-cov`).
- **No fixtures library** for the platform's MCP
  servers, infobases, or product configs.
- **No documented contributor workflow for running
  tests.** Track O recipe at
  `docs/dev/editable-install-and-workspace-discovery.md`
  intentionally left `pytest` as a non-required tool;
  it pointed at `selfcheck.py` as the verification
  gate.

### §2.5 What Track P therefore must close

A first-class **shipped automated test suite boundary**
for the existing repo behaviour: guidance and at most
one `tests/` directory slice + (optionally, depending
on Step 3 contract PATH selection) one narrow non-
production helper (e.g., a `conftest.py` for shared
fixtures, or a narrow `pytest`-aware CI workflow
extension), **without** silently expanding into
performance / load / stress / fuzz / browser / live-1С
/ multi-Python-version / coverage-gate-absolutism
territory.

The track must close that gap **honestly**: it does not
promise "testing solved forever", does not promise
"full QA stack shipped", does not promise "complete
confidence matrix", does not promise "production-grade
certification". It promises **one** documented test-
suite boundary plus (optionally, depending on Step 3
contract PATH selection) one narrow tests slice and/or
one narrow non-production helper, preserving every
Track G / H / I / J / K / L / M / N / O invariant byte-
identical.

---

## §3. Honest gap statement

Five observations, each independently verifiable in the
repo at `720ac54`:

1. **No `tests/` directory exists.** Filesystem check
   confirms.
2. **`pyproject.toml:31-32` declares aspirationally.**
   `[tool.pytest.ini_options] testpaths = ["tests"]`
   has been present across all Tracks A–O without a
   single test ever being committed.
3. **`scripts/dev/launch.ps1` repeats "no test suite
   yet" in two places.** This is the explicit hand-
   off marker for a future track.
4. **CI exercises only selfcheck.** `.github/workflows/
   dev-check.yml` (25 lines) runs
   `bootstrap_paths.ps1` + `selfcheck.py` only. No
   pytest invocation, no coverage, no integration
   step.
5. **Three existing verification gates cover three
   different axes**, but none of them is a behavioural
   unit-test layer:
   - `selfcheck.py` → import-time pre-flight + registry
     counts + library smoke on safe data.
   - `verify-release.ps1` → release-side repo-layout +
     credential-hygiene + git-state invariants.
   - `mcp_client_smoke.py` → transport-boundary
     round-trip smoke.
   A `pytest`-style test suite would target the
   **behavioural layer underneath** — individual
   functions, classes, dataclass invariants, JSON-RPC
   envelope shapes, install-fast-path edge cases,
   policy-engine decisions, rollback whitelist
   semantics, etc. — that is not what the three
   existing gates cover.

The gap is real. It is not papered over by the
existing gates (each covers a different verification
axis and their combination still leaves the
behavioural-unit-test layer empty).

---

## §4. Why existing gates do NOT already equal a shipped test suite

Each of the following candidate "we already have this"
arguments is rejected from repo evidence:

- **"`selfcheck.py` is enough."** `selfcheck.py` is a
  **pre-flight gate**: it imports modules and calls
  base functions on safe data. It does not assert
  behavioural correctness across edge cases. A
  function returning the wrong value on a corner case
  would pass `selfcheck.py` as long as the import
  succeeded. Different layer.
- **"`verify-release.ps1` is enough."** It is a
  **release-side gate**: 8 checks on repo layout, git
  baseline, working tree, credential hygiene. It does
  not exercise any production code path. Different
  layer.
- **"`mcp_client_smoke.py` is enough."** It exercises
  **one round-trip scenario** (initialize + tools/list
  + one read-only tools/call + one 401 probe) over
  both transports against one server. It does not
  test the dozens of individual tools, the policy
  engine, the installer's edge cases, the rollback
  whitelist, the dataclass invariants, etc. Track K /
  Step 6 closure explicitly framed it as a diagnostic
  file, not a runtime QA framework.
- **"Operators write their own tests."** True but
  evades the gap. The same logic would have rejected
  Track J's deployment-boundary recipe ("operators
  can write their own nginx config") or Track L's
  recipe ("operators can write their own systemd
  unit"). Track P's purpose is to define **one**
  supported test-suite boundary in-repo so
  contributors do not need to invent it.
- **"The aspirational `testpaths = [\"tests\"]`
  declaration is enough."** A declaration without
  any committed test under `tests/` is not a test
  suite. The declaration has been carried byte-
  identically through Tracks A–O without
  materialising; Track P is the dedicated track that
  materialises it (or honestly removes the
  declaration).

---

## §5. Goal of the track

By Step 6 closure, Track P must have delivered:

1. A single normative test-suite-shipping contract
   (Step 3) that pins the closure-gate scope, the
   supported test class focus (or explicit "no tests
   shipped — boundary documented only"), the file
   surface for Step 4, and the verification protocol.
2. Either a single contributor-facing test-suite
   recipe (PATH A) **or** that recipe plus a narrow
   `tests/` slice (PATH B) **or** that recipe plus a
   narrow non-production helper (PATH C) — depending
   on Step 3 Q3 lock. Step 4 is the only step that
   may add files beyond docs.
3. Honest closure narrative in README / PROJECT-
   STATUS / CHANGELOG that documents what test-suite
   boundary Track P settled, what it explicitly did
   NOT solve, and what remains out-of-scope (e.g.,
   performance benchmarks, fuzzing, browser tests,
   live-1С integration, multi-Python-version matrix,
   coverage-gate absolutism).
4. Preserved byte-identical runtime and existing
   verification surfaces: Track G stdio path, Track H
   HTTP path, Track I installer round-trip, Track J
   reverse-proxy posture, Track K diagnostic harness,
   Track L service-supervision recipe + systemd
   template, Track M distribution-boundary recipe +
   wheel-build flip, Track N observability recipe,
   Track O dev-time recipe — all unchanged.

---

## §6. What is in scope

- Planning, audit, contract, narrow implementation,
  docs-alignment, and closure for shipped automated
  test suite boundary covering already-existing repo
  behaviour.
- Defining what counts as a "supported in-repo test
  suite" concretely for this repo at the current
  maturity level.
- Defining whether Step 4 targets:
  - **PATH A** — test-suite-boundary docs only
    (recipe formalises today's "selfcheck + verify-
    release + smoke harness" verification surface as
    sufficient; possibly removes the aspirational
    `testpaths = ["tests"]` declaration to match
    reality);
  - **PATH B** — recipe + a narrow `tests/` slice
    (one or two `test_*.py` files exercising
    already-existing behaviour with `pytest`-style
    assertions; no new MCP tools; no behaviour
    change; ≤ 200 LOC stdlib + pytest);
  - **PATH C** — recipe + a narrow non-production
    helper (e.g., a `conftest.py` for shared
    fixtures, or a narrow CI workflow extension
    invoking `pytest`).
- Defining whether tests stay cross-OS neutral or
  name one primary supported test-runner OS.
- Defining how test-suite relates to current
  selfcheck / verify-release / smoke / install /
  observability truths (cross-references only; no
  redesign).
- Preserving compatibility with all Tracks G / H / I /
  J / K / L / M / N / O invariants.

## §7. What is out of scope

The following are intentionally **not** Track P scope.
Each is denied explicitly to prevent silent expansion:

- **No performance benchmarking.** No `pytest-
  benchmark`, no `timeit` regression harness, no
  performance SLO.
- **No load testing.** No `locust`, no `wrk`, no
  JMeter, no load-generator anywhere in the repo.
- **No stress testing.** No long-running stability
  runs, no soak tests.
- **No fuzzing.** No `hypothesis` (even as a
  recommended-only tool by name), no `atheris`, no
  AFL, no Boofuzz.
- **No browser / UI tests.** No Selenium, no
  Playwright, no Cypress, no headless-browser
  driver.
- **No web dashboard testing.** No frontend test
  framework (the platform does not ship a frontend;
  no dashboard means no dashboard tests).
- **No real `1cv8.exe` execution.** Tests MUST NOT
  invoke `1cv8.exe`. The reference-stand round-trip
  (Track A) remains a separate operator-driven
  procedure, not a CI-runnable test.
- **No external SaaS / live-network integration.**
  Tests MUST NOT depend on outbound network
  connectivity, external APIs, third-party services,
  or any non-local resource.
- **No multi-Python-version matrix.** `.python-
  version` Python 3.11 pin preserved; no `tox.ini`,
  no `nox.py`, no CI matrix expansion.
- **No containerised CI lab.** No Docker-in-CI
  workflow, no `services:` block in
  `dev-check.yml`, no compose stack for tests.
- **No snapshot/golden approval framework.** No
  `approvaltests`, no `pytest-snapshot`, no
  golden-file regression library.
- **No mutation testing.** No `mutmut`, no
  `cosmic-ray`, no PIT-style mutator.
- **No coverage-gate absolutism.** Track P MUST NOT
  introduce a "must reach X% coverage to merge"
  policy. Coverage measurement, if introduced at
  all, remains diagnostic-only; no merge gate.
- **No rewriting verification philosophy of
  selfcheck / verify-release.** The three existing
  gates remain as-is; Track P does **not** subsume
  them, does **not** redirect their roles, does
  **not** absorb them into the test suite.
- **No transport / auth / deployment / service /
  packaging / observability redesign.** Tracks G/H/
  I/J/K/L/M/N preserved byte-identical.
- **No dev-time recipe redesign.** Track O
  preserved byte-identical.
- **No new MCP tools.** Registry invariant
  `read=15 / write=25 / intelligence=16` must carry
  through all six Track P steps.
- **No registry changes.**
- **No new CLI flag on existing servers.**
- **No new `[project.scripts]` console entries.**
- **No new project dependencies at Step 1.** Step 4
  MAY add `pytest` as a dev-only optional
  dependency under PATH B / PATH C, but only if
  Step 3 contract explicitly authorises it. Step 1
  must not pre-commit to that decision.
- **No new entrypoint module.**
- **No `1cv8.exe` runs.**
- **No remote push.** GitHub push remains operator
  decision.
- **No "testing solved forever" / "full QA stack
  shipped" / "complete confidence matrix" /
  "production-grade certification" / "enterprise
  test infrastructure" / "100% coverage achieved" /
  "all behaviours covered" claim.** Such phrases may
  appear in Track P docs only as explicit denials.

---

## §8. Guardrails

Each guardrail is verifiable on the post-Step-1 commit
and must remain verifiable through Step 6:

1. **Tracks A–O invariants byte-identical.**
   `apps/*/src/`, `packages/*/src/`, `docs/operators/
   deployment-boundary.md`, `docs/operators/service/
   service-supervision.md`, `docs/operators/service/
   mcp-server.service`, `docs/operators/packaging/
   distribution-boundary.md`, `docs/operators/
   observability.md`, `docs/dev/editable-install-and-
   workspace-discovery.md` not touched by any Track P
   step.
2. **`pyproject.toml`** byte-identical at Steps 1 / 2
   / 3 / 5. Step 4 MAY modify `pyproject.toml` only
   if Step 3 contract explicitly authorises PATH
   B/C with a narrow `[project.optional-
   dependencies]` `dev`/`test` block declaration; the
   default-expectation change is at most one narrow
   addition. Step 6 MAY further modify `pyproject.
   toml` `version` only if Q7 = PATCH; default
   expectation Q7 = NO-BUMP under PATH A.
3. **Registries invariant.** `selfcheck.py` registries
   `read=15 / write=25 / intelligence=16` must remain
   confirmed green at every step.
4. **No new MCP tools** at any step.
5. **No new CLI flag on existing servers.** The Track
   G / H flag surface
   (`--transport`, `--config-path`, `--log-level`,
   `--bind`, `--auth-token-env`) is locked.
6. **No new entrypoint module.**
7. **`scripts/dev/selfcheck.py`** byte-identical at
   every step.
8. **`scripts/dev/mcp_client_smoke.py`** byte-
   identical at every step.
9. **`scripts/release/install.ps1`**,
   **`scripts/release/verify-release.ps1`**,
   **`scripts/release/_install_runner.py`**,
   **`scripts/dev/launch.ps1`**,
   **`scripts/dev/bootstrap_paths.ps1`**,
   **`scripts/dev/run_dev_check.ps1`** byte-identical
   at Steps 1 / 2 / 3 / 5 / 6. Step 4 MAY modify
   `scripts/dev/launch.ps1`'s "no pytest yet" prose
   only if Step 3 contract explicitly authorises PATH
   B/C and the change is narrow (≤ 5 lines of prose).
   Default expectation: no `scripts/*` modification.
10. **`SECURITY.md`** byte-identical at every step.
11. **`docs/release-handoff.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add narrow
    CLASS-1 updates if a test-suite recipe becomes
    discoverable; default expectation is at most one
    new bullet in "Where to read deeper".
12. **`apps/platform/README.md`** byte-identical at
    every step.
13. **`docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add narrow
    cross-link in `docs/developer-manual.md`.
14. **`scripts/dev/README.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add narrow
    pointer.
15. **README.md "Closed parallel tracks" list** byte-
    identical at Steps 1 / 2 / 3 / 4 / 5 (still 15
    entries A–O). Only Step 6 extends it to 16
    entries.
16. **`CHANGELOG.md`** byte-identical at Steps 1 / 2 /
    3 / 4 / 5. Only Step 6 appends a Track P closure
    entry.
17. **`.github/workflows/dev-check.yml`** byte-
    identical at Steps 1 / 2 / 3 / 5 / 6. Step 4
    MAY extend the workflow file only if Step 3
    contract explicitly authorises PATH B/C with a
    pytest-invocation step.
18. **`.python-version`** byte-identical at every
    step (Python 3.11 pin preserved).
19. **No `1cv8.exe` runs** at any step. Tests MUST
    NOT invoke `1cv8.exe`.
20. **No outbound network** in tests. Tests MUST
    operate on stdlib + (if PATH B/C) pytest only,
    in-process, no live HTTP outbound, no DNS
    resolution beyond `localhost`.
21. **No real credentials** in any committed file.
22. **No premature closure language.** Steps 1–5 may
    not describe Track P as "закрыт" / "closed".
23. **No false implementation claims.** Step 1 plan
    must present Q1–Q7 as **defaults** and
    **recommendations**, not as decided answers.
24. **Step 4 file-surface cap.** Step 3 contract MUST
    pin a maximum number of touched files (default
    expectation: ≤ 4 — at most one recipe doc + at
    most one `tests/__init__.py` + at most one
    `tests/test_*.py` slice + at most one narrow
    `pyproject.toml` `[project.optional-dependencies]
    dev/test` block if PATH B/C). Step 3 may tighten.
25. **Step 4 LOC cap for tests slice.** Default
    expectation: ≤ 300 LOC stdlib + pytest only.
    Step 3 may tighten.

---

## §9. Acceptance criteria for eventual closure

By Step 6 commit:

1. Track P has shipped **at most one new architecture
   plan-doc, one new step-map doc, one new baseline-
   audit doc, one new normative contract doc, and
   (Step 4) at most four new files or surgical
   modifications** under Step 3 contract caps.
2. Production code (`apps/*/src/`, `packages/*/src/`)
   byte-identical to Track O closure state (`720ac54`).
3. `pyproject.toml` `version` either unchanged
   (`0.5.2`, Q7 = NO-BUMP) or bumped per Q7 rule.
4. Registries `read=15 / write=25 / intelligence=16`
   carried through unchanged.
5. README / PROJECT-STATUS / CHANGELOG closure
   narrative present and honest: explicit denial of
   "testing solved forever", "full QA stack shipped",
   "complete confidence matrix", "production-grade
   certification", "enterprise test infrastructure",
   "100% coverage achieved", "all behaviours covered"
   claims; explicit statement of which test-suite
   boundary Track P settled; explicit Q7 reasoning.
6. `verify-release.ps1` GREEN on 8 checks at every
   step.
7. `selfcheck.py` `status=ok` at every step.
8. No real credentials anywhere in committed text.
9. No `1cv8.exe` runs anywhere in the track.
10. No outbound-network calls in any committed test.
11. No remote push performed automatically by any
    step.
12. Track P moved into README's "Closed parallel
    tracks" list, growing it from 15 to 16 closed
    tracks (A through P).

---

## §10. Honest constraints after closure

These constraints remain after Track P closure:

- **No "production-ready test infrastructure" claim.**
  Track P's closure-gate covers one narrow test-suite-
  boundary slice; broader QA matrices recommended-
  only.
- **No coverage-gate enforcement.** Coverage
  measurement (if any) remains diagnostic-only.
- **No multi-Python-version matrix.** Python 3.11
  remains the pinned version.
- **No performance / load / stress / fuzz / mutation /
  snapshot / browser / live-1С / SaaS-integration
  capability.**
- **No new MCP tools / registry change.**
- **No `1cv8.exe` runs.**

---

## §11. Relationship to Tracks G / H / I / J / K / L / M / N / O

| Aspect | Track K (smoke harness) | Track N (observability) | Track O (dev-time) | Track P (this — test suite) |
| --- | --- | --- | --- | --- |
| Verification axis | Transport-boundary round-trip smoke (1 scenario) | Operator diagnostic surface classification | Contributor install workflow | Behavioural unit/integration test suite |
| Audience | Operator/contributor diagnostic-runner | Operator triaging failures | Contributor editing the repo | Contributor verifying behaviour |
| Primary artefact | `scripts/dev/mcp_client_smoke.py` | `docs/operators/observability.md` | `docs/dev/editable-install-and-workspace-discovery.md` | TBD by Step 3 contract |
| Lifecycle moment | Manual / on-demand | Operate-time | Dev-time install | Dev-time / CI test-time |
| Cross-OS | stdlib-only, cross-OS | Linux primary + others prose | Windows primary + POSIX via editable install | TBD; default cross-OS neutral |
| Code touched? | NO production code | NO production code | NO production code | **TBD by Step 3 contract** (default expectation: zero production code change) |
| New transport / endpoint / flag? | NO | NO | NO | NO |
| Registry change? | NO | NO | NO | NO |
| SemVer outcome | NO-BUMP | NO-BUMP | NO-BUMP | **TBD** (default = NO-BUMP if PATH A; PATCH considered only under PATH B/C with honest defect-class declarative repair — e.g., closing the aspirational `testpaths = ["tests"]` declaration by materialising the directory; see §12.Q7) |

Track P inherits all preceding tracks' invariants and
adds none that conflict with them.

---

## §12. Open questions Q1–Q7 with directional defaults

These are **defaults / directional recommendations**,
not decided answers. Step 2 audit may move them; Step 3
contract locks them.

### Q1 — what counts as "test suite shipping" for closure?

**Options.**
- **(A)** One contributor-facing test-suite-boundary
  recipe only — formalises today's "selfcheck +
  verify-release + smoke harness" verification
  surface as the supported verification stance; the
  aspirational `testpaths = ["tests"]` declaration in
  `pyproject.toml` is either left as-is (with prose
  pointing at the new recipe) or honestly removed.
  No `tests/` directory ships.
- **(B)** Recipe **plus** a narrow `tests/` slice —
  one or two `test_*.py` files exercising already-
  existing behaviour with `pytest`-style assertions;
  `pytest` declared as a dev-only optional dependency;
  no behaviour change.
- **(C)** Recipe **plus** a narrow non-production
  helper — e.g., a `conftest.py` for shared fixtures,
  or a narrow CI workflow extension invoking
  `pytest`.

**Default recommendation.** **(B) recipe + narrow
tests slice** as the most likely outcome, because
the aspirational `[tool.pytest.ini_options]
testpaths = ["tests"]` declaration is a long-
standing repo anchor that genuinely benefits from
materialisation (mirror of Track M / Step 4
closing the `packages = []` aspirational declaration).
**(A)** acceptable as fallback if Step 2 audit
reveals that materialising even a narrow tests slice
expands scope beyond what Track P can honestly
deliver. **(C)** rejected by default — a
`conftest.py` without any actual tests is hollow.

### Q2 — primary test class focus first?

**Options.**
- **(A)** Unit tests on dataclasses, models, registry
  helpers, policy-engine decisions — pure-function
  / pure-class behaviour with no I/O.
- **(B)** Integration tests on subprocess-level MCP
  transport behaviour — extending Track K's
  approach with more scenarios.
- **(C)** Repo-local behavioural tests — exercising
  `installer.py` round-trip, `selfcheck.py` parsing,
  rollback whitelist semantics, observability
  log-shape — at unit granularity.

**Default recommendation.** **(A) unit tests** on
pure-function / pure-class behaviour first; **(C)
repo-local behavioural tests** as the natural second
class. **(B) subprocess-level integration tests**
rejected by default — Track K's harness already
covers that axis adequately for the current
maturity; duplicating it inside pytest would
overlap rather than complement.

### Q3 — likely honest Step 4 path?

**Options.**
- **PATH A** — docs-only test-suite-boundary recipe.
- **PATH B** — docs + narrow `tests/` slice + narrow
  pyproject dev-extra declaration.
- **PATH C** — docs + narrow non-production helper
  (conftest / CI extension).

**Default recommendation.** **PATH B is the most
likely outcome**, with PATH A held in reserve if
Step 2 audit reveals that materialising even a
narrow tests slice expands scope beyond Track P's
narrow boundary. **Do not lock Step 4 PATH at
Step 1**; Step 3 contract is the lock point.

### Q4 — minimum closure scope

The eventual closure document MUST answer at minimum:

- What the supported test-suite shape is (`pytest`-
  invoked under `tests/`; no other framework).
- What tests cover and what they do not cover
  (behavioural unit layer; not performance / load /
  stress / fuzz / browser / live-1С / SaaS / CI
  matrix).
- How a contributor runs the tests (commands; from
  repo root after `pip install -e .[test]` or
  similar narrow declaration).
- How tests relate to existing gates (selfcheck =
  pre-flight; verify-release = release-side;
  smoke = transport-boundary; tests =
  behavioural-unit; complementary axes, not
  replacements).
- What is explicitly out-of-scope (the full §7
  forbidden-categories list).

### Q5 — what is insufficient as closure proof?

- **"The aspirational declaration is enough."** No —
  aspirational ≠ shipped.
- **"`selfcheck.py` covers it."** No — pre-flight
  gate, not behavioural unit layer.
- **"`verify-release.ps1` covers it."** No —
  release-side invariants, not behavioural.
- **"`mcp_client_smoke.py` covers it."** No —
  transport-boundary smoke, not behavioural unit
  layer.
- **"Manual checking works."** No — non-repeatable.
- **"Tests pass on my machine."** No — repo-local
  reproducibility required.

### Q6 — does Track P require production code changes?

**Default recommendation.** **No.** Tests target
existing behaviour; behaviour does not change.
Step 2 audit must verify this honestly, but the
default expectation is that no `apps/*/src/` or
`packages/*/src/` change is warranted.

### Q7 — SemVer expectation

**Options.**
- **(A)** NO-BUMP. Track P closes under existing
  `0.5.2` if Step 4 = PATH A docs-only. Mirrors
  Track J / Track K / Track L / Track N / Track O
  NO-BUMP precedents.
- **(B)** PATCH `0.5.2 → 0.5.3`. Track P closes with
  a PATCH bump if Step 4 = PATH B (materialises the
  aspirational `tests/` directory + declares the
  dev-only `pytest` extra) AND the change is
  honestly framed as defect-class declarative
  repair closing the long-standing
  `[tool.pytest.ini_options] testpaths = ["tests"]`
  aspirational declaration. Mirror of Track I /
  Track M PATCH precedents.
- **(C)** MINOR `0.5.2 → 0.6.0`. Explicitly
  rejected by guardrails — Track P does not ship
  new declared external capability for ordinary
  product consumers.
- **(D)** MAJOR. Explicitly rejected by track
  scope.

**Default recommendation.** **(A) NO-BUMP** if Step 4
PATH A; **(B) PATCH** as the more likely outcome if
Step 4 PATH B (the long-standing `testpaths` declaration
being materialised is legitimate defect-class
territory; Track M's `packages = []` → populated array
precedent applies directly). MINOR / MAJOR explicitly
rejected.

---

## §13. Six-step trajectory preview

| Step | Kind | Default file surface | Default scope cap |
| --- | --- | --- | --- |
| Step 1 (this) | planning | 2 new docs + README + PROJECT-STATUS | docs-only |
| Step 2 | descriptive baseline audit | 1 new doc under `docs/architecture/track-p-*-baseline-audit.md` | docs-only |
| Step 3 | normative contract | 1 new doc under `docs/architecture/track-p-*-contract.md` | docs-only |
| Step 4 | narrow implementation (PATH A / B / C) | ≤ 4 new files or surgical modifications (default under PATH B = one recipe + one `tests/__init__.py` + one `tests/test_*.py` + one narrow `pyproject.toml` `[project.optional-dependencies] test = ["pytest"]` block) | locked by Step 3 contract |
| Step 5 | docs / operator / release alignment | narrow CLASS-1 only: README, possibly `docs/release-handoff.md`, possibly `docs/developer-manual.md`, possibly `scripts/dev/launch.ps1` "no pytest yet" prose-only narrow replacement; NO production code | scope locked by Step 3 contract |
| Step 6 | final integration pass and track closure | README + PROJECT-STATUS + CHANGELOG; optionally `pyproject.toml` if Q7 = PATCH | NO production code; Q7 decision explicit |

---

## §14. Honest summary

**What Track P will do.** Convert the "no shipped
automated test suite" gap into one contributor-facing
test-suite-boundary recipe (and, if Step 3 contract
pins PATH B, a narrow `tests/` slice plus a narrow
dev-only `pytest` extra declaration that materialises
the aspirational `[tool.pytest.ini_options]
testpaths = ["tests"]` directive), preserving every
Tracks A–O invariant byte-identical.

**What Track P will not do.** It will not introduce a
broader QA platform (no performance / load / stress /
fuzz / browser / mutation / snapshot / approval / live-
1С / SaaS / multi-Python-matrix / containerised-CI /
coverage-gate-absolutism / verification-philosophy
redesign); will not add new MCP tools; will not change
registries; will not run `1cv8.exe`; will not push to
GitHub automatically.

**Why this is the next right narrow track.** The
`pyproject.toml:31-32` `[tool.pytest.ini_options]
testpaths = ["tests"]` declaration has been
aspirational across all Tracks A–O without
materialising; `scripts/dev/launch.ps1` says "no test
suite yet" in two places. Track P closes that long-
standing aspirational anchor the same way Track M
closed the `packages = []` aspirational declaration:
one document and at most one narrow declarative slice
(plus the directory it implies), with explicit denial
of the broader QA-platform claims a less disciplined
version of the same track would make.

**Default Q7 outcome.** **NO-BUMP** if Step 4 PATH A
(docs-only); **PATCH** if Step 4 PATH B (narrow
declarative materialisation closing the long-standing
`testpaths` aspirational declaration). Q7 lock is
Step 6 territory.
