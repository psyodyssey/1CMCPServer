# 1C Agent Platform

Проект **1C Agent Platform** — собственная MCP-платформа (Model Context Protocol) для работы
ИИ-агентов с конфигурацией и инфобазами 1С:Предприятие.

## Quickstart

> **Что это.** MCP-платформа для работы AI-агентов с конфигурацией и
> инфобазами 1С:Предприятие. На сегодня закрыты Phases 1–6 (read /
> write / metadata / intelligence / product layer / industrialization),
> Parallel Track A — full real binary-backed write path
> (DumpCfg → LoadConfigFromFiles → UpdateDBCfg), отработанный на
> reference stand'е, Parallel Track B — productization & delivery
> polish, Parallel Track C — packaging & installer delivery
> (release-facing layout, verify path, release handoff document),
> Parallel Track D — operator credentials hardening
> (env-substitution `${ENV:NAME}` path с render-time fail-closed,
> password-position redaction в `command_preview`, 8-й
> credential-template-hygiene check в `verify-release.ps1`; **не**
> enterprise security platform), и Parallel Track E —
> multi-version 1C smoke matrix scaffolding (frozen
> `frozen-smoke-v1` scenario, operator runbook, matrix-table doc
> с reference row на `8.3.27.1859`; см.
> [`docs/version-support-matrix.md`](docs/version-support-matrix.md)).
> Additional version evidence rows не добавлены — Step 4 закрыт
> через honest operator-supplied gap (на operator machine
> отсутствуют 1С minor families помимо `8.3.27`); это **не**
> «поддержка всех версий», **не** full QA program и **не**
> blanket multi-version support claim. И Parallel Track F —
> rollback whitelist expansion: `_AUTOMATIC_RECOVERY_SUPPORTED`
> расширен с 2 до 6 tools (`add_catalog_attribute`,
> `add_document_attribute` уже были; добавлены
> `add_form_attribute`, `add_form_element`,
> `append_module_method`, `replace_module_method_body`).
> Coverage broader, но **по-прежнему узкий**: 6 of 25
> mutating registry tools = 24% surface. **Не** universal
> rollback, **не** public `delete_*`, **не** multi-file
> restore, **не** AST-based semantic reverse. Tier 3
> categorical exclusions (`create_*` family,
> `apply_config_from_files`,
> `update_database_configuration`) остаются вне whitelist'а
> by design. Parallel Track G — Production-Grade MCP
> Transport and CLI: три canonical `__main__.py`
> entrypoint'а (`python -m mcp_read_server`,
> `python -m mcp_write_server`,
> `python -m mcp_intelligence_server`), minimum-viable
> stdio JSON-RPC 2.0 transport (line-delimited, stdlib-only,
> no third-party SDK), original CLI surface (`--help`,
> `--config-path`, `--transport`, `--log-level`),
> `[project.scripts]` console entries в `pyproject.toml`.
> И Parallel Track H — Network-Grade MCP Transport and
> Authentication Boundary: добавлен второй transport family
> поверх того же `list_tools()` / `get_tool(name)`
> boundary — single HTTP/1.1 `/mcp` endpoint, POST only,
> `application/json`, 1 MiB body cap, static bearer
> authentication (`Authorization: <case-insensitive-Bearer>
> <token>`, constant-time compare, fail-closed on
> missing/empty/malformed/invalid), token sources via
> `ProductConfig.auth.tokens` (`${ENV:NAME}` env-substitution
> only, literal cleartext rejected at config-load) или
> `--auth-token-env <VARNAME>` CLI flag (CLI wins, replace
> not merge); two new CLI flags `--bind <HOST>:<PORT>` и
> `--auth-token-env <VARNAME>`. Threat model = local trusted
> stdio для `--transport stdio`; trusted-network behind
> operator-owned reverse proxy для `--transport http`.
> Это **не** in-process TLS / HTTPS termination, **не**
> mTLS / client certificate auth, **не** JWT / OAuth 2.0 /
> OIDC / SAML / SCIM, **не** RBAC / ABAC / per-tool ACL /
> per-tenant isolation / multi-tenant, **не** WebSocket /
> SSE / TCP / Unix-socket / named-pipe transports, **не**
> supervisor daemon / systemd unit / Windows Service
> registration / hot reload / restart watcher, **не** web
> UI / dashboard, **не** packaging ecosystem (`.msi` /
> `.deb` / GUI installer / signed distribution / wheel
> publication beyond `[project.scripts]` declarations),
> **не** standalone `apps/platform` entrypoint, **не**
> новые MCP tools (registries `read=15 / write=25 /
> intelligence=16` invariant carried through). Активный
> трек сейчас — **Parallel Track I — Installer Auth
> Round-Trip Integrity**: узкий defect-fix follow-up к
> Track H, закрывший один honest gap из Track H closure
> narrative. Step 4 ship'нул +15 LOC additive emit branch
> в `installer.py:_config_to_dict` symmetric к existing
> Phase 6 / Step 8 enterprise-block emit-only-when-
> divergent pattern; auth.tokens теперь preserved через
> install fast path round-trip byte-identical, raw
> `${ENV:NAME}` strings round-tripped как configuration
> data (env resolution остаётся runtime boundary в
> `_network_transport._resolve_env_token`, не install
> time). Pre-Track-H configs без `auth` section продолжают
> round-trip'ить byte-identical (no implicit `"auth": {}`
> injection). Active no longer — Track I закрыт девятым
> по счёту post-phase треком (Q6 = PATCH bump
> `0.5.0 → 0.5.1`; Step 4 — defect-class round-trip
> integrity fix, no new public API surface, no new
> runtime capability для end users). Это **не** redesign
> auth model, **не** packaging ecosystem, **не** secrets
> vault / KMS, **не** новые MCP tools, **не** deployment
> ecosystem solved.

### Системные требования

- Windows + PowerShell 5.1 / 7+ (текущие entrypoints — PowerShell-скрипты);
- Python 3.11 (см. `.python-version`);
- (опционально) `1cv8.exe` — нужен только для real binary-backed
  write path; без него работают read-only / synthetic режимы.

### Install — материализовать product config

```powershell
.\scripts\release\install.ps1 `
    -ConfigPath examples\demo-infobase\infobase6.config.json `
    -OutputConfigPath C:\path\to\target\product.config.json
```

По умолчанию запускается в **preview** режиме (ничего не пишется на
диск). Чтобы реально записать config — добавьте `-Confirm`. Подробности
параметров и exit-кодов: [`scripts/release/README.md`](scripts/release/README.md).

### Check — local selfcheck

```powershell
.\scripts\dev\launch.ps1 selfcheck
```

Печатает компактный отчёт с registry counts (`read=15 / write=25 /
intelligence=16`), `imports_ok=true`, `selfcheck_status=ok`.
Эквивалент [`scripts/dev/run_dev_check.ps1`](scripts/dev/run_dev_check.ps1)
(используется в `.github/workflows/dev-check.yml`).

### Local dev launch — operator / dev umbrella

```powershell
.\scripts\dev\launch.ps1 help                 # usage
.\scripts\dev\launch.ps1 selfcheck            # см. выше
.\scripts\dev\launch.ps1 repl                 # interactive Python с PYTHONPATH
.\scripts\dev\launch.ps1 run <script.py> ...  # ad-hoc Python script
```

Подробности и список того, что `launch.ps1` сознательно **не**
делает (не стартует MCP-серверы, не запускает pytest, не дублирует
install fast path, не трогает инфобазу): [`scripts/dev/README.md`](scripts/dev/README.md).

### Куда идти дальше

- [`docs/release-handoff.md`](docs/release-handoff.md) —
  release handoff для receive-side оператора: что вы получили,
  prerequisites, reproducible install sequence, verify sequence,
  known limitations.
- [`apps/platform/README.md`](apps/platform/README.md) — product
  layer: bootstrap, runtime, dashboard, guided workflows, rollback
  assistant, real-stand smoke, enterprise foundation inspector.
- [`docs/operator-manual.md`](docs/operator-manual.md) —
  operator-facing reference.
- [`docs/runbooks/`](docs/runbooks/) — воспроизводимые сценарии,
  включая `track-a-reference-stand-round-trip.md` (real binary-backed
  round-trip) и `track-e-multi-version-smoke-matrix.md` (operator
  runbook для `frozen-smoke-v1` на operator-supplied 1С версиях).
- [`docs/version-support-matrix.md`](docs/version-support-matrix.md) —
  evidence table с frozen 12-column shape (Track E); single source
  of truth для актуального уровня multi-version evidence — **не**
  blanket support claim.
- [`docs/architecture/`](docs/architecture/) — phase- и track-plans
  + step maps (включая Track B, Track C, Track D и Track E
  planning).
- [`PROJECT-STATUS.md`](PROJECT-STATUS.md) — детальный статус фаз
  и треков с per-step deliverables.

### Что Quickstart **не** обещает

