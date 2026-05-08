# Parallel Track G — Production-Grade MCP Transport and CLI (step map)

> **Companion file:** `track-g-production-grade-mcp-transport-and-cli-plan.md`
> (план трека). Этот файл — пошаговый map. Каждый шаг
> открывается отдельным заходом, не комбинируется в один
> commit с другим step'ом.

> **Track invariants** (повтор из плана):
> - registries `read=15 / write=25 / intelligence=16` без
>   drift'а на каждом step;
> - никаких новых MCP tools;
> - `server.py:REGISTERED_TOOLS` для всех 3 servers
>   identical content / identical lookup functions / identical
>   tool callable signatures;
> - никакого back-door write channel;
> - никаких 1cv8.exe runs ни на одном шаге трека (Track G
>   работает на process / transport layer, не на 1cv8 binary
>   surface);
> - production code touched только в Step 4 и **только**
>   на explicit allowed surfaces (см. Step 4 спецификацию);
> - никаких real credentials в repo / docs / commit messages;
> - transport — local stdio only; никакого network, никакого
>   auth, никакого supervisor daemon в текущем scope трека.

---

## Step 1 — planning production-grade MCP transport and CLI (этот шаг)

**Цель.** Зафиксировать документационный вход в Track G:
назначение, целевой результат, что входит / не входит,
guardrails, acceptance criteria, открытые вопросы Q1–Q7.

**Что меняем.** Только два planning-документа:

- `docs/architecture/track-g-production-grade-mcp-transport-and-cli-plan.md`
- `docs/architecture/track-g-production-grade-mcp-transport-and-cli-step-map.md`

Плюс минимальные status-правки в `README.md` и
`PROJECT-STATUS.md` под открытие active track'а G.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `.github/`, `.editorconfig`, `.python-version`,
`.gitignore`, `examples/`, `LICENSE`, `SECURITY.md`,
`CHANGELOG.md`, `docs/release-handoff.md`,
`docs/operator-manual.md`, `docs/administrator-manual.md`,
`docs/developer-manual.md`, `docs/runbooks/*`,
`apps/platform/README.md`, server `server.py` files —
без изменений на Step 1.

**Результат.** Track G открыт как active planning-only трек.
Implementation Step 4 не открывается в этом же заходе.

---

## Step 2 — transport / entrypoint baseline audit (docs-only)

**Цель.** Честно описать current state каждого из трёх MCP
server packages с точки зрения «что сейчас есть в коде, что
именно не хватает для transport readiness, где должна
интегрироваться MCP protocol implementation», и зафиксировать
final transport choice (Q1) + Python SDK vs custom decision
(Q2). Никакая implementation. Никаких code changes.

**Что меняем.**

1. Новый short audit-документ
   `docs/architecture/track-g-transport-baseline-audit.md`:
   - per-server inventory (`mcp_read_server`, `mcp_write_server`,
     `mcp_intelligence_server`): module structure, current
     `server.py` shape, registered tool count, existing public
     boundary functions (`list_tools()`, `get_tool(name)`),
     module docstring evidence missing transport;
   - exact integration points: где в `server.py` (или в новом
     `__main__.py`) должен жить JSON-RPC dispatch loop, где
     должна быть привязка `get_tool(name)` → MCP-protocol
     `tools/call` handler;
   - дискуссия Q1 (transport choice — default stdio only) с
     resolved answer + rationale (local trusted environment;
     consistent с MCP client integration patterns; minimum-
     viable);
   - дискуссия Q2 (`mcp` Python SDK availability +
     suitability) с resolved answer + manual code review SDK
     dependency graph;
   - дискуссия Q6 (`apps/platform` standalone entrypoint —
     out-of-scope initial Track G по умолчанию).
2. Optional: short discovery note about MCP-aware client
   ecosystem (Claude Desktop, MCP CLI tools) и формате
   stdio JSON-RPC они ожидают.

**Что НЕ меняем.** Никакого code change. `server.py` файлы,
`__main__.py` (которых нет), `pyproject.toml`, registries,
scripts, README/PROJECT-STATUS/CHANGELOG/SECURITY/release-handoff —
все untouched. Никаких runtime tests против MCP protocol.

**Результат.** Step 3 имеет concrete baseline + resolved Q1 /
Q2 / Q6 как trusted input для contract formalization.

---

## Step 3 — exact runtime / CLI / entrypoint contract (docs-only)

**Цель.** Formalize Step 4 implementation boundary через
prescriptive normative contract. RFC 2119-style language
(MUST / MUST NOT / SHALL / MAY).

