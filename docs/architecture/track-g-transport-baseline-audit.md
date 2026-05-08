# Track G — transport / entrypoint baseline audit

> **Companion files:**
> `track-g-production-grade-mcp-transport-and-cli-plan.md` (Step 1
> plan), `track-g-production-grade-mcp-transport-and-cli-step-map.md`
> (Step 1 step-map), `track-g-runtime-cli-entrypoint-contract.md`
> (Step 3 partner — formal normative contract).

> **Status:** Track G / Step 2 deliverable. Documentation-only.
> **Descriptive snapshot** of the current transport / entrypoint
> picture before Step 3 contract formalization. Никакой code
> change. Никаких 1cv8.exe runs. Все findings — pure read-only
> inspection of repository state at HEAD `7a39454` (Track G /
> Step 1 closure).

---

## 1. Purpose / scope

Этот документ отвечает на **один** вопрос:

> «Как реально выглядит текущая transport / entrypoint картина
> проекта **перед** Step 3 contract formalization, и какие
> exact gaps / available baseline pieces должен учесть Step 3
> normative contract?»

Документ **descriptive, не normative.** Документ **не**:

- formalize'ует eligibility / contract rules — это Step 3
  territory (`track-g-runtime-cli-entrypoint-contract.md`);
- ship'ит code — это Step 4 territory;
- pretend'ует, что production-grade transport уже есть;
- pretend'ует, что MCP Python SDK интегрирован (он **не**
  интегрирован — см. section 7);
- alignning operator-facing docs (Step 5);
- making closure narrative claims (Step 6).

Документ **строго отделяет** четыре класса things:

- **Class 1 — already existing useful baseline** (re-usable
  Step 4 input);
- **Class 2 — adjacent but insufficient** (looks related, не
  решает transport problem);
- **Class 3 — clearly missing pieces** (Step 4 implementation
  scope);
- **Class 4 — explicitly out-of-scope для Track G** (отдельные
  tracks post-Track-G).

Эти классы — single source of truth для Step 3 boundary
formalization.

---

## 2. Current baseline by surface

### 2.1 `pyproject.toml`

Full file 46 строк. Critical findings:

- `version = "0.3.0"` (post-Track-F closure).
- **NO `[project.dependencies]` block.** Runtime dependencies
  не объявлены вообще. Project running на pure stdlib +
  internal monorepo packages.
- **NO `[project.scripts]` block.** Никаких console entry
  points; `pip install <wheel> && mcp-read-server` не
  существует как path.
- **NO `[project.optional-dependencies]`.**
- `[tool.hatch.build.targets.wheel] packages = []` —
  intentionally empty per Track C / Step 3 honest constraint;
  `pip install` не работает; install flow через
  `scripts/release/install.ps1`.

**Implication для Track G:** Step 4 **MAY** add `[project.scripts]`
block (per Track G plan); **MUST NOT** add `[project.dependencies]`
(custom-implementation Q2 decision keeps stdlib invariant).
Wheel-build не задаётся Track G — это Track C honest
constraint которое стоит preserve.

### 2.2 Three MCP server packages

Identical structure pattern:

```
apps/mcp-{read,write,intelligence}-server/src/mcp_{read,write,intelligence}_server/
├── __init__.py
├── models.py
├── runtime/
│   ├── __init__.py
│   ├── ... (server-specific internal modules)
├── server.py
└── tools.py
```

**Никакого `__main__.py`** ни в одном из трёх. Verified Step
1 inventory + повторно verified в Step 2.

`server.py` для всех 3 имеет **identical shape**:

- module docstring явно: «Skeleton server bootstrap... Real
  MCP transport ... will be added later.»
- import'ы из `mcp_common`: `ToolCallable`,
  `build_tool_registry`, `get_registered_tool`,
  `list_registered_tools`;
- import'ы из `.tools`: 15 / 25 / 16 tool functions
  (соответственно для read / write / intelligence);
- `REGISTERED_TOOLS: dict[str, ToolCallable] =
  build_tool_registry({ ... })` — registry dict;
- public boundary: `list_tools() -> list[str]` и
  `get_tool(name: str) -> ToolCallable | None`.

**Это registry skeleton, не MCP server.** Реальный JSON-RPC
framing, transport loop, dispatch logic — **отсутствуют.**

