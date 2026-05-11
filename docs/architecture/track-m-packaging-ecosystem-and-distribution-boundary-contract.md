# Parallel Track M — Packaging Ecosystem and Distribution Boundary — Contract

**Status.** Normative contract document produced by Track M /
Step 3 at HEAD `79c541f` (Track M / Step 2 closure). This
document uses RFC 2119 MUST / MUST NOT / SHOULD / SHOULD
NOT / MAY language. It pins the final Step 4 PATH and locks
every Step 4 / Step 5 / Step 6 boundary that derives from
the Step 2 baseline audit. It is **not** an implementation;
Step 4 implements within this contract's surface caps.

**Companion documents.**

- [`track-m-packaging-ecosystem-and-distribution-boundary-plan.md`](track-m-packaging-ecosystem-and-distribution-boundary-plan.md)
  — Step 1 planning document (14 sections, Q1–Q7
  directional defaults).
- [`track-m-packaging-ecosystem-and-distribution-boundary-step-map.md`](track-m-packaging-ecosystem-and-distribution-boundary-step-map.md)
  — Step 1 step-map (21 invariants, 21 categorical
  denials, 6-step boundary).
- [`track-m-packaging-ecosystem-and-distribution-boundary-baseline-audit.md`](track-m-packaging-ecosystem-and-distribution-boundary-baseline-audit.md)
  — Step 2 descriptive baseline audit (9 sections, 10
  enumerated absences, 16 handoff items, Q1–Q6
  directional resolutions).

---

## §1. Purpose / scope

### §1.1 What this contract is

A single prescriptive normative document that translates
the Step 2 audit's directional Q1–Q6 resolutions and 16
Step 3 handoff items into RFC 2119 MUST / MUST NOT /
SHOULD / SHOULD NOT / MAY rules. The contract pins the
final Step 4 PATH, the final primary artefact class, the
exact wheel contents, the exact wheel non-contents, the
allowed Step 4 file surface, the forbidden Step 4 file
surface, the closure-gate definition, the insufficient-
evidence list, the carry-forward invariants, and the
verification protocol. Step 4 implements **within** this
contract's surface caps; Step 5 / Step 6 operate within
this contract's forbidden-file lists.

### §1.2 What this contract is not

This contract is **not** an implementation. It does not
flip `[tool.hatch.build.targets.wheel] packages = []`, it
does not ship a recipe, it does not modify production
code. It does not rewrite Step 1 plan or Step 2 audit
anchors. It does not move Track M into README's Closed
parallel tracks list — Track M remains **active** through
Step 5; closure narrative is Step 6 territory only.

### §1.3 RFC 2119 keyword usage

The key words **MUST**, **MUST NOT**, **REQUIRED**,
**SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**,
**RECOMMENDED**, **MAY**, and **OPTIONAL** in this
document are to be interpreted as described in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

### §1.4 Track M scope reminder (binding)

In scope (carry-forward from plan §6, audit §1.3): planning,
audit, contract (this document), narrow implementation,
docs-alignment, and closure for packaging ecosystem +
distribution boundary; defining what counts as supported
distribution artefact; preserving every Tracks G / H / I /
J / K / L invariant byte-identical.

Out of scope (carry-forward verbatim from plan §7, step-
map "Track M hard out-of-scope", audit §1.3): broader
packaging ecosystem (`.msi` / `.deb` / `.rpm` / `.dmg` /
`.pkg` / `.apk` / `.snap` / `.flatpak`); multi-package-
manager publication (PyPI / Chocolatey / Homebrew / apt /
conda-forge / NuGet); signed-distribution chain; GUI
installer / wizard; transport / auth / deployment-
boundary / service-supervision redesign; enterprise
identity stack; clustering / HA / orchestration; web UI;
full observability stack; new MCP tools; registry changes;
new CLI flag on existing servers; new `[project.scripts]`
entries; new dependencies; `1cv8.exe` runs; remote push.
The phrases "packaging solved forever" / "PyPI release
ready" / "signed binary distribution" / "all package
managers supported" / "production-ready packaging" /
"enterprise-ready packaging" MUST appear in any Track M
deliverable only as explicit DENIALS.

---

## §2. Relationship to Step 1 plan and Step 2 audit

### §2.1 Step boundary

The six-step boundary established by the Step 1 step-map
is **binding**:

- Step 1 = planning (closed at `43bc9ae`).
- Step 2 = descriptive baseline audit (closed at
  `79c541f`).
- Step 3 = normative contract (this document).
- Step 4 = the **only** step that MAY add an
  implementation artefact or modify `pyproject.toml`.
- Step 5 = docs / release / operator alignment (narrow
  CLASS-1).
- Step 6 = final integration pass and track closure with
  explicit Q7 SemVer decision.

### §2.2 Re-litigation rule

Step 3 **MUST NOT** reopen Step 2 audit findings unless
new contradictory repo evidence emerges. The contract is
permitted to **tighten** directional resolutions into
normative locks, to **narrow** Step 4 PATH selection from
multiple acceptable options to a single chosen option, and
to **add** Step-4-specific caps and forbidden-file lists
that did not appear in the audit. It is **not** permitted
to soften, reverse, or contradict any Step 2 conclusion.

### §2.3 Carried-forward Q1–Q6 audit resolutions

Step 2 audit §7 produced six directional resolutions. This
contract **MUST** preserve their direction:

- Q1 audit-directional: closure-gate target = documented
  distribution-boundary recipe + one buildable artefact
  (single wheel).
  → Locked normatively below in §4 / §5 / §6.
- Q2 audit-directional: primary artefact class = single
  wheel (`.whl`); sdist as recommendation-only; operator-
  bundle rejected by default.
  → Locked normatively below in §5.
- Q3 audit-directional: PATH B (docs + narrow
  `pyproject.toml` wheel-build flip) as the honest
  narrowest path.
  → **Locked normatively below in §7 as PATH B.**
- Q4 audit-directional: mandatory for closure = artefact
  definition + build command + operator delivery + wheel
  contents + wheel non-contents.
  → Locked normatively below in §4 / §6.
- Q5 audit-directional: 9-item insufficient-evidence
  list.
  → Locked normatively below in §9.
- Q6 audit-directional: no production code change.
  → Locked normatively below in §8.

---

## §3. Inherited fixed decisions from Step 2

These observations from the Step 2 audit are **fixed
inputs** to this contract. The contract treats them as
load-bearing facts and does not re-prove them. Any attempt
to contradict them in Step 4 / Step 5 / Step 6 is
out-of-contract.

1. **Hatchling backend already declared.**
   `pyproject.toml:2-3` declares
   `requires = ["hatchling"]` and `build-backend =
   "hatchling.build"`. Audit §3.1 + §4.2. No build
   backend change is needed; the wheel will be produced
   by the already-declared hatchling backend.

2. **Three `[project.scripts]` console entries already
   declared but currently un-installable.**
   `pyproject.toml:22-25` declares `mcp-read-server`,
   `mcp-write-server`, `mcp-intelligence-server` →
   `mcp_<role>_server.__main__:main`. Audit §3.1 / §3.7
   / §6.10 establish that these entries are operator-
   aspirational today: a `pip install` against the repo
   does not currently produce functional console
   scripts because the wheel build is empty. Step 4
   PATH B makes these entries functional **without**
   adding new entries — the entries themselves remain
   locked.

