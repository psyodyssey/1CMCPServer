# Parallel Track M — Packaging Ecosystem and Distribution Boundary — Baseline Audit

**Status.** Descriptive baseline audit produced by Track M /
Step 2 at HEAD `43bc9ae` (Track M / Step 1 closure). This
document is **not** a contract. It does **not** use RFC 2119
MUST / MUST NOT / SHOULD / MAY language. All "decisions"
appear here as directional resolutions grounded in repo
evidence, intended for Step 3 contract consumption. Step 3
locks; Step 2 observes.

**Companion documents.**

- [`track-m-packaging-ecosystem-and-distribution-boundary-plan.md`](track-m-packaging-ecosystem-and-distribution-boundary-plan.md)
  — Step 1 planning document (14 sections, Q1–Q7 directional
  defaults).
- [`track-m-packaging-ecosystem-and-distribution-boundary-step-map.md`](track-m-packaging-ecosystem-and-distribution-boundary-step-map.md)
  — Step 1 step-map document (21 invariants, 21 categorical
  denials, 6-step boundary).

---

## §1. Purpose / scope

### §1.1 What this audit is

A single descriptive read-only inventory of every repo
surface that is either (a) part of the current packaging /
build / distribution story for the platform, or (b) part
of an **adjacent** install / release-side layer that
already exists. The audit grounds Step 3's contract
decisions in repo facts at HEAD `43bc9ae`, not in wishful
thinking.

### §1.2 What this audit is not

Not a Step 3 contract. Not a Step 4 implementation. Not a
closure narrative. Not a rewrite of Track M Step 1
planning docs. Not a normative MUST-language document.
Not an attempt to commit pre-emptively to PATH A / PATH B
/ PATH C — those are Step 3 contract territory.

### §1.3 Track M scope reminder (carry-forward from Step 1)

In scope: planning / audit / contract (this is the audit
step) / narrow implementation / docs-alignment / closure
for packaging ecosystem + distribution boundary; defining
what counts as supported distribution artefact;
preserving Tracks G/H/I/J/K/L invariants byte-identical.

Out of scope (carry-forward verbatim from plan §7, step-
map "Track M hard out-of-scope"): broader packaging
ecosystem (`.msi` / `.deb` / `.rpm` / `.dmg` / `.pkg` /
`.apk` / `.snap` / `.flatpak`); multi-package-manager
publication (PyPI / Chocolatey / Homebrew / apt / conda-
forge / NuGet); signed-distribution chain; GUI installer
/ wizard; transport / auth / deployment-boundary /
service-supervision redesign; enterprise identity stack;
clustering / HA / orchestration; web UI; full
observability stack; new MCP tools; registry changes; new
CLI flag on existing servers; new `[project.scripts]`
entries; new dependencies; `1cv8.exe` runs; remote push.
The phrases "packaging solved forever" / "PyPI release
ready" / "signed binary distribution" / "all package
managers supported" / "production-ready packaging" /
"enterprise-ready packaging" MUST appear in any Track M
deliverable only as explicit DENIALS.

---

## §2. Method / evidence sources

The audit observes the repo at HEAD `43bc9ae` via these
mechanisms only — no `1cv8.exe`, no real-network probe,
no remote push, no production code change:

- **Whole-repo grep** (ripgrep via the Grep tool, case-
  insensitive) for the packaging-vocabulary terms:
  `wheel`, `sdist`, `dist/`, `MANIFEST.in`, `setup.py`,
  `setup.cfg`, `.msi`, `.deb`, `.rpm`, `.dmg`, `.pkg`,
  `signing`, `PyPI`, `Chocolatey`, `Homebrew`,
  `conda-forge`, `cosign`, `sigstore`, `SBOM`, `SLSA`,
  `hatch`, `hatchling`, `bdist`, `twine`.
  Coverage: every `.py`, `.md`, `.ps1`, `.toml`,
  `.json`, `.sh` tracked file.
- **Targeted reads** of `pyproject.toml` (57 lines
  total), `scripts/release/install.ps1`,
  `scripts/release/_install_runner.py`,
  `scripts/release/verify-release.ps1`,
  `scripts/release/README.md` (247 lines),
  `docs/release-handoff.md` head + "What is NOT in this
  handoff" + "Known limitations" sections.
- **Directory listings** for `dist/`, `release/`,
  `build/`, project root for `*.whl` / `*.tar.gz` (all
  return "no such directory" / "no matches").
- **`.gitignore`** read for build-artefact ignore rules.
- **Track C architecture docs glob**
  (`docs/architecture/track-c-*.md`) — confirms Track C
  plan + step-map are the prior packaging-related
  artefacts in repo.
- **`verify-release.ps1`** GREEN on 8 checks at HEAD =
  baseline-state guarantee that registries are
  `15 / 25 / 16` and `selfcheck status=ok`.

