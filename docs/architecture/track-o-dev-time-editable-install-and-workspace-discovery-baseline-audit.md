# Parallel Track O — Dev-Time Editable Install and Workspace Discovery — Baseline Audit

**Step status.** Parallel Track O / Step 2 — descriptive
baseline audit. Companion to
[track-o-dev-time-editable-install-and-workspace-discovery-plan.md](track-o-dev-time-editable-install-and-workspace-discovery-plan.md)
(Step 1 planning, Q1–Q7 directional defaults) and
[track-o-dev-time-editable-install-and-workspace-discovery-step-map.md](track-o-dev-time-editable-install-and-workspace-discovery-step-map.md)
(Step 1 six-step boundary).

This document is **descriptive**, not normative. It
inventories what dev-time editable install / workspace
discovery / bootstrap surfaces already exist at HEAD
`4122431` (project version `0.5.2`), classifies them,
and produces **directional** Q1–Q6 resolutions grounded
in the repo evidence below. It does **not** use RFC 2119
MUST / MUST NOT / SHOULD / SHOULD NOT / MAY language;
that vocabulary is reserved for the Step 3 normative
contract.

The audit explicitly does **not** decide Step 4 path
dogmatically. The intent is to give Step 3 a credible
evidence base, not to pre-empt Step 3.

---

## §1. Purpose / scope

### §1.1 What this document is

A single descriptive audit covering:

- Dev-time surfaces actually present in the repo at
  `4122431` (`scripts/dev/*`, `pyproject.toml`,
  `.python-version`, `.github/workflows/dev-check.yml`).
- Adjacent release-time surfaces only where they help
  draw the dev-time vs deploy-time boundary
  (`scripts/release/README.md`,
  `docs/operators/packaging/distribution-boundary.md`).
- The honest gap between "there is some bootstrap
  scaffolding" and "there is a supported dev-time
  editable install / workspace discovery boundary".
- Directional Q1–Q6 resolutions to hand off into
  Step 3.

### §1.2 What this document is **not**

- Not a contract. No MUST / MUST NOT / SHOULD.
- Not a Step 4 implementation decision.
- Not a forecast of every possible future dev-tooling
  surface. Out-of-scope categories (containerised
  dev / IDE integrations / remote-dev / multi-Python-
  version matrix / formatter-linter-test-runner
  policy redesign / alternative build-backend
  evaluation) are named only for boundary hygiene,
  not analysed for feasibility.
- Not a rewrite or amendment of Step 1 planning docs.
  Step 1 plan + step-map remain the planning anchors;
  this audit complements them with repo evidence.

### §1.3 What the audit explicitly preserves

- Tracks A–N closure invariants byte-identical
  (verifiable via `git diff 2737a52 -- apps/
  packages/ scripts/ docs/operators/`, etc.).
- Registry invariant `read=15 / write=25 /
  intelligence=16` (verifiable via `python
  scripts/dev/selfcheck.py`).
- No production code change.
- No `pyproject.toml`, `scripts/*`, `SECURITY.md`,
  `docs/release-handoff.md`, `apps/platform/README.md`,
  `CHANGELOG.md`, `README.md`, `PROJECT-STATUS.md`
  edit in this step.

---

## §2. Method / evidence sources

The audit is grounded in direct repo inspection at
`4122431`. Specifically:

- **`pyproject.toml`** read end-to-end (64 lines).
- **`.python-version`** read end-to-end (1 line).
- **All `scripts/dev/*` files inspected directly.**
  `bootstrap_paths.ps1` (32 lines); `launch.ps1` (146
  lines); `run_dev_check.ps1` (22 lines);
  `selfcheck.py` (110 lines); `mcp_client_smoke.py`
  (Track K artefact — Track K closure-locked, not
  modified by Track O); `README.md` (198 lines —
  contains the explicit hand-off marker).
- **`scripts/release/README.md`** read in the
  dev-vs-deploy-boundary delimiting section
  (operator-facing prose; not modified by Track O).
- **`docs/operators/packaging/distribution-boundary.md`**
  surveyed for dev-time terminology hits (zero hits —
  see §3.10).
- **`.github/workflows/dev-check.yml`** read end-to-end
  (25 lines; carries forward unchanged from Track N
  audit).
- **`.gitignore`** surveyed for dev-tooling artefact
  patterns.
- **Whole-repo grep** on dev-time vocabulary —
  `pip install -e`, `editable`, `PEP 660`,
  `setup.py develop`, `develop-mode`, `bootstrap`,
  `workspace`, `monorepo`, `PYTHONPATH`.
- **Filesystem check** for `tests/` directory
  (declared in `[tool.pytest.ini_options]` but
  inspected to confirm existence).

All findings below cite file paths plus line numbers
so Step 3 can verify directly.

---

## §3. Current dev-time baseline

### §3.1 `pyproject.toml` — build backend and project metadata

Repo evidence (`pyproject.toml:1-13`):

- `[build-system]` line 1-3: `requires = ["hatchling"]`;
  `build-backend = "hatchling.build"`. Hatchling is
  the declared build backend.
- `[project]` line 5-13: `name = "1c-agent-platform"`,
  `version = "0.5.2"`, `description = "Platform for
  working with 1C configurations through MCP"`,
  `requires-python = ">=3.11"`, `readme = "README.md"`,
  one `authors` entry.

