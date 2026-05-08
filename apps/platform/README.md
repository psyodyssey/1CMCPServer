# platform — product layer of 1C Agent Platform

Продуктовый слой Phase 5: тонкая обвязка поверх уже готовых
read- / write- / intelligence-серверов. Это **не** MCP-сервер
сам по себе — здесь нет registry, нет публичных MCP tool'ов,
нет MCP-транспорта.

Пакет: `onec_platform` (`apps/platform/src/onec_platform/`).

## Что сейчас внутри (Phase 5 закрыта + Phase 6 закрыта на Step 9 — final integration pass)

> **Operator / Administrator / Developer guides** теперь живут как
> standalone-документы в корневой `docs/` (Phase 6 / Step 7):
>
> - [`docs/operator-manual.md`](../../docs/operator-manual.md)
> - [`docs/administrator-manual.md`](../../docs/administrator-manual.md)
> - [`docs/developer-manual.md`](../../docs/developer-manual.md)
> - [`docs/runbooks.md`](../../docs/runbooks.md)
>
> Этот README остаётся техническим справочником по продуктовому
> слою (boundary-функции, modes, findings, registry counts), но
> ежедневная operator/admin/developer-документация выделена туда.

Минимально-честный bootstrap-контракт:

- **Модели** (`models.py`) — простые dataclass'ы, без поведения:
  - `ProductConfig` — верхнеуровневый product-конфиг (имя
    продукта, имя профиля, ссылка на `ProjectConfig`,
    дефолтное окружение, server toggles, bootstrap settings).
  - `ProductServerToggles` — какие из трёх серверов
    (`read`/`write`/`intelligence`) этот профиль ожидает
    запускать. Doctor проверяет importability только
    включённых серверов.
  - `ProductBootstrapSettings` — настройки bootstrap'а:
    `work_dir`, `require_dump_path`, `require_base_path`,
    `require_python`. Все три `require_*` — `True` по
    умолчанию; отключение видно в отчёте, не молча.
  - `DoctorFinding` — одна находка doctor'а с явным
    `severity` (`ok`/`warning`/`error`) и `confidence`
    (`confirmed`/`presumed`).
  - `DoctorReport` — суммарный отчёт doctor'а: список
    findings, `error_count`, `warning_count`,
    `recommended_actions`.
  - `BootstrapResult` — результат bootstrap-вызова:
    `ok` (отработал ли сам шаг), `product_name`,
    `profile_name`, `default_environment`, `doctor`,
    `message`.
- **Loader** (`loader.py`):
  - `load_product_config(data: dict) -> ProductConfig` —
    структурная валидация dict'а; делегирует
    `onec_config.load_project_config` для секции
    `project`. Fail-closed через `ValueError`.
  - `load_product_config_from_json_file(path) -> ProductConfig`
    — читает JSON-файл, парсит, передаёт в
    `load_product_config`. Все file-system / JSON-parse
    ошибки конвертируются в `ValueError` для единообразия.
- **Doctor** (`doctor.py`):
  - `run_prereqs_doctor(config: ProductConfig) -> DoctorReport`
    — минимальный, но реальный doctor. **Никогда не
    бросает исключений**. Выполняет:
    1. resolve `default_environment` в `project.environments`
       (defensive — loader уже проверил);
    2. `base_path` существует (если
       `require_base_path=True`);
    3. `dump_path` существует (если
       `require_dump_path=True`);
    4. `python` на `PATH` через `shutil.which("python")`
       (если `require_python=True`);
    5. `http_base_url` распарсивается в scheme + host —
       помечено как **presumed** (реального HTTP-probe
       нет; это задача Step 4 health dashboard);
    6. для каждого включённого server toggle —
       importability через `importlib.util.find_spec`;
    7. опциональный `bootstrap.work_dir` существует и
       является директорией.
- **Bootstrap entrypoint** (`bootstrap.py`):
  - `bootstrap_product(data: dict) -> BootstrapResult` —
    boundary-функция. Никогда не бросает. На битом
    конфиге — `ok=False` с понятным `message`. На
    валидном — `ok=True` с заполненным `doctor`.
  - `bootstrap_product_from_json_file(path) -> BootstrapResult`
    — то же, но читает JSON-файл. Тоже не бросает.
- **Runtime models** (Step 3, в `models.py`):
  - `ProductServiceSpec(name, enabled, command, working_dir,
    env_overrides)` — декларативный спек одного long-lived
    сервиса. `command` — **список аргументов**, не shell-строка.
    `command=None` означает «оператор не сконфигурировал runtime
    команду» — orchestration делает fail-closed для этого
    сервиса, ничего не угадывая.
  - `ProductRuntimeSettings(services: dict[str, ProductServiceSpec])`
    — секция `runtime` верхнеуровневого конфига; ключи
    словаря — операторские имена сервисов
    (рекомендуется `read`/`write`/`intelligence`).
  - `RuntimeServiceState` — runtime snapshot одного сервиса:
    `name`, `enabled`, `configured`, `status`, `command`,
    `working_dir`, `env_override_keys`, `pid`, `started_at`,
    `last_error`. `env_override_keys` — это **ключи** override'ов
    (не значения), чтобы state-файл не утаскивал секреты.
  - `RuntimeStateFile` — формат файла под
    `<work_dir>/.runtime/runtime-state.json`:
    `schema_version` + product/profile/env идентификаторы +
    `services` map. Schema unsupported → fail-closed через
    `ValueError`.
  - `RuntimeOperationResult` — результат `start` / `stop` /
    `reload`: `ok` (отработал ли шаг), `operation`,
    `services` (полный snapshot после операции),
    `findings`, `message`.
  - `RuntimeStatusResult` — результат `get_product_runtime_status`:
    тот же набор полей + `state_path`.
  - Допустимые `status`-значения (`RUNTIME_STATUSES`):
    `configured` (готов стартовать, ещё не стартовал) /
    `running` (state видит running, PID жив) /
    `stopped` (явно остановлен) /
    `stale` (state видит running, но PID мёртв) /
    `error` (последний start/stop провалился) /
    `disabled` (`enabled=False`) /
    `missing` (нет команды или нет спека).
- **Process control primitives** (`process_control.py`,
  Step 3): cross-platform helper'ы на чистом stdlib —
  `is_pid_alive(pid)`, `terminate_pid(pid)`,
  `spawn_service(command, working_dir, env_overrides)`.
  POSIX: `os.kill(pid, 0)` + `SIGTERM`. Windows:
  `OpenProcess`+`WaitForSingleObject`+`TerminateProcess`
  через `ctypes`. На Windows `os.kill(pid, 0)` намеренно
  **не** используется (некоторые сборки CPython фактически
  вызывают `TerminateProcess`, что было бы катастрофой
  для liveness-пробы).
  Spawn детачит stdio в `DEVNULL` и стартует ребёнка в
  своей сессии / process group, чтобы Ctrl-C в родительской
  оболочке не убивал сервис.
- **Runtime state store** (`state.py`, Step 3):
  - `runtime_dir(work_dir)` / `state_file_path(work_dir)` —
    helper'ы для путей. `.runtime/` — платформенно-владенный
    подкаталог, создаётся автоматически. Сам `work_dir`
    создаёт оператор, **не** платформа.
  - `read_state(work_dir) -> RuntimeStateFile | None` — читает
    state, fail-closed через `ValueError` на битый JSON или
    неподдерживаемый schema_version. Отсутствие файла — не
    ошибка, а `None`.
  - `write_state(work_dir, state) -> Path` — атомарная запись:
    tmp + `os.fsync` + `os.replace`.
- **Runtime orchestration boundary** (`runtime.py`, Step 3):
  четыре boundary-функции, **никогда не бросают**:
  - `start_product_runtime(data, *, only=None) ->
    RuntimeOperationResult` — поднимает только
    enabled+configured сервисы; **идемпотентно**: если PID жив
    и state говорит `running`, не дублирует процесс, а отдаёт
    finding `runtime_already_running`.
  - `stop_product_runtime(data, *, only=None) ->
    RuntimeOperationResult` — гасит только то, что state
    видит `running`/`stale`. Если процесс уже мёртв — чистит
    state, не считает это ошибкой.
  - `get_product_runtime_status(data) -> RuntimeStatusResult`
    — read-only snapshot. Если state видит `running`, но
    PID мёртв → отдаёт `stale` в результате, **не**
    переписывая state-файл (это работа start/stop/reload).
  - `reload_product_runtime(data, *, only=None) ->
    RuntimeOperationResult` — **controlled stop-then-start**,
    не hot reload. Это явно зафиксировано: stop pass +
    start pass с агрегированными findings.
  - У всех четырёх есть `_from_json_file` варианты для
    JSON-файлового потока.
  - `only=[…]` — surgical-фильтр: операция применяется только
    к перечисленным сервисам; неизвестные имена — warning, не
    abort.
- **Dashboard models** (Step 4, в `models.py`):
  - `DashboardSectionResult(name, ok, source,
    confirmed_findings, presumed_findings, recommended_actions,
    payload, message)` — одна секция dashboard'а; за каждой
    секцией стоит ровно один источник сигнала (`source` —
    маркер происхождения, например `platform.bootstrap_product`,
    `read.check_runtime_health`,
    `intelligence.analyze_runtime_issue`).
  - `DashboardVerdict(overall_status, ready_for_workflows,
    blocking_issues, warnings, rationale)` — верхнеуровневый
    rule-based вердикт. `overall_status ∈ {healthy, degraded,
    blocked}` — единая константа `DASHBOARD_OVERALL_STATUSES`.
    Каждое правило записано в `rationale` отдельной строкой,
    чтобы оператор мог вручную перепроверить вердикт.
  - `EnvironmentDashboardResult(ok, product_name, profile_name,
    default_environment, work_dir, state_path, sections,
    verdict, confirmed_findings, presumed_findings,
    recommended_actions, sources_used, message)` — итоговый
    payload. `confirmed_findings` / `presumed_findings`
    aggregated по всем секциям, и каждый код тагируется
    префиксом `<section>/<original_code>` для трассируемой
    provenance.
- **Dashboard aggregation boundary** (`dashboard.py`, Step 4):
  - `build_environment_dashboard(data) ->
    EnvironmentDashboardResult` — boundary, **никогда не
    бросает**. Resolve config → run **6 секций** в фиксированном
    порядке → compute verdict → aggregate findings/actions/
    sources → собрать `EnvironmentDashboardResult`. На любой
    непредвиденной ошибке внутри sub-tool'а соответствующая
    секция помечается `ok=False` с error-finding'ом, но сам
    dashboard остаётся `ok=True`. Полный `ok=False` — только
    если product config не загружается.
  - `build_environment_dashboard_from_json_file(path) ->
    EnvironmentDashboardResult` — то же, но из JSON-файла.
