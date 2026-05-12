# Dev-Time Editable Install and Workspace Discovery — Contributor Recipe

> **What this is.** A single contributor-facing recipe
> for installing 1C Agent Platform from a checkout for
> editing, classifying which dev-time workflows are
> first-class supported vs recommended-only vs
> out-of-scope, and pointing at the existing
> verification gate.
>
> **What this is not.** A broader developer-experience
> platform. Not a containerised dev environment. Not an
> IDE integration. Not a remote-dev workflow. Not a
> multi-Python-version matrix. Not a formatter / linter
> / test-runner policy. Not an alternative build-
> backend. Not an installable-from-git-URL story. See
> §7 for the complete non-goals list.

---

## §1. Purpose / scope

### §1.1 What this recipe covers

This document tells a contributor who has cloned the
repository and wants to edit it in place:

- Which install verb is **first-class supported** (§2).
- Which alternative is **recommended-only** (§2).
- Which tools the contributor MUST have available
  before installing (§3).
- How workspace discovery works — which packages a
  Python interpreter sees after install (§4).
- How to verify the install worked (§5).
- How this dev-time workflow relates to the deploy-
  time wheel workflow Track M ships (§6).
- What is explicitly out-of-scope (§7).
- Where to read deeper (§8).

### §1.2 What this recipe does not cover

This recipe is **not** any of:

- A guarantee that any specific package manager beyond
  `pip` is supported. The recipe pins `pip install -e
  .` as the first-class verb; alternatives like `uv pip
  install -e .`, `pdm install`, or `hatch env create`
  may coincidentally work but are **not** supported by
  this recipe.
- A guarantee that any specific IDE workflow works.
  The recipe documents the install + workspace-
  discovery boundary; what an IDE does on top of that
  is the contributor's responsibility.
- A guarantee of cross-OS implementation-covered parity
  (see §2.3).
- A commitment to ship containerised dev, remote-dev,
  IDE bundles, or any forbidden category enumerated in
  §7.

### §1.3 Forbidden maturity claims — explicit denials

This recipe does **not** claim, and MUST NOT be cited
as evidence of, any of the following:

- ❌ **"Developer workflow solved forever."** The
  recipe closes one narrow integration-and-naming gap;
  future tooling realities may surface additional
  needs that fall outside this recipe's scope.
- ❌ **"All IDE integrations supported."** The recipe
  documents install + workspace discovery only. IDE
  behaviour after that is operator/contributor choice.
- ❌ **"All package managers supported for dev
  install."** Only `pip install -e .` is first-class.
  Other managers (`uv`, `pdm`, `hatch`, `poetry`,
  `conda`) are not supported by this recipe.
- ❌ **"Containerised dev environment shipped."** No
  Dockerfile, no `docker-compose.yml`, no
  `.devcontainer/` configuration ships in the repo.
- ❌ **"Remote-dev shipped."** No Codespaces, no
  GitPod, no Coder template, no remote-dev hook.
- ❌ **"Enterprise developer experience."** Recipe
  scope is contributor-scale, not enterprise-platform
  scale.
- ❌ **"Production-ready DX."** This is a working
  baseline, not a production-ready DX surface.
- ❌ **"DX matrix complete."** Many DX questions
  (multi-Python matrix, lint enforcement, test-suite
  shipping, IDE pre-configuration) are deliberately
  outside this recipe.

---

## §2. Supported install verbs

### §2.1 First-class supported — `pip install -e .`

The **first-class supported** dev-time install verb is:

```bash
pip install -e .
```

Run from the **repo root** in a Python 3.11
environment (typically a virtual environment — see
§3). On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

