# Parallel Track O — Dev-Time Editable Install and Workspace Discovery — Contract

**Step status.** Parallel Track O / Step 3 — normative
contract. Companion to
[track-o-dev-time-editable-install-and-workspace-discovery-plan.md](track-o-dev-time-editable-install-and-workspace-discovery-plan.md)
(Step 1 planning, Q1–Q7 directional defaults) and
[track-o-dev-time-editable-install-and-workspace-discovery-baseline-audit.md](track-o-dev-time-editable-install-and-workspace-discovery-baseline-audit.md)
(Step 2 descriptive baseline, Q1–Q6 directional
resolutions grounded in repo evidence at HEAD
`c8941a4`, project version `0.5.2`).

This document is **normative**. It translates Step 2
audit findings into RFC 2119 MUST / MUST NOT /
SHOULD / SHOULD NOT / MAY rules that lock Step 4 PATH,
Step 4 file surface, the supported dev-time workflow
boundary, and the verification protocol. After this
commit there is no remaining design freedom for Step 4
beyond what this contract explicitly authorises.

The contract MUST NOT widen Track O into a broader
developer-experience platform (containerised dev / IDE
integrations / remote-dev / multi-Python-version
matrix / formatter-linter-test-runner policy redesign /
alternative build-backend evaluation). Each forbidden
category is named in §9 / §12.

---

## §1. Purpose / scope

### §1.1 What this contract is

A single normative document that:

- Locks the final answers to Q1 / Q2 / Q3 / Q4 / Q5
  from Step 1 plan §12 and Step 2 audit §7.
- Pins the **Step 4 PATH** to a single named option.
- Defines the **closure-gate scope** in terms of
  concrete, testable artefacts.
- Defines the **supported dev-time workflow boundary**
  in terms of existing surfaces (no new tooling
  introduced by Track O).
- Defines the **Step 4 file surface** (exact allowed
  paths, file counts, LOC caps, forbidden-files list).
- Defines the **verification protocol** Step 4 must
  satisfy pre-commit and post-commit.
- Carries forward every Tracks A–N invariant byte-
  identical.

### §1.2 What this contract is not

- Not an implementation. No production code, no
  recipe content, no `pyproject.toml` change, no
  `scripts/*` change.
- Not an audit. Step 2 already produced the
  descriptive baseline at
  `docs/architecture/track-o-dev-time-editable-install-and-workspace-discovery-baseline-audit.md`;
  this contract MUST NOT re-litigate Step 2 evidence
  except where a new contradictory fact appears.
- Not a Step 5 alignment doc. CLASS-1 alignment of
  README / PROJECT-STATUS / possibly
  `docs/release-handoff.md` / possibly
  `docs/developer-manual.md` / possibly
  `scripts/dev/README.md` targeted line replacement is
  Step 5 territory.
- Not a Step 6 closure document. Q7 (SemVer outcome)
  is **framed** here but **locked** at Step 6.

### §1.3 RFC 2119 keyword usage

Throughout this document:

- **MUST** / **MUST NOT** / **REQUIRED** /
  **SHALL** / **SHALL NOT** — absolute requirements
  whose violation invalidates a Step 4 commit.
- **SHOULD** / **SHOULD NOT** / **RECOMMENDED** —
  default behaviour; deviation MUST be justified
  inline in the affected commit message.
- **MAY** / **OPTIONAL** — operator/contributor-level
  discretion; no justification required.

Keywords appear in **bold** when they carry RFC 2119
weight; lowercase usage in prose has its ordinary
English meaning.

### §1.4 Track O scope reminder (binding)

This contract MUST keep Track O narrow. Specifically,
the contract MUST NOT authorise, encourage, or
indirectly enable any of:

- A containerised dev environment (Dockerfile bundled,
  `docker-compose.yml`, `.devcontainer/` configuration).
- IDE-specific integration (VSCode `.vscode/`,
  JetBrains `.idea/`, Cursor / Zed / Sublime / Vim
  project files bundled).
- Remote-dev workflow (Codespaces, GitPod, Coder
  template).
- Multi-Python-version matrix (`.python-version`
  Python 3.11 pin preserved; no tox/nox matrix).
- Formatter / linter / test-runner policy redesign
  (existing `[tool.ruff]` and `[tool.pytest.ini_options]`
  configuration is operator/contributor-side
  discretion; Track O MUST NOT mandate or extend it).
- Alternative build-backend evaluation (hatchling
  remains the build backend).
- Test-suite shipping (the empty `tests/` directory
  is out-of-Track-O scope).
- Installable-from-git-URL story (operator-side or
  end-user-side install via `pip install <git-URL>` is
  a different workflow with different threat-model
  implications and is rejected by Step 2 audit §7.2).
- Transport redesign (Track G stdio + Track H HTTP
  preserved byte-identical).
- Auth redesign (Track H bearer + Track D
  `${ENV:NAME}` + Track I round-trip preserved byte-
  identical).
- Deployment-boundary redesign (Track J preserved
  byte-identical).
- Service-supervision redesign (Track L preserved
  byte-identical).
- Packaging redesign (Track M wheel-build flip +
  recipe preserved byte-identical, including the
  11-element `[tool.hatch.build.targets.wheel]
  packages` array).
- Observability redesign (Track N preserved byte-
  identical).
- New MCP tools or registry change (`read=15 /
  write=25 / intelligence=16` invariant carried
  through).
- New CLI flags on existing servers (Track G/H flag
  surface locked).
- New `[project.scripts]` console entries.
- New entries to `[project.dependencies]` or
  `[project.optional-dependencies]`.
- New entrypoint module in any `apps/*/src/`
  package.
- `1cv8.exe` runs.
- Remote push (operator decision; never automated).
- Any maturity claim of the form "developer workflow
  solved forever" / "all IDE integrations supported"
  / "all package managers supported for dev install"
  / "containerised dev environment shipped" /
  "remote-dev shipped" / "enterprise developer
  experience" / "production-ready DX" / "DX matrix
  complete".

---

## §2. Relationship to Step 1 plan and Step 2 audit

### §2.1 Step boundary

This contract sits between Step 2 (descriptive audit)
and Step 4 (narrow implementation slice). The six-step
shape is fixed by Step 1 step-map:

| Step | Kind | Status at this commit |
| --- | --- | --- |
| Step 1 | planning | closed (commit `4122431`) |
| Step 2 | descriptive baseline audit | closed (commit `c8941a4`) |
| Step 3 | normative contract | **this commit** |
| Step 4 | narrow implementation slice | upcoming |
| Step 5 | docs / operator / release alignment | future |
| Step 6 | final integration pass + Q7 lock | future |

### §2.2 Re-litigation rule

This contract MUST NOT silently amend Step 2 findings
without naming the contradiction. If, during Step 4
authoring, a Step 2 fact is contradicted by repo
evidence, the Step 4 commit MUST cite this contract
§2.2 and explicitly call out the contradiction in its
commit message before proceeding. Re-opening Step 2 is
a separate process.

### §2.3 Inherited Step 2 audit resolutions