Этот entry — про **локальный** install и check. Track G / Step 4
ship'нул узкий local stdio MCP transport baseline (три
`python -m <server>` entrypoint'а + minimum-viable JSON-RPC 2.0
stdio loop). Track H / Step 4 добавил **второй transport family**
поверх того же registry boundary: single HTTP/1.1 `/mcp` endpoint
с static bearer authentication (case-insensitive scheme,
constant-time compare, fail-closed on missing/invalid token,
required-when-`--transport http` startup gate), плюс два новых
CLI флага (`--bind <HOST>:<PORT>` + `--auth-token-env <VARNAME>`).
Этот совокупный baseline (stdio + narrow HTTP+bearer) — **не**
in-process TLS / HTTPS termination (operator's reverse proxy
ответственен за TLS termination перед HTTP listener'ом), **не**
mTLS / client certificate authentication, **не** JWT / OAuth 2.0
/ OIDC / SAML / SCIM (token introspection / refresh / rotation
endpoints из этого набора тоже out-of-scope), **не** RBAC / ABAC
/ per-tool ACL / multi-tenant isolation, **не** WebSocket / SSE /
TCP / Unix-socket / named-pipe transports, **не** session cookies
/ rate limiting, **не** installer ecosystem (`.msi` / `.deb` /
GUI wizard / signed binary distribution / wheel publication beyond
`[project.scripts]` declarations — wheel build по-прежнему пуст
по Track C honest constraint), **не** web UI / dashboard frontend,
**не** enterprise-ready deployment (SSO/RBAC, multi-tenant,
secrets vault, federated audit storage, multi-instance HA), **не**
hot reload / OS-level service supervision (systemd unit / Windows
Service / automatic restart watcher), **не** standalone
`apps/platform` entrypoint. Threat model HTTP transport — **trusted-
network deployment** behind operator-owned reverse proxy; не
hostile-internet zero-trust posture. Эти направления — out of
scope активных треков; см. honest constraints в
[`SECURITY.md`](SECURITY.md), [`CHANGELOG.md`](CHANGELOG.md) и
[`docs/architecture/`](docs/architecture/).

## Идея

Платформа строится как единая система, через которую ИИ-агенты (Claude Code и другие)
в перспективе смогут безопасно и структурированно:

- читать конфигурацию и метаданные 1С;
- изменять объекты конфигурации и данные инфобазы;
- анализировать поведение системы, журналы и состояние;
- решать прикладные задачи разработчика и аналитика 1С.

Эти возможности — целевое направление развития платформы, а не уже реализованная
функциональность: на текущем этапе создан только каркас проекта.

## Архитектура

Платформа делится на три изолированных MCP-сервера и продуктовый слой
поверх них:

- **mcp-read-server** — чтение конфигурации, метаданных, данных, журналов (только чтение).
- **mcp-write-server** — изменение конфигурации, объектов, кода, миграций (операции записи).
- **mcp-intelligence-server** — аналитика, диагностика, подсказки, troubleshooting.
- **platform** (`apps/platform/`, пакет `onec_platform`) — продуктовый
  слой Phase 5: product-config, prereqs doctor, bootstrap entrypoint.
  Не MCP-сервер; обвязка над тремя серверами выше.

Разделение на read / write / intelligence позволяет гибко управлять правами,
безопасностью и политиками применения операций. Продуктовый слой не
размывает эти границы — он только собирает их в продуктовую
поверхность.

## Текущий статус по фазам

- **Phase 0** — инфраструктурная база завершена.
- **Phase 1** — Read MVP завершён. `mcp-read-server` содержит 15
  инструментов чтения (configuration, metadata, dump/code,
  query path, event log, diagnostics).
- **Phase 2** — Write MVP завершён. `mcp-write-server` содержит 15
  инструментов: группа A (preflight/snapshot), группа B
  (controlled write через единый `run_write_flow`), группа C
  (verification), группа D (audit / rollback hint). Остаются
  временные stub'ы поверх `onec-process-runner` для apply /
  update-db / dump snapshot — до появления пути к `1cv8` в
  `onec-config`.
- **Phase 3** — Metadata Changes завершён. `mcp-write-server`
  содержит 23 инструмента: object/attribute level
  (`create_catalog`, `add_catalog_attribute`,
  `add_document_attribute`, `create_common_module`),
  form/module level (`create_managed_form`, `add_form_element`,
  `append_module_method`, `replace_module_method_body` с
  обязательным `confirm_replace=True`), metadata shape verification
  (`verify_attribute_exists`, расширенный `verify_metadata_change`
  с `kind ∈ {object_exists, module_contains, attribute_exists,
  form_exists, method_exists}`, `diff_dump_fragment`) — плюс
  сохранившиеся группы A (preflight/snapshot) и D (audit/rollback
  hint). Mutating metadata-tools строго идут через единый
  `run_write_flow(...)`; real-`1cv8` binary integration остаётся
  parallel follow-up.
- **Phase 4** — Intelligence Layer завершён. `mcp-intelligence-server`
  содержит 16 **read-only** public tool'ов в четырёх группах:
  group A (dependency / reference analysis —
  `find_references_to_object`, `find_module_method_usages`,
  `analyze_object_dependencies`); group B (impact / affected scope —
  `estimate_change_impact`, `find_affected_forms`,
  `find_affected_modules`, `suggest_safe_change_order`); group C
  (diagnostics / troubleshooting — `analyze_runtime_issue`,
  `analyze_event_log_patterns`, `diagnose_broken_form_binding`,
  `diagnose_missing_method_or_attribute`); group D (recommendations
  / planning — `suggest_fix_for_issue`,
  `suggest_metadata_patch_plan`, `summarize_configuration_risk`,
  `prepare_intelligence_report`). Контракт: intelligence-server
  никогда не пишет, не идёт через `run_write_flow`, не пишет audit
  и не импортирует `onec_policy_engine`. Read- и write-серверы на
  Phase 4 не деградировали (15 и 23 tool'а соответственно).
  Step 7 — final integration pass — пройден.
- **Phase 5** — Product Layer **завершён** на Step 8 final
  integration pass. Цель — **Product Layer**: переход от
  набора серверов и tool'ов к цельному продуктовому
  контуру, который можно установить, поднять, подключить
  к 1С, безопасно использовать, сопровождать, откатывать,
  диагностировать. Это **не** означает, что продукт уже
  достиг финального industrial-grade / enterprise-ready
  состояния — крупные хвосты честно перечислены в
  `PROJECT-STATUS.md` (полное замещение Phase 2 stub'ов
  реальным 1cv8-backed write path, multi-step real-stand
  smoke, public `delete_*` write-tools, hot reload,
  production MCP transport, web-UI, full enterprise
  hardening и т.п.). Phase 5 закрывает именно
  product-layer контур поверх существующих read/write/
  intelligence-серверов. Phase 5 строится **поверх** уже готовых
  read/write/intelligence слоёв и **не** добавляет новые MCP
  tool'ы ради расширения tool surface. Шесть продуктовых
  блоков: installation/bootstrap, runtime orchestration,
  guided workflows, rollback/recovery/audit UX, real-stand /
  1cv8 binary integration track, operator/admin/developer
  docs. Safety guarantees Phase 2–4 (никакого silent prod
  write, обязательные snapshots, обязательный verify,
  обязательный audit, read-only intelligence) сохраняются и
  на product-уровне не размываются. После Phase 5 / Step 3
  у продуктового слоя `apps/platform/` (пакет
  `onec_platform`) есть и **bootstrap contract** Step 2
  (product-config schema + JSON loader, prereqs doctor,
  bootstrap entrypoint), и **runtime orchestration
  contract** Step 3: декларативные argv-команды на сервис
  в `runtime.services`, единые boundary-функции
  `start_product_runtime` / `stop_product_runtime` /
  `get_product_runtime_status` / `reload_product_runtime`,
  атомарный state-файл под `<work_dir>/.runtime/runtime-state.json`,
  cross-platform проверка PID-liveness на чистом stdlib.
  Это **не** означает, что у read/write/intelligence
  серверов уже есть production-grade MCP transport — Step 3
  даёт **product-level launcher contract** над тем, что
  оператор объявил, а не подменяет собой будущую
  серверную transport-обвязку. `reload` сейчас — это
  controlled stop-then-start, не hot reload. После
  Phase 5 / Step 4 у продуктового слоя есть и
  **environment doctor / health dashboard**: единая
  read-only функция `build_environment_dashboard(...)`,
  агрегирующая в один снимок секции `bootstrap` +
  `runtime` + `read_health` + `read_diagnosis` +
  `intelligence_runtime` + `intelligence_risk` поверх уже
  существующих read- и intelligence-tool'ов. Dashboard
  выдаёт rule-based вердикт `healthy` / `degraded` /
  `blocked` и флаг `ready_for_workflows`, который Step 5
  guided workflows используют как pre-condition.
  После Phase 5 / Step 5 у продуктового слоя есть и
  **guided workflow layer**: единая boundary-функция
  `run_guided_workflow(...)` поверх трёх готовых сценариев
  — `safe-add-attribute` (через
  `add_catalog_attribute` / `add_document_attribute` +
  `verify_attribute_exists`), `safe-add-module-method`
  (через `append_module_method` + `verify_module_contains`)
  и `stand-health-check` (read-only diagnostic). Каждый
  mutating workflow строит план через intelligence
  (`estimate_change_impact`, `suggest_safe_change_order`,
  `suggest_metadata_patch_plan`), показывает оператору и
  **не исполняется без `confirm_execute=True`**;
  фактическое mutating-исполнение идёт через существующие
  public write-tool'ы, которые сами проходят через
  `run_write_flow` (preflight → snapshot → operation →
  verify → audit). Никакого silent apply, никакого
  обхода audit/snapshots. После Phase 5 / Step 6 у
  продуктового слоя есть и **rollback / recovery / audit
  UX**: три read-only boundary-функции
  (`get_operation_history`, `inspect_operation`,
  `run_rollback_assistant`), которые работают над уже
  существующим audit JSONL и `prepare_rollback_hint`
  / `describe_last_write_operation`. Assistant строит
  preview всегда (даже на degraded окружении); на
  `confirm_execute=True` он либо `mode=blocked` (если
  dashboard не ready), либо `mode=unsupported` (если для
  этого write-tool family нет supported automatic recovery
  path). На Step 6 supported automatic recovery whitelist
  пуст: автоматический content-level rollback не
  ship'ится без публичных `delete_*` write-tool'ов —
  product layer не делает back-door write channel в
  dump. Operator получает honest operator summary +
  snapshot paths и решает сам. После Phase 5 / Step 7
  у продуктового слоя есть и **real-stand / 1cv8
  binary integration track**: новый optional contract
  в `onec-config` (`onec_binary_path` /
  `onec_binary_probe_args`), две boundary-функции
  (`get_real_stand_readiness`, `run_real_stand_smoke_test`),
  reference stand spec в README продуктового слоя, и
  **настоящий** controlled smoke test: на
  `confirm_execute=True` с готовым окружением platform
  стартует реальный subprocess через `onec_process_runner`
  с operator-declared argv (cap timeout 30s, output
  excerpts обрезаны до 1024 chars). Phase 2 stub'ы
  (`create_dump_snapshot` / `apply_config_from_files` /
  `update_database_configuration`) на Step 7 **не**
  переписываются — это параллельный track. Никаких новых
  MCP tool'ов; никакого back-door write channel в
  infobase; никакого 1cv8-CLI guessing — оператор
  владеет probe args. **Step 8** — final integration
  pass — пройден без правок кода: один сквозной
  Scenario A через bootstrap → runtime → dashboard →
  guided workflow → recovery UX → real-stand smoke
  отработал out-of-the-box на synthetic-окружении
  (реальный стенд не трогался). Failure paths —
  workflow blocked by dashboard, rollback assistant
  unsupported, broken JSON config, malformed audit
  line — все деградировали честно без единого
  исключения наружу. Registry'ы read=15 / write=23 /
  intelligence=16 не менялись; `onec_policy_engine` не
  импортируется ни в product layer, ни в
  intelligence-server. **Phase 5 закрыт**.
- **Phase 6** — **закрыта на Step 9 — final integration pass**.
  **Industrialization & Completion Track**: специально
  выделенная фаза доведения продукта до finished /
  deployable состояния. После **Step 2** у платформы
  есть первый честный binary-backed slice:
  `create_dump_snapshot` теперь имеет два режима —
  classic **stub** (backward-compat default) и
  **binary-backed** (включается, когда оператор задал
  оба поля `EnvironmentConfig.onec_binary_path` +
  `EnvironmentConfig.onec_dumpcfg_command_template`).
  Платформа **не угадывает** 1cv8 CLI grammar:
  оператор пишет полный argv-template с whitelisted
  placeholder'ами (`{binary_path}` / `{output_path}` /
  `{base_path}` / `{base_id}` / `{publication_name}` /
  `{http_base_url}`); render — безопасный
  `str.format_map` с fail-closed на unknown
  placeholder; subprocess идёт через
  `onec_process_runner` с timeout 300 s; captured
  output обрезан до 1024 chars; runtime failure
  binary-backed subprocess'а **не** падает в silent
  fallback на stub — только config-time развилка.
  Phase 2 stub'ы `apply_config_from_files` и
  `update_database_configuration` на Step 2 **не**
  тронуты — это первый partial slice
  Industrialization Track, не полная замена. После
  **Step 3** в `apps/platform/onec_platform` появился
  install / setup fast path: read-only
  `inspect_release_layout`, declarative
  `build_product_config_template`, и главный boundary
  `run_install_fast_path(data, *, output_config_path,
  confirm_write)` с двумя режимами (preview / executed)
  и одним fail-closed (`rejected`). Helper материализует
  JSON product-config атомарно (`*.tmp` + `os.replace`),
  отказывается перезаписывать существующий файл, и
  после записи делает round-trip
  `bootstrap_product_from_json_file` для подтверждения
  читаемости. Это **не** GUI installer и **не** release
  packaging ecosystem — это product-layer fast path,
  который сокращает manual install ritual до ≤ 5
  ручных шагов; helper не запускает MCP-серверы, не
  модифицирует инфобазу, не вызывает write-tool'ы.
  После **Step 4** платформа получила первый
  **исполняемый rollback path**: `_AUTOMATIC_RECOVERY_SUPPORTED`
  переехал из пустого frozenset'а в whitelist из ровно двух
  tool'ов — `add_catalog_attribute` и `add_document_attribute`,
  то есть объектов, чьё содержание полностью описывается одним
  XML-файлом и обратимо ровно копированием snapshot-копии этого
  файла. Чтобы это сделать честно, в audit запись добавлен
  optional `details` dict (`operation_name`, `rollback_supported`,
  `backup_snapshot_path`, `dump_snapshot_path`, `relative_path`);
  pre-Step-4 строки **байт-идентичны** (`details=None` явно
  вырезается из JSON). В write-server registry добавлен ровно
  один новый mutating tool —
  **`restore_dump_file_from_snapshot(environment, relative_path,
  snapshot_file_path, label)`** — single-file restore, отвергающий
  абсолютные пути и `..` сегменты fail-closed, идущий через тот
  же `run_write_flow` (preflight + snapshot + operation + verify
  + audit), что и forward write. Recovery-ассистент в
  product-layer'е (`run_rollback_assistant`) на
  `confirm_execute=True` для whitelisted tool'а с healthy
  dashboard'ом теперь возвращает `mode='executed'` и
  ответственно вызывает этот public write-tool — никаких
  back-door filesystem write'ов из продуктового слоя по-прежнему
  нет; rollback наследует policy / preflight / snapshot / verify /
  audit дисциплину «настоящего» write'а. Сразу после рестора
  ассистент делает обязательный post-rollback verify через
  существующий read-only `diff_dump_fragment` и считает успехом
  только сочетание `restore.ok=True` AND
  `diff.data.changed=False`. Whitelist умышленно остался узким:
  расширять его — отдельные шаги Phase 6, не Step 4. Registry'ы
  read=15 / write=**24** (был 23) / intelligence=16; Phase 4
  intelligence-server остаётся read-only по конструкции.
  После **Step 5** платформа получила первый честный
  **structural XML edit slice**: добавлен один новый public
  mutating tool **`add_form_attribute(environment, object_name,
  form_name, attribute_spec, label)`**, идущий строго через
  `run_write_flow` и редактирующий XML-карту через
  `xml.etree.ElementTree`, а не через substring/`rfind`
  патчинг. В internal helper layer
  (`runtime/metadata_ops.py`) появились шесть DOM-style
  helper'ов на stdlib (`parse_xml_file`, `write_xml_file`,
  `find_form_element`, `get_or_create_form_attributes_block`,
  `add_attribute_to_form_attributes_block`,
  `form_has_attribute`); если у формы ещё нет блока
  `<Attributes>`, tool создаёт его structurally, а не падает
  и не делает rfind-fallback'а. Существующий public
  dispatcher `verify_metadata_change(...)` получил одну
  новую read-only ветку `kind="form_attribute_exists"` —
  без нового standalone verify-tool'а, чтобы public surface
  оставалась узкой. `add_catalog_attribute` /
  `add_document_attribute` намеренно **не** переписаны на
  DOM-edit на этом шаге — Step 5 ship'ит structural edit
  точечно, не sweep'ом. Registry'ы read=15 / write=**25**
  (был 24) / intelligence=16. После **Step 6** платформа
  получила первый честный slice **runtime hardening**
  поверх existing Phase 5 / Step 3 runtime contract:
  каждый long-lived product service теперь логирует
  `stdout` / `stderr` в файлы под
  `<work_dir>/.runtime/logs/<service>.{out,err}.log`
  (вместо старого безусловного `DEVNULL`); добавлена
  rotate-if-exceeds-size в одно поколение (`.1`-файл) с
  настраиваемым `log_max_bytes` (default 1 MiB);
  введена узкая `restart_policy ∈ {"never",
  "restart-if-stale"}` (default `"never"`), причём
  `"restart-if-stale"` срабатывает **только** на
  boundary-вызовах `start` / `reload` / `status` — нет
  никакого фонового watcher'а, нет timer-loop'а, нет
  daemon-supervisor'а; persisted `runtime-state.json`
  расширен (schema bumped 1 → 2) полями
  `restart_policy` / `restart_attempts` /
  `last_exit_code` / `stdout_log_path` /
  `stderr_log_path` / `last_started_at` /
  `last_stopped_at`, при этом reader honestly
  читает schema=1 файлы с дефолтами; новые findings
  `runtime_log_paths:<svc>` /
  `runtime_log_rotated:<svc>` /
  `runtime_log_dir_failed:<svc>` /
  `runtime_restart_attempted:<svc>` /
  `runtime_restart_succeeded:<svc>` /
  `runtime_restart_failed:<svc>` поднимают
  происходящее в operator-readable форму. Никаких
  новых MCP tool'ов: registry'ы read=15 / write=25 /
  intelligence=16 не изменены. Это **не** Windows
  Service / systemd integration, **не** hot reload,
  **не** journald / log aggregation — большие куски
  явно вынесены за пределы Phase 6. **Step 7** прошёл
  как **documentation-only**: одно сквозное
  Scenario A (bootstrap → install fast path → start →
  status → dashboard → safe-add-attribute mutating
  workflow → history → inspect → executed rollback →
  post-rollback verify → readiness → smoke → stop) +
  пять honest failure paths (workflow blocked,
  rollback unsupported, broken JSON, malformed audit
  lines, smoke non-zero exit) **прошли без единой
  кодовой правки** на synthetic стенде. Кnowledge,
  которое ранее распухало по READMEам, вынесено в
  четыре standalone-документа: `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md`.
  Registry-инвариант сохранён ровно: read=15 /
  write=25 / intelligence=16. После **Step 8**
  платформа получила узкий **enterprise foundation
  slice**: добавлена одна optional product-config
  секция `enterprise` (`deployment_tier ∈
  {"dev","test","stage","prod-like"}`, `instance_id`,
  `config_owner`, `change_control_required`,
  `require_operator_identity`, `runbook_reference`)
  и один новый read-only product-layer boundary
  `inspect_enterprise_foundation(...)` /
  `inspect_enterprise_foundation_from_json_file(...)`,
  который детерминистически проверяет четыре секции
  (identity, operability, traceability, binary
  contract) и возвращает `foundation_level ∈
  {"absent","minimal","partial","strong"}` плюс
  отдельный `ready_for_enterprise_track: bool`. Это
  **foundation verdict**, не enterprise-readiness
  verdict — платформа отвечает за «есть ли опора под
  следующий enterprise шаг», не за «можно ли это
  везти в prod». Step 1–7 конфиги без секции
  продолжают грузиться; loader строго валидирует
  shape; `build_product_config_template(...)` принял
  шесть новых optional kwargs и эмитит
  enterprise-блок ровно когда хотя бы один из них
  передан. Никаких новых MCP tool'ов: registry'ы
  read=15 / write=25 / intelligence=16 не изменены.
  Это **не** SSO/RBAC, **не** multi-tenant, **не**
  secrets vault, **не** policy-as-code, **не**
  federated audit storage — всё это явно вынесено за
  Phase 6 в parallel enterprise track. **Step 9** —
  final integration pass Phase 6 — пройден: один
  связный Scenario A (16 шагов от bootstrap до stop,
  через каждый Phase 6 slice по очереди — install
  fast path, runtime layer с реальным subprocess,
  dashboard, два mutating workflow'а через
  `run_write_flow` с **подтверждённой binary-backed**
  `create_dump_snapshot` (snapshot-директория
  физически содержит скопированный
  `Catalogs/SampleCatalog.xml`, доказательство, что
  это именно binary-backed mode, а не stub),
  history → inspect → executed rollback на
  whitelisted op'е → структурный post-rollback
  verify через ElementTree + byte-equal с pre-add
  baseline'ом, real-stand smoke с реальным
  subprocess'ом, enterprise-foundation inspection
  (`foundation_level='strong',
  ready_for_enterprise_track=True`), stop runtime с
  реально умирающим PID'ом, проверка наличия
  `<work_dir>/.runtime/logs/<svc>.{out,err}.log` на
  диске). Шесть honest failure paths (workflow
  blocked, rollback unsupported для
  `add_form_attribute`, broken JSON через девять
  `_from_json_file` boundary'ев включая Step 8
  enterprise-foundation entry, smoke с реальным
  non-zero exit, enterprise foundation weak/minimal
  на prod-like без identity / binary contract,
  binary-backed dump snapshot с non-zero subprocess
  exit'ом без silent stub fallback'а). Discipline
  asserts: registries pre/post `read=15 / write=25 /
  intelligence=16` без drift'а; 0 import'ов
  `onec_policy_engine` под `apps/platform/src` и
  `apps/mcp-intelligence-server/src`; 14
  suggested-tool / suggested-write-tool lists, все
  имена реальные; ни одно boundary не raise'нуло
  наружу. Кодовых правок на Step 9 — **две
  минимальные**: добавлен один тонкий guided-wrapper
  `safe-add-form-attribute` (Step 5 shipped public
  `add_form_attribute` без guided-обёртки, без неё
  brief'овский «`run_guided_workflow` →
  `add_form_attribute`» был структурно невозможен)
  + закрыт реальный gap в
  `installer._config_to_dict`, который silently
  dropped Step 6 service-level поля и Step 8
  enterprise-блок при install fast path round-trip'е.
  Никаких новых MCP tool'ов; registries нетронуты.
  **Phase 6 закрыта.** Следующий шаг — это уже
  parallel / enterprise tracks ПОСЛЕ Phase 6 (см.
  список ниже); Phase 7 не начинается. Это **не**
  очередное расширение MCP tool surface — после
  Phase 1–5 ядро
  и product-layer контур уже есть; Phase 6 закрывает
  разрыв между «у нас сильное ядро + работающий
  product-layer контур» и «это можно установить,
  запустить, использовать, поддерживать и передать
  другому человеку как реальный индустриальный
  продукт». Шесть продуктовых блоков: real 1cv8
  binary-backed execution (точечно, для одного Phase 2
  stub-backed пути; остальные остаются follow-up'ом),
  full rollback / recovery (исполнимый хотя бы для
  одного класса), installer / packaging / setup
  short path (≤ 5 ручных шагов), metadata completion
  + первый шаг к structural editing, runtime
  hardening (логи, restart policy), operator / admin
  / developer manuals + runbooks как standalone
  docs, foundation для enterprise-трека (без полной
  enterprise-вселенной). Safety guarantees Phase 2–5
  сохраняются: `run_write_flow` остаётся единственным
  путём к mutating операциям; intelligence остаётся
  read-only; `onec_policy_engine` не импортируется;
  никакого back-door write channel в product layer.
  Закрытие Phase 6 не означает, что продукт стал
  полностью enterprise-ready — крупные хвосты
  (полная enterprise-поверхность, AST-парсер всей
  кодовой базы, web-UI, multi-instance HA, полный
  version-matrix smoke на всех 1С версиях) явно
  выносятся за пределы фазы.

Закрытые фазы:

- `docs/architecture/phase-0-summary.md` — итоги Phase 0.
- `docs/architecture/phase-1-entry.md`,
  `docs/architecture/phase-1-read-mvp-plan.md`,
  `docs/architecture/phase-1-step-map.md` — материалы Phase 1.
- `docs/architecture/phase-2-write-mvp-plan.md`,
  `docs/architecture/phase-2-step-map.md` — материалы Phase 2.
- `docs/architecture/phase-3-metadata-changes-plan.md`,
  `docs/architecture/phase-3-step-map.md` — материалы Phase 3.
- `docs/architecture/phase-4-intelligence-plan.md` — план
  Phase 4: стартовый набор intelligence-инструментов по группам
  A/B/C/D, guardrails, критерии приёмки.
- `docs/architecture/phase-4-step-map.md` — implementation map
  (7 шагов). Phase 4 закрыта на Step 7.
- `docs/architecture/phase-5-product-layer-plan.md` — план
  Phase 5: назначение, целевой результат, шесть продуктовых
  блоков (A–F), 16+ продуктовых capability'ов, guardrails,
  критерии приёмки, явный список того, что **не** входит в
  фазу.
- `docs/architecture/phase-5-step-map.md` — implementation
  map (8 шагов): product contract → installer → runner →
  doctor → workflows → rollback/recovery → real-stand →
  final integration pass. Phase 5 закрыта на Step 8.
- `docs/architecture/phase-6-industrialization-plan.md` —
  план **Phase 6 — Industrialization & Completion Track**:
  узкий honest set из шести продуктовых блоков
  (A real 1cv8 execution; B full rollback / recovery;
  C installer / packaging; D metadata completion /
  structural editing; E runtime hardening;
  F operator UX / docs / runbooks; G enterprise
  foundation). 10 проверяемых критериев приёмки. Явный
  «что НЕ входит в фазу». Phase 6 закрыта на Step 9
  (final integration pass) — see `apps/platform/README.md`
  раздел «Phase 6 закрыта» для подробного списка того,
  что закрыто честно, и того, что осталось как parallel
  / enterprise tracks после Phase 6.

Активных фаз нет. Следующие шаги — parallel / enterprise
tracks **после** Phase 6 (полный enterprise super-set,
полное замещение всех Phase 2 stub'ов одновременно,
полное rollback покрытие, AST-парсер, web-UI, full
version-matrix smoke, etc.). Phase 7 как отдельная
интеграционная фаза не запланирована — крупные новые
направления входят как параллельные track'и, а не как
ещё один линейный MVP.

## Closed parallel tracks

После закрытия Phase 6 были последовательно открыты и
закрыты девять post-phase completion track'ов:

- **Parallel Track A — Full Real 1cv8-backed Write Path** —
  закрыт на Step 7 (final integration pass and Track A
  closure).
- **Parallel Track B — Productization & Delivery Polish** —
  закрыт на Step 6 (final integration pass and Track B
  closure).
- **Parallel Track C — Packaging & Installer Delivery** —
  закрыт на Step 6 (final integration pass and Track C
  closure).
- **Parallel Track D — Operator Credentials Hardening** —
  закрыт на Step 6 (final integration pass and Track D
  closure).
- **Parallel Track E — Multi-Version 1C Smoke Matrix** —
  закрыт на Step 6 (final integration pass and Track E
  closure).
- **Parallel Track F — Rollback Whitelist Expansion** —
  закрыт на Step 6 (final integration pass and Track F
  closure).
- **Parallel Track G — Production-Grade MCP Transport and
  CLI** — закрыт на Step 6 (final integration pass and
  Track G closure).
- **Parallel Track H — Network-Grade MCP Transport and
  Authentication Boundary** — закрыт на Step 6 (final
  integration pass and Track H closure).
- **Parallel Track I — Installer Auth Round-Trip
  Integrity** — закрыт на Step 6 (final integration pass
  and Track I closure).

## Active parallel track

Активного трека сейчас нет. Девять post-phase parallel
track'ов (A, B, C, D, E, F, G, H, I) закрыты последовательно;
Phase 7 как линейная фаза не запланирована. Открытие
следующего параллельного трека — отдельное operator
decision. Подробности по последнему закрытому треку — в
секции «Track I detail (закрыт)» ниже; предыдущий трек
описан в «Track H detail (закрыт)».

## Track I detail (закрыт)

**Цель Track I** была — закрыть один honest gap, явно
зафиксированный в Track H closure narrative:
`apps/platform/src/onec_platform/installer.py:_config_to_dict`
не emit'ил новый `auth` section, поэтому config round-tripped
через `scripts/release/install.ps1 ... -Confirm` silently
терял declarations `auth.tokens`. Operator получал clean
fail-closed startup ("`--transport http requires
--auth-token-env or auth.tokens in product config`"), что
было не silent insecure success (Track H §10.6 fail-closed
gate работал корректно), но silent configuration data loss,
ломающий declarative round-trip guarantee, на которую
полагаются другие installer paths (existing `enterprise`
block + `runtime.services[*]` Phase 6/Step 6 service-level
fields — оба honored emit-only-when-divergent pattern'ом).
Track I восстановил preservation symmetric к существующему
Phase 6 / Step 8 enterprise-block pattern. Это **не**
redesign `ProductAuthSettings` schema, **не** changes к
`_parse_auth` validation, **не** changes к
`_network_transport.py` auth resolution, **не** introduction
secret storage / vault / KMS / OS keychain, **не** packaging
ecosystem (`.msi` / `.deb` / signed distribution / PyPI
publication / wheel publication beyond existing
`[project.scripts]` declarations), **не** service supervision
(systemd / Windows Service / hot reload / supervisor daemon),
**не** network hardening (TLS-in-process / mTLS / new
transport family), **не** enterprise identity stack
(SSO / OIDC / RBAC / multi-tenant), **не** standalone
`apps/platform` entrypoint, **не** новые MCP tools (registry
invariant `read=15 / write=25 / intelligence=16` carried
through unchanged). Платформа архитектурно осталась при том
же подходе: existing Track G + Track H artefacts (3
`__main__.py` entrypoints, `_stdio_transport.py` helper,
`_network_transport.py` helper, `[project.scripts]` block,
`ProductAuthSettings` dataclass, `_parse_auth` loader,
`_AUTH_ENV_TOKEN_RE` regex, `Authorization` header parsing
+ case-insensitive scheme + `hmac.compare_digest` validation
+ failure-equivalence rule + complete redaction discipline)
preserved byte-identical; Track I ship'ил **только narrow
installer.py extension** (+15 / -0 LOC, single emit branch).
Шесть шагов; production-код Track I правил **только Step 4
commit** и **только** в `installer.py:_config_to_dict`.

- **Step 1 (planning, docs-only, commit `cb79597`)** — два
  planning-документа
  ([`docs/architecture/track-i-installer-auth-round-trip-integrity-plan.md`](docs/architecture/track-i-installer-auth-round-trip-integrity-plan.md),
  [`track-i-...-step-map.md`](docs/architecture/track-i-installer-auth-round-trip-integrity-step-map.md)):
  назначение трека, целевой результат, что закрывает /
  не закрывает Track I, отличия от Tracks A–H, guardrails,
  acceptance criteria, открытые вопросы Q1–Q7. Никакого
  code change.
- **Step 2 (installer round-trip baseline audit, docs-only,
  commit `e7d9973`)** — новый descriptive audit-документ
  [`track-i-installer-auth-round-trip-baseline-audit.md`](docs/architecture/track-i-installer-auth-round-trip-baseline-audit.md)
  (889 lines, 12 sections); per-section `_config_to_dict`
  inventory (9 logical sections); 4-class breakdown
  идентифицировал `auth` как единственный CLASS-3 gap;
  resolved Q1 (`installer.py` only — verified by Phase
  6/Step 6 service-level + Phase 6/Step 8 enterprise
  single-file precedents), Q2 (5 preservation rules с
  file/line anchors), Q3 (11 forbidden sub-rules с Track H
  contract + observed-evidence anchors).
- **Step 3 (auth round-trip preservation contract,
  docs-only, commit `525c611`)** — новый prescriptive
  normative document
  [`track-i-installer-auth-round-trip-contract.md`](docs/architecture/track-i-installer-auth-round-trip-contract.md)
  (843 lines, 118 RFC 2119 keyword usages: 78 MUST, 32
  MUST NOT, 4 SHOULD, 3 MAY, 1 SHALL); 11 sections
  pinning round-trip integrity definition, exact emit-
  branch placement (after `enterprise_block` attach at
  l.314, before `return out`), exact accumulator-and-
  conditional-attach shape, list-copying discipline,
  raw `${ENV:NAME}` byte-identical preservation, no env-
  resolution-at-install-time rule, exact Step 4 allowed/
  forbidden file surfaces, verification protocol (6
  positive checks + 6 negative checks + 4 insufficient-
  verification exclusions + no-real-MCP-client-gate
  carry-over), 15 honest non-goals each followed by "No
  ..." denial clauses, 8-precondition + 11-prohibition
  Step 4 handoff note.
- **Step 4 (narrow installer auth round-trip
  implementation, единственный шаг с production code
  change, commit `d047a6d`)** — 1 file modified, +15/-0
  LOC. Additive emit branch в `installer.py:_config_to_dict`
  между existing `enterprise_block` attach (l.314) и
  `return out`:

  ```python
  auth_block: dict[str, Any] = {}
  if config.auth.tokens:
      auth_block["tokens"] = list(config.auth.tokens)
  if auth_block:
      out["auth"] = auth_block
  ```

  Comment block описывает Track I provenance + raw
  `${ENV:NAME}` preservation rule + resolution boundary
  в `_network_transport.py`. **No new imports** (`Any`
  already imported at l.33 per Step 3 §7.3 default-zero);
  **no edits в existing 8 emit branches** (per §7.1
  byte-identical preservation); **no helper extraction**
  / no refactor / no cleanup churn. Verification: 14/14
  PASS через одноразовый `.tmp_track_i_smoke.py` smoke
  harness (deleted pre-commit) — multi-token round-trip
  preserved с order; single-token round-trip; empty/
  default no-injection across 3 cases; pre-Track-H
  reload defaults to empty; token order positionally
  preserved; raw `${ENV:NAME}` byte-for-byte preserved
  WITHOUT populating os.environ; no env resolution at
  install time (probe value `should-never-appear-in-
  projection` set в os.environ → never appears в
  projected JSON); literal cleartext rejected fail-
  closed by `loader._parse_auth` upstream; end-to-end
  install fast-path executed-mode real-IO round-trip
  preserves `auth.tokens` element-wise.
- **Step 5 (operator docs and installer auth alignment,
  docs-only, commit `2e9e0b8`)** — narrow alignment
  под фактический Step 4 fix state; 3 files +185/-84:
  `SECURITY.md` (single bullet "Known limitation in
  install fast path round-trip" → "Install fast path
  auth round-trip preserved (Track I / Step 4)");
  `docs/release-handoff.md` (2 locations: "What is NOT
  in this handoff" bullet + "Known limitations"
  pointer); `README.md` (Quickstart paragraph + "Active
  parallel track" section enumerating Steps 1-4 closure
  summary). Drift inventory classified 8 candidates: 3
  CLASS-1 (touched), 3 CLASS-2 (apps/platform/README.md
  + scripts/dev/launch.ps1 + scripts/dev/README.md —
  qualitatively still accurate, no gap mention), 2
  CLASS-3 (PROJECT-STATUS.md + CHANGELOG.md — closure
  narrative territory).
- **Step 6 (final integration pass and Track I closure,
  этот closure)** — `pyproject.toml` version bumped
  `0.5.0` → `0.5.1` (Q6 = PATCH; см. ниже); README +
  PROJECT-STATUS + CHANGELOG обновлены под Track I
  closed.

**Q6 resolution = PATCH (NOT MINOR).** Track I — defect-
class round-trip integrity fix, не feature delta:

- Step 4 commit (`d047a6d`) изменил `+15 / -0` LOC в
  одной функции (`installer.py:_config_to_dict`),
  symmetric к существующему Phase 6 / Step 8
  `enterprise_block` pattern, который в `_config_to_dict`
  с момента Phase 6.
- **No new public API surface.** `ProductAuthSettings` и
  `ProductConfig.auth` уже существовали (Track H Step 4 в
  version 0.5.0). Track I добавил zero new public types,
  zero new functions, zero new module imports, zero new
  CLI flags, zero new MCP tools, zero changes to
  `mcp_common/__init__.py` `__all__`, zero changes to
  `[project.scripts]`.
- **No new runtime capability.** Operators using
  `--transport http` уже имели два рабочих пути pre-Track-I:
  declare `auth.tokens` в source config (worked unless
  они round-trip'ят через install fast-path), либо use
  `--auth-token-env` CLI override. Track I closed silent
  data-loss bug в install fast-path materialization,
  который operators обходили. Net-new capability нет;
  есть previously-broken round-trip, который теперь
  работает.
- **SemVer prior precedent comparison.** Track D
  `0.1.0 → 0.2.0` (env-substitution + verify-release Check
  8 — added 50+ LOC of new credential-resolution logic +
  new release-side check). Track F `0.2.0 → 0.3.0`
  (whitelist 2→6 entries — meaningful runtime-reachable
  rollback capability for 4 new tool families). Track G
  `0.3.0 → 0.4.0` (3 new `__main__.py` + 245-LOC
  `_stdio_transport.py` + new `[project.scripts]` block —
  net-new runnable surface). Track H `0.4.0 → 0.5.0`
  (549-LOC `_network_transport.py` + new HTTP/`/mcp`
  endpoint + bearer auth + new CLI flags — net-new
  transport family). Each of D/F/G/H added a recognizable
  new external capability. **Track I does not.** It
  restores integrity of a flow that should have always
  preserved this section.
- **Per Keep-a-Changelog conventions and SemVer §6**, "Bug
  fixes" → PATCH. Track I plan §10 Q6 explicitly framed
  PATCH `0.5.1` как «alternative path только if Step 4
  diff truly tiny and framing honest as defect-fix»; Step
  4 diff был 15 LOC (well within "truly tiny"); fix —
  genuinely defect-class round-trip integrity repair.

После Track I closure фактически работает:

```powershell
# Operator declares config с auth section
.\scripts\release\install.ps1 `
    -ConfigPath input.config.json `
    -OutputConfigPath out.config.json `
    -Confirm
# Materialised out.config.json теперь содержит
# "auth": {"tokens": ["${ENV:MCP_TOKEN}"]}
# byte-identical к source (raw env-substitution form
# preserved as configuration data; no env resolution
# at install time)
```

Что Track I **реально закрыл** (на основе Steps 1–5
deliverables):

- installer auth round-trip integrity — `_config_to_dict`
  теперь preserves `config.auth.tokens` через install
  fast-path materialization round-trip byte-identical к
  source list (operator's declared `${ENV:NAME}` strings
  round-trip как configuration data, не resolved env
  values);
- backward compatibility — pre-Track-H configs (без
  `auth` section) round-trip byte-identical (no implicit
  `"auth": {}` injection); existing 8 emit branches в
  `_config_to_dict` byte-identical; Track H auth/runtime
  surfaces (`ProductAuthSettings`, `ProductConfig.auth`,
  `_parse_auth`, `_AUTH_ENV_TOKEN_RE`,
  `_network_transport.py`, `_stdio_transport.py`, three
  `__main__.py`, `mcp_common/__init__.py` `__all__`)
  byte-identical;
- two new architecture docs (descriptive baseline audit
  + RFC 2119 normative contract) + plan + step-map = 4
  Track I architecture docs;
- aligned operator-facing docs (`SECURITY.md`,
  `docs/release-handoff.md`, `README.md`) — все говорят
  one truth: post-Step-4 fix preserved auth round-trip;
  broader installer / packaging / deployment ecosystem
  limitations carry forward;
- registries invariant `read=15 / write=25 /
  intelligence=16` carried through unchanged;
  `mcp_common` public API export'ы preserved
  byte-identical.

Что Track I **не делает** «installer ecosystem solved»
после closure (honest constraints, никаких скрытых
гэпов):

- никакого full installer ecosystem (`.msi` / `.deb` /
  signed binary distribution / GUI installer / wizard /
  PyPI publication / wheel publication beyond existing
  `[project.scripts]` declarations); Track C wheel-build
  empty constraint preserved;
- никакого secret storage / vault / KMS / HashiCorp Vault
  / AWS Secrets Manager / OS keychain integration;
- никакого env-var resolution at install time (это design
  invariant, не gap — resolution остаётся
  `_network_transport._resolve_env_token` runtime
  boundary);
- никакого Track H auth model changes (bearer / case-
  insensitive scheme / constant-time compare / failure-
  equivalence rule preserved byte-identical);
- никакого new transport / network / TLS / mTLS / OAuth
  / JWT / OIDC / SAML / SCIM / RBAC / multi-tenant /
  sessions / rate limiting / token rotation /
  refresh tokens;
- никакого supervisor daemon / systemd unit / Windows
  Service registration / `launchd` plist / hot reload /
  restart watcher / auto-update / orchestration
  templates / HA / clustering / load balancing;
- никакого web UI / dashboard frontend;
- никакого distributed tracing / observability stack
  (OpenTelemetry / Jaeger / Prometheus / OpenMetrics);
- никакого standalone `apps/platform` entrypoint
  (carry-over out-of-scope from Tracks G/H);
- никаких новых MCP tools (registry invariant
  preserved);
- никаких 1cv8.exe runs ни на одном шаге Track I —
  трек работает на install/materialization layer уровне,
  не на 1cv8 binary surface;
- никакого deployment perimeter беyond Track H trusted-
  network behind operator-owned reverse proxy;
- никакого enterprise-ready / hostile-network-ready
  posture claim;
- никакого real MCP client integration test (Claude
  Desktop, MCP CLI launching server) **не** часть Track
  I closure gate — recommended но не blocker (carry-over
  Track G/H pattern).

Registry-инвариант сохранён точно на всём треке: `read=15
/ write=25 / intelligence=16`, `selfcheck_status=ok`.
Никаких реальных credentials ни в одном из шести Track I
commit'ов (Step 4 smoke harness использовал abstract
`${ENV:MCP_TOKEN_*}` test placeholders + ephemeral non-
secret canary string `"should-never-appear-in-projection"`
inside the deleted harness; nothing committed). Никаких
1cv8.exe runs ни на одном шаге Track I. **GitHub remote
push** не часть Track I — repo готов к выкладке, но
пушить — operator action.

Документы трека:
[`track-i-installer-auth-round-trip-integrity-plan.md`](docs/architecture/track-i-installer-auth-round-trip-integrity-plan.md),
[`track-i-installer-auth-round-trip-integrity-step-map.md`](docs/architecture/track-i-installer-auth-round-trip-integrity-step-map.md),
[`track-i-installer-auth-round-trip-baseline-audit.md`](docs/architecture/track-i-installer-auth-round-trip-baseline-audit.md),
[`track-i-installer-auth-round-trip-contract.md`](docs/architecture/track-i-installer-auth-round-trip-contract.md).

## Track H detail (закрыт)

**Цель Track H** была — ship'ить **второй слой зрелости**
поверх Track G: добавить один network-facing MCP transport
family и один minimum authentication baseline, additive
над existing local stdio surface (Track G `python -m
<server> --transport stdio` остаётся supported byte-
identically). Это **не** universal enterprise deployment
platform, **не** full identity stack (SSO / SAML / OIDC
federation / SCIM / organizational RBAC / multi-tenant
policy), **не** zero-trust mesh (mTLS-everywhere / service
mesh / KMS / vault как mandatory baseline), **не** web UI
/ dashboard frontend, **не** packaging ecosystem (`.msi`
/ `.deb` / signed distribution / PyPI publication / wheel
publication beyond existing `[project.scripts]`
declarations), **не** service management ecosystem
(systemd unit / Windows Service registration / `launchd`
plist / auto-update / HA / clustering / load balancing /
hot reload / supervisor daemon с restart watcher), **не**
standalone `apps/platform` entrypoint (carry-over
out-of-scope from Track G Q6), **не** новые MCP tools
(registry invariant `read=15 / write=25 / intelligence=16`
carried through unchanged). Платформа архитектурно
осталась при том же подходе: existing
`server.py:REGISTERED_TOOLS` registries для всех 3 MCP
servers preserved byte-identical (`list_tools()` /
`get_tool(name)` API без изменений); Track H ship'ил
**дополнительный transport / auth layer поверх** этих
registries, не задевая их; existing Track G artefacts
(3 `__main__.py` entrypoints, `_stdio_transport.py`
helper, `[project.scripts]` block) preserved. Шесть шагов
+ один Step 2 follow-up; production-код Track H правил
**только Step 4 commit** и **только** на explicit allowed
surfaces (1 new private helper + 3 modified
`__main__.py` + 2 modified `apps/platform` files).

- **Step 1 (planning, docs-only, commit `563b27b`)** —
  два planning-документа
  ([`docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md),
  [`track-h-...-step-map.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md)):
  назначение трека, целевой результат, что закрывает /
  не закрывает Track H, отличия от Tracks A–G,
  guardrails, acceptance criteria, открытые вопросы Q1–Q7.
  Никакого code change.
- **Step 2 (transport / auth baseline audit, docs-only,
  commit `3c74564`)** — новый descriptive audit-документ
  [`track-h-transport-and-auth-baseline-audit.md`](docs/architecture/track-h-transport-and-auth-baseline-audit.md)
  (1085 lines, 11 sections): per-server / per-package /
  per-pyproject inventory current state + 4-class
  breakdown (11 reusable / 8 adjacent / 11 missing / 12
  out-of-scope) + read-only evidence (zero hits across 8
  grep categories — HTTP server libs, SSE, WebSocket,
  TCP, TLS, auth, sessions, rate-limit). Resolved Q1
  (HTTP-based MCP transport), Q2 (exactly one transport
  family), Q3 (static bearer token via Authorization
  header, constant-time compare, fail-closed), Q4
  (`ProductConfig.auth.tokens` + Track D `${ENV:NAME}`
  pattern + `--auth-token-env` CLI override).
- **Step 2 follow-up (commit `0628f4c`)** — narrow
  one-file fix removing literal credential-leak-guard
  pattern strings from the audit doc that were
  triggering `verify-release.ps1` Check 7 self-match
  after the doc became tracked. The same self-reference
  hazard is already handled for the script and its
  README via the script's `$excludes` list; the audit
  doc fell into the same trap on tracked-state. Fix
  paraphrased the strings without weakening the audit's
  meaning; touched only `scripts/release/verify-release.ps1`
  was deliberately avoided (that would be Track H docs
  follow-up scope creep).
- **Step 3 (network transport / auth contract, docs-only,
  commit `2e76061`)** — новый prescriptive normative
  document
  [`track-h-network-transport-and-auth-contract.md`](docs/architecture/track-h-network-transport-and-auth-contract.md)
  (1650 lines, 293 RFC 2119 keyword usages: 199 MUST,
  74 MUST NOT, 17 MAY, 2 SHOULD, 1 SHALL). 18 sections:
  purpose / inheritance / network transport contract
  (HTTP/1.1 ThreadingHTTPServer, single `/mcp` endpoint,
  POST only, `application/json`, 1 MiB body cap, SSE
  forbidden in Step 4 baseline) / MCP method coverage
  (same six methods as `_stdio_transport`) / JSON-RPC ↔
  HTTP boundary (per-failure-mode HTTP status + envelope
  pinned) / concurrency / auth (`Authorization: <case-
  insensitive-Bearer> <token>`, `hmac.compare_digest`,
  failure-equivalence rule, complete redaction
  discipline, exhaustive forbidden auth-shape list) /
  config schema / CLI surface / integration boundary /
  backward compatibility / TLS posture (in-process TLS
  forbidden; operator's reverse proxy responsibility) /
  pyproject posture / Step 4 implementation surface
  (allowed/forbidden file lists) / verification protocol
  / honest non-goals / Step 4 handoff note.
- **Step 4 (narrow HTTP transport and bearer auth boundary,
  единственный шаг Track H с production code change,
  commit `5814041`)** — PATH A. Ship'нуто 5 файлов
  (+877/-35; 1 new + 4 modified):
  - `packages/mcp-common/src/mcp_common/_network_transport.py`
    (новый, 549 LOC, underscore-prefixed private,
    **NOT** в `mcp_common/__init__.py` `__all__`,
    pure stdlib `http.server.ThreadingHTTPServer` +
    `hmac.compare_digest`); содержит handler для `/mcp`
    POST endpoint (GET → 405+`Allow: POST`; non-`/mcp`
    → 404; wrong Content-Type → 415+`-32600`; body >
    1 MiB → 413+`-32600`; multiple Authorization
    headers → 400+`-32600`; case-insensitive Bearer
    scheme; constant-time token compare; failure-
    equivalence 401+`WWW-Authenticate: Bearer
    realm="mcp"`+JSON-RPC `-32001` для missing / empty
    / malformed / invalid token; notifications → 204;
    complete redaction discipline); unified
    `run_main_http(...)` с одним argparser'ом для обоих
    transport'ов (stdio path делегирует в existing
    `_stdio_transport._serve_stdio` byte-identically).
  - 3 `__main__.py` (modified) — switched import
    `_stdio_transport.run_main` →
    `_network_transport.run_main_http`; `SERVER_VERSION`
    bumped 0.3.0→0.4.0; module docstrings updated;
    `main() -> int` signature preserved.
  - `apps/platform/src/onec_platform/models.py`
    (modified) — добавлен `ProductAuthSettings`
    dataclass с `tokens: list[str]` + `auth` field на
    `ProductConfig` с `default_factory`.
  - `apps/platform/src/onec_platform/loader.py`
    (modified) — `_AUTH_ENV_TOKEN_RE` regex byte-
    identical к Track D pattern; `_parse_auth(auth_raw)`
    с unknown-keys reject, list-of-strings validation,
    env-substitution regex enforce per entry, literal
    cleartext fail-closed at config-load time.

  Verification: 51/51 PASS через одноразовый smoke
  harness — per-server `--help` exits, HTTP startup
  negative tests (missing `--bind`, missing token
  source, unresolved env), per-server HTTP positive
  smoke (tools/list valid Bearer → 200 с правильным
  tool count 15/25/16), **byte-identical 401 fail-
  closed** (no-Authorization vs wrong-token дают
  identical status + headers + JSON envelope с
  `-32001`), case-insensitive scheme {`Bearer`, `bearer`,
  `BEARER`, `BeArEr`} × 3 servers, GET 405+`Allow: POST`,
  non-`/mcp` 404, malformed JSON 400+`-32700`, wrong
  Content-Type 415+`-32600`, unknown method 200+`-32601`,
  multiple Authorization 400+`-32600`, notification 204,
  `tools/call ping` 200, cross-transport parity
  (sorted stdio names == sorted http names).
- **Step 5 (operator docs and security alignment,
  docs-only, commit `407a2f2`)** — narrow alignment
  под фактический Step 4 surface; 6 files +410/-173:
  README.md (Quickstart + «Что Quickstart не обещает»
  + полный rewrite Active parallel track секции с
  Steps 1-4 closure summary), SECURITY.md (single-
  per-transport-block rewrite + exhaustive still-NOT
  list + installer auth-round-trip gap), docs/release-
  handoff.md (4 locations: «What is in this handoff» /
  «What is NOT» / launch parenthetical / Known
  limitations), apps/platform/README.md (4 locations:
  Phase 5/Step 3 callout + «Чего сейчас намеренно
  ещё нет» + 2 lower-section parallel lists), 
  scripts/dev/launch.ps1 (header comment + Show-Usage
  help text — both transports described; in-process
  TLS not provided framing), scripts/dev/README.md
  (per-transport launch.ps1 parenthetical).
  PROJECT-STATUS.md и CHANGELOG.md deliberately
  не тронуты (Step 6 closure territory).
- **Step 6 (final integration pass and Track H closure,
  этот closure)** — `pyproject.toml` version bumped
  `0.4.0` → `0.5.0` (Q7 = ДА; Step 4 ship'нул real
  production code change с **observable runtime
  capability delta** — `python -m <server>
  --transport http --bind ... --auth-token-env ...`
  теперь реально стартует HTTP/1.1 listener с bearer
  auth, что до Track H было невозможно; backward-
  compatible new functionality classifying as MINOR
  bump per SemVer; precedent — Track D `0.1.0 → 0.2.0`,
  Track F `0.2.0 → 0.3.0`, Track G `0.3.0 → 0.4.0`);
  README + PROJECT-STATUS + CHANGELOG обновлены под
  Track H closed.

После Track H closure фактически работают:

```powershell
python -m mcp_read_server --transport stdio --help
python -m mcp_read_server --transport http --bind 127.0.0.1:8765 --auth-token-env MCP_TOKEN --help
```

(и аналогично для двух остальных серверов). Каждый сервер
поддерживает оба transport'а через единый
`list_tools()` / `get_tool(name)` boundary; `run_write_flow`
discipline для write-tools и read-only-by-construction
discipline intelligence-сервера preserved unchanged на
обоих transport'ах. CLI surface: `--help`, `--config-path`,
`--transport {stdio,http}`, `--log-level
{DEBUG,INFO,WARNING,ERROR}`, `--bind <HOST>:<PORT>`,
`--auth-token-env <VARNAME>`. Token sources: либо
`ProductConfig.auth.tokens` (each entry MUST be
`${ENV:NAME}` env-substitution; literal cleartext rejected
at config-load), либо `--auth-token-env <VARNAME>` CLI
flag (CLI wins, replace not merge). Threat model =
trusted-local-stdio для `--transport stdio`; trusted-
network behind operator-owned reverse proxy для
`--transport http`. In-process TLS не предоставляется.

Что Track H **реально закрыл** (на основе Steps 1–5
deliverables):

- second transport family поверх existing `list_tools()`
  / `get_tool(name)` boundary — single HTTP/1.1 `/mcp`
  endpoint, POST only, `application/json`, 1 MiB body
  cap, single JSON-RPC message per body, ThreadingHTTPServer
  one-thread-per-request, daemon-thread Ctrl-C, stderr-
  only logging;
- minimum authentication boundary — static bearer token
  via `Authorization: <case-insensitive-Bearer> <token>`,
  byte-exact constant-time comparison via
  `hmac.compare_digest`, failure-equivalence rule
  (missing / empty / malformed / invalid → identical
  401), complete token redaction discipline (token value
  / length / prefix / suffix / hash / fingerprint MUST
  NOT appear anywhere);
- new `ProductConfig.auth.tokens` optional schema +
  `_parse_auth` loader validation (env-substitution
  regex enforcement; literal cleartext fail-closed at
  config-load);
- two new CLI flags (`--bind`, `--auth-token-env`) +
  extended `--transport` choice set (`{stdio,http}`);
- four track-H architecture docs (plan + step-map +
  baseline audit + RFC 2119 normative contract);
- aligned operator-facing docs (README, SECURITY,
  docs/release-handoff.md, apps/platform/README.md,
  scripts/dev/launch.ps1, scripts/dev/README.md);
- registries invariant `read=15 / write=25 /
  intelligence=16` carried through unchanged;
  `mcp_common` public API export'ы preserved
  byte-identical; `_stdio_transport.py` byte-identical;
  audit `details` shape preserved.

Что Track H **не делает** «hostile-network-ready
enterprise deployment» после closure (honest constraints,
никаких скрытых гэпов):

- никакого in-process TLS / HTTPS termination — operator
  обязан terminate TLS at a reverse proxy and bind the
  Track H listener to a loopback or private interface;
- никакого mTLS / client certificate authentication;
- никакого JWT / OAuth 2.0 / OIDC / SAML / SCIM —
  introspection, refresh tokens, rotation endpoints
  тоже out-of-scope;
- никакого RBAC / ABAC / per-token permissioning /
  per-tool ACL / per-tenant isolation / multi-tenant
  policy engine — single-tier auth (valid token →
  access full registry);
- никаких session cookies / rate limiting / quotas;
- никаких WebSocket / Server-Sent Events / TCP /
  Unix-socket / named-pipe transports;
- никакого supervisor daemon / systemd unit / Windows
  Service registration / `launchd` plist / Docker /
  Kubernetes deployment manifests / `supervisor` /
  `runit` / `s6` recipes / auto-update / orchestration
  templates / HA / clustering / load balancing / hot
  reload / background watchers;
- никакого distributed tracing / observability stack
  (OpenTelemetry / Jaeger / Prometheus / OpenMetrics);
- никакого web UI / dashboard frontend;
- никакого packaging ecosystem beyond
  `[project.scripts]` declarations (`.msi` / `.deb` /
  signed distribution / GUI installer / wizard / PyPI
  publication / wheel publication; wheel build по-
  прежнему пуст по Track C honest constraint);
- никакого standalone `apps/platform` entrypoint
  (carry-over out-of-scope from Track G Q6);
- никаких новых MCP tools (registry invariant
  preserved);
- никаких 1cv8.exe runs ни на одном шаге Track H —
  трек работает на process / transport / auth layer
  уровне, не на 1cv8 binary surface;
- known install fast path round-trip limitation:
  `apps/platform/src/onec_platform/installer.py:_config_to_dict`
  не emit'ит новый `auth` section, поэтому config
  round-tripped через `scripts/release/install.ps1 ...
  -Confirm` silently теряет declarations
  `auth.tokens` — operator получает clean fail-closed
  startup и либо re-add the section by hand либо use
  `--auth-token-env <VARNAME>` to bypass the config;
  future post-Track-H fix аналогичен Phase 6 / Step 9
  service-level + enterprise round-trip fix;
- real MCP client integration test (Claude Desktop,
  MCP CLI launching server) **не** часть Track H
  closure gate — recommended но не blocker (carry-over
  Track G pattern).

Registry-инвариант сохранён точно на всём треке: `read=15
/ write=25 / intelligence=16`, `selfcheck_status=ok`.
Никаких реальных credentials ни в одном из шести Track H
commit'ов плюс одного Step 2 follow-up. Никаких 1cv8.exe
runs ни на одном шаге Track H. **GitHub remote push** не
часть Track H — repo готов к выкладке, но пушить —
operator action.

Документы трека:
[`track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md),
[`track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md),
[`track-h-transport-and-auth-baseline-audit.md`](docs/architecture/track-h-transport-and-auth-baseline-audit.md),
[`track-h-network-transport-and-auth-contract.md`](docs/architecture/track-h-network-transport-and-auth-contract.md).

Track H сейчас на **Step 5 (operator/security docs
alignment, docs-only)**. Закрытые шаги:

- **Step 1 (planning, docs-only, commit `563b27b`)** —
  ship'нуты два planning-документа
  ([`docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md),
  [`track-h-...-step-map.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md)).
- **Step 2 (transport / auth baseline audit, docs-only,
  commit `3c74564`; follow-up commit `0628f4c` removed
  literal credential-leak-guard pattern strings to keep
  the audit doc outside `verify-release.ps1` Check 7's
  match set)** — ship'нут
  [`track-h-transport-and-auth-baseline-audit.md`](docs/architecture/track-h-transport-and-auth-baseline-audit.md);
  resolved Q1 (HTTP-based), Q2 (exactly one), Q3 (static
  bearer + constant-time compare), Q4
  (`ProductConfig.auth.tokens` + `${ENV:NAME}` +
  `--auth-token-env` CLI override).
- **Step 3 (network transport / auth contract, docs-only,
  commit `2e76061`)** — ship'нут
  [`track-h-network-transport-and-auth-contract.md`](docs/architecture/track-h-network-transport-and-auth-contract.md)
  (1650 lines, 293 RFC 2119 keyword usages: 199 MUST,
  74 MUST NOT, 17 MAY, 2 SHOULD, 1 SHALL); 18 sections
  pinning every transport / auth / config / CLI /
  integration / verification rule for Step 4.
- **Step 4 (narrow HTTP transport and bearer auth
  boundary, единственный шаг с production code change,
  commit `5814041`)** — PATH A (per Step 3 contract
  §11). Ship'нуто 5 файлов (+877/-35):
  - `packages/mcp-common/src/mcp_common/_network_transport.py`
    (новый, 549 LOC, underscore-prefixed private,
    **NOT** в `mcp_common/__init__.py`'s `__all__`,
    pure stdlib `http.server.ThreadingHTTPServer` +
    `hmac.compare_digest`); содержит handler для
    `/mcp` POST endpoint (GET → 405+`Allow:POST`;
    non-`/mcp` → 404; wrong Content-Type → 415+`-32600`;
    body > 1 MiB → 413+`-32600`; multiple Authorization
    headers → 400+`-32600`; case-insensitive Bearer
    scheme; constant-time token compare; failure-
    equivalence 401+`WWW-Authenticate`+JSON-RPC `-32001`
    для missing/empty/malformed/invalid token;
    notifications → 204; complete redaction discipline);
    unified `run_main_http(...)` с одним argparser'ом
    для обоих transport'ов (stdio path делегирует в
    existing `_stdio_transport._serve_stdio` byte-
    identically).
  - 3 `__main__.py` (modified) — switched import
    `_stdio_transport.run_main` → `_network_transport.run_main_http`;
    `SERVER_VERSION` 0.3.0→0.4.0; module docstrings
    updated; `main() -> int` signature preserved.
  - `apps/platform/src/onec_platform/models.py`
    (modified) — добавлен новый `ProductAuthSettings`
    dataclass с `tokens: list[str]` + `auth` field на
    `ProductConfig` с `default_factory`.
  - `apps/platform/src/onec_platform/loader.py`
    (modified) — новый `_AUTH_ENV_TOKEN_RE` regex
    byte-identical к Track D pattern; новый
    `_parse_auth(auth_raw)` с unknown-keys reject,
    list-of-strings validation, env-substitution regex
    enforce per entry, literal cleartext fail-closed
    at config-load time.