On POSIX shells (Linux / macOS bash / zsh):

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .
```

#### What `pip install -e .` provides

After a successful editable install:

- All **eleven** src-layout packages enumerated in
  [`pyproject.toml`](../../pyproject.toml)
  `[tool.hatch.build.targets.wheel] packages` (the
  list at lines 51-63) become importable directly,
  without any further `PYTHONPATH` manipulation.
- The three console scripts declared at
  `pyproject.toml:22-25` are installed as
  contributor-runnable binaries:
  - `mcp-read-server`
  - `mcp-write-server`
  - `mcp-intelligence-server`
- In-place source edits are reflected **immediately**:
  modifying a file under `apps/` or `packages/` takes
  effect on the next Python process invocation; no
  rebuild step is required for code changes.
- **Zero** third-party runtime dependencies are
  installed into the virtual environment. The
  project's `[project.dependencies]` is empty by
  construction; the runtime is stdlib-only.

#### Why this works mechanically

The build backend is `hatchling` (declared at
`pyproject.toml:1-3`). Hatchling supports PEP 660
editable installs by default when
`[tool.hatch.build.targets.wheel] packages` is
populated. Track M / Step 4 populated it with the
eleven-element src-layout array. `pip install -e .`
therefore mechanically produces a working editable
install with no special configuration in this repo.

### §2.2 Recommended-only alternative — `bootstrap_paths.ps1` (Windows)

A **recommended-only** alternative exists for
contributors on Windows who prefer not to use editable
install:

```powershell
. .\scripts\dev\bootstrap_paths.ps1
```

(Note the leading `.` — this is PowerShell dot-source
syntax. It sets `$env:PYTHONPATH` for the current
PowerShell session only.)

After dot-sourcing, the eleven src-layout paths are
on PYTHONPATH and the same packages become importable.

#### When you might prefer this alternative

- You want to avoid touching `site-packages` (e.g.,
  shared system Python).
- You already have a preferred virtual-environment
  workflow that you do not want to combine with `pip
  install -e .`.
- You only need a one-off REPL session to inspect
  the codebase (the `launch.ps1 repl` umbrella wraps
  this for you — see §8).

#### Why this is recommended-only, not first-class

- **PowerShell-only.** The script uses Windows path
  separators (`\`); dot-sourcing it from `bash`/`zsh`
  on POSIX hosts does not produce a working
  PYTHONPATH even if `pwsh` is installed.
- **Session-scoped.** The PYTHONPATH lives only in
  the current PowerShell session — every new shell
  must re-bootstrap. Editable install survives shell
  restarts.
- **No console scripts.** Dot-sourcing the bootstrap
  does **not** install the three `[project.scripts]`
  console entries; contributors must invoke
  `python -m mcp_read_server` etc. directly.

### §2.3 Cross-OS posture

| Host | First-class? | Notes |
| --- | --- | --- |
| Windows + PowerShell + Python 3.11 | YES | Both `pip install -e .` (first-class) and `bootstrap_paths.ps1` (recommended-only) work. |
| POSIX (Linux / macOS) + bash/zsh + Python 3.11 | YES (via `pip install -e .` only) | `bootstrap_paths.ps1` is **not** supported on POSIX even with `pwsh` installed. Use editable install. |
| Other shells / non-3.11 Python | OUT OF SCOPE | `.python-version` pins Python 3.11. Older or newer Python versions, exotic shells, and embedded interpreters are not Track O-supported. |

Track O does not claim implementation-covered parity
across all OS / shell / Python combinations. The
first-class verb (`pip install -e .`) works wherever
Python 3.11 and a PEP 660-supporting `pip` are
available; everything beyond that is contributor
discretion.

---

## §3. Supported tooling preconditions

Before running the first-class verb, contributors
MUST have:

| Tool | Required? | Notes |
| --- | --- | --- |
| **Python 3.11** | YES | Pinned in [`.python-version`](../../.python-version) and declared as `requires-python = ">=3.11"` at `pyproject.toml:9`. Tools that honour `.python-version` (`pyenv`, `mise`, etc.) will pick it up automatically. |
| **`pip`** (≥ 21.3 for PEP 660) | YES | Ships with every supported Python distribution. Upgrade if needed: `python -m pip install --upgrade pip`. |
| Virtual-environment tool | RECOMMENDED | Built-in `venv` is sufficient (`python -m venv .venv`). Any compatible alternative works (`virtualenv`, the venv layer of `uv` / `pdm` / `hatch` / `poetry`). The recipe does not mandate one. |
| `build` (PEP 517 frontend) | NO (only for Track M wheel) | Required only if the contributor wants to construct a wheel via `python -m build`. That is **Track M's** workflow, not Track O's. See §6. |
| Formatter / linter / test-runner | NO | `[tool.ruff]` and `[tool.pytest.ini_options]` are declared in `pyproject.toml` but neither is installed by this recipe and neither is enforced. Contributors who want `ruff` or `pytest` must install them themselves; this recipe takes no position. |
| IDE | NO | No IDE configuration ships. Contributors choose freely; no bundled `.vscode/`, `.idea/`, or equivalent. |

Track O does not ship a `[project.optional-
dependencies] dev = [...]` block. Editable install
introduces **zero** third-party dependencies into
your virtual environment; what you install on top is
your decision.

---

## §4. Workspace discovery answer

### §4.1 The eleven src-layout package roots

The workspace consists of exactly **eleven** src-layout
package roots, enumerated as the single source of
truth in [`pyproject.toml:51-63`](../../pyproject.toml):

```toml
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