- **Workflow models** (Step 5, в `models.py`):
  - `WorkflowStepResult(name, kind, ok, source, payload,
    message)` — один шаг workflow-прогона.
    `kind ∈ {precondition, intelligence, preview, mutating,
    verify, diagnostic, audit}`. `source` — провенанс
    (например `intelligence.suggest_metadata_patch_plan`,
    `write.add_catalog_attribute`).
  - `WorkflowPlan(workflow_name, target_kind, target_name,
    summary, suggested_tools, suggested_write_tools,
    impact_level, risk_level)` — операторски-видимый план.
    `summary` — короткие human-readable bullets;
    `suggested_*` — **только реально зарегистрированные**
    public tool names (см. дисциплину ниже).
  - `WorkflowRunResult` — итоговый payload boundary-функции:
    `ok`, `workflow_name`, `mode`, `product_name`,
    `profile_name`, `default_environment`,
    `ready_for_workflows`, `execution_performed`, `plan`,
    `steps`, `confirmed_findings`, `presumed_findings`,
    `recommended_actions`, `suggested_tools`,
    `suggested_write_tools`, `write_results`,
    `verify_results`, `last_write_operation`,
    `rollback_hint`, `message`.
  - Допустимые `mode`-значения (`WORKFLOW_MODES`):
    `preview` (план собран, ничего не выполнялось) /
    `executed` (mutating workflow выполнялся; success или
    failure определяется по `ok`) / `diagnostic`
    (read-only stand-health-check) / `blocked`
    (mutating workflow остановлен dashboard'ом) /
    `rejected` (config или params отвергнуты).
  - Известные имена workflow'ов (`WORKFLOW_NAMES`):
    `safe-add-attribute`, `safe-add-module-method`,
    `stand-health-check`. Любое другое → fail-closed
    через `mode=rejected`.
- **Guided workflow boundary** (`workflow.py`, Step 5):
  - `run_guided_workflow(data, *, workflow_name, params,
    confirm_execute=False) -> WorkflowRunResult` — единая
    точка входа. **Никогда не бросает.** На любой
    непредвиденной ошибке runner'а — `ok=False`,
    `mode=rejected`, finding `workflow_unexpected_error`.
  - `run_guided_workflow_from_json_file(path, ...)` —
    JSON-файловый вариант.
  - Под капотом — три private runner'а
    (`_run_safe_add_attribute`, `_run_safe_add_module_method`,
    `_run_stand_health_check`), приватные helper'ы для
    провенанс-тагирования findings, агрегации и
    нормализации foreign ToolResult'ов в наш
    `DoctorFinding` shape.
- **Recovery models** (Step 6, в `models.py`):
  - `OperationHistoryEntry(position, operation_id, tool_name,
    environment, base_id, status, message, raw_line)` —
    нормализованная audit-запись. `position` — 0-based индекс
    в audit JSONL (timestamp в audit-формате нет, поэтому
    позиция — единственный стабильный монотонный порядок).
  - `OperationHistorySummary(total, ok_count, error_count,
    other_count)`.
  - `OperationHistoryResult` — boundary-результат
    history viewer'а: `ok`, контекст продукта,
    `audit_path` (всегда резолвится, даже когда файла нет),
    `entries`, `summary`, `findings`, `message`.
  - `OperationInspectResult` — focus-результат: `ok`,
    `operation_id`, **`operation_found`** (источник правды
    о том, нашлась ли операция), `history_entry`,
    `rollback_hint`, **`automatic_recovery_supported`**,
    `operator_summary`, `findings`, `suggested_tools`,
    `suggested_write_tools`, `message`.
  - `RollbackPlan(operation_id, tool_name,
    automatic_recovery_supported, summary, suggested_tools,
    suggested_write_tools, suggested_backup_root,
    suggested_dump_root)` — operator-visible план;
    `automatic_recovery_supported` — самостоятельный
    boolean, явно показывающий, готов ли assistant
    исполнить recovery автоматически.
  - `RollbackAssistantResult` — assistant-результат: всё то
    же что у workflow-result'а Step 5, плюс
    `operation_found`, `history_entry`, `history_summary`,
    `dashboard_summary`, `rollback_hint`. `mode` ∈
    `RECOVERY_MODES`.
  - Допустимые `mode`-значения (`RECOVERY_MODES`):
    `preview`, `executed`, `blocked`, `unsupported`,
    `rejected`. Step 6 не отдаёт `executed` ни для одной
    операции (см. ниже).
- **Rollback / recovery / audit boundary** (`recovery.py`,
  Step 6):
  - `get_operation_history(data, *, limit=None,
    only_status=None) -> OperationHistoryResult` — read-only
    history viewer; **никогда не бросает**. `ok=True`
    одинаково покрывает «N операций загружено» и «audit
    файла ещё нет» (чистое окружение без записей).
  - `inspect_operation(data, *, operation_id) ->
    OperationInspectResult` — focus на одной операции;
    подтягивает `prepare_rollback_hint`. Missing operation
    → `ok=False, operation_found=False` (caller ветвится
    по `operation_found`, а не по message).
  - `run_rollback_assistant(data, *, operation_id,
    confirm_execute=False) -> RollbackAssistantResult` —
    preview / advisory assistant. **Никогда не бросает.**
    Mode resolution:
    - `confirm_execute=False` → `mode=preview`,
      `execution_performed=False`;
    - `confirm_execute=True` + dashboard не ready →
      `mode=blocked`, `ok=False`, preview всё равно
      построен;
    - `confirm_execute=True` + dashboard ready + tool в
      whitelist `_AUTOMATIC_RECOVERY_SUPPORTED` →
      зарезервировано под executed (на Step 6 unreachable);
    - `confirm_execute=True` + dashboard ready + tool **не**
      в whitelist → `mode=unsupported`, `ok=True`,
      честное сообщение оператору.
  - У всех трёх boundary-helpers — `_from_json_file`
    варианты для JSON-файлового потока.

## Что такое guided workflow layer (Step 5)

Step 5 даёт **операторски-ориентированную** обёртку поверх
intelligence (план/риск/impact) и write (реальное mutating
исполнение через `run_write_flow`). Цель — не «ещё одни
tool'ы», а сценарий, по которому продукт безопасно проводит
оператора от намерения до проверенного результата:

1. **Precondition.** Workflow runner строит Step 4 dashboard
   и смотрит на `verdict.ready_for_workflows`. Mutating
   workflow'ы (`safe-add-attribute`, `safe-add-module-method`)
   стартуют только если `ready_for_workflows == True`. Если
   нет — `mode=blocked`, никакого исполнения, никакого
   write-side вызова.
2. **Intelligence-сбор.** Дёргаются read-only intelligence
   tool'ы (`estimate_change_impact`, `suggest_safe_change_order`,
   `suggest_metadata_patch_plan`,
   `summarize_configuration_risk`, плюс
   `find_affected_modules` для метода). Их результаты
   попадают в `WorkflowStepResult` со своим `source`.
3. **Operator-visible plan.** `WorkflowPlan.summary` — короткие
   bullets для оператора: что будет делаться, какой impact,
   какой risk, какие реальные write-tool'ы будут вызваны и
   что это пройдёт через `run_write_flow`.
4. **Confirm gate.** Без `confirm_execute=True` mutating
   workflow завершается в `mode=preview`, ровно с
   `execution_performed=False` и пустыми `write_results`.
   Никаких silent apply.
5. **Mutating execution.** При `confirm_execute=True`
   workflow дёргает **реальный** public write-tool —
   `add_catalog_attribute` / `add_document_attribute` /
   `append_module_method`. Эти tool'ы внутри сами проходят
   через `run_write_flow` (preflight → backup snapshot →
   dump snapshot → operation → verify → audit).
   Workflow runner **не обходит** эти гарантии.
6. **Verify.** После успешного write — реальный
   `verify_attribute_exists` или `verify_module_contains`.
   Если write провалился, verify не запускается (нет
   смысла верифицировать неудачное изменение).
7. **Audit / rollback hint.** Workflow дёргает
   `describe_last_write_operation` для получения свежего
   `operation_id`, затем `prepare_rollback_hint` по этому
   id. Оба — read-only; их сбой не влияет на verdict.

### Три текущих workflow

#### `safe-add-attribute`

Поддерживаемые `target_kind`: `catalog` (→
`add_catalog_attribute`) и `document` (→
`add_document_attribute`).

Параметры:

```json
{
  "target_kind": "catalog" | "document",
  "object_name": "Items",
  "attribute_spec": {"name": "Title", "type": "String", "synonym": "..."}
}
```

Verify использует `verify_attribute_exists` с
`object_name = Справочник.<name>` или `Документ.<name>`,
который собирается внутри workflow.

#### `safe-add-module-method`

Параметры:

```json
{
  "module_relative_path": "CommonModules/Helpers/Ext/Module.bsl",
  "method_spec": {"name": "PrepareReport", "body": "...", "export": false}
}
```

Verify использует `verify_module_contains` с
`expected_substring = method_spec.name`.

#### `stand-health-check`

Read-only диагностика: `build_environment_dashboard` +
`analyze_runtime_issue` + `summarize_configuration_risk`.
**Не требует** `ready_for_workflows=True` — может
запускаться даже на degraded/blocked окружении, чтобы
оператор видел, что именно сломано. Никогда не выполняет
write-side операций. `mode=diagnostic`,
`execution_performed=False`.

### Дисциплина имён tool'ов

`WorkflowPlan.suggested_tools` и
`WorkflowPlan.suggested_write_tools` фильтруются через
приватный `_allow_only_real_tools(...)`, который проверяет
каждое имя по живому объединению трёх registries
(`mcp_read_server.list_tools()`,
`mcp_write_server.list_tools()`,
`mcp_intelligence_server.list_tools()`) плюс
фиксированному whitelist платформенных boundary-функций
(`bootstrap_product`, `start_product_runtime`,
`build_environment_dashboard`, `run_guided_workflow` …).
Имена, которых нет в этом множестве, **молча
отбрасываются**, чтобы план не утверждал, что у нас есть
tool, которого на самом деле нет. Эта дисциплина
программно проверяется в manual check'е.

### Что workflow layer сейчас НЕ делает

- **Не обходит safety guarantees write-server'а.**
  Каждый mutating step идёт через реальный public
  write-tool, который сам проходит preflight + snapshot +
  verify + audit.
- **Не вводит собственный write channel.** В
  `onec_platform` нет ни одной строчки, которая бы
  что-либо писала в инфобазу или dump в обход существующих
  write-tool'ов.
- **Не делает silent apply.** Mutating workflow без
  `confirm_execute=True` всегда возвращается в
  `mode=preview`. Это поведение покрыто manual check'ом
  (сценарий F).
- **Не рулит rollback'ом.** Step 5 только подтягивает
  `prepare_rollback_hint`, чтобы оператор увидел подсказку.
  Реальный rollback / recovery UX — это Step 6.
- **Не строит UI / web-app.** Возвращается чистый
  структурированный `WorkflowRunResult`.
- **Не делает hot reload / hot apply / push subscription.**
- **Не реализует автоматический retry mutating step'ов**
  при transient-ошибках. Ошибка → честный `ok=False` с
  сохранённым планом и step-details; решение «повторить»
  принимает оператор.
- **Не реализует параметризованный `prepare_intelligence_report`
  внутри `stand-health-check`.** `prepare_intelligence_report`
  требует non-empty `subject`, которого у read-only
  диагностики нет; добавлять синтетический subject было
  бы нечестно. Соответствующие сигналы и так уже видны
  через dashboard и через `analyze_runtime_issue` /
  `summarize_configuration_risk`, которые workflow вызывает
  явно.

## Что такое environment doctor / health dashboard (Step 4)

Step 4 даёт **единую точку чтения состояния продукта** —
read-only aggregation поверх уже готовых сигналов проекта. Это
**не** UI и **не** новый MCP-сервер. Это product-уровневый
aggregation contract, на который Step 5 guided workflows будут
смотреть, чтобы решить «можно ли сейчас безопасно стартовать
mutating workflow».

Источники, из которых собирается dashboard, и соответствующие
секции:

| Section name | Источник | Что несёт |
|---|---|---|
| `bootstrap` | `platform.bootstrap_product` | findings prereqs doctor'а (Step 2) |
| `runtime` | `platform.get_product_runtime_status` | per-service runtime states (Step 3) |
| `read_health` | `read.check_runtime_health` | per-check `dump_path_exists` / `http_gateway` / `search_index` (live) |
| `read_diagnosis` | `read.diagnose_connectivity_issue` | rule-based interpretation `dump_missing` / `gateway_down` / `index_lock` |
| `intelligence_runtime` | `intelligence.analyze_runtime_issue` | aggregated read-side diagnostic findings + probable causes |
| `intelligence_risk` | `intelligence.summarize_configuration_risk` | risk_level (low/medium/high) + reasoning |

Намеренное решение: `read.health_summary` **не** включён в
dashboard. Это легаси-stub helper с булевыми флагами; вызывать
его с дефолтными `gateway_available=True / search_index_available=True`
было бы нечестно (это тихий «всё ок» без реальной проверки), а
вызывать с булями, выведенными из `check_runtime_health`,
дублирует уже учтённый сигнал. Принцип — не дублировать.

Каждая секция явно держит:

- `ok` — отработала ли сама секция (sub-tool ответил, не упал);
- `source` — провенанс (имя sub-tool'а);
- `confirmed_findings` — факты (например, дамп существует, PID
  жив, health-код `gateway_down` присутствует);
- `presumed_findings` — эвристики (probable cause, risk_level,
  rule-based reasoning);
- `recommended_actions` — оригинальные next-step'ы из sub-tool'а;
- `payload` — сырой ответ sub-tool'а для drill-in.

Confirmed/presumed разделение на уровне dashboard'а **не
размывается**: даже у aggregated `confirmed_findings` /
`presumed_findings` каждый item помечен своим `confidence`, и
каждый код префиксован именем секции (например,
`bootstrap/dump_path_missing` или
`intelligence_risk/intelligence_risk_level:medium`).

### Verdict — правила (deterministic, rule-based)

Все правила — read-only, hand-written, без ML. Они полностью
описаны в docstring'е `_compute_verdict` и продублированы здесь
для оператора:

**`blocked`**, если хоть одно условие выполнено:

- bootstrap section возвратил `ok=False`;
- bootstrap doctor нашёл хоть один error-severity finding;
- runtime section возвратил `ok=False` (например, `work_dir`
  невалиден);
- любой **required** runtime service (`enabled=True` +
  `configured=True`) находится в статусе `missing` или `error`;
- read-side health codes содержат `dump_missing` или
  `gateway_down`.

**`degraded`**, если не blocked, но хоть одно условие выполнено:

- любой runtime service в статусе `stale`;
- read-side health codes содержат любой не-ok код, не
  попавший в blocking-список;
- bootstrap doctor имеет хоть один warning;
- intelligence risk_level `medium` или `high`;
- runtime контракт пуст (старый Step 2 product-config без
  секции `runtime`);
- любая секция, кроме trivially-blocking уже учтённых, отдала
  `ok=False`;
- connectivity diagnosis сообщил непустой `problem_code`.

**`healthy`** — иначе.

`ready_for_workflows = (overall_status == "healthy")`. Это
жёсткое правило: Step 5 workflows должны видеть полностью
зелёный dashboard, чтобы запуститься без операторского
override. Любая degradation — это явный сигнал «оператор
смотрит и решает».

### Что считается required service

Сервис считается «обязательным» для verdict-правил **тогда и
только тогда**, когда:

- `spec.enabled == True`, и
- `spec.command` непуст (т.е. сервис «configured» в смысле
  Step 3).

Disabled сервисы не валят verdict как blocking. Сервисы без
команды → собственный `runtime_command_missing:<svc>`
finding на runtime-уровне; они **не** делают verdict
автоматически blocked, потому что оператор мог явно
указать «этим сервисом я управляю снаружи». Если такой
сервис **нужен** — добавьте `command` в product-config.

### Что dashboard сейчас НЕ делает

- **Это не UI.** Никакого web-dashboard, никакой графики;
  возвращается простой структурированный payload.
- **Никакого write-канала.** `build_environment_dashboard` —
  read-only; `onec_platform` не импортирует
  `onec_policy_engine` и не вызывает write-tool'ов.
- **Никаких новых MCP tool'ов** в read/write/intelligence;
  registry трёх серверов не менялись.
- **Никакого реального hot-monitoring.** Один вызов = один
  снимок. Подписки, ws, push — out of scope.
- **Никакой ML-оценки риска / здоровья.** Все правила —
  hand-written и зафиксированы выше.
- **Не подменяет Step 5 guided workflows.** Dashboard
  описывает «что сейчас», не «что делать дальше». Workflows —
  следующий шаг.
- **Не кэширует sub-tool вызовы.** Sub-tools вызываются
  каждый раз: например, `analyze_runtime_issue` внутри
  intelligence-секции сам вызывает `check_runtime_health`
  и `diagnose_connectivity_issue` — те же endpoint'ы
  вызываются один раз read-секцией и снова косвенно
  intelligence-секцией. Это сознательный MVP-компромисс на
  Step 4: дублирование вызовов важнее, чем разделяемое
  состояние, которое усложнило бы failure mode.

## Что такое runtime contract / single entry point (Step 3)

`ProductConfig.runtime` — **декларативный** контракт: набор
именованных сервисов с argv-командами, которые platform layer
готов управлять как long-lived процессами. Поверх этого контракта
`onec_platform` даёт **единую точку входа**:

```
start_product_runtime(...)
stop_product_runtime(...)
get_product_runtime_status(...)
reload_product_runtime(...)
```

Это **не** новый MCP-транспорт внутри read/write/intelligence:
сами серверы в Step 3 не получают встроенный transport. Product
layer запускает только то, что оператор явно описал в
product-config'е. Если сервис не описан или у него нет команды —
orchestration честно отказывается стартовать его, а не угадывает.

Что считается каким status'ом:

- **configured** — сервис заявлен в `runtime.services`, у него
  есть команда, он включён, но ещё не стартовал в текущем
  state-файле.
- **running** — state-файл говорит running, и PID **живой**
  по `is_pid_alive`. Эти два условия проверяются вместе.
- **stopped** — `stop_product_runtime` явно остановил его.
- **stale** — state-файл говорит running, но PID мёртв. Это
  surfaces в любом результате (status / start / stop / reload),
  но **on-disk** state переписывается только при следующем
  start/stop/reload, не при чистом status.
- **error** — последний start/stop провалился; `last_error`
  заполнен.
- **disabled** — `enabled=False` в product-config.
- **missing** — спека нет, либо `command=None`. Fail-closed:
  никаких silent default'ных команд.

Что значит `reload` сейчас (MVP-компромисс): **controlled
stop-then-start**. Сначала всем сервисам в scope (или к указанным
в `only=`) даётся stop pass, затем start pass; PID'ы после reload
гарантированно новые. Это не hot reload и в коде/README прямо
помечено как restart, чтобы оператор не строил иллюзий о zero-
downtime поведении на этом шаге.

Backward compatibility Step 2: если в product-config нет секции
`runtime` — это **не** ошибка загрузки. `bootstrap_product`
работает как раньше; `start/stop/status/reload` отдают `ok=True`
с пустым `services` и warning-finding'ом `runtime_contract_empty`.

## Формат product-config

JSON. Решение Step 2: используем стандартную библиотеку
(`json`), не привнося новых зависимостей. Step 3 расширяет схему
опциональной секцией `runtime`. Минимальный пример со Step 3:

```json
{
  "product_name": "1C Agent Platform",
  "profile_name": "local-dev",
  "default_environment": "local-dev",
  "project": {
    "environments": {
      "local-dev": {
        "name": "Local Dev",
        "base_id": "local-dev",
        "base_path": "C:\\tmp\\infobase",
        "publication_name": "local-dev",
        "http_base_url": "http://localhost:8080/local-dev",
        "dump_path": "C:\\tmp\\dump\\local-dev",
        "timeout_seconds": 30,
        "allow_write": false
      }
    }
  },
  "servers": {
    "read": true,
    "write": true,
    "intelligence": true
  },
  "bootstrap": {
    "work_dir": "C:\\tmp\\platform-work",
    "require_dump_path": true,
    "require_base_path": true,
    "require_python": true
  },
  "runtime": {
    "services": {
      "read": {
        "enabled": true,
        "command": ["python", "-m", "mcp_read_server"],
        "working_dir": null,
        "env_overrides": {}
      },
      "write": {
        "enabled": true,
        "command": ["python", "-m", "mcp_write_server"]
      },
      "intelligence": {
        "enabled": true,
        "command": ["python", "-m", "mcp_intelligence_server"]
      }
    }
  }
}
```

`servers`, `bootstrap` и `runtime` опциональны: если не указаны,
используются дефолты (все toggles включены, все `require_*` = true,
`work_dir` отсутствует, runtime-контракт пустой).

> **Внимание про команды в примере выше.** Аргументы
> `python -m mcp_read_server` приведены как **иллюстрация
> формата**. Фактическое наличие у наших MCP-серверов настоящего
> CLI / `__main__` — отдельный шаг (см. follow-ups в Step 7
> step-map'а). Step 3 даёт honest orchestration **контракт** и
> поднимает **те команды, которые оператор укажет**; он не
> декларирует, что серверы уже имеют production-grade transport.

Для runtime ops обязателен валидный `bootstrap.work_dir` — туда
пишется `<work_dir>/.runtime/runtime-state.json`. Если `work_dir`
не задан / не существует / не директория — boundary помечает
операцию `ok=False` с конкретным error-finding'ом.

## Чего сейчас намеренно ещё нет

- **Production-grade MCP transport внутри read/write/intelligence.**
  Серверы по-прежнему живут как in-process модули; их встроенный
  CLI / `__main__` / production transport — отдельный track,
  не Step 3. Step 3 управляет **теми командами**, которые
  оператор явно описал, и **не** изобретает CLI за серверы.
- **Hot reload.** `reload_product_runtime` сейчас — это
  controlled stop-then-start (новые PID'ы гарантированы).
  Hot reload без перезапуска процесса — отдельный track.
- **Daemon / service manager.** Нет регистрации Windows
  Service / systemd unit. Управление — только PID-уровневое
  на время жизни оркестратора.
- **Захват stdout/stderr дочерних процессов.** Step 3 редиректит
  child stdio в `DEVNULL` для предсказуемости pipe-буфферов.
  Логирование — внутри argv-команды, которую запускает
  оператор. Honest log capture — possible follow-up.
- **Авто-restart упавших сервисов.** Если сервис умер вне
  `stop`, он переходит в `stale`; `start` его поднимет, но
  policy «watch-and-restart» — отдельная подсистема, не Step 3.
- **Реального HTTP / health probe.** `http_base_url`
  только парсится как URL; реальной достижимости не
  проверяем — это Step 4.
- **Реального installer'а под ОС.** Нет .msi, .exe, .deb
  и т.п. Phase 5 / Step 2 — только product-config + doctor
  + bootstrap helper.
- **Интерактивного wizard'а.** Setup декларативный:
  пользователь предоставляет JSON-файл product-config'а.
  Решение фиксировано в Step 2.
- **Реальной 1cv8-binary интеграции.** Это product track
  Step 7 (real-stand / 1cv8 integration).
- **Workflow runner'а.** Step 5.
- **Rollback assistant'а.** Step 6.
- **Запуска write-операций из платформы.** Никогда из этого
  пакета: `onec_platform` — orchestration/product layer, а не
  новый write channel.

## Что такое rollback / recovery / audit UX (Step 6)

Step 6 даёт операторски-удобную **read-only** обёртку над
тем audit JSONL, который уже пишет write-server (Phase 2 +
Phase 3) под `<dump_path>/.audit/audit.jsonl`. Цель — не
«отменять операции магически», а:

1. показать оператору цельную историю прошлых write-операций
   в текущем окружении;
2. дать сфокусированный взгляд на одну операцию по её
   `operation_id`;
3. предоставить честный rollback assistant с разделением
   preview / execute и явным **`automatic_recovery_supported`**
   флагом для каждого class'а write-tool'ов.

### Три boundary-функции

| Boundary | Что делает | Mutating? |
|---|---|---|
| `get_operation_history(data, *, limit, only_status)` | Загружает audit JSONL, нормализует записи, считает counts. | Нет |
| `inspect_operation(data, *, operation_id)` | Находит запись, подтягивает `prepare_rollback_hint`, собирает operator summary. | Нет |
| `run_rollback_assistant(data, *, operation_id, confirm_execute)` | Строит preview-план + dashboard summary + rollback hint; на `confirm_execute=True` с healthy dashboard и whitelist'нутым tool'ом — попыталась бы исполнить recovery (см. ниже). | Нет на Step 6 |

### Modes (`RECOVERY_MODES`)

- **`preview`** — assistant прогнался успешно, ничего не
  исполнялось (`confirm_execute=False`).
- **`executed`** — supported automatic recovery был
  выполнен. Достижим для tools в whitelist'е
  `_AUTOMATIC_RECOVERY_SUPPORTED` (after Track F / Step 4 —
  6 entries: `add_catalog_attribute`, `add_document_attribute`,
  `add_form_attribute`, `add_form_element`,
  `append_module_method`, `replace_module_method_body`).
  Изначально (Phase 5 / Step 6) этот mode был недостижим
  (whitelist пуст); Phase 6 / Step 4 расширил whitelist до
  2 tools; Track F / Step 4 — до 6.
- **`blocked`** — `confirm_execute=True`, но dashboard
  Step 4 не в `ready_for_workflows` состоянии. Preview
  всё равно построен — оператор видит, что хотел сделать
  и какие dashboard issues нужно сначала разрешить.
- **`unsupported`** — `confirm_execute=True`, dashboard
  healthy, **но** для этого class'а write-tool'ов нет
  поддержанного автоматического recovery path. Honest
  fail: assistant отказывается исполнять что-то, чего у
  него на самом деле нет.
- **`rejected`** — invalid input (пустой `operation_id`,
  битый product config, не-dict root, missing JSON file).

### Почему `_AUTOMATIC_RECOVERY_SUPPORTED` исторически был пуст и как он расширялся

В платформе **нет** публичных `delete_*` write-tool'ов
(нет `delete_catalog_attribute`,
`remove_module_method`, `delete_catalog`). Чтобы
автоматически отменить, например,
`add_catalog_attribute`, нужно было бы либо:

1. вызвать write-tool, которого нет;
2. либо product layer самостоятельно отредактировал бы
   XML/BSL в `dump_path` — это **back-door write channel**
   мимо `run_write_flow`, audit, snapshots и verify.
   Phase 5 / Step 6 явно отказывается от этого.

Поэтому исходно Phase 5 / Step 6 ship'ил **advisory-only**
rollback UX: preview всегда построен,
`prepare_rollback_hint` подтянут, оператор видит точные
snapshot-paths и осмысленный operator summary, но финальный
шаг — **manual snapshot-restore** — оператор делает сам,
осознанно. На том этапе whitelist
`_AUTOMATIC_RECOVERY_SUPPORTED` был оставлен в коде как
frozenset с честным docstring'ом — будущий шаг должен был
расширить его без изменения скелета assistant'а.

Этот «будущий шаг» уже состоялся в два прохода:

- **Phase 6 / Step 4** перевёл whitelist из пустого
  frozenset'а в набор из **2 tools**
  (`add_catalog_attribute`, `add_document_attribute`) —
  узкая полоса single-XML-file ops без расширения public
  surface'а write-server'а; см. секцию
  «Phase 6 / Step 4 — первый исполняемый rollback (узкая
  полоса)» ниже.
- **Track F / Step 4** (post-Phase-6 parallel track)
  расширил whitelist до **6 tools** добавлением
  `add_form_attribute`, `add_form_element`,
  `append_module_method`, `replace_module_method_body`
  — все Tier 1 candidates per Track F eligibility contract
  (file-based mutating ops, single relative_path payload key
  из `_RELATIVE_PATH_KEYS`, pre-state file всегда
  существовал, inverse через single-file snapshot restore).

Дальнейшее расширение по-прежнему — отдельный track. Tier
3 categorical exclusions (`create_*` family,
`apply_config_from_files`, `update_database_configuration`)
остаются вне whitelist'а by design: их inverse semantics
требует public `delete_*` tools / multi-file restore /
DB-schema rollback, ничего из чего Track F **не** ship'ил.
См. `docs/architecture/track-f-rollback-eligibility-contract.md`
для нормативного contract'а.

### Behavioral discipline

- **History / inspect / preview работают на degraded.**
  Read-only boundary никогда не блокируется dashboard'ом;
  оператор должен видеть состояние даже когда стенд
  плохо себя чувствует.
- **Execution блокируется на degraded.** `confirm_execute=True`
  + dashboard.ready_for_workflows=False → `mode=blocked`,
  `ok=False`. Preview сохранён.
- **Confirm gate жёсткий.** Без `confirm_execute=True`
  никаких mutating effects, никаких записей в audit, ни
  одного байта изменённого XML/BSL.
- **Boundary никогда не бросает.** Любая внутренняя
  ошибка превращается в `ok=False` с понятным
  `message` и (где уместно) error-finding'ом.
- **Suggested tools — только реальные имена.** Recovery
  модуль переиспользует `_allow_only_real_tools(...)`
  из workflow-слоя Step 5, который проверяет каждое имя
  по живому объединению трёх registries
  (`mcp_read_server.list_tools()`,
  `mcp_write_server.list_tools()`,
  `mcp_intelligence_server.list_tools()`) плюс
  whitelist платформенных boundary-функций.

### Что rollback / recovery / audit UX сейчас НЕ делает

- **Выполняет автоматический content-level rollback
  только для whitelisted tools** (after Track F / Step 4 —
  6 entries: `add_catalog_attribute`,
  `add_document_attribute`, `add_form_attribute`,
  `add_form_element`, `append_module_method`,
  `replace_module_method_body`). Для любого write-tool вне
  whitelist'а — `mode='unsupported'` honest fail; manual
  snapshot-restore остаётся operator's responsibility.
- **Не исполняет multi-file filesystem snapshot-restore.**
  Single-file snapshot restore через
  `restore_dump_file_from_snapshot` доступен whitelisted
  tools'ам; multi-file copytree-обратное копирование
  (`shutil.copytree`-style) оператор по-прежнему делает
  руками. Это сознательно: product layer не должен иметь
  multi-file write channel на dump/base.
- **Не модифицирует audit JSONL.** История — append-only;
  Step 6 только читает.
- **Не делает UI / web frontend / push subscription.**
- **Не подменяет Step 5 guided workflows.** Если в
  будущем появится supported recovery path, он будет
  делегировать в `run_guided_workflow(...)`, а не строить
  параллельный writer.
- **Не делает запросы за пределами audit + dashboard.**
  Никаких сетевых пробинг'ов, никаких отдельных
  intelligence-вызовов сверх того что уже агрегирует
  dashboard.

### Phase 6 / Step 4 — первый исполняемый rollback (узкая полоса)

Step 4 переводит `_AUTOMATIC_RECOVERY_SUPPORTED` из пустого
frozenset'а в **whitelist из ровно двух tool'ов**:
`add_catalog_attribute`, `add_document_attribute`. Для них
`run_rollback_assistant(..., confirm_execute=True)` теперь
действительно исполняет автоматический content-level откат —
**без** того, чтобы продуктовый слой сам трогал dump-файлы.

Что меняется:

- **Audit row теперь несёт structured `details`.** При
  каждом успешном write-flow record получает dict вида
  `{"operation_name", "rollback_supported",
  "backup_snapshot_path", "dump_snapshot_path",
  "relative_path"}`. Pre-Step-4 строки байт-идентичны:
  `details=None` явно вырезается из JSON. Reader-слой
  принимает оба формата.
- **Whitelist жёстко зафиксирован.** В whitelist'е только
  tools, чей `operation_payload` carries single
  `relative_path` key (один из
  `flow.py:_RELATIVE_PATH_KEYS`), pre-state file всегда
  существовал, и inverse полностью покрывается single-file
  snapshot restore. На Phase 6 / Step 4 это были два
  XML-attribute tools'а (`add_catalog_attribute`,
  `add_document_attribute`); Track F / Step 4 (post-Phase-6
  parallel track) расширил whitelist до 6 entries
  добавлением `add_form_attribute`, `add_form_element`
  (XML form-edit ops) и `append_module_method`,
  `replace_module_method_body` (BSL module-edit ops). См.
  `docs/architecture/track-f-rollback-eligibility-contract.md`
  для нормативного contract'а и
  `docs/architecture/track-f-rollback-baseline-audit.md`
  для per-tool sanity-check evidence.
- **`automatic_recovery_supported=True` требует трёх
  условий одновременно:** имя tool'а в whitelist'е, в
  audit-строке есть `details`, и `details` содержат
  непустые строки `dump_snapshot_path` и `relative_path`.
  Любой из трёх отсутствующих факторов — honest degrade
  до `mode='unsupported'`, без write'а. Это автоматически
  закрывает старые pre-Step-4 строки: для них `details=None`,
  поэтому ассистент не пытается их откатывать.
- **Исполнение идёт через public write-tool.** Recovery
  ассистент вызывает `mcp_write_server.tools.restore_dump_file_from_snapshot`,
  то есть rollback наследует ту же `run_write_flow`
  дисциплину (preflight + snapshot + operation + verify +
  audit), что и forward write. Никакого back-door
  filesystem-канала из продуктового слоя нет —
  `apps/platform/src/onec_platform/recovery.py` по-прежнему
  не пишет файлы напрямую.
- **Post-rollback verify обязателен.** После восстановления
  ассистент вызывает существующий read-only
  `diff_dump_fragment(env, relative_path, baseline)` против
  текста snapshot-файла и считает успехом только сочетание
  `restore.ok=True` AND `diff.data.changed=False`. Любое
  расхождение — `ok=False` с понятным сообщением; «откат
  прошёл, но содержимое не совпадает» в success не
  превращается.
- **`mode='executed'` имеет точную семантику.** Это «попытка
  отката случилась». `ok=True` дополнительно требует
  чтобы рестор и verify оба прошли. `ok=False` под тем же
  `mode='executed'` означает, что попытка была реальной,
  но что-то пошло не так — write_results / verify_results
  показывают, что именно.
- **`mode='blocked'` и `mode='unsupported'` остаются как
  раньше:** dashboard не `ready_for_workflows` → blocked;
  tool вне whitelist'а или audit row без details →
  unsupported. Никаких mutating effects в обоих случаях.

Что Phase 6 / Step 4 НЕ делал:
- не расширял whitelist дальше двух tool'ов (это было
  следующим шагом — фактически выполнен Track F / Step 4
  post-Phase-6, расширил whitelist до 6 tools, см. ниже);
- не трогал Step 5 guided workflows и Step 7 real-stand
  smoke test;
- не делал `delete_*` public write-tool'ы (их по-прежнему
  нет — потребовало бы отдельного решения по семантике
  удаления в 1С; out-of-scope Track F тоже);