### 2.3 `runtime/` subdirs внутри MCP server packages

- `mcp_read_server/runtime/`: `__init__.py`, `context.py`,
  `dump_adapter.py`, `live_adapter.py`, `models.py`.
- `mcp_write_server/runtime/`: `__init__.py`,
  `binary_dispatch.py`, `context.py`, `dump_ops.py`,
  `flow.py`, `guards.py`, `metadata_ops.py`, `models.py`.
- `mcp_intelligence_server/runtime/`: `__init__.py`,
  `context.py`, `dump_scanner.py`, `graph.py`, `models.py`,
  `reference_finder.py`.

**Это internal server-specific runtime layer** (data
adapters, write-flow discipline, metadata operations, graph
analysis, etc.) — **не transport layer**. Track G **MUST
NOT** touch any of these (per Track G plan implementation
surface contract).

### 2.4 `apps/platform/src/onec_platform/`

Product layer. **Не MCP server по архитектуре.** 14 modules:
`bootstrap.py`, `dashboard.py`, `doctor.py`, `enterprise.py`,
`installer.py`, `loader.py`, `models.py`,
`process_control.py`, `realstand.py`, `recovery.py`,
`runtime.py`, `runtime_logs.py`, `state.py`, `__init__.py`.

`runtime.py` имеет 8 public boundary functions (lines
783-961): `get_product_runtime_status(...)`,
`start_product_runtime(...)`, `stop_product_runtime(...)`,
`reload_product_runtime(...)` + 4 `_from_json_file`
variants. Это **generic process orchestration через
operator-declared argv** в `runtime.services` config section
(Phase 5 / Step 3 + Phase 6 / Step 6 hardening: structured
logs, restart-policy `"never" | "restart-if-stale"`
boundary-only).

**Это generic process management abstraction.** Она **не
запускает MCP servers напрямую** (нет `__main__` чтобы
запустить); но после Step 4 ship'ит `__main__`, operator
сможет declare MCP server invocation в `runtime.services`
без extension этого layer'а.

### 2.5 `mcp_common` package

`packages/mcp-common/src/mcp_common/`:
- `__init__.py`, `errors.py`, `registry.py`, `result.py`,
  `types.py`.

Public exports: `HealthCheckError`, `PlatformError`,
`PolicyDeniedError`, `ProcessExecutionError`, `ToolCallable`,
`build_tool_registry`, `get_registered_tool`,
`list_registered_tools`, `ToolResult`, `OperationContext`.

**Это pure stdlib utility package для tool registry
abstractions** + error hierarchy + `ToolResult` model +
`OperationContext` type. Naming совпадение historical
(«mcp» reflects «MCP servers share these helpers», не «MCP
protocol library»).

**`mcp_common` НЕ содержит:**
- JSON-RPC parsing / serialization;
- stdio / network transport loop;
- MCP protocol message types (`InitializeRequest`,
  `ListToolsRequest`, `CallToolRequest`, etc.);
- handshake / capability negotiation;
- streaming / cancellation primitives.

### 2.6 `scripts/dev/`

5 files: `bootstrap_paths.ps1`, `launch.ps1`,
`run_dev_check.ps1`, `selfcheck.py`, `README.md`.

`launch.ps1` (Track B / Step 4) — operator/dev umbrella
для local actions; явно говорит:

> «What this wrapper deliberately does NOT do:
>    - it does NOT start MCP read / write / intelligence
>      servers (there is no production-grade transport
>      yet);»

Subcommands: `selfcheck` / `repl` / `run <script.py>` /
`help`. **Никакого server start subcommand.**

`bootstrap_paths.ps1` — PYTHONPATH bootstrap для 11
internal `src/` directories.

`run_dev_check.ps1` / `selfcheck.py` — CI-aligned health
verification (registry counts + import smoke).

### 2.7 `scripts/release/`

4 files: `install.ps1`, `_install_runner.py`,
`verify-release.ps1`, `README.md`.

`install.ps1` — product-config materialization wrapper
(Track B / Step 3 + Track C honest constraints). **Не
запускает MCP servers.**

`verify-release.ps1` — release verify (Track C / Step 2 +
Track D / Step 5 8th check). **Не запускает MCP servers.**

`_install_runner.py` — Python helper для install.ps1.

### 2.8 Existing Track G Step 1 docs