Step 2 §7 produced six directional resolutions. This
contract converts them into normative answers.

**Q1 — what counts as "dev-time editable install /
workspace discovery" for closure?**
Audit recommendation: PATH A docs-only primary, high
confidence.
**Contract LOCK (§4 / §6 / §7).** Closure is **one
contributor-facing dev-time-boundary recipe** plus
the named supported-workflow classification it
embeds; no new tooling, no new code-bearing
artefact, no new dependency.

**Q2 — primary problem focus?**
Audit recommendation: narrow contributor-facing
scope confirmed.
**Contract LOCK (§5).** Contributor/internal-
developer workflow editing the repo in place is
the only supported audience. Installable-from-git-
URL story (§7.2(B)) is rejected. Broader DX axis
(formatter/linter/test-runner policies, §7.2(C)) is
rejected.

**Q3 — likely honest Step 4 path?**
Audit recommendation: PATH A docs-only primary;
PATH B held in reserve; PATH C rejected.
**Contract LOCK (§7.1).** Step 4 PATH = **PATH A
docs-only**. PATH B (narrow declarative slice
adding e.g. `bootstrap_paths.sh` cross-OS sibling
or `pyproject.toml` editable-install comment block)
is explicitly rejected in §7.2. PATH C (developer
bootstrap helper script) is explicitly rejected in
§7.3.

**Q4 — what is definitely mandatory for closure?**
Audit recommendation: six mandatory items.
**Contract LOCK (§4.1 / §6).** Six mandatory recipe
content elements pinned: supported install
procedure; supported tooling preconditions;
workspace-discovery answer; verification step;
authoritative non-goals enumeration; relationship-
to-Track-M statement.

**Q5 — what is definitely insufficient as closure
proof?**
Audit recommendation: each existing source
individually insufficient.
**Contract LOCK (§9).** Each named source on its
own is normatively insufficient; only the
integration document closes the gap.

**Q6 — does Track O require production code?**
Audit recommendation: very likely no.
**Contract LOCK (§10).** No production code change
under PATH A. Q7 SemVer outcome framed (§13.5) but
locked at Step 6.

---

## §3. Inherited fixed decisions from Step 2

The following decisions are inherited from Step 2 §3 /
§4 evidence and MUST NOT be revisited by this contract
or by Step 4 without new contradictory evidence.

### §3.1 Existing dev-time surfaces preserved byte-identical

Step 2 §3 enumerated the existing surfaces. Each MUST
be preserved byte-identical through Step 4:

1. **`pyproject.toml` build backend** at
   `pyproject.toml:1-3` (`hatchling.build`).
2. **`pyproject.toml [project]` metadata** at
   `pyproject.toml:5-13` (`name = "1c-agent-platform"`,
   `version = "0.5.2"`, `requires-python = ">=3.11"`).
3. **`pyproject.toml [project.dependencies]` implicitly
   absent** — runtime stdlib-only orientation.
4. **`pyproject.toml [project.scripts]`** three
   console entries at `pyproject.toml:22-25`.
5. **`pyproject.toml [tool.ruff]`** at
   `pyproject.toml:27-29`.
6. **`pyproject.toml [tool.pytest.ini_options]`** at
   `pyproject.toml:31-32` (testpaths declaration;
   `tests/` directory does not exist; not in scope).
7. **`pyproject.toml [tool.hatch.build.targets.wheel]
   packages`** 11-element array at
   `pyproject.toml:34-63` (Track M / Step 4 lock).
8. **`.python-version`** Python 3.11 pin.
9. **`scripts/dev/bootstrap_paths.ps1`** PowerShell-
   only PYTHONPATH bootstrap (32 LOC; 11 src paths
   mirroring the wheel-build array).
10. **`scripts/dev/launch.ps1`** umbrella
    (146 LOC; subcommands `selfcheck` / `repl` /
    `run` / `help`).
11. **`scripts/dev/run_dev_check.ps1`** wrapper
    (22 LOC).
12. **`scripts/dev/selfcheck.py`** pre-flight gate
    (110 LOC; Track N FC4).
13. **`scripts/dev/mcp_client_smoke.py`** Track K
    closure-locked harness.
14. **`scripts/dev/README.md`** including the
    verbatim hand-off marker at lines 5-11 and
    192-198 (Step 5 MAY narrowly replace those
    sentences with a pointer at the new recipe;
    no other change permitted).
15. **`scripts/release/*`** all files (`install.ps1`,
    `verify-release.ps1`, `_install_runner.py`,
    `README.md`).
16. **`.github/workflows/dev-check.yml`** CI
    workflow.
17. **`docs/architecture/phase-1-entry.md:79-82`**
    older anchor predicting future editable-install
    need (frozen architecture-doc).

### §3.2 Existing gap statement preserved

Step 2 §3 / §6 established the gap as **integration
and naming**, not signal generation or tooling
introduction. This contract MUST NOT introduce new
tooling surfaces.

### §3.3 Existing reusable surfaces preserved

Step 2 §4 enumerated 8 reusable surfaces. All MUST
be preserved byte-identical through Step 4.

### §3.4 Hatchling PEP 660 editable-install latent capability

Step 2 §3.1 / §3.5 / §4.2 established that
`pip install -e .` is **mechanically possible** at
HEAD `c8941a4` via hatchling's PEP 660 default
behaviour, because the `[tool.hatch.build.targets.
wheel] packages` array is populated (Track M / Step
4 lock). This latent capability is the central
operational anchor Track O's recipe formalises.
This contract LOCKS that capability as the
first-class supported dev-time install verb under
PATH A; see §5 / §6.

### §3.5 Hand-off marker preservation