3. **`[tool.hatch.build.targets.wheel] packages = []`
   intentionally empty.** `pyproject.toml:57`, with a
   verbatim 24-line Track C / Step 3 honest-constraint
   comment block at `pyproject.toml:34-57` explicitly
   anticipating "a future packaging track may revisit
   it" and naming two acceptable shapes (single-wheel
   layout containing all 11 packages, or multi-wheel
   split per package). Audit §3.1 / §4.1 / §3.6. Track
   M is that future packaging track.

4. **No buildable wheel artefact today.** `python -m
   build` against `pyproject.toml:57` `packages = []`
   produces no usable output. Audit §3.4 / §6.1.

5. **11 src-layout packages stable.** Four under
   `apps/*/src/` (`mcp_read_server`, `mcp_write_server`,
   `mcp_intelligence_server`, `onec_platform`) and seven
   under `packages/*/src/` (`mcp_common`,
   `onec_process_runner`, `onec_policy_engine`,
   `onec_audit`, `onec_health`, `onec_troubleshooting`,
   `onec_config`). Audit §4.4 / §8.4. These eleven
   packages are the operator-facing platform surface
   and are stable across Tracks G–L; flipping
   `packages = []` to a populated list referencing
   these eleven src paths is the narrowest honest
   wheel-build change.

6. **`.gitignore` already ignores build artefacts.**
   `.gitignore` enumerates `dist/`, `build/`,
   `*.egg-info/`. Audit §3.3. The repo intentionally
   does not track build outputs.

7. **`scripts/release/install.ps1` is config materialiser,
   not packaging.** Audit §3.2 / §5.1. Track M does not
   redesign the install fast path; the materialised
   config + a wheel become the two complementary
   artefacts (config side + Python distribution side).

8. **`docs/release-handoff.md` already enumerates
   packaging non-goals.** Audit §3.5. The "What is NOT
   in this handoff" list (rewritten by Track L / Step 5)
   already names every packaging-ecosystem non-goal.

9. **`apps/platform/src/onec_platform/runtime.py`
   byte-identical and NOT a service manager** (Track L
   §10.2 invariant carries forward). Audit §3 implicit
   carry-forward.

10. **`scripts/release/README.md` lines 215-246
    "Packaging-facing install flow (honest constraint)"
    section** verbatim documents the Track C /
    Step 3 honest constraint with full rationale.
    Audit §3.2. Track M's Step 4 recipe MUST
    cross-reference this section as the historical
    origin of the constraint Track M closes.

---

## §4. Closure-gate contract

### §4.1 Definition of "honest Track M closure"

Track M closure (Step 6) **REQUIRES** all of the following
to be true at Step 6 commit:

1. **C1 — Distribution-boundary recipe.** Exactly one
   operator-facing recipe document MUST exist at the
   Step-4-locked path under
   `docs/operators/packaging/` (see §8.2).
2. **C2 — Buildable artefact configuration.** Exactly
   one `pyproject.toml` change MUST be present:
   `[tool.hatch.build.targets.wheel] packages = []` is
   flipped to a populated list referencing the eleven
   src-layout package paths (see §5 / §6 / §8.3). The
   24-line Track C / Step 3 honest-constraint comment
   block at `pyproject.toml:34-56` MUST be updated to
   reflect the post-Track-M reality (the wheel build now
   produces a usable artefact); the line `packages = []`
   becomes `packages = [<list>]`.
3. **C3 — Wheel contents declaration.** The recipe MUST
   contain a section enumerating exactly which Python
   packages the wheel contains (the eleven src-layout
   packages from §5.2) and the exact `pyproject.toml`
   `packages` list line operators see.
4. **C4 — Wheel non-contents declaration.** The recipe
   MUST contain a section enumerating what the wheel
   does **not** contain (no operator credentials; no
   Track L systemd template; no Track J recipe; no
   real `ProductConfig` JSON; no `.env` file; no
   `examples/` data; no `docs/` content). See §6.3.
5. **C5 — Build verb documented.** The recipe MUST
   document the operator command to build the wheel
   (`python -m build`) plus the build's expected
   filesystem effect (output under `dist/`, with a
   `.whl` filename matching the project version).
6. **C6 — Install verb documented.** The recipe MUST
   document the operator command to install the wheel
   (`pip install <wheel-path>`) plus the expected
   operator-visible result (three console scripts on
   `PATH`: `mcp-read-server`, `mcp-write-server`,
   `mcp-intelligence-server`; all importable modules
   available).
7. **C7 — Placeholder discipline.** All examples in the
   recipe MUST use abstract placeholders only
   (`<WHEEL_PATH>`, `<CONTROL_HOST>`,
   `<DEPLOYMENT_HOST>`, `<VENV_PATH>`, `<VERSION>`).
   No real domains, ports, accounts, tokens, paths, or
   hostnames. The wheel itself MUST contain zero
   credentials by construction.
8. **C8 — Honest non-goals.** The recipe MUST contain
   explicit denial of "packaging solved forever",
   "PyPI release ready", "signed binary distribution",
   "all package managers supported", "production-ready
   packaging", "enterprise-ready packaging", "hostile-
   internet distribution ready", "automatic update /
   OTA", "GUI installer".
9. **C9 — Carry-forward invariants.** §10 invariants
   MUST all be observable as byte-identical in the
   Step 6 commit's `git diff` against the relevant
   surfaces.
10. **C10 — Verify-release GREEN.** `verify-release.ps1`
    (and `-AllowDirtyTree` during the working pass)
    MUST be GREEN on all 8 checks at every Track M
    commit from Step 3 onward.
11. **C11 — Selfcheck OK.** Registries `read=15 /
    write=25 / intelligence=16` and
    `selfcheck_status=ok` MUST be confirmed at every
    Track M commit from Step 3 onward.

### §4.2 What does NOT count as closure-gate proof

The following MUST NOT, on its own, be accepted as Track M
closure-gate evidence (locked from audit §5 / §6 / §7.5):

- **"Just clone the repo"** — that is the current state
  and the whole reason Track M exists.
- **Release-handoff prose only** — a paragraph in
  `docs/release-handoff.md` saying "to install the
  platform, build your own wheel" without an
  accompanying `pyproject.toml` flip and a recipe.
- **`install.ps1` helper only** — config materialiser,
  not packaging.
- **Commented TODOs in `pyproject.toml`** — the current
  24-line honest-constraint comment block is honest
  but does not close the gap; Track M MUST update it,
  not just leave another commented intention.