- `docs/architecture/track-g-production-grade-mcp-transport-and-cli-plan.md`
  (424 lines).
- `docs/architecture/track-g-production-grade-mcp-transport-and-cli-step-map.md`
  (410 lines).

Frozen anchors; этот audit doc **не** дублирует их content.

---

## 3. What already exists (Class 1 — re-usable Step 4 input)

Following items уже на диске и могут служить **trusted
input** для Step 4 implementation без modification:

1. **Tool registries (3 servers).** `server.py:REGISTERED_TOOLS`
   dict + `list_tools()` / `get_tool(name)` boundary
   functions. Public, tested через `verify-release.ps1`
   selfcheck (`read=15 / write=25 / intelligence=16`
   invariant). **Step 4 transport layer должен dispatch к
   `get_tool(name)(...)` без any registry modification.**
2. **Tool definitions в `tools.py` каждого server'а.**
   Already callable as Python functions; transport layer
   should invoke them directly с positional / keyword args
   parsed из MCP `tools/call` request.
3. **`mcp_common` registry abstractions.** `ToolCallable`
   type, `ToolResult` model, error hierarchy. Step 4
   transport layer **MAY** reuse `ToolResult.payload` shape
   when serializing tool responses to MCP wire format.
4. **`apps/platform/runtime.py` 8 boundary functions.**
   Generic process orchestration; available для post-Step-4
   supervision integration через `runtime.services` config.
   **Не extension'ится Track G'ом.**
5. **`scripts/dev/launch.ps1` operator umbrella.** Existing
   pattern для adding new subcommand (e.g.
   `launch.ps1 mcp-read-server`) на Step 5.
6. **`scripts/dev/bootstrap_paths.ps1` PYTHONPATH bootstrap.**
   Re-usable для Step 4 server invocation in dev mode.
7. **`scripts/release/verify-release.ps1`.** Существующий 8
   checks набор; Step 4 implementation должен сохранять
   GREEN status (no new checks added; existing checks 1-8
   покрывают presence новых files implicitly где
   applicable).
8. **`pyproject.toml` package metadata.** `name`, `version`,
   `requires-python`, `authors`. Step 4 **MAY** add
   `[project.scripts]` block без trogая existing fields.

---

## 4. What is merely adjacent but insufficient (Class 2)

Following items **look related** to transport problem, но
**не** решают его и **не** должны быть extended Track G'ом:

1. **`apps/platform/runtime.py`** — **generic process
   orchestration layer**, не MCP-specific transport. Может
   orchestrate любой operator-declared argv (включая будущий
   `python -m mcp_read_server`), но сам entry point должен
   существовать **сначала** (Step 4 ship'ит entry point;
   runtime layer уже готов orchestrate его). **Step 4 не
   extends runtime.py;** Track G plan implementation surface
   ограничивает changes ровно: 3 new `__main__.py` files +
   `pyproject.toml` `[project.scripts]` block.
2. **`mcp_common` package.** Naming совпадение с upstream
   `mcp` PyPI SDK; **не имеет protocol implementation**.
   Pure stdlib utility. Step 4 **MAY** add transport-helper
   modules внутри `mcp_common` (если final shape requires
   shared transport code), но это уточнение — Step 3 contract
   territory; default minimal-touch preference suggests
   keeping `mcp_common` untouched.
3. **`scripts/dev/launch.ps1`** — **явно сам говорит** «does
   NOT start MCP servers». Existing operator-side wrapper для
   adhoc Python actions, не server standup. Step 5 (operator
   docs alignment) **MAY** add new subcommand для server
   start.
4. **`scripts/release/install.ps1`** — config materialization,
   не server start. Не задевается Track G'ом.
5. **`server.py` registry skeletons.** Provide tool registries,
   но **не protocol layer**; missing JSON-RPC framing, stdio
   loop, dispatch logic. Step 4 implementation поверх
   registries.
6. **`apps/platform/onec_platform`** — product layer; не MCP
   server по архитектуре. Standalone entrypoint для product
   operations — **out-of-scope Track G** (Q6 resolution).

---

## 5. What is missing (Class 3 — Step 4 implementation scope)

Concrete missing pieces — single source of truth для Step 3
contract definition + Step 4 implementation:

1. **3 new `__main__.py` files** — по одному в каждом MCP
   server package:
   - `apps/mcp-read-server/src/mcp_read_server/__main__.py`
   - `apps/mcp-write-server/src/mcp_write_server/__main__.py`
   - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
2. **`[project.scripts]` block в `pyproject.toml`** —
   три console entry points mapping к
   `<package>.__main__:main`.
3. **MCP protocol implementation** — JSON-RPC 2.0 message
   parsing (request envelopes, response envelopes, error
   envelopes); custom-implementation на stdlib (Q2 resolution).
4. **stdio transport loop** — line-delimited JSON read от
   `sys.stdin`, write к `sys.stdout`, graceful EOF / SIGINT
   handling.
5. **MCP method handlers**:
   - `initialize` — capability negotiation handshake;
   - `tools/list` — delegate к existing `list_tools()`;
   - `tools/call` — parse name + arguments, delegate к
     existing `get_tool(name)(...)`, serialize `ToolResult` к
     MCP response shape;
   - error responses для unknown / malformed methods.
6. **CLI argument parsing** — `argparse`-based; flags
   `--help`, `--config-path <path>`, `--transport stdio`
   (default + only supported в Step 4),
   `--log-level {DEBUG,INFO,WARNING,ERROR}` (default `INFO`).
7. **Logging configuration setup** — `logging.basicConfig`
   с resolved level; logs к `sys.stderr` чтобы не
   засорять stdout transport channel.
8. **Graceful exit semantics** — clean exit code 0 на EOF
   stdin / SIGINT; non-zero на uncaught Python exceptions
   prevented (per Step 3 contract — никаких raw tracebacks
   на operator).
9. **Single-command server start story** — operator runbook
   answer на «как поднять MCP server» (Step 5 territory, но
   doc gap уже existed pre-Track-G).
10. **Production run model** — explicit «trusted local
    environment, no auth, no network exposure» honest
    constraint surfaced в SECURITY.md / release-handoff.md
    (Step 5 territory).

---

## 6. Q1 resolution — transport choice

**Resolved: stdio only.**

**Reasoning** (read-only grounded):

- **Standard MCP client integration pattern.** Major MCP
  clients в industry today (Claude Desktop, MCP CLI tools,
  MCP-aware editor integrations) **default к stdio JSON-RPC**
  transport. Stdio support = «works with majority of MCP
  clients out-of-the-box без extra config».
- **Closes factual gap «cannot start at all» narrowly.**
  Operator получает working MCP server в trusted local
  environment без network stack management, port allocation,
  service discovery infrastructure.
- **Zero new dependencies.** stdio = `sys.stdin` + `sys.stdout` +
  stdlib `json` + stdlib `argparse` + stdlib `logging`.
  Consistent с current monorepo philosophy (verified в
  section 2.1: `pyproject.toml` без `[project.dependencies]`).
- **Trusted local environment security model.** No network
  exposure → no auth surface to defend → matches Track G plan
  Q4 «no auth on transport» decision.

**Why HTTP / WebSocket / SSE остаются out-of-scope:**

- **Web framework dependency.** Adding FastAPI / Uvicorn /
  aiohttp / Starlette = significant transitive deps tree;
  ломает stdlib-only invariant.
- **Auth posture concern.** HTTP transport практически
  всегда требует token validation / TLS / mutual auth — это
  отдельный security architecture decision, не Track G
  scope.
- **Network hardening.** Rate limiting, CORS, denial-of-
  service protection, TLS certificate management —
  отдельный hardening track.
- **No current consumer requirement.** Trusted local
  environment satisfied stdio.
- **Subsequent track legitimacy.** Network MCP transport
  legitimately scoped поверх Track G stdio baseline в
  separate parallel track post-Track-G.

---

## 7. Q2 resolution — MCP SDK availability vs custom

**Resolved: CUSTOM IMPLEMENTATION (stdlib only). No new
dependency added к `pyproject.toml`.**

**Read-only evidence:**

1. **`pyproject.toml` line-by-line read** (full 46 lines):
   - **NO `[project.dependencies]` block exists** —
     verified literal absence; project declares zero runtime
     dependencies.
   - **NO `[project.optional-dependencies]` block** —
     verified literal absence.