- не делал full filesystem snapshot-restore — это
  **single-file** restore, выбираемый одной строкой
  `relative_path` (Track F / Step 4 сохранил эту дисциплину
  без изменений).

### Track F / Step 4 — расширение whitelist до 6 tools

Track F (post-Phase-6 parallel track «Rollback Whitelist
Expansion») в своём Step 4 расширил
`_AUTOMATIC_RECOVERY_SUPPORTED` (и его mirror
`_ROLLBACK_SUPPORTED_OPERATIONS` в
`apps/mcp-write-server/src/mcp_write_server/runtime/flow.py`)
с 2 до **6 entries** добавлением:

- **`add_form_attribute`** — XML DOM edit формы (Phase 6 /
  Step 5 deliverable);
- **`add_form_element`** — XML substring patch формы;
- **`append_module_method`** — BSL append к module file;
- **`replace_module_method_body`** — BSL signature-bounded
  body edit.

Все четыре tools проходят через тот же
`run_write_flow` + `restore_dump_file_from_snapshot` +
`diff_dump_fragment` post-rollback verify mechanism, что и
исходные два whitelisted tools. Никаких изменений в
recovery API, audit `details` shape, `_RELATIVE_PATH_KEYS`,
`_extract_relative_path`, write-tool definitions
(`tools.py`), registries (`read=15 / write=25 /
intelligence=16` без drift'а на всём треке).

Что Track F / Step 4 (и Track F в целом) **не** делает:

- не ship'ит универсальный rollback для произвольного
  write-tool'а;
- не ship'ит multi-file restore framework;
- не ship'ит public `delete_*` write-tools (semantics
  удаления в 1С остаётся undecided — out-of-scope Track F);
- не ship'ит DB / schema rollback
  (`update_database_configuration` остаётся
  external-DB-backup territory);
- не ship'ит rollback для multi-file
  `apply_config_from_files`;
- не ship'ит rollback для `create_*` family — их inverse
  semantics требует delete которого нет (Tier 3
  categorical exclusion в Track F audit);
- не ship'ит AST-based semantic inversion для BSL / XML;
- не делает blanket reversibility claim — после Track F /
  Step 4 covered 6 of 25 mutating registry tools = 24%
  surface; 19 tools остаются manual snapshot-restore
  territory by design.

Детали — в
`docs/architecture/track-f-rollback-whitelist-expansion-plan.md`,
`track-f-rollback-baseline-audit.md`,
`track-f-rollback-eligibility-contract.md`.

## Что такое real-stand / 1cv8 binary integration track (Step 7)

Step 7 даёт **product-layer контракт** для интеграции с
реальным 1cv8 binary и первый **controlled smoke test**.
Это не подмена Phase 2 stub'ов и не «волшебная» полная
интеграция: Phase 2 write-tools (`create_dump_snapshot`,
`apply_config_from_files`,
`update_database_configuration`) на Step 7 **не**
переписываются — флипать их на binary-backed branch это
параллельный track, не scope этого шага.

Step 7 ship'ит:

1. **Binary integration contract** в `onec-config` —
   две опциональные строки в окружении:
   - `onec_binary_path: str | None` — абсолютный путь
     к 1cv8 executable;
   - `onec_binary_probe_args: list[str] | None` —
     operator-declared argv для контролируемого smoke
     probe (платформа **не** угадывает 1cv8-специфические
     флаги).
2. **Reference stand spec** (см. ниже).
3. **Readiness boundary** — read-only doctor.
4. **Smoke-test boundary** — preview / executed / blocked /
   rejected.

### Boundary-функции

| Boundary | Что делает | Mutating? |
|---|---|---|
| `get_real_stand_readiness(data)` | Read-only readiness verdict: binary path declared, существует, не директория, executable bit (на POSIX), base/dump паths существуют, dashboard verdict не blocked. | Нет |
| `run_real_stand_smoke_test(data, *, confirm_execute)` | Preview by default. На `confirm_execute=True` + readiness ready: filesystem probe (всегда) + контролируемый subprocess через `onec_process_runner` (только если operator declared `onec_binary_probe_args`). | Нет в смысле infobase — никаких MCP write-tool'ов; subprocess стартуется операторски-объявленным argv'ом |