The two hand-off-marker sentences at
`scripts/dev/README.md:5-11` and `:192-198`
("editable install и workspace discovery всё ещё
out of scope") MUST remain byte-identical through
Steps 3 / 4. Only Step 5 MAY narrowly replace them
with a pointer at the new recipe; this contract
authorises that Step 5 edit and **no other** edit
to `scripts/dev/README.md` across Track O.

---

## §4. Closure-gate contract

### §4.1 Definition of "honest Track O closure"

Track O closes honestly **iff** all of the following
hold at the Step 6 commit:

C1. **Single contributor-facing dev-time-boundary
    recipe** committed at the path locked in §8.2.
C2. The recipe **MUST** contain a **supported install
    procedure** naming the primary install verb
    (locked at §5) and any recommended-only
    alternatives.
C3. The recipe **MUST** contain a **supported tooling
    preconditions list** stating which tools the
    contributor MUST have available (Python 3.11
    interpreter, `pip`) and which are
    recommended-only (e.g., `build` only if the
    contributor wants to construct a wheel — Track M
    boundary).
C4. The recipe **MUST** contain a **workspace-
    discovery answer** naming the eleven-element
    src-layout package list as the workspace and
    explaining its dual role (wheel-build packages
    array per Track M + dev-time PYTHONPATH per
    `bootstrap_paths.ps1`).
C5. The recipe **MUST** contain a **verification
    step** naming `python scripts/dev/selfcheck.py`
    (or equivalently `.\scripts\dev\launch.ps1
    selfcheck` on Windows) as the canonical
    contributor-runnable verification gate, citing
    `selfcheck_status = ok` as the canonical PASS
    line. This step MUST preserve Track N FC4
    classification of `selfcheck.py`.
C6. The recipe **MUST** contain an **authoritative
    non-goals enumeration** collecting Step 1 plan
    §7 denials plus the eight forbidden maturity
    claims (§9.2) into one contributor-facing list.
C7. The recipe **MUST** contain a **relationship-to-
    Track-M statement** explicitly distinguishing
    dev-time contributor workflow (`pip install -e .`
    or PYTHONPATH bootstrap) from deploy-time
    operator workflow (`pip install <WHEEL_PATH>`
    of the Track M wheel artefact), and naming the
    two as **orthogonal-and-complementary** axes.
    This statement MUST cite
    `docs/operators/packaging/distribution-boundary.md`
    by relative path.
C8. The recipe **MUST** contain **at least one
    explicit cross-reference each** to: Track M
    `distribution-boundary.md` (orthogonal axis);
    `pyproject.toml`'s
    `[tool.hatch.build.targets.wheel] packages`
    array (the eleven-package list);
    `scripts/dev/bootstrap_paths.ps1` (the
    alternative dev-time discovery mechanism);
    `scripts/dev/launch.ps1` (the umbrella
    discoverability surface);
    `scripts/dev/selfcheck.py` (the verification
    gate); `scripts/dev/README.md` (the file
    containing the now-replaced hand-off marker —
    see §3.5).
C9. The recipe **MUST** contain a **cross-OS
    posture** section per §5.3 (Windows primary
    via the existing PowerShell bootstrap; POSIX
    contributors served by `pip install -e .`
    via Python interpreter alone; no fake parity).
C10. README / PROJECT-STATUS / CHANGELOG closure
     narrative (Step 5 + Step 6) MUST honestly
     describe what was settled and MUST explicitly
     deny each forbidden-claim phrase from §9.2.
C11. Tracks A–N production code byte-identical to
     Track N closure state (`2737a52`).
C12. Registries `read=15 / write=25 /
     intelligence=16` unchanged.
C13. `verify-release.ps1` GREEN on 8 checks at each
     of Step 3 / 4 / 5 / 6 commits (pre- and post-).
C14. `selfcheck.py` `status=ok` at each step.
C15. No real credentials in any committed file.
C16. No `1cv8.exe` runs.
C17. No remote push performed by the track.

### §4.2 What does NOT count as closure-gate proof

The following claims, however true individually, are
**NOT** sufficient closure-gate proof:

- "Just clone the repo." (Step 2 §5 / §7.5; necessary
  but not sufficient.)
- "`pip install -e .` maybe works." (Step 2 §5.2
  established this as latent-but-unpromised.)
- `scripts/dev/bootstrap_paths.ps1` alone (Step 2
  §5.1; PowerShell-only).
- `scripts/dev/launch.ps1` alone (Step 2 §5.3;
  discoverability only).
- `scripts/dev/selfcheck.py` alone (Step 2 §3.10 /
  §5.4; verification not install).
- `scripts/dev/README.md` alone (Step 2 §5.4; names
  gap, does not close it).
- `docs/architecture/phase-1-entry.md:79-82` alone
  (Step 2 §5.5; architecture doc, not recipe).
- `.github/workflows/dev-check.yml` alone (Step 2
  §5.6; validates only bootstrap workflow).
- Ad-hoc tribal knowledge (Step 2 §5.7).
- Hatchling's PEP 660 default behaviour as
  documented elsewhere (Step 2 §5.2; not a repo-
  evidenced supported boundary).
- Screenshots of working terminals.
- Commit-message claims without a committed recipe.
- Verbal commitments outside the recipe file.

### §4.3 What Step 4 MUST commit

Step 4 MUST commit exactly the file set defined in
§8 and MUST NOT commit anything else. Specifically:

- Exactly one new contributor-facing recipe file at
  the path locked in §8.2.
- Zero modifications to any file enumerated in §8.5
  (forbidden file surface).
- No new dependencies.
- No new scripts.
- No new MCP tools.
- No registry change.

---

## §5. Primary supported dev-time workflow boundary contract

### §5.1 Locked first-class supported install verb

The first-class supported dev-time install verb under
Track O is:

> **`pip install -e .`** run from the repo root in a
> Python 3.11 environment.

This verb is **first-class supported** because:

- Step 2 §3.1 / §3.5 / §4.2 established that
  hatchling's PEP 660 default behaviour mechanically
  produces a working editable install when
  `[tool.hatch.build.targets.wheel] packages` is
  populated (which it is, per Track M / Step 4 lock).
- Step 2 §3.3 established that the three
  `[project.scripts]` console entries (`mcp-read-
  server` / `mcp-write-server` / `mcp-intelligence-
  server`) become contributor-runnable binaries
  immediately after `pip install -e .`.
- Step 2 §3.2 established that `[project.dependencies]`
  is implicitly empty, so the install introduces no
  third-party dependencies into the contributor's
  virtual environment.
- Step 2 §4.1 established that workspace discovery
  via this verb is byte-equivalent to the PYTHONPATH-
  bootstrap path: both expose the same 11 src-layout
  package roots.

### §5.2 Locked recommended-only alternative

The recommended-only alternative dev-time workflow is:

> **`. .\scripts\dev\bootstrap_paths.ps1`** (dot-
> source) in a Windows PowerShell session.

This alternative is **recommended-only** (not first-
class) because:

- Step 2 §3.7 / §5.1 established that the bootstrap
  is PowerShell-only — POSIX contributors cannot
  dot-source it without `pwsh` installed, and even
  then path separators do not resolve correctly.
- Step 2 §4.3 / §3.8 established that the
  `launch.ps1` umbrella exists as a discoverability
  surface for this alternative.

The recipe **MUST** clearly state that this alternative
remains supported for contributors who choose not to
use editable install (e.g., those who prefer to avoid
modifying their site-packages, or who already have a
preferred virtual-environment workflow).

### §5.3 Cross-OS posture

The Track O recipe **MUST** state the cross-OS posture
as:

- **Windows + PowerShell + Python 3.11** — primary
  implementation-covered path. Either `pip install
  -e .` (first-class) or `bootstrap_paths.ps1`
  (recommended-only) work end-to-end.
- **POSIX (Linux / macOS) + bash/zsh + Python 3.11** —
  served by `pip install -e .` first-class; the
  PowerShell bootstrap is **not** implementation-
  covered on POSIX (operators MAY install `pwsh` and
  use it, but that path is not supported by Track O).
- **Other shells / non-3.11 Python** — out of scope
  per §1.4.

The recipe **MUST NOT** claim implementation-covered
parity for any non-Windows path beyond what `pip
install -e .` provides; the bootstrap script remains
Windows-supported only.

### §5.4 No new tooling introduced

Track O **MUST NOT** introduce:

- A `bootstrap_paths.sh` POSIX-shell sibling (this is
  PATH B; rejected in §7.2).
- A dev-onboarding helper script under `scripts/dev/`
  (this is PATH C; rejected in §7.3).
- A `[project.optional-dependencies] dev = [...]`
  block (no project-supplied dev tools).
- A virtual-environment management helper.

Contributors who require any of the above MUST
arrange them themselves with no project-side support.

---

## §6. Workspace-discovery and editable-install boundary contract

### §6.1 What the boundary is

The Track O boundary is:

- **A single in-repo contributor-facing recipe** at
  the path locked in §8.2.
- **Six mandatory content elements** (C2–C7 from
  §4.1).
- **Cross-references** to the six anchors in C8.
- **Cross-OS posture** (C9 / §5.3).
- **Explicit denial of forbidden categories** from
  §1.4 / §9.2.

### §6.2 What the boundary is NOT

The Track O boundary is **NOT**:

- A guarantee of contributor-side outcomes
  (contributors retain full discretion over their
  virtual-environment management, IDE choice, and
  tooling).
- A guarantee that any specific package manager
  beyond `pip` is supported. The recipe pins
  `pip install -e .` as the first-class verb;
  alternatives like `uv pip install -e .`, `pdm
  install`, or `hatch env create` may
  coincidentally work but are **not** Track O-
  supported.
- A claim that all IDE integrations work. The
  recipe documents the install + workspace-
  discovery boundary; what an IDE does on top of
  that is operator/contributor responsibility.
- A claim that all OS combinations work
  equivalently — see §5.3.
- A health-endpoint, alerting story, or any other
  cross-track surface.

### §6.3 Workspace-discovery answer

The recipe **MUST** state that the workspace is
exactly the eleven src-layout package roots
enumerated in `pyproject.toml:51-63` (Track M / Step
4 lock). The recipe **MUST** make explicit that
this list is the **single source of truth**, even
though it is currently duplicated byte-equivalently
in `scripts/dev/bootstrap_paths.ps1:9-21`. The
contract LOCKS this duplication as **acceptable
duplication** for Track O purposes; resolving it
into a single source is out of Track O scope.

### §6.4 Editable-install posture

The recipe **MUST** state that `pip install -e .`:

- Installs the project in "editable mode" via
  hatchling's PEP 660 default behaviour.
- Makes all eleven src-layout packages importable
  without any further `PYTHONPATH` manipulation.
- Installs the three `[project.scripts]` console
  entries (`mcp-read-server` / `mcp-write-server`
  / `mcp-intelligence-server`) as contributor-
  runnable binaries.
- Reflects subsequent in-place source edits
  immediately (no rebuild step required for code
  changes).
- Introduces **zero** third-party runtime
  dependencies into the virtual environment, per
  the absent `[project.dependencies]`.

The recipe **MAY** clarify that the contributor is
responsible for the virtual environment (creation,
activation, deactivation) — Track O does not
mandate a specific virtual-environment tool.

### §6.5 Verification step

The recipe **MUST** state that after `pip install
-e .` (or alternatively, after dot-sourcing
`bootstrap_paths.ps1` on Windows), the canonical
contributor verification is:

```
python scripts/dev/selfcheck.py
```

or equivalently on Windows:

```powershell
.\scripts\dev\launch.ps1 selfcheck
```

The recipe **MUST** name `selfcheck_status = ok` as
the canonical PASS line and reference Track N FC4
classification of `selfcheck.py`. The recipe **MUST
NOT** introduce a new verification gate.

### §6.6 Non-goals enumeration scope

The recipe **MUST** include an explicit non-goals
section. The non-goals enumeration MUST cover at
minimum:

- No containerised dev environment.
- No IDE-specific integration.
- No remote-dev workflow.
- No multi-Python-version matrix.
- No formatter/linter/test-runner policy redesign.
- No alternative build-backend evaluation.
- No installable-from-git-URL story.
- No test-suite shipping (the empty `tests/` is
  acknowledged but out of scope).
- No transport/auth/deployment/service/packaging/
  observability redesign.
- No new MCP tools.
- No new CLI flag on existing servers.
- No new `[project.scripts]` entries.
- No new dependencies.

For each item, the recipe MAY either restate the
denial verbatim or cite the existing anchor (Track O
Step 1 plan §7, this contract §1.4).

### §6.7 Relationship to Track M (orthogonal-and-complementary)

The recipe **MUST** explicitly position dev-time
editable install (Track O) as orthogonal-and-
complementary to deploy-time wheel install (Track M):

- **Track M** — operator receiving a built
  `1c_agent_platform-<VERSION>-py3-none-any.whl`
  via out-of-band delivery; install verb is
  `pip install <WHEEL_PATH>`; lifecycle moment is
  deploy-time; recipe is
  `docs/operators/packaging/distribution-boundary.md`.
- **Track O** — contributor editing the repo in
  place; install verb is `pip install -e .`;
  lifecycle moment is dev-time; recipe is the new
  Track O recipe.

The recipe **MUST NOT** duplicate Track M content;
cross-references are sufficient.

---

## §7. Final Step 4 PATH selection

### §7.1 Locked: PATH A docs-only

**Step 4 PATH = PATH A docs-only.**

Step 4 SHALL produce exactly one new contributor-
facing recipe under the path locked in §8.2 and
SHALL NOT modify any production code, `pyproject.toml`,
`scripts/*`, or any existing operator/dev/release
recipe.

### §7.2 PATH B explicitly rejected

PATH B (docs + one narrow declarative slice — e.g.,
`bootstrap_paths.sh` POSIX-shell sibling, or a
`pyproject.toml` editable-install comment block) is
explicitly rejected by this contract. Justification
grounded in Step 2 evidence:

- Step 2 §7.3 explicitly framed PATH B as "held in
  reserve only if Step 3 contract decides cross-OS
  friction warrants it". This contract now decides
  it does **not** warrant a code-bearing addition,
  because `pip install -e .` first-class on POSIX
  (per §5.3) makes the PowerShell-only bootstrap a
  Windows-specific convenience rather than a
  cross-OS blocker.
- Step 2 §4.2 established that `pip install -e .`
  works on all PEP 660-supporting platforms (which
  includes Windows, Linux, and macOS with
  appropriately recent pip ≥ 21.3 — the dev-time
  prerequisite is `pip` itself, which is in every
  supported Python distribution).
- Adding a `bootstrap_paths.sh` POSIX-shell sibling
  would create a third source of truth for the
  eleven src-layout paths (after `pyproject.toml`
  and `bootstrap_paths.ps1`), increasing
  duplication-drift risk for marginal benefit when
  `pip install -e .` already covers POSIX.
- Adding an editable-install comment block to
  `pyproject.toml` would touch Track M's locked
  artefact for prose value, which contradicts §3.1
  invariant #7.
- Step 2 §7.6 explicitly stated "production code
  change very likely not needed".

PATH B remains theoretically available for a future
track; this Track O closes under PATH A.

### §7.3 PATH C explicitly rejected

PATH C (docs + one narrow developer bootstrap helper
script under `scripts/dev/`) is explicitly rejected
by this contract. Justification:

- Step 2 §7.1 explicitly rejected PATH C: "a
  dev-onboarding helper script would duplicate
  `launch.ps1`'s discoverability surface for
  marginal value".
- The existing `launch.ps1` umbrella already
  provides single-entry-point discoverability
  (`launch.ps1 selfcheck`, `launch.ps1 repl`,
  `launch.ps1 run <script>`, `launch.ps1 help`).
  A new dev-onboarding script would compete with
  it rather than complement it.
- Step 2 §3.8 established `launch.ps1`'s
  deliberate non-goals (does NOT start MCP
  servers, does NOT run pytest, does NOT run
  install fast path, does NOT touch infobase) —
  introducing a separate dev-onboarding script
  that also installs would muddy these boundaries.
- A POSIX-shell version of such a helper would
  re-introduce the same cross-OS-duplication
  concerns rejected in §7.2.

PATH C remains theoretically available for a future
track; this Track O closes under PATH A.

### §7.4 PATH A defended

PATH A is the narrowest honest closure path because:

- The gap is **integration and naming**, not
  tooling generation (Step 2 §3 / §6 / §9).
- Every workflow Track O needs to formalise
  **already exists** (Step 2 §3.1–§3.18 / §4.1–
  §4.8).
- Production code change is **very likely not
  required** (Step 2 §7.6).
- Tracks J / K / L / N closed comparable
  documentation-class gaps under docs-only PATH A
  patterns; Track J / Track N are direct
  analogues (pure prose recipe, no helper, no
  template, no code).

---

## §8. Exact Step 4 implementation surface

### §8.1 File count cap

Step 4 **MUST** add **exactly one** new file and
**MUST** modify **exactly zero** files. Total Step 4
touched-files count = 1 (add).

If Step 4 authoring encounters a situation that
appears to require touching more than one file, the
authoring MUST STOP and surface the conflict
explicitly rather than silently expand scope.

### §8.2 Recipe path — canonical location

The new recipe **MUST** be created at exactly:

```
docs/dev/editable-install-and-workspace-discovery.md
```

Rationale:

- Symmetric with `docs/operators/` (where Tracks J /
  L / M / N recipes live) — contributor-facing
  recipes live under `docs/dev/` paralleling the
  `scripts/dev/` directory.
- Step 1 plan §13 and Step 2 audit §8 item 6 both
  proposed either `docs/dev/editable-install-and-
  workspace-discovery.md` or `docs/contributors/
  dev-workflow.md`. The contract picks the former
  for naming consistency with `scripts/dev/` and
  for descriptive clarity of the recipe's content.
- A subdirectory (`docs/dev/...`) is only warranted
  if multiple peer files ship, which Track O MUST
  NOT do.

Creating `docs/dev/` (the parent directory) is
implicitly authorised by this contract since the
file path requires it; no other content under
`docs/dev/` is authorised.

### §8.3 Recipe required content shape

The new file **MUST** be structured as a recipe
(not a contract, not an audit). Recommended top-
level sections (the recipe MAY rename / reorder;
section content is normative per §4.1 / §6):

- §1 Purpose / scope (what this recipe is and is
  not; opening with explicit denials of forbidden
  maturity claims per §9.2).
- §2 Supported dev-time install verbs (first-class
  `pip install -e .` per §5.1; recommended-only
  `bootstrap_paths.ps1` per §5.2; cross-OS posture
  per §5.3).
- §3 Supported tooling preconditions (Python 3.11
  per `.python-version`; `pip` required; nothing
  else mandatory).
- §4 Workspace-discovery answer (the eleven src-
  layout package roots; dual-role explanation per
  §6.3).
- §5 Verification step (selfcheck per §6.5).
- §6 Relationship to Track M deploy-time wheel
  workflow (orthogonal-and-complementary per §6.7).
- §7 Honest non-goals (per §6.6).
- §8 Cross-references (file list pointing at the
  six anchors in C8).

### §8.4 Recipe size cap

- **Hard cap: ≤ 1000 lines** (recipes for narrow
  boundaries should be operator-/contributor-
  readable in one sitting; Track N's recipe at
  1043 lines is the upper end of practice and
  represents a broader observability surface than
  Track O addresses).
- **Soft cap: ≤ 700 lines** (RECOMMENDED).
- LOC cap is on contributor-facing prose. The
  recipe MUST NOT contain executable code beyond
  literal command-line examples in fenced code
  blocks. Code examples MUST use abstract
  placeholders (`<VENV_NAME>`, `<PYTHON>`) rather
  than real values where applicable.

### §8.5 Forbidden file surface for Step 4 (exhaustive list)

Step 4 **MUST NOT** create, modify, delete, or
rename any file in this exhaustive list:

**Production code (byte-identical):**
- `apps/mcp-read-server/src/mcp_read_server/**`
- `apps/mcp-write-server/src/mcp_write_server/**`
- `apps/mcp-intelligence-server/src/mcp_intelligence_server/**`
- `apps/platform/src/onec_platform/**`
- `packages/mcp-common/src/mcp_common/**`
- `packages/onec-process-runner/src/onec_process_runner/**`
- `packages/onec-policy-engine/src/onec_policy_engine/**`
- `packages/onec-audit/src/onec_audit/**`
- `packages/onec-health/src/onec_health/**`
- `packages/onec-troubleshooting/src/onec_troubleshooting/**`
- `packages/onec-config/src/onec_config/**`

**Project configuration (byte-identical):**
- `pyproject.toml`
- `.python-version`
- `.gitignore`
- `LICENSE`

**Existing scripts (byte-identical):**
- `scripts/dev/selfcheck.py`
- `scripts/dev/mcp_client_smoke.py`
- `scripts/dev/launch.ps1`
- `scripts/dev/bootstrap_paths.ps1`
- `scripts/dev/run_dev_check.ps1`
- `scripts/dev/README.md` (Step 5 may narrowly
  replace the hand-off-marker sentences per §3.5;
  Step 4 must not touch)
- `scripts/release/install.ps1`
- `scripts/release/verify-release.ps1`
- `scripts/release/_install_runner.py`
- `scripts/release/README.md`

**Existing operator recipes (byte-identical):**
- `docs/operators/deployment-boundary.md`
- `docs/operators/service/service-supervision.md`
- `docs/operators/service/mcp-server.service`
- `docs/operators/packaging/distribution-boundary.md`
- `docs/operators/observability.md`

**Existing status / handoff docs (byte-identical;
those listed here are Step-5 / Step-6 territory):**
- `README.md`
- `PROJECT-STATUS.md`
- `CHANGELOG.md`
- `SECURITY.md`
- `docs/release-handoff.md`
- `apps/platform/README.md`
- `docs/operator-manual.md`
- `docs/administrator-manual.md`
- `docs/developer-manual.md`
- `docs/runbooks.md`
- `docs/runbooks/**`

**Tests / data (byte-identical):**
- `tests/**` (declared in pyproject but absent;
  Step 4 must not create it)
- `examples/**`
- `dist/**`

**Track O step docs (byte-identical):**
- `docs/architecture/track-o-dev-time-editable-install-and-workspace-discovery-plan.md`
- `docs/architecture/track-o-dev-time-editable-install-and-workspace-discovery-step-map.md`
- `docs/architecture/track-o-dev-time-editable-install-and-workspace-discovery-baseline-audit.md`
- this file (`docs/architecture/track-o-dev-time-editable-install-and-workspace-discovery-contract.md`)

**All Tracks A–N architecture docs (byte-identical):**
- `docs/architecture/track-a-*.md`
- `docs/architecture/track-b-*.md`
- `docs/architecture/track-c-*.md`
- `docs/architecture/track-d-*.md`
- `docs/architecture/track-e-*.md`
- `docs/architecture/track-f-*.md`
- `docs/architecture/track-g-*.md`
- `docs/architecture/track-h-*.md`
- `docs/architecture/track-i-*.md`
- `docs/architecture/track-j-*.md`
- `docs/architecture/track-k-*.md`
- `docs/architecture/track-l-*.md`
- `docs/architecture/track-m-*.md`
- `docs/architecture/track-n-*.md`
- `docs/architecture/phase-*.md`

**CI workflow (byte-identical):**
- `.github/workflows/dev-check.yml`
- `.github/**` (any other file present)

If Step 4 touches any path on this list, the commit
MUST be rejected.

### §8.6 LOC and dependency caps

- **LOC cap (Step 4):** the new recipe MAY be up to
  the soft / hard caps in §8.4. No other LOC
  accrues because no other file changes.
- **Net code LOC change (Step 4):** **0**.
- **New `[project.dependencies]` entries:** 0.
- **New `[project.optional-dependencies]` entries:** 0.
- **New `[project.scripts]` entries:** 0.
- **New entrypoint modules:** 0.

### §8.7 What Step 4 MAY do beyond §8.1–§8.6

- Step 4 MAY use Markdown features (tables, fenced
  code blocks, headings, lists, blockquotes) in
  the recipe.
- Step 4 MAY include short fenced shell snippets
  (`bash`, `pwsh`) with abstract placeholders or
  literal example values (`python -m venv .venv`,
  `pip install -e .`).
- Step 4 MAY quote prose verbatim from
  `scripts/dev/README.md` (acknowledging the old
  hand-off marker as historical context).
- Step 4 MAY include a "Cross-references" tail
  section pointing back at the six anchors in C8.

---

## §9. Forbidden evidence / insufficient-evidence contract

### §9.1 Insufficient-on-its-own list (binding)

The following claims, presented as standalone closure
proof, MUST be rejected by any Step 4 review:

1. **"Just clone the repo."** Step 2 §5 / §7.5.
2. **"`pip install -e .` maybe works."** Step 2
   §5.2; latent capability ≠ supported boundary.
3. **`bootstrap_paths.ps1` alone.** Step 2 §5.1;
   PowerShell-only.
4. **`launch.ps1` alone.** Step 2 §5.3;
   discoverability only.
5. **`selfcheck.py` alone.** Step 2 §3.10 / §5.4;
   verification not install.
6. **`scripts/dev/README.md` alone.** Step 2 §5.4;
   names gap, does not close it.
7. **`docs/architecture/phase-1-entry.md:79-82`
   alone.** Step 2 §5.5; architecture, not recipe.
8. **`.github/workflows/dev-check.yml` alone.** Step
   2 §5.6; validates only bootstrap workflow.
9. **Ad-hoc tribal knowledge.** Step 2 §5.7.
10. **Hatchling PEP 660 default behaviour documented
    elsewhere.** Step 2 §5.2; not a repo-evidenced
    supported boundary.
11. **Screenshots of a working terminal.** Non-text,
    non-reproducible.
12. **Verbal commitments outside the recipe file.**
13. **Generic statements about future dev-tooling
    intent.** Aspiration, not commitment.

### §9.2 What MUST appear in the recipe as explicit denial

The recipe **MUST** explicitly deny each of the
following claims (verbatim quote acceptable;
explicit restatement acceptable; bare reference is
NOT sufficient for these specific phrases):

- "Developer workflow solved forever."
- "All IDE integrations supported."
- "All package managers supported for dev install."
- "Containerised dev environment shipped."
- "Remote-dev shipped."
- "Enterprise developer experience."
- "Production-ready DX."
- "DX matrix complete."

The recipe MUST collect these as a single "forbidden
maturity claims" sub-section under §7 of the recipe
(per §8.3 suggested structure) or in functionally
equivalent location.

### §9.3 What MUST NOT appear in any Track O artefact

- Real credentials of any kind.
- Real customer / operator / contributor host
  names, IP addresses, GitHub usernames, or email
  addresses.
- Vendor-specific cloud-platform references (AWS /
  GCP / Azure / Yandex / etc.) as required-tools
  claims; vendor names MAY appear only as
  out-of-scope examples.
- IDE vendor names as required-tools claims
  (VSCode / IntelliJ / Cursor / Zed / etc.); IDE
  names MAY appear only as out-of-scope examples.
- Forward-looking commitments to ship containerised
  dev, IDE integrations, remote-dev, or any of
  §1.4 forbidden categories.
- "Soon" / "in the next release" / "tracked for
  future work" framing applied to forbidden
  categories.
- Premature closure language for Track O itself
  before Step 6 (e.g., "Track O is closed"
  appearing in Step 3 / 4 / 5 artefacts).

---

## §10. Carry-forward invariants / backward compatibility

### §10.1 Tracks A–N runtime invariants

The following MUST remain byte-identical to their
state at Track N closure commit `2737a52`:

- All files enumerated in §8.5 "Production code".
- `pyproject.toml` (`version=0.5.2` preserved;
  `[tool.hatch.build.targets.wheel] packages`
  11-element array preserved; `[project.scripts]`
  three console entries preserved;
  `[project.dependencies]` empty preserved;
  `[tool.ruff]` and `[tool.pytest.ini_options]`
  preserved).
- All files enumerated in §8.5 "Existing scripts".
- All files enumerated in §8.5 "Existing operator
  recipes".
- `.python-version` (Python 3.11 pin preserved).
- CI workflow `.github/workflows/dev-check.yml`.

### §10.2 Track G / H invariants (transport + auth)

Preserved verbatim.

### §10.3 Track I invariants (installer round-trip)

Preserved verbatim.

### §10.4 Track J invariants (deployment-boundary)

Preserved verbatim.

### §10.5 Track K invariants (smoke harness)

`scripts/dev/mcp_client_smoke.py` byte-identical.

### §10.6 Track L invariants (service supervision)

Preserved verbatim.

### §10.7 Track M invariants (packaging / distribution)

Preserved verbatim, including the 11-element
`[tool.hatch.build.targets.wheel] packages` array
that is the foundational anchor for Track O's
editable-install posture (see §3.4).

### §10.8 Track N invariants (observability)

`docs/operators/observability.md` byte-identical;
Track N FC4 classification of `selfcheck.py`
inherited verbatim (see §6.5).

### §10.9 Registry invariant

`scripts/dev/selfcheck.py` MUST report `registries
read=15 / write=25 / intelligence=16` unchanged at
every Track O step.

### §10.10 No new MCP tools

The MCP tool surface is locked to the existing
56-tool inventory (15 + 25 + 16). No tool MAY be
added, removed, or renamed by Track O.

### §10.11 No 1cv8.exe, no real credentials, no remote push

Track O MUST NOT run `1cv8.exe`. Track O MUST NOT
commit real credentials. Track O MUST NOT execute
`git push` to any remote.

---

## §11. Verification contract for Step 4

### §11.1 Pre-commit verification (mandatory)

Before staging the Step 4 commit, the authoring
agent / operator **MUST** run all of:

V1. `git status` shows exactly one new file at the
    path locked in §8.2 (no modified files, no
    deleted files, no renamed files).
V2. `git diff --stat` confirms zero changes to any
    file enumerated in §8.5.
V3. `python scripts/dev/selfcheck.py` exits 0 and
    output line `selfcheck_status = ok` appears.
V4. The output includes registry counts equivalent
    to `read=15 / write=25 / intelligence=16`.
V5. `scripts/release/verify-release.ps1
    -AllowDirtyTree` exits 0 and all 8 named checks
    show `[PASS]` / `[WARN]` (no `[FAIL]`).
V6. Grep over the new file confirms it contains all
    six C2–C7 mandatory elements (per §4.1):
    supported install procedure (C2); supported
    tooling preconditions (C3); workspace-discovery
    answer (C4); verification step (C5); non-goals
    enumeration (C6); relationship-to-Track-M
    statement (C7).
V7. The new file contains at least the six explicit
    cross-references named in C8.
V8. The new file contains the cross-OS posture
    section per C9 / §5.3.
V9. The new file contains all eight mandatory
    denial phrases per §9.2.
V10. The new file MUST NOT contain real credentials
     (the existing `verify-release.ps1` Credential
     leak guard check covers this; cross-check
     should still apply).
V11. The new file MUST NOT contain premature
     closure language for Track O itself.
V12. The new file MUST NOT contain any of the
     forbidden maturity claims from §9.2 except as
     explicit denials.

### §11.2 Post-commit verification (mandatory)

After the Step 4 commit lands, **MUST** run:

P1. `git status` shows clean working tree.
P2. `git log -1` shows the new commit as the HEAD.
P3. `scripts/release/verify-release.ps1` (no
    `-AllowDirtyTree`) exits 0 and all 8 checks
    PASS on clean tree.
P4. `python scripts/dev/selfcheck.py` exits 0.

### §11.3 Step 5 verification carry-forward

Step 5 alignment commits MUST preserve V1–V12 and
P1–P4 except where Step 5 modifies the specifically
authorised CLASS-1 alignment files (README,
PROJECT-STATUS, possibly `docs/release-handoff.md`,
possibly `docs/developer-manual.md`, possibly
`scripts/dev/README.md` targeted line replacement
per §3.5).

### §11.4 Step 6 verification carry-forward

Step 6 closure commit MUST preserve V1–V12 and
P1–P4 except where Step 6 modifies README,
PROJECT-STATUS, CHANGELOG, and (only if Q7 = PATCH)
`pyproject.toml [project] version`. Q7 lock at
Step 6 MUST defend one of:

- **NO-BUMP** (default per §13.5 expectation): if
  Step 4 PATH A closed without code change. Mirrors
  Track J / Track K / Track L / Track N closure
  precedents.
- **PATCH** (`0.5.2 → 0.5.3`): explicitly
  prohibited under PATH A because no code change
  occurs.
- **MINOR**: explicitly prohibited by §1.4 (no new
  CLI flag, no new declared surface).
- **MAJOR**: explicitly prohibited by track scope.

Under PATH A, Step 6 Q7 outcome MUST be NO-BUMP.

### §11.5 Forbidden verification proxies

The following do NOT substitute for V1–V12 / P1–P4:

- "I tried `pip install -e .` once and it worked"
  — not a verification.
- "The recipe looks complete" — not a verification.
- "Step 2 audit said this would work" — Step 2 is
  evidence, not closure proof.
- "The forbidden-files list is mostly intact" — V2
  requires zero modifications, not "mostly intact".

---

## §12. Honest non-goals

### §12.1 Containerised dev / IDE / remote-dev non-goals

Track O **MUST NOT** introduce:

- A `Dockerfile` bundled at the repo root.
- A `docker-compose.yml`.
- A `.devcontainer/` configuration.
- Any IDE-specific bundle (`.vscode/`, `.idea/`,
  Cursor / Zed / Sublime / Vim project files).
- A Codespaces / GitPod / Coder template.

### §12.2 Multi-Python-version / build-backend non-goals

Track O **MUST NOT** introduce:

- A `tox.ini` / `nox.py` configuration.
- A multi-Python-version testing matrix in CI.
- Any change to `.python-version` (Python 3.11
  preserved).
- Any alternative-build-backend evaluation
  (hatchling remains).
- Any `[build-system].requires` change.

### §12.3 Tooling policy non-goals

Track O **MUST NOT** introduce:

- A change to `[tool.ruff]` (existing line-length
  100 and target-version py311 preserved).
- A change to `[tool.pytest.ini_options]`.
- A `tests/` directory shipping a test suite.
- An IDE configuration or linter rule extension.
- A formatter / linter / test-runner version pin.

### §12.4 Installable-from-git-URL non-goals

Track O **MUST NOT** introduce:

- A documented `pip install git+https://...` flow.
- A documented "download a zip and `pip install
  ./zip`" flow.
- Any non-checkout install path beyond Track M's
  wheel-distribution recipe (which remains operator-
  facing, not contributor-facing).

### §12.5 Cross-track non-goals

Track O **MUST NOT** introduce:

- A new MCP tool.
- A new CLI flag on any existing MCP server.
- A new `[project.scripts]` entry.
- A new project dependency.
- A new entrypoint module.
- A new env-var convention.
- A `/healthz` / `/readyz` / `/livez` endpoint.
- A new transport, auth scheme, deployment posture,
  service-supervision pattern, packaging format, or
  observability surface.

### §12.6 Other carry-over non-goals

- No `1cv8.exe` runs.
- No real-credential commits.
- No remote push.
- No rollback / AST / multi-version 1С matrix
  expansion.

---

## §13. Step 4 handoff note

### §13.1 Allowed Step 4 commit shape

Step 4 commit message subject **MUST** be:

```
Track O / Step 4 — editable install and workspace discovery recipe
```

(or a close functional equivalent that names the
recipe).

Commit body **MUST** cite this contract §§4 / 6 / 8 /
9 / 11 for closure-gate, recipe content, file
surface, denials, and verification respectively.

### §13.2 Allowed Step 4 file change set

Single addition at `docs/dev/editable-install-and-
workspace-discovery.md` (per §8.2). Nothing else.

### §13.3 Recipe authorship guidance (non-normative)

(This subsection is descriptive / advisory, NOT
normative. It is included to make Step 4 authoring
easier without expanding contract scope.)

The recipe SHOULD:

- Open with a one-paragraph "what this is and is
  not" statement, mirroring §1.1 / §1.2 of this
  contract.
- Use tables for the install-verb classification
  (first-class vs recommended-only) and the
  tooling preconditions.
- Use fenced shell snippets (`bash`, `pwsh`) for
  literal command examples — `python -m venv .venv`,
  `.\.venv\Scripts\Activate.ps1`, `pip install -e .`,
  `python scripts/dev/selfcheck.py`.
- Cite Track M's recipe by relative path (`../operators/
  packaging/distribution-boundary.md`).
- Cross-link back to the six anchors in C8 (file
  paths in monospace, plus brief inline
  descriptions of each anchor's role).
- Acknowledge the old hand-off-marker sentence at
  `scripts/dev/README.md:5-11` as historical
  context — the new recipe makes it obsolete, but
  the sentence itself remains until Step 5 narrowly
  replaces it.

### §13.4 Step 5 handoff expectations

After Step 4, Step 5 (docs / operator / release
alignment) MAY:

- Add at most one narrow bullet to
  `docs/release-handoff.md` pointing at the new
  recipe in the "Where to read deeper" list.
- Add a "Active parallel track: Track O at Step 5"
  / Step 4 transition note in `PROJECT-STATUS.md`.
- Add a CLASS-1 Quickstart-paragraph cross-
  reference in `README.md` to the new recipe.
- Narrowly replace the hand-off-marker sentences in
  `scripts/dev/README.md:5-11` and `:192-198` with a
  single pointer at the new recipe (per §3.5).
- Modify `docs/developer-manual.md` only if its
  prose develops direct factual drift from the new
  recipe content.

Step 5 MUST NOT modify any file in §8.5 except for
the five CLASS-1 alignment files just named.

### §13.5 Step 6 Q7 framing (lock at Step 6)

Under PATH A docs-only, Q7 default expectation =
**NO-BUMP**. Track O closes under existing `0.5.2`
without `pyproject.toml [project] version` change.
Mirrors Track J / Track K / Track L / Track N
NO-BUMP precedents:

- Track J — docs-only deployment-boundary recipe →
  Q7 = NO-BUMP.
- Track K — single new diagnostic file under
  `scripts/dev/` → Q7 = NO-BUMP.
- Track L — docs + one declarative systemd unit
  template → Q7 = NO-BUMP.
- Track N — docs-only observability recipe →
  Q6 = NO-BUMP.

Track O under PATH A is closest to Track J and
Track N: pure docs, no template, no helper, no
code-bearing change. Hence the default Q7 framing
is NO-BUMP.

Q7 lock is at Step 6; this contract pins the
expectation, not the final lock.

### §13.6 Track O closure target after Step 6

After Track O closure:

- README "Closed parallel tracks" list grows from
  14 entries to 15 (A through O).
- PROJECT-STATUS shows "Активного шага нет" again
  until an operator opens a future track.
- CHANGELOG appends a Track O closure narrative
  (under existing `0.5.2` section if Q7 = NO-BUMP,
  mirroring Track J/K/L precedent under `0.5.1` and
  Track N precedent under `0.5.2`).
- Fifteen post-phase parallel tracks (A–O) closed
  sequentially.

### §13.7 Forbidden Step 4 / 5 / 6 actions (recap)

Even though §8.5 and §10 are exhaustive, the most-
common Step 4 / 5 / 6 mistakes are explicitly named
here:

- ❌ Adding a `bootstrap_paths.sh` POSIX-shell
  sibling. (PATH B; rejected by §7.2.)
- ❌ Adding a developer bootstrap helper script.
  (PATH C; rejected by §7.3.)
- ❌ Adding a `[project.optional-dependencies]
  dev = [...]` block. (§5.4; rejected.)
- ❌ Touching `pyproject.toml` to add an editable-
  install comment block. (§3.1 invariant #7;
  rejected.)
- ❌ Creating a `tests/` directory with a test
  suite. (§12.3; rejected.)
- ❌ Adding a Dockerfile / `docker-compose.yml`
  "as a recommendation". (§12.1; rejected.)
- ❌ Adding a `.devcontainer/` configuration.
  (§12.1; rejected.)
- ❌ Adding an IDE-specific bundle (`.vscode/`,
  `.idea/`, etc.). (§12.1; rejected.)
- ❌ Adding a `tox.ini` for multi-Python testing.
  (§12.2; rejected.)
- ❌ Touching Track M's `distribution-boundary.md`
  to "centralise install guidance". (§10.7 / §8.5;
  rejected.)
- ❌ Adding a forward-looking sentence "Track P
  will add IDE integrations". (§9.3; rejected.)

---

## §14. Honest summary

**What this contract does.** Locks the final answers
to Step 1 plan Q1–Q5 (Q6 framed for Step 6 lock)
using repo evidence from Step 2 audit. Pins Step 4
PATH = **PATH A docs-only**. Pins the exact single-
file Step 4 deliverable at
`docs/dev/editable-install-and-workspace-discovery.md`.
Pins six mandatory recipe content elements (C2–C7
of §4.1). Pins the exhaustive forbidden-file
surface for Step 4 (§8.5). Pins the verification
protocol (§11). Preserves every Tracks A–N
invariant byte-identical (§10).

**What this contract does not do.** Does not
implement the recipe (Step 4 territory). Does not
align README / PROJECT-STATUS / CHANGELOG (Step 5 /
Step 6 territory). Does not lock Q7 SemVer outcome
(Step 6 territory; framed as NO-BUMP per §13.5).
Does not authorise any of the forbidden categories
in §1.4 / §12.

**Why one normative file is sufficient.** Step 2
established that the gap is integration-and-naming.
Step 3 contracts the integration shape and the
naming discipline in a single document; Step 4
ships the recipe; Step 5 / Step 6 close. Tracks J /
L / M / N each closed under similar single-
contract-file Step 3 patterns; Track O follows the
established pattern.

**Step 4 is unambiguously specified.** Path:
`docs/dev/editable-install-and-workspace-discovery.md`.
Content: contributor-facing recipe with six
mandatory elements (C2–C7), six mandatory cross-
references (C8), cross-OS posture (C9 / §5.3), and
all explicit denials from §9.2. Cap: ≤ 1000 lines
hard, ≤ 700 lines RECOMMENDED. Forbidden surface:
exhaustively enumerated in §8.5. Verification:
V1–V12 pre-commit, P1–P4 post-commit.

**No premature closure.** Track O is **active**.
Step 1 / Step 2 / Step 3 are closed; Step 4 / 5 / 6
remain. Phrases enumerated in §9.2 appear in this
contract only as DENIALS or as the verbatim list of
forbidden maturity claims that the recipe must
itself deny.

**Canonical next step.** Parallel Track O / Step 4
— narrow PATH A implementation: ship
`docs/dev/editable-install-and-workspace-discovery.md`
per §4 / §6 / §8. Opening Step 4 is a separate
operator decision; not auto-opened.
