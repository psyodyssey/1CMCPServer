# Operator-Facing Packaging / Distribution-Boundary Recipe

> **Audience.** Operators who need to build, install,
> uninstall, upgrade, or verify the 1C Agent Platform as a
> single Python wheel, on a control host and a deployment
> host they own.
>
> **What this document is.** A practical operator recipe
> for the narrow, honestly supported distribution boundary
> of the 1C Agent Platform (project version `0.5.1` as of
> this document). The normative source-of-truth for every
> claim below is the Track M Step 3 contract
> (`docs/architecture/track-m-packaging-ecosystem-and-distribution-boundary-contract.md`).
> This document operationalizes that contract for the five
> lifecycle verbs: **build**, **install**, **uninstall**,
> **upgrade**, **verify**.
>
> **What this document is NOT.** It is not a claim that
> "packaging solved forever". It is not a claim that the
> platform is "PyPI release ready". It is not a "signed
> binary distribution" recipe. It is not an "all package
> managers supported" matrix. It is not a "production-ready
> packaging" or "enterprise-ready packaging" statement. It
> is not a "GUI installer" or "wizard". It is not a multi-OS
> package manifest. Those shapes are explicitly out of
> scope — see §13 (Honest non-goals) for the full denial
> list.

---

## 1. Purpose / scope

You are reading this because you have built or received
the 1C Agent Platform source tree and you need to turn it
into something an operator on a deployment host can
install with `pip` and uninstall with `pip` — without
inventing your own packaging story for each handoff.

This document answers, in order:

- what artefact class the platform supports as its
  distribution boundary;
- exactly which Python packages are inside that artefact;
- exactly which artefacts are NOT inside it;
- how to build it on a control host;
- how to install it on a deployment host;
- how to uninstall, upgrade, and verify it;
- how the artefact relates to the existing
  install-fast-path (`scripts/release/install.ps1`) and to
  the Track J / Track L operator recipes;
- what packaging shapes are explicitly NOT supported.

### 1.1 What this document is for

- One place to look when an operator asks "how do I
  install the 1C Agent Platform as a wheel?".
- One place to look when an operator asks "what's
  actually inside that wheel?".
- One place to look when an operator asks "what isn't
  inside it, and where do those things live instead?".
- The operator-facing companion to the Track M Step 3
  contract's normative artefact-class declaration.

### 1.2 What this document is NOT for

This document is **not**:

- a claim that "packaging solved forever";
- a claim that the platform is "PyPI release ready";
- a "signed binary distribution" guide;
- a "all package managers supported" matrix;
- a "production-ready packaging" attestation;
- a "enterprise-ready packaging" attestation;
- a "hostile-internet distribution ready" guide;
- an "automatic update / OTA" mechanism;
- a "GUI installer" or "wizard" recipe;
- a "the platform now publishes to PyPI" announcement;
- a "Chocolatey / Homebrew / apt / conda-forge / NuGet
  support" matrix.

Each of those phrases is **denied** by the supported
distribution boundary documented here. See §13 (Honest
non-goals).

---

## 2. Supported distribution boundary

### 2.1 — Artefact class

The supported distribution boundary is **one
pure-Python wheel**: a single `.whl` file with the
platform tag `py3-none-any`, produced from the
repository's `pyproject.toml` via the standard PEP 517
build flow.

The wheel filename pattern is:

```
1c_agent_platform-<VERSION>-py3-none-any.whl
```

For project version `0.5.1`, the operator-visible
filename is `1c_agent_platform-0.5.1-py3-none-any.whl`.
The wheel is **pure Python** (no compiled extensions),
which is why the platform tag is `py3-none-any` and the
same wheel installs on any host with Python 3.11+
regardless of OS.

### 2.2 — Why a single wheel

The repository uses an src-layout with eleven Python
packages spread across `apps/*/src/` and `packages/*/src/`
(enumerated in §3). A multi-wheel split (one wheel per
package) would require eleven `pyproject.toml` files or
eleven separate build invocations, and would make
operator delivery more complex for marginal benefit.