### Modes (`REAL_STAND_SMOKE_MODES`)

- **`preview`** — `confirm_execute=False`. Plan + readiness
  step + dashboard step; **никакого** filesystem probe и
  **никакого** subprocess.
- **`executed`** — `confirm_execute=True` + readiness met.
  **Всегда** делает filesystem probe (stat: size,
  mtime). **Дополнительно** стартует subprocess через
  `onec_process_runner.run_process` тогда и только тогда,
  когда оператор задал `onec_binary_probe_args`. Это
  настоящий subprocess с captured exit_code + truncated
  stdout/stderr excerpts (cap 1024 chars). Timeout — 30s
  fixed.
- **`blocked`** — `confirm_execute=True` но readiness не
  пройдена (binary missing / dir / dashboard blocked).
  Preview сохранён.
- **`rejected`** — invalid input или unloadable config.

### Что значит «readiness»

Readiness — это деревовидный AND:

1. `onec_binary_path` set (не `None`).
2. Файл существует на диске.
3. Это файл, не директория.
4. На POSIX — есть хоть один executable bit; на Windows —
   любой обычный файл.
5. `base_path` существует.
6. `dump_path` существует.
7. Dashboard verdict не `blocked`.

`presumed_findings` несёт honest signals на degraded
dashboard, отсутствующих probe args и т.п. — они не
блокируют readiness, но видны оператору.

### Reference stand spec

Что считается «поддержанным стендом» для Step 7
controlled smoke test:

- **Платформа 1С:** версия 8.3.x; конкретная сборка не
  закрепляется — оператор сам выбирает binary в
  `onec_binary_path`. Step 7 не делает 1cv8-version-sniffing.
- **ОС:** Windows preferred (typical 1cv8.exe location);
  Linux supported в той же мере, в какой `onec-process-runner`
  и `is_pid_alive` Step 3 уже работают cross-platform.
- **Тип базы:** любая, **которая не открывается в GUI без
  параметров**. Если probe argv пустой и binary в
  стандартном режиме открывает GUI — оператор обязан
  задать probe args, иначе платформа в execute mode
  не стартует subprocess (only metadata probe).
- **`base_path`:** существует и читаем оператором.
- **`dump_path`:** существует и содержит хотя бы один
  `.bsl` файл (для дашборд-уровневого `search_index`
  check).
- **`http_base_url`:** доступен (для дашборд-уровневой
  `gateway` проверки). На stage-стендах допустимо
  замокать локальным HTTP-сервером; production-стенд
  Step 7 не должен трогать без отдельного operator
  approval.
- **`onec_binary_path`:** absolute path; реальный
  существующий файл; если POSIX — executable bit set.
- **`onec_binary_probe_args`:** опц.; operator-declared
  argv-tail. Должны быть **безопасны** — не открывать
  GUI, не мутировать infobase. Примеры безопасных args
  (зависят от версии и режима 1cv8): `["DESIGNER",
  "/?"]`, `["/?"]` (на разных версиях даёт help-вывод и
  exits). **Платформа не валидирует семантику этих
  args** — оператор владеет своим стендом.
- **Права:** оператор должен иметь право запускать
  `onec_binary_path` и читать `dump_path` /
  `base_path` /  `audit/.audit/`.
- **Smoke-test ограничения:** filesystem probe (stat) +
  один subprocess invocation. Timeout 30s. Excerpts
  обрезаны до 1024 chars. Exit code surface'ится. Полный
  DESIGNER → BackupCfg → DumpCfg → ENTERPRISE round-trip
  **не** делается на Step 7 — это требует реального
  стенда с реальной инфобазой и больше operator-контракта,
  чем Step 7 может ship'ить.

### Что real-stand / binary integration track сейчас НЕ делает

- **Не переписывает Phase 2 stub'ы.**
  `create_dump_snapshot` / `apply_config_from_files` /
  `update_database_configuration` остаются stub-backed.
  Их evolution на binary-backed dispatch с
  `onec_binary_path` — параллельный track после Step 7.
- **Не валидирует 1cv8-CLI семантику.** Оператор владеет
  выбором `onec_binary_probe_args`. Платформа просто
  передаёт их в subprocess.
- **Не открывает GUI.** Если operator-declared argv
  открывает GUI — это операторский choice, и timeout 30s
  принудительно завершит subprocess.
- **Не делает full DESIGNER → DumpCfg → ENTERPRISE
  round-trip.** Это требует реальной инфобазы и больше
  state, чем Step 7 готов ship'ить честно.
- **Не мутирует infobase / dump / audit.** Никаких MCP
  write-tool'ов из binary boundary не вызывается.
- **Не подменяет MCP tools.** Никаких новых tool'ов в
  read/write/intelligence; никаких изменений их registry.
- **Не валидирует конкретную версию 1cv8.** Оператор
  выбирает binary под свой стенд.

## Phase 5 / Step 8 — final integration pass (Phase 5 закрыта)

Step 8 — закрывающий, документационный по сути шаг.
Сквозной интеграционный сценарий прошёл **без правок
кода**: всё, что собирали Step 2–7, реально склеилось в
один продуктовый контур поверх существующих
read/write/intelligence-серверов.

### Что подтвердил интеграционный прогон

Один сквозной Scenario A на временном synthetic-окружении
(tempdir + локальный in-process HTTP listener + реальные
subprocess'ы для runtime и real-stand smoke probe; ни одна
строка не была отправлена в боевой стенд):

1. **`bootstrap_product`** — конфиг загружен, prereqs
   doctor отработал, ноль blocking findings.
2. **`start_product_runtime`** — три runtime-сервиса
   реально стартовали; PID'ы живые; state-файл
   `<work_dir>/.runtime/runtime-state.json` записан.
3. **`get_product_runtime_status`** — снимок честный
   (running × 3).
4. **`build_environment_dashboard`** — Step 4 boundary
   собрал шесть секций; verdict `healthy`,
   `ready_for_workflows=True`.
5. **`run_guided_workflow`** safe-add-attribute
   `confirm_execute=True` — реально дописал атрибут
   `Title` в `Catalogs/Items.xml` через **существующий**
   public write-tool `add_catalog_attribute`, который сам
   прошёл через `run_write_flow` (preflight → snapshot
   → operation → verify → audit). `verify_attribute_exists`
   подтвердил наличие на диске. `last_write_operation`
   и `rollback_hint` появились.
6. **`get_operation_history`** — увидел реальную audit
   запись с тем же `operation_id`.
7. **`inspect_operation`** — сфокусировался на ней,
   приложил rollback hint, явно показал
   `automatic_recovery_supported=False`.
8. **`run_rollback_assistant`** preview — план собран,
   никаких write-эффектов.
9. **`get_real_stand_readiness`** — readiness ready
   (binary path = `sys.executable`, probe args =
   `["--version"]`).
10. **`run_real_stand_smoke_test`** `confirm_execute=True`
    — реальный subprocess через `onec_process_runner.run_process`
    стартовал и завершился с `binary_exit_code=0`,
    stdout содержит `Python`. Это **настоящий**
    binary-backed шаг, не fake.
11. **`stop_product_runtime`** — все три PID'а реально
    мертвы.

### Failure paths

- **F1 — workflow blocked by dashboard.** `dump_path`
  не существует → `mode=blocked, ok=False,
  execution_performed=False`. Ни одного mutating /
  verify / audit step'а в steps.
- **F2 — rollback assistant unsupported.**
  `confirm_execute=True` на здоровом окружении →
  `mode=unsupported, ok=True, execution_performed=False`,
  `automatic_recovery_supported=False`, дамп **не**
  изменился.
- **F3 — broken JSON config.** Все девять
  `_from_json_file` boundary-функций (`bootstrap`,
  `start`, `dashboard`, `workflow`, `history`,
  `inspect`, `rollback`, `readiness`, `smoke`) одинаково
  отдают `ok=False`. Никаких исключений наружу.
- **F4 — malformed audit line.** Дописали в audit
  JSONL `{ this is not valid json` и `"a string, not a
  dict"`; history viewer остаётся `ok=True`, реальные
  записи присутствуют, malformed строки попадают в
  `findings` как warnings (`audit_line_invalid_json:*`,
  `audit_line_not_a_dict:*`).

### Discipline asserts (программно проверены)

- **Registry invariants:** `read=15`, `write=23`,
  `intelligence=16` до и после интеграционного прогона.
- **Real-tool-name discipline:** все `suggested_tools`
  и `suggested_write_tools` во всех payload (workflow
  plan, inspect result, rollback plan, readiness,
  smoke result) — реальные имена, существующие в одном
  из живых registries трёх MCP-серверов или в
  whitelist'е product-layer boundary-функций.
- **Import discipline:** grep
  `^\s*(from|import)\s+onec_policy_engine\b` по
  `apps/platform/src/**` и `apps/mcp-intelligence-server/src/**`
  — **0 импортов**.
- **Boundary не бросает:** ни одна boundary-функция
  product layer не вернула наружу исключение в любом
  из 14+ сценариев.

### Что Step 8 не делает

- **Не правил код.** Интеграционный прогон прошёл
  out-of-the-box; кодовые изменения на Step 8 не
  потребовались.
- **Не расширял scope.** Никаких новых MCP tool'ов,
  никаких новых модулей, никаких изменений в
  registries.
- **Не закрыл крупные хвосты.** Полное замещение
  Phase 2 stub'ов реальной 1cv8-binary, full
  DESIGNER → DumpCfg → ENTERPRISE round-trip,
  installer polish, web-UI, enterprise hardening —
  всё это **остаётся за пределами Phase 5** и явно
  перечислено как non-blocking follow-ups в
  `PROJECT-STATUS.md`.

### Честные ограничения, которые остаются после Phase 5

Закрытый Phase 5 **не означает**, что продукт уже в
финальном industrial-grade состоянии. Что остаётся
честно открытым:

- Phase 2 stub'ы (`create_dump_snapshot`,
  `apply_config_from_files`,
  `update_database_configuration`) **не переписаны**
  на binary-backed dispatch — это самый жирный
  follow-up track после Phase 5.
- Real-stand smoke ловит **один** subprocess
  invocation с operator-declared argv. Multi-step
  smoke (DESIGNER → BackupCfg → DumpCfg → ENTERPRISE)
  требует реальной инфобазы и больше state-machine,
  чем Phase 5 готов ship'ить честно.
- Rollback / recovery — **advisory-only**.
  `_AUTOMATIC_RECOVERY_SUPPORTED` whitelist пуст;
  автоматический content-level rollback требует
  публичных `delete_*` write-tool'ов, которых пока нет.
- MCP-серверы (read/write/intelligence) живут как
  in-process модули. Production-grade MCP transport /
  CLI / `__main__` — отдельный track.
- Hot reload — не реализован (`reload` =
  controlled stop-then-start).
- Watch-and-restart упавших сервисов — нет.
- Захват stdout/stderr дочерних процессов — `DEVNULL`,
  логирование лежит на операторе.
- AST-парсер XML / BSL — не вводился; substring +
  regex остаются базой intelligence-tool'ов.
- Web-UI / push subscription / hot monitoring — out
  of Phase 5 scope.
- Полная enterprise-поверхность (SSO/RBAC,
  multi-tenant, secrets vault, policy-as-code,
  multi-instance HA, federated audit storage) —
  отдельный enterprise-track.

## Минимальный пример использования

```python
from onec_platform import (
    bootstrap_product,
    start_product_runtime,
    get_product_runtime_status,
    stop_product_runtime,
)

config = {
    "product_name": "1C Agent Platform",
    "profile_name": "local-dev",
    "default_environment": "local-dev",
    "project": {
        "environments": {
            "local-dev": {
                "name": "Local Dev",
                "base_id": "local-dev",
                "base_path": "C:\\tmp\\infobase",
                "publication_name": "local-dev",
                "http_base_url": "http://localhost:8080/local-dev",
                "dump_path": "C:\\tmp\\dump\\local-dev",
                "timeout_seconds": 30,
                "allow_write": False,
            }
        }
    },
    "bootstrap": {"work_dir": "C:\\tmp\\platform-work"},
    "runtime": {
        "services": {
            "read":         {"enabled": True,  "command": ["python", "-m", "mcp_read_server"]},
            "write":        {"enabled": True,  "command": ["python", "-m", "mcp_write_server"]},
            "intelligence": {"enabled": True,  "command": ["python", "-m", "mcp_intelligence_server"]},
        }
    },
}

# Step 2 surface: prereqs doctor + bootstrap.
boot = bootstrap_product(config)
print(boot.ok, boot.message)

# Step 3 surface: runtime orchestration.
res = start_product_runtime(config)
print(res.ok, res.message)
for s in res.services:
    print(f"  {s.name}: status={s.status} pid={s.pid}")

snap = get_product_runtime_status(config)
print(snap.message, snap.state_path)

stop = stop_product_runtime(config)
print(stop.ok, stop.message)
```