После Step 4 фактически работают:

```powershell
python -m mcp_read_server --transport stdio --help
python -m mcp_read_server --transport http --bind 127.0.0.1:8765 --auth-token-env MCP_TOKEN --help
```

(и аналогично для двух остальных серверов). Каждый сервер
поддерживает оба transport'а через единый
`list_tools()` / `get_tool(name)` boundary; `run_write_flow`
discipline для write-tools и read-only-by-construction
discipline intelligence-сервера preserved unchanged на
обоих transport'ах. Step 4 verification — 51 / 51 PASS
(per-server `--help` exit 0; HTTP startup negative tests:
missing `--bind`, missing token source, unresolved env;
HTTP positive smoke на всех 3 servers; **byte-identical
401 fail-closed** для no-Authorization vs wrong-token;
case-insensitive scheme через {`Bearer`, `bearer`,
`BEARER`, `BeArEr`}; GET 405; non-`/mcp` 404; malformed
JSON 400+`-32700`; wrong Content-Type 415+`-32600`;
unknown method 200+`-32601`; multiple Authorization
400+`-32600`; notification 204; `tools/call ping` 200;
cross-transport parity stdio = HTTP tool-name set).

Registries `read=15 / write=25 / intelligence=16` без
drift'а; никаких новых MCP tools; никаких новых runtime
dependencies (implementation pure stdlib); никаких
1cv8.exe runs ни на одном шаге трека; никаких реальных
credentials в repo / docs / commit messages.