The Track M Step 3 contract therefore locks the
**single-wheel layout**: one wheel containing all eleven
src-layout packages, named under the project name
`1c-agent-platform`. The multi-wheel split is explicitly
rejected by the contract and MUST NOT be inferred from
this recipe.

### 2.3 — What this closes

Until the Track M contract closed (commit `00a8e1f`,
Track M / Step 3), the `[tool.hatch.build.targets.wheel]`
block in `pyproject.toml` carried an `packages = []`
declaration accompanied by a 24-line honest-constraint
comment block (Track C / Step 3) explaining that the
wheel build intentionally produced no usable artefact
and that operators were expected to use
`scripts/release/install.ps1` instead. Track M Step 4
flips that empty list to the eleven src-layout package
paths and replaces the comment block with a pointer to
this recipe. The wheel build is now functional; the
install-fast-path remains complementary (see §11).

---

## 3. Wheel contents — exact eleven packages

The wheel contains exactly these eleven src-layout
Python packages. The list mirrors the
`[tool.hatch.build.targets.wheel]` `packages` array in
`pyproject.toml`:

| # | Source path | Importable name |
|---|---|---|
| 1 | `apps/mcp-read-server/src/mcp_read_server` | `mcp_read_server` |
| 2 | `apps/mcp-write-server/src/mcp_write_server` | `mcp_write_server` |
| 3 | `apps/mcp-intelligence-server/src/mcp_intelligence_server` | `mcp_intelligence_server` |
| 4 | `apps/platform/src/onec_platform` | `onec_platform` |
| 5 | `packages/mcp-common/src/mcp_common` | `mcp_common` |
| 6 | `packages/onec-process-runner/src/onec_process_runner` | `onec_process_runner` |
| 7 | `packages/onec-policy-engine/src/onec_policy_engine` | `onec_policy_engine` |
| 8 | `packages/onec-audit/src/onec_audit` | `onec_audit` |
| 9 | `packages/onec-health/src/onec_health` | `onec_health` |
| 10 | `packages/onec-troubleshooting/src/onec_troubleshooting` | `onec_troubleshooting` |
| 11 | `packages/onec-config/src/onec_config` | `onec_config` |

After `pip install`, all eleven names are importable
under their unprefixed Python module names (e.g.
`import mcp_read_server`, `from onec_platform import
runtime`).

The relevant `pyproject.toml` lines an operator sees:

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

The wheel ALSO contains the three console-script
entrypoints declared in `[project.scripts]`, which `pip`
materializes onto `PATH` at install time:

- `mcp-read-server` → `mcp_read_server.__main__:main`
- `mcp-write-server` → `mcp_write_server.__main__:main`
- `mcp-intelligence-server` → `mcp_intelligence_server.__main__:main`

These three entries are locked by the Track G / Step 4
contract and the Track M Step 3 contract; this recipe
does not introduce or remove any console script.

---

## 4. Wheel non-contents — explicit denial list

The wheel **does NOT** contain any of the following.
Hatchling's default behaviour already excludes most of
them; this section enumerates them for operator clarity
so there is no surprise:

- **No operator credentials of any form.** No tokens,
  no passwords, no API keys, no infobase usernames. The
  wheel is constructed to ship zero credential material.
- **No `.env` file with real values.** Any operator
  `.env` lives on the operator's deployment host and is
  loaded at runtime by the platform via the
  `${ENV:NAME}` substitution mechanism (Track D /
  Step 3); the wheel never embeds one.
- **No real `ProductConfig` JSON.** For example,
  `examples/demo-infobase/infobase6.config.json` is
  excluded. ProductConfig JSON files are operator-side
  artefacts that the install-fast-path materializes;
  they are not part of the platform code.
