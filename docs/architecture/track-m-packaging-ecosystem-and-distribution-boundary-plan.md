# Parallel Track M — Packaging Ecosystem and Distribution Boundary — Plan

**Track status at the time of this document.** Parallel Track M
opened as the thirteenth post-phase parallel track after Track L
closure (commit `e21e185`). Step 1 — planning only;
documentation-only. No production code change. No
`pyproject.toml` change. No `scripts/*` change. No registry
change. No `1cv8.exe` runs.

**Track M positioning relative to Tracks A–L.** Tracks A–L
closed sequentially as twelve post-phase parallel tracks (A
real-write-path, B productization, C packaging, D credentials
hardening, E version-matrix scaffolding, F rollback expansion,
G stdio transport + CLI, H HTTP transport + bearer auth, I
installer auth round-trip integrity, J TLS and reverse-proxy
deployment boundary, K real MCP client integration test, L
service supervision and OS service registration). After Track
L closure the platform has:

- a stdio MCP transport (Track G);
- a narrow HTTP `/mcp` endpoint with static bearer auth
  (Track H);
- `ProductConfig.auth.tokens` with `${ENV:NAME}` env-
  substitution and `--auth-token-env` CLI override
  (Tracks D + H);
- an install fast-path with auth round-trip integrity
  (Track I);
- an operator-facing deployment-boundary recipe at
  `docs/operators/deployment-boundary.md` (Track J);
- a real MCP client smoke harness at
  `scripts/dev/mcp_client_smoke.py` (Track K);
- an operator-facing service-supervision recipe at
  `docs/operators/service/service-supervision.md` plus a
  declarative systemd unit-file template at
  `docs/operators/service/mcp-server.service` (Track L).

What it still does **not** have is a first-class
"how-this-product-is-shipped" story.

---

## §1. Purpose — why this track exists

Track M exists to convert the current honest gap

> "the platform **runs**, can be **supervised**, and can be
> **operated**, but it is not yet **packaged** or
> **distributed** like a product"

into a disciplined six-step closure track using the same
shape as Tracks A–L (planning → audit → contract → narrow
implementation → docs alignment → final integration pass).

Every prior post-phase track left "packaging ecosystem"
(`.msi` / `.deb` / signed distribution / wheel publication /
PyPI / GUI installer / wizard) in its honest-non-goals list.
The Track C / Step 3 honest constraint left
`[tool.hatch.build.targets.wheel] packages = []` intentionally
empty. Track M is the dedicated narrow track that finally
answers the operator-facing question

> "What artefact am I supposed to consume to use this
> platform, and where is the supported boundary between
> the source repository and a shipped product?"