No file was modified during the evidence-gathering pass.
All commands were read-only.

---

## §3. Current packaging / distribution baseline

### §3.1 `pyproject.toml` declared surface (57 lines total)

Verbatim from `pyproject.toml`:

- **Lines 1-3** — build backend declaration:
  ```toml
  [build-system]
  requires = ["hatchling"]
  build-backend = "hatchling.build"
  ```
  Hatchling is declared as the build backend.

- **Lines 5-13** — `[project]` metadata block: `name =
  "1c-agent-platform"`, `version = "0.5.1"`,
  `description = "Platform for working with 1C
  configurations through MCP"`, `requires-python =
  ">=3.11"`, `readme = "README.md"`, `authors = [{ name
  = "1C Agent Platform Team" }]`. No `[project.urls]`,
  no `classifiers`, no `keywords`, no
  `[project.dependencies]`, no
  `[project.optional-dependencies]`, no `license`
  field (license file ships separately as `LICENSE`).

- **Lines 15-25** — `[project.scripts]` console-entries
  block:
  ```toml
  [project.scripts]
  mcp-read-server = "mcp_read_server.__main__:main"
  mcp-write-server = "mcp_write_server.__main__:main"
  mcp-intelligence-server = "mcp_intelligence_server.__main__:main"
  ```
  Three console entries declared. Per the inline
  comment block (lines 15-21): "No new runtime
  dependencies are introduced (the stdio transport is
  pure stdlib, see packages/mcp-common/src/mcp_common/_stdio_transport.py).
  The wheel-build block below remains empty, so these
  entries become installable binaries only when a future
  packaging track ships an actual wheel."

- **Lines 27-29** — `[tool.ruff]`: `line-length = 100`,
  `target-version = "py311"`. Lint tooling, not
  packaging.

- **Lines 31-32** — `[tool.pytest.ini_options] testpaths
  = ["tests"]`. Test-discovery setting; `tests/`
  directory does not actually exist in the repo (Track
  K Step 2 audit §3.1 already established this).

- **Lines 34-57** — `[tool.hatch.build.targets.wheel]`
  block with verbatim 24-line honest-constraint comment:
  ```toml
  [tool.hatch.build.targets.wheel]
  # Intentionally empty (Track C / Step 3 honest constraint).
  #
  # The operator install flow for this project runs through
  # `scripts/release/install.ps1` (a thin wrapper over
  # `onec_platform.run_install_fast_path_from_json_file`), NOT through
  # `pip install`. The source layout spreads 11 importable packages
  # across `apps/*/src/` and `packages/*/src/`; PYTHONPATH for local
  # development is bootstrapped by `scripts/dev/bootstrap_paths.ps1`,
  # which the rest of the scripts/ tree dot-sources.
  #
  # Consequences of leaving this empty:
  #   - `python -m build` produces no usable artifact for this project;
  #   - the build toolchain (`build` / `hatch` / `hatchling`) is NOT
  #     part of the documented dev prerequisites;
  #   - no one is expected to install this project via pip today.
  #
  # This is a deliberate honest limitation of the current scaffolding,
  # not an oversight. A future packaging track may revisit it and adopt
  # either a single-wheel layout (one wheel containing all 11 packages)
  # or a multi-wheel split (one wheel per package). Until that track is
  # opened, see `scripts/release/README.md` for the canonical install
  # story.
  packages = []
  ```

This is the central observation. `packages = []` is the
single declarative line that closes the wheel-build
declaration empty. The 24-line comment block above it
explicitly cites "a future packaging track may revisit
it" — that future packaging track is Track M, opened
~10 tracks after Track C / Step 3 left the constraint.

### §3.2 `scripts/release/` directory (4 files + README)

- **`install.ps1`** (Track B / Step 3 + Track I / Step 4)
  — operator-facing config-materialisation wrapper.
  Forwards to `_install_runner.py` which calls
  `onec_platform.run_install_fast_path_from_json_file`.
  Materialises `ProductConfig` JSON; prints follow-up
  `python -m mcp_<server>` commands. **Not** a
  packaging step — it produces no Python distribution,
  no archive, no OS package. Verbatim
  `scripts/release/README.md` line 12-15: "Neither
  introduces a new install ecosystem — no `.msi`, no
  `.deb`, no GUI wizard, no signed distribution — they
  only make existing capabilities operator-discoverable
  and verify release-facing invariants."
- **`_install_runner.py`** — internal helper called by
  `install.ps1`. Not meant to be imported by external
  consumers. Per its module docstring and underscore
  prefix.
- **`verify-release.ps1`** (Track C / Step 2) — 8-check
  release-side gate. Verbatim `scripts/release/README.md`
  line 183-184: "It does **not** validate publication
  to package managers (PyPI / Chocolatey / winget /
  apt). No publication is in scope."