Что **не** входит в Track H (повтор для ясности после
Step 4): in-process TLS / HTTPS termination, mTLS /
client certificate authentication, JWT / OAuth 2.0 /
OIDC / SAML / SCIM, RBAC / ABAC / per-tool ACL /
per-tenant isolation / multi-tenant policy engine,
token rotation endpoint / refresh tokens / session
cookies, rate limiting, WebSocket / SSE / TCP /
Unix-socket / named-pipe transports, supervisor daemon
/ systemd unit / Windows Service registration /
`launchd` plist / auto-update / orchestration templates
/ HA / clustering / load balancing / hot reload /
background watchers, web UI / dashboard frontend,
packaging ecosystem (`.msi` / `.deb` / signed
distribution / GUI installer / PyPI publication / wheel
publication beyond `[project.scripts]` declarations),
new MCP tools (registries without drift), 1cv8 work,
rollback / AST / multi-version 1С matrix expansion,
standalone `apps/platform` entrypoint, distributed
tracing / observability stack, real MCP client
integration test as closure gate, remote push.

Известный gap из Step 4 (operator-facing item handled
in this Step 5 alignment, not a Step 4 code-fix):
`apps/platform/src/onec_platform/installer.py:_config_to_dict`
не emit'ит новый `auth` section, поэтому config
round-tripped через `scripts/release/install.ps1 ...
-Confirm` silently теряет declarations `auth.tokens`.
Operators using `--transport http` against a round-
tripped config get a clean fail-closed startup и либо
re-add the section by hand либо use `--auth-token-env
<VARNAME>` CLI flag to bypass the config. Future
post-Track-H fix к `_config_to_dict` analogous Phase 6
/ Step 9 service-level + enterprise round-trip fix.

