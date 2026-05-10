# Parallel Track H — Network-Grade MCP Transport and Authentication Boundary (step map)

> **Companion file:**
> `track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`
> (план трека). Этот файл — пошаговый map. Каждый шаг
> открывается отдельным заходом, не комбинируется в один
> commit с другим step'ом.

> **Track invariants** (повтор из плана; нарушение любого =
> stop and surface, не silent fix):
> - registries `read=15 / write=25 / intelligence=16` без
>   drift'а на каждом step;
> - никаких новых MCP tools;
> - `server.py:REGISTERED_TOOLS` для всех 3 servers
>   identical content / identical lookup functions /
>   identical tool callable signatures на всех шагах;
> - `mcp_common/__init__.py` `__all__` preserved
>   byte-identical (никаких добавленных / удалённых /
>   переименованных public exports);
> - existing local stdio transport (`python -m <server>
>   --transport stdio`) preserved без regression;
> - `_stdio_transport.py` Track G helper не удаляется и не
>   меняет public shape; new transport помещается в
>   parallel underscore-prefixed private helper по тому же
>   pattern;
> - никакого back-door write channel; `run_write_flow`
>   discipline для write-tools preserved;
> - read-only-by-construction discipline для
>   `mcp-intelligence-server` preserved;
> - никаких 1cv8.exe runs ни на одном шаге трека (Track H
>   работает на process / transport / auth layer, не на
>   1cv8 binary surface);
> - production code touched **только в Step 4** и **только**
>   на explicit allowed surfaces (см. Step 4 спецификацию
>   ниже / финал — Step 3 contract);
> - никаких real credentials в repo / docs / commit
>   messages; bearer tokens / auth secrets — только через
>   `${ENV:NAME}` env-substitution или operator-private
>   overlay-файлы, никогда не committed;
> - `[tool.hatch.build.targets.wheel] packages = []`
>   preserved (Track C honest constraint carried through);
> - никакого `[project.dependencies]` block as mandatory
>   baseline без жёсткого технического обоснования (Step 2
>   audit + Step 3 contract обязаны это решить);
> - никакого supervisor / service registration / hot
>   reload / web UI / packaging-beyond-`[project.scripts]` /
>   standalone `apps/platform` entrypoint в текущем scope
>   трека;
> - GitHub remote push — operator action, не часть трека.

---

## Step 1 — planning network-grade MCP transport and authentication boundary (этот шаг)

**Цель.** Зафиксировать документационный вход в Track H:
назначение трека, целевой результат, что закрывает / не
закрывает Track H, чем отличается от Tracks A–G, guardrails,
acceptance criteria, открытые вопросы Q1–Q7 с default
recommendations.

**Что меняем.** Только два planning-документа:

- `docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`
  (новый, plan-уровень).
- `docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md`
  (новый, step-map; этот файл).

Плюс минимальные status-правки в `README.md` и
`PROJECT-STATUS.md` под открытие active track'а H:

- `README.md` — Quickstart paragraph (после Track G
  closure говорит «Активного трека сейчас нет» —
  переводим в «Активный трек: Track H planning-only»);
  «Active parallel track» секция (после Track G closure
  компактна — добавляем minimal Track H opening block с
  pointer'ом на planning docs; никаких premature
  implementation claims).
- `PROJECT-STATUS.md` — header `Текущий шаг` + `Статус`
  (после Track G closure говорят «Активного шага нет» /
  `closed` для Track G — переводим в `in progress` для
  Track H / Step 1); добавляем одну новую per-step
  opening section
  `### Parallel Track H / Step 1 — planning network-grade
  MCP transport and authentication boundary (завершён)`
  симметрично Track G / Step 1 / Track F / Step 1
  patterns.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `.github/`, `.editorconfig`,
`.python-version`, `.gitignore`, `examples/`, `LICENSE`,
`SECURITY.md`, `CHANGELOG.md`, `docs/release-handoff.md`,
`docs/operator-manual.md`, `docs/administrator-manual.md`,
`docs/developer-manual.md`, `docs/runbooks/*`,
`apps/platform/README.md`, server `server.py` files,
`__main__.py` files, `_stdio_transport.py` helper —
без изменений на Step 1.

**Результат.** Track H открыт как active planning-only
трек. Implementation Step 4 не открывается в этом же
заходе. Никаких production code changes; никаких registry
changes; никаких 1cv8.exe runs.

---

## Step 2 — transport / auth baseline audit (docs-only)