**Что меняем.**

1. Новый contract document
   `docs/architecture/track-g-runtime-cli-entrypoint-contract.md`:
   - **`__main__.py` shape contract** — ровно три новых файла
     (`apps/mcp-{read,write,intelligence}-server/src/mcp_{read,write,intelligence}_server/__main__.py`);
     минимальный entry-point pattern (argument parsing →
     transport setup → server loop → graceful exit);
   - **CLI surface contract** (Q3 resolution) — `--help`,
     `--config-path <path>`, `--transport stdio`,
     `--log-level {DEBUG,INFO,WARNING,ERROR}`; точный exit
     code semantics (0 = clean exit, non-zero = error;
     **MUST NOT** raise uncaught Python exception на operator);
   - **Transport contract** — JSON-RPC 2.0 over stdio с
     line-delimited JSON framing; reuse Q1 / Q2 decisions из
     Step 2;
   - **Tool dispatch contract** — server `tools/list` MCP
     handler **MUST** delegate к existing `list_tools()`
     boundary; `tools/call` MCP handler **MUST** delegate к
     existing `get_tool(name)(...)` boundary; никаких новых
     tool-specific code paths;
   - **Auth contract** (Q4 resolution) — **none на transport
     уровне.** Servers operate в trusted local environment.
     Authentication / authorization / token validation —
     deliberately out-of-scope Track G (separate post-Track-G
     track);
   - **Supervision integration contract** (Q5 resolution) —
     servers **MUST** runnable как single-shot processes без
     internal supervision logic; existing
     `apps/platform/runtime.py` boundary (Phase 5 / Step 3 +
     Phase 6 / Step 6) operator может использовать без
     изменений (declare MCP server invocation в
     `runtime.services`); никакого background watcher'а Track
     G не ship'ит;
   - **`[project.scripts]` console entry points contract** —
     ровно три new console binary names (`mcp-read-server`,
     `mcp-write-server`, `mcp-intelligence-server`)
     mapping к `<package>.__main__:main`;
   - **Backward compatibility** — existing
     `server.py:REGISTERED_TOOLS` / `list_tools()` /
     `get_tool(name)` API **MUST** оставаться без изменений;
     никаких изменений в tool registry counts; pre-Track-G
     code paths которые import'или server modules
     должны continue importing without breakage;
   - **Implementation surface contract** — Step 4 production
     code touches **MUST** быть ограничены: 3 new
     `__main__.py` files + `pyproject.toml` (new
     `[project.scripts]` block); minor adjustments в
     `server.py` allowed if absolutely necessary для
     transport integration (preferred minimal touch);
     **MUST NOT** trogать `tools.py`, runtime/, models, dump_ops,
     guards, flow, packages/, scripts/, `apps/platform/`,
     registries;
   - **Non-goals** — explicit list mirror'ом из plan'а Section 6;
   - **Verification contract** — Step 4 commit message
     **MUST** include sanity-check artifact: `python -m
     mcp_read_server --help` / `python -m mcp_write_server
     --help` / `python -m mcp_intelligence_server --help`
     все возвращают exit 0 + non-empty usage output;
     verify-release.ps1 GREEN на 8 checks; registries без
     drift'а.
2. Resolve Q3 / Q4 / Q5 финально явно в этом document'е.

**Что НЕ меняем.** Никакого code change. `apps/`, `packages/`,
`scripts/`, `pyproject.toml` — untouched. README /
PROJECT-STATUS / CHANGELOG / SECURITY / release-handoff —
untouched (alignment Step 5 deliverable; closure Step 6
deliverable).

**Результат.** Step 4 имеет formal contract как trusted input.
Step 5 имеет contract document для cross-reference в operator-
facing docs.

---

## Step 4 — narrow implementation slice

**Цель.** Реализовать Track G runtime/CLI/transport ровно по
Step 3 contract'у. Это **единственный шаг Track G с
production code change.**

**Что меняем.**