Implication for dev-time: hatchling supports PEP 660
editable installs by default (no extra hook needed
when `[tool.hatch.build.targets.wheel] packages` is
populated). Since Track M / Step 4 populated that
array, `pip install -e .` from the repo root is
**mechanically possible** today. There is **no
explicit declaration** in `pyproject.toml` that
editable install is a supported workflow.

### §3.2 `pyproject.toml` — `[project.dependencies]` absent

Whole-file grep for `[project.dependencies]` returns
zero hits. The `[project]` block at lines 5-13 does
not include any `dependencies = [...]` entry. The
project therefore declares **no runtime dependencies
beyond the standard library**. Hatchling itself is
declared only in `[build-system].requires` (a build-
time-only dependency invoked by `python -m build` or
by `pip install` when constructing a wheel).

Implication for dev-time: a contributor performing
`pip install -e .` will install only the project's
own packages and nothing else. There is no
dev-extras declaration (`[project.optional-dependencies]
dev = [...]`) — formatter / linter / test-runner /
debug tooling is left entirely to the contributor's
own discretion.

### §3.3 `pyproject.toml` — `[project.scripts]` console entries

`pyproject.toml:22-25`:

```
mcp-read-server = "mcp_read_server.__main__:main"
mcp-write-server = "mcp_write_server.__main__:main"
mcp-intelligence-server = "mcp_intelligence_server.__main__:main"
```

Three console entries declared. Per the wheel-build
flip (Track M / Step 4), these become installable as
executable binaries when the wheel is installed via
`pip install <WHEEL_PATH>`. **By the same mechanism,
`pip install -e .` would also install them as
editable-mode console scripts** — but this is not
documented as a supported dev workflow.

### §3.4 `pyproject.toml` — `[tool.ruff]` and `[tool.pytest.ini_options]`

`pyproject.toml:27-32`:

```
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Two tooling configuration blocks are present:

- `[tool.ruff]` — configures the `ruff` linter (line-
  length 100, Python 3.11 target). Not declared as a
  runtime or build-time dependency; contributors who
  invoke `ruff` must install it themselves.
- `[tool.pytest.ini_options]` — declares the test
  discovery path as `tests/`. **Filesystem check
  shows `tests/` does not exist** at HEAD `4122431`
  (`ls tests/` returns "tests/ does not exist").
  The declaration is therefore aspirational; no test
  suite is shipped.

Implication for dev-time: the project declares
opinions about tooling (ruff line-length, pytest
testpaths) but does not install or supply those
tools. A contributor running `ruff check` or `pytest`
must bring those tools themselves; neither is part
of any documented dev workflow today.

### §3.5 `pyproject.toml` — `[tool.hatch.build.targets.wheel] packages`

`pyproject.toml:34-63`:

```
[tool.hatch.build.targets.wheel]
# Track M / Step 4 — narrow supported distribution boundary.
# ...
packages = [
    "apps/mcp-read-server/src/mcp_read_server",
    "apps/mcp-write-server/src/mcp_write_server",
    "apps/mcp-intelligence-server/src/mcp_intelligence_server",
    "apps/platform/src/onec_platform",
    "packages/mcp-common/src/mcp_common",
    "packages/onec-process-runner/src/onec_process_runner",
    "packages/onec-policy-engine/src/onec_policy_engine",
    "packages/onec-audit/src/onec_audit",
    "packages/onec-health/src/onec_health",
    "packages/onec-troubleshooting/src/onec_troubleshooting",
    "packages/onec-config/src/onec_config",
]
```

Eleven src-layout package paths. The Track M / Step 4
comment block (lines 35-50) explicitly frames this as
the **deploy-time** boundary; "Operator recipe:
`docs/operators/packaging/distribution-boundary.md`."
The comment names broader-packaging non-goals (no
PyPI, no signed distribution, no GUI installer, no
Chocolatey/Homebrew/apt) and says "The install-fast-
path (`scripts/release/install.ps1`) and the wheel
are orthogonal-but-complementary axes; see the
recipe."

Implication for dev-time:

- The same eleven src-layout paths are simultaneously
  (a) the wheel-build `packages = [...]` array
  (deploy-time, Track M), and (b) the PYTHONPATH
  entries set by `scripts/dev/bootstrap_paths.ps1`
  (dev-time, see §3.7 below). **Workspace
  discovery currently has two sources of truth that
  happen to agree.**
- No `[tool.hatch.build.targets.wheel.hooks.*]`
  block exists. Hatchling will use its default
  editable behaviour if `pip install -e .` is
  invoked.

### §3.6 `.python-version`

`.python-version:1`: `3.11`. Single line. Pins the
Python interpreter version for tooling that honours
this file (`pyenv`, `mise`, certain CI runners).
`pyproject.toml:9` independently declares
`requires-python = ">=3.11"`. The two declarations
agree; the file is the dev-time anchor and the
pyproject directive is the install-time anchor.

### §3.7 `scripts/dev/bootstrap_paths.ps1`

32-line PowerShell script (`bootstrap_paths.ps1:1-32`).
Sets `$env:PYTHONPATH` for the **current PowerShell
session only** (`bootstrap_paths.ps1:24`). The eleven
src paths added (lines 9-21) mirror exactly the
`[tool.hatch.build.targets.wheel] packages` array in
§3.5 above (different separator: Windows path
delimiter `\` here; package-path slash `/` there).

Explicit constraints visible in the script:

- Comment line 2-3: "Sets PYTHONPATH for the 1C Agent
  Platform monorepo in the current session only. Does
  not touch the system PATH or the registry."
- Line 5: `$ErrorActionPreference = "Stop"` — strict
  failure on any error.
- Line 7: `$root = (Resolve-Path (Join-Path $PSScriptRoot
  "..\..")).Path` — repo-root-relative; assumes the
  script lives at `scripts/dev/`.
- Line 26-31: human-readable confirmation output
  ("PYTHONPATH set for this PowerShell session.").

Implication for dev-time: this is the **only**
in-repo workspace-discovery mechanism. It is
PowerShell-only — no `.sh` sibling for Linux/macOS
contributors exists in the repo.

### §3.8 `scripts/dev/launch.ps1`

146-line PowerShell umbrella (`launch.ps1:1-146`).
Track B / Step 4. Thin dispatcher over
`bootstrap_paths.ps1` + `run_dev_check.ps1` (lines
44-45 declare both as discovered relative to
`$PSScriptRoot`). Subcommands defined at lines 104-145:

- `help` / `--help` / etc. (lines 105-108) — prints
  usage and exits 0.
- `selfcheck` (lines 110-117) — delegates to
  `run_dev_check.ps1`.
- `repl` (lines 119-126) — dot-sources
  `bootstrap_paths.ps1`, then launches `python` REPL.
- `run <script> [args...]` (lines 128-139) — dot-
  sources bootstrap, then `python @Rest`.
- default (lines 141-145) — unknown command → exit
  64.

Explicit non-goals enumerated in the file header
(lines 11-31):

- Does NOT start the three MCP servers
  (`mcp-read-server` / `mcp-write-server` /
  `mcp-intelligence-server`).
- Does NOT run pytest (the comment at line 28
  states verbatim "there is no test suite yet").
- Does NOT run the install fast path
  (lines 29-30 redirect to
  `scripts\release\install.ps1`).
- Does NOT touch a 1C infobase.

Implication for dev-time: `launch.ps1` is a
discoverability surface (a single entry point that
helps a new contributor learn the bootstrap + REPL +
script-run workflow) but is **not** an install
boundary. It does not document or invoke
`pip install -e .` at any point.

### §3.9 `scripts/dev/run_dev_check.ps1`

22-line PowerShell script (`run_dev_check.ps1:1-22`).
Dot-sources `bootstrap_paths.ps1` (line 12) and then
runs `python selfcheck.py` (line 14). On success
prints `Dev check completed successfully.` (lines
17-18); otherwise propagates the Python exit code
(lines 19-20). Same `$ErrorActionPreference = "Stop"`
discipline as the bootstrap script.

This script is referenced from
`.github/workflows/dev-check.yml` (per `scripts/dev/
README.md:184-187`). It is the project's **only
quality gate** today.

### §3.10 `scripts/dev/selfcheck.py`

110-line Python script (`selfcheck.py:1-110`).
Behaviour was fully audited at Track N / Step 2 (§3.7
of `track-n-observability-and-diagnostics-boundary-baseline-audit.md`),
and remains byte-identical at HEAD `4122431`. Key
properties relevant for Track O:

- Imports modules from all seven library packages
  plus the three MCP server packages (lines 7-29).
  Operates on PYTHONPATH set by `bootstrap_paths.ps1`
  (or by a wheel install).
- No `try/except` (docstring line 4 — "No
  try/except: if anything is wired incorrectly, we
  want a loud, honest failure.").
- Prints 11 key=value lines (lines 95-105),
  terminating with `selfcheck_status = ok`.
- Exit code 0 on success; non-zero on any
  ImportError or registry mismatch.

Implication for dev-time: `selfcheck.py` is the
indirect proof that workspace discovery worked —
if all imports succeed, all eleven src-layout
packages are importable. It is **not** an install
boundary itself.

### §3.11 `scripts/dev/mcp_client_smoke.py`

Track K closure-locked harness. Per Track K / Step 6
classification, this is a developer/operator
diagnostic file, **not** an install or workspace-
discovery artefact. It is mentioned here only to
acknowledge its existence under `scripts/dev/` and
to flag that it is **not part of Track O's scope**
(byte-identical preservation per Track O step-map
invariant §10).

### §3.12 `scripts/dev/README.md` — the explicit hand-off marker

198-line README. The most important sentence for
Track O is at lines 5-11 (verbatim):

> "На текущем этапе это временный bootstrap для
> монорепы: editable install и workspace discovery
> всё ещё out of scope. Track M / Step 4 ввёл узкий
> supported distribution boundary — один buildable
> `py3-none-any` wheel (см.
> [`docs/operators/packaging/distribution-boundary.md`](../../docs/operators/packaging/distribution-boundary.md)),
> но он покрывает `pip install` deployment flow, не
> dev-time editable install."

This sentence was committed during Track M / Step 4
as an explicit hand-off marker. It is the most
concrete in-repo evidence that the dev-time boundary
is intentionally deferred and that a future track
is expected to close it.

A second occurrence appears in the "Статус"
section at lines 192-198 (verbatim):

> "Это временный bootstrap-этап. Track M / Step 4
> закрыл deploy-time packaging boundary (один
> buildable wheel, см. `docs/operators/packaging/
> distribution-boundary.md`); dev-time editable
> install, workspace discovery и CLI-скрипты под
> local-dev workflow по-прежнему out of scope."

Two anchors → unambiguous: the dev-time gap is
**explicitly** declared, not implicitly missing.

### §3.13 An older anchor — `docs/architecture/phase-1-entry.md`

`docs/architecture/phase-1-entry.md:79-82` (verbatim):

> "**Импортный wiring при реальном запуске.**
> Текущий `PYTHONPATH` bootstrap хорош для selfcheck,
> но для реального MCP-процесса потребуется
> нормальный packaging / workspace setup (editable
> install, entry points)."

This anchor predates Track M / Step 4 by many tracks
(it is part of the original Phase 1 entry document).
It identifies the same gap that Track O addresses,
framing PYTHONPATH-bootstrap as a transitional
arrangement that would eventually need editable
install + entry points. Track M closed the entry-
points half (now installable via wheel); the
editable-install half is what Track O addresses.

### §3.14 `scripts/release/README.md` — dev-vs-deploy delimitation

`scripts/release/README.md:6-15` (verbatim):

> "This directory holds two thin wrappers: …
> `install.ps1` — operator-facing entry to the
> install fast path (Track B / Step 3).
> `verify-release.ps1` — pre-handoff release sanity
> check (Track C / Step 2).
> Neither introduces a new install ecosystem — no
> `.msi`, no `.deb`, no GUI wizard, no signed
> distribution — they only make existing
> capabilities operator-discoverable and verify
> release-facing invariants."

Implication: `scripts/release/*` is explicitly framed
as operator-facing and release-time. It does not
overlap with dev-time editable install; it covers
the orthogonal operator workflow that follows after
a wheel is built (or after the install fast path
materialises a `ProductConfig` JSON).

`scripts/release/install.ps1` does dot-source
`scripts/dev/bootstrap_paths.ps1` (per release/README
lines 24-26), which is an interesting cross-boundary
detail: the operator install fast-path still relies
on the dev-time PYTHONPATH bootstrap for its own
in-process invocation. This is acceptable because
the operator runs the install script from a
checkout; it does not imply that operators use
editable install.

### §3.15 `docs/operators/packaging/distribution-boundary.md` — zero dev-time hits

Whole-file grep on `developer` / `dev-time` /
`editable` returned **zero hits** at HEAD
`4122431`. The Track M recipe is exclusively
operator-facing and exclusively deploy-time. This
confirms Track O's orthogonality claim: the two
tracks address different lifecycle moments
(`pip install <WHEEL_PATH>` deploy-time vs
`pip install -e .` dev-time-candidate) and
different audiences (operator receiving a wheel
artefact vs contributor editing the repo in
place).

### §3.16 `.gitignore`

`.gitignore` lines 7-66 (sampled): standard
patterns (`venv/`, `dist/`, `build/`,
`Thumbs.db`, `examples/demo-dumps/_snapshots/`,
`examples/demo-dumps/infobase6/`, etc.). No
editable-install-specific patterns
(`*.egg-info/`, `*.pth`, `__editable__.*`).
This is consistent with the fact that PEP 660
editable installs (which hatchling produces by
default) write only to the operator's
site-packages, not to the source tree — so no
gitignore entries are needed for editable
installs in the repo root. If future Track O
work changes that posture (e.g., a `tox`-style
dev-virtualenv directory under the repo root),
new `.gitignore` entries would be considered at
that point — but no such workflow exists today.

### §3.17 `.github/workflows/dev-check.yml`

25-line CI workflow (audited at Track N / Step 2
§3.12). On `push` and `pull_request`: checkout +
Python 3.11 setup + dot-source bootstrap + run
selfcheck. The CI **does not** exercise
`pip install -e .`, **does not** install the
wheel, and **does not** run `ruff` or `pytest`. The
only CI signal is selfcheck PASS/FAIL.

Implication for dev-time: CI today validates that
the PYTHONPATH-bootstrap workflow imports
successfully. It does not validate any editable-
install workflow.

### §3.18 `tests/` directory does not exist

Filesystem check: `ls tests/` at HEAD `4122431`
returns "does not exist". `pyproject.toml:32`
declares `[tool.pytest.ini_options] testpaths =
["tests"]`. The declaration is aspirational; no
test suite ships. This is **not** a Track O
concern (Track O is editable install / workspace
discovery, not test-runner policy); it is named
only to round out the inventory.

---

## §4. Existing reusable surfaces

The audit groups what is **already in the repo and
honestly reusable** for a Track O closure:

### §4.1 The eleven-element src-layout package list

Currently maintained in **two synchronised** places:

- `pyproject.toml:51-63` — `[tool.hatch.build.targets.
  wheel] packages` (Track M / Step 4 lock).
- `scripts/dev/bootstrap_paths.ps1:9-21` — the
  PYTHONPATH entries.

The two lists are byte-equivalent (modulo
path-separator). This means a contributor running
`pip install -e .` would get exactly the same set of
import-discoverable packages as a contributor
running `. .\scripts\dev\bootstrap_paths.ps1`. The
two workflows are functionally interchangeable for
import resolution.

### §4.2 Hatchling editable-install capability (latent)

Hatchling supports PEP 660 editable installs by
default when `[tool.hatch.build.targets.wheel]
packages` is populated. Since Track M / Step 4
populated it, the editable install path is
**latent**: it would mechanically work today, with
no `pyproject.toml` change required, if the
contributor runs `pip install -e .` from the repo
root. Track O's primary work in PATH A is to
**document** this latent capability and define its
supported scope; in PATH B it could be to **declare**
it explicitly via a `[tool.hatch.build.targets.
wheel.hooks.*]` comment block or similar.

### §4.3 `launch.ps1` umbrella

The discoverability surface is already present. A
new contributor reaching `launch.ps1` learns about
`selfcheck` / `repl` / `run`. A future Track O
recipe could extend this discoverability without
modifying `launch.ps1` itself, by documenting that
`launch.ps1 selfcheck` is the supported entry
point.

### §4.4 `selfcheck.py` as the dev-workflow verification gate

Already exists, already documented (Track N / FC4),
already wired into CI. A Track O recipe can use
"run `selfcheck.py` after install" as the canonical
verification step for any dev-time install workflow
(editable or otherwise) without modifying
`selfcheck.py`.

### §4.5 `.python-version` + `requires-python` agreement

Two-source-of-truth-but-synchronised Python 3.11
pin (§3.6). Reusable as a stable dev-time
prerequisite.

### §4.6 Stdlib-only runtime

`[project.dependencies]` is implicitly empty (§3.2).
This means a contributor's editable install
introduces no third-party dependencies into their
virtual environment. The contributor can manage
their own tooling (ruff / pytest / debuggers) without
fearing version-pin collisions with the platform.

### §4.7 The dev-vs-deploy boundary already drawn in prose

`scripts/dev/README.md:5-11` and the second
occurrence at lines 192-198 already state that
Track M is deploy-time and the dev-time gap remains.
Track O does not need to invent this distinction;
it needs to formalise it positively.

### §4.8 Track M wheel as a reference artefact

The buildable wheel produced by `python -m build`
(Track M / Step 4) is an existing reference for what
"installed" means at deploy time. A Track O recipe
can contrast that artefact against `pip install -e .`
without duplicating Track M's content.

---

## §5. Adjacent but insufficient surfaces

These exist but do not, on their own, close the
Step 1 gap:

### §5.1 `bootstrap_paths.ps1` alone

PowerShell-only. A Linux/macOS contributor cannot
dot-source it without `pwsh` installed (and even
then, the Windows path separators in
`bootstrap_paths.ps1:9-21` would not resolve to
existing directories on a POSIX filesystem). The
script is a working dev-time mechanism for one OS
family; it is not a cross-OS solution.

### §5.2 Latent `pip install -e .` capability alone

Mechanically works (see §4.2), but:

- Is not mentioned in any operator-facing or
  contributor-facing document anywhere in the repo.
- Is not exercised by CI.
- Has no verification recipe.
- Has no documented scope (does it install the
  three console scripts? does it expose all eleven
  packages on `sys.path`? what does it require the
  contributor to install first?).

A capability that exists in the build backend but
nowhere in operator-readable prose is not a
supported boundary.

### §5.3 `launch.ps1` alone

Discoverability surface for *post-bootstrap*
actions (selfcheck / repl / run). Does not address
the install step itself. A contributor must
already know to dot-source the bootstrap (or to
run `launch.ps1 selfcheck`, which invokes
`run_dev_check.ps1`, which dot-sources the
bootstrap) before any of this works.

### §5.4 `scripts/dev/README.md` alone

Names the gap (§3.12) but does not close it.
Documents the existing surface (`launch.ps1`,
`bootstrap_paths.ps1`, `selfcheck.py`,
`mcp_client_smoke.py`, `run_dev_check.ps1`) but
does not document an editable-install workflow
because no such workflow currently exists in
supported form.

### §5.5 `phase-1-entry.md` alone

Mentions the future need (§3.13) but is an
architecture document, not a recipe. It does not
unblock a contributor today.

### §5.6 `.github/workflows/dev-check.yml` alone

Validates the bootstrap+selfcheck workflow.
Does not validate any editable install. Cannot
serve as the implementation-covered proof for a
dev-time install workflow that is not yet
shipped.

### §5.7 Tribal / non-repo knowledge

A contributor familiar with hatchling can guess
that `pip install -e .` "probably works", but
that is not a repo-evidenced supported boundary.
Step 1 plan §12 Q5 explicitly identified this
as insufficient closure proof.

---

## §6. Clearly missing pieces

Items that **do not exist anywhere at `4122431`**
and would have to be created (or deliberately
denied as out-of-scope) for Track O closure:

### §6.1 A contributor-facing install recipe

No document under `docs/dev/`, `docs/contributors/`,
or any equivalent path covers "how to install the
platform from a checkout for editing". The
`docs/operators/` directory has four recipes
(deployment-boundary / service-supervision /
distribution-boundary / observability) — all
operator-facing.

### §6.2 A documented `pip install -e .` posture

Nothing in the repo states whether `pip install
-e .` is supported, recommended, tolerated, or
unsupported. Hatchling's default behaviour makes
it mechanically work, but the project takes no
position.

### §6.3 A cross-OS workspace-discovery answer

The PowerShell-only `bootstrap_paths.ps1` is the
only in-repo workspace-discovery mechanism. No
`.sh` sibling exists for POSIX hosts. Track L /
Track M recipes have cross-OS prose; the dev-time
bootstrap does not.

### §6.4 A first-class-vs-recommended-only-vs-out-of-scope classification

Track N (observability) demonstrated this
classification pattern (FC1–FC7 + R1–R4 + 10-item
out-of-scope). Nothing equivalent exists for the
dev-time workflow: which tools (`pip` / `build` /
`hatch` / `pdm` / `uv` / `tox` / `nox` / `ruff` /
`pytest`) are supported, recommended-only, or
explicitly out-of-scope?

### §6.5 An authoritative non-goals enumeration

No file collects "what the project does not
ship for dev workflow" into a single statement.
Out-of-scope items mentioned in Step 1 plan §7
(containerised dev, IDE integrations, remote-dev,
multi-Python-version matrix, etc.) live only in
the Step 1 plan doc; no contributor-facing
artefact reiterates them.

### §6.6 What is not missing

For honesty: a containerised dev environment,
IDE-specific bundles, a remote-dev workflow, a
multi-Python-version matrix, an alternative
build-backend evaluation, a formatter/linter/
test-runner policy redesign — are **not
missing** because **they are not in scope**.
They are out-of-scope per Step 1 plan §7 and
step-map hard out-of-scope list.

---

## §7. Directional Q1–Q6 resolutions

Per Step 1 plan §12, these are **defaults /
directional recommendations grounded in repo
evidence**, not decided answers. Step 3 contract
locks final answers.

### §7.1 Q1 — what counts as "dev-time editable install / workspace discovery" for closure?

**Step 1 default.** (A) one supported dev-time
workflow recipe — formalises today's
`bootstrap_paths.ps1` plus the latent
`pip install -e .` capability into one
positively-defined supported workflow.

**Audit-grounded recommendation.** **(A) recipe-
only** holds with high confidence:

- §4.2 establishes the editable install is latent
  (mechanically works today). What is missing is
  prose, not code.
- §4.1 establishes the eleven-element src-layout
  list is already synchronised between
  `pyproject.toml` (wheel-build) and
  `bootstrap_paths.ps1` (PYTHONPATH). Workspace
  discovery is not broken; it is undocumented.
- §3.10 / §4.4 establish that `selfcheck.py` is
  available as the verification gate without
  modification.

**PATH B** considered acceptable fallback only if
Step 3 audit reveals that the
PowerShell-only bootstrap is a real cross-OS
friction blocker. If so, a sibling
`bootstrap_paths.sh` (≤ 50 LOC stdlib-shell) or a
`pyproject.toml` editable-install comment block
mirroring the Track M wheel-build comment block
would be the narrowest declarative repair.

**PATH C** rejected by audit — a separate
dev-onboarding helper script would duplicate
`launch.ps1`'s discoverability surface for
marginal value.

### §7.2 Q2 — primary problem focus?

**Step 1 default.** (A) narrow contributor-facing
dev-time editable install + workspace discovery +
bootstrap boundary.

**Audit-grounded recommendation.** **(A)
confirmed.** Repo evidence supports the narrow
contributor focus:

- `scripts/dev/README.md:5-11` and 192-198 both
  frame the gap as "dev-time", not "user-side
  install" and not "DX policy".
- `phase-1-entry.md:79-82` frames the future need
  as "editable install, entry points" for the
  "real MCP-process" — a contributor's
  iterative development context, not an end-user
  install or a DX policy concern.
- Track M is operator/deploy-time (§3.15);
  Track O is contributor/dev-time (orthogonal).

**(B) installable-from-git-URL** rejected — that
workflow has different threat-model implications
(arbitrary-URL execution) and a different
audience (end-users, not contributors).

**(C) broader DX axis** (formatter / linter /
test-runner policies) rejected — `[tool.ruff]`
and `[tool.pytest.ini_options]` are configuration
present but not enforced (§3.4). Imposing policy
on these is a separate, larger decision.

### §7.3 Q3 — likely honest Step 4 path?

**Step 1 default.** PATH A docs-only primary;
PATH B held in reserve; Step 4 PATH not locked
at Step 1.

**Audit-grounded recommendation.** **PATH A is
the most likely outcome**, with PATH B held in
reserve only if Step 3 contract decides that
declarative cross-OS bootstrap or
explicit-editable-install comment block is
honestly needed. Repo evidence is mixed on the
cross-OS question:

- Pro-PATH-A: every signal Track O needs already
  exists (latent editable install via hatchling,
  populated wheel-build `packages`, working
  bootstrap, working selfcheck).
- Pro-PATH-B: the bootstrap is PowerShell-only;
  a POSIX contributor today cannot dot-source it
  without `pwsh`.

The cross-OS friction is real but not blocking
(a POSIX contributor can hand-construct
`PYTHONPATH` from the eleven paths in
`bootstrap_paths.ps1:9-21`, or use `pip install
-e .` and bypass the bootstrap entirely). Step
3 contract is the right place to weigh whether
that workaround is acceptable as the supported
posture, or whether a small declarative fix is
warranted.

PATH C very low probability; see §7.1.

### §7.4 Q4 — minimum closure scope (what is definitely mandatory)

**Audit-grounded recommendation.** The following
should be mandatory in the eventual Track O
closure recipe:

1. **A supported install procedure for
   contributors.** Either "dot-source
   `bootstrap_paths.ps1`" (current latent
   working path), or "run `pip install -e .`"
   (latent capability), or both — with the
   recipe stating which is first-class and which
   is recommended-only.
2. **A supported tooling preconditions list.**
   Python 3.11; `pip` (always present in the
   stdlib install); `build` only if the
   contributor wants to construct a wheel
   (Track M boundary, not Track O).
3. **A workspace-discovery answer.** Naming the
   eleven-element src-layout list as the
   workspace and noting its dual role
   (wheel-build packages + dev-time PYTHONPATH).
4. **A verification step.** "Run `python
   scripts/dev/selfcheck.py` (or
   `.\scripts\dev\launch.ps1 selfcheck`)" — the
   `selfcheck_status = ok` line is the canonical
   PASS signal.
5. **An authoritative non-goals enumeration.**
   Aggregating Step 1 plan §7 denials into a
   single contributor-facing list.
6. **A relationship-to-Track-M statement.**
   Naming the dev-time vs deploy-time boundary
   explicitly (orthogonal axes).

**Recommended-only** (acceptable to omit):
- Specific tool recommendations beyond Python +
  pip (e.g., uv / pdm / hatch).
- Multi-OS implementation-covered parity (Step 3
  may pin Windows primary + POSIX prose-only).
- A virtual-environment management policy.

### §7.5 Q5 — what is definitely insufficient as closure proof?

The audit explicitly rejects each of the
following as sufficient on its own:

- "Just clone the repo" — necessary but not
  sufficient (imports fail without
  PYTHONPATH or editable install).
- "`pip install -e .` maybe works" — maybe-
  works is not a supported boundary.
- `bootstrap_paths.ps1` alone — PowerShell-
  only, not cross-OS (§5.1).
- `launch.ps1` alone — discoverability surface
  only, not an install boundary (§5.3).
- `selfcheck.py` alone — verification gate, not
  an install procedure (§3.10 / §5.4).
- `scripts/dev/README.md` alone — names the
  gap, does not close it (§5.4).
- `phase-1-entry.md:79-82` alone — architecture
  doc, not a recipe (§5.5).
- Ad-hoc tribal knowledge (§5.7).
- Hatchling's PEP 660 default behaviour as
  documented elsewhere — not a repo-evidenced
  supported boundary (§5.2).

Closure requires **a single contributor-facing
document that integrates these signals into a
positive supported workflow**, plus the recipe /
verification / non-goals content named in §7.4.

### §7.6 Q6 — does Track O likely require production code at all?

**Step 1 default.** Likely NOT required.

**Audit-grounded recommendation.** **Confirmed.
Production code change very likely not needed.**
Repo evidence:

- §4.2: editable install is **latent**; hatchling
  already supports it via PEP 660 default
  behaviour. No code change needed to enable it.
- §4.1: workspace-discovery list is already
  synchronised between two files; no third
  source of truth needs to be introduced.
- §4.4: verification gate (`selfcheck.py`)
  already exists.
- §4.6: stdlib-only runtime means a contributor's
  editable install introduces no dependency
  conflicts.

The only candidate for code change under PATH B
is adding a `bootstrap_paths.sh` cross-OS
sibling (≤ 50 LOC stdlib-shell) — and that is
new dev-tooling, not production code. Step 3
contract decides whether the cross-OS friction
warrants even that narrow addition.

Step 3 contract may still pin PATH B if Step 2
audit (this document) is overridden by operator
preference, but the audit identifies no
gap-driven justification for production code
change in `apps/*/src/` or `packages/*/src/`.

---

## §8. Step 3 handoff note

Items the Step 3 contract will need to lock based
on this audit (a non-exhaustive list, ≥ 12 items):

1. **Q1 / Q3 final answer** — PATH A docs-only
   vs PATH B narrow declarative slice. Audit
   recommends PATH A.
2. **Q2 final answer** — narrow contributor-
   facing scope only. Audit recommends as-is.
3. **Step 4 file-surface cap.** Default
   expectation: ≤ 3 files under PATH A (one
   contributor recipe + at most one accompanying
   file). Step 3 may tighten to exactly 1 file.
4. **Step 4 LOC cap.** Default ≤ 200 LOC
   stdlib-only. Under PATH A this is effectively
   0 LOC; under PATH B (cross-OS bootstrap
   sibling) ≤ 50 LOC stdlib-shell.
5. **Mandatory recipe sections** — supported
   install procedure / supported tooling
   preconditions / workspace-discovery answer /
   verification step / non-goals enumeration /
   relationship-to-Track-M statement (audit §7.4
   items 1–6).
6. **Recipe path.** Step 1 plan §13 suggested
   `docs/dev/editable-install-and-workspace-discovery.md`
   or `docs/contributors/dev-workflow.md`. Step
   3 contract should pick one canonical path
   for symmetry with prior recipe locations
   (`docs/operators/*` for operator-facing
   recipes; analogous `docs/dev/` or
   `docs/contributors/` for contributor-facing).
7. **Authoritative non-goals carry-through.**
   Step 1 plan §7 denials plus the six
   forbidden maturity claims must appear in the
   recipe as explicit denials.
8. **Cross-OS posture.** Step 3 contract should
   pin one of: (a) Windows primary +
   POSIX prose-only; (b) cross-OS implementation-
   covered via `bootstrap_paths.sh` sibling under
   PATH B; (c) `pip install -e .` first-class
   bypassing the bootstrap question entirely.
9. **`pip install -e .` posture lock.** Audit
   recommends naming `pip install -e .` as a
   **first-class supported** workflow (latent
   capability now formalised by prose) and
   `bootstrap_paths.ps1` as a **recommended-only**
   alternative for contributors not using
   editable install — but Step 3 contract is the
   lock point.
10. **Selfcheck role lock.** `selfcheck.py`
    naming as the canonical verification gate,
    inherited from Track N FC4.
11. **Track M cross-reference lock.** The recipe
    must explicitly cross-reference
    `docs/operators/packaging/distribution-boundary.md`
    to clarify the dev-time vs deploy-time
    boundary.
12. **Q7 SemVer outcome.** Default NO-BUMP under
    PATH A; PATCH considered only under PATH B
    with honest defect-class declarative repair
    framing.
13. **Step 4 forbidden-files list.** Production
    code under `apps/*/src/` and `packages/*/src/`
    byte-identical; all `scripts/release/*`
    byte-identical; all `scripts/dev/*` byte-
    identical except `scripts/dev/README.md`
    (which Step 5 may narrowly update to replace
    the hand-off sentence with a pointer at the
    new recipe); Track J / L / M / N operator
    recipes byte-identical; `pyproject.toml`
    byte-identical unless PATH B authorises a
    narrow declarative addition.
14. **Step 5 forbidden-files list.** Beyond the
    narrow CLASS-1 alignment surfaces (README +
    PROJECT-STATUS + possibly `docs/release-
    handoff.md` + possibly `docs/developer-
    manual.md` + possibly `scripts/dev/README.md`
    targeted line replacement), everything stays
    byte-identical.

---

## §9. Honest summary

**Gap as it actually stands at `4122431`.** The
project has a working but **undocumented and
PowerShell-only** dev-time bootstrap
(`bootstrap_paths.ps1` + `selfcheck.py` +
`launch.ps1`), a **mechanically latent but
unpromised** `pip install -e .` capability (via
hatchling's PEP 660 default with Track M's
populated `packages` array), and **two explicit
in-repo anchors** (`scripts/dev/README.md:5-11`,
`scripts/dev/README.md:192-198`) plus **one
older architecture anchor**
(`docs/architecture/phase-1-entry.md:79-82`) all
naming the gap that Track O addresses. What is
missing is **one contributor-facing document
that integrates the above into a positive
supported workflow** — not new tooling, not
new dependencies, not new code.

**Why one descriptive audit file is sufficient.**
The gap is integration-and-naming, mirroring the
Track N audit's conclusion at a different
boundary. Every surface this audit names is
already in the repo. The Step 3 contract will
pin which surfaces are first-class vs.
recommended-only vs. out-of-scope, what the
closure-gate scenario is, and what the Step 4
file/LOC caps are. Step 4 will ship the
contributor recipe (and, under PATH B, an
optional narrow declarative slice). Step 2's
job is to give Step 3 a credible evidence base
— that is now done.

**Track O likely closure shape.** Highest-
probability trajectory: Step 3 contract pins
PATH A docs-only; Step 4 ships a single
contributor recipe at
`docs/dev/editable-install-and-workspace-discovery.md`
(or analogue path) integrating §3 / §4 / §7
content into contributor-readable form; Step 5
adds narrow CLASS-1 alignment edits to README +
PROJECT-STATUS + the `scripts/dev/README.md`
hand-off-sentence replacement; Step 6 closes
Track O with NO-BUMP, fifteen post-phase
parallel tracks (A through O) closed
sequentially.

**Track O likely does not require production
code.** Audit identifies no driver for code
change. Step 3 may still pin PATH B (e.g.,
`bootstrap_paths.sh` cross-OS sibling) if
operator/contributor preference justifies; under
that path the bump likely lands at PATCH
(`0.5.2 → 0.5.3`) mirroring Track I / Track M
precedent if the cross-OS sibling is framed as
closing a defect-class
PowerShell-only-bootstrap gap. Audit does not
see gap-driven justification for PATH B at this
stage; operator/contributor-preference-driven
justification remains a Step 3 decision.

**Out-of-scope reaffirmed.** No containerised dev
environment, no IDE-specific bundles, no
remote-dev / Codespaces / GitPod / Coder, no
multi-Python-version matrix, no formatter /
linter / test-runner policy redesign, no
alternative build-backend evaluation, no
transport / auth / deployment / service /
packaging / observability redesign, no new MCP
tools, no registry change, no `1cv8.exe` work,
no remote push.

**No premature closure language.** Track O is
**active**, currently between Step 2 (this
commit) and Step 3 (next operator decision).
Phrases like "developer workflow solved
forever" / "all IDE integrations supported" /
"all package managers supported for dev
install" / "containerised dev environment
shipped" / "remote-dev shipped" / "enterprise
developer experience" / "production-ready DX" /
"DX matrix complete" appear in this audit
**only as denials**.

**Canonical next step.** Parallel Track O /
Step 3 — normative contract (RFC 2119 MUST /
MUST NOT / SHOULD / SHOULD NOT / MAY) locking
Q1–Q6 final answers plus Step 4 file/LOC caps
and forbidden-files list. Opening Step 3 is a
separate operator decision; not auto-opened.
