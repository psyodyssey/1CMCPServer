# Parallel Track O — Dev-Time Editable Install and Workspace Discovery — Plan

**Track status at the time of this document.** Parallel
Track O opens as the fifteenth post-phase parallel track
after Track N closure (commit `2737a52`, project version
`0.5.2`). Step 1 — planning only; documentation-only. No
production code change. No `pyproject.toml` change. No
`scripts/*` change. No registry change. No `1cv8.exe`
runs. No remote push.

**Track O positioning relative to Tracks A–N.** Fourteen
post-phase parallel tracks have closed sequentially:
A real-write-path, B productization, C packaging, D
credentials hardening, E version-matrix scaffolding, F
rollback expansion, G stdio transport + CLI, H HTTP
transport + bearer auth, I installer auth round-trip
integrity, J TLS and reverse-proxy deployment boundary,
K real MCP client integration test, L service supervision
and OS service registration, M packaging ecosystem and
distribution boundary, N observability and diagnostics
boundary. After Track N closure the platform has:

- a stdio MCP transport (Track G);
- a narrow HTTP `/mcp` endpoint with static bearer auth
  (Track H);
- `ProductConfig.auth.tokens` with `${ENV:NAME}` env-
  substitution and `--auth-token-env` CLI override
  (Tracks D + H);
- an install fast-path with auth round-trip integrity
  (Track I);
- an operator-facing deployment-boundary recipe (Track J);
- a real MCP client smoke harness (Track K);
- an operator-facing service-supervision recipe and a
  declarative systemd unit-file template (Track L);
- a single buildable pure-Python wheel
  (`1c_agent_platform-0.5.2-py3-none-any.whl`) and an
  operator-facing distribution-boundary recipe (Track M);
- an operator-facing observability/diagnostics recipe
  with FC1–FC7 first-class signals and a triage recipe
  (Track N).

What it still does **not** have is a first-class
**developer-time** story for editable install, workspace
discovery, or bootstrap expectations. That gap is the
subject of Track O.

---

## §1. Purpose — why this track exists

Track O exists to convert the current honest gap

> "the platform now has a **deploy-time** packaging
> boundary (Track M ships a buildable wheel for
> `pip install <WHEEL_PATH>` on a deployment host), but
> it does not yet have a formal **dev-time** boundary —
> there is no committed answer for how a contributor or
> internal developer should install the platform from a
> checkout for in-place editing, how workspace discovery
> works, and what is supported vs. merely possible vs.
> out-of-scope at dev time"

into a disciplined six-step closure track using the same
shape as Tracks A–N (planning → audit → contract →
narrow implementation → docs alignment → final
integration pass).

The gap is **explicitly acknowledged** in the repo at
HEAD `2737a52`. `scripts/dev/README.md:5-11` states
verbatim:

> "На текущем этапе это временный bootstrap для монорепы:
> editable install и workspace discovery всё ещё out of
> scope. Track M / Step 4 ввёл узкий supported
> distribution boundary — один buildable `py3-none-any`
> wheel … но он покрывает `pip install` deployment flow,
> не dev-time editable install."

That sentence — written during Track M / Step 4 — is the
explicit hand-off from deploy-time packaging (Track M) to
dev-time editable install / workspace discovery (Track
O, this track).

The track is **not** justified by a defect — there is no
broken behaviour. It is justified by a **developer-
ergonomics gap**: today a contributor cloning the repo
must either (a) use the `scripts/dev/bootstrap_paths.ps1`
PYTHONPATH bootstrap (Track B), or (b) attempt
`pip install -e .` (which **may** work via hatchling
but has never been tested, documented, or framed as the
supported developer workflow). Neither path has a
positive supported boundary statement; one is documented
as "temporary bootstrap for the monorepo" and the other
is not mentioned anywhere.

---

## §2. Current post-Track-N baseline

The relevant baseline for Track O (as of `2737a52`):

### §2.1 Dev-time surfaces that exist today

- **`scripts/dev/bootstrap_paths.ps1`** — PowerShell
  PYTHONPATH bootstrap. Adds the eleven src-layout paths
  (the same eleven now referenced by Track M's wheel-
  build `packages = [...]` array) to `$env:PYTHONPATH`.
  Used by `launch.ps1` and `run_dev_check.ps1`.