Следующий шаг по Track H — **Step 6 (final integration
pass and Track H closure)**: closure narrative pass
через `README.md` + `PROJECT-STATUS.md` + `CHANGELOG.md`
(Q7 default ДА — version bump 0.4.0→0.5.0 на closure
если Step 4 functional delta проходит SemVer MINOR-
bump bar; финальное решение — Step 6); **GitHub remote
push — operator action, не часть трека**.

Документы трека:
[`track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md),
[`track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md),
[`track-h-transport-and-auth-baseline-audit.md`](docs/architecture/track-h-transport-and-auth-baseline-audit.md),
[`track-h-network-transport-and-auth-contract.md`](docs/architecture/track-h-network-transport-and-auth-contract.md).

Подробности по последнему закрытому треку — в секции
«Track G detail (закрыт)» ниже.

## Track G detail (закрыт)

**Цель Track G** была — ship'ить **первый production-grade
operational слой** для трёх MCP servers, закрывая factual
gap «MCP servers cannot start at all»: canonical
`__main__.py` для всех трёх MCP servers, minimum-viable
stdio JSON-RPC 2.0 transport, minimal CLI surface
(`--help`, `--config-path`, `--transport`, `--log-level`),
`[project.scripts]` console entry points в `pyproject.toml`.
Это **не** universal production transport, **не**
network-grade HTTP/WebSocket layer, **не** authentication /
authorization, **не** supervisor daemon, **не** HA /
clustering, **не** web UI, **не** packaging ecosystem
(`.msi` / `.deb` / signed distribution), **не** enterprise
super-set (SSO/RBAC/multi-tenant), **не** standalone
`apps/platform` entrypoint. Платформа архитектурно остаётся
при том же подходе: existing `server.py:REGISTERED_TOOLS`
registries (`list_tools()` / `get_tool(name)`) preserved
byte-identical; Track G ship'ил **transport layer поверх**
этих registries, не задевая их. Шесть шагов;
production-код Track G правил **только Step 4 commit** и
**только** на explicit allowed surfaces (3 new `__main__.py`
files + 1 new private `mcp_common._stdio_transport` helper +
`pyproject.toml` `[project.scripts]` block).

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-g-production-grade-mcp-transport-and-cli-plan.md`](docs/architecture/track-g-production-grade-mcp-transport-and-cli-plan.md),
  [`docs/architecture/track-g-production-grade-mcp-transport-and-cli-step-map.md`](docs/architecture/track-g-production-grade-mcp-transport-and-cli-step-map.md)):
  назначение трека, целевой результат, что закрывает /
  не закрывает Track G, отличия от Tracks A–F, guardrails,
  acceptance criteria, открытые вопросы Q1–Q7. Никакого
  code change. Commit `7a39454`.
- **Step 2 (transport baseline audit)** — новый
  documentation-only audit-документ
  ([`docs/architecture/track-g-transport-baseline-audit.md`](docs/architecture/track-g-transport-baseline-audit.md),
  587 строк) с per-server inventory current state +
  4-class breakdown (already useful baseline / adjacent
  insufficient / clearly missing / out-of-scope) +
  read-only evidence. Critical findings: pyproject.toml
  имеет zero declared runtime deps (no `[project.dependencies]`
  block at all), zero MCP SDK imports anywhere в repo,
  все 3 MCP server packages идентичная structure без
  `__main__.py`. **Q1 resolved** (stdio only), **Q2
  resolved** (custom stdlib без новых deps), **Q6
  resolved** (`apps/platform` standalone entrypoint
  out-of-scope). Никакого code change. Commit `6f3ad73`.
- **Step 3 (runtime CLI / entrypoint contract)** — новый
  prescriptive normative document
  ([`docs/architecture/track-g-runtime-cli-entrypoint-contract.md`](docs/architecture/track-g-runtime-cli-entrypoint-contract.md),
  879 строк) с RFC 2119-style MUST / MUST NOT / SHALL /
  SHOULD / MAY wording (85 normative keyword usages).
  15 sections: exact `__main__.py` shape, exact CLI
  surface, exact transport scope (stdio JSON-RPC 2.0 only,
  forbidden libraries, stdout/stderr discipline,
  minimum-viable MCP method set), server binding /
  dispatch contract (через existing `list_tools()` /
  `get_tool(name)` indirection — никаких parallel
  registration paths), no-auth posture, no-supervisor
  posture, exact `[project.scripts]` block, backward
  compatibility (15/25/16 registries + `mcp_common` API +
  audit shape preserved), exact Step 4 implementation
  surface (allowed files + forbidden surfaces + scope
  creep markers), verification protocol. Никакого code
  change. Commit `8bb3883`.
- **Step 4 (narrow stdio transport and CLI entrypoints)** —
  единственный шаг Track G с production code change.
  Implementation path **PATH B** (3 entrypoints + pyproject
  scripts + 1 private `mcp_common` helper). PATH A pure
  inline был отвергнут потому что каждый `__main__.py`
  carried бы ~140 LOC идентичных argparse / JSON-RPC
  framing / dispatch logic — ~280 LOC pure copy-paste
  через 3 server'а — что qualifies as «duplication
  otherwise unreasonable» под Step 3 contract §12.1.4.
  Ship'нуто 5 файлов (+361 lines):
  - `packages/mcp-common/src/mcp_common/_stdio_transport.py`
    (новый, 245 LOC) — underscore-prefixed internal helper,
    **NOT** экспортирован из `mcp_common/__init__.py`;
    pure stdlib (`argparse`, `json`, `logging`, `inspect`,
    `sys`); реализует line-delimited JSON-RPC 2.0 loop,
    четыре required CLI флага, handlers для `initialize` /
    `ping` / `tools/list` / `tools/call` /
    `notifications/initialized` / `notifications/cancelled`,
    serialization `ToolResult` → MCP envelope (`content`
    + `structuredContent` + `isError`), top-of-`run_main`
    exception boundary; stdout reserved для JSON-RPC
    envelopes, диагностика — в stderr через `logging`;
  - `apps/mcp-read-server/src/mcp_read_server/__main__.py`
    (новый, ~30 LOC);
  - `apps/mcp-write-server/src/mcp_write_server/__main__.py`
    (новый, ~30 LOC);
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
    (новый, ~30 LOC) — каждый определяет `main() → int`
    которая зовёт `run_main` с per-package's existing
    `list_tools` / `get_tool` boundary и per-server name +
    version. No `__init__.py` edits, no `server.py` edits,
    no `tools.py` / `models.py` / `runtime/` / `apps/platform/`
    touches;
  - `pyproject.toml` (edit) — добавлен `[project.scripts]`
    block с ровно тремя console entries
    (`mcp-read-server`, `mcp-write-server`,
    `mcp-intelligence-server`); никаких новых deps;
    `[tool.hatch.build.targets.wheel] packages = []`
    preserved unchanged (Track C / Step 3 honest
    constraint kept).

  Commit `370c5a8`.
- **Step 5 (operator docs and transport alignment)** —
  docs-only narrow alignment под фактический Step 4
  surface; 6 files +229/-81 lines: `README.md` (Quickstart
  paragraph + «Что Quickstart не обещает» + полный rewrite
  Active parallel track секции), `SECURITY.md` (один bullet
  «No production-grade MCP transport yet» → «Local stdio
  MCP transport only» с explicit threat model и still-NOT
  list), `docs/release-handoff.md` (новый bullet под
  «What is in this handoff» + «What is NOT in this
  handoff» reworded + «Local check / launch» parenthetical
  fix + Known limitations alignment),
  `apps/platform/README.md` (4 locations: Phase 5/Step 3
  callout + «Чего сейчас намеренно ещё нет» + parallel
  list + Phase 6 honest-constraints item),
  `scripts/dev/launch.ps1` (header comment + Show-Usage
  help text — operators pointed at `python -m <server>
  --help`), `scripts/dev/README.md` (две parenthetical
  wording fixes + CI workflow note distinguishes live
  MCP runtime от selfcheck). NOT touched: PROJECT-STATUS
  + CHANGELOG (closure territory); production code;
  pyproject.toml (Q7 = Step 6); registries `15/25/16`
  invariant. Commit `5890ba5`.
- **Step 6 (final integration pass and Track G closure)** —
  этот closure: `pyproject.toml` version bumped
  `0.3.0` → `0.4.0` (Q7 = ДА; Track G / Step 4 ship'нул
  real production code change с **observable runtime
  capability delta** — `python -m mcp_{read,write,intelligence}_server`
  теперь реально стартуют stdio JSON-RPC server, что
  до Track G было невозможно; backward-compatible new
  functionality classifying as MINOR bump per SemVer;
  precedent — Track D `0.1.0 → 0.2.0` и Track F
  `0.2.0 → 0.3.0` shipped comparable scale functional
  delta);
  README + PROJECT-STATUS + CHANGELOG обновлены под
  Track G closed.

После Track G closure фактически работают:

```powershell
python -m mcp_read_server --help
python -m mcp_write_server --help
python -m mcp_intelligence_server --help
```

Каждый сервер поднимает line-delimited stdio JSON-RPC 2.0
loop с handler'ами для `initialize` / `ping` / `tools/list`
/ `tools/call` / `notifications/initialized` /
`notifications/cancelled`. Stdout зарезервирован под
JSON-RPC envelopes; диагностика идёт в stderr через
`logging`. Tool dispatch идёт через existing `server.py`
boundary (`list_tools()` / `get_tool(name)`);
`run_write_flow` discipline для write-tool'ов сохранена;
read-only-by-construction discipline intelligence-сервера
сохранена; `mcp_common` public API surface (export'ы из
`mcp_common/__init__.py`) preserved byte-identical.

Что Track G **реально закрыл** (на основе Steps 1–5
deliverables):

- три canonical entrypoint'а
  (`apps/mcp-{read,write,intelligence}-server/src/.../`__main__.py``)
  + одну private internal stdio JSON-RPC 2.0 transport
  библиотеку (`packages/mcp-common/src/mcp_common/_stdio_transport.py`,
  underscore-prefixed, **NOT** в public `mcp_common`
  surface) — `python -m <server>` теперь runtime-достижим;
- minimal CLI surface на каждом сервере: `--help`,
  `--config-path`, `--transport stdio`, `--log-level
  {DEBUG,INFO,WARNING,ERROR}`; `--help` exit 0 + non-empty
  usage verified для всех трёх servers;
- `[project.scripts]` block в `pyproject.toml` с тремя
  console entries (готовы к activation, как только future
  packaging track ship'ит real wheel — wheel build по-
  прежнему пуст по Track C honest constraint);
- formal normative entrypoint / CLI / transport contract
  (RFC 2119-style, 879 строк) — единая reference для
  любого future transport extension;
- aligned operator-facing docs (README, SECURITY,
  docs/release-handoff.md, apps/platform/README.md,
  scripts/dev/launch.ps1, scripts/dev/README.md) — все
  говорят one truth: local stdio transport baseline
  exists, network/auth/supervisor still out-of-scope;
- registries invariant `read=15 / write=25 /
  intelligence=16` carried through unchanged;
  `mcp_common` public API export'ы preserved
  byte-identical; audit `details` shape preserved.

Что Track G **не делает** «production-deployment-ready
MCP сервером для adversarial network» после closure
(honest constraints, никаких скрытых гэпов):

- никакого network transport (HTTP / WebSocket / SSE /
  TCP / Unix domain socket / named pipe / Windows IPC) —
  это subsequent post-Track-G track;
- никакой authentication / authorization (token / Bearer
  / JWT / API key / mTLS / OAuth 2.0 / OpenID Connect /
  SAML / RBAC / ABAC / multi-tenant isolation) —
  trusted-stdio-only threat model;
- никакого supervisor daemon (systemd unit / Windows
  Service / `launchd` plist / Docker / Kubernetes /
  `supervisor` / `runit` / `s6` integration recipes /
  automatic restart watcher / log aggregation);
- никакого hot reload или background config watcher;
- никакого web UI / dashboard frontend;
- никакого packaging ecosystem beyond
  `[project.scripts]` declarations (`.msi` / `.deb` /
  GUI installer / signed distribution / PyPI publication
  / wheel publication — Track C wheel-build empty
  constraint preserved);
- никакого standalone `apps/platform` entrypoint
  (deliberately out-of-scope per Q6);
- никакого 1cv8.exe execution work на любом шаге трека;
- никаких новых MCP tools (registries без drift'а);
- никакого distributed tracing / observability stack
  (OpenTelemetry / Jaeger / Prometheus);
- никаких rate limiting / multi-instance load balancing;
- real MCP client integration test (Claude Desktop, MCP
  CLI launching server) **не** часть Track G closure
  gate — это operator infra territory.

Registry-инвариант сохранён точно на всём треке: `read=15 /
write=25 / intelligence=16`, `selfcheck_status=ok`. Никаких
реальных credentials ни в одном из шести Track G commit'ов.
Никаких 1cv8.exe runs ни на одном шаге Track G (Track G
работает на process / transport layer уровне, не на 1cv8
binary surface). **GitHub remote push** не часть Track G —
repo готов к выкладке, но пушить — operator action.

Документы трека:
[`docs/architecture/track-g-production-grade-mcp-transport-and-cli-plan.md`](docs/architecture/track-g-production-grade-mcp-transport-and-cli-plan.md),
[`docs/architecture/track-g-production-grade-mcp-transport-and-cli-step-map.md`](docs/architecture/track-g-production-grade-mcp-transport-and-cli-step-map.md),
[`docs/architecture/track-g-transport-baseline-audit.md`](docs/architecture/track-g-transport-baseline-audit.md),
[`docs/architecture/track-g-runtime-cli-entrypoint-contract.md`](docs/architecture/track-g-runtime-cli-entrypoint-contract.md).

## Track F detail (закрыт)

**Цель Track F** была — узко и контролируемо расширить
`_AUTOMATIC_RECOVERY_SUPPORTED` whitelist
(`apps/platform/src/onec_platform/recovery.py:126-133`) за
пределы Phase-6 / Step-4 baseline'а в 2 tools для нескольких
file-based mutating tools, чьи inverse semantics уже честно
покрываются existing `restore_dump_file_from_snapshot`
mechanism'ом. Это **не** universal rollback, **не** «rollback
теперь есть везде», **не** public `delete_*` write-tools,
**не** multi-file / DB schema rollback, **не** AST-based
semantic reverse engine, **не** новый MCP surface, **не**
execution-core rewrite. Платформа архитектурно осталась при
том же подходе: rollback идёт через public write-tool по
`run_write_flow` дисциплине; Track F расширил **whitelist
configuration**, не mechanism. Шесть шагов; production-код
Track F правил **только два** boundary'а в одном Step 4
commit'е.

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-f-rollback-whitelist-expansion-plan.md`](docs/architecture/track-f-rollback-whitelist-expansion-plan.md),
  [`docs/architecture/track-f-rollback-whitelist-expansion-step-map.md`](docs/architecture/track-f-rollback-whitelist-expansion-step-map.md)):
  назначение трека, целевой результат, gap statement, 10
  acceptance criteria, открытые вопросы Q1–Q7. Никакого code
  change. Commit `351278b`.