- **`README.md`** (247 lines) — operator-facing
  documentation for the two wrappers, plus a final
  section §"Packaging-facing install flow (honest
  constraint)" (lines 215-246) that says verbatim:
  - line 217: "**The project does not ship a meaningful
    Python wheel today.**"
  - line 220-221: "...materialises a product config
    through the `onec_platform.run_install_fast_path_from_json_file`
    boundary helper, NOT through `pip install <wheel>`."
  - lines 226-231: the three bullets enumerating why
    the empty packages list is honest, not an oversight.
  - line 232-233: "`python -m build` therefore produces
    no usable artifact and attempting it is not a
    supported workflow."
  - lines 244-246: "This is a documented Track C honest
    constraint, not a hidden gap. A future packaging
    track may revisit it. No `.msi`, `.deb`, GUI wizard,
    or signed binary distribution is currently in scope."

The `scripts/release/` surface is operator-helper
oriented; it is **adjacent to** but **not** packaging.

### §3.3 `.gitignore` build-artefact ignore rules

Verbatim from `.gitignore`:

```text
# === Build artifacts ===
dist/
build/
*.egg-info/
```

Even if `python -m build` were run today, the resulting
`dist/` directory + any `.egg-info/` byproduct would be
gitignored. The repo has chosen not to track build
artefacts. This is a normal convention but reinforces
the "repo is the artefact" baseline.

### §3.4 Filesystem state for packaging artefacts

`ls -la dist/`, `ls -la release/`, `ls -la build/`,
`ls *.whl`, `ls *.tar.gz` all return "no such directory
/ file" at HEAD `43bc9ae`. There is **no** in-repo
artefact directory of any kind; **no** loose wheel
file; **no** sdist; **no** operator bundle. The repo
itself is the only delivery surface today.

### §3.5 `docs/release-handoff.md` distribution prose

The handoff document is the closest in-repo document
that discusses "what operators receive". Key verbatim
quotes (after Track L / Step 5 alignment):

- Lines 169-170: "**No wheel-based install.**
  `pyproject.toml` declares
  `[tool.hatch.build.targets.wheel] packages = []`
  deliberately."
- Lines 176-179: "**No GUI installer / `.msi` / `.deb`
  / signed binary distribution.**"; "**No publication
  to package managers** (PyPI / Chocolatey / winget /
  apt)."
- Lines 192-200 (post-Track-L rewrite of the "What is
  NOT in this handoff" line): "in-repo daemon framework
  / pywin32 service wrapper / shipped `.plist` artefact
  / shipped NSSM install script / Windows Service
  registration helper / hot reload / zero-downtime
  restart / clustered HA". This is the post-Track-L
  enumeration; the original Track H/C-era enumeration
  of packaging non-goals carries through.
- Lines 484-486: "**No installer ecosystem.** See
  'What is NOT in this handoff' above."

The handoff document itself is documentation; it does
not ship an artefact. Its "What is in this handoff"
list enumerates scripts and docs that live in the repo.

### §3.6 Track C origin (frozen anchors)

The packaging-honest-constraint trail begins at Track C
/ Step 3 (Track B/C era productization). The Track C
plan and step-map exist as
`docs/architecture/track-c-packaging-installer-delivery-plan.md`
and `docs/architecture/track-c-packaging-installer-delivery-step-map.md`.
Track C chose **not** to ship a wheel; that choice was
intentional and is the constraint Track M now addresses.

### §3.7 `pyproject.toml` declared but currently un-installable `[project.scripts]`

The three console entries declared at
`pyproject.toml:23-25` are operator-aspirational today:
they are documented as a future capability but cannot
actually be installed because the wheel build is empty.
A user running `pip install /path/to/repo` today gets
either an error (depending on `pip` / `build` version
behaviour) or an empty installable wheel that does not
populate the `mcp-read-server` / `mcp-write-server` /
`mcp-intelligence-server` entry points on `PATH`.

This is the **single biggest** observable consequence
of the empty `packages = []`. Operators are documented
to invoke `python -m mcp_<server>` (Track G shape) with
a pre-bootstrapped PYTHONPATH, not the declared console
scripts.

### §3.8 No PyPI / publication metadata

Grep for `[project.urls]`, `classifiers`, `keywords`,
`MANIFEST.in`, `setup.py`, `setup.cfg`, `twine`, `bdist`
across the repo returns either no matches (most) or
only honest-non-goals-list mentions in track docs (e.g.,
"no PyPI publication" denials in Track C / Track H /
Track L documents). There is no PyPI publication
metadata anywhere; no upload workflow; no
`pyproject.toml` `[project.urls]` block.

---

## §4. Existing reusable surfaces

These are repo surfaces Track M can legitimately rely on,
without modifying them:

### §4.1 Honest constraint comment block at `pyproject.toml:34-57`

The 24-line comment block explicitly anticipates a
future packaging track that "may revisit it". Track M
is that track. The comment block names two acceptable
shapes:

- "a single-wheel layout (one wheel containing all 11
  packages)", and