The track is **not** justified by a defect — there is no
broken behaviour. It is justified by an **operator-
delivery-ergonomics gap**: today the supported delivery is
"clone the repo, bootstrap PYTHONPATH, run `python -m
mcp_<server>`". That is acceptable for developers and for
the reference-stand operator, but does not answer "how do I
ship this to a third party who will operate it without
cloning the repo themselves".

---

## §2. Current post-Track-L baseline

The relevant baseline for Track M (as of `e21e185`):

### §2.1 Build / packaging surfaces that exist today

- **`pyproject.toml`** — declares `[project]` (name, version
  `0.5.1`, description, `requires-python = ">=3.11"`,
  authors, readme); declares three `[project.scripts]`
  console entries (`mcp-read-server`, `mcp-write-server`,
  `mcp-intelligence-server` → `mcp_<role>_server.__main__:main`);
  declares `[tool.ruff]` (line-length 100, target Py 3.11);
  declares `[tool.pytest.ini_options] testpaths = ["tests"]`;
  declares `[tool.hatch.build.targets.wheel] packages = []`
  — **intentionally empty** per Track C / Step 3 honest
  constraint, with a 24-line comment block explaining the
  consequences (`python -m build` produces no usable
  artefact; build toolchain not part of documented dev
  prerequisites; no one is expected to install via pip
  today).
- **`scripts/release/install.ps1`** — operator install
  fast-path (Track B / Step 3, extended by Track I / Step 4
  for `auth.tokens` round-trip integrity). Materialises a
  `ProductConfig` JSON; prints follow-up `python -m
  mcp_<server>` invocation strings. Explicitly **not** a
  packaging step.
- **`scripts/release/verify-release.ps1`** — 8-check
  release-side gate (Track C / Step 2).
- **`scripts/release/README.md`** — verbatim line 12-15:
  "Neither introduces a new install ecosystem — no `.msi`,
  no `.deb`, no GUI wizard, no signed distribution — they
  only make existing capabilities operator-discoverable and
  verify release-facing invariants."

### §2.2 What is **not** in the repo today

- No buildable wheel artefact. `python -m build` (with the
  current `packages = []` setting) produces an effectively
  empty wheel; no operator-consumable Python distribution.
- No source-archive release flow (no `MANIFEST.in`, no
  `sdist` configuration beyond hatchling defaults, no
  release-artefact directory).
- No operator-facing bundle artefact (no `dist/`, no
  `release/`, no tarball, no zip).
- No OS-native package shipped (no `.msi`, `.deb`, `.rpm`,
  `.dmg`, `.pkg`, `.apk`, `.snap`, `.flatpak`).
- No PyPI publication metadata (no `[project.urls]`, no
  `keywords`, no classifiers).
- No signed-distribution chain (no signing keys, no
  `cosign`/`sigstore` workflow, no checksums file).
- No GUI installer / wizard.
- No "what artefact do I consume" answer in operator-facing
  documentation. `docs/release-handoff.md` describes how to
  receive a clone, not how to receive a packaged drop.
- No documented version-update protocol for downstream
  consumers (the version bumps in `CHANGELOG.md` exist, but
  there is no "how do I upgrade an installed instance"
  flow).

### §2.3 What Track M therefore must close

A first-class "packaging / distribution story": guidance
and at most one declarative artefact or build configuration
slice that defines what operators consume as the supported
delivery boundary, **without** silently expanding into the
broader packaging ecosystem (`.msi` / `.deb` / PyPI
publication / GUI installer / signed distribution / cross-
distro matrix).

The track must close that gap **honestly**: it does not
promise "packaging solved forever", does not promise "PyPI
release ready", does not promise "signed binary
distribution", does not promise "all package managers
supported". It promises **one** documented distribution
boundary plus (optionally, depending on Step 3 contract
PATH selection) at most one declarative build artefact or
wrapper, preserving every Track G / H / I / J / K / L
invariant byte-identical.

---

## §3. Honest gap statement

Four observations, each independently verifiable in the
repo at `e21e185`:

1. **No buildable wheel.** `[tool.hatch.build.targets.wheel]
   packages = []` is verbatim in `pyproject.toml:57`,
   accompanied by a 24-line comment block (lines 34-57)
   describing the consequence: "`python -m build` produces
   no usable artifact for this project". A first-time
   operator running `pip install .` will get either an
   error or an empty wheel that installs nothing functional.
2. **No distribution-artefact directory.** Whole-repo glob
   for `dist/`, `release/`, `build/`, `.whl`, `.tar.gz`,
   `.zip` (excluding `.gitignore` matches and committed
   test data) returns no operator-shipped artefacts. The
   repo is the shipped artefact.
3. **No "what artefact do you consume" answer.**
   `docs/release-handoff.md` titled "Release Handoff" is
   prose for receiving a clone, not for receiving a
   packaged drop. The "What is in this handoff" list
   enumerates scripts and docs (which live in the repo),
   not a separately-distributable artefact. The "What is
   NOT in this handoff" list explicitly says "no wheel-
   based install", "no GUI installer / `.msi` / `.deb` /
   signed binary distribution", "no publication to package
   managers".
4. **No upgrade protocol.** The platform has no documented
   way for a downstream operator to upgrade an installed
   instance — there is no "installed instance" concept in
   repo terminology. `CHANGELOG.md` records version bumps,
   but the operator-facing question "I installed `0.5.0`
   from a clone; how do I move to `0.5.1`?" has no answer
   beyond "re-clone and re-run install fast path".

The gap is real. It is not papered over by
`scripts/release/install.ps1` (materialises config; does
not register an artefact) nor by `pyproject.toml`'s console
scripts (declared, but un-installable today because the
wheel build is empty).

---

## §4. Why this gap is real and not already solved

Each of the following candidate "we already have this"
arguments is rejected from repo evidence:

- **"Cloning the repo IS the distribution."** True
  operationally for developers; insufficient for an
  operator who must accept the repo blindly. Cloning a
  repo with 100+ files and untracked toolchain assumptions
  is fundamentally different from installing a single
  declared artefact. Every prior productization-class track
  (Track B / Track C) explicitly left "no packaging
  ecosystem" in its honest non-goals. This track is the
  dedicated answer; cloning is acceptable until it isn't.
- **"`install.ps1` is enough."** It materialises a config.
  It does not install a Python package, does not register
  a service (Track L's separate concern), does not produce
  a downloadable artefact. Different layer.
- **"`[project.scripts]` is enough."** They are
  **declared** in `pyproject.toml:22-25` but currently
  **un-installable** because the wheel build is empty
  (`pyproject.toml:57`). Until the wheel build is non-
  empty (or until a separate artefact ships the
  entrypoints), the console scripts are aspirational, not
  operator-consumable.
- **"Operators write their own wheel."** True but evades
  the gap. The same logic would have rejected Track J's
  recipe ("operators can write their own nginx config") or
  Track L's recipe ("operators can write their own
  systemd unit"). Track M's purpose is to define **one**
  supported distribution boundary in-repo so operators do
  not need to invent it.
- **"Track C already covered this."** Track C / Step 3
  explicitly chose to keep wheel-build empty as an
  **honest constraint**, deferring the decision to a
  future packaging track. Track M is that future track.
  Track C did not close packaging; Track C explicitly
  left it open with a comment block citing this exact
  future moment.

---

## §5. Goal of the track

By Step 6 closure, Track M must have delivered:

1. A single normative packaging / distribution contract
   (Step 3) that pins the closure-gate scope, the
   distribution-artefact class (or explicit "no artefact —
   distribution boundary documented only"), the file
   surface for Step 4, and the verification protocol.
2. Either a single operator-facing distribution-boundary
   recipe **or** a single declarative build-configuration
   change **or** a single artefact slice **or** a hybrid —
   depending on Step 3 Q3 lock. Step 4 is the only step
   that may add code/config beyond docs.
3. Honest closure narrative in README / PROJECT-STATUS /
   CHANGELOG that documents what distribution boundary
   Track M settled, what it explicitly did NOT solve, and
   what remains operator-supplied.
4. Preserved byte-identical runtime and existing artefacts:
   Track G stdio path, Track H HTTP path, Track I
   installer round-trip, Track J reverse-proxy posture,
   Track K diagnostic harness, Track L service-supervision
   recipe + systemd template — all unchanged.

---

## §6. What is in scope

- Planning, audit, contract, narrow implementation, docs-
  alignment, and closure for packaging ecosystem +
  distribution boundary of the existing platform.
- Defining what counts as a "supported distribution
  artefact" concretely for this repo.
- Defining whether Step 4 targets:
  - **PATH A** — distribution-boundary docs only (no
    artefact change; recipe formalises today's "repo IS
    the artefact" reality with explicit non-goals);
  - **PATH B** — narrow declarative build-configuration
    change (e.g., flip `[tool.hatch.build.targets.wheel]
    packages = []` to a populated list so one
    wheel becomes buildable, paired with a recipe);
  - **PATH C** — operator-bundle artefact (zip / tarball /
    archive layout under a new path, paired with a recipe
    explaining the bundle shape).
- Defining whether packaging stays cross-OS neutral or
  names one primary distribution channel.
- Defining how packaging relates to current service /
  auth / deployment / installer truths (cross-references
  only; no redesign).
- Preserving compatibility with all Tracks G / H / I /
  J / K / L invariants.

## §7. What is out of scope

The following are intentionally **not** Track M scope.
Each is denied explicitly to prevent silent expansion:

- **No new MCP tools.** Registry invariant `read = 15 /
  write = 25 / intelligence = 16` must carry through all
  six Track M steps.
- **No registry changes** of any kind.
- **No transport redesign.** Track G stdio + Track H HTTP
  preserved byte-identical.
- **No auth redesign.** Track H static bearer + Track I
  round-trip integrity + Track D `${ENV:NAME}` substitution
  preserved byte-identical.
- **No deployment-boundary redesign.** Track J reverse-
  proxy / TLS-termination model preserved byte-identical.
- **No service-supervision redesign.** Track L recipe +
  systemd template preserved byte-identical.
- **No multiple-package-manager publication.** No PyPI
  publication, no Chocolatey, no Homebrew, no apt
  repository, no rpm repository, no conda-forge — even
  if Step 4 ships a single wheel.
- **No `.msi` / `.deb` / `.rpm` / `.dmg` / `.pkg` /
  `.apk` / `.snap` / `.flatpak`** — OS-native package
  formats remain operator-side.
- **No signed distribution chain.** No signing keys, no
  `cosign` / `sigstore` workflow, no SBOM, no notarisation.
- **No GUI installer / wizard.**
- **No enterprise identity stack.** No SSO / SAML / OIDC /
  SCIM / RBAC / ABAC / multi-tenant identity bound to
  the packaging story.
- **No clustering / HA / orchestration platforms.**
- **No web UI / dashboard frontend.**
- **No full observability stack** bound to the packaging
  story.
- **No standalone `apps/platform` daemon entrypoint.**
- **No automatic-update / OTA / self-upgrade mechanism.**
- **No rollback expansion / AST work / 1С matrix
  expansion.**
- **No `1cv8.exe` runs.**
- **No remote push.** GitHub push remains operator
  decision.
- **No "packaging solved forever" / "PyPI release
  ready" / "signed binary distribution" / "all package
  managers supported" / "production-ready packaging" /
  "enterprise-ready packaging" claim.** Such phrases may
  appear in Track M docs only as explicit denials.

---

## §8. Guardrails

Each guardrail is verifiable on the post-Step-1 commit and
must remain verifiable through Step 6:

1. **Tracks A–L invariants byte-identical.** `apps/*/src/`,
   `packages/*/src/`, `_stdio_transport.py`,
   `_network_transport.py`, `installer.py`,
   `runtime.py`, `process_control.py`, `runtime_logs.py`,
   `models.py`, `scripts/dev/mcp_client_smoke.py`,
   `docs/operators/deployment-boundary.md`,
   `docs/operators/service/service-supervision.md`,
   `docs/operators/service/mcp-server.service` not touched
   by Steps 1 / 2 / 3 / 5 / 6. Step 4 may modify
   `pyproject.toml` only if Step 3 contract explicitly
   authorises PATH B (declarative build-configuration
   change); the default expectation remains that
   `pyproject.toml` is touched at most by one narrow
   `packages = [...]` flip plus an accompanying comment
   update.
2. **Registries invariant.** `selfcheck.py` registries
   `read=15 / write=25 / intelligence=16` must remain
   confirmed green at every step.
3. **No new MCP tools** at any step.
4. **No new CLI flag on existing servers.** No new
   `--bind`, `--auth-token-env`, or sibling flag added by
   Track M; the existing flag surface is locked.
5. **No new entrypoint module.** No new `__main__.py` in
   any `apps/*/src/` package.
6. **No new dependencies.** Step 4 must not add to
   `[project.dependencies]` or
   `[project.optional-dependencies]`. The existing
   stdlib-only orientation of `mcp_common` and the three
   servers is preserved.
7. **No `1cv8.exe` runs** at any step.
8. **No remote push** at any step.
9. **No real credentials** in any committed file. All
   examples must use abstract placeholders.
10. **No premature closure language.** Steps 1–5 may not
    describe Track M as "закрыт" / "closed".
11. **No false implementation claims.** Step 1 plan must
    present Q1–Q7 as **defaults** and **recommendations**,
    not as decided answers.
12. **No "packaging solved forever" / "PyPI release
    ready" / "signed binary distribution" / "all package
    managers supported" / "production-ready packaging" /
    "enterprise-ready packaging" framing** except as
    explicit denials.
13. **Step 4 file-surface cap.** Step 3 contract MUST pin
    a maximum number of touched files (default
    expectation: ≤ 3 — at most one recipe doc + at most
    one declarative artefact-or-config change + at most
    one accompanying file under the chosen artefact-
    location path). Step 3 may tighten.
14. **Step 4 LOC cap for any code-bearing artefact.**
    Default expectation: ≤ 200 LOC stdlib-only, no new
    dependencies. Step 3 may tighten.

---

## §9. Acceptance criteria for eventual closure

By Step 6 commit:

1. Track M has shipped **at most one new architecture
   plan-doc, one new step-map doc, one new baseline-audit
   doc, one new normative contract doc, and (Step 4) at
   most three new files or surgical modifications**
   under Step 3 contract caps.
2. Production code (`apps/*/src/`, `packages/*/src/`)
   byte-identical to the Track L closure state
   (`e21e185`).
3. `pyproject.toml` `version` either unchanged
   (`0.5.1`, Q7 = NO-BUMP) or bumped per Q7 rule. Other
   `pyproject.toml` fields (specifically
   `[tool.hatch.build.targets.wheel] packages`) may
   change only if Step 3 contract authorises PATH B
   explicitly.
4. Registries `read=15 / write=25 / intelligence=16`
   carried through unchanged.
5. README / PROJECT-STATUS / CHANGELOG closure narrative
   present and honest: explicit denial of "packaging
   solved forever", "PyPI release ready", "signed
   binary distribution", "all package managers
   supported", "production-ready packaging",
   "enterprise-ready packaging" claims; explicit
   statement of which artefact class Track M settled on;
   explicit Q7 reasoning.
6. `verify-release.ps1` GREEN on 8 checks at every step.
7. `selfcheck.py` `status=ok` at every step.
8. No real credentials anywhere in committed text.
9. No `1cv8.exe` runs anywhere in the track.
10. No remote push performed automatically by any step.
11. Track M moved into README's "Closed parallel tracks"
    list, growing it from twelve to thirteen closed
    tracks (A / B / C / D / E / F / G / H / I / J / K /
    L / M).

---

## §10. Honest constraints after closure

These constraints remain after Track M closure:

- **No "production-ready packaging for hostile-internet
  distribution" claim.** Track J trusted-internal-network
  posture preserved; Track M packaging story does not
  bind to internet-facing publication.
- **No automatic update / OTA / self-upgrade.** Operator-
  driven upgrade only.
- **No multi-channel publication.** Whatever single
  artefact Track M settles on, it ships through a single
  documented channel (typically: the repo / release-side
  directory). No PyPI / Chocolatey / apt / homebrew /
  conda-forge / NuGet publication.
- **No OS-native package formats.** No `.msi` / `.deb` /
  `.rpm` / `.dmg` / `.pkg` / `.apk` / `.snap` /
  `.flatpak`.
- **No GUI installer / wizard / setup.exe.**
- **No signed distribution.** No `cosign` / `sigstore` /
  Authenticode / Notarisation / SBOM / SLSA attestation.
- **No web UI for distribution management.**
- **No multi-version 1С matrix expansion** bound to
  packaging.
- **No rollback / AST work** bound to packaging.
- **No new MCP tools / registry change.**
- **No `1cv8.exe` runs.**

---

## §11. Relationship to Tracks G / H / I / J / K / L

| Aspect | Track G | Track H | Track I | Track J | Track K | Track L | Track M (this) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Surface | stdio transport + CLI | HTTP `/mcp` + bearer auth | installer auth round-trip | TLS / reverse-proxy boundary | real MCP client smoke proof | service supervision / OS service registration | packaging ecosystem / distribution boundary |
| Code touched? | YES (3 `__main__.py` + 245-LOC `_stdio_transport.py` + `[project.scripts]`) | YES (549-LOC `_network_transport.py` + auth wiring) | YES (+15 LOC in `installer.py`) | NO (docs-only) | NO (one new diagnostic file under `scripts/dev/`) | NO (two new files under `docs/operators/service/`) | **TBD by Step 3 contract** (default expectation: ≤ 3 files; possibly one narrow `pyproject.toml` flip + one operator recipe + at most one artefact) |
| New transport? | YES | YES | NO | NO | NO | NO | NO |
| New endpoint? | NO | YES | NO | NO | NO | NO | NO |
| New CLI flag? | YES | YES | NO | NO | NO | NO | NO (Q4 invariant) |
| Registry change? | NO | NO | NO | NO | NO | NO | NO |
| SemVer outcome | MINOR (0.3.0 → 0.4.0) | MINOR (0.4.0 → 0.5.0) | PATCH (0.5.0 → 0.5.1) | NO-BUMP | NO-BUMP | NO-BUMP | **TBD** (default = NO-BUMP if PATH A; PATCH considered if Step 4 = PATH B/C with honest operator-visible improvement; see §12.Q7) |

Track M inherits all preceding tracks' invariants and adds
none that conflict with them.

---

## §12. Open questions Q1–Q7 with default recommendations

These are **defaults and directional recommendations**, not
decided answers. Step 2 audit may move them; Step 3
contract locks them.

### Q1 — what exactly counts as "packaging/distribution" for closure?

**Options.**
- **(A)** Documented distribution-boundary recipe only —
  formalise today's "repo IS the artefact" reality with
  explicit non-goals, no buildable artefact change.
- **(B)** Documented distribution boundary **plus** one
  declarative buildable artefact — e.g., a wheel buildable
  via `python -m build` plus an operator recipe describing
  what the wheel contains.
- **(C)** Documented distribution boundary **plus** one
  operator-bundle artefact (zip / tarball / archive layout)
  plus an operator recipe.

**Default recommendation.** **(B)** as closure gate **if**
Step 2 audit confirms that the existing
`[project.scripts]` declarations can be made operator-
consumable via a single narrow `[tool.hatch.build.targets.wheel]
packages = [...]` flip without expanding scope into PyPI
publication or multi-package-manager workflows. **(A)**
acceptable as fallback if Step 2 audit reveals that even a
narrow wheel slice triggers ecosystem expansion. **(C)**
acceptable only if Step 2 audit reveals a strong reason to
avoid wheel building entirely.

### Q2 — does the track cover build artefact only, or installation/distribution story too?

**Options.**
- **(A)** Build artefact only — Step 4 produces a
  buildable artefact, operator-facing distribution story
  remains today's "operator clones the repo".
- **(B)** Build artefact + installation story — Step 4
  produces a buildable artefact **plus** a documented
  operator install procedure ("download the wheel from
  release directory; pip install").
- **(C)** Distribution story only — Step 4 documents
  what the supported distribution boundary is without
  shipping a buildable artefact (PATH A from Q1).

**Default recommendation.** **(B) installation story
included** as the operator-facing closure target. A
buildable artefact without an install recipe is operator-
hostile (operators do not know which artefact to consume).
Step 4 recipe MUST cover the install verb (e.g., "operator
downloads release artefact, runs `pip install <wheel>`")
even if the broader publication channel remains
operator-side.

### Q3 — what artefact class does Step 4 produce?

**Options.**
- **(A)** Single wheel (`.whl`) — buildable via
  `python -m build` after a narrow `pyproject.toml` flip.
  Contains the three MCP server modules + `mcp_common` +
  optionally the `apps/platform` boundary helpers.
- **(B)** Single source archive (`sdist`) — buildable via
  `python -m build --sdist`. Lower install ergonomics than
  wheel but no Python-side install logic needed at all.
- **(C)** Single operator bundle (zip / tarball) — manual
  layout under `release/` or similar; pure file-system
  artefact, no Python packaging.
- **(D)** No artefact — PATH A from Q1.

**Default recommendation.** **(A) single wheel** as the
narrowest honest closure path **if** Q1 = (B). The wheel
exists as a declared concept in `pyproject.toml` since
Track C / Step 3; making it actually buildable is the
narrowest step. **(B)** acceptable as alternative if Step 2
audit reveals wheel-build complications that make the
sdist path simpler. **(C)** acceptable if Step 2 audit
reveals operator-side preference for filesystem bundles
over Python packages. **(D)** acceptable as fallback per
Q1 (A).

### Q4 — cross-OS neutral or one primary distribution OS?

**Options.**
- **(A)** Cross-OS neutral — wheel works wherever Python
  3.11+ is installed; recipe makes no OS-specific claims.
- **(B)** Windows first — recipe walks Windows install
  end-to-end, cross-OS prose only for Linux/macOS.
- **(C)** Linux first — symmetric to Track L closure
  target.

**Default recommendation.** **(A) cross-OS neutral.**
Python wheels are platform-neutral by default for pure
Python code (this codebase is stdlib-only beyond
hatchling's build-side dependency); the recipe MAY mention
Windows-specific tooling notes (e.g., `scripts/release/
install.ps1` is Windows-side) but the **artefact itself**
remains cross-OS. Windows-first or Linux-first acceptable
only if Step 2 audit reveals platform-specific obstacles.

### Q5 — do service files / templates belong inside the packaging story?

**Options.**
- **(A)** No — Track L service-supervision recipe +
  systemd template remain under `docs/operators/service/`
  and stay outside the Track M artefact.
- **(B)** Yes — the wheel (or bundle) ships the Track L
  systemd template as a `data_files` entry.
- **(C)** Documented cross-reference only — the Track M
  recipe points operators at the Track L recipe but does
  not ship the template inside the artefact.

**Default recommendation.** **(C) documented cross-
reference only.** The Track L systemd template is an
operator-facing template that operators copy + substitute
+ install via `systemctl`; bundling it inside the wheel
adds packaging complexity (`data_files` placement, etc.)
for marginal operator benefit. **(A)** acceptable as
alternative if Step 3 contract decides cross-reference is
sufficient on its own. **(B)** explicitly rejected by
guardrail §8 #5 (no new entrypoint module) and by §8 #13
(file-surface cap) — bundling templates expands the
artefact scope.

### Q6 — does Track M need `pyproject.toml` changes at all?

**Options.**
- **(A)** No — if Q1 = (A) (docs-only distribution
  boundary), `pyproject.toml` remains byte-identical.
- **(B)** YES, narrow — flip `[tool.hatch.build.targets.wheel]
  packages = []` to a populated list with the
  src-layout paths, update the accompanying 24-line
  honest-constraint comment block.
- **(C)** YES, broader — beyond (B), additionally add
  `[project.urls]`, classifiers, keywords, `MANIFEST.in`,
  etc. for PyPI-ready metadata.

**Default recommendation.** **(B) narrow flip only.** This
is the narrowest honest change that makes the wheel
buildable. (A) acceptable as fallback per Q1 (A). (C)
explicitly rejected — PyPI-ready metadata triggers the
"PyPI publication" non-goal cascade and would force
ecosystem expansion.

### Q7 — what SemVer bump does Track M justify?

**Options.**
- **(A)** NO-BUMP. Track M closes under existing `0.5.1`
  if Step 4 = PATH A (docs-only) and no `pyproject.toml`
  changes happen. Mirrors Track J / Track K / Track L
  closure precedent.
- **(B)** PATCH `0.5.1 → 0.5.2`. Track M closes with a
  PATCH bump if Step 4 = PATH B (declarative
  `pyproject.toml` flip) AND the resulting wheel build is
  honestly framed as a defect-class repair of the long-
  standing "empty wheel build" honest constraint. Track C
  / Step 3 specifically left a comment block citing a
  future packaging track; making the wheel buildable
  closes that long-standing constraint.
- **(C)** MINOR `0.5.1 → 0.6.0`. Track M closes with a
  MINOR bump only if Step 4 ships net-new external
  capability for ordinary product consumers — e.g., a
  newly-installable `mcp-read-server` console script that
  operators can `pip install` and run, where previously
  they could not. This is plausible if Q1 / Q3 land on
  PATH B (wheel becomes buildable AND installable).
  However, MINOR risks claiming more maturity than the
  narrow Track M scope warrants.
- **(D)** MAJOR. Explicitly rejected by track scope.

**Default recommendation.** **(A) NO-BUMP** if Step 4
PATH A. **(B) PATCH** as the most likely outcome if Step 4
PATH B (the long-standing empty-wheel-build constraint is
a legitimate defect-class issue that has been openly
documented since Track C / Step 3; closing it is honest
PATCH territory). MINOR considered only if Step 4
introduces net-new operator-facing surface beyond making
existing declarations functional; default expectation
rejects MINOR per the "no new CLI flag" Q4 invariant.

---

## §13. Step trajectory preview

| Step | Kind | Default file surface | Default scope cap |
| --- | --- | --- | --- |
| Step 1 (this) | planning | 2 new docs + README + PROJECT-STATUS | docs-only |
| Step 2 | descriptive baseline audit | 1 new doc under `docs/architecture/track-m-*-baseline-audit.md` | docs-only |
| Step 3 | normative contract | 1 new doc under `docs/architecture/track-m-*-contract.md` | docs-only |
| Step 4 | narrow implementation (PATH A / B / C) | ≤ 3 new files or surgical modifications (default expectation: one operator recipe under `docs/operators/` or `docs/operators/packaging/` + at most one narrow `pyproject.toml` flip + at most one accompanying file) | locked by Step 3 contract |
| Step 5 | docs / operator / release alignment | narrow CLASS-1 only: README, possibly `docs/release-handoff.md`, possibly `apps/platform/README.md`, possibly `scripts/release/README.md`; NO production code | scope locked by Step 3 contract |
| Step 6 | final integration pass and track closure | README + PROJECT-STATUS + CHANGELOG; optionally `pyproject.toml` if Q7 = PATCH or MINOR | NO production code; Q7 decision explicit |

---

## §14. Honest summary

**What Track M will do.** Convert the "no first-class
packaging / distribution story" gap into one operator-
facing distribution-boundary recipe (and, if Step 3
contract pins PATH B, one narrow `pyproject.toml` flip
that makes the existing wheel-build declaration
functional), preserving every Tracks A–L invariant byte-
identical.

**What Track M will not do.** It will not introduce a
broader packaging ecosystem (.msi / .deb / .rpm / .dmg /
.pkg / GUI installer / wizard / signed distribution /
PyPI publication / multi-package-manager workflow), will
not promise hostile-internet distribution, will not bind
upgrades to an automatic mechanism, will not add new MCP
tools, will not change registries, will not run
`1cv8.exe`, will not push to GitHub automatically.

**Why this is the next right narrow track.** Every prior
post-phase track left "packaging ecosystem" in its
honest-non-goals list, and Track C / Step 3 left an
explicit comment block in `pyproject.toml` citing this
exact future moment. Track M closes that long-standing
constraint the same way Track L closed "service
supervision": one document and at most one narrow
declarative slice, with explicit denial of the broader
claims a less disciplined version of the same track
would make.

**Default Q7 outcome.** **NO-BUMP** if Step 4 PATH A
(docs-only); **PATCH** if Step 4 PATH B (narrow wheel-
build flip closing the Track C honest constraint).
Q7 lock is Step 6 territory.