- **No Track L systemd unit template** (the file
  `docs/operators/service/mcp-server.service`). That
  file is operator-facing service-supervision content
  and lives under `docs/operators/service/`, not inside
  the wheel.
- **No Track J deployment-boundary recipe content.**
  The file `docs/operators/deployment-boundary.md` is
  operator-facing prose; it stays in the repository,
  not in the wheel.
- **No `docs/` content.** All operator-facing prose
  (this recipe included) stays in the repository.
- **No `examples/` data.** The demo-infobase and
  demo-dumps trees are operator-side reference
  material; they are not shipped inside the wheel.
- **No `scripts/` content.** PowerShell wrappers
  (`scripts/release/install.ps1`,
  `scripts/dev/launch.ps1`, etc.) are operator-side
  tooling; they remain in the repository and are
  invoked from a checkout, not from an installed wheel.
- **No `.git/` data.** Hatchling never includes
  `.git/` in the wheel.
- **No CI configuration.** `.github/`, build pipelines,
  or workflow definitions are not inside the wheel.
- **No `runbooks/` content.** Runbooks under
  `docs/runbooks/` are operator-facing prose and stay
  in the repository.

The wheel is **only** the eleven Python packages listed
in §3, plus the three console-script entrypoints declared
in `[project.scripts]`. Everything else is excluded by
construction.

---

## 5. Build verb

### 5.1 — Operator command

The supported build command is the standard PEP 517
build front-end:

```
python -m build
```

Run this from the project root on a **control host**
(the host where you have a clone of the repository and
an internet-capable Python environment).

### 5.2 — Operator-side prerequisite

The build front-end is **not** part of
`[project.dependencies]` or any other declared
dependency surface. It is an **operator-side
prerequisite**, installed on the control host before the
first build:

```
pip install build
```

(Some operators prefer `pip install build hatchling` to
have hatchling resolvable up-front; this is optional —
`python -m build` will pull in the backend declared by
`[build-system] requires`.)

The platform itself ships **no new dependencies** under
Track M; the only operator-visible build prerequisite is
the `build` front-end.

### 5.3 — Expected operator-visible result

After `python -m build` completes successfully, the
operator sees a new `dist/` directory at the project
root containing two files:

```
dist/1c_agent_platform-<VERSION>-py3-none-any.whl
dist/1c_agent_platform-<VERSION>.tar.gz
```

The `.whl` is the closure-target wheel — this is the
artefact the operator delivers to the deployment host.
The `.tar.gz` source archive (`sdist`) is a **recommendation-only**
complementary artefact produced by hatchling's default
build flow; it is acceptable to keep, ignore, or delete
on the control host. The closure target is the wheel.

### 5.4 — `.gitignore` policy reminder

The repository's `.gitignore` excludes `dist/` and
`build/`. The wheel and the sdist are build outputs an
operator produces on demand on the control host; they
are **not** committed back into the repository, and this
recipe does not instruct operators to publish them
anywhere.

### 5.5 — Build failure surface

If `python -m build` fails, common operator-visible
causes are:

- the control host's Python is `<3.11`
  (`[project] requires-python = ">=3.11"`);
- the `build` front-end was not `pip install`-ed;
- the operator ran `python -m build` from outside the
  project root (no `pyproject.toml` visible);
- a transient network failure prevented hatchling from
  being fetched into the isolated build environment.

The recipe does not attempt to enumerate every possible
build error; the standard `python -m build` error
output points at the specific cause.

---

## 6. Install verb

### 6.1 — Operator command

On the **deployment host** (which may be the same as the
control host or a separate machine), the supported
install command is:

```
pip install <WHEEL_PATH>
```

where `<WHEEL_PATH>` is the path to the wheel file
delivered out-of-band from the control host (e.g.
`/home/<DEPLOYMENT_HOST>/wheels/1c_agent_platform-<VERSION>-py3-none-any.whl`
or `C:\wheels\1c_agent_platform-<VERSION>-py3-none-any.whl`).