- **Generic packaging aspirations without a committed
  artefact boundary** — abstract prose ("the platform
  is packaging-ready") without a `pyproject.toml`
  change that makes the wheel actually buildable.
- **An sdist without a documented build recipe** —
  hatchling can produce a `.tar.gz` source archive,
  but without a recipe it is operator-hostile.
- **Adding new dependencies, new MCP tools, or new
  CLI flags** — these violate the Track M Step 1
  invariants and would expand scope.
- **PyPI publication metadata without actual
  publication** — adding `[project.urls]`,
  classifiers, keywords without shipping anywhere
  triggers the "PyPI release ready" non-goal cascade.
- **Multi-package-manager workflows** — Chocolatey /
  Homebrew / apt / conda-forge / NuGet manifests are
  out of scope.
- **Screenshots, video, or external-link-only
  evidence** — any non-text artefact.
- **A recipe without an executable wheel** — without
  the `pyproject.toml` flip, the recipe describes a
  build that does nothing operator-useful.
- **A `pyproject.toml` flip without a recipe** —
  flipping `packages = []` to `packages = [<list>]`
  without operator-facing documentation leaves
  operators unable to discover the new artefact.
- **Real credentials in the recipe or in any tracked
  file** — forbidden by §4.1 C7 and by `verify-
  release.ps1` Check 7 (credential leak guard).

### §4.3 What artefact proof Step 4 MUST commit

The Step 4 deliverables MUST commit, in repo:

- the recipe at the Step-4-locked path,
- the `pyproject.toml` flip that makes the wheel
  buildable.

The Step 4 commit MUST NOT commit the built `.whl` or
`.tar.gz` artefacts themselves — `.gitignore` already
excludes `dist/` / `build/`, and the artefacts are
build outputs the operator produces on demand. Step 4
verification protocol (§11.1 C5) instead verifies
buildability by demonstrating that the operator command
documented in the recipe produces a non-empty wheel
when run on a clean control host; this is a verifiable
recipe-correctness check, not a commit-the-output
check.

---

## §5. Primary artefact class contract

### §5.1 Locked: single wheel (`.whl`)

Step 4's primary artefact class **MUST** be a **single
buildable Python wheel** produced via `python -m build`
against the post-Track-M `pyproject.toml`. The wheel
filename will be `1c_agent_platform-0.5.1-py3-none-any.whl`
(if Q7 = NO-BUMP) or `1c_agent_platform-0.5.2-py3-none-any.whl`
(if Q7 = PATCH) at Step 6 — Step 4 does not change
`pyproject.toml` `version`.

### §5.2 Wheel contents — exact eleven packages

The Step 4 `pyproject.toml`
`[tool.hatch.build.targets.wheel]` `packages` list MUST
populate to exactly these eleven src-layout package
directories (no more, no fewer):

```toml
[tool.hatch.build.targets.wheel]
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

The contract chooses the **single-wheel layout** (one
wheel containing all 11 packages) explicitly named in
the Track C / Step 3 comment block as one of the two
acceptable shapes. The multi-wheel split is **rejected
in this Track M** as scope expansion (it would require
eleven `pyproject.toml` files or eleven build
invocations; operator delivery becomes more complex
for marginal benefit). A future track MAY revisit the
multi-wheel split; Track M MUST NOT.

### §5.3 Wheel non-contents — explicit denial list

The wheel **MUST NOT** contain any of the following.
Hatchling's default behaviour already excludes most;
the contract names them for clarity:

- No operator credentials of any form.
- No `.env` file with real values.
- No real `ProductConfig` JSON (e.g.,
  `examples/demo-infobase/infobase6.config.json` is
  excluded).
- No Track L systemd unit template
  (`docs/operators/service/mcp-server.service`).
- No Track J deployment-boundary recipe content.
- No `docs/` content (operator-facing prose stays in
  repo; not embedded in wheel).
- No `examples/` data (demo-infobase, demo-dumps).
- No `scripts/` content (PowerShell wrappers are
  operator-side, not Python-package content).
- No `.git/` data.
- No CI configuration.
- No `runbooks/` content.

The wheel is **only** the eleven Python packages
listed in §5.2. The recipe MUST cross-reference this
exclusion list operator-facingly.

### §5.4 Wheel platform tag

The wheel MUST be a **pure-Python wheel** with platform
tag `py3-none-any`. The codebase is stdlib-only (no
compiled extensions); hatchling produces a universal
wheel by default for this layout. The contract does NOT
authorise platform-specific wheels, `manylinux` /
`musllinux` / `win_amd64` / `macosx_*` variants, or
any wheel tag manipulation.

### §5.5 Source-archive (`sdist`) status

A source archive (`.tar.gz`) MAY be produced by hatchling
as a side-effect of `python -m build` (default
behaviour). The recipe MAY mention the sdist as a
**recommendation-only** complementary artefact for
operators who want a source-form delivery, but the
**closure-gate target is the wheel**. The sdist is
RECOMMENDED-only; it MUST NOT be the primary closure
artefact.

### §5.6 Operator-bundle artefact status

A zip / tarball / archive layout under a new `release/`
or `bundle/` directory **MUST NOT** be produced by
Step 4. Track M's narrowest honest closure path is
wheel + recipe; introducing a sibling operator-bundle
artefact would (a) duplicate the artefact-class
decision, (b) introduce a new filesystem-layout boundary
that operators must learn separately, (c) trigger
"operator bundle" PATH-C scope expansion that audit
§7.3 left explicitly available only "if Step 3 audit-
revealed reason". No such reason emerged in Step 2;
the contract closes PATH C.

---

## §6. Packaging / distribution boundary contract

### §6.1 What the distribution boundary is

The Track M distribution boundary **is** the wheel and
its accompanying recipe. The recipe explains:

1. Which Python packages the wheel contains (§5.2).
2. Which content the wheel does NOT contain (§5.3).
3. How to build the wheel (§4.1 C5; default command
   `python -m build`).
4. How to install the wheel (§4.1 C6; default command
   `pip install <wheel-path>`).
5. How to uninstall the wheel (§6.5 default command
   `pip uninstall 1c-agent-platform`).
6. How to upgrade an installed wheel (§6.6 default
   command `pip install --upgrade <wheel-path>`).
7. How to verify the install (§6.7 default check: the
   three console scripts appear on `PATH` and respond
   to `--help`).

### §6.2 What the distribution boundary is NOT

The Track M distribution boundary **is NOT**:

- a multi-package-manager publication channel;
- a PyPI release;
- a signed-distribution chain;
- an OS-native package;
- a GUI installer;
- a wizard;
- an automatic update mechanism;
- a hostile-internet distribution channel;
- a separate operator-bundle artefact alongside the
  wheel;
- a Track L service-supervision artefact alternative
  delivery path (Track L recipe + systemd template
  remain under `docs/operators/service/`);
- a Track J deployment-boundary artefact alternative
  delivery path (Track J recipe remains under
  `docs/operators/`);
- a replacement for `scripts/release/install.ps1`
  config materialisation (the install fast-path
  continues to materialise `ProductConfig` JSON
  separately from the wheel).

### §6.3 Five lifecycle verbs in the recipe

The recipe MUST document the five operator lifecycle
verbs end-to-end. Each verb has a default command and
expected operator-visible result:

| Verb | Operator command | Expected result |
|---|---|---|
| **build** | `python -m build` (run from project root on control host) | `dist/1c_agent_platform-<VERSION>-py3-none-any.whl` and `dist/1c_agent_platform-<VERSION>.tar.gz` appear; no errors; build toolchain (`build`, `hatch`, `hatchling`) is operator-installed prerequisite (see §6.8). |
| **install** | `pip install <WHEEL_PATH>` (run on deployment host with Python 3.11+) | Console scripts `mcp-read-server`, `mcp-write-server`, `mcp-intelligence-server` appear on `PATH`; `python -c "import mcp_read_server"` succeeds. |
| **uninstall** | `pip uninstall 1c-agent-platform` | Console scripts removed from `PATH`; `python -c "import mcp_read_server"` fails with `ModuleNotFoundError`. |
| **upgrade** | `pip install --upgrade <NEW_WHEEL_PATH>` | Console scripts re-point at new version; `python -c "import mcp_read_server"` succeeds with new code on `sys.path`. |
| **verify** | (a) `mcp-read-server --help` runs and exits 0; (b) optionally run `python scripts/dev/mcp_client_smoke.py --server read --transport both` from the repo against the installed wheel (Track K cross-reference). | Console script prints usage; smoke harness exits 0 if invoked. |

### §6.4 Build verb details (§4.1 C5 expansion)

- The recipe MUST name `python -m build` as the
  canonical build command.
- The recipe MUST state that `build` is an operator-
  side prerequisite (`pip install build`); it is **not**
  added to `pyproject.toml`'s `[project.dependencies]`
  (§8.4 forbidden). This MUST be operator-visible.
- The recipe MUST state the build output filename
  pattern (`1c_agent_platform-<VERSION>-py3-none-any.whl`).
- The recipe MUST state that `dist/` is `.gitignore`-d
  by repo policy; the built `.whl` lives on the
  control host and is operator-delivered to deployment
  host out-of-band.
- The recipe MUST NOT instruct the operator to publish
  the wheel anywhere.

### §6.5 Uninstall verb details

- The recipe MUST name `pip uninstall 1c-agent-platform`
  as the canonical uninstall command.
- The recipe MUST state that uninstall removes the
  three console scripts and the eleven importable
  packages, but does **not** remove operator-side
  artefacts: materialised `ProductConfig` JSON files,
  `.env` files, systemd unit files installed under
  `/etc/systemd/system/`, NSSM service registrations,
  launchd plists. Those have their own removal verbs
  (Track J / Track L recipes cross-referenced).

### §6.6 Upgrade verb details

- The recipe MUST name `pip install --upgrade <NEW_WHEEL_PATH>`
  as the canonical upgrade command.
- The recipe MUST state that upgrade replaces the
  installed wheel **only**; operator-side artefacts
  (config, service registrations) survive.
- The recipe MUST state that for systemd-supervised
  services (Track L), the operator typically wants to
  `systemctl restart <UNIT_NAME>` after upgrade so the
  new code is picked up.

### §6.7 Verify verb details

- The recipe MUST name `mcp-read-server --help` (or
  the equivalent for `mcp-write-server` /
  `mcp-intelligence-server`) as a minimum verify
  command — if the console script runs and prints
  usage, the install is functional.
- The recipe MAY cross-reference the Track K
  `scripts/dev/mcp_client_smoke.py` harness as
  recommendation-only deeper-verify path; the harness
  exercises the MCP method set externally over both
  stdio and HTTP transports.

### §6.8 Cross-OS posture

The wheel is `py3-none-any` (pure Python). It MUST
install on any host with Python 3.11+ regardless of
OS. The recipe MAY include OS-specific operator notes
where appropriate:

- Windows operators MAY use `py -m build` instead of
  `python -m build` if their Python installation uses
  the launcher.
- POSIX operators MAY use a `python -m venv .venv`
  workflow with `.venv/bin/pip install <wheel>`.
- Both patterns are operator-side choices; the
  contract requires only that the recipe acknowledge
  the cross-OS shape.

### §6.9 Relationship to `scripts/release/install.ps1`

The Track M wheel and the Track B / Track I install
fast-path are **orthogonal but complementary** artefacts:

- the wheel = Python distribution (the platform code);
- `install.ps1` = config materialiser (the deployment-
  side `ProductConfig` JSON).

The recipe MUST document this complementary
relationship: an operator typically (a) builds the
wheel on a control host; (b) copies the wheel to a
deployment host; (c) `pip install`s the wheel on the
deployment host; (d) runs `scripts/release/install.ps1`
to materialise their `ProductConfig` JSON; (e)
optionally installs the Track L systemd unit (or
equivalent cross-OS supervisor) referencing the
materialised config. Steps (a)–(c) are Track M
territory; steps (d)–(e) are Track B / Track I /
Track L territory carried forward.

---

## §7. Final Step 4 PATH selection

### §7.1 Locked: PATH B

Step 4's PATH **MUST** be **PATH B** — docs + narrow
`pyproject.toml` `[tool.hatch.build.targets.wheel]
packages = []` flip. Exactly two new/modified files
(see §8): one recipe doc + one `pyproject.toml` flip.

### §7.2 PATH A explicitly rejected

PATH A (docs-only, no `pyproject.toml` change) is
rejected. Audit §6.1 closure-gate observation ("zero
buildable wheel artefact at HEAD `79c541f`") cannot be
closed honestly by prose alone — the wheel build remains
empty regardless of how many recipes describe how the
operator would build the wheel "if the build worked".
Audit §7.3 leaned away from PATH A; contract locks the
rejection.

### §7.3 PATH C explicitly rejected

PATH C (operator-bundle artefact alongside / instead of
wheel) is rejected. Audit §7.2 found that hatchling is
already declared, three `[project.scripts]` are already
declared, and the src-layout is already stable —
flipping `packages = []` to a populated list is
mechanically narrower than constructing a parallel
`release/` / `bundle/` directory layout. Audit §5.6
acknowledged PATH C as available only "if Step 2 audit
revealed strong reason"; Step 2 audit found no such
reason. The contract closes PATH C.

### §7.4 No code change defended again

Step 4 MUST NOT modify any file under `apps/*/src/` or
`packages/*/src/`. Step 4 MUST NOT add a new helper
under `scripts/dev/` or `scripts/release/`. Step 4 MUST
NOT add a Python module. The only legitimate Step 4
outputs are the two files described in §8.

### §7.5 PATH B file shape

PATH B is exactly:

- **one new file**: the recipe at
  `docs/operators/packaging/distribution-boundary.md`
  (path locked in §8.2).
- **one modified file**: `pyproject.toml` (the
  `packages = []` flip and the accompanying 24-line
  comment-block update, both per §8.3).

Total Step 4 surface: exactly 2 files (1 new + 1
modified). No third file.

---

## §8. Exact Step 4 implementation surface

### §8.1 File count cap

Step 4 MUST add exactly **one** new file and modify
exactly **one** existing file. Step 4 MUST NOT create
any other new file under any other path, and MUST NOT
modify any other existing file. The forbidden-files list
in §8.5 is exhaustive.

### §8.2 Recipe file — exact path and required structure

The recipe file path **MUST** be:

```
docs/operators/packaging/distribution-boundary.md
```

The new directory `docs/operators/packaging/` MUST be
created by Step 4 specifically for this file. The
directory MUST NOT receive any other Step 4 file.

The recipe file MUST contain at minimum:

- §1 **Purpose** — what this document is for; what it
  is NOT for; explicit denial list per §4.1 C8.
- §2 **Supported distribution boundary** — the wheel
  is the supported artefact; `py3-none-any` pure-
  Python wheel; what is and is not in scope; why the
  Track C / Step 3 long-standing constraint is now
  closed.
- §3 **Wheel contents** — exact enumeration of the
  eleven src-layout packages (§5.2 list) plus the
  `pyproject.toml` `packages` list line operators see.
- §4 **Wheel non-contents** — exact denial list (§5.3
  list).
- §5 **Build verb** — `python -m build` walkthrough
  per §6.4 details; operator-side prerequisite
  (`pip install build`) named explicitly; expected
  output filename pattern; `.gitignore` policy
  reminder.
- §6 **Install verb** — `pip install <WHEEL_PATH>`
  walkthrough per §6.3 + §6.6 details; expected
  operator-visible result.
- §7 **Uninstall verb** — `pip uninstall
  1c-agent-platform` walkthrough per §6.5 details;
  what is NOT removed (operator-side artefacts).
- §8 **Upgrade verb** — `pip install --upgrade <NEW_WHEEL_PATH>`
  walkthrough per §6.6 details; Track L `systemctl
  restart` cross-reference.
- §9 **Verify verb** — `mcp-read-server --help`
  minimum check; Track K smoke-harness cross-reference
  for deeper verify (recommendation-only).
- §10 **Cross-OS posture** — Windows / POSIX operator-
  side notes per §6.8.
- §11 **Relationship to install fast path** — the wheel
  / config-materialiser orthogonal-but-complementary
  framing per §6.9.
- §12 **Honest non-goals** — the §6.2 list plus the
  §4.1 C8 explicit denial list.
- §13 **Cross-references** — to Track M Step 1 / Step 2
  / Step 3 docs (frozen anchors), to Track J recipe, to
  Track L recipe + systemd template, to Track K smoke
  harness, to `scripts/release/install.ps1` and
  `scripts/release/README.md` (specifically lines
  215-246 which document the now-closed Track C /
  Step 3 honest constraint).

The recipe file MUST be ≤ 1000 lines (soft cap); ≤ 1200
lines (hard cap). All examples MUST use abstract
placeholders only (§4.1 C7).

### §8.3 `pyproject.toml` modification — exact scope

The `pyproject.toml` modification MUST be:

1. **Lines 34-57 (the 24-line honest-constraint
   comment block) updated** to reflect post-Track-M
   reality. The comment block MAY be shortened
   significantly (the original block was anticipating
   a future packaging track; that future is now
   present). The updated comment block MUST briefly
   document:
   - the Track C / Step 3 historical origin of the
     long-standing empty `packages = []` state;
   - the Track M closure (this contract) that flipped
     it;
   - the cross-reference to the recipe at
     `docs/operators/packaging/distribution-boundary.md`;
   - the explicit denial list per §4.1 C8 (no PyPI
     publication, no signed distribution, no GUI
     installer, etc.) — same denials carried over to
     the post-Track-M comment block.
2. **Line 57 `packages = []` flipped** to
   `packages = [<11 src-layout paths>]` per the §5.2
   exact list.

The `pyproject.toml` modification MUST NOT:

- change `[project]` `version` (Step 6 / Q7 territory);
- change `[project]` `name`, `description`,
  `requires-python`, `readme`, `authors`;
- add `[project.urls]`, classifiers, keywords, or any
  other `[project]` field beyond the existing five;
- modify `[project.scripts]` (the three console entries
  are locked);
- add `[project.dependencies]` or
  `[project.optional-dependencies]`;
- modify `[build-system]` (hatchling backend is locked);
- modify `[tool.ruff]` or `[tool.pytest.ini_options]`;
- add any other `[tool.hatch.*]` block beyond the
  existing `[tool.hatch.build.targets.wheel]`;
- add `MANIFEST.in` (forbidden by §8.5);
- add `setup.py` or `setup.cfg` (forbidden by §8.5).

### §8.4 LOC and dependency caps

- Recipe (§8.2): ≤ 1000 lines soft; ≤ 1200 lines hard.
- `pyproject.toml` change (§8.3): net change ≤ ~30 LOC
  (the comment block shrinks and the `packages` list
  grows; the file remains under ~70 lines total).
- No new `[project.dependencies]` entries.
- No new `[project.optional-dependencies]` entries.
- No new `[project.scripts]` entries.
- No new dependencies of any kind for the recipe
  (Markdown only, no embedded scripts).

### §8.5 Forbidden file surface for Step 4 (exhaustive list)

Step 4 MUST NOT modify or create any file outside the
two listed in §8.2 / §8.3. The following list is
exhaustive — any file not listed here is **automatically
forbidden** for Step 4 by closure-of-scope discipline:

**Forbidden production code:**

- `apps/mcp-read-server/src/**`
- `apps/mcp-write-server/src/**`
- `apps/mcp-intelligence-server/src/**`
- `apps/platform/src/**` (specifically including
  `runtime.py`, `process_control.py`,
  `runtime_logs.py`, `models.py`, `state.py`,
  `installer.py`, `loader.py`).
- `packages/mcp-common/src/**` (specifically including
  `_stdio_transport.py`, `_network_transport.py`).
- All other `packages/*/src/**` files.

**Forbidden configuration / build / CI:**

- `.python-version`.
- `.editorconfig`.
- `.github/**`.
- `.gitignore`.
- `MANIFEST.in` (MUST NOT be created).
- `setup.py` (MUST NOT be created).
- `setup.cfg` (MUST NOT be created).

**Forbidden existing scripts:**

- `scripts/dev/launch.ps1`.
- `scripts/dev/bootstrap_paths.ps1`.
- `scripts/dev/run_dev_check.ps1`.
- `scripts/dev/selfcheck.py`.
- `scripts/dev/mcp_client_smoke.py`.
- `scripts/dev/README.md`.
- `scripts/release/install.ps1`.
- `scripts/release/_install_runner.py`.
- `scripts/release/verify-release.ps1`.
- `scripts/release/README.md`.
- Any new file under `scripts/dev/` or
  `scripts/release/` — Step 4 PATH C is rejected, so
  no wrapper script is permitted.

**Forbidden Track / closure docs:**

- `README.md`.
- `PROJECT-STATUS.md`.
- `CHANGELOG.md`.
- `SECURITY.md`.
- `LICENSE`.
- `docs/release-handoff.md`.
- `apps/platform/README.md`.
- `docs/operator-manual.md`.
- `docs/administrator-manual.md`.
- `docs/developer-manual.md`.
- `docs/runbooks.md`.
- `docs/version-support-matrix.md`.

**Forbidden Track-precedent artefacts:**

- `docs/operators/deployment-boundary.md`
  (Track J / Step 4 artefact).
- `docs/operators/service/service-supervision.md`
  (Track L / Step 4 artefact).
- `docs/operators/service/mcp-server.service`
  (Track L / Step 4 artefact).
- `docs/runbooks/track-a-reference-stand-round-trip.md`.
- All `docs/architecture/track-{a,b,c,d,e,f,g,h,i,j,k,l}-*.md`
  files.
- Track M Step 1 / Step 2 / Step 3 docs (this contract
  included).

**Forbidden examples / demo data:**

- `examples/**` (no demo-infobase changes; no demo-
  dumps changes).

**Forbidden new directories or files anywhere else.**
Any directory not named in §8.2 or specifically
`docs/operators/packaging/` itself is forbidden. The
new directory `docs/operators/packaging/` MAY contain
only the one file listed in §8.2; no `.gitkeep`, no
`README.md`, no other files.

---

## §9. Forbidden evidence / insufficient-evidence contract

### §9.1 Insufficient-on-its-own list (binding)

The following MUST NOT, individually or in any
combination short of meeting all of §4.1 C1–C11, count
as Track M closure-gate proof:

1. **"Just clone the repo"** — current state; Track M
   exists to close it.
2. **Launch instructions only** — paragraph in
   `README.md` or `docs/operator-manual.md`.
3. **Release-handoff prose only** — bullet in
   `docs/release-handoff.md` saying "to install,
   build your own wheel".
4. **Generic packaging aspirations** — abstract prose
   without `pyproject.toml` change.
5. **Operator lore not committed in repo** — chat
   logs, screenshots, operator-side notebooks.
6. **Recipe without `pyproject.toml` flip** — the
   recipe describes a build that does nothing today.
7. **`pyproject.toml` flip without a recipe** —
   operators have no documented entry point to the
   new artefact.
8. **An sdist without a documented build recipe** —
   `python -m build` produces `.tar.gz` alongside
   `.whl` by default; without recipe coverage, the
   sdist is operator-hostile.
9. **Adding new dependencies, new MCP tools, or new
   CLI flags** — violates §10 invariants and Step 1
   guardrails.
10. **PyPI publication metadata without actual
    publication** — adding `[project.urls]` /
    classifiers / keywords without shipping triggers
    the "PyPI release ready" non-goal cascade.
11. **Multi-package-manager workflows** — Chocolatey
    / Homebrew / apt / conda-forge / NuGet manifests
    are out of scope.
12. **A multi-wheel split** — the contract chose
    single-wheel layout per §5.2; splitting into
    eleven separate wheels is rejected scope
    expansion.
13. **Platform-specific wheels** — manylinux /
    musllinux / win_amd64 / macosx_* variants are
    out of scope per §5.4.
14. **Operator-bundle artefact instead of wheel** —
    PATH C rejected per §7.3.
15. **Real credentials in the recipe or wheel** —
    forbidden by §4.1 C7 and by
    `verify-release.ps1` Check 7.
16. **Screenshots, videos, or external-link-only
    evidence**.

### §9.2 What MUST appear in the recipe as explicit denial

The recipe MUST contain explicit DENIAL of each of
these phrases / claims (each may appear in the recipe
only as a negation):

- "packaging solved forever"
- "PyPI release ready"
- "signed binary distribution"
- "all package managers supported"
- "production-ready packaging"
- "enterprise-ready packaging"
- "hostile-internet distribution ready"
- "automatic update / OTA"
- "GUI installer"
- "the platform now publishes to PyPI"
- "Chocolatey / Homebrew / apt / conda-forge / NuGet
  support"

### §9.3 What MUST NOT appear in any Track M artefact

The following phrases MUST NOT appear in any Track M
artefact (this contract, the Step 4 recipe, the Step 4
`pyproject.toml` updated comment block) except as
quoted explicit denials:

- "PyPI ready" / "PyPI publication"
- "signed distribution" / "signing key" / "cosign" /
  "sigstore"
- "GUI installer" / "wizard"
- "Chocolatey" / "Homebrew" / "apt" / "conda-forge" /
  "NuGet"
- ".msi" / ".deb" / ".rpm" / ".dmg" / ".pkg" / ".snap"
  / ".flatpak"
- "enterprise-ready"
- "production-grade packaging"

---

## §10. Carry-forward invariants / backward compatibility

Step 4 / Step 5 / Step 6 commits MUST preserve all of
these byte-identical:

### §10.1 Tracks G / H / I / J / K / L runtime invariants

- **Track G stdio runtime** —
  `packages/mcp-common/src/mcp_common/_stdio_transport.py`
  byte-identical.
- **Track H HTTP runtime** —
  `packages/mcp-common/src/mcp_common/_network_transport.py`
  byte-identical. `/mcp` POST-only; 1 MiB body cap;
  bearer auth with failure-equivalence + redaction
  discipline; `WWW-Authenticate: Bearer realm="mcp"`
  on 401; non-`/mcp` 404 deterministic.
- **Track I installer auth round-trip** —
  `apps/platform/src/onec_platform/installer.py`
  byte-identical.
- **Track J deployment-boundary recipe** —
  `docs/operators/deployment-boundary.md` byte-
  identical.
- **Track J carry-forward §13 / §6 / §7 / §8** —
  in-process TLS forbidden; mTLS forbidden; Forwarded
  headers MUST-NOT-consume; `/healthz` not shipped.
- **Track K diagnostic harness** —
  `scripts/dev/mcp_client_smoke.py` byte-identical.
- **Track L recipe + systemd template** —
  `docs/operators/service/service-supervision.md` and
  `docs/operators/service/mcp-server.service` byte-
  identical.

### §10.2 Platform-layer invariants

- **`apps/platform/src/onec_platform/runtime.py`** —
  byte-identical. Track M MUST NOT extend it. Track L
  §10.2 invariant carries forward.
- **`apps/platform/src/onec_platform/process_control.py`** —
  byte-identical.
- **`apps/platform/src/onec_platform/runtime_logs.py`** —
  byte-identical.
- **`apps/platform/src/onec_platform/models.py`** —
  byte-identical.

### §10.3 Registry invariants

- `mcp-read-server` registry: 15 tools.
- `mcp-write-server` registry: 25 tools.
- `mcp-intelligence-server` registry: 16 tools.

`selfcheck status=ok` and the four-line registry
summary MUST be confirmed via `verify-release.ps1` at
every Track M commit from Step 3 onward.

### §10.4 `pyproject.toml` invariants

Step 4 may modify `pyproject.toml` only within the
narrow scope locked in §8.3. Every other field MUST
remain byte-identical to the Track M Step 2 closure
state:

- `[build-system] requires` / `build-backend` byte-
  identical.
- `[project] name` / `version` (`0.5.1`) /
  `description` / `requires-python` / `readme` /
  `authors` byte-identical at Steps 3 / 4 / 5. Step 6
  MAY modify `version` only if Q7 = PATCH or MINOR;
  default Q7 = PATCH most likely (closing the long-
  standing Track C / Step 3 empty-wheel-build
  constraint is legitimate defect-class repair
  framing).
- `[project.scripts]` byte-identical at every step
  (three entries locked; no addition; no removal).
- `[tool.ruff]` byte-identical.
- `[tool.pytest.ini_options]` byte-identical.

### §10.5 No new MCP tools, no registry change

- Step 4 / Step 5 / Step 6 MUST NOT add any new tool to
  any of the three MCP servers.
- Step 4 / Step 5 / Step 6 MUST NOT modify any tool
  registration.
- Step 4 / Step 5 / Step 6 MUST NOT modify
  `mcp_common/__init__.py` `__all__`.

### §10.6 No 1cv8.exe, no real credentials, no remote push

- No `1cv8.exe` runs at any step.
- No real credentials in any committed file.
  Placeholder vocabulary (§4.1 C7) is the only
  acceptable form.
- No remote push at any step. GitHub push remains an
  explicit operator action outside the track.

---

## §11. Verification contract for Step 4

### §11.1 Pre-commit verification (mandatory)

Before the Step 4 commit, the following MUST be
verified, in this order, with each result captured in
the Step 4 commit body:

**Scope checks (S1–S6):**

- **S1.** Exactly one new file at
  `docs/operators/packaging/distribution-boundary.md`.
  Verified by `git status --short` showing exactly
  one `??` line for that path.
- **S2.** Exactly one modified file at
  `pyproject.toml`. Verified by `git status --short`
  showing exactly one ` M ` line for that path.
- **S3.** Total file count: 2 (1 new + 1 modified).
  No other new or modified files.
- **S4.** No file in §8.5's forbidden list is touched.
  `git diff --name-only` returns only the two paths.
- **S5.** Recipe file LOC ≤ 1200 (hard cap, §8.4).
- **S6.** `pyproject.toml` change scope per §8.3:
  only the comment block at lines ~34-56 and the
  `packages = []` → `packages = [...]` line are
  changed; all other `pyproject.toml` content byte-
  identical.

**Selfcheck checks (Z1–Z2):**

- **Z1.** `verify-release.ps1 -AllowDirtyTree`
  selfcheck line shows registries `read=15 / write=25
  / intelligence=16` and `status=ok`.
- **Z2.** No registry drift since Track L closure
  (`e21e185`).

**Release-verify check (R1):**

- **R1.** `verify-release.ps1 -AllowDirtyTree` GREEN
  on all 8 checks pre-commit.

**Build-buildability check (B1) — recommendation-only:**

- **B1.** Optionally, on a control host with the
  `build` toolchain installed: `python -m build`
  produces a non-empty `.whl` under `dist/` whose
  filename matches `1c_agent_platform-0.5.1-py3-none-any.whl`
  and whose contents include the eleven src-layout
  packages from §5.2. This check is RECOMMENDED but
  not closure-blocking — the build toolchain is not
  in documented dev prerequisites per
  `pyproject.toml`'s updated comment block, and Step 4
  closes on the declarative-flip + recipe artefacts.
  Operators verify buildability on their own control
  hosts.

**Honesty checks (H1–H8):**

- **H1.** No `1cv8.exe` invocation in Step 4 work or
  commit message.
- **H2.** No real credentials in either Step 4 file
  or commit message. Placeholder discipline (§4.1 C7)
  observable: only `<WHEEL_PATH>`, `<CONTROL_HOST>`,
  `<DEPLOYMENT_HOST>`, `<VENV_PATH>`, `<VERSION>`,
  `<NEW_WHEEL_PATH>` appear as concrete example
  values.
- **H3.** No premature Track M closure language in
  Step 4 commit message. "Closed", "closure", "fully
  solved" appear only in references to **Step 4
  itself being closed**, not Track M being closed
  (Step 6 is the closure step).
- **H4.** No false implementation claims. The recipe
  MUST NOT claim "PyPI release ready", "signed
  distribution", "all package managers supported",
  "production-ready packaging", "enterprise-ready
  packaging", "GUI installer" except as explicit
  denials per §9.2.
- **H5.** No new MCP tools claimed; registries
  `15 / 25 / 16` unchanged.
- **H6.** No fake closure phrases. Per §9.3, the
  forbidden phrases appear in the artefact only as
  quoted explicit denials.
- **H7.** No remote push performed by Step 4.
- **H8.** The wheel itself MUST contain zero
  credentials by construction. Verified by §5.3
  exclusion list discipline (hatchling default
  behaviour excludes `docs/`, `examples/`,
  `scripts/`, `.git/`; the wheel `packages` list
  enumerates only the 11 src-layout package dirs).

**Recipe coverage checks (C1–C13):**

- **C1.** Recipe section count ≥ 13 (§8.2).
- **C2.** Recipe contains exact §5.2 wheel-contents
  enumeration.
- **C3.** Recipe contains exact §5.3 wheel-non-
  contents exclusion list.
- **C4.** Recipe contains all five lifecycle verbs
  (build / install / uninstall / upgrade / verify)
  per §6.3.
- **C5.** Recipe documents `python -m build` as
  build verb with operator-side prerequisite
  (`pip install build`) called out.
- **C6.** Recipe documents `pip install <WHEEL_PATH>`
  as install verb with expected operator-visible
  result.
- **C7.** Recipe contains §9.2 explicit-denial list
  with each phrase appearing as a quoted negation.
- **C8.** Recipe contains §6.9 install-fast-path
  orthogonality cross-reference.
- **C9.** Recipe contains §8.2 §13 cross-references
  to Track M Step 1/2/3 docs + Track J recipe +
  Track L recipe + Track L systemd template + Track
  K harness.
- **C10.** Recipe uses placeholders exclusively per
  §4.1 C7.
- **C11.** Recipe LOC within §8.4 caps.
- **C12.** `pyproject.toml` comment-block update per
  §8.3 cross-references the recipe path.
- **C13.** `pyproject.toml` `packages` list matches
  the §5.2 list exactly.

### §11.2 Post-commit verification (mandatory)

Step 4's commit MUST be followed by:

- **P1.** `verify-release.ps1` (clean tree) GREEN on
  all 8 checks.
- **P2.** Working tree clean (`git status` returns
  `nothing to commit, working tree clean`).
- **P3.** New commit count = HEAD pre-commit + 1.
- **P4.** Step 4 commit message subject = exactly
  `Track M / Step 4 — packaging recipe and wheel-build flip`
  (or other Step-4-canonical subject locked at Step 4
  drafting; this contract does not pre-lock the exact
  subject string, only the file surface and the
  verification protocol).

### §11.3 Step 5 verification carry-forward

Step 5 MUST satisfy:

- **V1.** Production code byte-identical to Step 4
  commit.
- **V2.** `pyproject.toml` byte-identical to Step 4
  commit (Step 5 does NOT touch pyproject; Step 6
  may touch only `version`).
- **V3.** `scripts/*` byte-identical to Track L
  closure (no new wrapper script per PATH C
  rejection).
- **V4.** Step 4 deliverables byte-identical to
  Step 4 commit.
- **V5.** Track L and earlier deliverables byte-
  identical.
- **V6.** `verify-release.ps1` GREEN.
- **V7.** Selfcheck OK; registries unchanged.

Step 5 MAY modify only:

- `README.md` Quickstart paragraph + "Active parallel
  track" section to reflect Steps 1–4 closed and
  Step 5 active.
- `docs/release-handoff.md` — one bullet in "What is
  in this handoff" pointing at the Step 4 recipe;
  rewrite of the "No wheel-based install" line in
  "What is NOT in this handoff" to reflect that the
  wheel is now buildable (but **not** published); one
  bullet in "Where to read deeper".
- `apps/platform/README.md` — only if Step 4
  introduces a packaging boundary that the platform
  README's existing inventory reasonably mentions;
  default expectation = no edit.
- `SECURITY.md` — only if Step 4 ships a security-
  relevant section; default expectation = no edit
  (the wheel is placeholder-only and ships no
  credentials).
- `scripts/release/README.md` — only if Step 4
  introduces a release-side surface that the existing
  "no install ecosystem" framing develops drift;
  default expectation = no edit (the existing
  packaging-honest-constraint section at lines
  215-246 may receive a cross-link update; that is
  the only allowed change).

Step 5 MUST NOT modify Track M closed-tracks list,
PROJECT-STATUS, CHANGELOG, or `pyproject.toml`
`version` — those are Step 6 territory.

### §11.4 Step 6 verification carry-forward

Step 6 MUST satisfy:

- **W1.** Production code byte-identical.
- **W2.** `scripts/*` byte-identical.
- **W3.** Step 4 deliverables byte-identical
  (immutable Step 4 anchors).
- **W4.** Track M Step 1 / 2 / 3 deliverables byte-
  identical (immutable anchors).
- **W5.** `pyproject.toml` MAY be modified **only**
  to `version` — only if Q7 = PATCH (`0.5.1 → 0.5.2`)
  or MINOR (`0.5.1 → 0.6.0`) is honestly defended in
  the Step 6 commit body. Q7 = PATCH is the default
  expectation per §10.4 and audit §7.6 + §8.15 (the
  long-standing Track C / Step 3 honest constraint is
  closed by Step 4 PATH B; this is legitimate defect-
  class repair framing). MINOR considered only if
  Step 4 ships net-new operator-facing capability
  beyond making existing declarations functional —
  default expectation rejects MINOR per §15 step-map
  invariant.
- **W6.** README / PROJECT-STATUS / CHANGELOG MAY be
  modified to reflect Track M closure.
- **W7.** `verify-release.ps1` GREEN pre-commit and
  post-commit.
- **W8.** Selfcheck OK; registries unchanged.

### §11.5 Forbidden verification proxies

The following MUST NOT be used as substitute proof for
any §11 check:

- Manual operator confirmation in chat.
- Screenshot of `pip install` output.
- External video demo.
- "Worked on my machine" assertions in commit messages.
- Soft "should work" language without concrete `git
  diff` / `verify-release` / `selfcheck` output.

---

## §12. Honest non-goals

By Step 6 closure under this contract, Track M will
**NOT** have delivered any of the following. Each is an
explicit denial:

### §12.1 Publication / distribution-channel non-goals

- No PyPI publication.
- No Chocolatey publication.
- No Homebrew publication.
- No apt / rpm repository publication.
- No conda-forge publication.
- No NuGet publication.
- No internal package-mirror publication automation.
- No release-CI-pipeline ship.

### §12.2 OS-native package non-goals

- No `.msi` / `.deb` / `.rpm` / `.dmg` / `.pkg` /
  `.apk` / `.snap` / `.flatpak` artefacts.
- No platform-specific wheel variants (manylinux /
  musllinux / win_amd64 / macosx_*).
- No SystemV-init / upstart packages.

### §12.3 Signed-distribution non-goals

- No signing keys committed to repo.
- No `cosign` / `sigstore` / Authenticode /
  Notarisation / SBOM / SLSA attestation workflow.
- No checksum file.
- No release attestation publication.

### §12.4 Installer / GUI non-goals

- No GUI installer / wizard / setup.exe.
- No PowerShell `Install-Module`-style auto-install
  helper.
- No `nssm install`-style bundled service registration
  (Track L recipe carries forward separately).

### §12.5 Identity / auth / multi-tenant non-goals

- No SSO / SAML / OIDC / SCIM / RBAC / ABAC / multi-
  tenant identity bound to packaging.
- No per-tenant wheel variants.
- No license-key embedding.
- No telemetry collection from installed wheels.

### §12.6 Update / rollback non-goals

- No automatic update / OTA / self-upgrade mechanism.
- No version-rollback automation.
- No diff-based update.
- No delta-update.

### §12.7 Other carry-over non-goals

- No web UI / dashboard frontend.
- No standalone `apps/platform` daemon entrypoint.
- No clustering / HA / orchestration platforms
  (Kubernetes / Compose / Nomad / Consul / etcd /
  Zookeeper) bound to packaging.
- No `/healthz` / `/readyz` / `/livez` endpoint —
  Track J §8 defer carried forward.
- No rollback expansion / AST work / 1С matrix
  expansion.
- No new MCP tools / registry change.
- No `1cv8.exe` runs anywhere in Track M.
- No real credentials.
- No remote push.

---

## §13. Step 4 handoff note

This contract hands the following exact items to Step 4
for implementation. Step 4 MUST satisfy each item
without expansion:

1. **File count: exactly two.** One new file at the
   §8.2 path; one modified file at `pyproject.toml`.
   No other new files. No other modified files.
   Verified by §11.1 S1–S3.

2. **Recipe file location:**
   `docs/operators/packaging/distribution-boundary.md`.
   New `docs/operators/packaging/` directory; co-
   located with Track J's `docs/operators/` and
   Track L's `docs/operators/service/`. No other
   location.

3. **Recipe content: ≥ 13 sections per §8.2 structure.**
   Each section MUST be present.

4. **`pyproject.toml` modification scope: §8.3
   only.** Comment-block update + `packages` list
   flip; no other `pyproject.toml` field touched.

5. **`packages` list contents: exactly §5.2 list.**
   Eleven src-layout package paths, no more, no
   fewer.

6. **Wheel non-contents: §5.3 list documented in
   recipe.**

7. **Five lifecycle verbs documented procedurally per
   §6.3 / §6.4 / §6.5 / §6.6 / §6.7.** All five
   mandatory; partial coverage rejected.

8. **Placeholder vocabulary fixed (§4.1 C7 + §11.1
   H2).** Only these placeholders MAY appear:
   `<WHEEL_PATH>`, `<NEW_WHEEL_PATH>`,
   `<CONTROL_HOST>`, `<DEPLOYMENT_HOST>`,
   `<VENV_PATH>`, `<VERSION>`, `<UNIT_NAME>` (cross-
   reference to Track L only). No real values.

9. **Honest non-goals per §9.2 / §12.** Recipe MUST
   contain each denial as a quoted negation. No false
   maturity claims.

10. **Cross-references per §8.2 §13.** Recipe MUST
    cross-reference Track M Step 1/2/3 docs (frozen
    anchors), Track J recipe, Track L recipe +
    systemd template, Track K harness, install
    fast-path script, and `scripts/release/README.md`
    lines 215-246 (the now-closed Track C / Step 3
    honest-constraint section).

11. **Verification per §11.1.** All scope / selfcheck
    / release-verify / honesty / recipe coverage
    checks MUST PASS pre-commit. Each check's outcome
    MUST be captured in the Step 4 commit body.

12. **Commit message discipline.** Step 4 commit
    message body MUST include: §11.1 verification
    summary; Step 4 file paths + change types
    (1 new + 1 modified); explicit "Track M still
    active" framing; no premature closure language;
    explicit denial that Step 4 closes Track M (only
    Step 6 does).

13. **No production code change.** §10.1 / §10.2
    invariants byte-identical.

14. **No `pyproject.toml` change outside §8.3 scope.**
    `version`, `[project.scripts]`, `[build-system]`,
    `[tool.ruff]`, `[tool.pytest.ini_options]`,
    `[project]` metadata fields (other than
    intentional comment-block update around the
    `packages = []` flip) all byte-identical.

15. **No `scripts/*` change.** §8.5 forbidden list.

16. **No README / PROJECT-STATUS / CHANGELOG change.**
    Those are Step 5 / Step 6 territory.

17. **No external publication.** Step 4 MUST NOT push
    the wheel to PyPI / Chocolatey / Homebrew / apt /
    conda-forge / NuGet / any other channel. The
    wheel exists only as a Step-4-described build
    output on the operator's control host; the repo
    commits only the recipe + the `pyproject.toml`
    flip.

---

## §14. Honest summary

**This contract pins Step 4.** Two files: one new
recipe at `docs/operators/packaging/distribution-
boundary.md` and one modified `pyproject.toml` with a
narrow `[tool.hatch.build.targets.wheel] packages = []`
→ populated-list flip plus an updated comment block.
PATH B locked. PATH A and PATH C explicitly rejected.
Single-wheel layout containing the eleven src-layout
packages locked. Five lifecycle verbs (build / install
/ uninstall / upgrade / verify) mandatory in the
recipe. No production code change. No new
dependencies. No new `[project.scripts]`. No new CLI
flag.

**This contract does not pin Q7.** Step 6 chooses Q7;
the default expectation is **PATCH** (`0.5.1 → 0.5.2`)
per §10.4 and audit §7.6 — the long-standing Track C /
Step 3 honest constraint about the empty wheel build
is closed by Step 4 PATH B, which is legitimate defect-
class repair framing. NO-BUMP acceptable only if Step 4
PATH A had been chosen (it was not); MINOR considered
only if Step 4 ships net-new capability beyond making
existing declarations functional — default expectation
rejects MINOR.

**This contract preserves every prior track
invariant.** §10 enumerates them; §8.5 enforces them
via the forbidden-file list; §11 verification catches
drift.

**This contract makes Track M closable in the
narrowest honest way.** Two files in repo, eleven
packages in one wheel, five lifecycle verbs documented,
the long-standing Track C / Step 3 honest constraint
finally closed, every prior-track surface untouched,
every false-maturity claim explicitly denied, no
production code change, no `[project.scripts]`
addition, no new dependencies, no `scripts/*` change,
no registry change, no `1cv8.exe` runs, no real
credentials, no remote push, no PyPI publication, no
OS-native package, no signed-distribution chain, no
GUI installer.

**Track M is active at Step 3.** Step 3 closes with
this contract. Step 4 is the next step and MAY be
opened by the operator in a separate session. Closure
narrative remains Step 6 territory.