- **Step 2 (rollback baseline audit and candidate selection)** —
  новый documentation-only audit-документ
  ([`docs/architecture/track-f-rollback-baseline-audit.md`](docs/architecture/track-f-rollback-baseline-audit.md),
  637 строк): per-tool evaluation 12 mutating tools (Group
  C/D/E из 25 registry) против criteria a/b/c с manual code
  review evidence (file/line + payload key для каждого);
  **Tier 4** (already, 2 tools), **Tier 1** (strong
  candidates, 4 tools), **Tier 2** (deferred — `update_module_code`
  payload key gap), **Tier 3** (categorically excluded — 5
  tools: 3 `create_*` family + `apply_config_from_files` +
  `update_database_configuration`); resolve **Q2** —
  exact Step 4 target set. Никакого code change. Commit
  `e9725b2`.
- **Step 3 (rollback eligibility contract)** — новый
  prescriptive normative document
  ([`docs/architecture/track-f-rollback-eligibility-contract.md`](docs/architecture/track-f-rollback-eligibility-contract.md),
  633 строки) с RFC 2119-style MUST / MUST NOT / SHALL / MAY
  wording (64 normative keyword usages): formal eligibility
  criteria 4.A–4.F (payload shape via `_RELATIVE_PATH_KEYS`,
  restore semantics, verification, sync discipline,
  non-expansion, implementation surface), 9 categorical
  exclusions, exact Step 4 implementation boundary с per-tool
  sanity check anchors, escape clause без silent target-set
  drift, backward compatibility statement. Никакого code
  change. Commit `45ad2b2`.
- **Step 4 (narrow rollback whitelist expansion)** —
  единственный шаг Track F с production code change. Narrow
  two-file expansion 2 → 6 entries: расширены
  `apps/platform/src/onec_platform/recovery.py:_AUTOMATIC_RECOVERY_SUPPORTED`
  и
  `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py:_ROLLBACK_SUPPORTED_OPERATIONS`
  identical content'ом — добавлены `add_form_attribute`,
  `add_form_element`, `append_module_method`,
  `replace_module_method_body` (alphabetically). Plus minor
  sync-comment wording update в `flow.py:97-103` (allowed per
  Step 3 contract Section 6.3.1). Per-tool sanity check
  anchors зафиксированы в commit message с
  `tools.py` line numbers (3512-3520 / 2680-2687 / 2833-2838 /
  2994-2999). Никаких изменений в `tools.py`,
  `_RELATIVE_PATH_KEYS`, `_extract_relative_path`, audit
  shape, registries. Commit `cd95627`.
- **Step 5 (operator docs and rollback coverage alignment)** —
  8 точечных wording-edits в трёх operator-facing docs:
  `apps/platform/README.md` (5 правок: RECOVERY_MODES
  executed-mode wording; section heading «Почему пуст» →
  «исторически был пуст и как он расширялся»; «Что rollback
  UX не делает» bullet; Phase 6 / Step 4 historical section
  + новая «Track F / Step 4 — расширение whitelist до 6
  tools» subsection), `README.md` (2 правки: Quickstart
  Track F open + Track A detail honest constraints bullet),
  `docs/release-handoff.md` (1 правка: «Limited rollback
  coverage» Known limitations bullet). Никакого code change.
  Commit `60f1761`.
- **Step 6 (final integration pass and Track F closure)** —
  этот closure: `pyproject.toml` version bumped
  `0.2.0` → `0.3.0` (Q5 = ДА; Track F / Step 4 ship'нул real
  code change с functional delta — backward-compatible new
  functionality classifying as MINOR bump per SemVer);
  README + PROJECT-STATUS + CHANGELOG обновлены под Track F
  closed.

Что Track F **реально закрыл** (на основе Steps 1–5
deliverables):

- расширение `_AUTOMATIC_RECOVERY_SUPPORTED` whitelist'а
  с 2 до 6 entries identical в обеих mirror frozenset'ах
  (recovery.py + flow.py); `automatic_recovery_supported=True`
  теперь runtime-достижим для 4 дополнительных tool families
  (XML form-edit ops + BSL module-edit ops);
- formal normative eligibility contract (RFC 2119-style)
  определяющий что считается eligible (payload shape +
  restore semantics + verification + sync discipline +
  non-expansion + implementation surface) — единая reference
  для будущих whitelist expansion attempts;
- per-tool descriptive audit с manual code review evidence
  (file/line + payload key) для всех 12 mutating tools
  registry surface;
- aligned operator-facing docs (`apps/platform/README.md`,
  `README.md`, `docs/release-handoff.md`) под фактический
  whitelist size 6 — все говорят one truth: coverage broader
  but still narrow, no blanket reversibility claim, Tier 3
  categorical exclusions remain.

Что Track F **не делает** «полным rollback'ом всего» после
closure (honest constraints, никаких скрытых гэпов):

- никакого universal / arbitrary rollback для любого
  write-tool — whitelist остаётся ограничен exact 6 entries;
- никакого AST-based semantic reverse engine для BSL / XML;
- никакого public `delete_*` write-tools (semantics удаления
  в 1С остаётся undecided);
- никакого multi-file / full filesystem snapshot-restore —
  single-file `restore_dump_file_from_snapshot` остаётся
  exclusive mutating mechanism;
- никакого rollback для `apply_config_from_files`
  (multi-file impact violates criterion (a));
- никакого rollback для `update_database_configuration`
  (DB schema migration violates criteria (a)/(b)/(c));
- никакого rollback для `create_*` family (`create_catalog`,
  `create_common_module`, `create_managed_form` — Tier 3
  categorical exclusion: inverse = delete; snapshot
  pre-create не содержит file для restore);
- coverage breadth: 6 of 25 mutating registry tools = 24%
  mutating surface; 19 mutating tools остаются manual
  snapshot-restore territory by design.

Registry-инвариант сохранён точно на всём треке: `read=15 /
write=25 / intelligence=16`, `selfcheck_status=ok`. Никаких
реальных credentials ни в одном из шести Track F commit'ов.
Никаких 1cv8.exe runs ни на одном шаге Track F (Track F
работает на whitelist configuration уровне, не на 1cv8
binary surface). **GitHub remote push** не часть Track F —
repo готов к выкладке, но пушить — operator action.

Документы трека: `docs/architecture/track-f-rollback-whitelist-expansion-plan.md`,
`docs/architecture/track-f-rollback-whitelist-expansion-step-map.md`,
`docs/architecture/track-f-rollback-baseline-audit.md`,
`docs/architecture/track-f-rollback-eligibility-contract.md`.

## Track E detail (закрыт)