### 6.2 — Environment assumption

The deployment host MUST have Python 3.11 or later. The
wheel is `py3-none-any`, so the same wheel installs
identically on Linux, macOS, and Windows; the only
binding requirement is Python 3.11+.

Operators are strongly encouraged to install into a
dedicated virtual environment rather than the system
Python. A representative pattern (operator-side, not
mandated by the platform):

```
python -m venv <VENV_PATH>
<VENV_PATH>/bin/pip install <WHEEL_PATH>      # POSIX
<VENV_PATH>\Scripts\pip.exe install <WHEEL_PATH>   # Windows
```

The platform makes no assumption about where the venv
lives; that decision is operator-owned.

### 6.3 — Expected operator-visible result

After `pip install` succeeds, the operator sees:

- three console scripts on `PATH` (or under
  `<VENV_PATH>/bin/` / `<VENV_PATH>\Scripts\` if
  installed into a venv):
  - `mcp-read-server`
  - `mcp-write-server`
  - `mcp-intelligence-server`
- the eleven importable modules listed in §3 available
  to any Python process using the same interpreter
  (e.g. `python -c "import mcp_read_server"` exits 0,
  prints nothing).

The three console scripts are the **only** thing the
wheel installs onto `PATH`. The wheel does NOT register
any system service, NOT modify any system file outside
the Python install location, NOT touch any
`ProductConfig` JSON, and NOT write any operator
credentials anywhere.

### 6.4 — How current entrypoints relate after install

Before the wheel install, an operator developing or
running the platform from a checkout uses
`scripts/dev/bootstrap_paths.ps1` to bring the eleven
`src/` paths onto `PYTHONPATH`. After `pip install`, the
bootstrap script is no longer needed for that
interpreter: the wheel's `pip`-managed install location
makes the eleven packages importable directly.

The PowerShell launchers under `scripts/dev/` (for
example `launch.ps1`, `run_dev_check.ps1`) and the
release helper `scripts/release/install.ps1` continue to
work from a repository checkout regardless of whether
the wheel is also installed; they are operator-side
tooling, not wheel content.

---

## 7. Uninstall verb

### 7.1 — Operator command

```
pip uninstall 1c-agent-platform
```

Pip prompts for confirmation by default; operators
scripting this MAY pass `--yes` per their own automation
policy.

### 7.2 — Expected operator-visible result

After uninstall:

- the three console scripts (`mcp-read-server`,
  `mcp-write-server`, `mcp-intelligence-server`)
  disappear from `PATH` (or from `<VENV_PATH>/bin/`);
- `python -c "import mcp_read_server"` exits non-zero
  with `ModuleNotFoundError`;
- the eleven `1c_agent_platform-*.dist-info/` and
  package directories disappear from the Python
  install location.

### 7.3 — What uninstall does NOT touch

`pip uninstall` removes ONLY the wheel content. It does
not remove operator-side artefacts living elsewhere on
the deployment host. Operators MUST clean those up
separately if they want a full teardown:

- **Materialised `ProductConfig` JSON files** —
  removed by the operator manually, or via the
  install-fast-path's own teardown convention. See
  `scripts/release/README.md` for the
  `install.ps1` lifecycle.
- **Operator `.env` files** — never written by the
  platform; operators remove their own `.env` files if
  they exist.
- **Systemd unit files installed under
  `/etc/systemd/system/` (Track L)** — removed by the
  operator per the Track L recipe at
  `docs/operators/service/service-supervision.md`. The
  wheel uninstall does NOT touch `/etc/systemd/system/`.
- **NSSM service registrations on Windows (Track L)** —
  removed by the operator with `nssm remove`. The wheel
  uninstall does NOT touch Windows services.
- **launchd plists on macOS (Track L)** — removed by
  the operator with `launchctl unload` and `rm`. The
  wheel uninstall does NOT touch launchd.

These are operator-side artefacts because they live
outside the Python install location and have their own
recipes (Track J / Track L). The wheel uninstall is
narrow on purpose.

---

## 8. Upgrade verb

### 8.1 — Operator command

```
pip install --upgrade <NEW_WHEEL_PATH>
```

where `<NEW_WHEEL_PATH>` is the path to a newer wheel
file built from a later project version.

### 8.2 — Expected operator-visible result

After `pip install --upgrade` succeeds:

- the three console scripts re-point at the new
  version's `__main__:main` entrypoints;
- the eleven importable modules now resolve to the new
  version's code;
- `pip show 1c-agent-platform` reports the new
  `<VERSION>`.

### 8.3 — Upgrade does NOT touch operator-side state

`pip install --upgrade` replaces wheel content **only**.
Operator-side artefacts survive:

- materialised `ProductConfig` JSON files survive;
- operator `.env` files survive;
- systemd unit files / NSSM registrations / launchd
  plists survive;
- log files, runtime state on disk, and any operator
  monitoring configuration survive.

### 8.4 — Restart-after-upgrade recommendation

For deployments that supervise the MCP servers as
long-running processes (Track L territory), the
operator typically wants to restart the supervised
service after upgrade so that the new code is loaded:

- POSIX with systemd (Track L):
  `systemctl restart <UNIT_NAME>` after `pip install
  --upgrade`.
- Windows with NSSM (Track L cross-reference):
  `nssm restart <SERVICE_NAME>` after `pip install
  --upgrade`.
- macOS with launchd (Track L cross-reference):
  `launchctl kickstart -k <DOMAIN_TARGET>` after
  `pip install --upgrade`.

A running MCP process imported its modules at startup;
without a restart it continues to execute the previous
version's code. This is standard Python deployment
behaviour, not a platform quirk.

---

## 9. Verify verb

### 9.1 — Minimum verify command

The minimum verify the operator runs after install (or
after upgrade) is:

```
mcp-read-server --help
```

If the console script runs, prints its usage banner,
and exits 0, then the wheel install is functional from
`PATH`'s point of view: `pip` placed the script
correctly, Python can import `mcp_read_server`, and the
`__main__:main` callable resolves.

Equivalent verifies for the other two console scripts:

```
mcp-write-server --help
mcp-intelligence-server --help
```

Any of the three is sufficient as a minimum verify; the
operator MAY run all three for completeness.

### 9.2 — Recommendation-only deeper verify

For operators who want stronger evidence than `--help`
that the installed wheel actually services real MCP
requests end-to-end, the Track K diagnostic harness at
`scripts/dev/mcp_client_smoke.py` provides a real MCP
client that drives each server over both stdio and HTTP
transports. A representative invocation from a
repository checkout (note: the harness lives in
`scripts/` and is therefore operator-side tooling, not
wheel content):

```
python scripts/dev/mcp_client_smoke.py --server read --transport both
```

The harness exits 0 on success. This is a
**recommendation-only** deeper verify; the
closure-target verify for this recipe is the `--help`
check, which is sufficient evidence that the install
mechanics succeeded.

### 9.3 — What verify does NOT prove

The `--help` verify and the smoke-harness deeper verify
do **not** prove:

- that the operator's `ProductConfig` JSON is valid
  (Track B / Track I install-fast-path territory);
- that the operator's reverse proxy is wired correctly
  for HTTP transport (Track J recipe territory);
- that the operator's supervised service is healthy
  long-term (Track L recipe territory);
- that the operator's connection to a real 1C
  infobase will succeed (out of scope for any track).

Verify confirms the wheel install is functional; it
does not certify the operator's deployment.

---

## 10. Relationship to current runtime surface

Wheel packaging is a **declarative / lifecycle** change.
It does not redesign the runtime, the transport, the
auth contract, the deployment boundary, or the
service-supervision boundary. The Track G / H / I / J /
K / L truths remain byte-identical after Step 4:

- **Track G (stdio MCP transport).** Stdio is a
  trusted-local-subprocess channel with no listener;
  `_stdio_transport.py` is unchanged.
- **Track H (HTTP MCP transport).** `/mcp` POST-only,
  1 MiB body cap, static bearer auth with
  failure-equivalence + redaction discipline,
  `WWW-Authenticate: Bearer realm="mcp"` on 401,
  non-`/mcp` 404 deterministic, in-process TLS
  forbidden, mTLS forbidden, `Forwarded` header
  MUST-NOT-consume, `/healthz` not shipped.
  `_network_transport.py` is unchanged.
- **Track I (installer auth round-trip).**
  `apps/platform/src/onec_platform/installer.py` is
  unchanged.
- **Track J (deployment boundary).** Reverse-proxy-
  terminated TLS posture is unchanged; the recipe at
  `docs/operators/deployment-boundary.md` is
  unchanged.
- **Track K (real MCP client smoke harness).**
  `scripts/dev/mcp_client_smoke.py` is unchanged.
- **Track L (service supervision).** The recipe at
  `docs/operators/service/service-supervision.md` and
  the systemd template at
  `docs/operators/service/mcp-server.service` are
  unchanged.

The `apps/platform/src/onec_platform/runtime.py`
module remains the per-process MCP runtime entrypoint
it has been since Track G / Step 4; **it is not a
service manager** and Track M does not extend it.

Wheel packaging does not introduce any new MCP tool to
any of the three servers. Registry counts remain:

- `mcp-read-server` — 15 tools;
- `mcp-write-server` — 25 tools;
- `mcp-intelligence-server` — 16 tools.

`selfcheck status=ok` and the four-line registry
summary are confirmed via `scripts/release/verify-release.ps1`
at every Track M commit from Step 3 onward.

---

## 11. Relationship to install fast path, deployment boundary, and service supervision

The wheel is one axis of operator delivery; the
install-fast-path, the deployment boundary, and the
service-supervision recipe are three other axes. They
are **orthogonal but complementary**, not
replacements for each other.

### 11.1 — Install fast path (Track B / Track I)

`scripts/release/install.ps1` is a thin wrapper over
`onec_platform.run_install_fast_path_from_json_file`. It
materialises a `ProductConfig` JSON on the operator's
deployment host from a small input descriptor — it does
**not** install Python packages. The wheel and the
install-fast-path are complementary:

| Axis | Provided by |
|---|---|
| Python code (the 11 packages, the 3 console scripts) | the wheel |
| Operator `ProductConfig` JSON (deployment-side config) | `scripts/release/install.ps1` |

A typical operator end-to-end flow:

1. On a **control host**: clone the repo;
   `pip install build`; `python -m build`; deliver the
   wheel out-of-band to the deployment host.
2. On the **deployment host**: `pip install
   <WHEEL_PATH>` into a venv; verify with
   `mcp-read-server --help`.
3. On the **deployment host**: run
   `scripts/release/install.ps1` to materialise the
   operator's `ProductConfig` JSON. (This step is
   operator-side; the install-fast-path is still
   executed from a repository checkout, not from
   inside the installed wheel — see §4.)
4. **Optionally**, on the deployment host: install
   the Track L systemd unit (or the cross-OS
   equivalent supervisor) referencing the
   materialised config and the console scripts.

Steps 1 and 2 are Track M territory. Steps 3 and 4 are
Track B / Track I / Track L territory carried forward
unchanged. The historical note in
`scripts/release/README.md` at lines 215–246 (the
Track C / Step 3 honest packaging constraint) is now
superseded by this recipe; the cross-link from
`pyproject.toml`'s updated comment block points
operators here.

### 11.2 — Deployment boundary (Track J)

The Track J recipe at
`docs/operators/deployment-boundary.md` describes how
the HTTP transport listener should be deployed:
plain HTTP/1.1 over a trusted network segment behind an
operator-owned reverse proxy that terminates TLS. The
wheel does not change that boundary; it merely makes
the listener code installable via `pip` instead of
requiring a repository checkout plus a `PYTHONPATH`
bootstrap.

### 11.3 — Service supervision (Track L)

The Track L recipe at
`docs/operators/service/service-supervision.md` (with
the systemd unit template at
`docs/operators/service/mcp-server.service`) describes
how to run the MCP servers as supervised long-running
processes on POSIX (systemd), Windows (NSSM), and macOS
(launchd). Track L is about the supervisor; Track M is
about how the code is delivered. The two are
orthogonal:

- Track L unit/service files reference the absolute
  path of a console script (typically
  `<VENV_PATH>/bin/mcp-read-server` after `pip
  install`), or, equivalently, a `python -m
  mcp_read_server` invocation. Either form depends on
  the wheel being installed.
- The wheel install does NOT register any systemd
  unit, NSSM service, or launchd plist. That step is
  operator-driven via the Track L recipe.

### 11.4 — Why three axes instead of one

It would be tempting to "solve packaging" by collapsing
all four axes (wheel, config materialisation, deployment
posture, service supervision) into one operator
artefact. Track M Step 3 explicitly **rejects** that
approach as scope expansion: each axis has its own
operator concerns, its own failure modes, and its own
threat model. Keeping them orthogonal lets operators
upgrade the wheel without touching their config, change
their reverse-proxy posture without rebuilding the
wheel, and switch supervisors without re-shipping any
Python code.

---

## 12. Cross-OS posture

The wheel is `py3-none-any` and installs on any host
with Python 3.11+ regardless of OS. The recipe makes
only narrow OS-specific observations:

### 12.1 — Windows

- Windows operators MAY use `py -m build` instead of
  `python -m build` if their Python installation uses
  the launcher (`py.exe`).
- Console scripts land under `<VENV_PATH>\Scripts\` for
  venv installs, or under the Python `Scripts\`
  directory for system installs.
- Path separator in `<WHEEL_PATH>` is `\` (or `/` —
  Windows pip accepts both).

### 12.2 — POSIX (Linux / macOS)

- Operators typically use `python -m venv <VENV_PATH>`
  followed by `<VENV_PATH>/bin/pip install
  <WHEEL_PATH>`.
- Console scripts land under `<VENV_PATH>/bin/`.
- The wheel does not require `sudo`; install into a
  per-operator venv whenever possible.

### 12.3 — What cross-OS posture does NOT mean

Pure-Python `py3-none-any` does **not** mean the
platform supports every OS-native package format. The
wheel is the supported artefact class; it is not
re-packaged into `.msi`, `.deb`, `.rpm`, `.dmg`,
`.pkg`, `.snap`, or `.flatpak`. Those formats are
explicitly out of scope (see §13).

---

## 13. Honest non-goals

This section enumerates packaging shapes the platform
**does NOT** support. Each phrase below appears in this
section **only** as an explicit denial:

- **"packaging solved forever"** — denied. Track M
  closes a specific, narrow, honest distribution
  boundary; it does not claim universal packaging
  completeness. Future tracks MAY revisit packaging
  for new operator workflows; this recipe is not such
  a track.
- **"PyPI release ready"** — denied. Track M does NOT
  publish the wheel to any package index. There is no
  "PyPI publication" step in this recipe. There is no
  "the platform now publishes to PyPI" announcement.
  The wheel is delivered out-of-band from a control
  host to a deployment host the operator owns.
- **"signed binary distribution"** — denied. There is
  no "signing key", no "cosign", no "sigstore", no
  in-tree "signing key" material. Operators who require
  a "signed distribution" chain MUST establish one
  out-of-band.
- **"all package managers supported"** — denied.
  There is no "Chocolatey / Homebrew / apt /
  conda-forge / NuGet support" matrix. There are no
  `.msi`, `.deb`, `.rpm`, `.dmg`, `.pkg`, `.snap`, or
  `.flatpak` artefacts produced by this recipe.
- **"production-ready packaging"** — denied. Track M
  closes one operator-facing lifecycle; it makes no
  attestation that every production-deployment
  concern is solved. Operators retain responsibility
  for OS hardening, supervisor configuration,
  network posture, and credential management (Track J
  / Track L territory).
- **"enterprise-ready packaging"** — denied. The
  phrase "enterprise-ready" does not describe this
  artefact. The wheel is a narrow honest delivery
  primitive.
- **"hostile-internet distribution ready"** — denied.
  The wheel is delivered between an operator's
  control host and the operator's deployment host
  over an operator-owned channel. The wheel does NOT
  ship a hostile-internet update mechanism.
- **"automatic update / OTA"** — denied. There is no
  in-platform update agent. `pip install --upgrade`
  is operator-initiated.
- **"GUI installer"** — denied. There is no "GUI
  installer" and no "wizard". The five lifecycle
  verbs are CLI-driven (`pip`, `python -m build`,
  `mcp-read-server --help`).
- **"production-grade packaging"** — denied (as a
  marketing phrase). The packaging shape is honest
  and narrow; the phrase is used in this recipe only
  as a quoted denial.

### 13.1 — Track M scope discipline

Track M Step 4 also explicitly does **not**:

- add any new entry to `[project.dependencies]` or
  `[project.optional-dependencies]`;
- add any new `[project.scripts]` entry (the three
  existing console-script entries are locked);
- modify `[build-system]` (hatchling is locked);
- add any `MANIFEST.in`, `setup.py`, or `setup.cfg`;
- add any new MCP tool to any of the three servers;
- modify any registry;
- modify any runtime module under `apps/*/src/` or
  `packages/*/src/`;
- modify `scripts/dev/*` or `scripts/release/*`;
- redesign any transport, auth, deployment, or
  service-supervision boundary.

---

## 14. Cross-references

Normative source-of-truth and adjacent operator
documents:

- **Track M Step 1 (plan)** —
  `docs/architecture/track-m-packaging-ecosystem-and-distribution-boundary-plan.md`.
- **Track M Step 2 (baseline audit)** —
  `docs/architecture/track-m-packaging-ecosystem-and-distribution-boundary-baseline-audit.md`.
- **Track M Step 3 (normative contract)** —
  `docs/architecture/track-m-packaging-ecosystem-and-distribution-boundary-contract.md`.
  This recipe operationalizes the contract; the
  contract is the source-of-truth for every claim in
  this recipe.
- **Track M Step 4 step map** —
  `docs/architecture/track-m-packaging-ecosystem-and-distribution-boundary-step-map.md`.
- **Track J deployment-boundary recipe** —
  `docs/operators/deployment-boundary.md`. The
  reverse-proxy-terminated TLS posture for the HTTP
  transport.
- **Track L service-supervision recipe** —
  `docs/operators/service/service-supervision.md`.
  Cross-OS supervisor wiring (systemd / NSSM /
  launchd).
- **Track L systemd unit template** —
  `docs/operators/service/mcp-server.service`.
  POSIX-specific declarative unit file.
- **Track K real MCP client smoke harness** —
  `scripts/dev/mcp_client_smoke.py`. Optional
  deeper-verify path (§9.2).
- **Install fast path** —
  `scripts/release/install.ps1` and
  `scripts/release/README.md`. The install-fast-path
  README's section at lines 215–246 records the
  Track C / Step 3 honest packaging constraint that
  Track M Step 4 now closes; the present recipe is
  the operator-facing replacement.
- **`pyproject.toml`** — the
  `[tool.hatch.build.targets.wheel]` `packages` list
  is the declarative source for §3; the updated
  comment block at the same location points
  operators here.

---

*End of recipe.*