### §4.2 Dual-role explanation

The same eleven paths serve **two** roles in this
project:

1. **Track M deploy-time wheel-build packages array.**
   Read by hatchling when building the wheel via
   `python -m build`. Resulting wheel exposes
   exactly these eleven modules to operators
   installing via `pip install <WHEEL_PATH>`.
2. **Dev-time PYTHONPATH entries.** Mirrored in
   [`scripts/dev/bootstrap_paths.ps1:9-21`](../../scripts/dev/bootstrap_paths.ps1)
   (the `scripts/dev/bootstrap_paths.ps1` recommended-
   only alternative from §2.2).

The two lists are byte-equivalent (modulo path
separator). After `pip install -e .`, hatchling's
PEP 660 default exposes exactly the same eleven
package roots on `sys.path` — making
`bootstrap_paths.ps1` and editable install
functionally interchangeable for import resolution.

### §4.3 Acceptable duplication

This recipe acknowledges that the eleven paths are
currently maintained in **two** files
(`pyproject.toml` + `scripts/dev/bootstrap_paths.ps1`)
that must be kept synchronised by hand. Resolving
this duplication into a single source is **out of
Track O scope** and a candidate for a future track
if drift between the two ever becomes a maintenance
problem in practice.

---

## §5. Verification step

After install (either verb), verify the workspace is
correctly discovered by running the project's
existing pre-flight gate:

### §5.1 On Windows PowerShell

```powershell
.\scripts\dev\launch.ps1 selfcheck
```

This wraps [`scripts/dev/run_dev_check.ps1`](../../scripts/dev/run_dev_check.ps1),
which in turn dot-sources `bootstrap_paths.ps1`
and runs `python scripts/dev/selfcheck.py`. (If you
already installed via `pip install -e .`, the
`PYTHONPATH` bootstrap is harmless but unnecessary;
the umbrella works in either case.)

### §5.2 On POSIX (or directly via Python)

```bash
python scripts/dev/selfcheck.py
```

(After `pip install -e .` from the repo root in your
active virtual environment.)

### §5.3 Canonical PASS signal

Both invocation paths produce the same selfcheck
output. The canonical **PASS** signal is the final
line on stdout:

```
selfcheck_status = ok
```

Plus an exit code of `0`. The full output is
documented under Track N FC4 (the first-class
diagnostic signal classification in the
observability recipe at
[`docs/operators/observability.md`](../operators/observability.md));
this recipe does not re-document it.

### §5.4 What a successful selfcheck proves (and does not prove)

Successful selfcheck proves:

- All eleven src-layout packages are importable.
- The MCP tool registries report
  `read=15 / write=25 / intelligence=16` (the
  invariant carried through every closed track).
- The basic library smoke (`ping` / `list_tools` /
  health + troubleshooting library calls) works.

Successful selfcheck does **not** prove:

- That an MCP server binds and serves correctly on
  a transport (the Track K
  [`scripts/dev/mcp_client_smoke.py`](../../scripts/dev/mcp_client_smoke.py)
  harness covers that — recommended-only per Track
  N R1).
- That any 1С infobase is reachable.
- That your editor / IDE picks up the editable
  install (IDE behaviour is out of scope).

---

