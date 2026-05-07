# 1C Agent Platform

Проект **1C Agent Platform** — собственная MCP-платформа (Model Context Protocol) для работы
ИИ-агентов с конфигурацией и инфобазами 1С:Предприятие.

## Quickstart

> **Что это.** MCP-платформа для работы AI-агентов с конфигурацией и
> инфобазами 1С:Предприятие. На сегодня закрыты Phases 1–6 (read /
> write / metadata / intelligence / product layer / industrialization)
> и Parallel Track A — full real binary-backed write path
> (DumpCfg → LoadConfigFromFiles → UpdateDBCfg), отработанный на
> reference stand'е. Активный сейчас трек — Track B (productization
> & delivery polish), результаты которого вы видите в трёх блоках
> ниже.

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
  включая `track-a-reference-stand-round-trip.md`.
- [`docs/architecture/`](docs/architecture/) — phase- и track-plans
  + step maps (включая Track B planning).
- [`PROJECT-STATUS.md`](PROJECT-STATUS.md) — детальный статус фаз
  и треков с per-step deliverables.

### Что Quickstart **не** обещает

Этот entry — про **локальный** install и check. Он **не**: production-
grade MCP transport (нет authentication / authorisation / network
hardening), **не** installer ecosystem (`.msi` / `.deb` / GUI wizard
/ signed binary distribution), **не** web UI / dashboard frontend,
**не** enterprise-ready deployment (SSO/RBAC, multi-tenant, secrets
vault, federated audit storage, multi-instance HA), **не** hot
reload / OS-level service supervision. Эти направления — out of
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
закрыты два post-phase completion track'а:

- **Parallel Track A — Full Real 1cv8-backed Write Path** —
  закрыт на Step 7 (final integration pass and Track A
  closure).
- **Parallel Track B — Productization & Delivery Polish** —
  закрыт на Step 6 (final integration pass and Track B
  closure).

## Active parallel track

После closure'а Track B открыт третий post-phase track —
**Parallel Track C — Packaging & Installer Delivery**.
Цель — довести продукт до состояния, в котором его удобно
передать другому человеку как **packaged unit / process**:
release-facing layout polish, reproducible install sequence
checklist, pre-handoff sanity check, release handoff
документация, единый release entrypoint map. Это **не**
новый execution-core sprint, **не** enterprise track, **не**
GUI installer wizard, **не** signed binary distribution,
**не** package-manager publication.

Track C сейчас на **Step 1 (planning)** — ship'нуты только
два planning-документа
(`docs/architecture/track-c-packaging-installer-delivery-plan.md`,
`docs/architecture/track-c-packaging-installer-delivery-step-map.md`);
никаких code changes Step 1 не делал, registries `read=15 /
write=25 / intelligence=16` без drift'а.

Что **не** входит в Track C (повтор для ясности): GUI
installer wizard, `.msi` / `.deb` / signed binary
distribution, publication к package managers (PyPI /
Chocolatey / winget / apt), systemd / Windows Service
registration, hot reload, web-UI / dashboard frontend,
полный enterprise super-set (SSO/RBAC, multi-tenant,
secrets vault как сервис, federated audit storage,
policy-as-code DSL, multi-instance HA), production-grade
MCP transport, multi-version 1С matrix, полный AST-парсер
XML/BSL, полная rollback/delete-вселенная, новые MCP tools,
production code rewrite. Эти направления остаются
другими parallel track'ами после Phase 6 / Track A /
Track B / Track C.

Следующий шаг по Track C — **Step 2 (release-facing
`scripts/release/` layout полишинг)**: тонкое расширение
existing release scripts слоя через `verify-release.ps1`
(pre-handoff sanity check) + UPDATE
`scripts/release/README.md`. **GitHub remote push —
operator action, не часть трека.**

Документы трека: `docs/architecture/track-c-packaging-installer-delivery-plan.md`,
`docs/architecture/track-c-packaging-installer-delivery-step-map.md`.

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
покрыта (whitelist остаётся на двух tool'ах),
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