- **`scripts/dev/launch.ps1`** — Operator/dev umbrella
  (Track B / Step 4). Subcommands: `selfcheck`, `repl`,
  `run <script>`, `help`. Thin PowerShell dispatcher
  over `bootstrap_paths.ps1` + `run_dev_check.ps1`. No
  business logic.
- **`scripts/dev/run_dev_check.ps1`** — Selfcheck wrapper
  used by `dev-check.yml` CI workflow.
- **`scripts/dev/selfcheck.py`** — Pre-flight gate; 11
  key=value lines confirming imports + registry counts.
- **`scripts/dev/mcp_client_smoke.py`** — Track K
  transport-boundary smoke harness.
- **`scripts/dev/README.md`** — Describes the four
  scripts above; **explicitly says** "editable install и
  workspace discovery всё ещё out of scope".
- **`pyproject.toml`** — Hatchling build backend.
  `[tool.hatch.build.targets.wheel] packages = [...]`
  array (Track M / Step 4) declares eleven src-layout
  package paths. `[project.scripts]` declares three
  console entries. `requires-python = ">=3.11"`.
  `[project.dependencies]` is empty (stdlib-only). The
  configuration is **structured such that `pip install
  -e .` would mechanically work** (hatchling supports
  editable installs on PEP 660-compatible pip), but
  this path is not documented, not tested, and not
  named as supported.
- **`.python-version`** — pins Python 3.11.
- **`.github/workflows/dev-check.yml`** — CI runs only
  `bootstrap_paths.ps1` + `selfcheck.py`. CI does not
  exercise `pip install -e .` or any editable-install
  path.

### §2.2 What is **not** in the repo today

- **No documented `pip install -e .` flow.** Whole-repo
  grep for `pip install -e`, `editable`, `pep 660`,
  `[tool.hatch.build.targets.wheel.hooks.…]` returns
  zero functional hits; the only mention of "editable
  install" anywhere is the `scripts/dev/README.md`
  out-of-scope sentence quoted in §1.
- **No "what does workspace discovery look like" answer
  outside `bootstrap_paths.ps1`.** Contributors who do
  not read `bootstrap_paths.ps1` have no other source
  of truth for which packages live where.
- **No dev-onboarding recipe.** `docs/developer-
  manual.md` exists but its observability/Track N
  audit (§3.11.4) confirmed it does not currently
  cover editable install or workspace discovery.
- **No `bootstrap_paths` cross-OS sibling.** The
  bootstrap is PowerShell-only; there is no `.sh`
  equivalent for Linux/macOS contributors. Track M /
  Track L recipes have cross-OS prose; the dev-time
  bootstrap does not.
- **No statement of which Python tools (`pip`,
  `build`, `pytest`, `hatch`, `pdm`, `uv`, etc.) are
  supported dev-time tools.** The selfcheck script
  uses only stdlib; the install fast-path uses Python
  stdlib too; but contributors invariably bring their
  own tool preferences and no policy exists.
- **No "what counts as a supported developer
  workflow" statement.** Cloning + running
  `bootstrap_paths.ps1` works on Windows; what about
  other workflows?

### §2.3 What Track O therefore must close

A first-class **dev-time editable install / workspace
discovery boundary**: guidance and at most one
declarative artefact or `pyproject.toml`/`scripts/*`
adjustment that defines what a contributor's supported
workflow looks like, **without** silently expanding into
the deploy-time packaging boundary (Track M scope) or
into a broader build-tooling redesign.

The track must close that gap **honestly**: it does not
promise "developer workflow solved forever", does not
promise "all IDE integrations supported", does not
promise "all package managers supported for dev install",
does not promise "containerised dev environment shipped",
does not promise "remote dev shipped". It promises
**one** documented dev-time boundary plus (optionally,
depending on Step 3 contract PATH selection) at most one
narrow declarative or scripted artefact, preserving
every Track G/H/I/J/K/L/M/N invariant byte-identical.

---

## §3. Honest gap statement

Five observations, each independently verifiable in the
repo at `2737a52`:

1. **`scripts/dev/README.md:5-11` declares the gap
   verbatim.** "Editable install и workspace discovery
   всё ещё out of scope." That sentence was committed
   during Track M / Step 4 as an explicit hand-off
   marker; no later track has addressed it.
2. **`pip install -e .` is mechanically possible but
   never tested or documented.** Hatchling supports PEP
   660 editable installs by default; the
   `[tool.hatch.build.targets.wheel] packages` array is
   already populated (Track M). Nothing prevents `pip
   install -e .` from working, but no CI workflow
   exercises it, no recipe documents it, and no commit
   message in the entire repo references "editable" as
   a supported behaviour.
3. **`bootstrap_paths.ps1` is PowerShell-only.** A
   Linux/macOS contributor cannot use it directly. The
   project has no `.sh` equivalent; the `launch.ps1`
   umbrella is `.ps1` only. The selfcheck on a Linux
   contributor's machine therefore requires the
   contributor to either invoke PowerShell via `pwsh`
   (not always installed) or hand-construct
   `PYTHONPATH`.
4. **No "developer-supported tooling" policy.** The
   project's choice of build backend (`hatchling`),
   formatter / linter (`ruff` per `[tool.ruff]`), and
   test framework (`pytest` per
   `[tool.pytest.ini_options]`) are present in
   `pyproject.toml` but no document tells a contributor
   which of those a supported dev workflow uses, vs.
   which are operator-side choices, vs. which are
   incidental.
5. **`docs/developer-manual.md` does not cover this
   ground.** Per Track N / Step 2 audit, the developer
   manual touches concepts (write boundary, registry
   shape) but does not enumerate "how to install the
   platform from a checkout for editing".

The gap is real. It is not papered over by Track B's
`launch.ps1` (umbrella over a PowerShell-only bootstrap),
nor by Track M's wheel (deploy-time, not dev-time), nor
by `selfcheck.py` (pre-flight gate, not an install
boundary).

---

## §4. Why this gap is NOT already closed by Track M

Track M is the most adjacent prior track, and the
distinction matters. Five rejections of the candidate
"Track M already covers this" argument:

- **Track M's recipe is operator-facing, not contributor-
  facing.** Section §1 of `docs/operators/packaging/
  distribution-boundary.md` explicitly frames its
  audience as operators receiving a wheel artefact, not
  contributors editing the repo in place. The same
  document at §11 (relationship to install fast path /
  deployment boundary / service supervision) cites
  *deployment-side* axes; it does not name a developer
  workflow at all.
- **Track M's wheel is built, then installed.**
  `python -m build` produces a fixed artefact; `pip
  install <WHEEL_PATH>` lays it down. Editing a source
  file after installation requires re-running both
  steps. That is correct for operator distribution but
  hostile for contributor edit-test-edit cycles.
- **Track M closed an empty-wheel-build defect.** The
  Track M / Step 4 change (`packages = []` → 11-element
  array) **enables** wheel builds at deploy time. It
  also **happens to make** editable installs mechanically
  feasible — but Track M / Step 4 commit explicitly
  framed this only as a deploy-time enablement; no Track
  M document promises or tests editable install
  behaviour.
- **Track M's recipe explicitly disclaims dev-time
  scope.** `distribution-boundary.md` does not document
  any editable-install verb among its five lifecycle
  verbs (`build` / `install` / `uninstall` / `upgrade`
  / `verify`); the install verb is `pip install
  <WHEEL_PATH>`, not `pip install -e .`. The two flows
  are operationally and semantically different.
- **`scripts/dev/README.md` was updated *during* Track
  M to explicitly say the editable install / workspace
  discovery gap remained.** This is the strongest
  rejection: the people closing Track M deliberately
  carried forward the dev-time gap as a separate
  future-track concern. Track O is that future track.

---

## §5. Goal of the track

By Step 6 closure, Track O must have delivered:

1. A single normative dev-time editable install /
   workspace discovery contract (Step 3) that pins the
   closure-gate scope, the supported dev-time workflow
   shape (or explicit "no artefact — boundary
   documented only"), the file surface for Step 4, and
   the verification protocol.
2. Either a single contributor-facing dev-time recipe
   **or** that recipe plus at most one narrow
   `pyproject.toml`/`scripts/*` adjustment **or** that
   recipe plus at most one narrow bootstrap helper —
   depending on Step 3 Q3 lock. Step 4 is the only step
   that may add code/config beyond docs.
3. Honest closure narrative in README / PROJECT-STATUS /
   CHANGELOG that documents what dev-time boundary
   Track O settled, what it explicitly did NOT solve,
   and what remains out-of-scope (e.g., containerised
   dev environment, IDE-specific integration,
   remote-dev workflows).
4. Preserved byte-identical runtime, install, and
   distribution boundaries: Track G stdio path, Track H
   HTTP path, Track I installer round-trip, Track J
   reverse-proxy posture, Track K diagnostic harness,
   Track L service-supervision recipe + systemd
   template, Track M distribution-boundary recipe +
   wheel-build flip, Track N observability recipe — all
   unchanged.

---

## §6. What is in scope

- Planning, audit, contract, narrow implementation,
  docs-alignment, and closure for dev-time editable
  install + workspace discovery + dev bootstrap
  boundary.
- Defining what counts as a "supported dev-time
  workflow" concretely for this repo.
- Defining whether Step 4 targets:
  - **PATH A** — dev-time docs-only formalization (no
    `pyproject.toml` or `scripts/*` change; recipe
    formalises today's `bootstrap_paths.ps1`-plus-
    optional-editable workflow with explicit non-goals);
  - **PATH B** — docs + narrow `pyproject.toml` and/or
    `scripts/*` support for editable install (e.g.,
    document `pip install -e .` as supported; possibly
    add a `bootstrap_paths.sh` cross-OS sibling);
  - **PATH C** — docs + narrow developer bootstrap
    helper (e.g., a single dev-onboarding script that
    wraps install + selfcheck for new contributors).
- Defining whether dev-time stays cross-OS neutral or
  names one primary supported developer OS.
- Defining how dev-time relates to current
  deploy-time / install / service / packaging /
  observability truths (cross-references only; no
  redesign).
- Preserving compatibility with all Tracks G/H/I/J/K/
  L/M/N invariants.

## §7. What is out of scope

The following are intentionally **not** Track O scope.
Each is denied explicitly to prevent silent expansion:

- **No new MCP tools.** Registry invariant `read = 15 /
  write = 25 / intelligence = 16` must carry through
  all six Track O steps.
- **No registry changes** of any kind.
- **No transport redesign.** Track G stdio + Track H
  HTTP preserved byte-identical.
- **No auth redesign.** Track H static bearer + Track I
  round-trip integrity + Track D `${ENV:NAME}`
  substitution preserved byte-identical.
- **No deployment-boundary redesign.** Track J reverse-
  proxy / TLS-termination model preserved byte-
  identical.
- **No service-supervision redesign.** Track L recipe +
  systemd template preserved byte-identical.
- **No packaging redesign.** Track M wheel-build +
  recipe preserved byte-identical. No new
  `[project.scripts]` entry. No new dependency.
- **No observability redesign.** Track N recipe
  preserved byte-identical.
- **No containerised dev environment.** No Dockerfile
  bundled, no `docker-compose.yml`, no `.devcontainer/`
  configuration.
- **No IDE-specific integration.** No VSCode
  `.vscode/`, no JetBrains `.idea/`, no Cursor /
  Zed / Sublime / Vim project files bundled.
- **No remote-dev workflow.** No GitHub Codespaces
  config, no GitPod, no Coder template.
- **No CI redesign.** `.github/workflows/dev-check.yml`
  preserved byte-identical (Track O may eventually
  extend the workflow file in Step 4 only if Step 3
  contract authorises and only for the editable-
  install verification path, but the default
  expectation is to keep CI untouched).
- **No production code change.** `apps/*/src/`,
  `packages/*/src/` byte-identical to Track N closure
  state `2737a52`.
- **No new transport family, no auth-scheme change,
  no new endpoint.**
- **No `1cv8.exe` work.**
- **No remote push.** GitHub push remains operator
  decision.
- **No "developer workflow solved forever" / "all IDE
  integrations supported" / "all package managers
  supported for dev install" / "containerised dev
  environment shipped" / "remote-dev shipped" /
  "enterprise developer experience" claim.** Such
  phrases may appear in Track O docs only as explicit
  denials.

---

## §8. Guardrails

Each guardrail is verifiable on the post-Step-1 commit
and must remain verifiable through Step 6:

1. **Tracks A–N invariants byte-identical.**
   `apps/*/src/`, `packages/*/src/`,
   `docs/operators/deployment-boundary.md`,
   `docs/operators/service/service-supervision.md`,
   `docs/operators/service/mcp-server.service`,
   `docs/operators/packaging/distribution-boundary.md`,
   `docs/operators/observability.md` not touched by
   any Track O step. The dev-time boundary is a
   different axis from deployment / service / packaging
   / observability boundaries; cross-references only.
2. **`pyproject.toml`** byte-identical at Steps 1 / 2 /
   3 / 5. Step 4 MAY modify `pyproject.toml` only if
   Step 3 contract explicitly authorises PATH B (e.g.,
   adding a documentation-discoverable
   `[tool.hatch.build.targets.wheel.hooks.*]` editable
   hint or a comment block formalising the editable-
   install posture). Step 6 MAY further modify
   `pyproject.toml` `version` only if Q7 = PATCH;
   default expectation Q7 = NO-BUMP under PATH A.
3. **Registries invariant.** `selfcheck.py` registries
   `read=15 / write=25 / intelligence=16` must remain
   confirmed green at every step.
4. **No new MCP tools** at any step.
5. **No new CLI flag on existing servers.** No new
   flag added to `mcp-read-server` /
   `mcp-write-server` / `mcp-intelligence-server`. The
   existing flag surface
   (`--transport`, `--config-path`, `--log-level`,
   `--bind`, `--auth-token-env`) is locked.
6. **No new entrypoint module.** No new `__main__.py`
   in any `apps/*/src/` package.
7. **No new project dependencies.** Step 4 must not
   add to `[project.dependencies]` or
   `[project.optional-dependencies]`. Stdlib-only
   orientation of the runtime preserved.
8. **`scripts/dev/selfcheck.py`** byte-identical at
   every step.
9. **`scripts/dev/mcp_client_smoke.py`** byte-
   identical at every step.
10. **`scripts/release/*`** byte-identical at every
    step (`install.ps1`, `verify-release.ps1`,
    `_install_runner.py`, `README.md`).
11. **`docs/release-handoff.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add narrow
    CLASS-1 updates if a new dev-onboarding recipe
    becomes operator-discoverable; default
    expectation is at most one new bullet in "Where
    to read deeper".
12. **`apps/platform/README.md`** byte-identical at
    every step.
13. **`SECURITY.md`** byte-identical at every step.
14. **README.md "Closed parallel tracks" list** byte-
    identical at Steps 1 / 2 / 3 / 4 / 5 (still
    14 entries: A through N). Only Step 6 extends
    it to 15 entries (A through O).
15. **`CHANGELOG.md`** byte-identical at Steps 1 / 2 /
    3 / 4 / 5. Only Step 6 appends a Track O
    closure entry.
16. **No `1cv8.exe` runs** at any step.
17. **No remote push** at any step.
18. **No real credentials** in any committed file. All
    examples must use abstract placeholders.
19. **No premature closure language.** Steps 1–5 may
    not describe Track O as "закрыт" / "closed".
20. **No false implementation claims.** Step 1 plan
    must present Q1–Q7 as **defaults** and
    **recommendations**, not as decided answers.
21. **Step 4 file-surface cap.** Step 3 contract MUST
    pin a maximum number of touched files (default
    expectation: ≤ 3 — at most one recipe doc + at
    most one narrow declarative slice + at most one
    accompanying file). Step 3 may tighten.
22. **Step 4 LOC cap.** Default expectation: ≤ 200
    LOC stdlib-only, no new dependencies. Step 3
    may tighten.

---

## §9. Acceptance criteria for eventual closure

By Step 6 commit:

1. Track O has shipped **at most one new architecture
   plan-doc, one new step-map doc, one new baseline-
   audit doc, one new normative contract doc, and
   (Step 4) at most three new files or surgical
   modifications** under Step 3 contract caps.
2. Production code (`apps/*/src/`, `packages/*/src/`)
   byte-identical to Track N closure state `2737a52`.
3. `pyproject.toml` `version` either unchanged
   (`0.5.2`, Q7 = NO-BUMP) or bumped per Q7 rule.
4. Registries `read=15 / write=25 / intelligence=16`
   carried through unchanged.
5. README / PROJECT-STATUS / CHANGELOG closure
   narrative present and honest: explicit denial of
   "developer workflow solved forever", "all IDE
   integrations supported", "all package managers
   supported for dev install", "containerised dev
   environment shipped", "remote-dev shipped",
   "enterprise developer experience" claims; explicit
   statement of which dev-time boundary Track O
   settled; explicit Q7 reasoning.
6. `verify-release.ps1` GREEN on 8 checks at every
   step.
7. `selfcheck.py` `status=ok` at every step.
8. No real credentials anywhere in committed text.
9. No `1cv8.exe` runs anywhere in the track.
10. No remote push performed automatically by any
    step.
11. Track O moved into README's "Closed parallel
    tracks" list, growing it from fourteen to fifteen
    closed tracks (A through O).

---

## §10. Honest constraints after closure

These constraints remain after Track O closure:

- **No "production-ready developer experience"
  claim.** Track O's closure-gate covers one narrow
  dev-time-boundary slice; broader DX matrices
  recommended-only.
- **No containerised dev environment.** No bundled
  Dockerfile / `docker-compose.yml` / `.devcontainer/`.
- **No IDE-specific bundles.**
- **No remote-dev / Codespaces / GitPod / Coder
  template.**
- **No CI dev-install rollout.** If Step 4 = PATH B
  authorises a CI editable-install verification step,
  it stays narrow.
- **No multi-version-Python matrix.** Python 3.11
  remains the pinned dev version (`.python-version`).
- **No new MCP tools / registry change.**
- **No `1cv8.exe` runs.**

---

## §11. Relationship to Tracks G/H/I/J/K/L/M/N

| Aspect | Track M (deploy-time packaging) | Track N (observability) | Track O (this — dev-time) |
| --- | --- | --- | --- |
| Audience | Operator receiving a wheel | Operator running a deployed server | Contributor / internal developer editing the repo in place |
| Lifecycle moment | Deploy-time (build + install) | Runtime / operate-time | Dev-time (clone + edit + iterate) |
| Primary input | `python -m build` → `.whl` | Running server, stderr, exit codes | Cloned checkout |
| Primary verb | `pip install <WHEEL_PATH>` | (no install verb — runtime observation) | TBD by Step 3 contract; default candidate: `pip install -e .` and/or `bootstrap_paths` |
| Cross-OS | Cross-OS neutral via pure-Python wheel | Linux/systemd/journald primary; Windows/macOS prose-only | TBD; default candidate: cross-OS neutral with PowerShell + POSIX-shell parity if §10 §13 §14 hold |
| Code touched? | NO production code; one `pyproject.toml` flip + one recipe (Step 4 PATH B) | NO production code; one recipe | **TBD by Step 3 contract** (default expectation: ≤ 3 files; possibly one recipe + at most one narrow `pyproject.toml`/`scripts/*` adjustment) |
| New transport? | NO | NO | NO |
| New endpoint? | NO | NO | NO |
| New CLI flag? | NO | NO | NO (Q-O-out invariant) |
| Registry change? | NO | NO | NO |
| SemVer outcome | PATCH (0.5.1 → 0.5.2) | NO-BUMP (under 0.5.2) | **TBD** (default = NO-BUMP if PATH A; PATCH considered only under PATH B/C with honest defect-class dev-workflow repair; see §12.Q7) |

Track O inherits all preceding tracks' invariants and
adds none that conflict with them.

---

## §12. Open questions Q1–Q7 with directional defaults

These are **defaults / directional recommendations**,
not decided answers. Step 2 audit may move them; Step 3
contract locks them.

### Q1 — what counts as "dev-time editable install / workspace discovery" for closure?

**Options.**
- **(A)** One supported dev-time workflow recipe only —
  formalises today's `bootstrap_paths.ps1` plus a
  documented (but unimplemented-in-CI) `pip install -e
  .` posture; no code/config change.
- **(B)** Recipe **plus** one narrow `pyproject.toml`
  /`scripts/*` adjustment that explicitly supports
  editable install (e.g., a `[tool.hatch.build.targets.
  wheel.hooks.*]` editable-mode hint, or a sibling
  `bootstrap_paths.sh`).
- **(C)** Recipe **plus** one narrow developer
  bootstrap helper (e.g., a single dev-onboarding
  script that wraps install + selfcheck for new
  contributors).

**Default recommendation.** **(A) recipe-only** as the
narrowest honest closure. **(B)** acceptable as
fallback if Step 2 audit reveals that
`bootstrap_paths.ps1`-PowerShell-only is a real
cross-OS friction for contributors. **(C)** rejected
by default — a dev-onboarding helper duplicates
existing `launch.ps1` surface for marginal value.

### Q2 — primary problem focus?

**Options.**
- **(A)** Dev-time editable install and workspace
  discovery for contributors / internal developers,
  full stop.
- **(B)** (A) plus user-side install (e.g., an
  end-user wanting to `pip install -e <git-url>`
  becomes a documented case).
- **(C)** Broader "developer experience" axis
  including formatter / linter / test-runner policies.

**Default recommendation.** **(A) narrow contributor
focus.** Operators receive a built wheel (Track M).
End-users running the platform receive whatever the
operator distributes. Track O scope is the
contributor-editing-the-repo case. **(B)** rejected by
default — installable-from-git-URL is a different
workflow with different threat-model implications.
**(C)** rejected by default — formatter / linter /
test-runner policies are orthogonal to editable
install.

### Q3 — Step 4 PATH openness

**Options.**
- **PATH A** — docs-only dev-time-boundary recipe.
- **PATH B** — docs + narrow `pyproject.toml` /
  `scripts/*` declarative slice (e.g., add
  `bootstrap_paths.sh`; or add an editable-install
  comment block to `pyproject.toml` symmetric to the
  Track M wheel-build comment block).
- **PATH C** — docs + narrow developer bootstrap
  helper script.

**Default recommendation.** **PATH A is the most
likely outcome**, with PATH B held in reserve if Step
2 audit shows that the dev-time gap genuinely needs a
cross-OS bootstrap-paths sibling or an editable-
install pyproject hint to be honestly closed. **Do
not lock Step 4 PATH at Step 1**; Step 3 contract is
the lock point.

### Q4 — minimum closure scope

The eventual closure document MUST answer at minimum:

- How a developer installs from a checkout (editable
  install command + supported tooling preconditions).
- Whether `pip install -e .` is supported; if yes,
  what it provides; if no, what alternative is
  supported.
- How workspace discovery works (which src-layout
  paths are dev-time PYTHONPATH entries vs. wheel-
  build `packages` entries — currently the same
  eleven, per Track M).
- What exact dev workflow is first-class supported.
- What is recommended-only (e.g., specific tools
  like `pdm` / `uv` / `hatch` if used by individual
  contributors).
- What is explicitly out-of-scope (containerised
  dev, IDE integrations, remote-dev, multi-Python-
  version matrix).

### Q5 — what is insufficient as closure proof?

- **"Just clone the repo."** Repo cloning is
  necessary but not sufficient — without
  PYTHONPATH bootstrap or editable install, imports
  fail.
- **"`pip install -e .` maybe works."** Maybe-works
  is not a supported boundary.
- **Ad-hoc tribal knowledge in commit messages.**
- **Scattered comments in `scripts/dev/*.ps1`.**
- **Generic "set up your IDE" prose.**

A supported boundary requires a single document
stating what works, what is recommended-only, and
what is out-of-scope, with operator-runnable
verification.

### Q6 — does Track O likely require production code at all?

**Default recommendation.** **No.** The gap is
declarative / dev-tooling / documentation boundary —
adjacent to `pyproject.toml` and `scripts/*` but not
to runtime code. Step 2 audit must verify this
honestly, but the default expectation is that no
`apps/*/src/` or `packages/*/src/` change is
warranted.

### Q7 — SemVer expectation

**Options.**
- **(A)** NO-BUMP. Track O closes under existing
  `0.5.2` if Step 4 = PATH A docs-only. Mirrors
  Track J / Track K / Track L / Track N NO-BUMP
  precedents.
- **(B)** PATCH `0.5.2 → 0.5.3`. Track O closes with
  a PATCH bump only if Step 4 = PATH B with an
  honest defect-class declarative repair (e.g.,
  closing the long-standing
  `scripts/dev/README.md:5-11` "editable install и
  workspace discovery всё ещё out of scope" gap by
  flipping `pip install -e .` from undocumented-but-
  works to documented-and-tested). Mirrors Track I /
  Track M PATCH precedents.
- **(C)** MINOR `0.5.2 → 0.6.0`. Explicitly
  rejected by guardrails §8.5 (no new CLI flag) and
  §8.7 (no new project dependency); MINOR not
  warranted by docs-only or narrow declarative
  changes.

**Default recommendation.** **(A) NO-BUMP** as the
most likely outcome; **(B) PATCH** acceptable only
under Step 4 PATH B with honest defect-class framing;
**(C) MINOR** explicitly rejected. **(D) MAJOR**
forbidden by track scope.

---

## §13. Six-step trajectory preview

| Step | Kind | Default file surface | Default scope cap |
| --- | --- | --- | --- |
| Step 1 (this) | planning | 2 new docs + README + PROJECT-STATUS | docs-only |
| Step 2 | descriptive baseline audit | 1 new doc under `docs/architecture/track-o-*-baseline-audit.md` | docs-only |
| Step 3 | normative contract | 1 new doc under `docs/architecture/track-o-*-contract.md` | docs-only |
| Step 4 | narrow implementation (PATH A / B / C) | ≤ 3 new files or surgical modifications (default expectation under PATH A = one recipe at `docs/dev/editable-install.md` or `docs/contributors/dev-workflow.md`; under PATH B = recipe + at most one narrow `pyproject.toml` or `scripts/*` adjustment) | locked by Step 3 contract |
| Step 5 | docs / operator / release alignment | narrow CLASS-1 only: README, possibly `docs/release-handoff.md`, possibly `docs/developer-manual.md`, possibly `scripts/dev/README.md`; NO production code | scope locked by Step 3 contract |
| Step 6 | final integration pass and track closure | README + PROJECT-STATUS + CHANGELOG; optionally `pyproject.toml` if Q7 = PATCH | NO production code; Q7 decision explicit |

---

## §14. Honest summary

**What Track O will do.** Convert the "no first-class
dev-time editable install / workspace discovery
boundary" gap into one contributor-facing recipe (and,
if Step 3 contract pins PATH B, one narrow
`pyproject.toml` or `scripts/*` adjustment that makes
editable install or cross-OS bootstrap supported by
construction), preserving every Tracks A–N invariant
byte-identical.

**What Track O will not do.** It will not introduce a
broader developer-experience platform (no containerised
dev, no IDE integrations, no remote-dev / Codespaces /
GitPod / Coder, no multi-Python-version matrix, no
formatter / linter / test-runner policy redesign);
will not add new MCP tools; will not change
registries; will not run `1cv8.exe`; will not push to
GitHub automatically.

**Why this is the next right narrow track.**
`scripts/dev/README.md:5-11` was committed with an
explicit "editable install и workspace discovery всё
ещё out of scope" sentence during Track M / Step 4;
Track M itself only closed the deploy-time packaging
boundary. The dev-time boundary remained explicitly
deferred. Track O closes that long-standing constraint
the same way Track N closed observability and Track M
closed packaging: one document and at most one narrow
declarative slice, with explicit denial of the
broader claims a less disciplined version of the same
track would make.

**Default Q7 outcome.** **NO-BUMP** if Step 4 PATH A
(docs-only); **PATCH** if Step 4 PATH B (narrow
declarative flip closing the explicit
`scripts/dev/README.md` honest constraint). Q7 lock
is Step 6 territory.