**Цель.** Честно описать current state каждого relevant
surface (трёх MCP server packages + `mcp_common` package +
`pyproject.toml`) с точки зрения «что сейчас есть в коде, что
именно отсутствует для network transport readiness, что
именно отсутствует для auth boundary readiness», и
зафиксировать factual evidence для Q1–Q4 resolution. Никакого
code change.

**Что меняем.** Один новый descriptive audit-документ:

- `docs/architecture/track-h-transport-and-auth-baseline-audit.md`
  (новый, descriptive read-only audit).

Плюс минимальные status-правки в `PROJECT-STATUS.md` под
закрытие Step 2 (новая `### Parallel Track H / Step 2 —
transport and auth baseline audit (завершён)` section
симметрично Track G / Step 2).

**Содержимое audit-документа** (минимальный obligatory
shape):

1. **Per-server / per-package inventory.** Точные file/line
   ссылки на existing transport boundary
   (`_stdio_transport.py` helper, `__main__.py` entrypoints,
   `server.py` registry surface), вне которых new transport
   будет жить.
2. **4-class breakdown.** Каждый existing surface
   классифицирован как:
   - Class 1 — **already useful baseline** для Track H
     (например, `list_tools()` / `get_tool(name)` boundary,
     `ToolResult` envelope, existing CLI flag parsing
     pattern в `_stdio_transport.py`);
   - Class 2 — **adjacent insufficient** (например,
     `apps/platform/runtime.py` имеет process orchestration
     boundary, но не MCP network transport);
   - Class 3 — **clearly missing** (network transport
     listener, auth header extraction, token validation,
     transport-level error envelope, network-side
     `tools/call` dispatch);
   - Class 4 — **out-of-scope Track H** (carry-over из
     plan §5: SSO / mTLS-everywhere / web UI / packaging
     ecosystem / supervisor / service registration /
     standalone `apps/platform` / new MCP tools / 1cv8 /
     rollback).
3. **Read-only evidence.** Подтверждённый grep'ом /
   inspection'ом current state (zero HTTP/WS/TCP/auth
   imports в server packages — повторить и зафиксировать
   как baseline).
4. **Q1 resolution.** Финальный transport family choice
   (`HTTP+SSE` / pure HTTP / WebSocket / TCP / Unix
   socket / named pipe) с per-option pros/cons и явным
   anchor decision.
5. **Q2 resolution.** Финальное количество transport
   families (default один; если audit выявит честную
   причину для двух — surface это явно).
6. **Q3 resolution.** Финальный auth baseline (static
   bearer token / API key / HMAC / Basic / mTLS-as-option)
   с per-option pros/cons.
7. **Q4 resolution.** Финальный config home (existing
   product-config schema vs new dedicated auth config
   file vs CLI-only).
8. **Open questions для Step 3 contract.** Точная shape
   transport framing, точная error envelope, точная token
   redaction discipline, точная failure semantics, точная
   intersection с existing `--transport stdio` flag.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `SECURITY.md`, `CHANGELOG.md`,
`docs/release-handoff.md`, `apps/platform/README.md`,
`README.md` (после Step 1 уже открыл active track —
дополнительно не правим), server `server.py` files,
`__main__.py` files, `_stdio_transport.py` helper.

**Результат.** Q1 / Q2 / Q3 / Q4 resolved; Step 3 contract
имеет фактическую basis. Production-код не правится.
Registries `15/25/16` без drift'а. Никаких 1cv8.exe runs.

---

## Step 3 — network transport / auth contract (docs-only)

**Цель.** Зафиксировать exact prescriptive normative
contract для Step 4 narrow implementation slice — какие
правила соблюдает new transport family, какой exact CLI
shape (расширение существующих `--transport` /
`--log-level` / `--config-path` плюс новые auth flags),
какой exact framing, какой exact auth token presentation /
validation / fail-closed / redaction discipline, какая exact
config schema, какая exact `mcp_common` integration boundary
(пacker / private helper по pattern Track G
`_stdio_transport.py`), какая exact `__main__.py`
integration shape (additive new transport branch без
ломания existing stdio default), какие allowed / forbidden
Step 4 file surfaces, какой verification protocol. Никакого
code change. Никакого 1cv8.exe.

**Что меняем.** Один новый prescriptive normative document:

- `docs/architecture/track-h-network-transport-and-auth-contract.md`
  (новый, RFC 2119-style; MUST / MUST NOT / SHALL / SHOULD /
  MAY с точным нормативным смыслом).