Все boundary-функции (`bootstrap_product`,
`start_product_runtime`, `stop_product_runtime`,
`get_product_runtime_status`, `reload_product_runtime`) и их
`_from_json_file` варианты возвращают структурированный
результат и **никогда** не пробрасывают исключения наружу.

## Safety guarantees Phase 2–4 — что сохраняется

Phase 5 / Step 3 **ничего** в существующих серверах не меняет:

- `mcp-read-server` — registry те же 15 tool'ов, не тронут.
- `mcp-write-server` — registry те же 23 tool'а, не тронут.
  `run_write_flow` остаётся единственным путём к mutating
  операциям.
- `mcp-intelligence-server` — registry те же 16 tool'ов, не
  тронут. Read-only контракт сохранён: `onec_policy_engine`
  не импортируется ни в нём, ни в `onec_platform`.
- Никаких write-эффектов в 1С из самого `onec_platform`.
  Платформа управляет PID-ами тех команд, которые оператор
  описал, и точка.
- `onec-config`, `onec-policy-engine`, `pyproject.toml`,
  `selfcheck.py` — не тронуты.

## Что такое install / setup fast path (Phase 6 / Step 3)

Step 3 даёт **минимальный** product-layer fast path, который
**сокращает ритуал установки** до одной boundary-функции. Это
**не** настоящий industrial installer (нет `.msi`/`.deb`/GUI),
**не** packaging ecosystem, **не** auto-launcher. Это
**fast path** поверх уже готовых Step 2 contracts: оператор
заполняет минимальный набор полей, получает JSON product-config
на диске и подтверждённый `bootstrap_product` round-trip — и
только.

### Boundary-функции

| Boundary | Что делает | Mutating? |
|---|---|---|
| `inspect_release_layout(root_path)` | Read-only проверка top-level entries (`apps/`, `packages/`, `docs/`, `README.md`, `PROJECT-STATUS.md`) у переданного пути. Honest findings: `release_entry_present:*` / `release_entry_missing:*`. | Нет |
| `build_product_config_template(...)` | Собирает JSON-serialisable dict под текущий контракт `onec_config.ProjectConfig` + product-layer wrapping. Bad input → `ok=False` с `template_input_rejected` finding'ом. | Нет |
| `run_install_fast_path(data, *, output_config_path, confirm_write=False)` | Главный Step 3 boundary. Preview (default) или executed (`confirm_write=True`). Executed пишет JSON и затем re-loads его через `bootstrap_product_from_json_file` для round-trip подтверждения. | Только запись JSON-файла, **только** при `confirm_write=True` и **только** если target не существует |
| `run_install_fast_path_from_json_file(path, *, output_config_path, confirm_write=False)` | Тот же entry, но с JSON-файла. | Аналогично |

### Modes (`INSTALL_MODES`)

- **`preview`** — `confirm_write=False` (default). Helper
  собрал template, прогнал layout-inspection и
  `bootstrap_product`, **ничего не записал на диск**.
  Operator видит `template_preview` под рукой.
- **`executed`** — `confirm_write=True` + target path
  свободен. Helper записал JSON атомарно (через
  `*.tmp` + `os.replace`), затем сделал
  `bootstrap_product_from_json_file` round-trip.
  `bootstrap_post.ok` показывает, читается ли config
  обратно.
- **`rejected`** — invalid input config / target file
  уже существует / I/O ошибка при записи / non-dict
  root. Никакого silent overwrite.

### Дисциплина

- **Никакого silent overwrite.** Если
  `output_config_path` уже существует на диске, helper
  отказывается перезаписывать молча — `mode="rejected"`,
  finding `output_config_path_exists`. Operator сам
  принимает решение (взять другой path или удалить
  существующий файл руками).
- **Атомарная запись.** Через `*.tmp` + `Path.replace`
  — никакого «полу-записанного» config'а на диске даже
  при сбое.
- **Создание родительской директории — да.** Это часть
  «уменьшения ритуала»: operator не должен делать
  `mkdir -p` руками. Создаются только директории,
  ведущие к `output_config_path`; никаких записей вне
  этого пути.
- **Никакого запуска runtime / workflows / write-tool'ов.**
  Step 3 boundary не зовёт `start_product_runtime`,
  `run_guided_workflow`, любые MCP write-tool'ы или
  `onec-process-runner`. Запуск runtime — отдельный шаг
  оператора через уже существующие boundary-функции.
- **Не трогает инфобазу.** Никаких write-эффектов в
  реальный 1С.
- **Round-trip подтверждение.** После записи
  `bootstrap_product_from_json_file` повторно читает
  JSON и прогоняет doctor — это honest проверка, что
  записанный файл сам по себе валиден как
  product-config.

### Короткий install runbook

После Step 3 fast path установка сводится к ≤ 5 ручным
шагам:

1. Получить релиз (clone репозитория или скачать
   архив).
2. Запустить `scripts/dev/bootstrap_paths.ps1`
   (PYTHONPATH в текущей PowerShell-сессии).
3. Подготовить минимальный input dict с
   `product_name`, `profile_name`,
   `default_environment`, `base_path`, `dump_path`,
   `http_base_url`, `bootstrap.work_dir`.
4. Вызвать
   `run_install_fast_path(input_dict,
   output_config_path=..., confirm_write=True)`.
5. После `mode="executed"` оператор уже имеет JSON
   config на диске + успешный `bootstrap_post`. Дальше
   он явно запускает runtime / dashboard / workflow /
   real-stand smoke как отдельные шаги через уже
   существующие boundary-функции.

### Что Step 3 НЕ делает

- **Не GUI installer.** Никаких setup-wizard'ов, окон,
  диалогов, мастеров.
- **Не release packaging ecosystem.** Никаких
  `.msi`/`.deb`/`.dmg`/wheel/PyPI release artefact
  генераторов; формальный release artifact format
  остаётся как Step 1 plan-level open question.
- **Не запускает MCP-серверы.** Helper не зовёт
  `start_product_runtime`, не открывает порты, не
  проверяет live-стенд.
- **Не модифицирует инфобазу.** Никаких write-tool'ов
  через `run_write_flow`, никаких mutating-операций.
- **Не подменяет Step 2 binary integration.**
  `create_dump_snapshot` остаётся ровно тем, что
  ship'нул Step 2 (stub default + binary-backed when
  configured).
- **Не делает silent overwrite.** Existing target
  → fail-closed, никакого «магического перезапуска
  install'а».

## Что такое runtime hardening / supervision / logs (Phase 6 / Step 6)

Phase 6 / Step 6 даёт **первый честный slice runtime hardening**
поверх уже существующего product runtime contract из Phase 5 /
Step 3. Это **не** production-grade process supervisor, **не**
GUI/web dashboard, **не** Windows Service / systemd unit, **не**
journald / centralized log aggregation, и **не** background
watch-and-restart daemon. Это узкое расширение существующего
boundary'а: добавлены логи на файл, минимальная rotate-if-exceeds-
size, узкая restart policy, и обогащение runtime-state.

### Что меняется

- **Structured runtime logs.** При `start` / `reload` каждого
  service'а `stdout` и `stderr` теперь маршрутизируются в
  файлы:
  - `<work_dir>/.runtime/logs/<service>.out.log`
  - `<work_dir>/.runtime/logs/<service>.err.log`

  Эти пути попадают в `RuntimeServiceState.stdout_log_path` /
  `RuntimeServiceState.stderr_log_path` и в persisted
  `runtime-state.json`, чтобы оператор и status-вывод видели,
  где смотреть логи. Файлы открываются в режиме append-binary
  (`"ab"`, `buffering=0`) — никаких пропавших байт, никакой
  магии кодировок. По умолчанию `logs_enabled=True`. Если
  оператор явно ставит `logs_enabled=False`, поведение
  откатывается к Step 3: `stdout`/`stderr` уходят в `DEVNULL`
  (legacy-совместимость).

- **Rotate-if-exceeds-size (одно поколение).** Перед каждым
  новым `spawn` сервиса runtime смотрит на текущий размер
  `<service>.out.log` / `<service>.err.log`. Если файл больше
  `log_max_bytes` (default 1 MiB), он переименовывается в
  `<service>.out.log.1` (через `os.replace` — atomic where
  the OS supports it; старый `.1` перезаписывается). Новый
  активный лог-файл создаётся заново. Это именно одно
  поколение — никакого `.2`/`.3`-цепочки, никакого `gzip`,
  никаких `logrotate`-style конфигов.

- **Declared restart policy.** В `ProductServiceSpec`
  появилось поле `restart_policy ∈ {"never", "restart-if-stale"}`
  (default `"never"`). Семантика:
  - `"never"` — runtime никогда не перезапускает stale
    сервисы; `runtime_pid_stale:<svc>` finding остаётся
    operator's cue.
  - `"restart-if-stale"` — на **boundary-вызовах** `start`,
    `reload`, **и** `status` runtime замечает stale PID,
    инкрементит `restart_attempts`, и зовёт обычный
    spawn-путь. **Никакого фонового daemon'а / timer
    loop'а**: ничего не запускается само по себе. На `stop`
    restart-if-stale **не срабатывает** — оператор только
    что попросил остановить, восстановление было бы
    surprise behavior'ом.

- **Runtime state enrichment + schema bump.**
  `RuntimeServiceState` теперь несёт:
  - `restart_policy` (mirror of spec);
  - `restart_attempts` (счётчик попыток рестарта, не
    success'ов);
  - `last_exit_code` — best-effort exit code stale PID'а;
    Windows: `GetExitCodeProcess` через ctypes; POSIX:
    всегда `None` (orchestrator не spawn'ил PID как child
    текущего процесса, поэтому `waitpid` недоступен — это
    честная деградация, а не fake-значение);
  - `stdout_log_path` / `stderr_log_path` — абсолютные пути
    активных логов, или `None` если logging отключён;
  - `last_started_at` / `last_stopped_at` — ISO-8601 UTC
    штампы. `started_at` сохранён без изменений для
    backward-compat; `last_started_at` обновляется при
    каждом успешном spawn'е, `last_stopped_at` — при
    каждом наблюдаемом stop / stale переходе.

  `RUNTIME_STATE_SCHEMA_VERSION` поднят `1 → 2`. Reader
  принимает обе версии: schema=1 файлы (pre-Step-6) читаются
  honestly, missing fields дефолтятся на `"never"` / `0` /
  `None`. Writer всегда пишет version=2. Operator видит upgrade
  при первой Step-6 boundary call'е.

- **Operator-visible runtime findings.** Новые findings в
  `RuntimeStatusResult.findings` /
  `RuntimeOperationResult.findings`:
  - `runtime_log_paths:<svc>` — `ok` severity; перечисляет
    `stdout_log_path` / `stderr_log_path`;
  - `runtime_log_rotated:<svc>` — `ok` severity; rotation
    реально произошла перед текущим start'ом;
  - `runtime_log_dir_failed:<svc>` / `runtime_log_open_failed:<svc>`
    / `runtime_log_rotate_failed:<svc>` — `error` severity;
    fail-closed для конкретного service'а (статус →
    `"error"`, no `pid`, no silent fallback to DEVNULL);
  - `runtime_pid_stale:<svc>` — расширен: текст теперь
    содержит `last_exit_code=N` когда он известен, или
    explicitly «exit code unavailable on this platform»
    когда POSIX-fallback вернул None;
  - `runtime_restart_attempted:<svc>` — `warning` severity;
    runtime собирается зайти на restart-if-stale path;
  - `runtime_restart_succeeded:<svc>` — `ok` severity;
    spawn после рестарта вернул `running`;
  - `runtime_restart_failed:<svc>` — `error` severity;
    spawn после рестарта НЕ вернул `running`.

### Минимально расширенный config-surface

В `ProductServiceSpec` (и в product-config JSON) появились **три**
optional поля. Step 3 конфиги без них продолжают грузиться без
изменений; loader fail-closed на bad shape:

| Поле | Тип | Default | Контракт |
|---|---|---|---|
| `restart_policy` | `str` | `"never"` | Whitelist `{"never", "restart-if-stale"}`; non-string или unknown value → `ValueError`. |
| `logs_enabled` | `bool` | `True` | Strict `bool` (не bool-ish — `"true"` отвергается). |
| `log_max_bytes` | положительный `int` | 1 MiB | `bool` отвергается явно (т.к. `bool ⊂ int` в Python); `0` / отрицательные → `ValueError`. |

`onec-config` / `onec-policy-engine` / read-server / write-server /
intelligence-server **не тронуты**. Никаких новых environment-level
полей.

### Process-control дисциплина

- `process_control.spawn_service(...)` теперь принимает optional
  `stdout_handle` / `stderr_handle`. `None` сохраняет старое
  поведение Step 3 (`DEVNULL`); открытый file handle / int FD
  маршрутизирует поток. `stdin` всегда `DEVNULL` — long-lived
  product services не читают stdin orchestrator'а.
- `shell=True` **никогда** не используется. argv list уходит в
  `subprocess.Popen` напрямую.
- `start_new_session=True` (POSIX) /
  `CREATE_NEW_PROCESS_GROUP` (Windows) сохранены без изменений
  — Ctrl-C в orchestrator'е по-прежнему не пропагируется в
  child'ов.
- Liveness probe (`is_pid_alive`) и `terminate_pid` без
  изменений. Добавлен новый `get_pid_exit_code(pid)`:
  Windows-only через `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)`
  + `GetExitCodeProcess`; POSIX честно возвращает `None`.

### Что Step 6 НЕ делает (и не претендует делать)

- **Не background watcher / supervisor / daemon manager.**
  `restart-if-stale` срабатывает **только** на boundary
  call'е (`start` / `reload` / `status`). Между boundary
  call'ами runtime не делает ничего самостоятельно.
- **Не Windows Service / systemd unit registration.**
  Полноценный OS-level service supervisor — отдельный
  follow-up track.
- **Не hot reload.** `reload_product_runtime` остаётся
  controlled stop-then-start как в Step 3.
- **Не logging framework.** Никакого journald, никакой
  стрим-мультиплексации, никаких log levels внутри
  product-runtime'а. Всё, что пишет child в stdout/stderr,
  appendится в файл «как есть».
- **Не централизованный log aggregation / forwarding.**
  Логи лежат локально под `<work_dir>/.runtime/logs/`.
- **Не auto-restart timer / exponential backoff /
  max-restarts.** Никаких таймеров, никаких счётчиков
  «остановиться после N попыток». Если каждый boundary
  call видит stale PID и `restart-if-stale`, каждый раз
  будет новая попытка — это сознательное узкое
  поведение Step 6.
- **Не log rotation за пределами одной generation.**
  `.1` файл — единственный backup. Old `.1` перезаписывается
  при следующей rotation. Operator с историческими
  потребностями отвечает за archiving сам.
- **Не PID-file exposure / реimport.** Persisted
  `runtime-state.json` — единственная точка persisted
  state.
- **Не security hardening.** Никаких namespaces, sandbox,
  user-droping, capability restrictions. Это runtime
  hardening **slice**, не security hardening.
- **Не trogает MCP servers / write-flow.** read-server
  (15) / write-server (25) / intelligence-server (16)
  registries не изменены; никаких новых MCP tool'ов; ни
  один write-tool не проходит мимо `run_write_flow`.

## Что такое enterprise foundation (Phase 6 / Step 8)

Phase 6 / Step 8 даёт **узкий честный foundation slice** под
будущий enterprise track. Это **не** SSO/RBAC, **не**
multi-tenant, **не** secrets vault, **не** policy-as-code,
**не** federated audit storage, **не** HA-кластер, **не**
web-UI и **не** новый MCP tool surface. Step 8 ship'ит:
1) одну optional product-config секцию с identity / discipline
   полями, 2) один read-only product-layer boundary, который
   честно отвечает «есть ли foundation под enterprise track?».

### Что появилось в product-config

Новая optional секция `enterprise` рядом с уже существующими
`servers` / `bootstrap` / `runtime`. Step 1–7 конфиги без неё
продолжают грузиться без изменений.

| Поле | Тип | Default | Контракт |
|---|---|---|---|
| `deployment_tier` | str \| None | None | Whitelist `{"dev", "test", "stage", "prod-like"}`; иначе `ValueError`. |
| `instance_id` | str \| None | None | Non-empty string если задан. Required для prod-like. |
| `config_owner` | str \| None | None | Non-empty string если задан. Required для prod-like. |
| `change_control_required` | bool | False | Strict bool. Surfaced verbatim — платформа НЕ enforce'ит change-control workflow сама. |
| `require_operator_identity` | bool | False | Strict bool. Foundation-flag, без enforcement. |
| `runbook_reference` | str \| None | None | Non-empty string если задан (operator's runbook URL / wiki page). |

Loader fail-closed на: unknown keys, non-string `deployment_tier`,
unknown tier value, non-string `instance_id` / `config_owner` /
`runbook_reference`, empty strings, не-`bool` для bool-полей.
`build_product_config_template(...)` принял шесть новых
optional kwargs (`enterprise_*`); enterprise-блок эмитится
**только** если хотя бы один из них передан.

### Boundary

```python
inspect_enterprise_foundation(data)
inspect_enterprise_foundation_from_json_file(path)
```

Read-only. Boundary никогда не raise'ит, не пишет в audit, не
зовёт `run_write_flow`, не стартует / стопает runtime, не
вызывает MCP tool'ы. Возвращает `EnterpriseFoundationResult` с
полями:

- `foundation_level ∈ {"absent", "minimal", "partial", "strong"}`
  — детерминистическое правило поверх четырёх секций (identity,
  operability, traceability, binary). `"strong"` означает
  «foundation годен под следующий enterprise шаг», **не**
  «продукт enterprise-ready».
- `ready_for_enterprise_track: bool` — true ровно когда
  `foundation_level == "strong"` AND нет error-finding'ов. Это
  **honest readiness for the next step**, не readiness for prod.
- `enterprise_section_present: bool`, плюс зеркала всех шести
  полей секции для удобства UI.
- стандартные `confirmed_findings` / `presumed_findings` /
  `recommended_actions` / `suggested_tools` / `suggested_write_tools` /
  `message`. `suggested_*` фильтруются через тот же
  `_allow_only_real_tools`, что в workflow / recovery — никаких
  invented имён.

### Четыре проверяемые секции

- **A. Identity / config discipline.** Проверка наличия
  `deployment_tier`, `instance_id`, `config_owner`,
  `change_control_required`, `require_operator_identity`. Для
  prod-like (или для config'а, в visible-полях которого торчит
  `prod` / `production`) отсутствие `instance_id` /
  `config_owner` — `error` severity.
- **B. Operability foundation.** `bootstrap.work_dir` declared,
  `runtime.services` non-empty, у всех enabled-сервисов
  `logs_enabled=True`, `restart_policy` в whitelist'е.
- **C. Traceability / recovery foundation.** Standalone manuals
  Step 7 (`docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md`) physically
  present; recovery boundaries (`get_operation_history`,
  `inspect_operation`, `run_rollback_assistant`) — реально
  callable на `onec_platform`. Узкий automatic-rollback
  whitelist Step 4 — **не** ошибка foundation, а honest
  constraint.
- **D. Real-stand / binary foundation.** `onec_binary_path` и
  `onec_dumpcfg_command_template` declared. Это inspection
  **контракта**, не probing бинаря — ничего не запускается;
  smoke-test'ы остаются территорией `run_real_stand_smoke_test`.

### Что Step 8 НЕ делает

- Не вводит новых MCP tool'ов. Registry counts ровно те же:
  read=15 / write=25 / intelligence=16.
- Не enforce'ит ни одного нового policy-инварианта. Все
  enterprise-поля surface'ятся verbatim; интерпретация —
  территория future steps / external CI.
- Не делает RBAC / SSO / multi-tenant / vault / federated audit
  storage / policy-as-code / HA / web-UI / новый transport /
  hot reload — всё это явно вынесено за Phase 6.
- Не probe'ит 1cv8 binary внутри inspector'а — это работа
  существующего `run_real_stand_smoke_test`.
- Не пишет fake-readiness verdict. `ready_for_enterprise_track`
  означает буквально «foundation для next-step enterprise track
  собран», а не «готовы к prod».

## Phase 6 закрыта (Phase 6 / Step 9 — final integration pass)

Phase 6 закрыта одним связным сквозным сценарием на synthetic
стенде, который последовательно проходит через **каждый** Phase 6
slice — без mock'ов, без stub-поверхностей и без skip'ов:

1. `bootstrap_product` (Step 2 contract loadable);
2. `run_install_fast_path(confirm_write=True)` — Step 3 install
   fast path материализует JSON product-config атомарно и
   round-trip'ит его через `bootstrap_product_from_json_file`;
3. `start_product_runtime_from_json_file` — Step 6 runtime
   layer поднимает реальный long-lived `subprocess.Popen` с
   логами в файлы;
4. `get_product_runtime_status_from_json_file` — Step 6
   surface показывает живой PID + populated `stdout_log_path` /
   `stderr_log_path` / `last_started_at`;
5. `build_environment_dashboard_from_json_file` — Step 4
   dashboard выдаёт `overall_status='healthy'`,
   `ready_for_workflows=True`;
6. `run_guided_workflow(safe-add-attribute, target_kind=catalog,
   confirm_execute=True)` — Step 5 mutating workflow через
   `run_write_flow`. Внутри: реальная binary-backed
   `create_dump_snapshot` (Step 2) — проверено тем, что
   snapshot-директория физически содержит **скопированный**
   `Catalogs/SampleCatalog.xml`, а не stub-marker;
   `add_catalog_attribute` действительно меняет XML на диске;
   audit row фиксируется, `operation_id` извлекается из
   `wf_cat.last_write_operation['operation_id']`;
7. `run_guided_workflow(safe-add-form-attribute,
   confirm_execute=True)` — Step 5 structural XML edit slice
   (Step 9 добавил минимальный guided-wrapper над уже
   существующим `add_form_attribute`). ElementTree-путь
   structurally создаёт пустой `<Attributes>` блок внутри
   формы и вставляет туда новый `<Attribute>`. Snapshot этой
   операции тоже binary-backed (содержит копию dump tree);
8. `get_operation_history_from_json_file` — Step 6 audit
   surface видит **обе** operation_id'и;
9. `inspect_operation_from_json_file(operation_id=catalog_op)` —
   Step 6 inspect surface отдаёт
   `automatic_recovery_supported=True` (Step 4 whitelist);
10. `run_rollback_assistant_from_json_file(confirm_execute=True)`
    — Step 4 executable rollback. Идёт через public
    `restore_dump_file_from_snapshot` write-tool (то есть через
    тот же `run_write_flow`); post-rollback verify через
    `diff_dump_fragment` (`changed=False`); никакого back-door
    write channel'а из продуктового слоя;
11. **Post-rollback verify** — re-parse XML через
    `xml.etree.ElementTree`. Подтверждено structurally: ни
    `Step9CatalogField`, ни `Step9FormField` больше нет в
    файле; live XML byte-equals оригинальной fixture (snapshot
    catalog op'а был сделан до обоих writes — это honest
    rollback semantics: «restore the file to the moment the
    rolled-back operation started», не selective undo);
12. `get_real_stand_readiness_from_json_file` — Step 7
    readiness gate (`ready_for_real_stand_smoke=True`);
13. `run_real_stand_smoke_test_from_json_file(confirm_execute=
    True)` — Step 7 контролируемый subprocess через
    `sys.executable` с probe args `["-c", "print('ok')"]`,
    `binary_invoked=True, binary_exit_code=0`;
14. `inspect_enterprise_foundation_from_json_file` — Step 8
    read-only doctor возвращает `foundation_level='strong'`,
    `ready_for_enterprise_track=True` на том же materialised
    JSON-config'е (после Step 9 fix'а в `_config_to_dict`,
    который раньше silently dropped enterprise-блок при
    install fast path round-trip);
15. `stop_product_runtime_from_json_file` — Step 6 shutdown,
    PID реально умирает (`is_pid_alive(pid_started)=False`);
16. Step 6 log files (`.runtime/logs/demo.{out,err}.log`)
    physically present.

В дополнение к Scenario A прошли **шесть** honest failure paths
без единого исключения наружу из boundary'ев:
- F1 — workflow blocked when dashboard is unhealthy (no gateway
  → mode=`'blocked'`, ничего не записано на диск);