- "a multi-wheel split (one wheel per package)".

Either shape is internally consistent with Step 1
plan §12.Q3 default expectation of "single wheel".
Track M can preserve the comment block (updating its
text to reflect post-Track-M reality) without inventing
a new framing.

### §4.2 Hatchling build backend already declared

`[build-system]` declares hatchling. This is the most
commonly-used modern Python build backend and is
operator-recognisable. Track M does **not** need to
change the build backend; flipping `packages = []` to
a populated list is sufficient to make hatchling
produce a usable wheel.

### §4.3 Three `[project.scripts]` console entries already declared

The three console entries (`mcp-read-server` /
`mcp-write-server` / `mcp-intelligence-server`) are
already declared and will activate automatically once
the wheel build is non-empty. Operators get the
operator-recognisable command surface "for free" the
moment the wheel becomes installable. Track M does
**not** need to add new entries — they exist and just
need to become functional.

### §4.4 Src-layout already established

The 11 src-layout paths (`apps/*/src/<package>/` and
`packages/*/src/<package>/`) are stable across Tracks
G–L. Hatchling's `packages = [<paths>]` directive
accepts a list of relative directories; populating it
with the existing 11 paths is mechanical.

### §4.5 Operator install flow already documented

`scripts/release/install.ps1` materialises a
`ProductConfig` JSON. If Step 4 PATH B ships a
buildable wheel, the materialised config + a wheel are
the two artefacts an operator needs; the install
sequence becomes "pip install wheel + run install.ps1
on the deployment host". Track M does **not** need to
redesign the install flow; it adds a new wheel-side
flow that complements the existing config-side flow.

### §4.6 Release verify already documents what publication is NOT

`scripts/release/verify-release.ps1` Check 7 (credential
leak guard) + Check 8 (credential template hygiene)
together enforce the "no real credentials in repo"
discipline; Track M's recipe and (if PATH B) `pyproject.toml`
flip are both placeholder-safe by construction (the wheel
contains no credentials; the recipe uses abstract
placeholders). The existing verify-release surface does
not need extension.

### §4.7 Track C docs as frozen anchors

`docs/architecture/track-c-packaging-installer-delivery-{plan,step-map}.md`
exist as the origin of the honest constraint. Track M
docs cross-reference them rather than re-litigating
them.

### §4.8 Track L recipe co-location pattern

`docs/operators/service/` was created by Track L /
Step 4 as a sibling to `docs/operators/deployment-
boundary.md`. Track M can use the same pattern:
`docs/operators/packaging/` for any operator-facing
recipe (Step 3 contract decides). Co-location with
Track J / Track L recipes preserves the operator-facing
docs hierarchy.

---

## §5. Adjacent but insufficient surfaces

These surfaces address something related to packaging /
distribution but are not, on their own, sufficient
closure of the Track M gap:

### §5.1 `install.ps1` config materialiser

Insufficient because: materialises a runtime config, not
a Python distribution. The operator must still know how
to run `python -m mcp_<server>` with a bootstrapped
PYTHONPATH. Adjacent but does not answer "what artefact
do I consume".

### §5.2 `verify-release.ps1` release-side gate

Insufficient because: validates that the repo is fit to
ship (8 checks: layout / entrypoints / docs / working
tree / git baseline / selfcheck / credential leak guard
/ credential template hygiene). It does not produce an
artefact; it only checks that the source tree is in a
shippable state. Adjacent.

### §5.3 `docs/release-handoff.md` handoff prose