## §6. Relationship to Track M — orthogonal and complementary

Track O (dev-time editable install) and **Track M**
(deploy-time wheel distribution) are **orthogonal-
and-complementary** axes. They serve different
audiences, different lifecycle moments, and use
different install verbs.

| Aspect | Track M (deploy-time) | Track O (dev-time, this recipe) |
| --- | --- | --- |
| Audience | Operator receiving a wheel artefact | Contributor / internal developer editing the repo |
| Lifecycle moment | Deploy-time (build then install) | Dev-time (clone then edit then iterate) |
| Primary input | A built `.whl` file | A cloned checkout |
| Primary install verb | `pip install <WHEEL_PATH>` | `pip install -e .` (run from repo root) |
| Source edits | Require rebuild + re-install | Reflected immediately |
| Authoritative recipe | [`docs/operators/packaging/distribution-boundary.md`](../operators/packaging/distribution-boundary.md) | this file |

### §6.1 When to use which

- You are an **operator** receiving a build of the
  platform for production use → use Track M's
  wheel install via `pip install <WHEEL_PATH>`;
  see [`distribution-boundary.md`](../operators/packaging/distribution-boundary.md).
- You are a **contributor** editing the repo in
  place → use this recipe's `pip install -e .`.
- You are a contributor on Windows who prefers a
  non-install workflow → dot-source
  [`bootstrap_paths.ps1`](../../scripts/dev/bootstrap_paths.ps1)
  (recommended-only).

### §6.2 Cross-track shared anchors

The two recipes share their workspace-discovery
foundation byte-identically — the eleven src-layout
paths in `pyproject.toml:51-63` (§4.1). This is
intentional: a contributor's editable install
exposes the same packages the deploy-time wheel
ships. Selfcheck (§5) works identically in both
contexts.

### §6.3 No content duplication

This recipe does **not** duplicate Track M's
content. It cross-references the deployment
recipe rather than restating any wheel-build or
install-fast-path detail. If you need the
operator-side install flow, read
[`distribution-boundary.md`](../operators/packaging/distribution-boundary.md)
directly.

---

## §7. Authoritative non-goals

This recipe does **not** provide, ship, or promise
to ship any of the following. These categories are
intentional limits of the current dev-time boundary,
inherited from Track O Step 1 plan §7 and Track O
Step 3 contract §1.4 / §12.

### §7.1 Containerised dev / IDE / remote-dev

- No `Dockerfile`, `docker-compose.yml`, or
  `.devcontainer/` configuration ships.
- No IDE-specific bundle (`.vscode/`, `.idea/`,
  Cursor / Zed / Sublime / Vim project files).
- No Codespaces, GitPod, or Coder template.

Contributors who use any of these tools wire them up
themselves; the project takes no position.

### §7.2 Multi-Python-version / build-backend

- No `tox.ini` or `nox.py`. No multi-Python-version
  CI matrix.
- No change to [`.python-version`](../../.python-version)
  (Python 3.11 preserved as the only supported
  contributor Python).
- No alternative build-backend evaluation —
  hatchling remains.

### §7.3 Tooling policy

- No enforced formatter / linter / test-runner. The
  `[tool.ruff]` and `[tool.pytest.ini_options]`
  blocks in `pyproject.toml` are configuration
  present but not installed or executed by any
  Track O artefact.
- No test suite ships. `tests/` directory does not
  exist at this writing.

### §7.4 Installable-from-git-URL story

- No documented `pip install git+https://...` flow.
- No `pip install ./zipfile.zip` flow.
- The supported install paths are exactly two:
  Track M `pip install <WHEEL_PATH>` (for
  operators) and Track O `pip install -e .` (for
  contributors, this recipe).

### §7.5 Cross-track scope

- No new MCP tools, no new CLI flag on any MCP
  server, no new `[project.scripts]` entry, no new
  project dependency, no new entrypoint module.
- No new env-var convention.
- No `/healthz` / `/readyz` / `/livez` endpoint
  (Track J §6 defer preserved).
- No change to runtime / transport / auth /
  deployment / service-supervision / packaging /
  observability behaviour.

### §7.6 Forbidden maturity claims (recap)