- F2 — rollback unsupported для `add_form_attribute` (вне Step 4
  whitelist'а) → mode=`'unsupported'`, нет write_results;
- F3 — broken JSON config через **девять** `_from_json_file`
  boundary'ев (включая Step 8 enterprise-foundation entry) →
  все возвращают `ok=False` без exception'а;
- F4 — real-stand smoke с реальным non-zero exit (probe
  возвращает 7) → `mode='executed', binary_exit_code=7,
  ok=False`, никакого fake-success'а;
- F5 — enterprise foundation на prod-like config'е без
  identity / binary contract → `foundation_level='minimal',
  ready=False`, четыре error-finding'а
  (`*_missing_on_prod`);
- F6 — binary-backed `create_dump_snapshot` падает с
  non-zero exit'ом → workflow `ok=False, stage='dump_snapshot'`,
  без silent fallback'а на stub mode (Step 2 honesty
  contract).

Discipline asserts тоже зелёные:
- registries pre/post: `read=15, write=25, intelligence=16`
  (без drift'а);
- 0 реальных import'ов `onec_policy_engine` под
  `apps/platform/src/` и `apps/mcp-intelligence-server/src/`;
- `suggested_tools` / `suggested_write_tools` 14 списков, все
  имена реальные (из live registries или
  `_KNOWN_PLATFORM_FUNCTIONS`); made-up name отвергается
  `_allow_only_real_tools`;
- ни одна boundary-функция не raise'ит наружу (каждый вызов в
  manual-check'е обёрнут в `must_not_raise`);
- никакого back-door write channel'а — структурно следует из
  D2.

### Что Phase 6 закрыла честно

- **Step 2**: один real binary-backed slice (`create_dump_snapshot`).
- **Step 3**: install / setup fast path сокращает manual ritual до
  одной boundary-функции.
- **Step 4**: первый исполняемый rollback path для двух tool'ов
  whitelist'а (`add_catalog_attribute`, `add_document_attribute`),
  идущий через public `restore_dump_file_from_snapshot` без
  back-door channel'а.
- **Step 5**: первый structural XML edit slice
  (`add_form_attribute`); шесть DOM-style helper'ов в
  `metadata_ops.py`; одна новая verify-ветка
  `kind="form_attribute_exists"`. На Step 9 добавлен ровно
  один тонкий guided-wrapper `safe-add-form-attribute`.
- **Step 6**: structured runtime logs +
  rotate-if-exceeds-size (one generation), narrow `restart_policy
  ∈ {"never","restart-if-stale"}` (boundary-only, no daemon),
  обогащённый `RuntimeServiceState` + `runtime-state.json`
  schema 2 с backward-compat reader'ом.
- **Step 7**: standalone manuals + runbooks
  (`docs/operator-manual.md`, `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md`).
- **Step 8**: enterprise foundation contract + read-only
  inspector. Никакого fake `enterprise_ready` флага — только
  `foundation_level` + отдельный `ready_for_enterprise_track`.
- **Step 9**: подтверждённая интеграция всего вышеперечисленного
  в один связный сценарий.

### Что Phase 6 НЕ делает (явные не-цели)

- Платформа **не** претендует на enterprise-ready / production-
  ready статус. `ready_for_enterprise_track=True` — это
  «foundation under next-step enterprise work собран», не
  «готовы к prod».
- Нет SSO/RBAC, нет multi-tenant, нет secrets vault как
  сервиса, нет federated audit storage, нет policy-as-code
  DSL, нет multi-instance HA, нет web-UI / dashboard
  frontend'а.
- Нет Windows Service / systemd unit registration; нет
  background watcher / supervisor / auto-restart-loop'а; нет
  hot reload; нет journald / log aggregation / forwarding.
- Нет AST-парсера для XML / BSL; нет полного DOM-edit covering
  для всех metadata-операций — структурно переписан только
  один slice (`add_form_attribute`); существующие
  `add_catalog_attribute` / `add_document_attribute` /
  form/module-level Phase 3 tools остались на substring-патч'е.
- Нет полного замещения Phase 2 stub'ов (`apply_config_from_files`,
  `update_database_configuration`) на binary-backed dispatch.
  Phase 6 ship'ит **один** binary-backed slice
  (`create_dump_snapshot`).
- Нет расширения rollback whitelist'а beyond двух tool'ов.
- Нет AST-парсера BSL; нет ML / clustering поверх
  `analyze_event_log_patterns`; нет настоящего topo-sort
  `suggest_safe_change_order` по графу зависимостей.
- Нет production-grade MCP transport / `__main__` / CLI у трёх
  MCP-серверов.
- Нет полного version-matrix smoke на всех 1С-версиях и
  стендах.
- Нет GUI installer / wizard / `.msi` / `.deb` / signed binary
  distribution.
- Operator/admin/developer **runbook coverage** ограничен
  шестью recipes Step 7 (`docs/runbooks.md`); production
  runbook-вселенная — отдельный track.

Эти ограничения — **honest constraints**, не «технический долг»;
они вынесены за пределы Phase 6 by design. Расширять их —
parallel / enterprise tracks ПОСЛЕ Phase 6.

## Parallel Track A / Step 5 — product-layer integration over real write path

После закрытия Phase 6 открыт **post-phase completion track A —
Full Real 1cv8-backed Write Path**. Шаги 2–4 трека жили
строго внутри `mcp-write-server`: они переключили три
binary-backed write-tool'а
(`create_dump_snapshot` / `apply_config_from_files` /
`update_database_configuration`) на честный dual-mode contract
через единый internal helper
`apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`
и расширили `EnvironmentConfig` симметричными
`onec_applycfg_command_template` / `onec_updatedb_command_template`
в дополнение к уже существовавшему
`onec_dumpcfg_command_template` (см. корневой README).

**Step 5 — это product-layer surface-only update.** Никаких
изменений в write-server'е, MCP-серверах, `onec-policy-engine`,
`onec-config` schema, registry counts'ах. Меняются ровно две
boundary-функции продуктового слоя — так, чтобы они честно
отражали уже существующий real write contract.

### Что меняет Step 5

- **`run_real_stand_smoke_test(...)` plan summary (Q7).** Раньше
  `_build_plan_summary` нёс stale claim «Phase 2 stubs … are NOT
  rewritten on this step — that is a parallel track». После
  Track A / Steps 2–4 этот текст лжив: dual-mode contract уже
  существует у всех трёх tool'ов. Step 5 заменяет advisory на
  честный текст: три tool'а названы по имени; явно указано, что
  они получили honest dual-mode contract в Track A / Steps 2–4
  через unified internal `binary_dispatch` helper; smoke сам по
  себе остаётся **bounded probe**, не chain'ит dump → apply →
  updatedb на реальном binary'е; multi-step round-trip — это
  Track A / Step 6, не данный surface; smoke по-прежнему не
  мутирует infobase и не вызывает MCP write-tool'ов из себя.
  Те же honest формулировки добавлены в module-docstring
  `realstand.py` и в Step 7-блок package-docstring'а
  `onec_platform.__init__`. Никаких изменений сигнатур,
  никаких изменений `RealStandSmokeResult` shape'а.
- **`inspect_enterprise_foundation(...)` section D (Q8).**
  Раньше binary-section проверяла только
  `onec_binary_path` + `onec_dumpcfg_command_template`,
  score 0..2. После Track A foundation должна оценивать
  **полный** real-write contract:
  - `_check_real_stand_contract` теперь проверяет все три
    template'а (dumpcfg / applycfg / updatedb) симметрично
    вместе с binary path; score range расширен до 0..4.
  - На prod-like config'ах отсутствие любого из трёх
    template'ов — **error** finding с code'ами вида
    `foundation_onec_<op>_template_missing_on_prod` и
    соответствующим recommended-action; на non-prod —
    presumed warning (`foundation_onec_<op>_template_missing`),
    не блокирующий ok=True.
  - При полном contract'е (binary + 3 template'а) появляется
    presumed-finding `foundation_real_write_path_contract_complete`;
    при только dumpcfg-сабсете — старый
    `foundation_real_stand_smoke_contract_available` остаётся
    как валидный fallback advisory.
  - `_SECTION_MAX_SCORE['binary']` поднят с 2 до 4. Логика
    `_classify_foundation_level` не изменена — `'strong'`
    автоматически требует full contract в section D.
  - Step 1–4 product-config'и (без apply/updatedb template'ов)
    продолжают загружаться без изменений: на non-prod ничего
    не сломано; на prod-like неполный contract честно
    surface'ится как error / not 'strong'.

### Дисциплина, которая сохранилась

- **Registries не двигались.** `read=15 / write=25 / intelligence=16` —
  без drift'а; никакого нового MCP-tool'а в Step 5 нет.
- **`onec_policy_engine` не импортируется** ни из
  `apps/platform/src`, ни из `apps/mcp-intelligence-server/src`.
- **Никакого back-door write channel'а** из продуктового слоя:
  Step 5 ничего не пишет на диск, не зовёт `run_write_flow`,
  не открывает subprocess'ы; это **surface-only** update.
- **Operator-facing shape'ы не трогали.** `RealStandSmokeResult`,
  `EnterpriseFoundationResult` — те же dataclass-поля, что и до
  Step 5; добавились только новые finding-code'ы на готовых
  списках `confirmed_findings` / `presumed_findings`.
- **Honest dual-mode discipline.** Foundation inspector
  по-прежнему не пытается **запустить** binary; Q8 — это
  contract-level inspection, а не probe.

### Manual verification (`phase-tracka-step5-check.py`)

В `C:\Users\user\AppData\Local\Temp\phase-tracka-step5-check.py`
лежит manual-check со семью сценариями:

- **A** — registry invariants (read=15, write=25, intelligence=16) +
  full whitelist parity со Step 4 contract;
- **B** — backward compatibility: Step 1–4 product-config (без
  apply/updatedb template'ов) загружается через
  `inspect_enterprise_foundation` без error'ов и видит missing
  template'ы как presumed warnings;
- **C** — четыре подкейса foundation inspector'а:
  - C1: enterprise section absent → `foundation_level='absent'`;
  - C2: только dumpcfg на prod-like → applycfg / updatedb error
    finding'и, binary=2/4, не `'strong'`;
  - C3: dumpcfg + applycfg, без updatedb на prod-like → updatedb
    error, binary=3/4, не `'strong'`;
  - C4: full contract на prod-like + чистые остальные секции →
    binary=4/4, presumed `foundation_real_write_path_contract_complete`,
    `foundation_level='strong'`, `ready_for_enterprise_track=True`;
- **D** — real-stand smoke advisory: plan_summary упоминает все
  три binary-backed tool'а, упоминает Track A / Steps 2–4,
  упоминает dual-mode и bounded probe semantics, упоминает что
  multi-step round-trip — это Track A / Step 6; запрещённые
  устаревшие фразы («Phase 2 stubs», «are NOT rewritten», fake
  chain claims) отсутствуют;
- **E** — broken JSON paths: оба `*_from_json_file` boundary'я
  возвращают `ok=False` без exception'ов, в т.ч. на синтаксически
  битом JSON'е;
- **F** — suggested-tools discipline: имена в
  `EnterpriseFoundationResult.suggested_tools` /
  `suggested_write_tools` и `RealStandSmokeResult.suggested_tools` /
  `suggested_write_tools` — все из live registries или из
  `_KNOWN_PLATFORM_FUNCTIONS`; made-up имя отвергается;
- **G** — ноль реальных импортов `onec_policy_engine` под
  `apps/platform/src/` и `apps/mcp-intelligence-server/src/`.

Все семь сценариев — green. Dev-check (`scripts/dev/selfcheck.py`)
после Step 5 — тоже green.

### Что Step 5 НЕ делает

- **Не запускает multi-step round-trip.** Реальный
  DumpCfg → LoadCfg → UpdateDBCfg на reference stand'е
  останется отдельным шагом — Track A / Step 6.
- **Не меняет behaviour write-tool'ов.** Step 5 только
  **наблюдает** контракт; per-tool placeholder whitelists,
  argv grammar, `ToolResult` shape — всё zero-touch для
  write-server'а.
- **Не вводит новый MCP-tool / новый product-layer boundary.**
  Все изменения — внутри двух уже существующих функций
  (`run_real_stand_smoke_test`, `inspect_enterprise_foundation`).
- **Не валидирует семантику CLI 1cv8.** Foundation inspector
  смотрит на присутствие template'а, не на «правильность»
  argv'а — это уже задача render-time placeholder validation
  у write-server'а (per-tool whitelist).
- **Не меняет `onec_policy_engine` / RBAC / SSO / multi-tenant.**
  Эти направления — отдельные track'и, Step 5 их не открывает.