Плюс минимальные status-правки в `PROJECT-STATUS.md` под
закрытие Step 3 (новая `### Parallel Track H / Step 3 —
network transport and auth contract (завершён)` section
симметрично Track G / Step 3).

**Минимальный obligatory shape contract'а** (mirror Track G
contract structure, 13–15 sections):

1. **Purpose / scope.** Что contract нормирует, что не
   нормирует.
2. **Relationship to Step 1 plan and Step 2 audit.**
   Descriptive vs normative split (Step 2 audit — current
   state evidence; этот contract — prescriptive Step 4
   rules).
3. **Inherited fixed decisions.** Q1 / Q2 / Q3 / Q4
   inherited resolution from Step 2 audit.
4. **Network transport contract.** Exact transport family,
   exact framing (например, для HTTP+SSE — точные
   endpoint paths, точный Content-Type, точный SSE event
   schema, точная JSON-RPC 2.0 envelope mapping), exact
   lifecycle (initialize handshake поверх HTTP, ping
   heartbeat semantics), exact request/response error
   envelope, exact concurrent-request handling (default
   sequential per-connection — обоснование в Step 4
   implementation simplicity).
5. **CLI surface extension.** Existing `--transport stdio`
   default preserved; new value `--transport <name>` (Q1
   resolve) добавляется как valid alternative; new
   transport-specific flags (`--bind <host:port>`,
   `--auth-token-env <varname>` или эквивалент per Q3 /
   Q4 resolve); fail-closed validation на unknown
   transport / missing required auth flag.
6. **Auth contract.** Exact token presentation
   (`Authorization: Bearer <token>` header или
   transport-equivalent); exact token source (env-
   substitution `${ENV:NAME}` per Track D pattern, или
   config file, или CLI flag — точная shape финал в
   contract); exact validation (constant-time compare для
   защиты от timing oracle); exact fail-closed semantics
   (missing / empty / mismatched token → JSON-RPC error
   envelope с `-326XX` code и appropriate transport-level
   status; никакого partial / mixed acceptance); exact
   redaction discipline (token не должен попадать в
   stderr logs / structured logs / `command_preview` /
   audit `details` — переиспользование Track D redaction
   pattern по аналогии).
7. **Server binding / dispatch contract.** Network
   transport консьюмит tool registry **только через
   existing public boundary** (`list_tools()` /
   `get_tool(name)` indirection); никакого parallel
   registration path; `run_write_flow` discipline для
   write-tools preserved; никакого back-door write
   channel.
8. **Session / state contract.** Default — stateless
   (per-request token validation); никаких persistent
   session cookies / server-side session store; точная
   shape финал в contract.
9. **Multi-tenant / RBAC stance.** Explicit «no per-token
   permissioning, no per-tool ACL, no tenant isolation» —
   single-tier auth (valid token → access full registry).
   Per-token permissioning / RBAC / multi-tenant — отдельные
   future tracks.
10. **TLS / HTTPS posture.** Default — operator's
    responsibility (recommended deployment behind
    reverse proxy с TLS termination); built-in TLS
    listener — optional **MAY**, не mandatory; mTLS —
    explicit out-of-scope.
11. **`pyproject.toml` `[project.scripts]` posture.**
    Default — existing 3 console entries preserved
    unchanged; никаких новых entries unless absolutely
    justified (Step 3 contract — финальное решение).
12. **`pyproject.toml` `[project.dependencies]` posture.**
    Default — preserved empty (pure stdlib
    implementation); если transport choice (Q1) делает
    stdlib честно неподъёмным — точное обоснование
    + точный список dependencies (минимальный, без
    transitive bloat) фиксируется в contract.
13. **Backward compatibility.** Existing
    `python -m <server>` invocation preserved; existing
    `--transport stdio` default preserved; existing
    `_stdio_transport.py` helper public shape preserved
    (Track H добавляет parallel new helper, не модифицирует
    старый); registries / `mcp_common` API / audit shape
    preserved.