2. **Repo-wide grep** через `apps/`, `packages/`,
   `scripts/`:
   - `^(from|import) mcp(\.|$| )` — **ZERO matches**.
   - `^(from|import) jsonrpc` — **ZERO matches**.
   - `^from anthropic_mcp` — **ZERO matches**.
   - Other transport library markers (`websockets`,
     `fastapi`, `JSONRPCMessage`, `stdio_server`,
     `MCPServer`, `transport_layer`) — verified Step 1 +
     re-verified Step 2: ZERO matches.
3. **`packages/mcp-common`** verified line-by-line:
   exports = error types + registry helpers + ToolResult +
   OperationContext. **Pure stdlib utility.** Не upstream
   MCP SDK; naming совпадение historical.
4. **No transitive dependency chain** к upstream `mcp` SDK
   возможен — since project declares zero deps, transitive
   deps tree empty.

**Decision rationale:**

1. **Pure stdlib consistency.** Current monorepo invariant —
   «pure stdlib + internal packages». Adding upstream `mcp`
   SDK ломает this invariant and introduces new transitive
   deps tree (`mcp` SDK itself может pull `pydantic` /
   `anyio` / `httpx` / etc. depending on version).
2. **No working install path для consumer.** Project
   doesn't ship as installable wheel today (Track C / Step 3
   honest constraint: `[tool.hatch.build.targets.wheel]
   packages = []`). Adding `mcp` к dependencies без working
   install path создаёт confusing operator UX («что мне
   делать с этим dependency?»).
3. **Manageable scope для stdlib implementation.** JSON-RPC
   2.0 stdio loop ≈ 150–200 lines on stdlib (`json` +
   `sys.stdin`/`sys.stdout` + `argparse` + `logging`).
   Maintained по-server: ≈ 100 lines `__main__.py` (CLI +
   logging setup + transport setup + signal handling) +
   ≈ 100 lines shared transport helper (parse / dispatch /
   serialize). Total Step 4 implementation ≈ 400-500 lines
   разделённых между 3 servers + 1 shared module.
4. **Track G stays narrow.** Adding SDK dependency
   introduces SDK-version compatibility concerns, breaking-
   change tracking, security advisory monitoring,
   transitive dep audits — все out-of-scope Track G.
5. **Future option preserved.** Track G doesn't preclude
   future migration к SDK. Step 4 implementation —
   **first** production-grade slice. Subsequent track
   может migrate to upstream SDK if value justifies new
   dependency surface.

**Caveat (для Step 4 verification):** custom implementation
должна быть проверена против real MCP client (Claude
Desktop, MCP CLI, Inspector) после Step 4 ship — но это part
of Step 5 verification по runbook'у, не blocker для Step 4
custom-implementation decision.

---

## 8. Q6 resolution — `apps/platform` standalone entrypoint

**Resolved: OUT-OF-SCOPE Track G.** Initial Track G ship'ит
`__main__.py` ровно для **3 MCP server packages**, не 4.

**Reasoning:**

1. **`apps/platform/onec_platform/` — product layer**, не MCP
   server по архитектуре. Не имеет
   `server.py:REGISTERED_TOOLS` registry; не expose'ит MCP
   tool surface.
2. **Existing operator entry paths уже available:**
   - `scripts/release/install.ps1` (через
     `_install_runner.py` → `run_install_fast_path`) — config
     materialization;
   - `scripts/dev/launch.ps1 selfcheck` (через `selfcheck.py` →
     import paths) — health check;
   - 8 boundary functions в `runtime.py` (`start_product_runtime`
     etc. + `_from_json_file` variants) — Python API;
   - другие product-layer Python boundaries (`installer`,
     `recovery`, `dashboard`, `realstand`, `enterprise`)
     доступны import'ом.
3. **Standalone `__main__.py` для onec_platform** = новая
   operator-experience surface track про CLI для product
   operations (install / verify / status / dashboard /
   start-runtime / stop-runtime / inspect-history). Это
   **отдельная operator-experience track**, не вписывается в
   Track G «MCP transport» scope.
4. **Track G plan Q6 default = НЕТ;** этот audit это
   подтверждает via по-surface inspection.
5. **Implementation surface contract** (Step 3 territory)
   будет formalize that Step 4 touches **3 `__main__.py`
   files only**, not 4.

**If operator demand demonstrably emerges** (post-Track-G):
standalone `__main__.py` для onec_platform может быть
opened as separate track, без modifying Track G closure.