**Цель Track E** была — расширить доказательную базу проекта с
**одного** reference stand'а / **одной** 1С версии
(`8.3.27.1859`, evidence Track A / Step 6) на узкую
documented smoke matrix из нескольких 1С версий по одному
и тому же узкому сценарию. Платформа архитектурно
остаётся multi-version-friendly: оператор сам выбирает
binary path в config'е; Track E добавляет
evidence-уровень и docs, **не** архитектуру. Это **не**
«поддержка всех версий», **не** full QA program, **не**
performance / stress / fuzzing track, **не** enterprise
certification, **не** новый MCP surface. Шесть шагов;
production-код Track E **вообще не правил**.

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-e-multi-version-smoke-matrix-plan.md`](docs/architecture/track-e-multi-version-smoke-matrix-plan.md),
  [`docs/architecture/track-e-multi-version-smoke-matrix-step-map.md`](docs/architecture/track-e-multi-version-smoke-matrix-step-map.md)):
  назначение трека, целевой результат, gap statement
  (argv-grammar drift между версиями + install layout
  dependency), guardrails, 10 acceptance criteria, открытые
  вопросы Q1–Q7. Никакого code change. Commit `1b233ce`.
- **Step 2 (current evidence audit + smoke scenario freeze)** —
  два новых short documentation-only документа:
  [`docs/architecture/track-e-current-evidence-audit.md`](docs/architecture/track-e-current-evidence-audit.md)
  (descriptive — что уже доказано на reference version,
  physical artifacts, чего пока нет, why single-version
  insufficient) и
  [`docs/architecture/track-e-smoke-scenario.md`](docs/architecture/track-e-smoke-scenario.md)
  (prescriptive **frozen** — name `frozen-smoke-v1`,
  cut-down `create_dump_snapshot` через `/DumpConfigToFiles`
  only, principle-based version selection criteria,
  12-column matrix shape, PASS / FAIL / NOT RUN semantics,
  required evidence fields). Никакого code change. Commit
  `630f837`.
- **Step 3 (matrix scaffolding and operator runbook)** — два
  новых operator-facing документа:
  [`docs/runbooks/track-e-multi-version-smoke-matrix.md`](docs/runbooks/track-e-multi-version-smoke-matrix.md)
  (operator runbook для прогона `frozen-smoke-v1` на
  operator-supplied 1С версии — preconditions, execution
  procedure, evidence capture, common stop conditions,
  honest constraints) и
  [`docs/version-support-matrix.md`](docs/version-support-matrix.md)
  (top-level evidence table с frozen 12-column shape; одна
  reference row заполнена copy-only из existing Track A /
  Step 6 evidence, scenario field явно
  `stronger-than-frozen-smoke-v1`; никаких имитированных
  additional rows). Никакого 1cv8.exe run. Commit `7c08cae`.
- **Step 4 (operator-driven smoke execution and matrix
  update)** — закрыт через **PATH B (honest
  operator-supplied gap)**. Никаких 1cv8.exe runs не было
  выполнено в этом шаге; никаких additional evidence rows
  не было добавлено. Operator-side inventory показал только
  `8.3.27` minor family (builds `1859/x64` reference и
  `1936/x86` дисквалифицирован per Step 2 §2.2 — same minor
  family); никаких `8.3.<other minor>` family у operator'а
  нет; ENV-substitution credentials не выставлены в session.
  Per Track E plan Q4 + step-map Step 4 это **honest
  closure**, не failure. Matrix doc дополнен Step 4 closure
  note с inventory-таблицей и explicit list того, что Step 4
  сознательно не делал. Commit `f962d78`.
- **Step 5 (support statement and docs alignment)** — три
  operator-facing документа выровнены под фактический Step 4
  PATH B результат:
  [`SECURITY.md`](SECURITY.md) («Single-version 1С evidence
  (with multi-version scaffolding)» bullet с pointer на
  matrix doc + «no blanket multi-version support claim»),
  [`docs/release-handoff.md`](docs/release-handoff.md)
  («Multi-version 1С smoke matrix — scaffolding only»
  Known limitations + Single-version coverage bullet pointer
  расширение), и Quickstart paragraph + «Куда идти дальше»
  navigation в этом README. Никакого code change. Commit
  `78d5956`.
- **Step 6 (final integration pass and Track E closure)** —
  этот closure: README + PROJECT-STATUS + CHANGELOG
  обновлены под Track E closed; никакого version bump
  (Q5 = НЕТ — Track E без functional delta).

Что Track E **реально закрыл** (на основе Steps 1–5
deliverables):

- frozen narrow smoke scenario `frozen-smoke-v1` —
  cut-down `create_dump_snapshot` через
  `/DumpConfigToFiles` only, читаемый contract на
  PASS / FAIL / NOT RUN verdict;
- documented matrix scaffolding (12-column frozen
  contract в `docs/version-support-matrix.md`,
  reference row copy-only из existing Track A
  evidence);
- operator runbook для прогона smoke на любой
  operator-supplied 1С версии без feature changes
  в платформе;
- aligned operator-facing docs (SECURITY,
  release-handoff, README) — все говорят одно и то
  же про current evidence level: reference есть,
  matrix scaffolding есть, additional rows нет,
  PATH B honest gap;
- single source of truth для actual evidence level —
  `docs/version-support-matrix.md`;
- post-closure additional rows возможны через
  operator-driven runs по runbook'у без re-open
  трека (per plan Q7).

Что Track E **не делает** «полной совместимостью
со всеми 1С версиями» после closure (honest
constraints, никаких скрытых гэпов):

- никаких additional version evidence rows beyond
  reference — Step 4 закрыт через PATH B; на
  operator machine отсутствуют 1С minor families
  помимо `8.3.27`;
- никакого blanket multi-version support claim;
- никакой полной QA-программы, performance /
  stress / fuzzing testing, enterprise
  certification;
- никакого version-sniffing в платформе;
- никаких новых MCP tools (registries `read=15 /
  write=25 / intelligence=16` без drift'а);
- никаких 1cv8 binary changes, transport rewrite,
  packaging rewrite;
- никакой CI matrix runner-инфраструктуры для
  multi-version 1cv8 (это physical operator
  territory);
- никакого long-tail backwards compatibility
  guarantee для будущих 1С версий, ещё не
  вышедших на момент closure.

Registry-инвариант сохранён точно на всём треке:
`read=15 / write=25 / intelligence=16`,
`selfcheck_status=ok`. Никаких реальных credentials
ни в одном из шести Track E commit'ов. Никаких
запусков 1cv8.exe ни на одном шаге Track E (Step 4
PATH B closure означал явное отсутствие runs).
**GitHub remote push** не часть Track E — repo
готов к выкладке, но пушить — operator action.

Документы трека: `docs/architecture/track-e-multi-version-smoke-matrix-plan.md`,
`docs/architecture/track-e-multi-version-smoke-matrix-step-map.md`,
`docs/architecture/track-e-current-evidence-audit.md`,
`docs/architecture/track-e-smoke-scenario.md`,
`docs/runbooks/track-e-multi-version-smoke-matrix.md`,
`docs/version-support-matrix.md`.

## Track D detail (закрыт)

**Цель Track D** была — сделать operator credentials flow
менее хрупким: ввести документированный env-substitution путь
для DESIGNER credentials в `onec_*_command_template`-массивах,
добавить redaction discipline в `command_preview` и trimmed
payload-excerpt'ы, перенести cleartext-password literal из
«нормального baseline'а» в legacy fallback, и расширить
`verify-release.ps1` узкой credential-template-hygiene
heuristic'ой. Это **не** enterprise security platform, **не**
vault / KMS / SSO / RBAC track, **не** OS keychain integration
as baseline и **не** production-grade MCP transport. Шесть
шагов; production-код Track D правил **только два**
boundary'а — один внутри `mcp-write-server` runtime layer и
один release-side скрипт.

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-d-operator-credentials-hardening-plan.md`](docs/architecture/track-d-operator-credentials-hardening-plan.md),
  [`docs/architecture/track-d-operator-credentials-hardening-step-map.md`](docs/architecture/track-d-operator-credentials-hardening-step-map.md)):
  назначение трека, целевой результат, guardrails,
  10 acceptance criteria, открытые вопросы Q1–Q7. Никакого
  code change; commit `61cf225`.
- **Step 2 (credentials-flow audit and contract)** — два
  новых documentation-only документа:
  [`docs/architecture/track-d-credentials-flow-audit.md`](docs/architecture/track-d-credentials-flow-audit.md)
  (где `/P "<password>"` физически появляется сегодня, какие
  payload-поля видят rendered argv, что значит «out-of-band»
  до Track D), и
  [`docs/architecture/track-d-credentials-contract.md`](docs/architecture/track-d-credentials-contract.md)
  (формальный contract на env-substitution syntax,
  render-time resolution order, fail-closed semantics,
  redaction discipline, backward-compat с literal
  cleartext). Никаких изменений production-кода; commit
  `0d708d1`.
- **Step 3 (env substitution and preview redaction)** —
  implementation в
  `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`:
  helper `_resolve_env_token(...)` резолвит full-element
  токен `${ENV:NAME}` из process environment в render-time
  (после structural-placeholder substitution); fail-closed
  на missing / empty / partial / mixed формах
  (`ok=False`, `command_preview=None`, subprocess **не**
  стартует); helper `_redact_password_args(...)` подменяет
  argv-элемент после `/P` или `/Pwd` (case-insensitive) на
  sentinel `<redacted>` в `command_preview` и trimmed
  excerpt'ах. Actual subprocess argv остаётся unredacted —
  иначе binary не аутентифицируется. Literal cleartext
  templates по-прежнему supported как legacy fallback.
  Registry-инвариант `read=15 / write=25 / intelligence=16`
  без drift'а; commit `af4436f`.
- **Step 4 (operator docs and migration alignment)** —
  operator-facing документация переведена на
  `${ENV:NAME}` форму как **рекомендованный default**, с
  literal cleartext clearly marked legacy fallback. Три
  документа выровнены:
  [`docs/runbooks/track-a-reference-stand-round-trip.md`](docs/runbooks/track-a-reference-stand-round-trip.md)
  (product-config example, env-substitution callout,
  failure mode F2 расширен под env-token failures,
  credentials-in-logs нота обновлена),
  [`SECURITY.md`](SECURITY.md) (Honest constraints block
  переписан под env-substitution),
  [`docs/release-handoff.md`](docs/release-handoff.md)
  (Known limitations DESIGNER credentials bullet
  переписан). Никаких изменений production-кода; commit
  `393e869`.
- **Step 5 (release verify credential hygiene heuristic)** —
  8-й check **Credential template hygiene** добавлен в
  [`scripts/release/verify-release.ps1`](scripts/release/verify-release.ps1).
  Сканирует tracked `*.config.json` (через `git ls-files`)
  на argv-элементы непосредственно после `"/P"` / `"/Pwd"`
  (case-insensitive) внутри command-template массивов.
  Документированные safe-формы (`"${ENV:NAME}"`,
  `"<password>"`) → PASS; literal cleartext → **WARN**
  (не FAIL), с file:line; пустые value не флагуются. WARN
  не меняет exit-code semantics, поэтому legacy templates
  не блокируют receive-side flow.
  [`scripts/release/README.md`](scripts/release/README.md) и
  [`docs/release-handoff.md`](docs/release-handoff.md)
  синхронизированы под 8 checks и описывают узкий
  heuristic-not-DLP scope; commit `1fd2d35`.
- **Step 6 (final integration pass and Track D closure)** —
  этот closure: `pyproject.toml` version bumped
  `0.1.0` → `0.2.0`; README + PROJECT-STATUS + CHANGELOG
  обновлены под Track D closed.

Что Track D **реально закрыл** (на основе Steps 1–5
deliverables):

- documented `${ENV:NAME}` substitution path для DESIGNER
  credentials в `onec_*_command_template`-массивах;
  render-time resolution; fail-closed на missing / empty /
  mixed формах;
- redaction discipline: argv-элемент после `/P` / `/Pwd`
  редактируется на `<redacted>` в `command_preview` и
  trimmed excerpt'ах; actual subprocess argv остаётся
  unredacted (binary должен аутентифицироваться);
- migration: env-substitution стал рекомендованным
  default'ом, literal cleartext остался supported как
  legacy fallback — backward-compat сохраняется;
- release-verify scope расширен 8-м credential-template-
  hygiene check'ом, который ловит наиболее очевидный
  паттерн утечки (literal `/P "<value>"` без
  env-substitution или `<password>` placeholder'а) как
  WARN, не блокируя release flow.

Что Track D **не делает** «enterprise security platform»
после closure (honest constraints, никаких скрытых гэпов):
никакого secrets manager / vault / KMS / cloud secrets
service / OS keychain integration / encrypted-at-rest
secrets format; никакого SSO / RBAC / multi-tenant
identity; никакого federated audit storage /
policy-as-code DSL; никакого production-grade MCP
transport / auth; никакого GUI installer wizard / signed
distribution / package-manager publication / web-UI /
dashboard; никакой multi-version 1С matrix / AST-парсер /
hot reload / новых MCP tools / 1cv8 binary changes. Эти
направления остаются за пределами Track A + Track B +
Track C + Track D.

Registry-инвариант сохранён точно на всём треке: `read=15 /
write=25 / intelligence=16`, `selfcheck_status=ok`.
Никаких реальных credentials ни в одном из шести Track D
commit'ов. **GitHub remote push** не часть Track D — repo
готов к выкладке, но пушить — operator action.

## Track C detail (закрыт)

**Цель Track C** была — довести существующий продукт до
состояния, в котором его удобно передать другому человеку
как **packaged unit / process**: release-facing layout
polish, reproducible install sequence checklist, pre-
handoff sanity check, release handoff документация,
единый release entrypoint map. Это **не** новый execution-
core sprint, **не** enterprise track, **не** GUI installer
wizard, **не** signed binary distribution, **не** package-
manager publication. Шесть шагов; production-код Track C
вообще **не правил**.

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-c-packaging-installer-delivery-plan.md`](docs/architecture/track-c-packaging-installer-delivery-plan.md),
  [`docs/architecture/track-c-packaging-installer-delivery-step-map.md`](docs/architecture/track-c-packaging-installer-delivery-step-map.md)):
  назначение трека, целевой результат, guardrails,
  10 acceptance criteria, явный список «что НЕ входит»;
  commit `af2d7f4`.
- **Step 2 (release-facing verify path and layout polish)** —
  [`scripts/release/verify-release.ps1`](scripts/release/verify-release.ps1)
  как pre-handoff sanity check (read-only: проверяет
  наличие entry points, dev-check workflow, planning docs,
  printing concise human-readable report); расширение
  [`scripts/release/README.md`](scripts/release/README.md)
  под трёх-entrypoint surface (install / verify / dev
  launch). Production-код не правил; commit `ef087c8`.
- **Step 3 (packaging-facing install flow honest review)** —
  честный review `pyproject.toml`: добавлен явный
  block-комментарий о том, что
  `[tool.hatch.build.targets.wheel] packages = []` —
  намеренный no-op (Phase 6 продукт не предназначен для
  publication как single Python wheel из-за multi-app
  monorepo shape); расширение release/README с
  packaging story. Никакого фиктивного wheel build не
  ввели; commit `a4f42f9`.
- **Step 4 (release handoff documentation)** — новый
  документ [`docs/release-handoff.md`](docs/release-handoff.md)
  для receive-side оператора: что вы получили, system
  prerequisites, reproducible install sequence, verify
  sequence, known limitations honest table; commit
  `7ca9b3f`.
- **Step 5 (integration and handoff polish)** —
  минимальный pointer на `docs/release-handoff.md` в
  Quickstart-навигации root README; никакой broad docs
  rewrite; commit `8ccecf6`.
- **Step 6 (final integration pass and Track C closure)** —
  этот closure: README + PROJECT-STATUS + CHANGELOG
  обновлены под Track C closed.

Что Track C **не** делает «глубоким индустриальным
продуктом» после closure (honest constraints, никаких
скрытых гэпов): GUI installer wizard, `.msi` / `.deb` /
signed binary distribution, publication к package
managers (PyPI / Chocolatey / winget / apt), systemd /
Windows Service registration, hot reload, web-UI /
dashboard frontend, полный enterprise super-set (SSO/RBAC,
multi-tenant, secrets vault как сервис, federated audit
storage, policy-as-code DSL, multi-instance HA),
production-grade MCP transport, multi-version 1С matrix,
полный AST-парсер XML/BSL, полная rollback/delete-
вселенная, новые MCP tools, production code rewrite. Эти
направления остаются за пределами Track A + Track B +
Track C — открытие отдельных тематических parallel
track'ов под них — operator decision.

Registry-инвариант сохранён точно на всём треке: `read=15 /
write=25 / intelligence=16`, `selfcheck_status=ok`. **GitHub
remote push** не часть Track C — repo готов к выкладке, но
пушить — operator action.

## Track B detail (закрыт)

**Цель Track B** была — довести существующий продукт до
удобного **install / run / repo / release** состояния, не
открывая нового execution-core sprint'а и не входя в
enterprise-super-set. Шесть шагов; production-код Track B
вообще **не правил**.

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-b-productization-polish-plan.md`](docs/architecture/track-b-productization-polish-plan.md),
  [`docs/architecture/track-b-productization-polish-step-map.md`](docs/architecture/track-b-productization-polish-step-map.md)):
  назначение трека, целевой результат, guardrails,
  10 acceptance criteria, явный список «что НЕ входит».