Insufficient because: explains how to receive a clone of
the repo. Today's "handoff" is "receive a clone and
follow the install fast path". After Track M, the
handoff may also include "or receive a wheel and `pip
install` it" — but the prose alone does not produce the
wheel.

### §5.4 `pyproject.toml` `[project.scripts]` declarations

Insufficient because: declared but currently un-
installable (per §3.7). They become functional only
after Step 4 PATH B flips the wheel-build packages
list.

### §5.5 `pyproject.toml` honest-constraint comment block

Insufficient because: it correctly documents the
**current** constraint but does not close it. Track C
deliberately left it open for a future packaging track;
Track M is that future track.

### §5.6 `.gitignore` build-artefact ignore rules

Insufficient because: they prevent the repo from
accidentally tracking build outputs but do not produce
any artefact. They reflect a "if a build happens, don't
commit the output" stance, which is correct repo
hygiene but says nothing about whether a build can
produce anything useful today (it cannot, per §3.1 +
§3.4).

### §5.7 Track A/B/C/J/K/L recipes and runbooks

Insufficient because: each is operator-facing for its
respective track scope (write-path / productization /
packaging-honest-constraint-only / deployment-boundary
/ smoke-harness / service-supervision). None of them
produces a distribution artefact. Adjacent across
operator-doc hierarchy; insufficient for distribution.

---

## §6. Clearly missing pieces

Each of the following is verifiably absent at HEAD
`43bc9ae`:

1. **Zero buildable wheel artefact.** `python -m build`
   today produces no usable output. Verifiable by:
   `pyproject.toml:57` `packages = []` is empty; `ls
   *.whl` returns no matches; `.gitignore` would ignore
   the output anyway.
2. **Zero source-archive release flow.** No
   `MANIFEST.in`, no `setup.py`, no `setup.cfg`, no
   explicit `sdist` configuration beyond hatchling
   defaults. `ls *.tar.gz` returns no matches.
3. **Zero operator-bundle artefact.** No `dist/`,
   `release/`, `bundle/`, or sibling directory shipping
   a zip/tarball/archive. The repo is the only delivery
   surface.
4. **Zero OS-native package shipped.** No `.msi`,
   `.deb`, `.rpm`, `.dmg`, `.pkg`, `.apk`, `.snap`,
   `.flatpak` anywhere in repo.
5. **Zero PyPI publication metadata.** No
   `[project.urls]`, no `classifiers`, no `keywords`
   in `pyproject.toml`. No upload workflow.
6. **Zero signed-distribution chain.** No signing keys,
   no `cosign` / `sigstore` workflow, no checksums file,
   no SBOM, no SLSA attestation, no Authenticode
   manifest, no notarisation entitlements.
7. **Zero GUI installer / wizard.**
8. **Zero "what artefact do I consume" answer in
   operator-facing docs.** `docs/release-handoff.md`
   describes how to receive a clone; no section
   describes how to receive a packaged drop.
9. **Zero documented upgrade protocol for downstream
   operators.** The operator-facing question "I
   installed `0.5.0` from a clone; how do I upgrade to
   `0.5.1`?" has no answer beyond "re-clone and re-run
   install fast path".
10. **`[project.scripts]` declared but un-installable.**
    The three console entries are documented as future
    capability; today they cannot be installed because
    the wheel build is empty. This is **the** single
    most observable consequence of the Track C / Step 3
    constraint.

---

## §7. Directional Q1–Q6 resolutions

These are **directional**, evidence-grounded
recommendations for Step 3 contract consumption. They
are not normative; they preserve Step 4 PATH openness
where evidence stays mixed.

### §7.1 Q1 — what counts as "packaging/distribution" for this repo?

**Evidence summary.** §3.1 / §3.7 establish that the
declarative surface for packaging already exists
(hatchling backend, `[project.scripts]`); §3.4 / §6
establish that no artefact exists today; §4.1 / §4.2 /
§4.3 / §4.4 establish that closing the gap requires
flipping one line in `pyproject.toml` plus a recipe
explaining what the resulting wheel contains and how
operators consume it.

**Directional resolution.** Track M's "packaging /
distribution" target is at minimum (a) **one
documented distribution-boundary recipe** plus (b)
**one buildable artefact** that operators can consume
via a standard Python tooling command (`pip install
<wheel>`). The recipe explains scope (single wheel
containing the 11 src-layout packages), install verb
(`pip install <wheel>`), and what the wheel does NOT
contain (no Track L service files; no Track J recipes;
no operator credentials).

This matches **plan §12.Q1 option (B)** (documented
distribution boundary + one declarative buildable
artefact). PATH A (docs-only) acceptable as fallback;
PATH C (operator bundle) acceptable only if Step 3
contract rejects PATH B for a specific reason audit
evidence does not currently suggest.

### §7.2 Q2 — what should be the primary artefact class?

**Evidence summary.** §3.1 declares hatchling as the
build backend already, §3.7 declares three console
entries already, §4.4 establishes the src-layout is
stable. A single wheel is the operator-recognisable
Python-tooling-native artefact; an sdist or a manual
operator bundle would be more work for less operator
benefit.

**Directional resolution.** **Single wheel (`.whl`)**
buildable via `python -m build` after the narrow
`packages = []` → `packages = [<11 src paths>]` flip.
The wheel becomes the supported delivery artefact;
operators run `pip install <wheel>` and gain three
`PATH`-installed console scripts plus importable
modules. Sdist (`tar.gz`) acceptable as
recommendation-only complement (hatchling produces it
alongside the wheel by default). Operator-bundle
artefact acceptable only if Step 3 contract has a
specific operator-side reason audit evidence does not
suggest.

This matches **plan §12.Q3 option (A)** (single wheel).

### §7.3 Q3 — likely Step 4 PATH?

**Evidence summary.** §7.1 + §7.2 lead toward PATH B
(docs + narrow `pyproject.toml` flip). §3.1 establishes
that the change is mechanically narrow: a single line
edit + a comment-block update. §6.10 establishes that
the operator-facing payoff is concrete:
`[project.scripts]` console entries become functional.

**Directional resolution.** **PATH B (docs + narrow
`pyproject.toml` `[tool.hatch.build.targets.wheel]
packages = []` → populated list flip)** is the honest
narrowest path. PATH A (docs-only formalization)
acceptable-as-fallback if Step 3 contract decides
flipping the wheel-build is too prescriptive for some
reason audit evidence does not currently suggest.
PATH C (operator bundle artefact) acceptable only if
Step 3 contract decides Python wheels are
inappropriate for the operator context audit evidence
does not suggest (the operator context observed in
`examples/demo-infobase/infobase6.config.json` is
Windows-resident but Python wheels are platform-
neutral; Track L recipe §12.1 NSSM prose shows
operators do run Python wrappers on Windows
unobtrusively).

Evidence does not uniquely lock to one PATH; the audit
**leans toward PATH B** by repo evidence and operator-
delivery payoff. Step 3 contract decides.

### §7.4 Q4 — what is definitely mandatory for closure?

**Evidence summary.** §3.7 / §6.10 establish the
biggest operator-facing improvement is making the
declared console entries actually installable. §3.5
establishes that the handoff document already
enumerates what is NOT in the handoff; making the
wheel buildable requires updating that enumeration.

**Directional resolution.** Mandatory for closure:

- **artefact definition** — exactly which packages
  belong in the wheel, locked in `pyproject.toml`;
- **how operator obtains it** — exactly which build
  command produces it (default: `python -m build`)
  and how it lands on operator's machine (default:
  "operator runs the command on a control host; the
  resulting `.whl` lives under the local `dist/`
  directory; operator copies the file to the
  deployment host");
- **what it contains** — exactly which Python packages
  the wheel ships (default: all 11 src-layout
  packages: `mcp_read_server`, `mcp_write_server`,
  `mcp_intelligence_server`, `mcp_common`,
  `onec_platform`, `onec_process_runner`,
  `onec_policy_engine`, `onec_audit`, `onec_health`,
  `onec_troubleshooting`, `onec_config`);
- **what it does NOT contain** — explicit denial list
  (no operator credentials, no Track L systemd
  template, no Track J recipe, no real `ProductConfig`
  JSON, no `.env` file with real values).

Recommended-only (not closure-blocking):

- documented upgrade protocol;
- documented uninstall protocol;
- documented "build on a clean control host" recipe.

### §7.5 Q5 — what is definitely insufficient as closure proof?

**Evidence summary.** §5.1 through §5.7 enumerate
adjacent-but-insufficient surfaces; §6 enumerates what
is missing.

**Directional resolution.** Definitively insufficient
on its own as Track M closure proof:

- **"Just clone the repo"** — that is the current state
  and the whole reason Track M exists.
- **Release-handoff prose only** — a paragraph in
  `docs/release-handoff.md` saying "to install the
  platform, build your own wheel" without an
  accompanying `pyproject.toml` flip and a recipe.
- **`install.ps1` helper only** — config materialiser,
  not packaging; cannot replace artefact production.
- **Commented TODOs in `pyproject.toml`** — the current
  24-line honest-constraint comment block is honest
  but does not close the gap; Track M must update it,
  not just add another commented intention.
- **Generic packaging aspirations without a committed
  artefact boundary** — abstract prose ("the platform
  is packaging-ready") without a `pyproject.toml`
  change that makes the wheel actually buildable.
- **An `sdist` without a documented build recipe** —
  hatchling can produce a `.tar.gz` source archive,
  but without a recipe explaining what's inside and
  how to install it, the artefact is operator-hostile.
- **Adding new dependencies, new MCP tools, or new
  CLI flags** — these violate the Track M Step 1
  invariants (step-map invariants #14 / #15 / #16 /
  #17) and would expand scope beyond the narrow
  packaging-and-distribution boundary.
- **PyPI publication metadata without actual
  publication** — adding `[project.urls]`,
  classifiers, keywords without shipping the wheel
  anywhere triggers the "PyPI release ready" non-goal
  cascade.
- **Multi-package-manager workflows** — Chocolatey
  / Homebrew / apt / conda-forge / NuGet manifests
  are out of scope per plan §7 and step-map "Track M
  hard out-of-scope".

### §7.6 Q6 — does Track M likely require production code?

**Evidence summary.** §3.1 / §4.4 establish that the
src-layout is stable and that the change to make the
wheel buildable is purely declarative
(`pyproject.toml`). No `__init__.py` change, no
`__main__.py` change, no new module, no new package.
The existing console-entry declarations
(`mcp_<role>_server.__main__:main`) point at modules
that already exist with their entry-point function.

**Directional resolution.** **NO production code
change.** The packaging surface is fully declarative.
Hatchling reads `pyproject.toml` `[tool.hatch.build.targets.wheel]
packages = [<list>]` and produces a wheel containing
the listed directories. No Python-side code change is
required to make the existing `[project.scripts]`
entries functional once the wheel is non-empty.

This matches **plan §12.Q6 default** (narrow
`pyproject.toml` flip; no production code change).

---

## §8. Step 3 handoff note

These items the audit hands off to Step 3 contract for
normative locking. They are **not** decided here; Step 3
locks them.

1. **Track M "packaging / distribution" target
   definition.** Audit-directional = documented
   distribution-boundary recipe + one buildable
   artefact (single wheel). Step 3 to lock the exact
   text.

2. **Primary artefact class.** Audit-directional =
   single wheel (`.whl`) buildable via `python -m build`.
   sdist as recommendation-only complement. Step 3 to
   lock.

3. **Step 4 PATH selection.** Audit-directional =
   PATH B (docs + narrow `pyproject.toml` wheel-build
   flip). Step 3 may pin PATH A or PATH C if it has a
   defensible reason from audit evidence; default =
   PATH B.

4. **Wheel contents.** Audit-directional = all 11 src-
   layout packages
   (`apps/*/src/<package>` × 4: `mcp_read_server`,
   `mcp_write_server`, `mcp_intelligence_server`,
   `onec_platform`; `packages/*/src/<package>` × 7:
   `mcp_common`, `onec_process_runner`,
   `onec_policy_engine`, `onec_audit`, `onec_health`,
   `onec_troubleshooting`, `onec_config`). Step 3 to
   lock the exact `packages = [...]` list with paths.

5. **Wheel non-contents (explicit denial list).**
   Audit-directional = no operator credentials; no
   Track L systemd template; no Track J recipe; no
   real `ProductConfig` JSON; no `.env` file with real
   values; no `examples/` data; no `docs/` content.
   Step 3 to lock.

6. **Step 4 file surface cap.** Audit-directional =
   ≤ 3 touched files for PATH B (one operator recipe
   under `docs/operators/packaging/` or similar +
   `pyproject.toml` flip + at most one accompanying
   file). Step 3 to lock final cap.

7. **Step 4 file locations.** Audit-directional =
   `docs/operators/packaging/` for the recipe (co-
   located with Track J `docs/operators/deployment-
   boundary.md` and Track L
   `docs/operators/service/service-supervision.md`);
   `pyproject.toml` flip in-place. Step 3 to lock.

8. **`pyproject.toml` change scope.** Audit-directional
   = exactly one narrow change: flip `packages = []`
   to populated list + update the 24-line comment
   block to reflect post-Track-M reality. No
   `[project.urls]`, no `classifiers`, no `keywords`,
   no `MANIFEST.in`, no new dependencies. Step 3 to
   lock.

9. **Lifecycle verbs documented in the recipe.**
   Audit-directional = build (`python -m build`),
   install (`pip install <wheel>`), uninstall (`pip
   uninstall 1c-agent-platform`), upgrade (`pip
   install --upgrade <wheel>`), verify (existing
   `verify-release.ps1` checks). Step 3 to lock which
   are closure-blocking vs recommendation-only.

10. **Production code modification.** Audit-directional
    = none. Step 3 to lock this as a forbidden
    surface for Step 4 (matching plan §8.6 / step-map
    invariant #1).

11. **Placeholder discipline.** Audit-directional =
    abstract placeholders only in recipe examples
    (`<WHEEL_PATH>`, `<CONTROL_HOST>`,
    `<DEPLOYMENT_HOST>`, `<VENV_PATH>`); no real
    values. The wheel itself ships zero credentials by
    construction (the build does not include any
    `ProductConfig` JSON or `.env` file). Step 3 to
    lock final list.

12. **Forbidden file surfaces for Step 4.** Audit-
    directional: production code (`apps/*/src/`,
    `packages/*/src/`); `pyproject.toml` `version`
    field (Step 6 territory); `pyproject.toml`
    `[project]` metadata fields other than the
    intentional `packages = []` flip;
    `[project.scripts]` block (entries locked); new
    `[project.urls]` / classifiers / keywords;
    `MANIFEST.in` (no addition); `scripts/release/*`
    existing files (unless Step 3 contract authorises
    one new sibling); `SECURITY.md`;
    `docs/release-handoff.md` (Step 5 territory);
    `docs/operators/deployment-boundary.md`,
    `docs/operators/service/*` (Track J / Track L
    artefacts); `apps/platform/README.md`; manuals;
    `examples/`; all Track A–L architecture docs;
    Track M Step 1–3 docs; README; PROJECT-STATUS;
    CHANGELOG. Step 3 to lock final list.

13. **Verification protocol for Step 4.** Audit-
    directional: scope checks (file-count cap,
    forbidden-surfaces byte-identical except for the
    intentional `pyproject.toml` flip); selfcheck
    (registries `15/25/16`, status=ok); release-
    verify (`verify-release.ps1 -AllowDirtyTree` GREEN
    on 8 checks); build-check (`python -m build`
    produces a non-empty wheel under `dist/` —
    recommended-only since `build` is not in
    documented dev prerequisites per `pyproject.toml`
    line 47); honesty (no 1cv8.exe, no real
    credentials in repo or in wheel, no premature
    closure language, no false implementation claims,
    no fake "packaging solved" framing); recipe-
    consistency (lifecycle verbs covered, denial list
    present, cross-references resolve). Step 3 to
    lock the exact check count.

14. **Honest non-goals carry-forward.** Audit-
    directional: full list verbatim from plan §7 plus
    §6 / §7.5 specifics. Step 3 to lock.

15. **Q7 framing for Step 6.** Audit-directional =
    **PATCH** as the most likely outcome if Step 4
    PATH B (closing the long-standing Track C / Step 3
    honest constraint about the empty wheel build is
    legitimate defect-class repair framing — Track C
    explicitly left the 24-line comment block citing
    this moment); **NO-BUMP** acceptable if Step 4
    PATH A; MINOR / MAJOR forbidden by track scope.
    Step 6 locks.

16. **Carry-forward invariants from Tracks G/H/I/J/K/L.**
    Audit-directional: identical to plan §11 table —
    Track G stdio runtime byte-identical; Track H HTTP
    runtime byte-identical; Track I installer round-
    trip byte-identical; Track J §13 / §6 / §7 / §8
    carry-forward unchanged; Track K diagnostic
    harness byte-identical; Track L service-
    supervision recipe + systemd template byte-
    identical. `apps/platform/src/onec_platform/runtime.py`
    byte-identical (Track L invariant carries through).
    Registries `15 / 25 / 16`. Step 3 to lock.

---

## §9. Honest summary

**The gap is real.** §6's ten enumerated absences are
each independently verifiable in the repo at HEAD
`43bc9ae`. No buildable wheel; no source-archive flow;
no operator-bundle artefact; no OS-native package; no
PyPI metadata; no signed-distribution chain; no GUI
installer; no "what artefact do you consume" answer in
operator docs; no upgrade protocol; declared
`[project.scripts]` entries un-installable. Existing
surfaces (`install.ps1` config materialiser,
`verify-release.ps1` release gate, release-handoff
prose) are adjacent but insufficient on their own and
were never designed to close this gap; they were
designed around it (per the Track C / Step 3 honest
constraint).

**The fix is narrow.** §7.6 establishes that no
production code change is required. §4.1 / §4.2 / §4.3
/ §4.4 establish that the declarative surface for a
buildable wheel already exists in `pyproject.toml` —
the only missing piece is the `packages = []` →
`packages = [<11 paths>]` flip plus an operator-facing
recipe explaining what the wheel contains and how to
install it.

**The risk of scope-creep is real.** §3.8 / §5 / §6
enumerate the broader packaging ecosystem (`.msi` /
`.deb` / `.rpm` / GUI installer / wizard / signed
distribution / multi-package-manager publication) that
Track M MUST keep out of scope. Track M's discipline is
exactly the same as Track J's (deployment-boundary
recipe-only) and Track L's (service-supervision recipe
+ one declarative template): close one narrow operator-
facing gap, deny everything broader as honest non-goal.

**The audit does not commit Step 3.** Step 3 locks the
final PATH (A / B / C), the final wheel-contents list,
the final file surfaces, the final LOC cap, the
verification protocol, and the Q7 framing for Step 6.
This audit recommends directionally; it does not decide
normatively. Step 4 PATH openness is preserved exactly
because audit evidence narrows directionally without
uniquely locking, though the lean toward PATH B is
strong from evidence.

**No "packaging solved forever" claim.** Track M's
closure target is one buildable wheel (or one operator
artefact, per Step 3 contract) plus one recipe plus an
honest denial of "PyPI release ready" / "signed binary
distribution" / "all package managers supported" /
"production-ready packaging" / "enterprise-ready
packaging" claims. The same honest-non-goals discipline
that closed Tracks J / K / L applies here.

**Active state at the end of Step 2.** Track M / Step 2
closed (this audit). Track M still **active**. Next
step = Track M / Step 3 (normative contract). Step 3
not opened in this commit.