---

## 9. Step 3 handoff note

После Step 2 closure (этот audit doc shipped), Step 3
formalize'ует normative contract в отдельный prescriptive
document
`docs/architecture/track-g-runtime-cli-entrypoint-contract.md`.
Этот audit document — **descriptive** input для Step 3;
contract — **normative** layer поверх него.

Step 3 contract MUST formalize (на основе этого audit):

1. **`__main__.py` shape contract** — exact 3 files (per Q6
   resolution = 3 servers, не 4); exact `main()` function
   signature; exact entry-point pattern (argument parsing →
   logging setup → transport setup → server loop → graceful
   exit).
2. **CLI surface contract** (Q3 default из Step 1 plan) —
   `--help`, `--config-path`, `--transport stdio` (Q1
   resolution = stdio only), `--log-level
   {DEBUG,INFO,WARNING,ERROR}`.
3. **Transport contract** — JSON-RPC 2.0 over stdio, custom
   stdlib implementation (Q2 resolution = no SDK
   dependency); line-delimited JSON framing; logs к stderr,
   not stdout.
4. **Tool dispatch contract** — `tools/list` → `list_tools()`,
   `tools/call` → `get_tool(name)(...)`; никаких registry
   modifications.
5. **Auth contract** (Q4 default из Step 1 plan = none on
   transport) — security model = trusted local environment.
6. **Supervision integration contract** (Q5 default из Step
   1 plan) — через existing `apps/platform/runtime.py`
   boundary без extension этого layer'а.
7. **`[project.scripts]` console entry points contract** —
   3 binary names mapping к `<package>.__main__:main`; **no
   `[project.dependencies]` change** (per Q2).
8. **Backward compatibility** — existing
   `server.py:REGISTERED_TOOLS` / `list_tools()` /
   `get_tool(name)` API preserved; registry counts
   preserved (`read=15 / write=25 / intelligence=16`).
9. **Implementation surface contract** — Step 4 production
   code touches **MUST** be limited to: 3 new `__main__.py`
   files + `pyproject.toml` `[project.scripts]` block;
   optional minor `server.py` adjustments preferred-minimal-
   touch; **no `mcp_common` extension** (default; Step 3
   may re-evaluate if shared transport helper genuinely
   reduces code duplication, но default — keep `mcp_common`
   untouched).
10. **Verification contract** — Step 4 commit message MUST
    include sanity-check artifact: `python -m
    mcp_{read,write,intelligence}_server --help` все
    возвращают exit 0 + non-empty usage output;
    verify-release.ps1 GREEN на 8 checks; registries без
    drift'а; никаких 1cv8.exe runs.

Step 3 contract document **MUST NOT** дублировать per-surface
inventory из этого audit'а. Reader обращается к этому audit
для current-state evidence, к Step 3 contract — для
implementation rules.

---

## 10. Honest summary (one paragraph)

На сегодня (Track G / Step 2 closure) проект имеет **strong
tool registry skeletons** для трёх MCP servers (`server.py`
с `REGISTERED_TOOLS` + `list_tools()` + `get_tool(name)`
boundary в каждом; tool counts `read=15 / write=25 /
intelligence=16` стабильны), **strong tool implementations**
в `tools.py` каждого server'а, **strong product layer**
(`apps/platform/onec_platform` 14 modules incl. `runtime.py`
8 boundary functions), и **strong operator helper scripts**
(`scripts/dev/launch.ps1` umbrella, `scripts/release/install.ps1`
config materialization, `verify-release.ps1` 8-check release
verify). **НО** проект **не имеет**: ни одного `__main__.py`
файла; ни одного `[project.scripts]` console entry; ни одной
строки real MCP protocol implementation; ни одного MCP SDK
import; ни одного network transport setup; ни одного
operator runbook про «как запустить MCP server». Repo declared
zero runtime dependencies; custom-implementation на stdlib —
forced choice (Q2 = custom). Stdio transport — narrow
sufficient first slice (Q1 = stdio only). `apps/platform`
standalone entrypoint — отдельный future track (Q6 =
out-of-scope). Step 3 contract будет formalize эти resolutions
плюс exact Step 4 implementation surface boundary, ссылаясь
на этот audit как trusted descriptive baseline.