- **Step 2 (repo hygiene + legal layer)** — `git init` на
  `main`, расширенный `.gitignore` под snapshot trees /
  audit dirs / live dump trees / runtime state / 1С DB-
  файлы / writable configs / scratch dirs;
  [`LICENSE`](LICENSE) (Apache-2.0, полный стандартный
  текст); [`CHANGELOG.md`](CHANGELOG.md);
  [`SECURITY.md`](SECURITY.md) (reporting flow + honest
  constraints + safety guarantees); первый meaningful
  commit `85a4a7e`.
- **Step 3 (operator-discoverable install fast path)** —
  тонкий PowerShell wrapper [`scripts/release/install.ps1`](scripts/release/install.ps1)
  поверх существующего `run_install_fast_path` из
  Phase 6 / Step 3, плюс `_install_runner.py` и
  [`scripts/release/README.md`](scripts/release/README.md).
  Production-код не правил.
- **Step 4 (operator/dev local launch umbrella)** —
  [`scripts/dev/launch.ps1`](scripts/dev/launch.ps1) с
  четырьмя subcommands (`selfcheck` / `repl` / `run` /
  `help`); добавлена секция в
  [`scripts/dev/README.md`](scripts/dev/README.md).
  Production-код не правил.
- **Step 5 (root README quickstart and docs polish)** —
  верхний `## Quickstart` блок в этом README с install /
  check / launch командами и map'ом deeper docs.
- **Step 6 (final integration pass and Track B closure)** —
  этот closure: README + PROJECT-STATUS + CHANGELOG
  обновлены под Track B closed.

Что Track B **не** делает «глубоким индустриальным продуктом»
после closure (honest constraints, никаких скрытых гэпов):
production-grade MCP transport (нет authentication /
authorisation / network hardening), full installer ecosystem
(`.msi` / `.deb` / GUI wizard / signed distribution),
web-UI / dashboard frontend, полный enterprise super-set
(SSO/RBAC, multi-tenant, secrets vault как сервис, federated
audit, policy-as-code DSL, multi-instance HA), hot reload /
OS-level service supervision, multi-version matrix smoke,
полный AST-парсер XML/BSL, полная rollback/delete-вселенная,
новые MCP tools, production code rewrite. Эти направления
остаются за пределами Track B — открытие отдельных тематических
parallel track'ов под них — operator decision.

Registry-инвариант сохранён точно на всём треке: `read=15 /
write=25 / intelligence=16`, `selfcheck_status=ok`. **GitHub
remote push** не часть Track B — repo готов к выкладке, но
пушить — operator action.

## Track A detail (закрыт)

- **Parallel Track A — Full Real 1cv8-backed Write Path
  (закрыт на Step 7).**
  Цель — **доведение существующего write-core до finished
  real-write behavior**, а не новый MCP-surface sprint.
  Конкретно:
  - `apply_config_from_files` и
    `update_database_configuration` сегодня остаются
    Phase 2 stub-backed. Track A переводит их на honest
    dual-mode contract с real binary-backed dispatch'ем
    при наличии operator-declared argv-template'ов;
    config-time fallback на stub при отсутствии binary
    contract'а сохраняется без изменений; runtime-failure
    при non-zero exit subprocess'а — honest failure без
    silent stub fallback'а;
  - `create_dump_snapshot` (binary-backed branch которого
    был ship'нут на Phase 6 / Step 2) нормализуется
    под общий shared payload-контракт со всеми тремя
    binary-backed write-tool'ами;
  - Один **реальный multi-step round-trip** на reference
    stand'е с настоящим 1cv8 binary'ом (real DumpCfg →
    real apply (LoadCfg) → real UpdateDBCfg) выполняется
    end-to-end и фиксируется как воспроизводимый
    runbook;
  - Существующие product-layer boundary'и
    (`run_guided_workflow`, `run_rollback_assistant`,
    `run_real_stand_smoke_test`,
    `inspect_enterprise_foundation`) используются
    поверх real write path **без правок собственной
    логики** — весь real binary-backed dispatch живёт
    в write-server'е, не в product layer'е.

Это **post-phase completion track**, **не** новая Phase 7.
Безопасность Phase 1–6 не размывается:
`run_write_flow` остаётся единственным mutating-путём,
intelligence-server остаётся read-only,
`onec_policy_engine` не импортируется в
product/intelligence, нет back-door write channel'а из
product layer'а, нет `shell=True`, audit append-only,
fail-closed по умолчанию. Default trek'а — registries
остаются `read=15 / write=25 / intelligence=16` без
изменений; любое отклонение honestly мотивируется в
шаговом документе.

План трека и step-map: [`docs/architecture/track-a-real-write-path-plan.md`](docs/architecture/track-a-real-write-path-plan.md),
[`docs/architecture/track-a-real-write-path-step-map.md`](docs/architecture/track-a-real-write-path-step-map.md).
Step 1 (planning), **Step 2 (real binary-backed
`apply_config_from_files` contract)**, **Step 3 (real
binary-backed `update_database_configuration` contract)**,
**Step 4 (internal unification of binary-backed write
contract)** и **Step 5 (product-layer integration over
real write path)** — пройдены. Step 2 расширил
`EnvironmentConfig` полем `onec_applycfg_command_template`;
Step 3 — симметричным полем `onec_updatedb_command_template`
(loader fail-closed на bad shape; placeholder whitelist
tighter — без `{output_path}` / `{source_dump_path}`,
поскольку UpdateDBCfg операционно работает на живой
инфобазе). `apply_config_from_files(...)` и
`update_database_configuration(...)` оба переведены на
dual-mode dispatcher с одной и той же дисциплиной:
config-time fallback на stub при отсутствии binary
contract'а; binary-backed branch при наличии (реальный
subprocess через `onec_process_runner.run_process`,
captured stdout/stderr, timeout 300 s); runtime failure
в binary-backed ветке = honest failure без silent
fallback'а на stub. **Step 4 — internal-only refactor:**
все три binary-backed write-tool'а
(`create_dump_snapshot`, `apply_config_from_files`,
`update_database_configuration`) теперь сидят на одном
shared internal helper layer (новый internal модуль
`apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`
— excerpt cap, default timeout, render-time placeholder
substitution engine, stub/render-fail/start-fail/
binary-backed payload field assembly, shape verify
helper); три duplicated константы
(`_*_OUTPUT_EXCERPT_LIMIT`) и три duplicated константы
(`_*_DEFAULT_TIMEOUT_SECONDS`) удалены, единые источники
правды теперь в `binary_dispatch`. Tool-specific
placeholder whitelists остаются **per-tool** (намеренно
не объединены в superset). Дополнительно Step 4 закрыл
payload-discipline gap у `create_dump_snapshot`: до
refactor'а несколько ветвей (stub success, render-fail,
PlatformError-fail, dump-meta-fail, mkdir-fail) не несли
всех шести honest-mode полей; теперь **каждая** ветка
**каждого** из трёх tool'ов несёт все шесть
(`mode`, `binary_invoked`, `exit_code`,
`command_preview`, `stdout_excerpt`, `stderr_excerpt`)
честно (`None` / `False` где не применимо). **Step 5 —
product-layer surface-only update:** boundaries в
`apps/platform` теперь честно отражают, что real write
path есть для всех трёх binary-backed write-tool'ов.
Q7 закрыт: `run_real_stand_smoke_test(...)` plan summary
(и module docstring) больше не утверждают "Phase 2
stubs are NOT rewritten"; вместо этого summary честно
называет три tool'а с their honest dual-mode contract'ом
после Track A / Steps 2–4, явно отмечает что smoke сам
по себе остаётся bounded probe и что multi-step
round-trip — это Track A / Step 6, а не этот surface.
Q8 закрыт: `inspect_enterprise_foundation(...)` теперь
оценивает binary section по полному real-write
contract'у — `onec_binary_path` плюс **три** command
template'а (dumpcfg, applycfg, updatedb), score range
0..4. На prod-like config'ах отсутствие любого из трёх
template'ов — error finding с recommended_actions; на
non-prod — presumed warning. `foundation_level='strong'`
требует full-contract + чистые остальные секции.
Step 1–4 product-config'и без apply/updatedb template'ов
продолжают загружаться без изменений. Никаких новых MCP
tool'ов, никаких изменений в registries (read=15 /
write=25 / intelligence=16), никаких импортов
`onec_policy_engine` из product layer'а, никаких
изменений `onec-config` schema (full contract уже
существовал после Steps 2–3 — Step 5 только начал
**использовать** его в product surface'е). Operator-facing
ToolResult shape / argv grammar — без изменений.
**Step 6 (reference stand multi-step round-trip) —
закрыт.** Operator-driven exercise по runbook'у
`docs/runbooks/track-a-reference-stand-round-trip.md`
прошёл honestly на real 1cv8 binary'е
(`C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe`)
и реальной file-based инфобазе InfoBase6
(`C:/Users/user/Documents/InfoBase6`). Все три
binary-backed write-tool'а отработали зелёным:
A.2 — `create_dump_snapshot` через
`/DumpConfigToFiles` (`mode='binary-backed'`,
`binary_invoked=True`, `exit_code=0`); A.4 —
`apply_config_from_files` через `/LoadConfigFromFiles`
(`stage='completed'`, mutating audit row написан);
A.5 — `update_database_configuration` через
`/UpdateDBCfg` (`stage='completed'`, mutating audit
row написан). На диске реальный
`Configuration.xml` + поддиректории, два backup
snapshot'а перед mutating операциями, два pre-mutating
dump-snapshot'а (созданы `run_write_flow`'ом
автоматически), и **две** append-only audit row'и
для двух mutating операций. Standalone
`create_dump_snapshot` audit row не пишет by design —
он не идёт через `run_write_flow`; pre-apply /
pre-updatedb dump подтверждается через
`details.dump_snapshot_path` mutating row'и. Runbook +
local closure logic выровнены под фактическое
поведение (две mutating audit row + dump_snapshot_path
в details). Никаких production-правок Step 6 не
делал — dual-mode contract уже введён Track A /
Steps 2–4, unified `binary_dispatch` уже на месте,
product-layer surface уже обновлён Step 5. **Step 7
(final integration pass and Track A closure) —
закрыт без production-правок:** existing evidence
Step 6 round-trip'а покрывает acceptance criteria
1–5 (full real binary-backed contract, multi-step
real round-trip, product-layer integration, no
silent fallback, honest payload discipline);
discipline asserts criteria 6–10 удовлетворены
(registries `read=15 / write=25 / intelligence=16`
без drift'а; ноль импортов `onec_policy_engine` под
`apps/platform/src` и
`apps/mcp-intelligence-server/src`; нет back-door
write channel'а; operator-facing messages честные;
Track A closed как documented status). Закрытие
выполнено только обновлением closure-status в
`README.md` и `PROJECT-STATUS.md` — никаких новых
запусков 1cv8.exe для Step 7 не понадобилось.

Что **не** входит в Track A (и **остаётся** будущей
работой после закрытия трека): enterprise super-set
(SSO/RBAC, multi-tenant, secrets vault, federated
audit, policy-as-code, multi-instance HA), web-UI,
полный AST-парсер, полная metadata-вселенная, полная
rollback/delete-вселенная, production-grade MCP
transport, packaging ecosystem, multi-version matrix
в полном объёме. Эти направления остаются **другими**
parallel track'ами после Phase 6 / Track A — Track A
их не открывал и не закрывал. После закрытия Track A
ни один из них автоматически не открывается;
открытие следующего трека — отдельное решение
оператора проекта.

Что Track A **реально закрыл** (на основе Steps 2–7
и Step 6 evidence на InfoBase6):

- real binary-backed dispatch для **всех трёх** ранее
  stub-backed-путей (`create_dump_snapshot`,
  `apply_config_from_files`,
  `update_database_configuration`);
- final contract correctness: один shared
  `binary_dispatch` helper, per-tool placeholder
  whitelists, fail-closed на unknown placeholder,
  fixed timeout cap;
- no silent fallback: при non-zero exit
  binary-backed branch'а tool возвращает honest
  `ok=False` с populated `mode='binary-backed'` /
  `exit_code != 0`, без тихого downgrade'а на
  stub;
- honest payload discipline: каждая ветка каждого
  из трёх tool'ов несёт все шесть unified
  honest-mode полей (`mode`, `binary_invoked`,
  `exit_code`, `command_preview`, `stdout_excerpt`,
  `stderr_excerpt`);
- reference-stand execution layer proven: real
  multi-step round-trip отработал на InfoBase6, audit
  honest, snapshot trees физически на диске.

Что Track A **не делает** «готовым индустриальным
продуктом** даже после closure: операторские
credentials всё равно out-of-band (не в config),
multi-version matrix на всех 1С версиях не пройдена
(закрыт single-version smoke на 8.3.27.1859),
production runbook ecosystem не построен
(один reference-stand runbook), packaging /
installer / signed distribution не сделан,
enterprise super-set не открыт, web-UI / dashboard
frontend не сделан, полная rollback-вселенная не
покрыта (whitelist расширен до 6 tools после
Track F / Step 4 — `add_catalog_attribute`,
`add_document_attribute`, `add_form_attribute`,
`add_form_element`, `append_module_method`,
`replace_module_method_body` — но это всё ещё
narrow set, 6 of 25 mutating tools; multi-file /
DB-schema / `create_*` / public `delete_*`
остаются categorically out-of-scope),
полный AST-парсер XML/BSL не написан. Это
явные honest constraints, **не** скрытые гэпы.

Документы parallel-track'ов:

- `docs/architecture/track-a-real-write-path-plan.md` —
  план **Parallel Track A — Full Real 1cv8-backed Write
  Path**: post-phase completion track для доведения
  оставшихся Phase 2 stub-backed-путей
  (`apply_config_from_files`,
  `update_database_configuration`) до honest dual-mode
  contract'а с real binary-backed dispatch'ем; нормализация
  `create_dump_snapshot` real path'а под общий
  payload-контракт; один реальный multi-step round-trip на
  reference stand'е. Не Phase 7. Без расширения MCP
  surface'а.
- `docs/architecture/track-a-real-write-path-step-map.md`
  — семь шагов: planning (documentation entry) → real
  apply → real update-db → unify dump-snapshot + payload
  discipline → product-layer integration → reference stand
  round-trip → final integration pass + closure.

Архивные планы:

- `docs/architecture/phase-6-industrialization-plan.md` —
  план **Phase 6 — Industrialization & Completion Track**
  (исходник — пройден).
  Это **не** очередное расширение MCP tool surface и **не**
  ещё один технический MVP — это специально выделенная
  фаза доведения продукта до **finished / deployable**
  состояния поверх уже готового ядра Phase 1–5: реальный
  1cv8-backed dispatch (хотя бы для одного Phase 2
  stub-backed пути), исполнимый rollback хотя бы для
  одного класса write-tool'ов, короткий install/setup
  сценарий, real-stand end-to-end smoke на reference
  stand'е, runtime hardening (логи, restart policy),
  operator/admin/developer manuals + runbooks как
  standalone docs, foundation для enterprise-трека (без
  полного enterprise-супер-сета). Шесть продуктовых
  блоков (A — real 1cv8 execution; B — full rollback /
  recovery; C — installer / packaging; D — metadata
  completion / structural editing; E — runtime
  hardening; F — operator UX / docs / runbooks; G —
  enterprise foundation). 10 проверяемых критериев
  приёмки. Явный «что НЕ входит в фазу» (полная
  enterprise-вселенная, AST-парсер всей кодовой базы,
  web-UI, multi-instance HA — out of Phase 6 scope).
- `docs/architecture/phase-6-step-map.md` — стартовый
  implementation map (8 шагов): planning → real 1cv8
  contract → installer → rollback execution → metadata
  completion → runtime hardening → real-stand validation
  + docs → final integration pass.

## По какому документу ведётся работа

Разработка ведётся строго по внутреннему **ТЗ v1.1**. Все решения по структуре,
именам пакетов и границам ответственности согласованы с этим документом.

## Структура репозитория

```
1c-agent-platform/
├── apps/         # Исполняемые MCP-серверы (read / write / intelligence)
├── packages/     # Переиспользуемые библиотеки платформы
├── docs/         # Архитектура, спецификации, безопасность, runbooks, API
├── examples/     # Демонстрационные инфобазы, дампы, примеры патчей
└── scripts/      # Скрипты для разработки, тестов и релизов
```