1. **Three new `__main__.py` files:**
   - `apps/mcp-read-server/src/mcp_read_server/__main__.py`
   - `apps/mcp-write-server/src/mcp_write_server/__main__.py`
   - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`

   Each ship'ит:
   - `main()` function как entry point;
   - argparse-based CLI parsing для `--help`,
     `--config-path`, `--transport`, `--log-level`;
   - logging configuration через `logging.basicConfig` с
     resolved log level;
   - stdio transport setup (per Q1 / Q2 resolution);
   - JSON-RPC 2.0 dispatch loop связывающий MCP `tools/list` →
     `list_tools()` и MCP `tools/call` → `get_tool(name)(...)`;
   - graceful exit handling (SIGINT / EOF on stdin → clean
     return); никаких uncaught exceptions на operator.

2. **`pyproject.toml`** — добавить `[project.scripts]` block:
   ```toml
   [project.scripts]
   mcp-read-server = "mcp_read_server.__main__:main"
   mcp-write-server = "mcp_write_server.__main__:main"
   mcp-intelligence-server = "mcp_intelligence_server.__main__:main"
   ```

3. **Optional minor adjustments в `server.py`** — только если
   absolutely necessary для transport integration (preferred
   minimal touch). Например, если import paths Step 4 транспорта
   требуют добавления re-export'ов из server module. По
   умолчанию `server.py` остаётся untouched.

**Что НЕ меняем.**

- `tools.py`, `runtime/`, `models.py`, `dump_ops.py`,
  `guards.py`, `flow.py` в `mcp-write-server`;
- analogous internal modules в `mcp-read-server` и
  `mcp-intelligence-server`;
- `packages/*/src/`;
- `apps/platform/` (никаких изменений в product layer);
- `scripts/`, `examples/`;
- registries (`read=15 / write=25 / intelligence=16`
  invariant — verified через verify-release.ps1 selfcheck
  после Step 4);
- никаких новых MCP tools;
- никаких изменений в существующих `list_tools()` /
  `get_tool(name)` API;
- README / PROJECT-STATUS / CHANGELOG / SECURITY / release-
  handoff (alignment — Step 5; closure — Step 6);
- никаких runtime/test fixtures (если такие будут добавлены —
  это отдельный hygiene task).

**Verification (post-Step-4):**

- `python -m mcp_read_server --help` exit 0, non-empty usage;
- `python -m mcp_write_server --help` exit 0, non-empty usage;
- `python -m mcp_intelligence_server --help` exit 0,
  non-empty usage;
- `verify-release.ps1 -AllowDirtyTree` GREEN на 8 checks;
- registries `read=15 / write=25 / intelligence=16` без
  drift'а через selfcheck;
- никакого 1cv8.exe не запускалось;
- per-tool registry sanity check: `list_tools()` для каждого
  server'а возвращает identical to pre-Step-4 set.

**Результат.** Three MCP servers runnable as `python -m <pkg>`
+ console entry points через installed wheel; minimal stdio
transport functional для local MCP client integration.

---

## Step 5 — operator/docs alignment

**Цель.** Точечно выровнять operator-facing docs под new
entrypoints. Никакого нового code change beyond Step 4
implementation.

**Что меняем.**

1. **`README.md`** — Quickstart обновлён с pointer на new
   `python -m <server>` invocation pattern + console entry
   point names; «Куда идти дальше» bullet про "MCP server
   start" runbook (если ship'ится — см. ниже).
2. **`docs/release-handoff.md`** — Known limitations bullet
   «No production-grade MCP transport» обновляется под
   factual post-Track-G state: «stdio transport ship'нут;
   network transport / auth / supervision daemon —
   out-of-scope, остаются future tracks».
3. **`SECURITY.md`** — bullet «No production-grade MCP
   transport yet» обновляется под factual: «stdio transport
   present; security model = trusted local environment; no
   network exposure / auth / supervisor daemon».
4. **`apps/platform/README.md`** — short pointer на new
   server entrypoints в relevant runtime / launcher section
   (если такая существует). Минимальная правка.
5. **`scripts/dev/launch.ps1`** — possibly add new subcommand
   для server start (e.g. `launch.ps1 mcp-read-server`),
   маппинг к `python -m`. **Optional**: если minimal-touch
   preference применяется, добавление subcommand defer'ится
   на subsequent operator-experience track.
6. **New short runbook (optional):**
   `docs/runbooks/mcp-server-start.md` — operator runbook
   для standup всех 3 MCP servers (preconditions: Python
   3.11+, PYTHONPATH bootstrap; exact commands; what
   client integration looks like; how to verify server
   alive). **Optional**: если в Step 4 docstring'ах
   `__main__.py` достаточно описано — runbook можно
   defer'нуть.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/release/`,
`pyproject.toml`, registries; никаких новых MCP tools; никаких
изменений в `recovery.py`, `flow.py`, `binary_dispatch.py`,
`tools.py`. Track G plan / step-map / audit / contract docs —
frozen anchors, не задеваются.

**Resolve Q-extensions при необходимости** (e.g. operator
runbook scope — ship или defer; launch.ps1 subcommand — ship
или defer).

**Результат.** Operator-facing docs и launcher scripts
aligned под new entrypoints; reader понимает «как поднять
MCP server» без чтения source code.

---

## Step 6 — final integration pass and Track G closure

**Цель.** Закрыть весь Track G как documented status.
Read-only final integration check уже закрытых Steps 1–5,
потом минимальные closure-docs/status updates +
`pyproject.toml` version bump (Q7 = ДА default), потом final
closure commit. Никакого нового feature work, никаких новых
MCP tools, никакого remote push'а, никакого 1cv8.exe run.

**Read-only final integration check.**

- working tree clean перед началом;
- git history линейная Step 1 → 2 → 3 → 4 → 5 → 6;
- Step 2 audit doc на диске;
- Step 3 contract doc на диске;
- Step 4 production code change на диске:
  - 3 `__main__.py` files;
  - `[project.scripts]` block в `pyproject.toml`;
  - optional `server.py` minor adjustments (if any);
- Step 4 verification artifacts: `python -m <server> --help`
  все возвращают exit 0 + non-empty usage;
- Step 5 operator-facing docs alignment;
- registries `read=15 / write=25 / intelligence=16` без
  drift'а; selfcheck_status=ok;
- verify-release.ps1 GREEN на 8 checks;
- no real credentials в diff'ах ни одного из пяти Track G
  commit'ов;
- никаких 1cv8.exe runs за весь трек.

**Что меняем (только closure docs/status updates).**

- `README.md` — «Closed parallel tracks» дополняется Track G
  bullet'ом (шесть → семь закрытых треков); «Active parallel
  track» секция возвращается к «нет активного трека»;
  Quickstart-блок упоминает Track G как closed; добавляется
  «Track G detail (закрыт)» секция симметрично Track A/B/C/D/E/F
  detail блокам.
- `PROJECT-STATUS.md` — header (Текущий шаг + Статус)
  обновляется под Track G closed; добавляются пять новых
  per-step секций (Steps 2/3/4/5/6).
- `CHANGELOG.md` — новый раздел `## 0.4.0 — Parallel Track G
  — Production-Grade MCP Transport and CLI` (Q7 default ДА —
  Step 4 ship'ит real code change with new functional delta).
  Per-step outcomes, registry invariant, honest constraints
  update.
- `pyproject.toml` — version bump 0.3.0 → 0.4.0 (Q7 = ДА).

**Что НЕ меняем.**

- никакого нового feature work;
- никаких новых MCP tools;
- никакого remote push'а;
- `apps/`, `packages/`, `scripts/`, `examples/`,
  `docs/architecture/track-g-*` (planning / audit / contract
  docs остаются как written), `apps/platform/README.md`
  (Step 5 уже выровнял), `docs/release-handoff.md` (Step 5
  уже выровнял), `SECURITY.md` (Step 5 уже выровнял),
  `.github/`, `.editorconfig`, `.python-version`, `.gitignore`,
  `LICENSE` — не тронуты в этом шаге **за пределами**
  closure-narrative updates.
- Resolve Q7 финально (bump или follow-up под 0.3.0).

**Результат.** Track G полностью закрыт как documented status.
Активного трека нет. Открытие следующего parallel track'а —
отдельное operator-решение.

---

## Out-of-scope шагов (deliberately)

- никакая HTTP / WebSocket / SSE network transports
  (отдельный subsequent track);
- никакая authentication / authorization / token validation /
  mTLS / OAuth / SAML / OpenID Connect / RBAC / multi-tenant
  isolation;
- никакой supervision daemon / systemd unit / Windows Service
  registration / automatic restart watcher;
- никакая HA / clustering / multi-node;
- никакая service discovery / load balancing;
- никакая distributed tracing / observability stack;
- никакой web UI / dashboard frontend;
- никакая packaging ecosystem (`.msi` / `.deb` / GUI installer
  / signed distribution / PyPI publication) beyond
  `[project.scripts]` console entries;
- никакой full enterprise super-set (SSO/RBAC/multi-tenant/
  secrets vault as service / federated audit / policy-as-code
  DSL);
- никакая 1cv8.exe execution work (Track A territory);
- никакая rollback work (Track F territory);
- никакая AST / metadata work;
- никакая multi-version 1С matrix expansion (Track E
  territory);
- никаких новых MCP tools (registries `read=15 / write=25 /
  intelligence=16` без drift'а на всём треке);
- никакого hot reload;
- никаких 1cv8.exe runs ни на одном шаге Track G.

**GitHub remote push** — operator action, не часть Track G.