This recipe MUST NOT be cited as evidence of any of
the following — see §1.3 for the explicit denials:

- "Developer workflow solved forever."
- "All IDE integrations supported."
- "All package managers supported for dev install."
- "Containerised dev environment shipped."
- "Remote-dev shipped."
- "Enterprise developer experience."
- "Production-ready DX."
- "DX matrix complete."

### §7.7 Other carry-over non-goals

- No `1cv8.exe` integration changes.
- No rollback / AST / multi-version 1С matrix
  expansion.

---

## §8. Cross-references

The following files are the authoritative anchors
for this recipe. Cross-reference each as needed.

- [`docs/operators/packaging/distribution-boundary.md`](../operators/packaging/distribution-boundary.md)
  — **Track M.** The deploy-time wheel
  distribution recipe. Orthogonal axis to this
  recipe (§6).
- [`pyproject.toml`](../../pyproject.toml)
  — The single source of truth for the eleven
  src-layout package roots (`[tool.hatch.build.
  targets.wheel] packages` at lines 51-63; §4).
  Also declares `requires-python = ">=3.11"`,
  the three `[project.scripts]` console entries,
  hatchling build-backend, and the empty
  `[project.dependencies]`.
- [`scripts/dev/bootstrap_paths.ps1`](../../scripts/dev/bootstrap_paths.ps1)
  — The PowerShell-only PYTHONPATH bootstrap;
  recommended-only alternative install path for
  Windows contributors (§2.2). Mirrors the
  eleven-element `pyproject.toml` packages
  array (§4.2).
- [`scripts/dev/launch.ps1`](../../scripts/dev/launch.ps1)
  — The Windows dev-umbrella. Subcommand
  `selfcheck` wraps the verification step in
  §5.1. Other subcommands (`repl`, `run`,
  `help`) are unrelated to install.
- [`scripts/dev/selfcheck.py`](../../scripts/dev/selfcheck.py)
  — The verification gate (§5). Track N FC4
  classification: first-class supported diagnostic
  signal. 11-line key=value output; canonical
  PASS line is `selfcheck_status = ok`.
- [`scripts/dev/README.md`](../../scripts/dev/README.md)
  — Describes the `scripts/dev/*` directory
  contents. Until Track O Step 5 alignment lands,
  the file's intro (lines 5-11) and status
  section (lines 192-198) still contain a
  historical hand-off marker ("editable install
  и workspace discovery всё ещё out of scope")
  that this recipe makes obsolete. Step 5 will
  narrowly replace those two sentences with a
  pointer to this recipe.

---

## §9. Honest summary

This recipe gives a contributor a single document
to read when installing the platform from a
checkout for editing, plus a single document to
cite when classifying which dev-time workflows the
platform supports and which it does not. The
integration scope is narrow on purpose:

- **What you can rely on:** `pip install -e .` as
  the first-class install verb, working on
  Windows / Linux / macOS in a Python 3.11
  environment; the verification gate via
  `selfcheck.py`.
- **What you can use carefully:**
  `bootstrap_paths.ps1` dot-source on Windows as
  the recommended-only alternative.
- **What is not shipped:** the entire forbidden
  surface enumerated in §1.3 + §7 — no
  containerised dev, no IDE integrations, no
  remote-dev, no multi-Python-version matrix, no
  formatter/linter/test-runner policy, no
  alternative build-backend, no installable-from-
  git-URL story, no new MCP tools / CLI flags /
  dependencies, no test suite, no `/healthz`.
- **The cross-OS posture is honest:** Windows is
  primary-with-both-paths; POSIX is served by
  `pip install -e .` only; non-3.11 Python is
  out of scope.
- **The relationship to Track M is explicit:**
  dev-time and deploy-time are orthogonal-and-
  complementary axes with different verbs, audiences,
  and lifecycle moments.
- **No maturity is claimed beyond what is shipped.**
  Every forbidden maturity claim from §1.3 / §7.6
  appears in this recipe **only as an explicit
  denial**.

This is the entire Track O dev-time editable
install / workspace discovery boundary. Future
tracks may extend it; this recipe does not promise
they will.