14. **Exact Step 4 implementation surface.** Allowed
    files (например, новый private
    `mcp_common._network_transport.py` underscore-
    prefixed helper + minor extensions в трёх
    `__main__.py` для wiring new transport branch +
    `pyproject.toml` если Step 4 ship'ит новый optional
    `[project.dependencies]` group — финальный список в
    contract); forbidden surfaces (registries / new MCP
    tools / `tools.py` / `runtime/` / `apps/platform/*` /
    `server.py` modifications / scripts/* / examples/* /
    docs за пределами этого contract); scope-creep
    markers.
15. **Verification contract для Step 4.** Required
    positive checks (`python -m <server> --transport
    <name> --help` exit 0 + non-empty usage; sample
    valid-token request → success; sample
    missing/invalid-token request → fail-closed error
    envelope; existing `--transport stdio --help` exit 0
    + usage без regression; verify-release.ps1 GREEN на
    8 checks; selfcheck `read=15 / write=25 /
    intelligence=16; status=ok`); required negative
    checks (no 1cv8.exe runs; no real credentials in
    diff; no registry drift; no new MCP tools; no
    forbidden surface touched).

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `SECURITY.md`, `CHANGELOG.md`,
`docs/release-handoff.md`, `apps/platform/README.md`,
`README.md`, server `server.py` files, `__main__.py` files,
`_stdio_transport.py` helper.

**Результат.** Step 3 contract на диске; Q5 / Q6 явно
re-confirmed как **out-of-scope** (carry-over из plan §5);
Q7 default ДА re-confirmed (финальное Step 6 closure
decision). Step 4 implementation имеет точные allowed /
forbidden file lists, exact auth shape, exact transport
shape, exact verification protocol. Production-код не
правится. Registries `15/25/16` без drift'а. Никаких
1cv8.exe runs.

---

## Step 4 — narrow network transport and auth implementation

**Цель.** Единственный шаг Track H с production code
change. Реализовать ровно тот узкий implementation slice,
который зафиксирован в Step 3 contract: одна network
transport family + один auth model, additive поверх
existing Track G stdio baseline. Никакого scope creep,
никаких новых MCP tools, никакого 1cv8.exe.

**Что меняем (предположительный shape; финальный список —
Step 3 contract).**

1. **Один новый private internal helper** (по pattern
   Track G `_stdio_transport.py`):
   - например,
     `packages/mcp-common/src/mcp_common/_network_transport.py`
     (точное имя — Step 3 contract; underscore-prefixed,
     **NOT** экспортирован из `mcp_common/__init__.py`;
     deliberate private status).
   - Реализует chosen transport family (Q1 resolve), auth
     middleware (Q3 resolve), transport-level error
     envelope, JSON-RPC 2.0 dispatch через existing
     `list_tools()` / `get_tool(name)` boundary.
2. **Минимальные additive extensions в трёх `__main__.py`**
   (без полной перезаписи; existing stdio path preserved):
   - branch на `args.transport` value;
   - new transport flag wiring;
   - existing default `--transport stdio` preserved;
   - existing `--config-path` / `--log-level` flags
     preserved.
3. **Optional `pyproject.toml` extensions** (только если
   Step 3 contract это явно разрешает):
   - new `[project.optional-dependencies]` group (например,
     `network`) с минимальным списком — если Q1 transport
     choice требует third-party dep;
   - existing `[project.scripts]` block preserved
     unchanged (default — Track H **не** добавляет новые
     console entries; финал — Step 3 contract);
   - existing `[tool.hatch.build.targets.wheel] packages
     = []` preserved unchanged (Track C honest constraint).
4. **Optional config schema extension** (если Q4 / Step 3
   contract выбрал config-file home для auth):
   - new optional `auth` или `transport.network` section в
     existing product-config JSON schema;
   - точная shape — Step 3 contract.

**Что НЕ меняем (forbidden Step 4 surfaces; финальный
список — Step 3 contract).** Registry contents
(`server.py:REGISTERED_TOOLS` для всех 3 servers);
`tools.py`, `models.py`, `runtime/*` packages; `apps/platform/*`
(Q6 explicit out-of-scope); `mcp_common/__init__.py`
`__all__` (preserved byte-identical); existing
`_stdio_transport.py` helper public shape; existing three
`server.py` files; existing three `__main__.py` files
**кроме** дополнительной transport branch wiring;
`scripts/*`; `examples/*`; documentation за пределами
status-правок в `PROJECT-STATUS.md`; `SECURITY.md`,
`CHANGELOG.md`, `docs/release-handoff.md`,
`apps/platform/README.md` (Step 5 / Step 6 territory);
all Track H planning / audit / contract docs (frozen
Step 1 / 2 / 3 anchors).

**Verification (минимально obligatory).**

- `python -m mcp_read_server --transport stdio --help` →
  exit 0 + non-empty usage (existing path не сломался).
- `python -m mcp_read_server --transport <Q1-resolve>
  --help` → exit 0 + non-empty usage (new path работает).
- Sample request с valid auth artifact на network transport
  → success path, valid JSON-RPC response envelope.
- Sample request с missing / invalid auth artifact на
  network transport → fail-closed (точная shape — Step 3
  contract); никакого partial acceptance; никакого silent
  bypass.
- `verify-release.ps1 -AllowDirtyTree` GREEN на 8 checks.
- Selfcheck registries `read=15 / write=25 /
  intelligence=16; status=ok`; `imports_ok=true`.
- Никаких 1cv8.exe runs.
- Никаких real credentials в commit / diff.

**Результат.** Network MCP transport ship'нут как additive
layer; auth boundary живой и fail-closed; existing stdio
baseline preserved; registries без drift'а; `mcp_common`
public API без изменений.

---

## Step 5 — operator docs and security alignment (docs-only)

**Цель.** Точечно выровнять operator-facing и security-
adjacent документацию под фактический post-Step-4 transport
+ auth surface, без раздувания в closure narrative Step 6.
Docs-only; никакого production code change; никакого
pyproject.toml; никаких registry changes; никакого 1cv8.exe.

**Что меняем (predicted scope; финальный список — Step 5
inventory).**

1. **`SECURITY.md`** — обновить «Local stdio MCP transport
   only» bullet под фактический post-Step-4 state: «Local
   stdio + one bounded network transport with minimum
   token-based auth»; explicit threat model statement (что
   именно covered, что нет); явно оставить still-NOT
   list (full enterprise identity / mTLS-everywhere /
   supervisor / multi-tenant / RBAC).
2. **`docs/release-handoff.md`** — добавить bullet под
   «What is in this handoff» listing новый network
   transport entrypoint flag + auth requirement; обновить
   «What is NOT in this handoff» (still no enterprise
   identity stack / no service ecosystem / no web UI /
   no packaging beyond `[project.scripts]`); обновить
   «Known limitations» bullet под фактический network
   surface.
3. **`README.md`** — обновить Quickstart paragraph
   («Активный трек Track H» → «Track H Steps 1-4 closed»
   + краткое описание фактического network/auth surface);
   обновить «Что Quickstart **не** обещает» под факт того,
   что network/auth теперь часть baseline'а; «Active
   parallel track» секция enumerates closed Steps 1-4 +
   actual launch surface + canonical Step 6 next.
4. **`apps/platform/README.md`** — точечный update «Чего
   сейчас намеренно ещё нет» list (если есть direct
   factual drift); если нет — НЕ трогать.
5. **`scripts/dev/launch.ps1` + `scripts/dev/README.md`** —
   только если есть direct user-facing drift в help/usage
   wording; default — НЕ трогать.

Плюс минимальные status-правки в `PROJECT-STATUS.md` под
закрытие Step 5 (новая `### Parallel Track H / Step 5 —
operator docs and security alignment (завершён)` section).

**Что НЕ меняем.** Production code (`apps/*/src`,
`packages/*/src` — Step 5 docs-only by contract);
`pyproject.toml` (Q7 = Step 6 territory); registries / new
MCP tools (`read=15 / write=25 / intelligence=16`
invariant); `CHANGELOG.md` (новая `## 0.5.0` или
equivalent section — Q7 / Step 6 closure deliverable);
all Track H planning / audit / contract docs (frozen
Step 1 / 2 / 3 anchors); other Tracks A–G docs.

**Результат.** Operator-facing docs не лгут об actual
post-Step-4 surface. Никакой premature Track H closure
language. Никаких false claims про
enterprise-identity-stack / zero-trust / packaging.
verify-release.ps1 остаётся GREEN. Registries без
drift'а. Никаких 1cv8.exe runs.

---

## Step 6 — final integration pass and Track H closure

**Цель.** Закрыть весь Track H как documented status.
Read-only final integration check уже закрытых Steps 1-5,
потом минимальные closure-docs/status updates +
`pyproject.toml` version bump (Q7 resolve), потом final
closure commit. Никакого нового feature work, никаких
новых MCP tools, никакого remote push'а, никакого 1cv8.exe
run.

**Pre-closure read-only check (mandatory gate).**

- working tree clean перед началом — gate PASS;
- git history линейная Step 1 → 2 → 3 → 4 → 5 → 6 (все
  commit'ы на месте; никаких accidental extra commits
  inside Track H scope);
- все Step 1–5 deliverables на диске: 3 architecture
  docs (plan + step-map + audit + contract; точное
  количество — финал на основе Step 3 result), Step 4
  implementation files (новый private helper + minor
  `__main__.py` extensions); existing Track G artefacts
  preserved;
- Step 5 operator-facing alignment confirmed;
- registries `read=15 / write=25 / intelligence=16` без
  drift'а;
- `verify-release.ps1 -AllowDirtyTree` GREEN на 8 checks
  с full selfcheck;
- no real credentials в diff'ах ни одного из пяти Track H
  commit'ов;
- никаких 1cv8.exe runs ни на одном шаге Track H.

**Q7 resolve (closure decision).** Default ДА (`0.4.0 →
0.5.0`) если Step 4 ship'нул real production code change с
observable runtime capability delta. Final reasoning —
закрепляется в Step 6 commit body на основе фактического
Step 4 functional delta:

- Step 4 ship'нул real network transport + real auth
  boundary (observable runtime capability delta —
  `python -m <server> --transport <network>` теперь
  принимает remote MCP-aware client requests, что до
  Track H было невозможно) → backward-compatible new
  functionality classifying as classic MINOR bump per
  SemVer → bump.
- Precedent: Track D `0.1.0 → 0.2.0`, Track F
  `0.2.0 → 0.3.0`, Track G `0.3.0 → 0.4.0` — все шли с
  MINOR bump на real production code change. Track E
  (scaffolding only, no functional delta) → no bump.
  Track H ship'ит real code change → bump.

**Что меняем (closure-docs only; финальный scope = symmetric
с Track A/B/C/D/E/F/G closure pattern).**

- `pyproject.toml` — version `0.4.0` → `0.5.0` (если Q7 = ДА).
  Никаких других changes; existing `[project.scripts]`
  preserved; existing `[tool.hatch.build.targets.wheel]
  packages = []` preserved (Track C honest constraint
  carried through); existing `[project.dependencies]`
  state — финальный по Step 4 result (если Step 4 добавил
  optional `network` extras — preserved).
- `README.md` — Quickstart paragraph переписан под
  «Активного трека сейчас нет — Track H закрыт восьмым
  по счёту post-phase треком»; «Closed parallel tracks»
  list дополнен Track H bullet'ом (семь → восемь
  закрытых треков); «Active parallel track» секция сжата
  под «нет активного трека» с pointer'ом на Track H
  detail; добавлена «Track H detail (закрыт)» секция
  полным блоком симметрично Track A / B / C / D / E /
  F / G detail (per-step bullets с commit hashes; что
  Track H реально закрыл; что Track H **не делает**
  «enterprise-ready MCP server'ом»; registry invariant;
  honest constraints).
- `PROJECT-STATUS.md` — header (`Текущий шаг` + `Статус`)
  обновлён под Track H closed + Q7 = ДА явное упоминание
  + 6 commit hashes + factual Step 4 surface; общий
  narrative-блок переписан под closure; добавлены пять
  новых per-step секций (Steps 2/3/4/5/6) симметрично
  Track G / Step 2-6 patterns.
- `CHANGELOG.md` — добавлен новый раздел `## 0.5.0 —
  Parallel Track H — Network-Grade MCP Transport and
  Authentication Boundary` (или соответствующий version,
  если Q7 = НЕТ — closure follow-up under existing 0.4.0
  с explicit reasoning) с per-step outcomes, actual
  network/auth surface block, registry invariant carried
  through, honest constraints update (no full enterprise
  identity / no zero-trust mesh / no web UI / no
  packaging beyond `[project.scripts]` / no service
  management / no new MCP tools / no 1cv8 / no remote
  push), Active work = None (post-Track-H).

**Что НЕ меняем (закрытый scope).** `apps/`, `packages/`,
`scripts/`, `examples/`, `.github/`, `.editorconfig`,
`.python-version`, `.gitignore`, `LICENSE`; `SECURITY.md`,
`docs/release-handoff.md`, `apps/platform/README.md`,
`scripts/dev/*` (Step 5 уже выровнял); Track H planning /
audit / contract docs (frozen Step 1 / 2 / 3 anchors);
Track A / B / C / D / E / F / G docs; runbooks; registries.
`1cv8.exe` не запускался ни на одном шаге Track H.

**Результат.** Track H закрыт как documented status. Все
12 acceptance criteria из плана §7 выполнены. Активного
трека нет; восемь post-phase parallel track'ов
(A, B, C, D, E, F, G, H) закрыты последовательно;
открытие следующего трека — отдельное operator decision.
**GitHub remote push не часть Track H — repo готов к
выкладке, но пушить — operator action.**
