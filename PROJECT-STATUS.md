# PROJECT STATUS — 1C Agent Platform

## Текущий шаг

**Активного шага нет.** Parallel Track C полностью закрыт
на Step 6 (final integration pass and Track C closure).
Track A и Track B закрыты ранее. Открытие следующего
parallel track'а — отдельное решение оператора.

## Статус

`closed` (для всего Parallel Track C — Steps 1–6 закрыты
последовательно; шесть meaningful commit'ов в `main`:
`af2d7f4` (Step 1 — planning packaging and installer
delivery), `ef087c8` (Step 2 — release-facing verify path
and layout polish), `a4f42f9` (Step 3 — packaging-facing
install flow honest review), `7ca9b3f` (Step 4 — release
handoff documentation), `8ccecf6` (Step 5 — integration
and handoff polish), плюс closure commit Step 6 фиксирует
обновлённые README/PROJECT-STATUS/CHANGELOG; production-
код Track C **не правил вообще ни разу** — все
deliverables это release-facing скрипты, документация и
honest pyproject limitation; registries без drift'а на
всём треке; `selfcheck_status=ok`).

`closed` (для всего Parallel Track B — Steps 1–6 закрыты
последовательно; четыре meaningful commit'а в `main`:
`85a4a7e` (Step 2 — repo hygiene + legal baseline),
`bce8966` (Step 3 — install fast path operator-discoverable),
`fd92477` (Step 4 — operator/dev local launch umbrella),
`0f65c58` (Step 5 — root README quickstart and docs polish),
плюс closure commit `6e2c5ee` (Step 6) фиксирует обновлённые
README/PROJECT-STATUS/CHANGELOG; production-код Track B
**не правил вообще ни разу** — все deliverables это
scripts-only wrapper'ы, repo hygiene и documentation;
registries без drift'а на всём треке;
`selfcheck_status=ok`).

`closed` (для всего Parallel Track A — Phase 1–6
закрыты ранее; Track A / Steps 1–7 закрыты;
Parallel Track A / Step 1 завершён как documentation-only
opening; Step 2 завершён —
`apply_config_from_files(...)` переведён на dual-mode;
Step 3 завершён —
`update_database_configuration(...)` тоже переведён на
dual-mode; Step 4 завершён — внутренняя унификация
binary-backed execution contract'а между всеми тремя
binary-backed write-tool'ами без расширения surface'а;
Step 5 завершён — product-layer surface honestly reflects
the real write contract: Q7 closed in `realstand.py` plan
summary, Q8 closed in `enterprise.py` foundation
inspector; **Step 6 закрыт honestly**: real
multi-step round-trip отработал на real 1cv8 binary'е
(`C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe`) и
real file-based инфобазе InfoBase6 — A.2 / A.4 / A.5
все binary-backed зелёные, audit honest (две mutating
audit row + `details.dump_snapshot_path` populated в
обеих); doc/expectation gap (runbook + local chain
ожидали 3 audit row, фактически 2) выровнен под
production-код by design. **Step 7 закрыт без
production-правок**: existing evidence Step 6
round-trip'а покрывает acceptance criteria 1–5,
discipline asserts criteria 6–10 удовлетворены
(registries без drift'а, ноль импортов
`onec_policy_engine` в product/intelligence, нет
back-door write channel'а, operator-facing messages
честные, Track A closed как documented status).
Closure выполнен обновлением closure-status в
`README.md` и `PROJECT-STATUS.md` — без новых
запусков 1cv8.exe. Registry-инвариант **сохранён точно**:
read-server = 15 public tools, write-server = 25 public
tools, intelligence-server = 16 public tools — без
изменений. Никаких новых MCP tool'ов; никаких новых
product-layer slice'ов; никаких изменений в
`mcp-read-server`, `mcp-write-server`,
`mcp-intelligence-server`, `onec-policy-engine`,
`onec-audit`, `onec-health`, `onec-process-runner`,
`onec-troubleshooting`, `mcp-common`, `onec-config`,
`selfcheck.py`, `bootstrap_paths.ps1`, `pyproject.toml`,
`.github/`, `.claude.json`. Все Step 5 правки
локализованы внутри `apps/platform/src/onec_platform/`:
`enterprise.py` (`_check_real_stand_contract` теперь
проверяет все три command template'а; `_SECTION_MAX_SCORE
['binary']` поднят с 2 до 4) + `realstand.py`
(`_build_plan_summary` обновлён + module-docstring) +
`__init__.py` (Step 7-блок package-docstring'а обновлён
до Track A-aware формулировки). Operator-facing argv
grammar / placeholder whitelists per tool / ToolResult
shape / `RealStandSmokeResult` / `EnterpriseFoundationResult`
shape **без изменений**. Step 5 — это **surface-only**
update: продуктовый слой ничего не пишет на диск, не
зовёт `run_write_flow`, не открывает subprocess'ы. Step 6
— **operator-driven exercise**: ship'нут один runbook
+ один prereq-inventory скрипт; production-код **не
тронут**; реальный round-trip запускается оператором
на reference stand'е, который должен быть подготовлен
по runbook'у (declared product-config, real infobase,
real DESIGNER credentials). В текущем dev-окружении
шаг **partial result**: real 1cv8 binary найден на
машине, render-pipeline для всех трёх template'ов OK,
но stand prereq'ы (infobase, source dump, credentials)
отсутствуют, поэтому real round-trip не запускался —
был бы нечестным. Это **partial slice** Track A, не
его финальное закрытие (Step 6 ждёт стенд, Step 7 —
final integration pass + closure). Safety
guarantees Phase 1–6 (`run_write_flow` единственный
mutating-путь; intelligence read-only;
`onec_policy_engine` не импортируется в
product/intelligence; нет back-door write channel'а;
нет `shell=True`; audit append-only; fail-closed по
умолчанию) **сохраняются без изменений**).

После closure'а Track C активного трека нет. Track A,
Track B и Track C закрыты последовательно как post-phase
completion track'и. Phase 7 как линейная фаза не
запланирована. Возможные следующие parallel track'и
перечислены в конце Track B Step 6 секции (operator
credentials hardening, multi-version 1С matrix, full
rollback whitelist) — это **только recommendations**, без
авто-открытия. **GitHub remote push** не часть Track C —
repo готов к выкладке, но пушить — operator action.

## Что сделано

### Phase 0 / Step 1 — каркас монорепозитория (завершён)

- Создана корневая папка проекта `C:\Tools\1c-agent-platform`.
- Создана полная структура каталогов монорепозитория:
  - `apps/` с подпапками `mcp-read-server`, `mcp-write-server`, `mcp-intelligence-server`;
  - `packages/` с подпапками `mcp-common`, `onec-process-runner`, `onec-policy-engine`,
    `onec-audit`, `onec-health`, `onec-troubleshooting` (позже добавлен `onec-config`);
  - `docs/` с подпапками `architecture`, `tools-spec`, `safety`, `runbooks`, `api`;
  - `examples/` с подпапками `demo-infobase`, `demo-dumps`, `sample-patches`;
  - `scripts/` с подпапками `dev`, `test`, `release`.
- Созданы базовые файлы в корне репозитория:
  - `README.md`, `PROJECT-STATUS.md`, `.gitignore`.
- В каждой папке первого уровня внутри `apps/`, `packages/`, `docs/`, `examples/`, `scripts/`
  добавлен короткий `README.md` с назначением раздела.

### Phase 0 / Step 2 — root-конфиг и Python bootstrap (завершён)

- Добавлен корневой `pyproject.toml` (минимальный: `hatchling`, метаданные проекта,
  базовые настройки `ruff` и `pytest`, пустой список пакетов в `hatch`).
- Добавлен `.editorconfig` (utf-8, LF, 4 пробела, отдельное правило для `*.md`).
- Добавлен `.python-version` (Python 3.11).
- Создан `src`-bootstrap для каждого приложения и пакета с `__init__.py`
  и собственным `README.md`.

### Phase 0 / Step 3 — базовые общие пакеты-заглушки (завершён)

- `mcp-common`: базовые контексты и исключения.
- `onec-process-runner`: `ProcessRunRequest`, `ProcessRunResult`,
  `run_process` (stub, поднимает `NotImplementedError`).
- `onec-policy-engine`: `PolicyDecision`, `check_write_allowed`.
- `onec-audit`: `AuditRecord`, `format_audit_record`.
- `onec-health`: `HealthCheckResult`, `check_dump_path_exists`.

### Phase 0 / Step 4 — troubleshooting / config / health flow (завершён)

- Добавлен новый пакет `onec-config`:
  `EnvironmentConfig`, `ProjectConfig`, `load_project_config`.
- `onec-troubleshooting`: `TroubleshootingReport`, `diagnose_from_health`.
- `onec-health` расширен: `summarize_health`, stub-проверки
  `check_http_gateway_available`, `check_search_index_available`.

### Phase 0 / Step 5 — skeleton для mcp-read-server (завершён)

- `mcp-read-server`: `ToolResult`, `ping()`, `health_summary(...)`.
- Server registry skeleton (`REGISTERED_TOOLS`, `list_tools()`, `get_tool()`).
- Wiring к `onec-health` и `onec-troubleshooting`.

### Phase 0 / Step 6 — skeleton для mcp-write-server и mcp-intelligence-server (завершён)

- `mcp-write-server`, `mcp-intelligence-server`: `ToolResult`, `ping()`, registry skeleton.
- Все три сервера платформы получили выровненный минимальный bootstrap.

### Phase 0 / Step 7 — workspace / import wiring и self-check (завершён)

- Создан `scripts/dev/bootstrap_paths.ps1` — PowerShell-скрипт,
  выставляющий `PYTHONPATH` под монорепо в **только текущую** сессию
  (10 путей: 3 apps + 7 packages). Не трогает системный PATH и реестр.
- Создан `scripts/dev/selfcheck.py` — минимальный self-check, который
  импортирует все skeleton-модули и безопасно вызывает их базовые функции
  (`ping`, `list_tools`, `check_write_allowed`, `summarize_health`,
  `diagnose_from_health`, `load_project_config`, `format_audit_record`,
  `health_summary`) на встроенных фиктивных данных. Без `try/except` —
  любая ошибка wiring должна валиться честно.
- Создан `scripts/dev/README.md` — описание назначения скриптов
  и команд запуска.
- Подтверждено, что `bootstrap_paths.ps1` отрабатывает корректно:
  `PYTHONPATH` проставляется, все 10 `src/` путей видны в текущей сессии.
- В `selfcheck.py` добавлен реальный вызов `health_summary(...)` через
  wiring `mcp-read-server → onec-health → onec-troubleshooting` и печать
  `health_summary_ok` / `health_summary_problem`.
- После установки реального Python 3.11+ selfcheck запущен локально
  и прошёл успешно: `imports_ok = true`, все три сервера видят свои
  registry-инструменты, `health_summary_ok = false` для заведомо плохих
  входных данных с корректным `health_summary_problem = gateway_down`,
  `selfcheck_status = ok`.

**Итог Step 7:**

- PYTHONPATH bootstrap работает в рамках текущей PowerShell-сессии.
- Все skeleton-модули (`mcp_read_server`, `mcp_write_server`,
  `mcp_intelligence_server`, `onec_policy_engine`, `onec_audit`,
  `onec_config`, `onec_health`, `onec_troubleshooting`) импортируются
  без ошибок.
- `scripts/dev/selfcheck.py` прошёл успешно и выдал
  `selfcheck_status = ok`.

### Phase 0 / Step 8 — mcp-common bootstrap contract и унификация envelope / registry (завершён)

- `mcp-common` расширен shared response envelope:
  `mcp_common/result.py` — dataclass `ToolResult`
  (`ok`, `tool_name`, `message`, `payload`). Это единый конверт ответа
  для всех трёх MCP-серверов платформы.
- `mcp-common` расширен shared registry helpers:
  `mcp_common/registry.py` — `ToolCallable`,
  `build_tool_registry(tools)`, `list_registered_tools(registry)`,
  `get_registered_tool(registry, name)`. Без валидации и магии,
  только стандартная библиотека.
- `mcp_common/__init__.py` теперь экспортирует:
  `OperationContext`, `PlatformError`, `PolicyDeniedError`,
  `ProcessExecutionError`, `HealthCheckError`, `ToolResult`,
  `ToolCallable`, `build_tool_registry`, `list_registered_tools`,
  `get_registered_tool`.
- `mcp-read-server`, `mcp-write-server`, `mcp-intelligence-server`
  приведены к общему контракту:
  - `models.py` в каждом сервере стал compatibility wrapper,
    re-export `ToolResult` из `mcp_common` — старые внутренние
    импорты `.models` продолжают работать;
  - `server.py` каждого сервера собирает `REGISTERED_TOOLS`
    через `build_tool_registry(...)`, а `list_tools()` / `get_tool()`
    делегируют shared helpers;
  - `tools.py` по смыслу не менялся.
- README `mcp-common` обновлён: shared exception hierarchy,
  `OperationContext`, shared `ToolResult`, shared registry helpers.
  README трёх серверов помечены как использующие shared contracts из
  `mcp-common`.
- Локальный `scripts/dev/selfcheck.py` (без изменений на этом шаге)
  повторно запущен после унификации и прошёл успешно:
  `imports_ok = true`, registry-составы серверов не изменились
  (`read=['health_summary','ping']`, `write=['ping']`,
  `intelligence=['ping']`), `health_summary_ok = false`,
  `health_summary_problem = gateway_down`, `selfcheck_status = ok`.

### Phase 0 / Step 9 — минимальный CI skeleton + единая команда локальной проверки (завершён)

- Добавлен `scripts/dev/run_dev_check.ps1` — единая локальная dev-check
  команда. Dot-source'ит `bootstrap_paths.ps1` в текущей сессии и
  запускает `selfcheck.py`; при успехе печатает
  `Dev check completed successfully.`, при ошибке завершается с exit
  code, полученным от Python. Ничего не устанавливает и не меняет
  системное окружение.
- Добавлен `.github/workflows/dev-check.yml` — минимальный CI skeleton.
  Один job `dev-check` на `windows-latest`: checkout,
  `actions/setup-python@v5` с Python 3.11, затем в pwsh-шаге
  `bootstrap_paths.ps1` + `selfcheck.py`. Без установки пакетов,
  без pytest, ruff, matrix и других job'ов.
- Добавлен `docs/runbooks/local-dev-check.md` — короткий runbook
  локальной dev-проверки: цель, prerequisites, команда запуска,
  критерии успеха, типовые падения.
- Обновлён `scripts/dev/README.md` — упомянута новая команда
  `run_dev_check.ps1` и соответствие CI workflow. Зафиксировано,
  что это минимальный quality gate Phase 0, проверяющий только
  import/wiring skeleton-проекта.
- Локальный `run_dev_check.ps1` запущен в текущей сессии: bootstrap
  выставляет все 10 `src/` путей, `selfcheck.py` печатает
  `selfcheck_status = ok`, скрипт заканчивает работу сообщением
  `Dev check completed successfully.`

### Phase 0 / Finalize — закрытие инфраструктурной фазы (завершён, Phase 0 закрыта)

- Добавлен `docs/architecture/phase-0-summary.md` — итоги Phase 0:
  назначение, что собрано, что подтверждено на практике, что пока
  ещё не реализовано, вывод по фазе.
- Добавлен `docs/architecture/phase-1-entry.md` — точка входа в Phase 1:
  цель фазы, что готово на входе, первое приближение набора
  read-tools, критерии MVP фазы, риски.
- Корневой `README.md` приведён в актуальное состояние: устаревший
  единичный блок «Статус» заменён на раздел «Текущий статус по фазам»
  с явной отметкой закрытия Phase 0 и входа в Phase 1 и ссылками
  на оба новых документа архитектуры.
- **Phase 0 завершена.** Инфраструктурная база готова:
  монорепо + shared контракты + skeleton трёх серверов + воспроизводимый
  dev-check локально и в CI.
- `dev-check` подтверждён зелёным: `selfcheck_status = ok`,
  `Dev check completed successfully.`
- Следующим этапом открывается Phase 1 — Read MVP.

### Phase 1 / Step 1 — планирование Read MVP и фиксация первого набора реальных read-tools (завершён)

- Phase 0 закрыта; Phase 1 — активная фаза разработки.
- Добавлен `docs/architecture/phase-1-read-mvp-plan.md` — план Read MVP:
  назначение фазы, целевой результат, первый набор инструментов по
  группам A (live-read), B (dump-read), C (health/diagnostics),
  порядок реализации внутри Phase 1, что не входит в Read MVP,
  критерии приёмки.
- Добавлен `docs/architecture/phase-1-step-map.md` — стартовый
  implementation map на первые 6 шагов Phase 1: реальный
  `onec-process-runner`, рабочий `onec-config` окружения,
  реальные live-health-checks в `onec-health`, базовый runtime/adapter
  слой для `mcp-read-server`, первые live-read инструменты,
  первые dump-read инструменты.
- Зафиксирован первый набор инструментов MVP:
  live-read — `get_configuration_info`, `get_metadata_tree`,
  `get_metadata_object`, `get_object_structure`, `get_form_structure`,
  `validate_query`, `execute_read_query`, `get_event_log`;
  dump-read — `read_module_code_from_dump`, `search_code`,
  `search_metadata`;
  diagnostics — `check_runtime_health`, `diagnose_connectivity_issue`.
- Обновлён корневой `README.md`: существующий блок «Текущий статус по
  фазам» уточнён — Phase 1 помечена как активный этап, добавлены
  ссылки на `phase-1-read-mvp-plan.md` и `phase-1-step-map.md`.

### Phase 1 / Step 2 — реальный `onec-process-runner` вместо stub (завершён)

- В `packages/onec-process-runner` stub заменён на реальный runner
  поверх `subprocess.run`. Никаких `shell=True`, `os.system` или
  ручного `Popen`.
- `ProcessRunRequest` расширен до нужного минимума: добавлены
  `env: dict[str, str] | None`, `input_text: str | None`, тип
  `timeout_seconds` расширен до `int | float | None`. `ProcessRunResult`
  оставлен без изменений (`exit_code`, `completed`, `stdout`, `stderr`).
- Runner поддерживает `cwd`, `timeout_seconds`, `env`, `input_text`,
  захват stdout/stderr в текстовом режиме. `check=False` — коды
  возврата не конвертируются в исключения.
- **Timeout** (`subprocess.TimeoutExpired`) не выбрасывается наружу:
  возвращается `ProcessRunResult(completed=False, exit_code=-1, ...)`
  с частично собранным stdout/stderr и служебной пометкой о таймауте
  в stderr.
- **`FileNotFoundError`** (отсутствует исполняемый файл) и прочие
  `OSError` на старте процесса преобразуются в `ProcessExecutionError`
  из `mcp_common` с понятным сообщением.
- README пакета переписан: актуальное поведение, контракт ошибок,
  ограничения (не shell, не логи, не файлы).
- Ручная проверка трёх сценариев выполнена через временный скрипт в
  `%TEMP%` под bootstrap'нутым `PYTHONPATH`:
  - A (success): `completed=True`, `exit_code=0`, `stdout='runner-ok'`;
  - B (timeout): `completed=False`, `exit_code=-1`, stderr содержит
    `[onec-process-runner] process timed out after 0.5 seconds`;
  - C (missing command): поднят `ProcessExecutionError: Executable
    not found: definitely-nonexistent-command-xyz`.
- `dev-check` после изменений остался зелёным: `selfcheck_status = ok`,
  `Dev check completed successfully.`

### Phase 1 / Step 3 — рабочая модель окружения в `onec-config` (завершён)

- `EnvironmentConfig` расширен до рабочей формы: добавлены обязательные
  поля `base_id: str`, `dump_path: str`, `timeout_seconds: int | float`.
  Существующие поля (`name`, `base_path`, `publication_name`,
  `http_base_url`, `allow_write`) сохранены. `allow_write` остаётся
  опциональным со значением по умолчанию `False`. `ProjectConfig`
  без изменений (`environments: dict[str, EnvironmentConfig]`).
- `load_project_config(data)` теперь валидирует структуру:
  `ValueError` при отсутствии ключа `environments`, при пустом
  `environments` и при отсутствии любого обязательного поля в
  окружении — с именем окружения и именем поля в тексте ошибки.
  Никаких файловых операций, `os.environ` или внешнего I/O —
  чистая валидация входного dict'а.
- `__init__.py` уже экспортировал `EnvironmentConfig`, `ProjectConfig`,
  `load_project_config` через `__all__` — оставлен как есть.
- README `onec-config` переписан: перечислены обязательные поля,
  описано поведение loader'а и явно зафиксировано, что чтение из
  файлов/переменных окружения пока не реализовано.
- Ручная проверка трёх сценариев выполнена через временный скрипт в
  `%TEMP%` под bootstrap'нутым `PYTHONPATH`:
  - A (valid config): `environments=['local-dev']`, все поля
    прочитаны корректно, `allow_write=True` учтён;
  - B (missing `environments`): `ValueError: Config is missing
    required key 'environments'.`;
  - C (missing required field `dump_path`): `ValueError: Environment
    'local-dev' is missing required field 'dump_path'.`.
- **Follow-up по `selfcheck.py` выполнен.** В тестовый dict
  `load_project_config` в `scripts/dev/selfcheck.py` добавлены
  безопасные фиктивные значения для новых обязательных полей:
  `base_id="local-dev"`, `dump_path="C:\\tmp\\dump\\local-dev"`,
  `timeout_seconds=30`. Остальная логика selfcheck'а не менялась,
  `run_dev_check.ps1` и `bootstrap_paths.ps1` не трогались.
- **Dev-check снова зелёный** после follow-up:
  `imports_ok = true`, `config_envs = ['local-dev']`,
  `health_summary_ok = false`, `health_summary_problem = gateway_down`,
  `selfcheck_status = ok`, `Dev check completed successfully.`

### Phase 1 / Step 4 — реальные live/dump health checks в `onec-health` (завершён)

- `onec-health` переведён со stub на реальные проверки. Контракт
  `HealthCheckResult` и `summarize_health` не меняются.
- `check_dump_path_exists(path)` — без изменений, уже был реальной
  проверкой через `pathlib.Path.exists()`.
- `check_http_gateway_available(target, timeout_seconds=None)` теперь
  работает в двух режимах:
  - `target: bool` — legacy stub-режим, сохранён ради совместимости
    с текущим `scripts/dev/selfcheck.py`;
  - `target: str` — реальный HTTP probe через `urllib.request`:
    `status="ok"` при HTTP 2xx/3xx, `status="error"` иначе. Сетевые
    исключения, таймауты и `HTTPError` не выходят наружу —
    всегда возвращается `HealthCheckResult` с кратким пояснением.
- `check_search_index_available(target)` также получила два режима:
  - `target: bool` — legacy stub;
  - `target: str` — путь к каталогу выгрузки: `status="ok"`, если
    каталог существует и рекурсивно найден хотя бы один файл `.bsl`;
    иначе `error`. Ошибки сканирования ловятся, не вылетают наружу.
- Добавлена функция
  `check_environment_health(environment: EnvironmentConfig)` —
  запускает три базовых проверки по `EnvironmentConfig` из
  `onec-config` (`dump_path`, `http_base_url` + `timeout_seconds`,
  `dump_path`) и возвращает список из трёх `HealthCheckResult` в
  стабильном порядке.
- `__init__.py` дополнен экспортом `check_environment_health` в
  `__all__`.
- README `onec-health` переписан: явно зафиксирован выход из stub,
  bool-совместимость, контракт новых режимов, what-not-does.
- **Ручная проверка на реальном стенде** выполнена через временные
  скрипты в `%TEMP%` под bootstrap'нутым `PYTHONPATH`:
  - **A (`dump_path_exists`)**: путь
    `C:\Tools\mcp-1c\config-dump\InfoBase5-with-code-20260423-004101`
    существует → `status="ok"`. ✓
  - **B (`http_gateway` по URL
    `http://localhost:8080/InfoBase5/hs/mcp-1c/version`)**:
    `status="error"` — WinError 10061 (connection refused).
    Проверка `Test-NetConnection localhost 8080` подтвердила, что
    TCP-порт 8080 сейчас **не слушается**, то есть Apache стенда
    не запущен. Это не баг реализации, а фактическое состояние
    окружения; инструкция запрещает трогать Apache/публикацию.
  - **B-local (контрольная проверка success-path)**: запущен
    короткоживущий `http.server` внутри того же Python-процесса на
    случайном порту `127.0.0.1:<port>`; `check_http_gateway_available`
    вернул `status="ok"` (HTTP 200). Это подтверждает, что сам
    HTTP-probe (urllib, тайм-аут, обработка кода ответа) работает
    корректно. Отрицательный результат пункта B — честный сигнал
    о состоянии стенда.
  - **C (`search_index` по dump path)**: dump содержит `.bsl` →
    `status="ok"`. ✓
  - **D (`check_environment_health` по реальному `EnvironmentConfig`
    стенда)**: возвращён список из трёх `HealthCheckResult`;
    `dump_path_exists=ok`, `http_gateway=error` (по той же причине,
    что и B), `search_index=ok`. Помимо HTTP-части, ожидание ТЗ
    (три ok) не подтверждено ровно потому, что Apache стенда сейчас
    лежит; сам helper работает правильно — все три проверки
    выполнены в правильном порядке, каждая вернула корректный
    `HealthCheckResult` для фактического состояния ресурса.
- **Dev-check после изменений зелёный:**
  `imports_ok = true`, `selfcheck_status = ok`,
  `Dev check completed successfully.` Сохранённая bool-совместимость
  в `check_http_gateway_available(False)` и
  `check_search_index_available(True)` удерживает skeleton selfcheck
  работоспособным.

### Phase 1 / Step 5 — базовый runtime/adapter слой для `mcp-read-server` (завершён)

- Внутри `apps/mcp-read-server/src/mcp_read_server/` создан подпакет
  `runtime/` — внутренний слой ниже tool-уровня. Пока он не
  используется ни одним зарегистрированным инструментом: `tools.py`,
  `server.py`, верхний `__init__.py` и `models.py` read-server'а
  не тронуты. Skeleton registry остался прежним.
- **`runtime/models.py`** — dataclass `RuntimeContext(environment,
  health_results, health_codes)`. Импортирует `EnvironmentConfig` из
  `onec_config`, `HealthCheckResult` из `onec_health`.
- **`runtime/context.py`** — `build_runtime_context(environment)`:
  вызывает `check_environment_health(environment)`, затем
  `summarize_health(...)`, возвращает `RuntimeContext`. Без
  side-effects и без искусственных исключений.
- **`runtime/live_adapter.py`** — `fetch_json(url, timeout_seconds)`:
  HTTP GET через `urllib.request`, UTF-8 decode, `json.loads`,
  проверка что тело — именно dict. Любые сетевые/decode-ошибки
  заворачиваются в `PlatformError` из `mcp-common`.
  `fetch_json_from_environment(environment, relative_path)` —
  аккуратная сборка `base.rstrip('/') + '/' + relative.lstrip('/')`
  (без двойных слэшей), вызов `fetch_json` с таймаутом окружения.
- **`runtime/dump_adapter.py`** — `resolve_dump_path(environment)`,
  `read_text_file(path)` (UTF-8 + `errors='replace'`, ошибки →
  `PlatformError`), `find_files_by_pattern(root, pattern)`
  (отсортированный `rglob`, `PlatformError` если `root` нет),
  `read_dump_file(environment, relative_path)`.
- **`runtime/__init__.py`** экспортирует в `__all__`: `RuntimeContext`,
  `build_runtime_context`, `fetch_json`, `fetch_json_from_environment`,
  `resolve_dump_path`, `read_text_file`, `find_files_by_pattern`,
  `read_dump_file`.
- README `mcp-read-server` дополнен разделом «Runtime / adapters
  layer» с кратким описанием трёх подсистем (context builder,
  live HTTP adapter, dump file adapter).
- **Ручная проверка 4 сценариев** через временный скрипт в `%TEMP%`
  под bootstrap'нутым `PYTHONPATH`:
  - **A (`build_runtime_context` по реальному `EnvironmentConfig`):**
    `RuntimeContext`, `health_results_len = 3`, `health_codes =
    ['gateway_down']` (как и ожидалось — Apache стенда не запущен).
    Результаты: `dump_path_exists=ok`, `http_gateway=error`,
    `search_index=ok`. ✓
  - **B (`fetch_json` против URL стенда):** `PlatformError: Failed
    to fetch http://localhost:8080/InfoBase5/hs/mcp-1c/version:
    <urlopen error [WinError 10061] ...>` — транспортная ошибка
    корректно заворачивается в `PlatformError`. Apache по-прежнему
    не поднят, инструкция запрещает его трогать.
  - **B-local (success-path `fetch_json`):** локальный
    `socketserver.TCPServer` с `BaseHTTPRequestHandler`, отдающий
    `{"version": "local-test-1.0"}`. Результат:
    `{'version': 'local-test-1.0'}` — JSON правильно раздекодирован
    в dict, dict-guard не ложно-позитивен.
  - **C (`resolve_dump_path` + `find_files_by_pattern`):** путь
    резолвится корректно; `find_files_by_pattern(root, "*.bsl")`
    возвращает 1 файл —
    `CommonModules\MCPTestCode\Ext\Module.bsl`. ✓
  - **D (`read_dump_file` для
    `CommonModules\MCPTestCode\Ext\Module.bsl`):** возвращён
    непустой текст (`text_len = 215`), маркер `MCP_SMOKE_TEST`
    найден, кириллическое имя функции `ПолучитьСтатусMCP` найдено
    (в консоли Windows отображение сбилось по кодовой странице,
    но substring-поиск идёт по Python-строке и честно возвращает
    `True`). ✓
- **Dev-check после изменений зелёный:** `selfcheck_status = ok`,
  `Dev check completed successfully.` Новый подпакет не
  импортируется из skeleton selfcheck (он, согласно ТЗ, не менялся);
  существующий wiring read-server'а сохранён как есть.

### Phase 1 / Step 6 — первые live-read инструменты (завершён)

- В `apps/mcp-read-server/src/mcp_read_server/tools.py` реализованы
  три реальных live-read инструмента поверх runtime/adapter слоя
  Step 5:
  - `get_configuration_info(environment)` — GET
    `<http_base_url>/configuration`;
  - `get_metadata_tree(environment, filter_value=None)` — GET
    `<http_base_url>/metadata`, при заданном `filter_value`
    добавляется `?filter=<urllib.parse.quote(filter_value)>`;
  - `get_metadata_object(environment, object_name)` — GET
    `<http_base_url>/metadata/object?name=<urllib.parse.quote(...)>`.
- Все три tool'а работают по одной схеме: вызывают
  `build_runtime_context(environment)`, кладут `health_codes` в
  `payload.runtime`, вызывают `fetch_json_from_environment(...)` и
  возвращают shared `ToolResult`. Любая `PlatformError` от live
  adapter заворачивается в `ToolResult(ok=False, ...)` — исключение
  наружу не уходит. Существующие `ping` и `health_summary` не
  менялись.
- В `apps/mcp-read-server/src/mcp_read_server/server.py` registry
  расширен до 5 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Общая архитектура
  `server.py` не менялась. `list_tools()` теперь возвращает
  отсортированно: `['get_configuration_info', 'get_metadata_object',
  'get_metadata_tree', 'health_summary', 'ping']`.
- README `mcp-read-server` дополнен: зафиксирована первая волна
  реальных live-read инструментов, общая схема «runtime context →
  fetch_json_from_environment → ToolResult», wiring с новым runtime
  подпакетом и `onec-config`.
- **Ручная проверка 4 сценариев** против реального стенда и
  контрольного локального HTTP-сервера (временный скрипт в
  `%TEMP%`, `PYTHONPATH` через bootstrap):
  - **A `get_configuration_info`**: против реального стенда —
    `ok=False`, `tool="get_configuration_info"`, message
    содержит `Failed to fetch http://localhost:8080/InfoBase5/hs/
    mcp-1c/configuration: <urlopen error [WinError 10061] ...>`,
    `payload.runtime.health_codes=['gateway_down']`. Apache
    по-прежнему не поднят; инструкция запрещает его трогать.
  - **B `get_metadata_tree`**: против реального стенда — `ok=False`,
    URL собран корректно: `/metadata` без query string.
  - **C `get_metadata_tree(filter_value="ОбщиеМодули")`**: против
    реального стенда — `ok=False`, URL
    `/metadata?filter=%D0%9E%D0%B1%D1%89%D0%B8%D0%B5%D0%9C%D0%BE%
    D0%B4%D1%83%D0%BB%D0%B8` (кириллица корректно URL-encoded через
    `urllib.parse.quote`).
  - **D `get_metadata_object("Справочник.Фильмы")`**: против
    реального стенда — `ok=False`, URL
    `/metadata/object?name=%D0%A1%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D1
    %87%D0%BD%D0%B8%D0%BA.%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B`.
    Точка между типом и именем сохраняется (это не reserved char).
  - Во всех четырёх случаях tool вернул `ToolResult`, наружу
    исключение не вышло — контракт соблюдён.
  - **Контрольный success-path** на локальном
    `socketserver.TCPServer` с маршрутизацией
    `/configuration` / `/metadata` / `/metadata/object`:
    - `A(local)` — `ok=True`, `data={'name':'DemoConfig',
      'version':'1.0'}`;
    - `B(local)` — `ok=True`, `data.tree` отдан, `filter_echo=None`;
    - `C(local)` — `ok=True`, сервер получил корректно
      URL-encoded фильтр (проверено substring'ом `%D0%9E`);
    - `D(local)` — `ok=True`, name пришло на сервер
      URL-encoded (substring `%D0%A1`), раздекодировано обратно
      корректно.
- **Dev-check после изменений зелёный**:
  `read_server_tools = ['get_configuration_info',
  'get_metadata_object', 'get_metadata_tree', 'health_summary',
  'ping']`, `selfcheck_status = ok`, `Dev check completed
  successfully.` Skeleton selfcheck не трогался — регрессии wiring
  нет.

### Phase 1 / Step 7 — первые dump-read инструменты (завершён)

- В `apps/mcp-read-server/src/mcp_read_server/tools.py` реализованы
  три реальных dump-read инструмента поверх `runtime/dump_adapter.py`
  (без regex, без внешних зависимостей, только стандартная
  библиотека):
  - `read_module_code_from_dump(environment, relative_path)` — читает
    текст одного файла через `read_dump_file(...)`, возвращает
    `ToolResult` с `payload.data = {"relative_path", "text"}`;
  - `search_code(environment, query)` — пробегает все `*.bsl` файлы
    (`find_files_by_pattern(resolve_dump_path(...), "*.bsl")`),
    делает `text.find(query)`, на каждом попадании собирает dict
    `{relative_path, matched=True, preview}`. Preview — фрагмент
    ±80 символов вокруг первого вхождения через общий helper
    `_snippet(...)`, защищённый от выхода за границы строки;
  - `search_metadata(environment, query)` — то же по `*.xml`, но
    совпадение засчитывается и по имени файла, и по содержимому.
    Для filename-only совпадений `preview` — пустая строка; для
    content-совпадений используется тот же `_snippet`.
  - Общая схема всех трёх tool'ов: `build_runtime_context(...)`,
    вызов dump-адаптера, оборачивание в shared `ToolResult`. Любая
    `PlatformError` от adapter-слоя → `ToolResult(ok=False, ...)` с
    `runtime.health_codes` в payload. Существующие ping/health_summary
    и live-tools не менялись.
- В `apps/mcp-read-server/src/mcp_read_server/server.py` registry
  расширен до 8 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Общая архитектура
  `server.py` не менялась. `list_tools()` теперь возвращает
  отсортированно:
  `['get_configuration_info', 'get_metadata_object',
  'get_metadata_tree', 'health_summary', 'ping',
  'read_module_code_from_dump', 'search_code', 'search_metadata']`.
- README `mcp-read-server` дополнен описанием первой волны
  dump-read инструментов, обновлён перечень registry (8 имён),
  и зафиксирована единая схема (live + dump) «runtime context →
  adapter → `ToolResult` с оборачиванием `PlatformError` в
  `ok=False`».
- **Ручная проверка 4 сценариев** против реального dump
  `C:\Tools\mcp-1c\config-dump\InfoBase5-with-code-20260423-004101`
  (временный скрипт в `%TEMP%`, `PYTHONPATH` через bootstrap):
  - **A `read_module_code_from_dump(env, "CommonModules\\MCPTestCode
    \\Ext\\Module.bsl")`**: `ok=True`,
    `payload.data.text_len = 215`, найдены оба ожидаемых маркера
    (`MCP_SMOKE_TEST` и кириллическое имя функции `ПолучитьСтатусMCP`
    — подтверждено substring-булевами `True`/`True`),
    `runtime.health_codes = ['gateway_down']` (Apache по-прежнему
    лежит, но dump-tool'у это не мешает).
  - **B `search_code(env, "MCP_SMOKE_TEST")`**: `ok=True`,
    `match_count = 1`, единственный match — именно
    `CommonModules\MCPTestCode\Ext\Module.bsl`, `matched=True`,
    `preview` включает BOM и начало модуля с комментарием
    `// MCP_SMOKE_TEST`. Сообщение: `Code search completed
    successfully.`
  - **C `search_metadata(env, "Фильмы")`**: `ok=True`,
    `match_count = 3`:
    `Catalogs\Фильмы.xml` (и по имени файла, и по содержимому),
    `ConfigDumpInfo.xml` и `Configuration.xml` (по содержимому —
    XML-каталоги конфигурации перечисляют имя объекта). В каждой
    строке `preview_len > 0` для content-совпадений. Сообщение:
    `Metadata search completed successfully.`
  - **D `search_code(env, "THIS_STRING_SHOULD_NOT_EXIST_12345")`**:
    `ok=True`, `match_count = 0`, `matches == []`. Сообщение:
    `Code search completed: no matches found.`
  - Во всех четырёх случаях tool вернул `ToolResult`, наружу
    исключение не вышло — dump adapter не ломает контракт.
- **Dev-check после изменений зелёный**:
  `read_server_tools = ['get_configuration_info',
  'get_metadata_object', 'get_metadata_tree', 'health_summary',
  'ping', 'read_module_code_from_dump', 'search_code',
  'search_metadata']`, `selfcheck_status = ok`,
  `Dev check completed successfully.` Skeleton selfcheck не трогался.

### Phase 1 / Step 8 — query path: validate_query и execute_read_query (завершён)

- В `apps/mcp-read-server/src/mcp_read_server/tools.py` реализованы
  два реальных live-tool'а query path поверх уже существующего
  runtime/adapter слоя:
  - `validate_query(environment, query)` — GET
    `<http_base_url>/query/validate?text=<urllib.parse.quote(query)>`,
    возвращает `ToolResult` с `payload.data` от live-адаптера;
  - `execute_read_query(environment, query, row_limit=100)` — GET
    `<http_base_url>/query/execute?text=<urlencoded>&limit=<row_limit>`.
    Перед live-вызовом — **временный read-only guardrail**: текст
    запроса приводится к верхнему регистру и, если встретится любое
    из `_WRITE_KEYWORDS` (`INSERT`, `UPDATE`, `DELETE`, `DROP`,
    `ALTER`, `CREATE`, `TRUNCATE`), сразу возвращается
    `ToolResult(ok=False, message="Only read-only queries are
    allowed.")` без обращения к live. Это stop-gap до появления
    полноценного policy-слоя (Phase 2+).
  - Оба tool'а используют `build_runtime_context(...)`, кладут
    `health_codes` в `payload.runtime`, ловят `PlatformError` от
    live adapter и оборачивают его в `ToolResult(ok=False, ...)` —
    наружу исключение не уходит.
- В `apps/mcp-read-server/src/mcp_read_server/server.py` registry
  расширен до 10 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Общая архитектура
  `server.py` не менялась. `list_tools()` теперь возвращает:
  `['execute_read_query', 'get_configuration_info',
  'get_metadata_object', 'get_metadata_tree', 'health_summary',
  'ping', 'read_module_code_from_dump', 'search_code',
  'search_metadata', 'validate_query']`.
- README `mcp-read-server` дополнен разделом про query path и
  явной пометкой о временном keyword-guardrail; перечень registry
  обновлён до 10 имён.
- **Ручная проверка 5 сценариев** через временный скрипт в `%TEMP%`
  (`PYTHONPATH` через bootstrap):
  - **A `validate_query(env, "ВЫБРАТЬ 1 КАК Число")` против
    реального стенда**: `ok=False` — transport error ожидаемо
    обёрнут в `ToolResult`; URL собран корректно с URL-encoded
    кириллицей (`%D0%92%D0%AB%D0%91%D0%A0%D0%90%D0%A2%D0%AC ...`);
    `runtime.health_codes=['gateway_down']`. Apache стенда по-прежнему
    не запущен — инструкция запрещает его трогать.
  - **B `execute_read_query(env, "ВЫБРАТЬ 1 КАК Число",
    row_limit=10)` против реального стенда**: guardrail пропустил
    read-query; live endpoint недоступен → `ok=False` с transport
    error; URL содержит `limit=10`.
  - **C `execute_read_query(env, "DELETE FROM Something",
    row_limit=10)`**: `ok=False`, `message="Only read-only queries
    are allowed."`, payload содержит только `runtime`
    (`data_key_present=False`) — **live adapter не вызывался**,
    guardrail сработал до transport.
  - **D Контрольный success-path на локальном in-process HTTP-сервере**
    (`socketserver.TCPServer`, маршруты `/query/validate` и
    `/query/execute`, валидный JSON):
    - `validate_query(..., "ВЫБРАТЬ 1 КАК Число")` → `ok=True`,
      `data={'valid': True, 'text_echo': 'ВЫБРАТЬ 1 КАК Число'}`;
      URL содержит корректно URL-encoded кириллицу (substring-проверка
      `%D0%92%D0%AB%D0%91%D0%A0%D0%90%D0%A2%D0%AC` → True).
    - `execute_read_query(..., "ВЫБРАТЬ 1 КАК Число", row_limit=10)`
      → `ok=True`, `data={'rows': [[1]], 'columns': ['Число'],
      'text_echo': 'ВЫБРАТЬ 1 КАК Число', 'limit_echo': '10'}`;
      URL содержит и URL-encoded query, и `limit=10`
      (substring-проверки обе True).
  - **E Registry check**: `len(REGISTERED_TOOLS) == 10`, `list_tools()`
    возвращает требуемый алфавитный список из 10 имён. ✓
  - Во всех случаях tool вернул `ToolResult`, исключение наружу
    не вышло.
- **Dev-check после изменений зелёный**:
  `read_server_tools = ['execute_read_query',
  'get_configuration_info', 'get_metadata_object',
  'get_metadata_tree', 'health_summary', 'ping',
  'read_module_code_from_dump', 'search_code', 'search_metadata',
  'validate_query']`, `selfcheck_status = ok`,
  `Dev check completed successfully.` Skeleton selfcheck не трогался.

### Phase 1 / Step 9 — get_event_log, get_object_structure, get_form_structure (завершён)

- В `apps/mcp-read-server/src/mcp_read_server/tools.py` реализованы
  три реальных live-read инструмента поверх уже существующего
  runtime/adapter слоя:
  - `get_event_log(environment, period_start=None, period_end=None,
    level=None, user=None)` — GET `<http_base_url>/event-log`.
    Переданные фильтры добавляются в query-string парами
    `start`/`end`/`level`/`user` с `urllib.parse.quote`; без
    фильтров URL остаётся без `?...`.
  - `get_object_structure(environment, object_name)` — GET
    `<http_base_url>/object/structure?name=<urllib.parse.quote(...)>`.
  - `get_form_structure(environment, object_name, form_name=None)`
    — GET `<http_base_url>/form/structure?object=<urlencoded>`,
    при переданном `form_name` добавляется `&form=<urlencoded>`.
- Все три tool'а работают по уже сложившейся единой схеме:
  `build_runtime_context(environment)`, `health_codes` в
  `payload.runtime`, вызов `fetch_json_from_environment(...)`,
  обёртка любой `PlatformError` в `ToolResult(ok=False, ...)` —
  наружу исключение не уходит.
- В `apps/mcp-read-server/src/mcp_read_server/server.py` registry
  расширен до 13 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Общая архитектура
  `server.py` не менялась. `list_tools()` теперь возвращает
  алфавитный список из 13 имён.
- README `mcp-read-server` дополнен секцией «event log и структура
  объектов/форм» и обновлённым перечнем registry (13 имён).
- **Ручная проверка 5 сценариев** через временный скрипт в `%TEMP%`
  (`PYTHONPATH` через bootstrap):
  - **A `get_event_log(env)`** против реального стенда: `ok=False`
    (Apache лежит), URL `/event-log` без query-string собран
    корректно, `runtime.health_codes=['gateway_down']`, исключение
    наружу не вышло.
  - **B `get_event_log(env, period_start="2026-01-01",
    period_end="2026-12-31", level="Error", user="user")`** против
    реального стенда: `ok=False`, URL содержит все четыре фильтра
    (`?start=2026-01-01&end=2026-12-31&level=Error&user=user`).
  - **C `get_object_structure(env, "Справочник.Фильмы")`** против
    реального стенда: `ok=False`, URL содержит URL-encoded
    `name=Справочник.Фильмы` (`%D0%A1%D0%BF%D1%80%D0%B0%D0%B2%
    D0%BE%D1%87%D0%BD%D0%B8%D0%BA.%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%
    D1%8B`).
  - **D `get_form_structure(env, "Справочник.Фильмы",
    "ФормаСписка")`** против реального стенда: `ok=False`, URL
    содержит и URL-encoded `object=Справочник.Фильмы`, и
    `form=ФормаСписка`.
  - **E Контрольный success-path** на локальном in-process HTTP
    сервере (`socketserver.TCPServer` + маршруты `/event-log`,
    `/object/structure`, `/form/structure`, валидный JSON):
    - `get_event_log(..., all four filters)` → `ok=True`;
      `data.filters_echo = {'start': '2026-01-01',
      'end': '2026-12-31', 'level': 'Error', 'user': 'admin'}`;
      substring-проверки в `last_path` —
      `has_start/has_end/has_level/has_user` все True;
    - `get_object_structure(..., "Справочник.Фильмы")` → `ok=True`;
      `data.name` round-trip'нулось правильно; substring
      `%D0%A1%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D1%87%D0%BD%D0%B8%D0%BA`
      → True;
    - `get_form_structure(..., "Справочник.Фильмы",
      "ФормаСписка")` → `ok=True`; в URL присутствуют и
      `object=`, и `form=`;
    - `get_form_structure(..., "Справочник.Фильмы")` без
      `form_name` → `ok=True`, параметр `&form=` **отсутствует**
      в URL (`has_form_param=False`) — опциональная ветка работает.
  - Ни в одном сценарии исключение наружу не вышло.
- **Dev-check после изменений зелёный**:
  `read_server_tools = ['execute_read_query',
  'get_configuration_info', 'get_event_log', 'get_form_structure',
  'get_metadata_object', 'get_metadata_tree',
  'get_object_structure', 'health_summary', 'ping',
  'read_module_code_from_dump', 'search_code', 'search_metadata',
  'validate_query']`, `selfcheck_status = ok`,
  `Dev check completed successfully.` Skeleton selfcheck не трогался.

### Phase 1 / Step 10 — diagnostics wrapping (завершён, Phase 1 Read MVP закрыт окончательно)

- В `apps/mcp-read-server/src/mcp_read_server/tools.py` реализованы
  два завершающих диагностических инструмента Phase 1 поверх уже
  готовых блоков (`build_runtime_context`, `check_environment_health`,
  `summarize_health`, `diagnose_from_health`) — без изменений в
  пакетах `onec-health` и `onec-troubleshooting`:
  - `check_runtime_health(environment)` — агрегированный снимок
    здоровья окружения. `ok=True` при `health_codes == ["ok"]`,
    иначе `ok=False`. payload содержит `runtime.health_codes`,
    slice окружения (`name`, `base_id`, `http_base_url`,
    `dump_path`) и полный список `checks` (`check_name`, `status`,
    `message`) из `context.health_results`.
  - `diagnose_connectivity_issue(environment)` — human-readable
    обёртка над `diagnose_from_health`. При `health_codes == ["ok"]`
    возвращается `ok=True` с `data.problem_code/probable_cause/
    recommended_action = None`. При проблемах —
    `ok=False`, `report.problem_code/probable_cause/
    recommended_action` из `onec-troubleshooting`.
  - Оба tool'а следуют общей схеме Phase 1: `build_runtime_context`,
    `health_codes` в `payload.runtime`, исключение наружу не уходит.
- В `apps/mcp-read-server/src/mcp_read_server/server.py` registry
  расширен до 15 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. `list_tools()` теперь
  возвращает:
  `['check_runtime_health', 'diagnose_connectivity_issue',
  'execute_read_query', 'get_configuration_info', 'get_event_log',
  'get_form_structure', 'get_metadata_object', 'get_metadata_tree',
  'get_object_structure', 'health_summary', 'ping',
  'read_module_code_from_dump', 'search_code', 'search_metadata',
  'validate_query']`.
- README `mcp-read-server` дополнен секцией «diagnostics wrapping
  (Phase 1 / Step 10)» и обновлённым перечнем registry (15 имён).
- **Ручная проверка 3 сценариев** через временный скрипт в `%TEMP%`
  (`PYTHONPATH` через bootstrap):
  - **A Реальный стенд** (Apache не запущен):
    - `check_runtime_health(stand_env)` → `ok=False`,
      `message="Runtime health issues detected."`,
      `health_codes=['gateway_down']`, `data.environment` содержит
      name/base_id/http_base_url/dump_path, `checks_count=3` с
      корректным раскладом
      `dump_path_exists=ok / http_gateway=error / search_index=ok`.
    - `diagnose_connectivity_issue(stand_env)` → `ok=False`,
      `message="Connectivity issue diagnosis completed."`,
      `problem_code='gateway_down'`,
      `probable_cause='HTTP gateway is not running or not reachable.'`,
      `recommended_action='Start the HTTP gateway and re-run health
      checks.'`
  - **B Локальный success-path** (in-process `socketserver.TCPServer`
    возвращает 200 на любой GET; реальный dump с `.bsl`):
    - `check_runtime_health(local_env)` → `ok=True`,
      `message="Runtime health check completed successfully."`,
      `health_codes=['ok']`, все три check'а `ok`.
    - `diagnose_connectivity_issue(local_env)` → `ok=True`,
      `message="No connectivity issues detected."`,
      `problem_code=None, probable_cause=None,
      recommended_action=None`.
  - **C Registry check**: `len(REGISTERED_TOOLS) == 15`,
    `list_tools()` — требуемый алфавитный список.
  - Ни в одном сценарии исключение наружу не вышло.
- **Dev-check зелёный** после изменений:
  `read_server_tools` содержит все 15 имён; `selfcheck_status = ok`;
  `Dev check completed successfully.` Skeleton selfcheck не трогался.
- **Phase 1 Read MVP закрыт.** Все 10 шагов фазы выполнены,
  критерии приёмки `phase-1-read-mvp-plan.md` достигнуты на
  уровне контракта и success-path. End-to-end против реального
  Apache стенда не покрыт только потому, что стенд сейчас
  выключен — это эксплуатационный вопрос, а не пробел платформы.

### Phase 2 / Step 1 — планирование Write MVP (завершён)

- Phase 1 Read MVP закрыт; Phase 2 — активная фаза разработки.
- Добавлен `docs/architecture/phase-2-write-mvp-plan.md` —
  план Write MVP: назначение фазы, целевой результат, первый
  набор инструментов по четырём группам (A safety/preflight,
  B controlled write, C verification, D audit/rollback support),
  базовые guardrails фазы (запрет prod по умолчанию, обязательный
  `allow_write=True`, обязательные backup/dump до операции,
  обязательный audit, обязательный verify после, запрет silent
  apply), порядок реализации, что не входит в MVP, критерии
  приёмки.
- Добавлен `docs/architecture/phase-2-step-map.md` — стартовый
  implementation map на первые 7 шагов Phase 2: реальный
  `onec-policy-engine` preflight, append-only JSONL audit store в
  `onec-audit`, runtime-слой `mcp-write-server`,
  safety/preflight tools группы A, единый
  `write_flow` helper (preflight → snapshot → operation → verify
  → audit), первые write-tools группы B
  (`apply_config_from_files`, `update_module_code`,
  `create_common_module`), первые verification-tools группы C.
- Зафиксирован первый набор write-tools Phase 2:
  safety — `check_write_preconditions`, `create_backup_snapshot`,
  `create_dump_snapshot`;
  controlled write — `apply_config_from_files`,
  `update_database_configuration`, `create_common_module`,
  `update_module_code`, `add_catalog_attribute`;
  verification — `verify_metadata_change`, `verify_module_contains`,
  `verify_object_exists`;
  audit/rollback — `write_audit_record`,
  `describe_last_write_operation`, `prepare_rollback_hint`.
- Обновлён корневой `README.md`: блок «Текущий статус по фазам»
  переписан под закрытую Phase 1 и активную Phase 2, добавлены
  ссылки на `phase-2-write-mvp-plan.md` и `phase-2-step-map.md`.

### Phase 2 / Step 2 — реальный write preflight / policy слой в onec-policy-engine (завершён)

- `onec-policy-engine` расширен от skeleton до минимального, но
  уже рабочего policy / preflight слоя. Модели:
  - `PolicyDecision` получила два новых поля: `reason_code: str`
    и `require_snapshots: bool` (плюс существующие `allowed`,
    `reason`). Все четыре — обязательные.
  - Добавлена новая dataclass `WriteIntent(operation_name: str,
    target: str | None = None)`.
- Engine:
  - Зафиксированы два множества операций:
    - mutating (`apply_config_from_files`,
      `update_database_configuration`, `create_common_module`,
      `update_module_code`, `add_catalog_attribute`) — требуют
      snapshot'ов;
    - non-mutating write-side support (`check_write_preconditions`,
      `create_backup_snapshot`, `create_dump_snapshot`,
      `verify_metadata_change`, `verify_module_contains`,
      `verify_object_exists`, `write_audit_record`,
      `describe_last_write_operation`, `prepare_rollback_hint`) —
      без snapshot'ов.
  - Консервативная production-эвристика: окружение считается
    production-like, если в нижнем регистре любое из полей
    `name` / `base_id` / `publication_name` / `http_base_url`
    содержит `prod` или `production`. Это временный guardrail до
    появления в `EnvironmentConfig` отдельного
    `environment_type`.
  - Новый основной режим
    `check_write_allowed(environment: EnvironmentConfig,
    intent: WriteIntent) -> PolicyDecision` даёт пять возможных
    `reason_code`: `production_blocked`, `write_not_allowed`,
    `allowed_mutating`, `allowed_non_mutating`, `unknown_intent`.
- **Backward compatibility сохранена.** Существующий
  `scripts/dev/selfcheck.py` (который трогать нельзя на этом шаге)
  продолжает вызывать legacy-форму
  `check_write_allowed("production", True)` и
  `check_write_allowed("local-dev", False)`. В `engine.py`
  реализован тип-диспатч: при `(str, bool)` уходим в
  `_legacy_check`, который возвращает
  `production_blocked` / `write_not_allowed` / `allowed_legacy`
  (legacy-ветка ставит `require_snapshots=True` как безопасный
  default).
- `__init__.py` экспортирует `PolicyDecision`, `WriteIntent`,
  `check_write_allowed` через явный `__all__`.
- README пакета переписан: описано текущее поведение, модели,
  правила, перечень `reason_code`, две формы вызова и отметка о
  временной legacy-совместимости.
- **Ручная проверка 5 сценариев** через временный скрипт в
  `%TEMP%`:
  - **A Legacy `("production", True)`**: `allowed=False`,
    `reason_code='production_blocked'`, `require_snapshots=False`.
  - **B Legacy `("local-dev", False)`**: `allowed=False`,
    `reason_code='write_not_allowed'`, `require_snapshots=False`.
  - **C New mode, local-dev+`allow_write=True`+mutating intent
    (`update_module_code`)**: `allowed=True`,
    `reason_code='allowed_mutating'`, `require_snapshots=True`.
  - **D New mode, non-mutating support
    (`describe_last_write_operation`)**: `allowed=True`,
    `reason_code='allowed_non_mutating'`, `require_snapshots=False`.
  - **E New mode, unknown intent (`totally_unknown_operation`)**:
    `allowed=False`, `reason_code='unknown_intent'`, `reason`
    содержит имя операции.
  - Assertion `isinstance(r, PolicyDecision)` на всех пяти
    результатах — OK.
- **Dev-check после изменений зелёный**:
  `production_write_allowed = false`, `local_dev_write_allowed =
  false` (совпадает с требуемыми значениями selfcheck'а благодаря
  legacy-диспатчу), `selfcheck_status = ok`, `Dev check completed
  successfully.` Skeleton selfcheck не трогался; чужие пакеты
  (`onec-config`, `onec-audit`, `onec-health` и др.) тоже не
  трогались.

### Phase 2 / Step 3 — append-only JSONL audit store в onec-audit (завершён)

- `onec-audit` расширен от форматтера до минимального append-only
  JSONL store. Публичный контракт `AuditRecord` не менялся;
  `format_audit_record(...)` оставлен как канонический форматтер
  (одна запись → одна JSON-строка через `json.dumps`,
  `ensure_ascii=False`).
- В `writer.py` добавлены две функции:
  - `append_record(audit_dir, record) -> str` — создаёт
    `audit_dir` (если нет) через `mkdir(parents=True,
    exist_ok=True)`, открывает `<audit_dir>/audit.jsonl` в режиме
    append/UTF-8, пишет `format_audit_record(record) + "\n"` и
    возвращает строковый путь файла аудита. Ошибки файловой
    системы поднимаются как `OSError` и не проглатываются.
    Append-only, файл никогда не перезаписывается.
  - `read_last_record(audit_dir) -> AuditRecord | None` — читает
    `<audit_dir>/audit.jsonl` в UTF-8, игнорирует пустые строки,
    берёт последнюю непустую, парсит JSON, возвращает
    `AuditRecord(**payload)`. Если файла нет или в нём нет
    непустых строк — `None`. На битой JSON-строке или
    рассогласовании с формой `AuditRecord` — `ValueError` с
    понятным сообщением; `OSError` пробрасывается как есть.
- Имя файла хранилища зафиксировано константой
  `_AUDIT_FILE_NAME = "audit.jsonl"`. Формат — JSONL (одна запись
  = одна строка), UTF-8, переводы `\n`.
- `__init__.py` экспортирует `AuditRecord`, `format_audit_record`,
  `append_record`, `read_last_record` через явный `__all__`.
- README пакета переписан: выход из чистого форматтера,
  описание append-only store, контракт ошибок, явная отметка что
  rotate/search/history не входят в MVP.
- **Ручная проверка 4 сценариев** через временный скрипт в
  `%TEMP%`, с использованием `tempfile.TemporaryDirectory(...)`
  для каждого случая:
  - **A `format_audit_record`**: вернулась однострочная JSON-строка
    c ожидаемыми ключами (`operation_id`, `tool_name`, `status`
    — все `True`), `ensure_ascii=False` сохранил читаемый
    `Local Dev`.
  - **B `append_record` в пустой каталог**: возвращён путь вида
    `<tempdir>\audit.jsonl`, файл создан, в нём ровно **1**
    непустая строка, идентичная canonical JSON.
  - **C append двух записей + `read_last_record`**: записаны
    `op-001 "first"` и `op-002 "second"`; `read_last_record`
    вернул `AuditRecord(operation_id='op-002',
    tool_name='update_module_code', status='error',
    message='second')`; `isinstance(AuditRecord)=True`;
    substring-проверка содержимого подтвердила — это именно
    вторая запись, не первая.
  - **D `read_last_record` на каталоге без `audit.jsonl`**:
    вернулся `None` (`is_none=True`).
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `selfcheck_status = ok`, `Dev check completed successfully.`
  Skeleton selfcheck не трогался; чужие пакеты
  (`onec-policy-engine`, `onec-config`, `onec-health` и др.) тоже
  не трогались.

### Phase 2 / Step 4 — runtime-слой mcp-write-server (завершён)

- Внутри `apps/mcp-write-server/src/mcp_write_server/` создан
  подпакет `runtime/` — внутренний слой ниже tool-уровня. Пока он
  не используется ни одним зарегистрированным инструментом
  write-server'а: `tools.py`, `server.py`, верхний `__init__.py`
  и `models.py` не тронуты; registry остаётся `['ping']`.
- **`runtime/models.py`** — dataclass `WriteRuntimeContext` со
  всеми перечисленными в ТЗ полями: `environment`,
  `intent: WriteIntent`, `health_results`, `health_codes`,
  `policy_decision`, `audit_dir: str`. Импорты согласованы с
  `onec_config`, `onec_health`, `onec_policy_engine`.
- **`runtime/context.py`** —
  `build_runtime_context(environment, intent)`:
  `check_environment_health(...)` → `summarize_health(...)` →
  `check_write_allowed(environment, intent)` (новый режим из
  Step 2, с `WriteIntent`) → `audit_dir` как
  `str(Path(environment.dump_path) / ".audit")` (временное
  правило до появления отдельного поля в `onec-config`).
  Без side-effects, ничего на диск не пишется.
- **`runtime/guards.py`** —
  `require_write_preconditions(context)`:
  fail-fast guard, сначала проверяет
  `context.policy_decision.allowed` (при deny →
  `PolicyDeniedError` из `mcp-common` с текстом
  `policy_decision.reason`), затем `context.health_codes !=
  ["ok"]` (→ `HealthCheckError` с сообщением
  `"Write preconditions failed due to unhealthy runtime: <codes>"`).
  Ничего не возвращает.
- **`runtime/__init__.py`** экспортирует `WriteRuntimeContext`,
  `build_runtime_context`, `require_write_preconditions` через
  явный `__all__`.
- README `mcp-write-server` дополнен разделом «Runtime слой
  (Phase 2 / Step 4)» с кратким описанием трёх символов,
  выводимого правила `audit_dir` и порядка проверок в guard'е.
- **Ручная проверка 4 сценариев** через временный скрипт в
  `%TEMP%` под bootstrap'нутым `PYTHONPATH`:
  - **A Allowed policy + unhealthy runtime** (URL указывает на
    пустой localhost:59999, dump реальный, `allow_write=True`,
    mutating intent): `WriteRuntimeContext` создан,
    `policy.allowed=True`, `reason_code='allowed_mutating'`,
    `health_codes=['gateway_down']`, `audit_dir` заканчивается на
    `\.audit` и равен
    `C:\Tools\mcp-1c\config-dump\InfoBase5-with-code-20260423-004101\.audit`.
    `require_write_preconditions` корректно поднял
    `HealthCheckError: Write preconditions failed due to unhealthy
    runtime: ['gateway_down']`.
  - **B Denied by policy** (тот же URL, но `allow_write=False`):
    `policy.allowed=False`, `reason_code='write_not_allowed'`,
    `require_write_preconditions` поднял `PolicyDeniedError:
    Write operations require allow_write=True.` — policy-guard
    отработал **до** health-проверки (как и требует порядок).
  - **C Production-like deny** (name=`Prod Local`,
    publication/base_id/URL содержат `prod`): `policy.allowed=
    False`, `reason_code='production_blocked'`,
    `PolicyDeniedError: Write operations are forbidden for
    production-like environments by default.`
  - **D Fully healthy local success-path** (in-process
    `socketserver.TCPServer` на случайном `127.0.0.1:<port>`,
    возвращает 200 на любой GET; реальный dump с `.bsl`):
    `health_codes=['ok']`, `policy.allowed=True`,
    `reason_code='allowed_mutating'`, `require_snapshots=True`,
    `require_write_preconditions` вернул `None` без исключения.
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `write_server_tools = ['ping']` (runtime не подключён к
  registry, как и требовалось), `selfcheck_status = ok`,
  `Dev check completed successfully.` Skeleton selfcheck не
  трогался; read-server, packages и прочее — тоже.

### Phase 2 / Step 5 — safety/preflight tools группы A (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py`
  реализованы три первых реальных write-side инструмента поверх
  готового runtime-слоя (`build_runtime_context`,
  `require_write_preconditions`), `onec-policy-engine`
  (`WriteIntent` + new-mode `check_write_allowed`) и
  `onec-process-runner` (`run_process`):
  - `check_write_preconditions(environment, intent)` — тонкая
    tool-обёртка над runtime guard; при успехе — `ok=True`,
    `"Write preconditions satisfied."`; при
    `PolicyDeniedError` / `HealthCheckError` — `ok=False` c
    оригинальным текстом. `payload.runtime` несёт
    `health_codes` и `policy.{allowed, reason_code,
    require_snapshots}`; `payload.data.audit_dir` — из
    `WriteRuntimeContext`.
  - `create_backup_snapshot(environment, label)` — **реальный**
    файловый snapshot инфобазы через
    `shutil.copytree(environment.base_path,
    <base_path.parent>/_snapshots/backup-<base_id>-<safe_label>)`.
    `safe_label` получается санитизацией до набора
    ASCII-букв / цифр / `-_`; пустой результат → `"snapshot"`.
    Перед копированием проходит preflight. Если целевой
    snapshot уже существует — `ok=False` без перезаписи. Ошибки
    `OSError` / `shutil.Error` ловятся и заворачиваются в
    `ToolResult(ok=False, ...)`.
  - `create_dump_snapshot(environment, label)` — **временный
    process-backed stub**. Создаёт каталог
    `<dump_path.parent>/_snapshots/dump-<base_id>-<safe_label>`,
    находит `shutil.which("python")`, через `run_process(...)`
    запускает маленький Python-процесс, который пишет
    `dump-created.txt` в каталоге snapshot; после success'а
    tool сам дописывает `dump-meta.json` с `base_id` / `label` /
    `source_dump_path`. Это не настоящий `1cv8 DumpCfg`: цель
    шага — впервые связать preflight + process runner + snapshot
    path; реальный dump придёт позднее, после `write_flow` и
    проброса пути к бинарю через `onec-config`. Честно
    зафиксировано в README сервера.
  - Добавлены два приватных helper'а: `_safe_snapshot_label(label)`
    и `_runtime_payload(context)`.
- В `apps/mcp-write-server/src/mcp_write_server/server.py`
  registry расширен до 4 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`.
  Алфавитный `list_tools()`:
  `['check_write_preconditions', 'create_backup_snapshot',
  'create_dump_snapshot', 'ping']`.
- README `mcp-write-server` дополнен новым разделом «Safety /
  preflight tools (Phase 2 / Step 5)» с явной пометкой, что
  backup реальный (copytree), а dump snapshot пока временный
  process-backed stub; существующий раздел Runtime слоя сохранён.
- **Ручная проверка 5 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` и in-process
  `socketserver.TCPServer` (200 на любой GET). Фейковый
  `base_path` с одним файлом `hello.txt`, фейковый `dump_path`
  с одним `.bsl` — всё во временном каталоге, реальный стенд
  не затрагивался:
  - **A `check_write_preconditions` success**: `ok=True`,
    `reason_code='allowed_mutating'`, `require_snapshots=True`,
    `health_codes=['ok']`, message `"Write preconditions
    satisfied."`
  - **B `check_write_preconditions` denied** (`allow_write=False`):
    `ok=False`, `reason_code='write_not_allowed'`, message из
    policy reason.
  - **C `create_backup_snapshot` success**: `ok=True`,
    `snapshot_path` создан по правилу
    `<base.parent>/_snapshots/backup-<base_id>-<safe_label>`;
    `hello.txt` скопирован внутрь; label `"step5 test"`
    санитизирован в `step5_test`.
  - **D `create_dump_snapshot` success**: `ok=True`,
    `snapshot_path` создан; `dump-created.txt` записан через
    `run_process` (содержимое `"ok"`); `dump-meta.json` содержит
    `base_id="local-dev"`, `label="step5 test"`,
    `source_dump_path=<fake dump path>`.
  - **E Registry check**: `list_tools() == ['check_write_preconditions',
    'create_backup_snapshot', 'create_dump_snapshot', 'ping']`,
    `len(REGISTERED_TOOLS) == 4`.
  - Во всех случаях tool вернул `ToolResult`, исключения наружу
    не выпадали.
- **Dev-check после изменений зелёный**:
  `write_server_tools = ['check_write_preconditions',
  'create_backup_snapshot', 'create_dump_snapshot', 'ping']`,
  `selfcheck_status = ok`, `Dev check completed successfully.`
  Skeleton selfcheck не трогался; чужие пакеты и read-server —
  тоже.

### Phase 2 / Step 6 — единый write_flow helper (завершён)

- Внутри `apps/mcp-write-server/src/mcp_write_server/runtime/`
  создан новый файл `flow.py` — внутренняя «труба»
  preflight → snapshot → operation → verify → audit для будущих
  write-tools группы B. На этом шаге новых public tool'ов нет:
  registry write-server остаётся прежним
  (`check_write_preconditions`, `create_backup_snapshot`,
  `create_dump_snapshot`, `ping`).
- Добавлен dataclass **`WriteFlowArtifacts`** (поля
  `backup_snapshot_path`, `dump_snapshot_path`, `audit_path`,
  `operation_payload`, `verify_payload` — все `... | None`) как
  контракт артефактов одного прогона flow.
- Добавлены type alias'ы `OperationCallable = Callable[[WriteRuntimeContext],
  dict]` и `VerifyCallable = Callable[[WriteRuntimeContext, dict],
  dict]`.
- Основная функция
  **`run_write_flow(environment, intent, *, label,
  operation_callable, verify_callable) -> ToolResult`** выполняет
  строго один путь:
  1. `build_runtime_context(environment, intent)`;
  2. preflight через `require_write_preconditions(...)`;
  3. snapshots — если `context.policy_decision.require_snapshots`,
     вызывает существующие из Step 5 `create_backup_snapshot(...)`
     и затем `create_dump_snapshot(...)`;
  4. `operation_callable(context)`;
  5. `verify_callable(context, operation_payload)`;
  6. `append_record(...)` в `context.audit_dir` с свежим
     `operation_id = str(uuid.uuid4())` и `tool_name="run_write_flow"`;
  7. итоговый `ToolResult(ok=True, ...)` с `stage="completed"` и
     всеми артефактами.
- **Исключения наружу не выпускаются.** Для `operation_callable` и
  `verify_callable` ловится `Exception` (tool boundary); на любой
  стадии при ошибке возвращается `ToolResult(ok=False, ...)` с
  `payload.data.stage ∈ {preflight, backup_snapshot, dump_snapshot,
  operation, verify}` и уже собранными артефактами (snapshot refs,
  `operation_id`, `audit_path`). При ошибке audit помечается
  `status="error"`; если сама запись в audit упала `OSError`,
  `audit_path=None` и tool всё равно возвращает `ToolResult` без
  исключений.
- Lazy import `from ..tools import create_backup_snapshot,
  create_dump_snapshot` внутри `run_write_flow` специально
  разрывает циклический импорт между `tools.py` (импортирует
  `.runtime`) и `.runtime.flow` (использует snapshot tools).
- `runtime/__init__.py` расширен: теперь экспортирует
  `WriteRuntimeContext`, `build_runtime_context`,
  `require_write_preconditions`, `WriteFlowArtifacts`,
  `run_write_flow` через явный `__all__`.
- README `mcp-write-server` дополнен разделом «Write-flow
  pipeline (Phase 2 / Step 6)» с явной пометкой, что это **не
  public tool**, registry не меняется, а dump snapshot внутри
  flow по-прежнему идёт через временный process-backed stub из
  Step 5 до появления реального `1cv8 DumpCfg`.
- **Ручная проверка 4 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` + in-process
  `socketserver.TCPServer` (200 на любой GET). Для каждого
  сценария — собственный tempdir с фейковыми `base_path` и
  `dump_path` (`.bsl` внутри). Реальный стенд не затрагивался:
  - **A Успешный flow (mutating intent)**: `ok=True`,
    `stage='completed'`, `operation_id` присутствует,
    `backup_snapshot_path` и `dump_snapshot_path` заполнены, в
    audit_dir реально лежит `audit.jsonl`, `read_last_record`
    вернул `status='ok'` и тот же `operation_id`;
    `operation_payload={'changed': True, 'target': 'Common...'}`,
    `verify_payload={'verified': True, 'target': 'Common...'}`.
  - **B Preflight deny** (`allow_write=False`): `ok=False`,
    `stage='preflight'`, `reason_code='write_not_allowed'`,
    callback'и вообще не вызывались.
  - **C `operation_callable` падает `RuntimeError("boom")`**:
    `ok=False`, `message='Write operation failed: boom'`,
    `stage='operation'`, есть `operation_id` и `audit_path`;
    последняя запись аудита — `status='error'`,
    `message='Write operation failed: boom'`, `operation_id`
    совпадает.
  - **D `verify_callable` падает `RuntimeError("verify failed")`**:
    `ok=False`, `message='Write verify failed: verify failed'`,
    `stage='verify'`, `operation_payload` присутствует в data
    (успешный первый callback), есть `operation_id` и
    `audit_path`; последняя запись аудита — `status='error'`,
    `message='Write verify failed: verify failed'`,
    `operation_id` совпадает.
  - Во всех четырёх сценариях исключение наружу не вышло.
- **Dev-check после изменений зелёный**:
  `write_server_tools = ['check_write_preconditions',
  'create_backup_snapshot', 'create_dump_snapshot', 'ping']`
  (registry не меняли, как и требовалось), `selfcheck_status = ok`,
  `Dev check completed successfully.` Skeleton selfcheck не
  трогался; read-server и пакеты — тоже.

### Phase 2 / Step 7 — первые write-tools группы B (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py`
  реализованы три первых **public write-tool'а группы B**. Каждый
  — тонкая обёртка над `run_write_flow(...)` из Step 6: собственный
  `WriteIntent`, собственный `label`, собственный
  `operation_callable`, собственный `verify_callable`. Общая труба
  `preflight → snapshot → operation → verify → audit` не
  дублируется, после flow `tool_name` в `ToolResult` заменяется на
  имя public-инструмента через небольшой helper
  `_with_tool_name(...)`.
- Добавлен внутренний helper-файл
  `apps/mcp-write-server/src/mcp_write_server/runtime/dump_ops.py`
  с единственной функцией `run_stub_apply_process(source_dump_path)`:
  проверяет каталог, находит `python` в PATH, через
  `onec-process-runner` пишет маркер `apply-stub.txt`, дописывает
  `apply-meta.json`, возвращает dict с `applied`, `mode`,
  `source_dump_path`, `marker_path`. Ошибки валидации/процесса
  поднимаются как `FileNotFoundError` / `RuntimeError` и ловятся
  уже в `run_write_flow` как operation-stage failure — исключения
  наружу не выходят.
- **`apply_config_from_files(environment, source_dump_path,
  label="apply-config")`** — первый реальный public-инструмент
  apply. На этом шаге apply-путь **честный stub-backed process
  apply**, а не настоящий `1cv8 LoadConfigFromFiles`: operation
  идёт через `run_stub_apply_process(...)`, verify проверяет, что
  маркер создан (`marker_exists=True`). Честно зафиксировано в
  README и в docstring.
- **`update_module_code(environment, module_relative_path, new_text,
  label="update-module-code")`** — **реальное** перезаписывание
  файла модуля в `environment.dump_path`. Операция:
  `target = Path(dump_path) / module_relative_path`, проверка
  `target.is_file()`, `target.write_text(new_text, encoding="utf-8")`.
  Verify перечитывает файл и сверяет побайтно с `new_text`. Пустой
  или whitespace-only `new_text` отвергается **до запуска flow**,
  tool возвращает `ToolResult(ok=False, ...)` без snapshots/audit.
- **`create_common_module(environment, module_name,
  initial_text="", label="create-common-module")`** — **реальное**
  создание `CommonModules/<module_name>/Ext/Module.bsl` в dump-
  дереве. Валидация имени — `re.fullmatch(r"\w+", module_name)`
  (латиница/кириллица/цифры/underscore; не пустой; без пробелов);
  при невалидном — `ToolResult(ok=False, ...)` до flow. Если файл
  уже существует — operation raises, flow возвращает
  `ok=False, stage="operation"`. При пустом `initial_text`
  пишется минимальный шаблон `// <module_name>\n`. Verify
  проверяет существование и побайтное совпадение.
- В `apps/mcp-write-server/src/mcp_write_server/server.py` registry
  расширен до 7 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Алфавитный
  `list_tools()`: `['apply_config_from_files',
  'check_write_preconditions', 'create_backup_snapshot',
  'create_common_module', 'create_dump_snapshot', 'ping',
  'update_module_code']`.
- README `mcp-write-server` дополнен разделом «Controlled
  write-tools, группа B (Phase 2 / Step 7)» с явной пометкой, что
  `update_module_code` и `create_common_module` реально меняют
  dump/source tree, а `apply_config_from_files` — честный
  stub-backed process apply до появления пути к реальному `1cv8
  LoadConfigFromFiles`. Указано, что public verification-tools
  группы C — в Step 8.
- **Ручная проверка 5 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` и in-process
  `socketserver.TCPServer`. Реальный стенд не затрагивался; для
  каждого сценария — собственный tempdir с фейковыми `base_path`
  (с файлом `hello.txt`) и `dump_path` (с `.bsl`-anchor'ом):
  - **A `update_module_code` success**: `ok=True`,
    `tool='update_module_code'`, `stage='completed'`, verify
    вернул `{verified: True, target, text_length: 66}`; файл на
    диске **реально содержит** `new_text` (побайтное сравнение
    True); `audit_path` существует.
  - **B `create_common_module("MCPTestCode2")` success**:
    `ok=True`, `tool='create_common_module'`, `stage='completed'`,
    операция вернула путь
    `CommonModules/MCPTestCode2/Ext/Module.bsl`, verify — тот же
    путь; файл создан в dump-дереве, содержимое — минимальный
    шаблон `// MCPTestCode2\n`.
  - **C `apply_config_from_files` success**: `ok=True`,
    `tool='apply_config_from_files'`, `stage='completed'`,
    `operation_payload.mode='stub-process-apply'`; маркер
    `apply-stub.txt` реально создан (содержимое `'applied'`);
    `apply-meta.json` тоже присутствует; verify получил
    `marker_exists=True`.
  - **D `update_module_code` invalid input (`new_text="   "`)**:
    `ok=False`, `message="new_text must be a non-empty,
    non-whitespace string."`, `payload.keys()=['data']` — в
    payload нет ни `runtime`, ни snapshot refs. Отказ сработал
    **до** `run_write_flow`, как и требовалось ТЗ.
  - **E Registry check**: `list_tools()` вернул 7 имён в
    алфавитном порядке, `len(REGISTERED_TOOLS)==7`.
  - Во всех случаях tool вернул `ToolResult`, исключение наружу
    не выпало.
- **Dev-check после изменений зелёный**:
  `write_server_tools = ['apply_config_from_files',
  'check_write_preconditions', 'create_backup_snapshot',
  'create_common_module', 'create_dump_snapshot', 'ping',
  'update_module_code']`, `selfcheck_status = ok`, `Dev check
  completed successfully.` Skeleton selfcheck не трогался;
  read-server (15 tools) и пакеты — тоже.

### Phase 2 / Step 8 — первые verification-tools группы C (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py`
  реализованы три public verification-tool'а. Они — **не**
  обёртки над `run_write_flow`: ничего не меняют, не снимают
  snapshot'ов, не пишут audit. Cross-app import разрешён только
  `write → read`: из `mcp_read_server.runtime` используются
  `fetch_json_from_environment`, `read_dump_file`,
  `resolve_dump_path`, `find_files_by_pattern`, `read_text_file`.
  Read-server не менялся; его контракт read-only сохранён.
- **`verify_module_contains(environment, module_relative_path,
  expected_substring)`** — dump-level verify. Через
  `read_dump_file(...)` читает файл модуля и проверяет наличие
  substring'а. Пустой/whitespace-only `expected_substring`
  отвергается до чтения. `PlatformError` от dump adapter
  заворачивается в `ToolResult(ok=False, ...)`. В payload —
  `module_relative_path`, `expected_substring`, `contains`.
- **`verify_object_exists(environment, object_name)`** —
  cross-check live + dump. Live-часть: GET на
  `<http_base_url>/metadata/object?name=<url-encoded object_name>`
  через `fetch_json_from_environment(...)`; `PlatformError`
  превращается в `live_exists=False` + `live_error=<текст>`.
  Dump-часть: `find_files_by_pattern(resolve_dump_path(env),
  "*.xml")` → substring-поиск `object_name` в текстах XML
  (`read_text_file`). `dump_exists = dump_match_count > 0`.
  `ok=True` только когда `live_exists AND dump_exists`. В payload —
  `object_name`, `live_exists`, `dump_exists`, `dump_match_count`,
  опционально `live_error` / `dump_error`.
- **`verify_metadata_change(environment, expectation)`** — фасад
  над минимальным expectation contract. Диспетчер по
  `expectation["kind"]`:
  - `"object_exists"` → делегирует в `verify_object_exists(env,
    expectation["object_name"])`;
  - `"module_contains"` → делегирует в `verify_module_contains(env,
    expectation["module_relative_path"],
    expectation["expected_substring"])`;
  - любой другой `kind` → `ok=False`, `"Unknown metadata
    verification kind: ..."`.
  Итоговый `ToolResult` переписывается так, что `tool_name` всегда
  `"verify_metadata_change"`, а в `payload.data` добавляется
  `verification_kind` (имя выбранной ветки). Отсутствие
  обязательных полей expectation тоже даёт понятный
  `ToolResult(ok=False, ...)` без исключения.
- В `apps/mcp-write-server/src/mcp_write_server/server.py`
  registry расширен до 10 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Алфавитный
  `list_tools()`: `['apply_config_from_files',
  'check_write_preconditions', 'create_backup_snapshot',
  'create_common_module', 'create_dump_snapshot', 'ping',
  'update_module_code', 'verify_metadata_change',
  'verify_module_contains', 'verify_object_exists']`.
- README `mcp-write-server` дополнен разделом «Verification-tools,
  группа C (Phase 2 / Step 8)» с явной отметкой, что cross-app
  import идёт только write→read, перечисленными импортами из
  `mcp_read_server.runtime`, описанием двух форм verification
  (встроенные callback'и в `run_write_flow` из Step 7 + public
  tools из Step 8).
- **Ручная проверка 5 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` и in-process
  `socketserver.TCPServer`, который маршрутизирует
  `/metadata/object` в валидный JSON. Реальный стенд не
  затрагивался:
  - **A `verify_module_contains` success**: файл содержит
    `MCP_SMOKE_TEST`; `ok=True`, `contains=True`, сообщение
    «Module verification succeeded.»
  - **B `verify_module_contains` failure**: ищется substring,
    которого в файле нет; `ok=False`, `contains=False`, сообщение
    «Expected substring was not found in module.»
  - **C `verify_object_exists` success**: локальный HTTP отдаёт
    JSON, в dump положен XML с `Справочник.Фильмы`;
    `ok=True`, `live_exists=True`, `dump_exists=True`,
    `dump_match_count=1`.
  - **D `verify_object_exists` partial failure**: URL указывает
    на `127.0.0.1:59999/dead` (порт не слушается), dump XML
    содержит объект; `ok=False`, `live_exists=False`,
    `dump_exists=True`, `dump_match_count=1`, в payload есть
    `live_error` с «Failed to fetch …/metadata/object?name=%D0%A1%D0%BF%D1%80…».
  - **E dispatcher**:
    - E1 `kind='object_exists'`: `tool_name='verify_metadata_change'`,
      `verification_kind='object_exists'`, `ok=True`,
      `object_name='Справочник.Фильмы'` пронесено.
    - E2 `kind='module_contains'`: `tool_name='verify_metadata_change'`,
      `verification_kind='module_contains'`, `ok=True`,
      `contains=True`.
  - Во всех случаях исключение наружу не выходит.
- **Dev-check после изменений зелёный**:
  `write_server_tools` содержит 10 имён,
  `read_server_tools` = 15 (не деградировал), `selfcheck_status
  = ok`, `Dev check completed successfully.`

### Phase 2 / Step 9 — оставшиеся B-tools и audit/rollback helpers (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py`
  реализованы **5 новых public tools**. Registry расширен до 15.
- **Группа B (через `run_write_flow`):**
  - `update_database_configuration(environment,
    label="update-database-configuration")` — запуск «обновления
    БД» через полную трубу flow. **Честный stub-backed update-db
    process** до настоящего `1cv8 UpdateDBCfg`: operation через
    `onec-process-runner` пишет маркер
    `<dump_path>/.update-db-stub.txt`, tool дополняет
    `<dump_path>/.update-db-meta.json`. Verify проверяет наличие
    обоих файлов.
  - `add_catalog_attribute(environment, catalog_name,
    attribute_spec, label="add-catalog-attribute")` — **реальный**
    pragmatic text-patch XML-карточки справочника в dump-дереве.
    Pre-flow валидация: `catalog_name` непустой, `attribute_spec`
    — dict, `attribute_spec.name` без edge-whitespace,
    `attribute_spec.type` из whitelist'а
    `{"String", "Number", "Date"}`. Operation читает
    `Catalogs/<catalog_name>.xml`, отказывает, если имя уже
    встречается в тексте, вставляет фрагмент
    `<Attribute name="..."><Type>...</Type>[<Synonym>...</Synonym>]</Attribute>`
    перед последним закрывающим тегом (`rfind("</")`) и пишет
    обратно в UTF-8. Synonym — опциональный. Verify перечитывает
    и проверяет наличие имени и типа. **Это MVP-уровень, не full
    1C XML DOM editor** — честно зафиксировано в README/docstring.
- **Группа D (самостоятельные, не через `run_write_flow`, не
  меняют состояние):**
  - `write_audit_record(environment, record)` — явная запись
    аудита. Требует dict с ненулевыми строковыми
    `operation_id`/`tool_name`/`status`/`message`; `environment`
    и `base_id` `AuditRecord`'а заполняются из `environment`.
    `audit_dir = <dump_path>/.audit`, запись — `append_record(...)`
    из `onec-audit`. `OSError` оборачивается в
    `ToolResult(ok=False, ...)`.
  - `describe_last_write_operation(environment)` — reader поверх
    `read_last_record(...)`. При отсутствии записей — `ok=False,
    "No audit records found."`; при успехе — `ok=True` с полным
    паспортом.
  - `prepare_rollback_hint(environment, operation_id)` —
    human-readable подсказка по ручному откату. **Не выполняет
    rollback.** Читает `<dump_path>/.audit/audit.jsonl`, идёт по
    строкам с конца, ищет запись с заданным `operation_id`. На
    отсутствии файла/записи — `ok=False` с понятным сообщением;
    при успехе — `ok=True` с `audit_status`,
    `suggested_backup_root`, `suggested_dump_root` и `hint_text`
    с подсказкой по ручному откату.
- В `apps/mcp-write-server/src/mcp_write_server/server.py`
  registry поднят до 15 через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Алфавитный
  `list_tools()`: `['add_catalog_attribute',
  'apply_config_from_files', 'check_write_preconditions',
  'create_backup_snapshot', 'create_common_module',
  'create_dump_snapshot', 'describe_last_write_operation', 'ping',
  'prepare_rollback_hint', 'update_database_configuration',
  'update_module_code', 'verify_metadata_change',
  'verify_module_contains', 'verify_object_exists',
  'write_audit_record']`.
- README `mcp-write-server` дополнен разделом «Оставшиеся group B
  + audit/rollback helpers (Phase 2 / Step 9)» с явными
  пометками про stub-backed `update_database_configuration`,
  pragmatic XML patch `add_catalog_attribute` и не-выполняющий
  rollback `prepare_rollback_hint`. Все предыдущие разделы
  сохранены.
- **Ручная проверка 6 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` и in-process
  `socketserver.TCPServer` (200 на любой GET). Реальный стенд не
  затрагивался:
  - **A `update_database_configuration` success**: `ok=True`,
    `stage='completed'`, `verify_payload.verified=True`;
    `.update-db-stub.txt` и `.update-db-meta.json` реально
    существуют в dump-корне.
  - **B `add_catalog_attribute` success**: `ok=True`,
    `stage='completed'`, после operation XML-файл содержит имя
    атрибута `Жанр`, тип `String` и synonym `Жанр фильма`;
    хвост XML: `<Name>Фильмы</Name><Attribute
    name="Жанр"><Type>String</Type><Synonym>Жанр фильма</Synonym></Attribute></MetaData>`.
    Verify прошёл.
  - **C `write_audit_record` success**: `ok=True`, `audit.jsonl`
    создан; JSON-строка реально содержит
    `operation_id="op-fixed-cde"`, `tool_name="synthetic_operation"`,
    `environment="Local Dev"`, `base_id="local-dev"`, `status="ok"`.
  - **D `describe_last_write_operation` после C**: `ok=True`,
    возвращает именно ту же запись (`operation_id=op-fixed-cde`,
    `status=ok`, `tool_name=synthetic_operation`, матчится с
    данными C).
  - **E `prepare_rollback_hint("op-fixed-cde")` после C**:
    `ok=True`, `audit_status=ok`, `suggested_backup_root` и
    `suggested_dump_root` заполнены (указывают на
    `<workdir>/_snapshots`), `hint_text` длиной 127 символов и
    начинается с «Locate the backup/dump snapshot created around
    this operation».
  - **F Registry check**: `list_tools()` возвращает 15 имён в
    алфавитном порядке; `len(REGISTERED_TOOLS) == 15`.
- **Dev-check после изменений зелёный**:
  `write_server_tools` = 15 имён, `read_server_tools` = 15 (не
  деградировал), `selfcheck_status = ok`, `Dev check completed
  successfully.` Skeleton selfcheck не трогался.

### Phase 2 / Step 10 — final integration pass (завершён, Phase 2 Write MVP закрыт окончательно)

- **Аудит консистентности выполнен.** Проверены все 15
  инструментов write-server'а:
  - все 5 mutating tools группы B (`apply_config_from_files`,
    `update_module_code`, `create_common_module`,
    `update_database_configuration`, `add_catalog_attribute`)
    идут строго через `run_write_flow(...)` — preflight,
    backup+dump snapshots, operation, verify, audit;
  - все 3 verification tools группы C (`verify_module_contains`,
    `verify_object_exists`, `verify_metadata_change`) —
    самостоятельные, состояние не меняют, не пишут audit;
  - все 3 audit/rollback helpers группы D (`write_audit_record`,
    `describe_last_write_operation`, `prepare_rollback_hint`) —
    не меняют state базы/dump; `prepare_rollback_hint` только
    готовит подсказку, rollback не выполняет;
  - все public tools возвращают `ToolResult` с `tool_name` = имя
    public-инструмента (rewrap через `_with_tool_name`);
  - исключения наружу не выпадают ни на одной границе tool.
- **Одна точечная правка сделана.** В
  `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py`
  функция `_append_audit` теперь записывает
  `tool_name = context.intent.operation_name` вместо жёстко
  прошитого `"run_write_flow"`. Это делает записи аудита
  трассируемыми до точного public-инструмента
  (`update_module_code`, `add_catalog_attribute` и т.д.) и
  согласует поле `tool_name` в `AuditRecord` с одноимённым полем
  в `ToolResult`. Ранее prior ручные проверки на Step 6 не
  завязывались на `tool_name="run_write_flow"` в audit — изменение
  не создаёт регрессий.
- **Интеграционный прогон** через временный скрипт в `%TEMP%`
  с `tempfile.TemporaryDirectory` и in-process HTTP 200 сервером.
  Реальный стенд не затрагивался.
  - **Registry integrity**: `list_tools()` вернул ровно 15
    ожидаемых имён;
    `len(REGISTERED_TOOLS) == 15 and set(...) == EXPECTED = True`.
  - **Scenario A — full write path via `update_module_code`.**
    1. `update_module_code(env, rel_path, new_text)` →
       `ok=True, tool='update_module_code', stage='completed'`,
       присутствуют `backup_snapshot_path`, `dump_snapshot_path`,
       `audit_path`; файл на диске действительно перезаписан
       (`file_on_disk_matches_new_text=True`).
    2. `verify_module_contains(env, rel_path, "MCP_Test")` →
       `ok=True, contains=True` (внешний verify вне flow).
    3. `describe_last_write_operation(env)` →
       `audit.tool_name='update_module_code'` (новое!),
       `audit.status='ok'`, `operation_id` совпадает с
       `data.operation_id` из шага 1.
    4. `prepare_rollback_hint(env, operation_id)` →
       `ok=True`, `audit_status='ok'`, оба
       `suggested_backup_root`/`suggested_dump_root` заполнены,
       `hint_text` непустой.
  - **Scenario B — metadata path via `add_catalog_attribute`.**
    `add_catalog_attribute(env, "Фильмы", {...})` →
    `ok=True, tool='add_catalog_attribute', stage='completed'`,
    audit присутствует. `verify_metadata_change(env,
    {"kind":"module_contains", ..., "expected_substring":"Жанр"})`
    → `ok=True`, `verification_kind='module_contains'`,
    `contains=True` — атрибут реально попал в XML.
    `describe_last_write_operation` → `audit.tool_name
    ='add_catalog_attribute'`, статус `ok`.
  - **Scenario C — failure path: `update_module_code` на
    несуществующий путь.** `ok=False,
    tool='update_module_code'`, `stage='operation'`, присутствуют
    `operation_id` и `audit_path`; message начинается с
    `"Write operation failed: Module not found in dump: ..."`.
    `describe_last_write_operation` →
    `audit.tool_name='update_module_code'`, **`audit.status
    ='error'`**, message совпадает. Исключение наружу не
    вышло — контракт fail-closed подтверждён.
- **README `mcp-write-server`** дополнен новым разделом
  «Write MVP закрыт (Phase 2 / Step 10 — final integration pass)»:
  explicit свод по группам A/B/C/D, перечень гарантий контура,
  честный список временных stub'ов (`apply_config_from_files`,
  `update_database_configuration`, `create_dump_snapshot`,
  `prepare_rollback_hint`, `add_catalog_attribute`) и пометка,
  что настоящий `1cv8`-integration — отдельный follow-up, не
  блокирующий MVP.
- **Root `README.md`** обновлён: блок «Текущий статус по фазам»
  помечает Phase 2 как завершённую (15 tools, краткий расклад
  по группам + честная пометка про stub'ы), добавлена строка
  «Phase 3 — следующий этап», материалы Phase 2 перенесены в
  список закрытых фаз.
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `read_server_tools` = 15, `write_server_tools` = 15,
  `selfcheck_status = ok`, `Dev check completed successfully.`
- **Phase 2 / Write MVP закрыт.** Все 10 шагов фазы выполнены;
  контур preflight → snapshots → operation → verify → audit
  действительно работает как единая система, что подтверждено
  интеграционным прогоном; read-server остался read-only; все
  временные stub'ы явно задокументированы как временные. Критерии
  приёмки `phase-2-write-mvp-plan.md` достигнуты на уровне
  контракта и success-path. End-to-end против реального Apache
  стенда + настоящий `1cv8`-binary — эксплуатационные вопросы,
  не пробел платформы.

### Phase 3 / Step 1 — planning Metadata Changes (завершён)

- Phase 2 / Write MVP закрыт; Phase 3 — активная фаза разработки.
- Добавлен `docs/architecture/phase-3-metadata-changes-plan.md` —
  план Phase 3: назначение фазы (переход от точечных write-операций
  к полноценным metadata-операциям — объекты / реквизиты / формы /
  модули / связи), целевой результат (metadata-oriented изменения
  через тот же `run_write_flow`, internal metadata patch layer,
  обязательные verify + audit, структура ближе к реальному 1C
  dev workflow), стартовый набор инструментов по четырём группам:
  - **A — object-level**: `create_catalog`, `create_document`,
    `create_information_register`, `create_common_module_from_template`,
    `create_role`;
  - **B — attribute/schema**: обновлённый `add_catalog_attribute`,
    `add_document_attribute`, `add_tabular_section`,
    `add_form_attribute`, `change_attribute_type` (с явным intent);
  - **C — form/module structure**: `create_managed_form`,
    `add_form_element`, `bind_form_handler`,
    `append_module_method`, `replace_module_method_body` (с
    подтверждением);
  - **D — verification / structural diagnostics**:
    `verify_attribute_exists`, `verify_form_exists`,
    `verify_module_method_exists`, `verify_metadata_shape`,
    `diff_dump_fragment`.
  Зафиксированы guardrails Phase 3 (жёстче, чем Write MVP):
  production-like blocked, любое metadata change строго через
  полный flow, идемпотентность-или-fail-closed, запрет silent
  mutation, переход от наивного text-patch к structural patch
  там, где возможно, явный intent для необратимых операций,
  verify+audit обязательны в том же flow. Описано, что не входит
  в фазу (autonomous refactoring, production automation,
  self-healing, multi-base, GUI, product workflows, замена stub'ов
  Phase 2 на реальный `1cv8`-binary). Определены критерии приёмки
  (не менее 4–5 mutating metadata tools, 2–3 verification tools,
  audit корректен, end-to-end metadata сценарий подтверждён,
  dev-check зелёный).
- Добавлен `docs/architecture/phase-3-step-map.md` — стартовый
  implementation map на первые 7 шагов Phase 3:
  1. Metadata operation contract / intent model
     (документация + фиксация intent names);
  2. Усиление `onec-policy-engine` (+ опционально `onec-config`)
     под новый список metadata operation names;
  3. Internal metadata patch helper layer в
     `apps/mcp-write-server/src/mcp_write_server/runtime/metadata_ops.py`
     (без public tools);
  4. Первая волна metadata tools на object/attribute level
     (`create_catalog`, `add_document_attribute`, обновлённый
     `add_catalog_attribute`);
  5. Verification-tools для metadata shape
     (`verify_attribute_exists`, `verify_metadata_shape`,
     `diff_dump_fragment`);
  6. Form/module level tools
     (`create_managed_form`, `add_form_element`,
     `append_module_method`, `replace_module_method_body` с
     подтверждением);
  7. Final integration pass Phase 3.
- Обновлён корневой `README.md`: блок «Текущий статус по фазам»
  помечает Phase 3 как активную фазу, добавлены ссылки на
  `phase-3-metadata-changes-plan.md` и `phase-3-step-map.md`.
- Никаких правок кода на этом шаге не делалось: `apps/`,
  `packages/`, `scripts/`, `.github/`, `pyproject.toml` не
  тронуты. Registry read-server = 15, registry write-server = 15.

### Phase 3 / Step 2 — metadata operation contract в `onec-policy-engine` (завершён)

- **Policy contract расширен до четырёх категорий operation_name.**
  В `packages/onec-policy-engine/src/onec_policy_engine/engine.py`
  добавлены два новых frozenset'а (поверх уже существующих, без
  пересечений):
  - `_METADATA_MUTATING_OPERATIONS` = `create_catalog`,
    `create_document`, `create_information_register`,
    `create_common_module_from_template`, `create_role`,
    `add_document_attribute`, `add_tabular_section`,
    `add_form_attribute`, `change_attribute_type`,
    `create_managed_form`, `add_form_element`, `bind_form_handler`,
    `append_module_method`, `replace_module_method_body`.
  - `_METADATA_SUPPORT_OPERATIONS` = `verify_attribute_exists`,
    `verify_form_exists`, `verify_module_method_exists`,
    `verify_metadata_shape`, `diff_dump_fragment`.
- **Существующие Phase 2 наборы не тронуты.** `_MUTATING_OPERATIONS`
  и `_NON_MUTATING_SUPPORT_OPERATIONS` остались точно в прежнем
  составе; новые metadata-ops добавлены поверх, а не вместо.
  `add_catalog_attribute` и остальные Phase 2 имена остались в
  своих категориях с теми же `reason_code`.
- **`_new_check` расширен двумя ветками** (в порядке: Phase 2
  mutating → Phase 2 support → Phase 3 metadata mutating →
  Phase 3 metadata support → unknown). Новые `reason_code`:
  - `allowed_metadata_mutating` — `require_snapshots=True`, reason
    `"Metadata mutating operation allowed; snapshots are
    required."`;
  - `allowed_metadata_support` — `require_snapshots=False`, reason
    `"Metadata verification/support operation allowed."`.
  Legacy Phase 2 `reason_code` (`allowed_mutating`,
  `allowed_non_mutating`) сохранены ровно в прежнем виде.
- **Backward compatibility сохранена.** `_legacy_check(str, bool)`
  не менялся; `check_write_allowed("production", True)` и
  `check_write_allowed("local-dev", False)` возвращают точно те же
  `PolicyDecision`, что и до шага. `scripts/dev/selfcheck.py` не
  трогался.
- **`models.py` и `__init__.py` не изменялись** — `PolicyDecision`
  уже имеет все нужные поля (`allowed`, `reason`, `reason_code`,
  `require_snapshots`), экспорты корректны.
- **`onec-config` не трогался.** Все заявленные metadata ops
  укладываются в уже существующие поля `EnvironmentConfig`
  (`dump_path`, `base_path`, `publication_name`, `http_base_url`,
  `allow_write`, `timeout_seconds`, `base_id`, `name`). Поле
  `onec_binary_path` — отдельный follow-up для настоящего
  `1cv8`-integration, не нужно для policy contract Phase 3.
- **README `onec-policy-engine` переписан.** Добавлен раздел
  «Категории operation_name» с явным перечислением всех четырёх
  групп; раздел «Коды решений» расширен до шести allow-кодов
  (`allowed_mutating`, `allowed_non_mutating`,
  `allowed_metadata_mutating`, `allowed_metadata_support`,
  `allowed_legacy`) + двух deny-кодов (`production_blocked`,
  `write_not_allowed`) + `unknown_intent`. README `onec-config`
  не трогался.
- **Ручная проверка 6 основных сценариев + 4 дополнительных +
  1 regression** через временный скрипт в `%TEMP%`:
  - **A legacy `("production", True)`**: `allowed=False,
    reason_code='production_blocked', require_snapshots=False`.
  - **B legacy `("local-dev", False)`**: `allowed=False,
    reason_code='write_not_allowed', require_snapshots=False`.
  - **C new-mode `WriteIntent("create_catalog", ...)` на writable
    local-dev**: `allowed=True,
    reason_code='allowed_metadata_mutating',
    require_snapshots=True` — Phase 3 metadata mutating ветка
    сработала, как и требовалось.
  - **D new-mode `WriteIntent("verify_attribute_exists", ...)`**:
    `allowed=True, reason_code='allowed_metadata_support',
    require_snapshots=False`.
  - **E new-mode `WriteIntent("update_module_code", ...)`
    (regression Phase 2)**: `allowed=True,
    reason_code='allowed_mutating', require_snapshots=True` —
    Phase 2 поведение не изменилось.
  - **F new-mode `WriteIntent("totally_unknown_operation")`**:
    `allowed=False, reason_code='unknown_intent',
    require_snapshots=False` — fail-closed.
  - Дополнительно проверены ещё 4 metadata intent'а
    (`create_document`, `append_module_method`,
    `change_attribute_type`, `verify_metadata_shape`,
    `diff_dump_fragment`) — каждый попал в ожидаемую ветку.
  - Regression-контроль: Phase 2 support
    (`describe_last_write_operation`) вернул
    `reason_code='allowed_non_mutating'` — как и прежде.
  - Во всех 11 вызовах результат — `PolicyDecision` (assertion
    через `isinstance` прошла).
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `production_write_allowed = false`, `local_dev_write_allowed =
  false` (точно как в selfcheck'е до шага), `selfcheck_status =
  ok`, `Dev check completed successfully.` Skeleton selfcheck не
  трогался.

### Phase 3 / Step 3 — internal metadata patch helper layer (завершён)

- **Создан новый файл**
  `apps/mcp-write-server/src/mcp_write_server/runtime/metadata_ops.py`.
  Это **internal** layer: не возвращает `ToolResult`, не ходит в
  HTTP/subprocess/audit/snapshot. Будет использован будущими
  metadata tools Phase 3 / Step 4–6, прямо сейчас **не подключён** к
  `tools.py` / `server.py`. Registry write-server'а не менялся
  (15 инструментов).
- **10 helper'ов в четырёх группах:**
  - **XML / text structural:**
    - `load_xml_text(path)` — UTF-8 `read_text`, `OSError`
      пробрасывается.
    - `insert_before_last_closing_tag(xml_text, fragment)` —
      fallback перед последним `</...>`; `ValueError` если
      closing tag нет.
    - `insert_fragment_into_named_block(xml_text, block_name,
      fragment)` — основной structural helper: поиск парной
      `<block_name>...</block_name>` и вставка перед её
      закрывающим тегом. Требует именно парную структуру
      (self-closing `<block_name/>` не подходит). Отсутствие
      блока → `ValueError` с понятным сообщением.
  - **Fragment builders:**
    - `build_attribute_fragment(name, attr_type, synonym=None)` —
      `<Attribute name="..."><Type>...</Type>[<Synonym>...</Synonym>]</Attribute>`.
    - `build_form_fragment(form_name)` — минимальный `<Form>` stub
      (не полная 1C managed form card).
    - `build_module_method_fragment(method_name, body, export=False)`
      — канонически зафиксированный формат BSL:
      `Процедура <name>() [Экспорт]\n<body>\nКонецПроцедуры\n`.
      Функции / директивы / аннотации — вне контракта Step 3.
  - **BSL helpers:**
    - `module_contains_method(module_text, method_name)` — regex
      `\b(Процедура|Функция|Procedure|Function)\s+<name>\s*\(` с
      `re.IGNORECASE`. Не полноценный парсер, но достаточно для
      smoke-verify.
    - `append_method_to_module(module_text, method_fragment)` —
      предсказуемые разделители строк на стыке.
  - **File patch helpers:**
    - `patch_xml_file(path, patcher)` — read-transform-write в
      UTF-8; `OSError` пробрасывается.
    - `patch_text_file(path, patcher)` — аналог для BSL/plain.
- **`runtime/__init__.py` не трогался.** Подход согласован с
  существующим `dump_ops.py` (Phase 2 / Step 5): helper'ы
  импортируются напрямую из submodule —
  `from .runtime.metadata_ops import ...`, без re-export на
  top-level runtime. Это сохраняет compact public surface.
- **Остальные runtime-файлы (`context.py`, `guards.py`, `flow.py`,
  `models.py`) не трогались.** `tools.py`, `server.py`, верхние
  `models.py` / `__init__.py` write-server'а — тоже не
  трогались. Registry write-server'а = те же 15 имён.
- **Ручная проверка 7 сценариев + 3 дополнительных smoke** через
  временный скрипт в `%TEMP%`:
  - **A `insert_fragment_into_named_block` success** на XML с
    `<Attributes>...</Attributes>`: fragment вставлен именно
    внутрь Attributes перед `</Attributes>` (substring
    `</Attribute></Attributes>` присутствует), `Genre` попал в
    текст.
  - **B `insert_fragment_into_named_block` failure** на XML без
    `<Attributes>`: `ValueError: XML block <Attributes> not
    found (no closing tag).`
  - **C `build_attribute_fragment`**: без synonym — `<Synonym>`
    тега нет; с synonym — есть; имя и тип присутствуют.
  - **D `module_contains_method`**: True для `ПерваяПроцедура`
    (Процедура) и `MCP_Test` (Функция), False для
    несуществующего имени.
  - **E `append_method_to_module`**: результат начинается с
    оригинала, содержит вставленный fragment, новый метод
    детектится через `module_contains_method`, старые методы
    по-прежнему детектятся.
  - **F `patch_xml_file`**: файл на диске реально изменился —
    `name="X"` и `<Type>Number</Type>` присутствуют.
  - **G `patch_text_file`**: BSL-файл на диске действительно
    дополнен; `module_contains_method('Hello')` → True.
  - **Extra smoke**: `load_xml_text` вернул корректную длину;
    `insert_before_last_closing_tag` вставил `<Extra/>` перед
    `</MetaData>`; на входе без `</` — `ValueError: No closing
    tag found in XML text.`; `build_form_fragment` содержит
    переданное имя.
- **README `mcp-write-server`** дополнен новым разделом
  «Internal metadata patch helper layer (Phase 3 / Step 3)» —
  полный перечень helper'ов по 4 группам, выбранный BSL-формат,
  явная отметка «это не public tool layer, registry не меняется».
  Блоки Step 4 / Step 5 / Step 6 / Step 7 / Step 8 / Step 9 /
  Step 10 из Phase 2 сохранены без изменений.
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `write_server_tools` = 15 (те же имена, новый helper layer не
  публикуется), `read_server_tools` = 15, `selfcheck_status =
  ok`, `Dev check completed successfully.`

### Phase 3 / Step 4 — первая волна object/attribute metadata tools (завершён)

- **В `apps/mcp-write-server/src/mcp_write_server/tools.py`
  добавлено 2 новых public mutating tool'а и рефакторен
  существующий `add_catalog_attribute`.** Все три tool'а идут
  через `run_write_flow(...)` (preflight → backup+dump snapshots
  → operation → verify → audit); tool_name в итоговом
  `ToolResult` — имя public-инструмента (rewrap через
  `_with_tool_name`). `runtime/metadata_ops.py` из Step 3 не
  менялся — только используется.
- **`create_catalog(environment, catalog_name, spec,
  label="create-catalog")`** — создаёт
  `Catalogs/<catalog_name>.xml` с минимальным stub-карточкой:
  `<MetaData><Name>...</Name>[<Synonym>...</Synonym>]<Attributes></Attributes></MetaData>`.
  Включение пустого `<Attributes></Attributes>` в stub делает
  карточку сразу пригодной для последующего
  `add_catalog_attribute`. Pre-flow валидация: `catalog_name` по
  regex `\w+` (тот же `_MODULE_NAME_RE`, что у
  `create_common_module`), `spec` — dict, `spec.synonym`
  опциональный string. Если файл уже существует —
  `FileExistsError` в operation (flow → `ok=False,
  stage=operation`, audit пишется со `status='error'`).
- **`add_document_attribute(environment, document_name,
  attribute_spec, label="add-document-attribute")`** — добавляет
  атрибут в `Documents/<document_name>.xml`. Целиком поверх
  helper layer Step 3: `build_attribute_fragment(...)` строит
  фрагмент, `insert_fragment_into_named_block(xml_text,
  "Attributes", fragment)` внутри `patch_xml_file(...)` вставляет
  его строго внутрь блока `<Attributes>...</Attributes>`. Если
  такого блока в XML нет — helper поднимает `ValueError`, flow
  отдаёт `ok=False, stage=operation`; **никакого silent fallback
  к последнему `</...>`**. Pre-flow валидация: `document_name`
  непустой, `attribute_spec` — dict, `name` без edge-whitespace,
  `type` из whitelist `{"String", "Number", "Date"}`,
  дубль имени в XML → `FileExistsError`.
- **`add_catalog_attribute(...)` переведён на helper layer Step 3.**
  Внешний public контракт сохранён без изменений: та же сигнатура,
  те же pre-flow валидации, тот же whitelist типов, тот же
  `payload.data` на успехе, те же verify-проверки. Внутри вместо
  старого `rfind("</")` + inline f-string теперь —
  `build_attribute_fragment(...)` + `patch_xml_file(target,
  _patcher)`, где `_patcher` сначала проверяет отсутствие
  дубля имени, затем зовёт `insert_fragment_into_named_block(
  xml_text, "Attributes", fragment)`. Если целевая карточка не
  имеет `<Attributes>` блока — fail-closed (ранее Phase 2 версия
  молча вставляла перед последним `</...>`; сейчас это считается
  ошибкой — соответствует ТЗ Phase 3).
- **В `apps/mcp-write-server/src/mcp_write_server/server.py`
  registry расширен до 17 инструментов** через тот же
  `build_tool_registry(...)` из `mcp-common`. Порядок добавления
  в dict: `ping`, Phase 2 group A (3), group B mutating (3 Step 7
  + 2 Step 9 = 5), group C verify (3), group D audit (3), затем
  2 новых Step 4. Алфавитный `list_tools()`:
  `['add_catalog_attribute', 'add_document_attribute',
  'apply_config_from_files', 'check_write_preconditions',
  'create_backup_snapshot', 'create_catalog',
  'create_common_module', 'create_dump_snapshot',
  'describe_last_write_operation', 'ping', 'prepare_rollback_hint',
  'update_database_configuration', 'update_module_code',
  'verify_metadata_change', 'verify_module_contains',
  'verify_object_exists', 'write_audit_record']`.
- **README `mcp-write-server`** дополнен разделом
  «Object/attribute level metadata tools (Phase 3 / Step 4)»:
  описание всех трёх tool'ов, явная отметка про переход
  `add_catalog_attribute` на helper layer, registry = 17. Блоки
  Step 3 и Phase 2 Step 4–10 сохранены без изменений.
- **Ручная проверка 6 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` + in-process HTTP 200:
  - **A `create_catalog("Контрагенты", {"synonym": ...})`
    success**: `ok=True, stage='completed'`; файл
    `Catalogs/Контрагенты.xml` реально создан со stub-XML
    `<MetaData><Name>Контрагенты</Name><Synonym>Контрагенты
    организации</Synonym><Attributes></Attributes></MetaData>`;
    verify.has_synonym=True; `describe_last_write_operation`
    показывает `audit.tool_name='create_catalog'` и
    `audit.status='ok'` (благодаря правке `_append_audit` из
    Step 10 Phase 2).
  - **B `create_catalog("Dup", {})` над существующим файлом**:
    `ok=False, stage='operation'`, message `"Write operation
    failed: Catalog XML already exists: Catalogs/Dup.xml"`,
    audit записан со `status='error'`, исключение наружу не
    вышло.
  - **C `add_document_attribute("Заказ", {"name":"Сумма",
    "type":"Number", "synonym":"Итоговая сумма"})`**: `ok=True,
    stage='completed'`; XML на диске — `<MetaData><Name>Заказ</Name>
    <Attributes><Attribute name="Сумма"><Type>Number</Type>
    <Synonym>Итоговая сумма</Synonym></Attribute></Attributes>
    </MetaData>`; все три substring-проверки `has_attr_name`,
    `has_type`, `has_synonym` → True.
  - **D `add_document_attribute("НетБлока", {"name":"X",
    "type":"String"})` на XML без `<Attributes>` блока**:
    `ok=False, stage='operation'`, message `"Write operation
    failed: XML block <Attributes> not found (no closing tag)."`,
    **`xml_unchanged=True`** (файл на диске остался идентичным
    исходному — `patch_xml_file` не дошёл до write_text потому что
    patcher поднял ValueError до этого), audit со
    `status='error'`. No silent fallback подтверждён.
  - **E regression `add_catalog_attribute("Фильмы", {...})` на
    карточке с `<Attributes></Attributes>`**: `ok=True,
    stage='completed'`; XML на диске — `<MetaData><Name>Фильмы</Name>
    <Attributes><Attribute name="Жанр"><Type>String</Type>
    <Synonym>Жанр фильма</Synonym></Attribute></Attributes>
    </MetaData>`; substring `</Attribute></Attributes>` присутствует
    → fragment именно внутри Attributes, не перед `</MetaData>`.
    Это ключевое отличие от Phase 2 поведения — новый helper
    layer действительно задействован.
  - **F Registry check**: `len(REGISTERED_TOOLS) == 17`,
    `set(REGISTERED_TOOLS) == EXPECTED_17` (все 15 Phase 2 имён +
    2 новых). ✓
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `write_server_tools` = 17 (два новых имени видны),
  `read_server_tools` = 15 (не деградировал),
  `selfcheck_status = ok`, `Dev check completed successfully.`

### Phase 3 / Step 5 — verification-tools для metadata shape (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py` добавлены
  два новых public read-only tool'а и расширен dispatcher
  `verify_metadata_change`. Все новые/расширенные verification'ы —
  **самостоятельные**, состояние не меняют, snapshot не снимают,
  audit не пишут, **не идут через `run_write_flow`**. Cross-app
  import по-прежнему строго `write → read` (`read_dump_file` из
  `mcp_read_server.runtime`). Новых runtime-файлов не создавалось —
  используется уже существующий helper layer Step 3.
- **Новый tool `verify_attribute_exists(environment, object_name,
  attribute_name)`**: dump-only substring-проверка наличия атрибута
  в XML-карточке resolved-объекта. Приватный helper
  `_resolve_object_xml_path(object_name)` поддерживает MVP-префиксы
  `Справочник.` → `Catalogs/<tail>.xml` и `Документ.` →
  `Documents/<tail>.xml`; другой/пустой префикс → `ok=False` с
  понятным reason. `PlatformError` от dump adapter → `ok=False`
  без утечки исключения. Payload: `object_name`, `attribute_name`,
  `relative_path` (если удалось разрешить), `exists`.
- **Расширение `verify_metadata_change(environment, expectation)`**
  — в dispatcher добавлены три новые ветки по `kind`:
  - `"attribute_exists"` с `object_name`, `attribute_name` —
    делегирует в `verify_attribute_exists(...)`;
  - `"form_exists"` с `object_name`, `form_name` — inline через
    приватный `_verify_form_exists_internal(...)`: MVP dump-level
    substring-поиск имени формы в XML карточки объекта. Отдельного
    public `verify_form_exists` tool'а на этом шаге не создавалось
    — только новая ветка dispatcher'а, как требует ТЗ;
  - `"method_exists"` с `module_relative_path`, `method_name` —
    inline через приватный `_verify_method_exists_internal(...)`:
    читает модуль через `read_dump_file` и проверяет объявление
    метода через уже существующий `module_contains_method` из
    helper layer Step 3.
  Итоговый `tool_name` всегда `"verify_metadata_change"`,
  `payload.data.verification_kind` — имя сработавшей ветки. Старые
  ветки `"object_exists"` / `"module_contains"` сохранены без
  изменений. Неизвестный `kind` по-прежнему fail-closed.
- **Новый tool `diff_dump_fragment(environment, relative_path,
  baseline)`**: unified-diff через `difflib.unified_diff` текста
  dump-файла против переданного baseline. `ok=True`, если файл
  удалось прочитать, независимо от наличия различий — diff это
  информация, не ошибка. `ok=False` только при
  `PlatformError`/отсутствии файла. Diff preview компактный —
  первые `_DIFF_PREVIEW_MAX_LINES=40` строк unified diff с
  маркером `(diff truncated)` при переполнении; при равенстве
  текстов `diff_preview=""`. Payload: `relative_path`, `changed`,
  `current_text_length`, `baseline_length`, `diff_preview`.
- **В `server.py` зарегистрированы два новых tool'а**
  (`verify_attribute_exists`, `diff_dump_fragment`). Registry
  вырос до **19 инструментов**. `verify_metadata_change` уже был
  в registry — получил только новые ветки внутри.
- **README `mcp-write-server`** дополнен разделом «Verification-tools
  для metadata shape (Phase 3 / Step 5)»: описание двух новых
  public tools, трёх новых веток dispatcher'а, явная отметка что
  все verify'и read-only и не идут через flow, registry = 19.
  Блоки Step 3/Step 4 и Phase 2 Step 4–10 сохранены.
- **Ручная проверка 8 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory`. HTTP-сервер в этом
  шаге не нужен — все проверки работают с dump-файлами напрямую.
  Реальный стенд не затрагивался:
  - **A `verify_attribute_exists("Справочник.Фильмы", "Жанр")`
    success**: `ok=True`, `exists=True`,
    `relative_path='Catalogs/Фильмы.xml'`, сообщение «Attribute
    exists in dump XML.»
  - **B `verify_attribute_exists` not found**: та же XML-карточка,
    но без нужного атрибута — `ok=False`, `exists=False`,
    `relative_path` всё ещё корректный.
  - **C `verify_metadata_change(kind="attribute_exists", ...)`**:
    `tool_name='verify_metadata_change'`,
    `verification_kind='attribute_exists'`, `exists=True` —
    dispatcher корректно делегировал в `verify_attribute_exists`.
  - **D form_exists (positive + negative)**: на карточке с
    `<Forms><Form>ФормаСписка</Form></Forms>` positive → `ok=True,
    exists=True`; negative с несуществующим именем формы → `ok=False,
    exists=False`; в обоих случаях `tool_name=verify_metadata_change`,
    `verification_kind=form_exists`.
  - **E method_exists (positive + negative)**: в
    `CommonModules/Test/Ext/Module.bsl` лежит
    `Процедура MCP_Test()`; positive с `method_name='MCP_Test'` →
    `ok=True, exists=True`; negative с несуществующим именем →
    `ok=False, exists=False`; `tool_name=verify_metadata_change`,
    `verification_kind=method_exists`.
  - **F `diff_dump_fragment` changed=False**: baseline идентичен
    файлу — `ok=True, changed=False`, `current_text_length =
    baseline_length = 38`, `diff_preview` пустой.
  - **G `diff_dump_fragment` changed=True**: в файле добавлен
    `<Attribute name="Код"/>` внутри `<Attributes>`; `ok=True,
    changed=True`, lengths 86 vs 63 (наглядно показывают, что
    было добавлено), `diff_preview` содержит корректный unified
    diff с `--- baseline / +++ current / @@ -1 +1 @@` и строками
    `-<MetaData>...<Attributes></Attributes>...</MetaData>` /
    `+<MetaData>...<Attributes><Attribute name="Код"/></Attributes>
    ...</MetaData>`.
  - **H Registry check**: `len(REGISTERED_TOOLS) == 19`,
    `set(REGISTERED_TOOLS) == EXPECTED_19` (все 17 из Step 4 + 2
    новых). ✓
  - Во всех случаях tool вернул `ToolResult`, исключение наружу
    не вышло.
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `write_server_tools` = 19 (оба новых имени на месте),
  `read_server_tools` = 15 (не тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`

### Phase 3 / Step 6 — form/module level metadata tools (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py` добавлены
  **4 новых public mutating tool'а** уровня форм и модулей. Все
  четыре идут через `run_write_flow(...)` — preflight,
  backup+dump snapshots, operation, verify, audit; `tool_name` в
  итоговом `ToolResult` переписывается на имя public-инструмента
  через `_with_tool_name`. Helper layer Step 3 активно
  переиспользуется.
- **`create_managed_form(environment, object_name, form_name,
  label="create-managed-form")`** — вставка `build_form_fragment`
  внутрь блока `<Forms>` resolved-XML объекта через
  `insert_fragment_into_named_block`. Pre-flow валидация
  `object_name` (ненулевая строка + поддерживаемый префикс
  `Справочник.`/`Документ.` через уже существующий
  `_resolve_object_xml_path`) и `form_name` (`\w+`). Fail-closed,
  если `<Forms>` нет в XML или форма уже существует.
- **`add_form_element(environment, object_name, form_name,
  element_spec, label="add-form-element")`** — pragmatic
  structural patch: приватные helper'ы `_find_form_block_bounds`
  и `_build_form_element_fragment` локализуют нужный
  `<Form name="form_name">...</Form>` блок и вставляют элемент
  **именно в его `<Elements>...</Elements>`**, а не в конец XML.
  Fail-closed, если формы нет, у неё нет парного `<Elements>`
  блока, или в ней уже есть элемент с таким именем (коллизия
  проверяется substring'ом `<Element name="element_name">` в
  границах формы). `element_spec`: `name`, `type`, опционально
  `title`.
- **`append_module_method(environment, module_relative_path,
  method_spec, label="append-module-method")`** — добавление
  нового BSL метода в модуль через helper layer Step 3:
  `build_module_method_fragment` → `append_method_to_module` →
  `patch_text_file`. Коллизия — через `module_contains_method`.
  `method_spec`: `name` (`\w+`), `body` (non-empty non-whitespace),
  `export: bool` по умолчанию `False`. Fail-closed при
  отсутствующем модуле или дубликате.
- **`replace_module_method_body(environment,
  module_relative_path, method_name, new_body, *,
  confirm_replace=False, label=...)`** — **намеренно опасная**
  операция. Требует явного `confirm_replace=True`, иначе
  отвергается до flow с понятным сообщением (без snapshots /
  audit). Локализация метода — через осторожный regex
  `_BSL_SIGNATURE_RE_TEMPLATE` +
  `_BSL_END_PROCEDURE_RE` / `_BSL_END_FUNCTION_RE` (совпадают с
  родом keyword'а сигнатуры). Тело заменяется **только между
  найденной сигнатурой и соответствующим end-keyword'ом**,
  никакого глобального replace по имени. Fail-closed, если
  модуля нет, метод не найден, или структура не распознаётся
  однозначно.
- **`runtime/metadata_ops.py`** получил точечное обратно-совместимое
  изменение: `build_form_fragment(form_name)` теперь включает пустой
  `<Elements></Elements>` блок внутри `<Form>`, чтобы будущие
  вызовы `add_form_element` имели детерминированную точку
  вставки. Это единственная правка helper layer Step 3; все
  предыдущие smoke-проверки Step 3 (substring `form_name in
  fragment`) по-прежнему проходят.
- В `server.py` зарегистрированы все 4 новых tool'а. Registry
  write-server'а вырос до **23 инструментов**:
  - group A (safety/preflight) = 3;
  - group B mutating = 5 Phase 2 + 2 Phase 3 Step 4 + 4 Phase 3
    Step 6 = 11;
  - group C verification = 3 Phase 2 + 1 Phase 3 Step 5 + 1
    Phase 3 Step 5 diff = 5;
  - group D audit/rollback = 3;
  - plus `ping`.
- README `mcp-write-server` дополнен разделом «Form/module level
  metadata tools (Phase 3 / Step 6)»: перечень всех 4 tool'ов,
  явная пометка про `confirm_replace` для
  `replace_module_method_body`, явное упоминание точечного
  tweak'а `build_form_fragment`, registry = 23. Блоки Step 3–5
  и Phase 2 Step 4–10 сохранены.
- **Ручная проверка 8 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` и in-process HTTP 200.
  Реальный стенд не затрагивался.
  - **A `create_managed_form` success**: XML с `<Forms></Forms>`;
    после вызова — `<Form name="ФормаСписка">...<Elements></Elements></Form>`
    внутри Forms; `ok=True`, `stage='completed'`,
    `form_in_xml=True`, `form_inside_Forms=True`; audit.tool_name=
    `create_managed_form`, status=ok.
  - **B `create_managed_form` без Forms**: XML без `<Forms>` →
    `ok=False, stage='operation'`, message «XML block <Forms>
    not found (no closing tag).»; XML **unchanged** (silent
    fallback отсутствует); audit.status=error.
  - **C `append_module_method` success**: модуль с `Первая()`;
    добавлен новый `Вторая() Экспорт` с body `Возврат 2;`;
    в файле видны обе сигнатуры; `ok=True, stage='completed'`;
    audit.tool_name=`append_module_method`, status=ok.
  - **D `append_module_method` duplicate**: модуль содержит `Dup()`
    → вторая попытка `ok=False, stage='operation'`, message
    «Method 'Dup' already declared…»; text unchanged;
    audit.status=error.
  - **E `replace_module_method_body` without confirm**: `ok=False,
    tool='replace_module_method_body'`, message «requires
    explicit confirm_replace=True.»; **в payload только `data`** —
    нет `runtime`, нет snapshot refs → flow не запускался, как и
    требует ТЗ.
  - **F `replace_module_method_body` with confirm**: в модуле две
    методы (`Первая()` procedure и `Вторая()` function); вызов
    replace на `Первая` с new_body `Возврат 42;` →
    `ok=True, stage='completed'`; в тексте `has_new_body=True`,
    `old_body_gone=True` (Возврат 1 исчез), `Вторая_intact=True`
    (второй метод не тронут — сигнатура + старое тело `Возврат 2;`
    сохранились); audit.tool_name=`replace_module_method_body`,
    status=ok.
  - **G `add_form_element` success**: XML с формой, содержащей
    `<Elements></Elements>`; элемент `КнопкаОк` с Title `ОК`
    реально появился **внутри** Elements блока нужной формы;
    `ok=True, stage='completed'`, `has_element=True`,
    `has_title=True`, `inside_Elements=True`.
  - **H Registry check**: `len(REGISTERED_TOOLS) == 23`,
    `set(REGISTERED_TOOLS) == EXPECTED_23`. ✓
  - Во всех 8 случаях tool вернул `ToolResult`, исключение наружу
    не вышло.
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `write_server_tools` = 23 (все 4 новых имени видны),
  `read_server_tools` = 15 (не тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`

### Phase 3 / Step 7 — final integration pass (завершён, Phase 3 закрыт)

- **Интеграционный прогон подтвердил metadata-контур end-to-end.**
  Один сквозной сценарий из 10 шагов (5 mutating + 3 verification +
  `describe_last_write_operation` + `prepare_rollback_hint`) на
  временном окружении + два failure path сценария. Реальный стенд
  не затрагивался.
- **Единственная кодовая правка Step 7** — минимальный обратно-
  совместимый tweak `create_catalog` stub в
  `apps/mcp-write-server/src/mcp_write_server/tools.py`: добавлен
  пустой `<Forms></Forms>` блок в XML-карточку наряду с уже
  присутствующим `<Attributes></Attributes>`. Без этого свежий
  каталог не принимал `create_managed_form` — композабильность
  create_catalog ↔ create_managed_form была сломана. Правка
  симметрична добавленному в Step 6 `<Elements></Elements>` внутри
  `build_form_fragment`. Assertions Step 4 manual check
  (`<Name>` / `<Synonym>` substring-проверки, `verify_has_synonym`)
  по-прежнему проходят.
- **Никаких других кодовых правок.** `runtime/flow.py`,
  `runtime/metadata_ops.py`, `runtime/context.py`, `runtime/guards.py`,
  `runtime/models.py`, `runtime/dump_ops.py`, другие public tools —
  не трогались. Registry write-server'а остался **23 инструмента**
  ровно, как и требовало ТЗ.
- **Scenario A — full end-to-end metadata path:** 10 шагов, все
  `ok=True`:
  1. `create_catalog("ТестовыйСправочник", {"synonym":
     "Тестовый справочник"})` → `ok=True, stage=completed`,
     `operation_id` + backup+dump snapshot + audit.
  2. `add_catalog_attribute("ТестовыйСправочник",
     {"name":"Жанр","type":"String","synonym":"Жанр"})` →
     `ok=True, stage=completed`, свой `operation_id` + audit.
  3. `create_managed_form("Справочник.ТестовыйСправочник",
     "ФормаСписка")` → `ok=True, stage=completed`.
  4. `add_form_element(..., {"name":"КнопкаОк","type":"Button",
     "title":"ОК"})` → `ok=True, stage=completed`.
  5. `append_module_method("CommonModules\\TestModule\\Ext\\Module.bsl",
     {"name":"MCP_Test","body":"\\tВозврат 1;","export":True})` →
     `ok=True, stage=completed`, собственный `op_id_5`.
  6. `verify_metadata_change(kind="attribute_exists", object_name=
     "Справочник.ТестовыйСправочник", attribute_name="Жанр")` →
     `ok=True, verification_kind=attribute_exists, exists=True`.
  7. `verify_metadata_change(kind="form_exists", ..., form_name=
     "ФормаСписка")` → `ok=True, verification_kind=form_exists,
     exists=True`.
  8. `verify_metadata_change(kind="method_exists",
     module_relative_path=<module>, method_name="MCP_Test")` →
     `ok=True, verification_kind=method_exists, exists=True`.
  9. `describe_last_write_operation` → `ok=True,
     audit.tool_name='append_module_method'` (не generic
     `run_write_flow` — подтверждает правку `_append_audit`
     Phase 2 Step 10), `audit.status='ok'`, `operation_id`
     совпадает с `op_id_5`.
  10. `prepare_rollback_hint(env, op_id_5)` → `ok=True,
      audit_status='ok'`, оба `suggested_backup_root` /
      `suggested_dump_root` заполнены, `hint_text` длиной 127
      символов.
  - **Финальное состояние на диске:**
    `Catalogs/ТестовыйСправочник.xml` содержит полную композицию
    `<MetaData><Name>...</Name><Synonym>...</Synonym>
    <Attributes><Attribute name="Жанр"><Type>String</Type>
    <Synonym>Жанр</Synonym></Attribute></Attributes>
    <Forms><Form name="ФормаСписка"><Type>ManagedApplicationForm</Type>
    <Elements><Element name="КнопкаОк"><Type>Button</Type>
    <Title>ОК</Title></Element></Elements></Form></Forms></MetaData>`
    (все 9 checks True).
    Модуль `CommonModules/TestModule/Ext/Module.bsl`: исходный
    якорь сохранён, метод `Процедура MCP_Test() Экспорт` добавлен.
  - **Snapshot artefacts:** 5 `backup-local-dev-<label>` и 5
    `dump-local-dev-<label>` директорий на каждой стороне (baseside
    `_snapshots` и dumpside `_snapshots`), по одной на каждый
    mutating шаг.
  - **Audit:** ровно 5 строк в `dump/.audit/audit.jsonl` —
    соответствует 5 mutating операциям.
- **Scenario B — fail-closed на отсутствие `<Forms>` блока:**
  каталог с `<MetaData><Name>БезФорм</Name><Attributes></Attributes></MetaData>`
  без `<Forms>`. `create_managed_form` → `ok=False,
  stage='operation'`, message «Write operation failed: XML block
  <Forms> not found (no closing tag).»; XML **unchanged**;
  `audit.tool_name='create_managed_form'`, `audit.status='error'`
  (flow всё равно написал audit с error статусом). Исключение
  наружу не вышло.
- **Scenario C — `replace_module_method_body` без
  `confirm_replace=True`:** `ok=False,
  tool='replace_module_method_body'`, message «requires explicit
  confirm_replace=True.»; `payload.keys()=['data']` — **нет
  runtime**, **нет snapshot refs**, **нет audit_path**; файл
  `dump/.audit/audit.jsonl` **не создан** (проверено
  `audit_file.exists()==False`). Flow не запускался вообще.
- **Интеграционные критерии (ТЗ Step 7):**
  1. Все mutating metadata tools Step 4–6 идут через
     `run_write_flow` и оставляют `operation_id`, snapshot refs,
     audit-запись. ✓ (подтверждено 5 mutating шагами сценария A)
  2. Все verification tools Step 5 работают как самостоятельные
     public tools, не идут через flow, не пишут audit. ✓
     (подтверждено 3 verification шагами + сценарием C для
     rollback-hint-path)
  3. `tool_name` в audit = public tool name. ✓ (Scenario A Step 9:
     `audit.tool_name='append_module_method'`)
  4. Registry write-server = 23 (не менялся). ✓
  5. Dev-check зелёный. ✓
- **Dev-check после Step 7:** `imports_ok = true`,
  `write_server_tools` = 23 (все 23 имени на месте),
  `read_server_tools` = 15 (не тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`
- **README `mcp-write-server`** дополнен разделом «Phase 3
  Metadata Changes закрыт (Phase 3 / Step 7 — final integration
  pass)» с сводкой по составу контура, гарантиями,
  registry = 23, зафиксированной минимальной правкой
  `create_catalog` stub и перечнем остающихся временных stub'ов.
- **Корневой `README.md`** обновлён: Phase 3 помечена завершённой
  с кратким расписыванием по group A/B/C/D, Phase 4 указана как
  следующий этап, материалы Phase 3 перенесены в «Закрытые фазы».
- **Phase 3 / Metadata Changes закрыт.** Критерии приёмки
  `phase-3-metadata-changes-plan.md` достигнуты: ≥ 4–5
  mutating metadata tools (реально 9: 2 создания объектов + 2
  attribute-level Step 4 + 4 form/module-level Step 6 + 1 уже
  существующий `create_common_module`); ≥ 2–3 verification tools
  (`verify_attribute_exists`, `diff_dump_fragment`, расширенный
  `verify_metadata_change` с 5 kind); audit отражает metadata
  operations корректно (`tool_name=intent.operation_name`); dev-check
  зелёный на каждом шаге; подтверждён end-to-end metadata scenario.

### Phase 4 / Step 1 — planning Intelligence Layer (в процессе)

- **Документационный вход в Phase 4 зафиксирован.** Phase 3
  (Metadata Changes) закрыта окончательно; Phase 4 (Intelligence
  Layer) открыта как активная фаза. Кода в Step 1 не пишется:
  затронуты только `docs/architecture/`, корневой `README.md` и
  этот файл.
- **Создан `docs/architecture/phase-4-intelligence-plan.md`** —
  полный плановый документ Phase 4 в стиле phase-плана:
  - **Назначение фазы.** `mcp-intelligence-server` превращается из
    skeleton (только `ping`) в рабочий read-only intelligence layer
    поверх готовых read- (15 tools) и write- (23 tools) серверов.
    Не «магический reasoning», а набор осмысленных read-only
    инструментов: где используется объект, что затронет правка,
    какая последовательность безопаснее, что сломалось по журналу,
    какую подсказку дать пользователю, где подозрительные места.
  - **Целевой результат.** Собственный `runtime/` слой
    intelligence-server'а; public tools, покрывающие dependency
    analysis, impact analysis, troubleshooting, recommendations;
    все intelligence-tools read-only, никогда не запускают
    write-flow; cross-app import строго `intelligence → read` и
    `intelligence → write` (только pure / read-only helpers);
    `ToolResult` явно разделяет `confirmed` / `presumed` источники;
    Phase 1/2/3 контуры не деградируют; `dev-check` зелёный.
  - **Набор инструментов фазы — 16 tools, 4 группы.**
    - Группа A (dependency / structure):
      `analyze_object_dependencies`, `build_dependency_subgraph`,
      `find_references_to_object`, `find_module_method_usages`.
    - Группа B (change impact / pre-change):
      `estimate_change_impact`, `find_affected_forms`,
      `find_affected_modules`, `suggest_safe_change_order`.
    - Группа C (troubleshooting / diagnostics):
      `analyze_runtime_issue`, `analyze_event_log_patterns`,
      `diagnose_broken_form_binding`,
      `diagnose_missing_method_or_attribute`.
    - Группа D (recommendation / assistant):
      `suggest_fix_for_issue`, `suggest_metadata_patch_plan`,
      `summarize_configuration_risk`,
      `prepare_intelligence_report`.
    Для каждого tool'а зафиксировано назначение, слой
    реализации (read-side dump adapter / read-server tools /
    intelligence runtime / pure helpers `metadata_ops`) и MVP
    содержимое payload'а. Это план, а не декларация готового
    продукта; конкретные сигнатуры уточняются в Step 2.
  - **Guardrails фазы.** Intelligence-tools ничего не меняют
    (нет snapshot'ов, нет `run_write_flow`, нет audit). Read-only
    by construction. Cross-app import — только вперёд:
    `intelligence → read` и `intelligence → write` (read-only
    helpers); обратное направление запрещено, чтобы read/write
    остались независимыми и без циклов. Fail-closed при недостатке
    данных (никаких silent-default'ов). Каждый payload честно
    разделяет `confirmed` (прямые данные: dump substring, XML tag,
    event-log row) и `presumed` (эвристики). Рекомендации ≠
    авто-применение: `suggest_*` отдают `suggested_tools` —
    имена существующих public write-tool'ов с набросками
    аргументов, **запуск остаётся за вызывающим**.
    Производительность дешевле точности в MVP (substring,
    `rglob`, lightweight BSL-regex; AST/индексы/graph databases —
    за рамками Phase 4).
  - **Что не входит в Phase 4.** Fully autonomous self-healing,
    auto-apply fixes, production decision making (prod-block
    guardrails Phase 2/3 остаются), multi-agent orchestration,
    настоящий reasoning engine / ML-модели, product workflows
    Phase 5, замена stub'ов Phase 2/3
    (`apply_config_from_files`, `update_database_configuration`,
    `create_dump_snapshot`) на реальный `1cv8`-integration —
    параллельный follow-up.
  - **Критерии приёмки.** Phase 4 закрыта, когда: реализованы
    и зарегистрированы **не менее 4–5** public intelligence-tools,
    покрывающих хотя бы **две** группы из A / B / C / D;
    подтверждены **не менее 2–3** рабочих troubleshooting-сценариев;
    подтверждён **хотя бы один** end-to-end intelligence scenario
    (например, зависимости → impact → порядок правок →
    intelligence report); `dev-check` остаётся зелёным; read- /
    write-серверы (15 / 23 tools) не деградируют; каждый
    intelligence-tool маркирует `confirmed` vs `presumed`.
- **Создан `docs/architecture/phase-4-step-map.md`** — стартовая
  карта Phase 4 на 7 шагов:
  - **Step 1.** Intelligence operation contract / phase planning
    (текущий, документационный).
  - **Step 2.** Подготовка policy / config / contracts (если
    нужно). Возможный вариант: новый frozenset
    `_INTELLIGENCE_OPERATIONS` в `onec-policy-engine` с
    `reason_code="allowed_intelligence"`,
    `require_snapshots=False`. Альтернатива — явно зафиксировать,
    что intelligence не проходит policy-check (read-only, отдельный
    сервер) и policy не трогать. Backward compatibility Phase 2/3
    сохраняется.
  - **Step 3.** Internal analysis helper layer
    `apps/mcp-intelligence-server/src/mcp_intelligence_server/runtime/`:
    `models.py` (`IntelligenceRuntimeContext`), `context.py`
    (`build_runtime_context` поверх `check_environment_health`),
    `dump_scanner.py` (XML + BSL поиск поверх `read_dump_file` /
    `find_files_by_pattern` / `read_text_file`), `reference_finder.py`,
    `graph.py` (минимальный `DependencyGraph`). Public tools пока
    не появляются; registry intelligence-server по-прежнему
    `['ping']`.
  - **Step 4.** Первая волна public intelligence-tools (группа A):
    `find_references_to_object`, `analyze_object_dependencies`,
    `find_module_method_usages`, опционально
    `build_dependency_subgraph`. Cross-app import — только через
    `mcp_read_server.runtime` и pure helpers
    `mcp_write_server.runtime.metadata_ops`.
  - **Step 5.** Diagnostics tools (группа C):
    `analyze_runtime_issue`, `analyze_event_log_patterns`,
    `diagnose_broken_form_binding`,
    `diagnose_missing_method_or_attribute`. Опираются на
    `get_event_log`, `get_object_structure`, `get_form_structure`,
    `check_runtime_health`, `diagnose_connectivity_issue` из
    read-server и helpers Step 3. Каждый `ToolResult` явно
    разделяет `confirmed` / `presumed`.
  - **Step 6.** Impact / recommendation tools (группы B и D):
    `estimate_change_impact`, `find_affected_forms`,
    `find_affected_modules`, `suggest_safe_change_order`,
    `suggest_fix_for_issue`, `suggest_metadata_patch_plan`,
    `summarize_configuration_risk`,
    `prepare_intelligence_report`. `suggested_tools` ссылается
    **только на существующие** public-инструменты write-server
    (Phase 2/3).
  - **Step 7.** Final integration pass: один сквозной сценарий
    (`find_references_to_object` → `estimate_change_impact` →
    `suggest_safe_change_order` → `prepare_intelligence_report`)
    плюс 1–2 failure-path. Кода стараемся не трогать; разрешена
    минимальная точечная правка только при честной необходимости
    (как в Phase 2 Step 10 / Phase 3 Step 7). Phase 4 закрывается.
- **Корневой `README.md` обновлён.** В блоке «Текущий статус по
  фазам» строка `**Phase 4** — следующий этап.` заменена на
  развернутый абзац: Phase 4 — активная фаза разработки, цель —
  Intelligence Layer (read-only intelligence-tools поверх
  read/write слоёв; dependency / impact analysis, troubleshooting,
  рекомендации; read- и write-серверы не деградируют;
  intelligence-tools не выполняют write-операции и не принимают
  решений за пользователя). Phase 0–3 остались в «Закрытых
  фазах». Добавлен новый раздел «Активная фаза:» со ссылками на
  `phase-4-intelligence-plan.md` и `phase-4-step-map.md`.
- **Никакого кода в Step 1 не написано.** `apps/`, `packages/`,
  `scripts/`, `.github/`, `pyproject.toml`, стенды, `.claude.json`
  не затрагивались. Registry всех трёх серверов **не менялись**:
  `read=15`, `write=23`, `intelligence=['ping']`. `dev-check`
  не запускался — Step 1 чисто документационный.

### Phase 4 / Step 2 — policy / config / contracts для intelligence (завершён)

- **Архитектурное решение Step 2: intelligence-server сознательно
  не проходит через `onec-policy-engine`.** Выбран второй вариант
  из двух, зафиксированных в `phase-4-step-map.md`: вместо добавления
  новой категории `_INTELLIGENCE_OPERATIONS` с
  `reason_code="allowed_intelligence"` контракт зафиксирован как
  отсутствие write-policy роутинга для intelligence.
- **Почему именно этот вариант.**
  1. Phase 4 guardrail требует read-only by construction: intelligence
     никогда не меняет состояние, не запускает `run_write_flow`,
     не пишет audit. Поля `PolicyDecision` (`allow_write`,
     `require_snapshots`) для read-only операций бессодержательны.
  2. `check_write_allowed` семантически про **write**. Добавление
     `_INTELLIGENCE_OPERATIONS` расширило бы поверхность движка и
     форсировало бы преждевременное перечисление 16 intelligence
     operation names, которые реально через движок не авторизуются.
  3. Выбранный вариант зеркалит уже существующий паттерн
     `mcp-read-server`: read-side тоже не роутится через
     write-policy. Единая политика «read-only серверы не трогают
     write-policy» делает архитектуру однородной.
  4. Ветка `unknown_intent` в `_new_check` — бесплатная страховка:
     если intelligence-operation name когда-нибудь случайно попадёт
     в `WriteIntent` и пойдёт через `check_write_allowed`, движок
     честно откажет fail-closed, не придумывая ответ.
- **Что сделано в коде (минимально).**
  - `packages/onec-policy-engine/src/onec_policy_engine/engine.py`
    — **только расширен module docstring** новым абзацем про
    intelligence: явно зафиксировано, что Phase 4 intelligence-ops
    не роутятся через этот движок, и что `unknown_intent` branch
    служит free safety net. Логика `check_write_allowed`,
    `_legacy_check`, `_new_check` и все четыре frozenset'а
    (`_MUTATING_OPERATIONS`, `_NON_MUTATING_SUPPORT_OPERATIONS`,
    `_METADATA_MUTATING_OPERATIONS`, `_METADATA_SUPPORT_OPERATIONS`)
    **не тронуты** — backward compatibility Phase 2/3 полная.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__init__.py`
    — docstring пакета расширен разделом про Phase 4 контракт:
    read-only by construction; намеренно **не импортирует**
    `onec_policy_engine`; cross-app import идёт строго вперёд
    (`intelligence → read`, `intelligence → write` только через
    pure / read-only helpers). Код (экспорт `ToolResult`, `ping`,
    `list_tools`, `get_tool`) не менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/server.py`
    — docstring модуля расширен явной фиксацией: bootstrap не
    импортирует `onec_policy_engine`. Logика `REGISTERED_TOOLS`,
    `list_tools()`, `get_tool()` не менялась.
- **Что сделано в документации.**
  - `packages/onec-policy-engine/README.md` — добавлен раздел
    «Intelligence-операции (Phase 4) — не проходят через этот
    движок», описывающий принятое решение, его практический эффект
    и bidirectional mirror с intelligence-server README.
  - `apps/mcp-intelligence-server/README.md` — добавлен раздел
    «Read-only контракт Phase 4»: не пишет файлы, не проходит
    через `check_write_allowed`, allowed cross-app import только
    вперёд, fail-closed при недостатке данных. Блок «Чего здесь
    намеренно ещё нет» расширен указанием, что реальные
    intelligence-инструменты появятся в Step 3–6, а текущий шаг
    фиксирует только контракт.
- **`onec-config` не тронут.** Проверено: `EnvironmentConfig` уже
  содержит все поля, которые intelligence runtime ожидает
  использовать в Step 3+ (`name`, `base_id`, `base_path`,
  `publication_name`, `http_base_url`, `dump_path`,
  `timeout_seconds`, `allow_write`). Никаких полей «на будущее»
  не добавлено.
- **`scripts/dev/selfcheck.py` не тронут.** Legacy режим
  `check_write_allowed("production", True)` /
  `check_write_allowed("local-dev", False)` работает как прежде
  (`production_blocked`, `write_not_allowed`).
- **Registry всех трёх серверов не менялись.**
  - `read_server_tools` = 15 (не тронут);
  - `write_server_tools` = 23 (не тронут);
  - `intelligence_server_tools` = `['ping']` (не тронут).
- **Ручная проверка (4 сценария, все зелёные).**
  - **Scenario A — no policy import leak.** Просканированы все
    4 `.py`-файла в
    `apps/mcp-intelligence-server/src/mcp_intelligence_server/`
    на наличие строки-импорта `from onec_policy_engine`/`import
    onec_policy_engine`. Найдено: **0 реальных импортов**. Docstring-
    упоминания (`__init__.py`, `server.py`) — ожидаемые и нужны,
    т.к. именно они фиксируют контракт в коде.
  - **Scenario B — backward compatibility Phase 2/3.** 4 представителя
    + legacy: `apply_config_from_files →
    allowed_mutating/require_snapshots=True`;
    `check_write_preconditions → allowed_non_mutating/False`;
    `create_catalog → allowed_metadata_mutating/True`;
    `verify_attribute_exists → allowed_metadata_support/False`;
    legacy `("production", True) → production_blocked`;
    legacy `("local-dev", False) → write_not_allowed`. Все коды
    `reason_code` и флаги `require_snapshots` совпадают с
    Phase 3 / Step 7 baseline.
  - **Scenario C — free safety net для intelligence-op name в
    WriteIntent.** 7 имён из плана Phase 4 (`find_references_to_object`,
    `analyze_object_dependencies`, `find_module_method_usages`,
    `estimate_change_impact`, `analyze_runtime_issue`,
    `suggest_fix_for_issue`, `prepare_intelligence_report`) → все
    возвращают `allowed=False`, `reason_code=unknown_intent`.
    Штатный путь для intelligence — не сюда; но если случайно
    попадёт, движок fail-closed'ит.
  - **Scenario D — intelligence-server импортируется и работает.**
    `import mcp_intelligence_server` чистый; `ping()` вернул
    `ok=True`, `tool_name='ping'`; `list_tools() == ['ping']`.
    Докстринги и README не сломали runtime.
- **Dev-check после Step 2 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15, `write_server_tools` = 23,
  `intelligence_server_tools = ['ping']`, `selfcheck_status = ok`,
  `Dev check completed successfully.`.

### Phase 4 / Step 3 — internal analysis helper layer в `mcp-intelligence-server/runtime/` (в процессе)

- **Создан подпакет
  `apps/mcp-intelligence-server/src/mcp_intelligence_server/runtime/`**
  — аналог `mcp_read_server.runtime` и
  `mcp_write_server.runtime`, но под **read-only** intelligence
  сценарии. Это внутренний helper-слой, на котором будут стоять
  будущие public intelligence-tools Step 4–6. Public tools на этом
  шаге **не добавляются**; `REGISTERED_TOOLS` intelligence-server'а
  и `list_tools()` остаются равны `['ping']`.
- **Состав подпакета (6 файлов, все новые).**
  - `runtime/models.py` — `IntelligenceRuntimeContext(environment,
    health_results, health_codes, dump_root)`. Data snapshot
    окружения и его health-состояния для одного вызова
    intelligence-инструмента. `dump_root` всегда заполнен
    (`Path(environment.dump_path)`); существует ли он на диске —
    отражено в `health_codes` (напр. `dump_missing`), так что
    context остаётся конструируемым даже для сломанных окружений.
  - `runtime/context.py` — `build_runtime_context(environment)`
    собирает `check_environment_health(...) +
    summarize_health(...)` из `onec-health`, резолвит
    `dump_root`, на диск не пишет, `onec_policy_engine` не
    импортирует.
  - `runtime/dump_scanner.py` — тонкие intelligence-ориентированные
    обёртки поверх `mcp_read_server.runtime` (allowed cross-app
    import направление `intelligence → read`):
    `list_xml_files(dump_root)`, `list_bsl_files(dump_root)`,
    `list_files_by_extensions(dump_root, extensions)`,
    `read_utf8_text(path)`. Нужны, чтобы intelligence-helper'ы
    вызывали осмысленно-именованный API вместо generic read-server
    примитивов напрямую.
  - `runtime/reference_finder.py` — substring поиск по `*.xml` и
    `*.bsl` дампа. Public-функции: `find_references(dump_root,
    needle, *, extensions=None, max_matches=None)` возвращает
    `list[ReferenceMatch]` (frozen dataclass: `relative_path`
    POSIX-style + relative к `dump_root`, `source` ∈ `{xml, bsl}`,
    `line_number` 1-based, `preview` — strip'нутая + обрезанная до
    160 символов matching-строка); `count_references` —
    вспомогательный счётчик. Пустой `needle` fail-closed через
    `ValueError`. Отсутствующее совпадение — пустой список, не
    ошибка.
  - `runtime/graph.py` — минимальный каркас dependency-графа:
    `DependencyNode(name, kind=None)` и `DependencyEdge(from_node,
    to_node, kind=None)` — оба frozen; `DependencyGraph(nodes,
    edges, adjacency)` — обычный dataclass. Helpers: `empty_graph()`,
    идемпотентный `add_node(graph, name, *, kind=None)` (возвращает
    `True/False` — добавил ли), `add_edge(graph, from_node,
    to_node, *, kind=None)` (auto-creates endpoint nodes; duplicates
    в `edges` допустимы, adjacency — без дубликатов),
    `neighbors(graph, name)` — прямые преемники или `[]` для
    неизвестного имени. Это именно маленький честный фундамент;
    реальный subgraph-обход с ограничением глубины появится в
    Step 4+ в public tool `build_dependency_subgraph`.
  - `runtime/__init__.py` — явный `__all__` с 15 именами
    (`IntelligenceRuntimeContext`, `build_runtime_context`,
    `list_xml_files`, `list_bsl_files`, `list_files_by_extensions`,
    `read_utf8_text`, `ReferenceMatch`, `find_references`,
    `count_references`, `DependencyNode`, `DependencyEdge`,
    `DependencyGraph`, `empty_graph`, `add_node`, `add_edge`,
    `neighbors`). Docstring подпакета явно фиксирует
    read-only контракт и разрешённые направления cross-app import.
- **Никаких других файлов не создано**, никакие другие зоны не
  тронуты. Read- и write-серверы, `onec-config`, `onec-health`,
  `onec-policy-engine`, `scripts/dev/selfcheck.py`, `.github/`,
  `pyproject.toml` — без изменений.
- **`mcp-intelligence-server/README.md`** дополнен разделом
  «Internal runtime helper layer (Phase 4 / Step 3)»: состав
  подпакета, описание каждого файла, прямое указание, что это
  **не** public tools и registry не меняется. В блоке «Чего здесь
  намеренно ещё нет» уточнение, что public tools появляются в
  Step 4–6.
- **Ручная проверка (5 сценариев, все зелёные).** Временный
  скрипт `C:\Users\user\AppData\Local\Temp\phase4_step3_checks.py`
  материализует dump на `tempfile.TemporaryDirectory` (3 файла:
  `Catalogs/ТестовыйСправочник.xml`, `Reports/ОбычныйОтчёт.xml`,
  `CommonModules/TestModule/Ext/Module.bsl`) и проверяет:
  - **A.** `build_runtime_context(env)` на temp dump →
    `dump_root == tempdir`; 3 health-check в стабильном порядке
    (`dump_path_exists`, `http_gateway`, `search_index`);
    `health_codes == ['gateway_down']` (dump существует + bsl
    есть → `dump_missing`/`index_lock` отсутствуют; http_base_url
    заведомо нереагирующий → `gateway_down` честно ловится).
  - **B.** `dump_scanner` → `list_xml_files` находит обе
    `*.xml`-карточки, `list_bsl_files` находит `Module.bsl`,
    `list_files_by_extensions(..., ("xml", "bsl"))` возвращает 3
    файла в отсортированном порядке; `read_utf8_text` прочитал
    модуль — 235 байт, содержит `Процедура MCP_Test()` и
    `ТестовыйСправочник`.
  - **C.** `find_references(dump_root, "ТестовыйСправочник")` →
    **4 совпадения** на 3 относительных путях (1 в XML
    каталога — `<Name>`; 2 в BSL — комментарий и вызов
    `Справочники.ТестовыйСправочник.СоздатьЭлемент()`; 1 в XML
    отчёта — `<Reference>`). `sources == ['bsl', 'xml']`.
    `max_matches=2` честно обрывает скан на двух.
    `count_references` == 4. Пустой `needle` → `ValueError(
    "find_references requires a non-empty needle.")`. Несуществующая
    строка → `[] ` (не ошибка).
  - **D.** `empty_graph() → DependencyGraph(nodes=[], edges=[],
    adjacency={})`. `add_node` дважды с тем же именем: первый
    `True`, второй `False` (идемпотентность). `add_edge` от
    `Report.ОбычныйОтчёт` к `Catalog.ТестовыйСправочник` дважды +
    `add_edge` от `CommonModule.TestModule` (не созданного
    явно) к каталогу: `len(nodes)=3`, `len(edges)=3` (дубликат
    edge сохраняется), `adjacency` — без дубликатов target'ов.
    `neighbors(graph, "Report.ОбычныйОтчёт") ==
    ["Catalog.ТестовыйСправочник"]`; `neighbors(graph,
    "Unknown.Name") == []`.
  - **E.** `intelligence_server.list_tools() == ['ping']`;
    `ping().ok == True`. Registry intelligence-server не изменился.
- **Dev-check после Step 3 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools` = 23
  (не тронут), `intelligence_server_tools = ['ping']` (не тронут),
  `selfcheck_status = ok`, `Dev check completed successfully.`.

### Phase 4 / Step 4 — первая волна public intelligence-tools группы A (в процессе)

- **Intelligence-server впервые поднят выше skeleton.** Registry
  intelligence-server'а вырос с `['ping']` до
  **`['analyze_object_dependencies', 'find_module_method_usages',
  'find_references_to_object', 'ping']`** (4 инструмента, группа A
  покрыта). Read- и write-серверы не тронуты, их registry
  остались `read=15`, `write=23`.
- **Контрактные инварианты Phase 4 сохранены.**
  - все три новых public tool'а строго **read-only**: не пишут
    файлы, не создают snapshot'ов, не идут через `run_write_flow`,
    не пишут audit;
  - `mcp_intelligence_server` по-прежнему **не импортирует**
    `onec_policy_engine` (подтверждено grep'ом по 10 `.py`-файлам
    intelligence-server'а — 0 реальных импортов);
  - cross-app import идёт только через
    `mcp_read_server.runtime` и внутренний
    `mcp_intelligence_server.runtime` Step 3;
  - исключения из runtime-слоя (`PlatformError`, `ValueError`,
    `OSError`) перехватываются внутри public tool'а и
    конвертируются в `ToolResult(ok=False, ...)` — наружу не
    пробрасываются.
- **Единый failure-style.** `ok=False` **только** при реальной
  проблеме (пустой аргумент / dump-root недоступен / объект не
  найден в дампе). Пустой-но-валидный результат поиска — `ok=True`
  с пустым списком и message «No references found» / «No
  occurrences … found».
- **Payload discipline.** В каждом `ToolResult` confirmed-факты
  (подстрочные совпадения в конкретном файле; токены из
  XML-карточки) явно отделены от presumed-выводов (эвристическая
  классификация declaration / usage по шаблону; зависимости,
  извлечённые из BSL, где токен может быть в комментарии или
  строковом литерале). Никакого fake-smart анализа: эвристика
  честно помечена как presumed.
- **Public tools группы A (3 штуки).**
  - **`find_references_to_object(environment, object_name,
    max_matches=None)`** — substring-скан `*.xml` + `*.bsl` под
    `environment.dump_path` через
    `runtime.reference_finder.find_references`. Payload:
    `object_name`, `total_matches`, `confirmed_matches`
    (`relative_path`, `source`, `line_number`, `preview`),
    `confirmed_sources` (уникальные пути), `sources_used`
    (`dump_xml` / `dump_bsl` — булевы), `max_matches_applied`,
    `runtime.health_codes`. Пустой `object_name` → `ok=False`.
  - **`find_module_method_usages(environment, method_name,
    max_matches=None)`** — substring-скан **только `*.bsl`**.
    `confirmed_matches` — все находки; дополнительно
    эвристическая классификация в `presumed_declarations`
    (шаблон `^(Процедура|Функция|Procedure|Function)\s+<name>\s*\(`)
    и `presumed_usages` (всё остальное). `sources_used` →
    `dump_bsl` булев.
  - **`analyze_object_dependencies(environment, object_name)`** —
    локализует XML-карточку объекта (`*.xml` со stem'ом равным
    `simple_name`) и его собственные BSL-модули (путь содержит
    `simple_name` как сегмент). Извлекает known-prefix ссылки
    (`Справочник.`, `Документ.`, `ОбщийМодуль.`, `Catalog.`,
    `CommonModule.` и ещё ~25 прочих, Cyrillic + English форм)
    через regex. Self-references отфильтрованы. Split payload:
    `confirmed_dependencies` (из XML-карточки —
    структурный сигнал), `presumed_dependencies` (из BSL —
    substring/regex heuristic). Возвращает также минимальный
    `graph` (`nodes`, `edges`, `adjacency`) поверх
    `runtime.graph`. Если объект не найден нигде (no XML, no BSL)
    → `ok=False`, честный fail-closed.
- **Опциональный `build_dependency_subgraph` не регистрировался.**
  В ТЗ Step 4 указан как опциональный «если MVP укладывается без
  раздутия». Решение: не добавлять. Минимальный `graph`-объект
  (`nodes`/`edges`/`adjacency`) уже возвращается внутри
  `analyze_object_dependencies`; отдельный public façade с
  depth-traversal добавит алгоритмическую сложность без
  проверяемого benefit на Step 4. Это задача естественно закроется
  в Step 6 (`estimate_change_impact` / `find_affected_*`
  переиспользуют тот же runtime).
- **Что изменилось в коде.**
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/tools.py`
    — переписан: добавлены 3 новые public-функции + internal
    helpers (`_runtime_payload`, `_match_to_dict`, `_simple_name`,
    `_extract_prefixed_references`, `_fail`). `ping` сохранён
    как был. Константа `_KNOWN_PREFIXES` (Cyrillic + English форм,
    single + plural).
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/server.py`
    — `REGISTERED_TOOLS` теперь собирается из четырёх callables.
    Docstring модуля (Phase 4 contract, отсутствие импорта
    `onec_policy_engine`) не менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__init__.py`
    — `__all__` расширен тремя новыми именами и добавлены
    соответствующие re-export'ы. Phase 4 contract docstring не
    менялся.
- **Никаких изменений за пределами intelligence-server и README /
  PROJECT-STATUS.** `mcp-read-server`, `mcp-write-server`,
  `packages/**`, `scripts/**`, `.github/**`, `pyproject.toml`,
  корневой `README.md`, plan/step-map Phase 4 — не тронуты.
  `runtime/` подпакет Step 3 — без правок, ни одного нового файла.
- **`mcp-intelligence-server/README.md` переписан.** Раздел «Что
  сейчас внутри» теперь перечисляет четыре tool'а с сигнатурами.
  Добавлен раздел «Public tools группы A (Phase 4 / Step 4)» с
  фиксацией read-only контракта (не пишут, не идут через policy /
  write-flow / audit), единого failure-style, confirmed vs
  presumed discipline и подробным описанием каждого из трёх
  новых инструментов. Блок «Чего здесь намеренно ещё нет»
  приведён в соответствие: группы C / B / D — в Step 5–6;
  `build_dependency_subgraph` пока не отдельный tool; AST-парсинга
  нет (MVP substring + regex).
- **Ручная проверка (6 сценариев, все зелёные).** Временный
  скрипт `C:\Users\user\AppData\Local\Temp\phase4_step4_checks.py`
  материализует в `tempfile.TemporaryDirectory` связный mini-dump
  (Catalogs/Main.xml + Catalogs/Secondary.xml + Reports/UsesMain.xml
  + Catalogs/Main/Ext/ManagerModule.bsl + CommonModules/UtilModule/Ext/Module.bsl)
  с **настоящими** взаимными ссылками между Main и Secondary и
  вызовами `MCP_Test()`, и проверяет:
  - **A.** `find_references_to_object(env, "Main")` → `ok=True`,
    `total_matches=6` на 4 относительных путях (Catalogs/Main.xml,
    Catalogs/Main/Ext/ManagerModule.bsl,
    CommonModules/UtilModule/Ext/Module.bsl, Reports/UsesMain.xml);
    `sources_used={dump_xml:True, dump_bsl:True}`; повторный
    вызов с `max_matches=2` → `total_matches=2`,
    `max_matches_applied=True`.
  - **B.** `find_module_method_usages(env, "MCP_Test")` →
    `ok=True`, `total_matches=3`; `presumed_declarations=1`,
    `presumed_usages=2`; preview declaration содержит
    «Процедура MCP_Test». `max_matches=1` → `total_matches=1`,
    `max_matches_applied=True`.
  - **C.** `analyze_object_dependencies(env, "Main")` → `ok=True`;
    `confirmed_sources=['Catalogs/Main.xml']`;
    `presumed_sources=['Catalogs/Main/Ext/ManagerModule.bsl']`;
    `confirmed_dependencies` содержит `Справочник.Secondary` и
    `Перечисление.ЕдиницыИзмерения`, self-ref `Справочник.Main`
    исключён; `presumed_dependencies` содержит `Справочники.Secondary`,
    `ОбщийМодуль.LegacyUtil`, `Перечисления.ЕдиницыИзмерения`;
    `graph.nodes=6`, `graph.edges=5`, `adjacency['Main']` непустой.
  - **D.** Failure-path'ы, единый стиль: несуществующая строка в
    find_references_to_object → `ok=True, total_matches=0`;
    несуществующий метод → `ok=True, total_matches=0`;
    несуществующий объект в analyze_object_dependencies →
    `ok=False, "not found in dump"`; пустой `object_name` /
    `method_name` → `ok=False`; недоступный dump_root →
    `ok=False, "Dump root does not exist: ..."`. Ни одного
    исключения наружу.
  - **E.** `mis.list_tools() == ['analyze_object_dependencies',
    'find_module_method_usages', 'find_references_to_object',
    'ping']`; `get_tool('find_references_to_object')` возвращает
    callable, `get_tool('nonexistent')` → `None`.
  - **F.** grep `^\s*(from|import)\s+onec_policy_engine\b` по
    всем 10 `.py`-файлам
    `apps/mcp-intelligence-server/src/**/*.py` → **0 реальных
    импортов**. Phase 4 cross-app import контракт сохранён и после
    Step 4.
- **Dev-check после Step 4 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools` = 23
  (не тронут), **`intelligence_server_tools =
  ['analyze_object_dependencies', 'find_module_method_usages',
  'find_references_to_object', 'ping']`**, `selfcheck_status = ok`,
  `Dev check completed successfully.`.

### Phase 4 / Step 5 — diagnostics / troubleshooting tools группы C (завершён)

- **Intelligence-server покрыл вторую группу Phase 4.** Registry
  вырос с 4 (`ping` + 3 tool'а группы A) до **8** tool'ов:
  `['analyze_event_log_patterns', 'analyze_object_dependencies',
  'analyze_runtime_issue', 'diagnose_broken_form_binding',
  'diagnose_missing_method_or_attribute', 'find_module_method_usages',
  'find_references_to_object', 'ping']`. Критерий приёмки фазы
  «≥ 4–5 public tools, покрывающих ≥ 2 группы из A/B/C/D»
  удовлетворён по счёту и охвату групп.
- **Контрактные инварианты Phase 4 сохранены.**
  - все четыре новых Step 5 tool'а строго **read-only**: не пишут,
    не идут через `run_write_flow`, не пишут audit, не создают
    snapshot'ов;
  - `mcp_intelligence_server` по-прежнему **не импортирует**
    `onec_policy_engine` (подтверждено grep'ом по 10 `.py`-файлам
    intelligence-server'а — 0 реальных импортов; docstring-упоминания
    остаются ожидаемыми);
  - cross-app import только вперёд: `intelligence → read`
    (`mcp_read_server.tools.{check_runtime_health,
    diagnose_connectivity_issue, get_event_log, get_form_structure}`)
    и `intelligence → write` через **pure read-only helper**
    (`mcp_write_server.runtime.metadata_ops.module_contains_method`
    — чистая substring+regex функция над текстом модуля, без
    побочных эффектов);
  - исключения перехватываются и превращаются в `ToolResult(ok=False, ...)`
    либо в findings — наружу не пробрасываются.
- **Единый failure-style сохранён с Step 4.**
  - `ok=True` — анализ завершён (findings могут быть пустыми).
  - `ok=False` — анализ провести не удалось (некорректный вход,
    критическая зависимость вернула ошибку, dump/модуль недоступен
    там, где критически нужен).
  - Для `analyze_event_log_patterns` и `diagnose_broken_form_binding`
    ошибка read-server'а пробрасывается как `ok=False` с message
    вида `read.<tool> failed: <original>`.
  - Для `analyze_runtime_issue` фиксация найденных health-кодов
    штатно идёт через `ok=True` — сам по себе runtime aggregator
    свою работу сделал.
- **Payload discipline — `confirmed_findings` / `presumed_findings`
  / `recommended_checks` / `sources_used`.**
  - `confirmed_findings` — факты, завязанные на конкретный артефакт
    (health-код из `check_runtime_health`, verdict
    `method_exists`/`method_missing` над реально прочитанным
    модулем, handler с явной привязкой, аттрибут в XML-карточке).
  - `presumed_findings` — эвристические объяснения: probable cause,
    pattern-метка (`error_spike`, `handler_method_missing`,
    `module_file_missing`, `attribute_missing` …).
  - `recommended_checks` — короткие next-step подсказки.
  - `sources_used` — список строковых маркеров использованных
    зависимостей (`read.check_runtime_health`,
    `read.get_event_log`, `dump_scanner.read_utf8_text`,
    `write_runtime.metadata_ops.module_contains_method`,
    `dump_xml:<path>`). Это честная трассируемая цепочка без
    скрытого reasoning.
- **Public tools группы C (4 штуки).**
  - **`analyze_runtime_issue(environment)`** — high-level
    aggregator поверх `read.check_runtime_health` +
    `read.diagnose_connectivity_issue` + intelligence runtime Step 3.
    Каждый non-`ok` health-код (`gateway_down` / `dump_missing`
    / `index_lock`) превращается в `confirmed_findings` с
    детерминированным hint; rule-based вывод
    `diagnose_connectivity_issue` идёт в `presumed_findings`; raw
    per-check snapshot — в `health_checks`; `recommended_checks`
    — под каждый код. `ok=False` только если `environment is None`
    или внутренняя ошибка.
  - **`analyze_event_log_patterns(environment, period_start=None,
    period_end=None, level=None, user=None)`** — делегирует в
    `read.get_event_log` (фильтры пробрасываются verbatim и реально
    доходят до endpoint'а). Полученные entries подсчитываются
    `collections.Counter`: `total_entries`, top-N `top_levels` /
    `top_users` / `top_events`, до 5 `error_samples`. Если
    error/critical entries ≥ 2 — в `presumed_findings` добавляется
    pattern `error_spike`. Пустой лог → `ok=True` с пустыми
    findings. Если read-server вернул `ok=False` — пропускаем с
    тем же message (`read.get_event_log failed: ...`).
  - **`diagnose_broken_form_binding(environment, object_name,
    form_name=None)`** — `read.get_form_structure` (live HTTP) +
    pure helper `module_contains_method` из write-runtime.
    Ожидаемая форма payload'а read-server'а:
    `{elements, handlers:[{event, handler_method}],
    module_relative_path}`. `confirmed_findings` содержит коды
    `form_has_no_elements`, `form_has_no_handlers`,
    `handler_method_missing`, `module_not_readable`; к каждому
    `presumed_findings` добавляет probable-cause narrative.
    `ok=False`, если endpoint/форма недоступны; во всех других
    случаях `ok=True` — даже когда найдены все три типа symptom'ов.
  - **`diagnose_missing_method_or_attribute(environment, *,
    object_name=None, module_relative_path=None, method_name=None,
    attribute_name=None)`** — два комбинируемых режима:
    **method_mode** (`module_relative_path` + `method_name`) —
    модуль читается из дампа, verdict через
    `module_contains_method`; **attribute_mode** (`object_name` +
    `attribute_name`) — XML-карточка ищется по stem-совпадению,
    regex поверх типовых `<Attribute>` форм
    (`<Attribute name="...">` и вложенный `<Name>...`). Verdicts:
    `method_exists` / `method_missing` / `module_file_missing` /
    `attribute_exists` / `attribute_missing` / `xml_card_missing`.
    `ok=False` только если не передан ни один валидный режим или
    dump-root отсутствует; в остальных случаях `ok=True` с
    verdict'ом в `confirmed_findings` и probable-cause narrative в
    `presumed_findings` (только для *missing*-verdict'ов).
- **Что изменилось в коде.**
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/tools.py`
    — расширен: новый блок cross-app import'ов (`mcp_read_server.tools`,
    `mcp_write_server.runtime.metadata_ops.module_contains_method`);
    добавлены helper'ы (`_HEALTH_CODE_HINTS`, `_extract_event_entries`,
    `_top_n`, `_ATTRIBUTE_TAG_PATTERNS`, `_xml_declares_attribute`);
    добавлены четыре новые public-функции группы C. Код группы A
    (Step 4) не менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/server.py`
    — `REGISTERED_TOOLS` теперь из 8 callables. Docstring не
    менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__init__.py`
    — `__all__` расширен четырьмя именами; добавлены re-export'ы.
    Phase 4 contract docstring не менялся.
- **Никаких изменений за пределами intelligence-server.**
  `mcp-read-server`, `mcp-write-server`, `packages/**`, `scripts/**`,
  `.github/**`, `pyproject.toml`, корневой `README.md`,
  `phase-4-intelligence-plan.md`, `phase-4-step-map.md`, `runtime/`
  подпакет intelligence-server'а (Step 3) — не тронуты.
- **`mcp-intelligence-server/README.md`** обновлён:
  - блок «Что сейчас внутри» теперь перечисляет **8** tool'ов в
    двух группах (A — Step 4, C — Step 5);
  - блок «Чего намеренно ещё нет» обновлён: группы B/D появятся в
    Step 6; MVP substring+regex остаётся без AST;
  - добавлен раздел «Public tools группы C (Phase 4 / Step 5)» с
    read-only контрактом, единым failure-style, описанием
    confirmed/presumed discipline и подробной спецификацией
    каждого из четырёх tool'ов.
- **Ручная проверка (7 сценариев, все зелёные).** Временный скрипт
  `C:\Users\user\AppData\Local\Temp\phase4_step5_checks.py` поднимает
  **in-process `ThreadingMixIn`/`TCPServer`** на `127.0.0.1:<rand>`
  (без сетевых вызовов к реальному стенду, без Apache, без `1cv8`)
  и материализует temp-dump в `tempfile.TemporaryDirectory`.
  Эндпоинт честно отдаёт event-log и form/structure, `last_event_log_query`
  фиксирует query-string, пришедшую на endpoint. Сценарии:
  - **A. `analyze_runtime_issue(dead_env)`** (dump жив, http мёртв) →
    `ok=True`, `health_codes` включает `gateway_down`;
    `confirmed_count=1` (gateway_down с hint), `presumed_count=1`
    (вывод `diagnose_connectivity_issue`), `health_checks=3` raw
    row; `sources_used = {read.check_runtime_health,
    read.diagnose_connectivity_issue}`.
  - **B. `analyze_event_log_patterns(env, period_start='2026-04-24',
    level='Error', user='alice')`** при 3 pre-loaded entries:
    `ok=True`, `total_entries=3`, `top_events` содержит
    `ConnectionLost` (2 повторa), `error_samples=2`,
    `presumed_findings=['error_spike']`; фильтры доходят до
    endpoint'а (`start=['2026-04-24'], level=['Error'],
    user=['alice']`) и эхо-отражаются в payload. Пустой лог →
    `ok=True`, `presumed_findings=[]`.
  - **C. `diagnose_broken_form_binding(env, 'Catalog.Main',
    'ФормаСписка')`** с handlers
    `[OnClick→MissingHandler, OnOpen→ExistingHandler]` и модулем,
    который содержит только `ExistingHandler` и `OtherMethod`:
    `ok=True`, `confirmed_findings` содержит
    `handler_method_missing` именно для `MissingHandler`,
    `ExistingHandler` не помечен; `sources_used` включает
    `read.get_form_structure` + `dump_scanner.read_utf8_text` +
    `write_runtime.metadata_ops.module_contains_method`.
  - **D. `diagnose_missing_method_or_attribute`** — пять суб-случаев:
    method positive (`method_exists`, presumed пустой), method
    negative (`method_missing` + probable cause), attribute positive
    (`attribute_exists` для `Main` + `Жанр`), attribute negative
    (`attribute_missing` + probable cause), combined mode
    (method_missing + attribute_exists в одном ответе).
  - **E. failure path (7 подсценариев, единый стиль):**
    пустой `object_name` → `ok=False`; ни один mode не передан →
    `ok=False, "Provide..."`; dead endpoint в
    `analyze_event_log_patterns` → `ok=False, sources_used=[read.get_event_log]`;
    dead endpoint в `diagnose_broken_form_binding` → `ok=False`;
    `environment is None` в `analyze_runtime_issue` → `ok=False,
    "environment is missing"`; несуществующий dump_root в
    `diagnose_missing_method_or_attribute` → `ok=False, "Dump root
    does not exist: ..."`; отсутствующий модульный файл
    (`Catalogs/Ghost/Ext/Module.bsl`) → `ok=True` с
    `confirmed_findings=[{code: module_file_missing, ...}]` —
    finding, не ошибка инструмента. Ни одного исключения наружу.
  - **F. registry invariant:** `mis.list_tools() == ['analyze_event_log_patterns',
    'analyze_object_dependencies', 'analyze_runtime_issue',
    'diagnose_broken_form_binding', 'diagnose_missing_method_or_attribute',
    'find_module_method_usages', 'find_references_to_object', 'ping']`;
    `ping()` работает; `get_tool('analyze_runtime_issue')` возвращает
    функцию; `get_tool('nonexistent')` → `None`.
  - **G. cross-app import контракт:** grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/mcp-intelligence-server/src/**/*.py` (10 файлов) →
    **0 реальных импортов**.
- **Dev-check после Step 5 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools` = 23
  (не тронут), **`intelligence_server_tools` — 8 tool'ов**,
  `selfcheck_status = ok`, `Dev check completed successfully.`.

### Phase 4 / Step 6 — impact / recommendation tools группы B и D (завершён)

- **Intelligence-server покрыл группы B и D Phase 4.** Registry
  вырос с 8 (`ping` + 3 группа A + 4 группа C) до **16** tool'ов.
  Полный отсортированный список:
  `['analyze_event_log_patterns', 'analyze_object_dependencies',
  'analyze_runtime_issue', 'diagnose_broken_form_binding',
  'diagnose_missing_method_or_attribute', 'estimate_change_impact',
  'find_affected_forms', 'find_affected_modules',
  'find_module_method_usages', 'find_references_to_object', 'ping',
  'prepare_intelligence_report', 'suggest_fix_for_issue',
  'suggest_metadata_patch_plan', 'suggest_safe_change_order',
  'summarize_configuration_risk']`. Покрытие групп Phase 4 теперь
  полное: A (3) + B (4) + C (4) + D (4) + `ping` = 16.
- **Контрактные инварианты Phase 4 сохранены.**
  - все восемь новых Step 6 tool'ов строго **read-only**: не пишут
    файлы, не идут через `run_write_flow`, не пишут audit, не
    создают snapshot'ов;
  - `mcp_intelligence_server` по-прежнему **не импортирует**
    `onec_policy_engine` (подтверждено grep'ом
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/mcp-intelligence-server/src/**/*.py` — 0 реальных импортов);
  - cross-app import только вперёд: `intelligence → read` (для
    Step 6 переиспользуется ровно тот же набор, что в Step 5),
    `intelligence → write` исключительно через pure read-only
    helper `module_contains_method` (не активирован новыми
    Step 6 tool'ами напрямую — они опираются на runtime Step 3 и
    public tools Step 4/5);
  - исключения перехватываются и превращаются в `ToolResult(ok=False, ...)`
    либо в findings — наружу не пробрасываются.
- **Единый failure-style сохранён с Step 4/5.**
  - `ok=True` — анализ/рекомендация выполнены (findings могут быть
    пустыми; «ничего не нашли» — валидный результат, а не ошибка).
  - `ok=False` — инструмент не смог отработать (пустой обязательный
    аргумент, dump-root отсутствует там, где он критически нужен,
    неизвестный `issue_code`).
  - `suggest_metadata_patch_plan` для unsupported-kind / unknown-kind
    / deletion-goal возвращает `ok=True` с честным
    `presumed_findings` объяснением и пустым
    `suggested_write_tools` — это рекомендация, а не отказ;
    делать это `ok=False` было бы неискренне.
- **Payload discipline — `confirmed_findings` / `presumed_findings`
  / `recommended_checks` / `suggested_tools` /
  `suggested_write_tools` / `recommended_sequence` /
  `sources_used`.**
  - `confirmed_findings` — факты из dump-сканов (точные счётчики
    ссылок, найденные XML/BSL пути, `health_codes`),
    либо явные входные параметры в plan/recipe инструментах.
  - `presumed_findings` — эвристики (impact band, weak form
    signals, probable causes, объяснение почему план пустой).
  - `suggested_tools` / `suggested_write_tools` — **только реальные
    имена** уже зарегистрированных public-tool'ов. Ни одного
    придуманного имени; будущие capability помечаются как
    отсутствующие через `presumed_findings` (как делает
    `suggest_metadata_patch_plan` для `document` /
    `information_register` / `role` / `report` /
    `data_processor`).
- **Public tools группы B (4 штуки).**
  - **`estimate_change_impact(environment, object_name)`** —
    компактная оценка радиуса. Использует `find_references` и
    `list_xml_files/list_bsl_files` из runtime Step 3.
    `confirmed_findings` — счётчики `reference_count`,
    `xml_references`, `bsl_references`, плюс `own_xml_cards` /
    `own_bsl_modules` (как в `analyze_object_dependencies`) и
    `referenced_paths`. `presumed_findings` — детерминированный
    `impact_level` band (none/low/medium/high от пороговых
    значений 0/5/20), плюс `module_impact_possible` если есть BSL
    hits и `form_impact_possible` если есть form-like пути.
    `suggested_tools` указывает на `find_references_to_object`,
    `analyze_object_dependencies`, `find_affected_forms`,
    `find_affected_modules`. Empty / not-found остаётся
    `ok=True` с честным «0 references».
  - **`find_affected_forms(environment, object_name)`** —
    `find_references` + path-эвристика `_is_form_path`
    (наличие сегмента `Forms`, либо `form` / `форма` в stem).
    Совпадения, попадающие в форму-подобный путь, идут в
    `confirmed_findings`; остальные — в `presumed_findings` с
    pattern `weak_form_signal`. Это MVP: substring + path
    inspection, не XML-парсер. Сильные хиты предполагают
    follow-up через `diagnose_broken_form_binding`.
  - **`find_affected_modules(environment, object_name)`** —
    `find_references`, разбивка по `source`. `*.bsl` matches
    идут в `confirmed_findings` + агрегируются в
    `module_summary` (per-module `match_count`, отсортированный
    по убыванию). `*.xml` matches идут в `presumed_findings` с
    pattern `module_signal_via_xml` (XML может косвенно описывать
    module-level linkage). `suggested_tools`:
    `find_module_method_usages`, `find_references_to_object`.
  - **`suggest_safe_change_order(environment, object_name)`** —
    рекомендательный orchestrator. Дёргает свои же
    `analyze_object_dependencies` и `estimate_change_impact`
    (без побочных эффектов — они read-only) для сбора
    `object_found_in_dump`, `confirmed_dependency_count`,
    `presumed_dependency_count`, `impact_level`. Возвращает
    фиксированный 6-шаговый `recommended_sequence`:
    (1) read-baseline (`get_object_structure`), (2) impact /
    dependency сканы (intelligence + read), (3) preflight
    snapshots (`check_write_preconditions`,
    `create_backup_snapshot`, `create_dump_snapshot`),
    (4) метадата-правка (`create_catalog`,
    `add_catalog_attribute`, `add_document_attribute`,
    `create_managed_form`, `add_form_element`,
    `append_module_method`, `replace_module_method_body`),
    (5) verification (`verify_*`, `diff_dump_fragment`,
    `get_form_structure`), (6) audit/rollback hint
    (`describe_last_write_operation`, `prepare_rollback_hint`).
    `presumed_findings` адаптируется: `cascade_risk` если есть
    зависимости, `object_not_in_dump` если объект не нашли,
    `high_blast_radius` для `impact_level=high`.
- **Public tools группы D (4 штуки).**
  - **`suggest_fix_for_issue(environment, issue_code,
    context_data=None)`** — rule-based mapping
    `_ISSUE_FIX_RULES` (11 codes: `gateway_down`, `dump_missing`,
    `index_lock`, `form_has_no_elements`, `form_has_no_handlers`,
    `handler_method_missing`, `method_missing`,
    `module_file_missing`, `attribute_missing`, `xml_card_missing`,
    `error_spike`). Каждый rule содержит `probable_cause` →
    `presumed_findings`, упорядоченные `steps` →
    `recommended_checks`, `suggested_tools` /
    `suggested_write_tools` — **только реальные** имена. Unknown
    `issue_code` → `ok=False` с message «Unknown issue_code …
    Known codes: [...]» — fail-closed (выбран один стиль и
    выдержан). `context_data` пробрасывается verbatim в
    `confirmed_findings` (MVP не параметризует recipe по
    контексту).
  - **`suggest_metadata_patch_plan(environment, target_kind,
    target_name, change_goal)`** — table-driven plan generator,
    использующий **только** реальные write-server tools.
    `_PATCH_PLAN_RECIPES` покрывает 8 видов: `catalog`,
    `common_module`, `catalog_attribute`, `document_attribute`,
    `managed_form`, `form_element`, `module_method`,
    `module_method_body`. Каждый recipe — упорядоченный список
    write-tool'ов: preconditions → backup → dump snapshot →
    metadata mutation → (опц.) `update_database_configuration`
    → verify. `_PATCH_PLAN_UNSUPPORTED` честно перечисляет
    target_kind'ы, для которых Phase 2/3 write-server **не
    имеет** create-tool (`document`, `information_register`,
    `role`, `report`, `data_processor`) — план возвращается
    пустой с pattern `kind_unsupported` в `presumed_findings`.
    Ключевые слова удаления (`delete`, `remove`, `drop`,
    `удалить`, `удалять`, `убрать`) в `change_goal` дают pattern
    `deletion_not_supported`. Unknown kind → `unknown_kind`.
    `_step_description(...)` подтягивает короткое объяснение
    каждого write-tool из `_WRITE_TOOL_DESCRIPTIONS`. Никаких
    выдуманных tool-имён.
  - **`summarize_configuration_risk(environment, object_name=None)`**
    — короткое rule-based резюме. Глобально (без `object_name`)
    риск задаёт `runtime.health_codes`: `dump_missing` → high,
    `gateway_down` или `index_lock` → medium, иначе low.
    Пер-объект также делает `find_references`, добавляет
    `reference_count` в `confirmed_findings`; > 20 ссылок →
    medium, ≤ 20 — low. `object_not_referenced` поднимается в
    `presumed_findings`, если объект указан, но 0 хитов —
    «либо изолированный, либо misspelled». Никаких категоричных
    утверждений — только pattern-based.
  - **`prepare_intelligence_report(environment, subject,
    include_tools=None)`** — read-only orchestrator.
    Whitelisted whitelist `_REPORT_KNOWN_TOOLS` (9 имён, все —
    public intelligence-tool'ы из этого же модуля). Дефолтный
    набор `_REPORT_DEFAULT_INCLUDE` =
    `(analyze_runtime_issue, analyze_object_dependencies,
    estimate_change_impact, summarize_configuration_risk)`.
    `subject` обязателен (пустой → `ok=False`); по нему
    параметризуются `analyze_object_dependencies` и аналоги
    через таблицу режимов (`no_subject` /
    `subject_as_object_name` / `subject_as_method_name` /
    `subject_as_object_name_optional`). Имена вне whitelist
    падают в `skipped_unknown_tools`, не теряются молча. Каждый
    sub-tool оборачивается `try / except Exception` —
    исключения превращаются в `sections[name]={ok:False,
    message,...}`, наружу никогда не пробрасываются. Aggregate
    включает `confirmed_findings`, `presumed_findings`,
    `recommended_checks`, `suggested_tools` (set, отсортирован),
    каждый item помечен своим `tool` для трассируемости.
- **Что изменилось в коде.**
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/tools.py`
    — расширен: добавлены private helper'ы (`_impact_level`,
    `_is_form_path`, `_step_description`, `_invoke_report_tool`,
    rule-таблицы `_ISSUE_FIX_RULES`, `_PATCH_PLAN_RECIPES`,
    `_PATCH_PLAN_UNSUPPORTED`, `_DELETION_KEYWORDS`,
    `_WRITE_TOOL_DESCRIPTIONS`, `_REPORT_KNOWN_TOOLS`,
    `_REPORT_DEFAULT_INCLUDE`); добавлены восемь новых
    public-функций групп B и D. Код групп A (Step 4) и C
    (Step 5) не менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/server.py`
    — `REGISTERED_TOOLS` теперь из 16 callables; список
    импортов расширен восемью новыми именами. Docstring не
    менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__init__.py`
    — `__all__` расширен восемью именами; добавлены
    re-export'ы; package-level docstring обновлён описанием
    публичной поверхности на конец Step 6 (16 tools, 4 группы).
- **Никаких изменений за пределами intelligence-server.**
  `mcp-read-server`, `mcp-write-server`, `packages/**`, `scripts/**`,
  `.github/**`, `pyproject.toml`, корневой `README.md`,
  `phase-4-intelligence-plan.md`, `phase-4-step-map.md`, `runtime/`
  подпакет intelligence-server'а (Step 3) — не тронуты. Ни одного
  нового файла в проекте: всё уложено в существующие модули.
- **`mcp-intelligence-server/README.md`** обновлён:
  - блок «Что сейчас внутри» теперь перечисляет **16** tool'ов
    в четырёх группах (A — Step 4, C — Step 5, B и D — Step 6);
  - блок «Чего намеренно ещё нет» обновлён: группы B/D больше
    не упоминаются как ожидаемые в Step 6 — они теперь часть
    публичной поверхности; оставлены MVP-honesty-заметки про
    отсутствие AST-парсера и ML-кластеризации;
  - добавлен раздел «Public tools группы B (Phase 4 / Step 6)»
    с подробной спецификацией impact/affected/safe-order
    инструментов;
  - добавлен раздел «Public tools группы D (Phase 4 / Step 6)»
    с подробной спецификацией fix/plan/risk/report
    инструментов и явной фиксацией, что `suggested_tools` /
    `suggested_write_tools` ссылаются исключительно на уже
    существующие public-имена.
- **Ручная проверка (11 сценариев, все зелёные).** Временный
  скрипт
  `C:\Users\user\AppData\Local\Temp\intelligence_step6_check.py`
  материализует синтетический dump в `tempfile.mkdtemp()`
  (`Catalogs/Primary/Primary.xml`,
  `Catalogs/Primary/Forms/ItemForm/Form.xml`,
  `Catalogs/Primary/Ext/Module.bsl`) и проходит:
  - **A. registry invariant.** `mis.list_tools()` возвращает
    ровно 16 имён (см. список выше); `tools == sorted(tools)`
    (стабильный алфавитный порядок); `get_tool('estimate_change_impact')
    is mis.estimate_change_impact`; `get_tool('nonexistent') is None`.
  - **B. `estimate_change_impact`.** «Primary» → `ok=True`,
    `reference_count=4`, `level=low`, 3 presumed findings
    (impact_estimate + module_impact_possible + form_impact_possible).
    «GhostObject» → `ok=True`, 0 ссылок, `level=none`,
    1 presumed (impact_estimate). Empty → `ok=False`. Bad dump
    → `ok=False`.
  - **C. `find_affected_forms`.** «Primary» → `ok=True`,
    1 confirmed (Forms/ItemForm/Form.xml), 3 presumed (XML/BSL
    вне form-пути). «Catalog.Secondary» → `ok=True`,
    0 confirmed, 1 presumed — only-presumed path.
  - **D. `find_affected_modules`.** «Primary» → `ok=True`,
    1 модуль (`Catalogs/Primary/Ext/Module.bsl`), 1 BSL match,
    3 XML signals.
  - **E. `suggest_safe_change_order`.** «Primary» → 6 шагов,
    `impact=low`, `suggested_write_tools` содержит 17 уникальных
    реальных имён write-server'а (`add_catalog_attribute`, …,
    `verify_object_exists`). «GhostObject» (не в дампе) →
    тоже `ok=True`, 6 шагов, `presumed_findings` содержит
    `object_not_in_dump` — sequence отдаётся как generic.
  - **F. `suggest_fix_for_issue`.** Известный
    `handler_method_missing` → `ok=True`, 3 step recipe,
    `suggested_write_tools=[append_module_method,
    verify_module_contains]`. Известный `error_spike` →
    `ok=True`, write-tools пуст. Неизвестный
    `totally_unknown_code` → `ok=False` с message «Unknown
    issue_code … Known codes: [...]» (fail-closed, как
    зафиксировано в ТЗ). Empty → `ok=False`.
  - **G. `suggest_metadata_patch_plan`.** Поддерживаемая задача
    `catalog/create new catalog` → `ok=True`, 6 write-tool
    шагов (`check_write_preconditions` …
    `verify_object_exists`). `module_method/add method` →
    `ok=True`, 5 шагов. Unsupported `document/create document`
    → `ok=True`, пустой план, `presumed_findings=[
    {pattern: kind_unsupported, ...}]`. Unknown
    `weird_thing/do something` → `unknown_kind`. Deletion
    `catalog/delete it` → `deletion_not_supported`. Empty kind
    / empty name → `ok=False`.
  - **H. `summarize_configuration_risk`.** Глобальный режим
    при `gateway_down` (live HTTP в тесте недоступен) →
    `ok=True, risk_level=medium`. Пер-объект «Primary» при том
    же health → `medium` (gateway-rule имеет приоритет, как
    задокументировано). Пер-объект «GhostObject» → тоже
    `medium`, но добавлен `presumed_findings` с
    `object_not_referenced`. Bad dump (`dump_missing` в
    health_codes) → `risk_level=high` глобально и пер-объект.
  - **I. `prepare_intelligence_report`.** Default include
    `(analyze_runtime_issue, analyze_object_dependencies,
    estimate_change_impact, summarize_configuration_risk)` →
    `ok=True`, 4 sections, ни одного skipped. Whitelist
    `[analyze_object_dependencies, find_affected_forms,
    wat_unknown]` → `ok=True`, 2 sections,
    `skipped_unknown_tools=['wat_unknown']`. Empty subject →
    `ok=False`. Bad dump → всё ещё `ok=True`: каждая sub-tool
    отдельно репортит свою ошибку через свой section, наружу
    исключений не выходит.
  - **J. failure-style.** Проверены все обязательные fail-paths
    выше; ни одного исключения наружу — все обработаны
    `ToolResult(ok=False, ...)` или превращены в findings.
  - **K. cross-app import контракт:** grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/mcp-intelligence-server/src/**/*.py` →
    **0 реальных импортов** (assert в скрипте).
- **Известные MVP-компромиссы Step 6 (зафиксированы честно).**
  - `find_affected_forms` и `find_affected_modules` —
    substring + path-heuristic, не XML/BSL парсер. Это
    осознанное MVP-решение (см. ТЗ: «Никакого AST-парсера»).
  - `suggest_safe_change_order` отдаёт фиксированный 6-шаговый
    шаблон, не настоящий topo-sort по графу зависимостей.
    Решение принимается каллером, какой именно
    `suggested_write_tool` из шага 4 применять.
  - `summarize_configuration_risk` — порог `> 20` references
    → medium и `dump_missing` → high — это rule, не модель.
    Это поведение явно перечислено в docstring и в README.
  - `prepare_intelligence_report` — orchestration по
    whitelisted списку, без условной маршрутизации. Если
    sub-tool вернул `ok=False` (например, dead HTTP в
    `analyze_runtime_issue`), report остаётся `ok=True`, но
    содержимое соответствующей section — `ok=False` со своим
    сообщением. Это сознательное решение: report должен
    собрать всё что смог, а не падать при первой деградации.
- **Dev-check после Step 6 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools` = 23
  (не тронут), **`intelligence_server_tools` — 16 tool'ов**,
  `selfcheck_status = ok`, `Dev check completed successfully.`.

### Phase 4 / Step 7 — final integration pass (завершён, Phase 4 Intelligence Layer закрыт окончательно)

- **Step 7 — это закрывающий integration pass, не новая
  разработка.** В intelligence-server **не добавлено ни одного
  нового public-tool'а**; ни одной новой private-функции, ни
  одного нового файла. Размер registry — 16 tool'ов, как и в
  конце Step 6. Read-server и write-server не тронуты вообще.
- **Никаких точечных правок кода не понадобилось.** Сквозной
  integration pass прошёл с первой попытки на коде, собранном в
  Step 4–6: payload discipline согласована, failure-style един,
  никаких выдуманных tool-имён в `suggested_*`. Это и было
  главной задачей Step 7 — подтвердить, что слой работает как
  единое целое.
- **Сквозной интеграционный сценарий A (happy path, 9 шагов,
  одна цепочка).** Каждый следующий tool работает над фактом,
  подтверждённым предыдущим — это не серия независимых
  вызовов, а реальная цепочка.

  Synthetic dump (`tempfile.mkdtemp()`):
  `Catalogs/Primary/Primary.xml` (с `<Type>Catalog.Primary</Type>`,
  `<Reference>Catalog.Secondary</Reference>`,
  `<Module>CommonModule.Helpers</Module>`),
  `Catalogs/Primary/Forms/ItemForm/Form.xml`,
  `Catalogs/Primary/Ext/Module.bsl` (русские
  `Процедура Старт()` + `Функция РассчитатьИтог() Экспорт`),
  `Catalogs/Secondary/Secondary.xml`,
  `CommonModules/Helpers/Ext/Module.bsl`.

  - **A.1 `find_references_to_object('Primary')`** → `ok=True`,
    4 точных substring-матча, `sources_used.dump_xml=True`,
    `dump_bsl=True`. `confirmed_sources` содержит файлы под
    `Catalogs/Primary/...`. Дальше передаётся
    `target_object='Primary'` (carry-forward).
  - **A.2 `analyze_object_dependencies('Primary')`** → `ok=True`,
    `confirmed_dependencies` = `{Catalog.Secondary,
    CommonModule.Helpers}` (XML-карточка), `presumed_dependencies`
    = русские формы тех же зависимостей (BSL-модуль). **Discipline
    invariant подтверждён скриптом**: `confirmed_names &
    presumed_names == ∅` — на одинаковых именах множества не
    пересекаются.
  - **A.3 `estimate_change_impact('Primary')`** → `ok=True`,
    `reference_count=4`, `impact_level='low'` (det. threshold).
    `sources_used` перечисляет три помощника runtime Step 3.
  - **A.4 `find_affected_forms('Primary')`** → `ok=True`,
    `confirmed_findings` непустой (структурный путь
    `Catalogs/Primary/Forms/ItemForm/Form.xml`),
    `presumed_findings` содержит weak-form-сигналы.
  - **A.5 `find_affected_modules('Primary')`** → `ok=True`,
    `module_summary` непустой (попадание в
    `Catalogs/Primary/Ext/Module.bsl`), XML-сигналы — в
    `presumed_findings`.
  - **A.6 `suggest_safe_change_order('Primary')`** → `ok=True`,
    6 шагов, `impact_level='low'`. `suggested_write_tools`
    содержит **17 уникальных имён** — все проверены скриптом
    через `mws.list_tools()` и подтверждены как реально
    зарегистрированные в write-server.
  - **A.7 `suggest_metadata_patch_plan('common_module', 'Helpers',
    "add a method to the helpers common module")`** → `ok=True`,
    6 write-tool шагов: `check_write_preconditions →
    create_backup_snapshot → create_dump_snapshot →
    create_common_module → update_database_configuration →
    verify_module_contains`. Все 6 имён есть в реальном
    write-registry.
  - **A.8 `suggest_fix_for_issue('handler_method_missing',
    context_data={...Primary, Module.bsl, GhostHandler})`** →
    `ok=True`, 3 step recipe, `suggested_write_tools=
    [append_module_method, verify_module_contains]` — оба
    реальны. `context_data` пробрасывается verbatim в
    `confirmed_findings`.
  - **A.9 `summarize_configuration_risk('Primary')`** →
    `ok=True`, `risk_level='medium'` (gateway_down в health_codes,
    как и предусмотрено правилом).
  - **A.10 `prepare_intelligence_report('Primary')`** →
    `ok=True`, **4 sections** (default include_set), 0 skipped,
    aggregated `confirmed=3, presumed=5, recommended_checks=3,
    suggested_tools=6`. **Provenance discipline подтверждена**:
    каждый item в `confirmed_findings` / `presumed_findings`
    помечен своим `tool` (имя — реальный intelligence-tool),
    каждое имя в aggregated `suggested_tools` — реальный tool
    из intelligence- или read-registry.
- **Failure-path сценарии (5 штук, единый стиль, все зелёные).**
  - **F.1** `analyze_object_dependencies(env_ok,
    'TotallyMissingObject')` → `ok=False`,
    message `Object '...' not found in dump (no XML card, no BSL module).`.
  - **F.2** `diagnose_missing_method_or_attribute(env_ok)` без
    обоих режимов → `ok=False`, message начинается с `Provide`.
  - **F.3** `find_references_to_object(env_ok, "")` →
    `ok=False`, `object_name is empty.`.
  - **F.4** `prepare_intelligence_report(env_no_dump,
    'TotallyMissingObject', include_tools=[
    'analyze_object_dependencies', 'wat_no_such_tool'])` —
    смешанный сценарий: и плохой dump, и неизвестный
    include-name. Результат соответствует контракту: report
    остаётся `ok=True` (orchestrator завершился), `wat_no_such_tool`
    — в `skipped_unknown_tools`, а внутренняя section
    `analyze_object_dependencies` имеет `ok=False`. Sub-tool
    отдельно отчитывается о своей деградации, исключений
    наружу нет.
  - **F.5** `suggest_metadata_patch_plan` под deletion-goal
    (`"delete this catalog"`) → `ok=True` с `recommended_sequence=[]`
    и `presumed_findings` содержит `deletion_not_supported`.
    Параллельно `suggest_metadata_patch_plan('report',
    'AnyReport', 'create a report')` (известный, но
    unsupported kind) → `ok=True`, `recommended_sequence=[]`,
    `presumed_findings == [{pattern: kind_unsupported, ...}]`,
    `suggested_write_tools == []` — никаких выдуманных имён.
- **Real-tool-name discipline (программный assert).** Скрипт
  собирает `mis.list_tools()`, `mrs.list_tools()`,
  `mws.list_tools()` в три set'а и для каждого payload (impact,
  safe-order, plan, fix, report) проверяет: каждое имя в
  `suggested_tools` принадлежит intelligence ∪ read; каждое имя
  в `suggested_write_tools` принадлежит write. **Ни одного
  выдуманного имени** — ни в одной точке цепочки.
- **Read-only контракт подтверждён программно.** В скрипте есть
  жёсткий assert: grep
  `^\s*(from|import)\s+onec_policy_engine\b` по
  `apps/mcp-intelligence-server/src/**/*.py` (10 `.py`-файлов
  пакета) → **0 реальных импортов**. Это автоматическая
  проверка, а не глаз — assert упадёт, если кто-то добавит
  такой импорт.
- **Registry invariants под программным assert.**
  - intelligence: `set(...)==expected_intel`,
    `tools == sorted(tools)` — 16 имён, алфавит;
  - read: `len(...) == 15`;
  - write: `len(...) == 23`.
  Любой дрифт обнаружится падением assert'а.
- **Что изменилось в коде Step 7.** Только PROJECT-STATUS и
  оба README. Ни строчки в `apps/mcp-intelligence-server/src/**`,
  ни в `apps/mcp-read-server/**`, ни в `apps/mcp-write-server/**`,
  ни в `packages/**`, ни в `scripts/**`. Это **сознательный итог
  Step 7** — закрывающий integration pass, не разработка.
- **`mcp-intelligence-server/README.md`** обновлён точечно:
  из блока «Чего намеренно ещё нет» убрана строка про
  «финальной интеграции Phase 4 (один сквозной integration
  pass и фиксация baseline'а — Phase 4 / Step 7)» — этот
  пункт теперь сделан. Остальные MVP-honesty заметки (отсутствие
  AST, ML-кластеризации, настоящего topo-sort, MCP-обвязки)
  оставлены как есть — они и есть честная неполнота, не
  имеющая отношения к закрытию Phase 4.
- **Корневой `README.md`** обновлён: Phase 4 переведена из
  «активная фаза» в «завершён» с краткой сводкой публичной
  поверхности (16 read-only intelligence tool'ов в группах
  A/B/C/D); материалы Phase 4 (`phase-4-intelligence-plan.md`,
  `phase-4-step-map.md`) перемещены в блок «закрытых фаз».
  Phase 5 пока без активной строки — её планирование не
  входит в Step 7.
- **Ручная проверка.** Временный скрипт
  `C:\Users\user\AppData\Local\Temp\intelligence_step7_integration.py`
  единым прогоном выполняет: registry invariants → 9-шаговую
  цепочку Scenario A → 5 failure-path сценариев → grep на
  `onec_policy_engine`. Все assert'ы прошли с первой попытки.
  Финальная строка вывода — `ALL Step 7 integration checks
  passed.`. Скрипт лежит **вне проекта**, в `%TEMP%`, и в
  репозиторий не попадает.
- **Dev-check после Step 7 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (без изменений), `write_server_tools`
  = 23 (без изменений), **`intelligence_server_tools` — 16 tool'ов**,
  `selfcheck_status = ok`, `Dev check completed successfully.`.

### Phase 5 / Step 1 — planning Product Layer (завершён)

- **Стратегический сдвиг фазы.** После закрытия Phase 4 у
  платформы есть полное инженерное ядро: read (15) + write
  (23) + intelligence (16). Phase 5 — **не «ещё несколько
  tool'ов»**: это переход от набора серверов к цельному
  продукту, который можно установить, поднять, подключить
  к 1С, безопасно использовать, сопровождать, откатывать,
  диагностировать и реально выдать другому человеку или
  команде. Step 1 фиксирует этот сдвиг документационно;
  кода в Step 1 не написано.
- **Создано два новых документа в `docs/architecture/`.**
  - `docs/architecture/phase-5-product-layer-plan.md` —
    основной план фазы. Содержит: назначение фазы (почему
    после четырёх закрытых фаз нам всё ещё нужен
    отдельный Product Layer); целевой результат в
    терминах того, что должен уметь пользователь после
    закрытия Phase 5 (8-пунктовый нарратив от установки
    до smoke test'а); прямой mapping незакрытых
    стратегических разрывов на блоки фазы (что
    закрывается полностью, что частично, что остаётся
    enterprise track'ом); сравнение Phase 5 с Phase 1–4
    (адресат меняется с агента на человека); шесть
    продуктовых блоков; список из 20 продуктовых
    capability'ов, сгруппированных по блокам;
    guardrails; явный список того, что **не** входит;
    11 критериев приёмки; связь с предыдущими фазами;
    раздел открытых вопросов для Step 2+.
  - `docs/architecture/phase-5-step-map.md` — стартовая
    карта фазы из 8 шагов в едином формате
    (Цель / Что меняем / Затронутые зоны / Результат):
    Step 1 — product contract / scope / packaging
    (текущий шаг); Step 2 — installer / bootstrap
    contract; Step 3 — runtime orchestration / single
    entry point; Step 4 — environment doctor / health
    dashboard; Step 5 — guided workflow layer (3
    базовых workflow'а); Step 6 — rollback / recovery /
    audit UX; Step 7 — real-stand / 1cv8 binary
    integration track; Step 8 — final integration pass.
- **Ключевые продуктовые блоки, зафиксированные в плане
  (A–F).**
  - **A. Installation / bootstrap** — installer, setup
    wizard, prereqs doctor; режимы установки local-dev /
    stand / enterprise-bootstrap-only.
  - **B. Runtime orchestration** — единая точка входа
    start/stop/status/reload; environment profile
    manager; product-уровневый health dashboard.
  - **C. Safe workflow layer** — 2–3 базовых guided
    workflow'а (safe-add-attribute, safe-add-module-method,
    stand-health-check); запрет silent apply.
  - **D. Rollback / recovery / audit UX** — operation
    history viewer, rollback assistant, recovery workflow.
  - **E. Real-stand / production-readiness** — reference
    stand spec, 1cv8 binary integration contract,
    end-to-end smoke test, packaging, versioning.
  - **F. Operator UX / docs** — operator manual,
    administrator manual, developer manual, user-facing
    message style guide.
- **Какие стратегические разрывы закрывает Phase 5.**
  Полностью закрываются: разрыв (1) runtime/deployment
  слой, (3) installer, (6) автоматический rollback, (7)
  intelligence в продуктовом UX, (8) workflow layer,
  (9) end-to-end на стенде. Частично закрываются:
  разрыв (2) 1cv8 binary integration (Phase 5 даёт
  contract + smoke test, не полное замещение всех
  stub'ов), (4) расширение metadata operations
  (намеренно не расширяется — фаза не про tool surface),
  (5) полное structural editing XML/BSL (AST не
  вводится). Остаётся enterprise track'ом: разрыв (10)
  enterprise hardening (SSO/RBAC, multi-tenant, secrets
  vault, federated audit storage) — отдельный трек
  после Phase 5.
- **Guardrails Phase 5 (зафиксированы в плане).** Запрет
  production write by default; обязательное явное
  targeting окружения; никакого silent apply; install /
  upgrade / rollback только с диагностикой; fail-closed
  при неполных prereqs; честная деградация, а не
  «магия»; **продуктовый UX не размывает safety
  guarantees Phase 2–4** (никакого обхода
  `run_write_flow`, никакого обхода audit, никакого
  обхода snapshot'ов, никакого импорта
  `onec_policy_engine` в intelligence-server, read-only
  intelligence сохраняется).
- **Что не входит в Phase 5 (зафиксировано явно).**
  Fully autonomous agent; magical self-healing
  production; бесконечная оркестрация; полная замена
  1С-администрирования; enterprise-всё-в-одном за один
  шаг; полное замещение всех Phase 2 stub'ов
  настоящей 1cv8-бинарью; AST-парсер XML/BSL;
  крупный рефакторинг read/write/intelligence ради
  продукта.
- **Критерии приёмки Phase 5 (11 пунктов).**
  Установка по короткому понятному сценарию;
  платформа поднимается как согласованный набор
  сервисов; ≥ 2–3 end-to-end user workflows;
  rollback / recovery — реальный продуктовый сценарий;
  реальный стенд / 1cv8 integration имеют явный трек
  готовности; документация существует как продукт;
  dev-check зелёный; read/write/intelligence не
  деградировали (15 / 23 / 16 tools); read-only
  контракт intelligence-server'а сохранён;
  safety guarantees Phase 2–4 не размыты; продукт
  ощутимо ближе к «готовому к выдаче пользователю».
- **Что изменилось в коде Step 1.** **Ничего.** Ни
  одной строчки. `apps/`, `packages/`, `scripts/`,
  `pyproject.toml`, `.github/`, `runtime/`, `tools.py`,
  `server.py` всех трёх серверов — не тронуты.
  Registry'ы read (15), write (23), intelligence (16)
  не менялись. Dev-check остаётся в том же зелёном
  состоянии, что и после Phase 4 / Step 7.
- **Обновлены документы.**
  - Корневой `README.md`: Phase 4 переведена в
    «закрытые фазы», Phase 5 помечена как активная
    фаза с кратким описанием цели (Product Layer);
    добавлены ссылки на оба новых документа
    (`phase-5-product-layer-plan.md`,
    `phase-5-step-map.md`); остальные разделы
    `README.md` не менялись.
  - `PROJECT-STATUS.md`: обновлены шапка (текущий
    шаг → Phase 5 / Step 1, статус → in progress),
    добавлен подробный Step 1 record (этот блок),
    обновлена «Следующий шаг» секция (см. ниже),
    обновлены «Крупные этапы проекта» (Phase 4 →
    Закрыта, Phase 5 → Активная фаза).
- **Открытые вопросы Step 1 (для Step 2+).** В плане
  явно зафиксированы вопросы, на которые Step 1 не
  даёт окончательного ответа: формат релиза (clone
  + lockfile / zip / wheel / installer-скрипт);
  формат product-config (YAML / TOML / JSON);
  транспорт MCP (stdio / TCP / локальный socket);
  интерактивный vs декларативный setup; storage
  operation history; глубина 1cv8-integration в
  smoke test. Step 1 не делает вид, что ответы
  уже найдены.

### Phase 5 / Step 2 — installer / bootstrap contract (завершён)

- **Принятые архитектурные решения Step 2 (закрывают
  открытые вопросы Step 1).**
  - **Расположение product-слоя:** `apps/platform/`,
    пакет `onec_platform`. Решение принято консервативно:
    это исполняемое приложение продукта (не reusable
    library), и оно органично встаёт рядом с тремя
    MCP-серверами в `apps/`. `packages/onec-product/`
    отвергнут, так как product layer — это **сам
    продукт**, а не разделяемая зависимость нескольких
    приложений. Соответствующая правка `apps/README.md`
    выполнена: раздел теперь честно описывает, что в
    `apps/` живут и MCP-серверы, и продуктовое
    приложение.
  - **Формат product-config:** **JSON**. Используем
    `json` из stdlib, новых зависимостей не привносим
    (важно: `pyproject.toml` не тронут). YAML/TOML
    отвергнуты ради нулевых dependency-измений на
    Step 2.
  - **Форма setup:** **декларативная**. Пользователь
    предоставляет JSON-файл product-config'а,
    `bootstrap_product_from_json_file(...)` его читает
    и валидирует. Интерактивный wizard сознательно
    отложен (если потребуется — отдельный шаг **после**
    Step 3).
  - **Транспорт MCP** — **не** решается на Step 2 (этот
    вопрос относится к Step 3 step-map'а). На Step 2
    серверы по-прежнему живут как in-process модули.
- **Что реально появилось в репозитории.**
  - Новое приложение `apps/platform/` со своим
    `README.md`. Содержит src-tree пакета `onec_platform`:
    - `models.py` — dataclass'ы:
      - `ProductConfig` — верхнеуровневый product-конфиг
        (`product_name`, `profile_name`, ссылка на
        `ProjectConfig` из `onec_config`,
        `default_environment`, `servers`, `bootstrap`);
      - `ProductServerToggles` — флаги включения
        `read` / `write` / `intelligence`;
      - `ProductBootstrapSettings` — `work_dir` (опц.) +
        три `require_*` флага (`require_dump_path`,
        `require_base_path`, `require_python`),
        отключение каждого видно как **warning-finding**
        в doctor-отчёте, не молча;
      - `DoctorFinding` — одна находка doctor'а:
        `code`, `severity ∈ {ok, warning, error}`,
        `confidence ∈ {confirmed, presumed}`, `detail`.
        Confirmed/presumed split — та же дисциплина,
        что у Phase 4 intelligence-tools;
      - `DoctorReport` — `findings`, `error_count`,
        `warning_count`, `recommended_actions`;
      - `BootstrapResult` — boundary-результат:
        `ok`, `product_name`, `profile_name`,
        `default_environment`, `doctor`, `message`.
    - `loader.py`:
      - `load_product_config(data: dict) -> ProductConfig`
        — строгая структурная валидация, fail-closed
        через `ValueError`. Делегирует
        `onec_config.load_project_config` для секции
        `project` (никакого дублирования
        `EnvironmentConfig`).
      - `load_product_config_from_json_file(path) ->
        ProductConfig` — чтение JSON-файла + парсинг +
        валидация. Все file-system / JSON-parse ошибки
        конвертируются в `ValueError` для единообразия.
    - `doctor.py`:
      - `run_prereqs_doctor(config) -> DoctorReport` —
        **никогда не бросает**. Проверки:
        1) resolve `default_environment` (defensive);
        2) `base_path` существует
        (skipped с warning-finding'ом, если
        `require_base_path=False`);
        3) `dump_path` существует (аналогично);
        4) `python` на `PATH` через `shutil.which("python")`
        (аналогично);
        5) `http_base_url` парсится в scheme + host —
        **presumed** (реального HTTP-probe нет; это
        Step 4);
        6) для каждого включённого server toggle —
        `importlib.util.find_spec(module_name)`;
        отключённый toggle — warning-finding
        `server_disabled:<name>`, не молчаливый skip;
        7) опциональный `bootstrap.work_dir`
        существует и является директорией.
    - `bootstrap.py`:
      - `bootstrap_product(data) -> BootstrapResult` —
        **boundary-функция, никогда не бросает**.
        Загружает конфиг, гоняет doctor, собирает
        `BootstrapResult` с человекочитаемым `message`.
      - `bootstrap_product_from_json_file(path)` — то
        же, но из JSON-файла.
    - `__init__.py` — публичная поверхность пакета +
      package-level docstring, фиксирующий Phase 5 /
      Step 2 surface и safety-контракт (никаких
      write-операций; никакого старта серверов;
      никакого `onec_policy_engine`-импорта; boundary
      не бросает).
  - `apps/README.md` — обновлён: раздел больше не
    утверждает, что в `apps/` живут только MCP-серверы;
    добавлено описание `platform` как продуктового
    слоя.
  - `scripts/dev/bootstrap_paths.ps1` — добавлен путь
    `apps\platform\src` в `$srcPaths`, чтобы пакет
    `onec_platform` был импортируем во всех скриптах
    проекта. Других изменений в скрипте нет.
- **Чего на Step 2 намеренно ещё нет (зафиксировано в
  README пакета).** MCP-транспорта; `start`/`stop`/
  `status`/`reload` (это Step 3); реального HTTP /
  health probe (это Step 4); реального installer'а
  под ОС; интерактивного wizard'а; реальной
  1cv8-binary интеграции (Step 7); workflow runner'а
  (Step 5); rollback assistant'а (Step 6); запуска
  write-операций — никогда из этого пакета.
- **Safety guarantees Phase 2–4 — что сохраняется.**
  - `mcp-read-server` registry — те же 15 tool'ов, не
    тронут.
  - `mcp-write-server` registry — те же 23 tool'а, не
    тронут. `run_write_flow` остаётся единственным
    путём к mutating операциям.
  - `mcp-intelligence-server` registry — те же 16
    tool'ов, не тронут. Read-only контракт сохранён:
    `onec_policy_engine` не импортируется ни в
    intelligence-server'е, ни в `onec_platform`.
  - `onec-config` — не тронут (используем существующие
    `load_project_config` и `EnvironmentConfig`).
  - `onec-policy-engine` — не тронут и **не**
    импортируется в product layer. Bootstrap — это
    install-readiness, не write-policy-решение.
  - `pyproject.toml`, `.github/`, корневой `README.md`
    (кроме блока «Текущий статус по фазам»),
    `selfcheck.py` — не тронуты.
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`bootstrap_product`,
    `bootstrap_product_from_json_file`) **никогда не
    бросают**; на любую проблему отдают
    `BootstrapResult(ok=False, ..., message=...)`.
  - Inner helpers (`load_product_config`,
    `load_product_config_from_json_file`) бросают
    `ValueError` на битый вход — fail-closed, как и
    `onec_config.load_project_config`.
  - `run_prereqs_doctor` тоже никогда не бросает —
    внутренние ошибки оборачиваются как
    `severity="error"` finding.
  - `ok=True` означает «шаг выполнился», не «всё
    здорово». Реальная готовность к запуску — в
    `result.doctor.error_count == 0`.
- **Ручная проверка (13 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step2_check.py`
  материализует synthetic temp-директории и JSON-файлы
  через `tempfile.mkdtemp()`. Сценарии:
  - **0. registry invariants** — read=15, write=23,
    intelligence=16 (sanity-check до и после) — без
    изменений.
  - **1. happy path** — валидный config + существующие
    base_path/dump_path + python на PATH + все три
    server-toggle включены → `ok=True`,
    `error_count=0`, `warning_count=0`, 8 ok-findings,
    `confirmed`/`presumed` распределены честно
    (`http_base_url_well_formed` — presumed,
    остальные — confirmed).
  - **2. broken config (3 подсценария).** Отсутствует
    `product_name` → `ok=False` с message содержащим
    имя поля. Root не dict → `ok=False`. Wrong type
    для `servers` → `ok=False`.
  - **3. bad default environment** —
    `default_environment="ghost-env"`, отсутствует в
    `project.environments` → `ok=False`, в message
    перечислены known environments.
  - **4. missing paths** — `base_path` и `dump_path`
    не существуют → `ok=True` (doctor отработал),
    `error_count=2`, findings содержат
    `base_path_missing` и `dump_path_missing` с
    severity=error, recommended_actions содержит
    указания по обоим путям.
  - **5. server toggles** — `intelligence=False` →
    `ok=True`, finding `server_disabled:intelligence`
    severity=warning; ни одного
    `server_module_importable:intelligence` или
    `server_module_missing:intelligence` (отключение
    видно, но importability check не дублируется).
  - **6. JSON file path** —
    `bootstrap_product_from_json_file` на валидный
    JSON-файл → `ok=True`, тот же набор findings, что
    и dict-вход.
  - **7. JSON file errors (3 подсценария).** Файл не
    существует → `ok=False, "not found"`. Файл
    битый JSON → `ok=False, "not valid JSON"`. Путь
    указывает на директорию → `ok=False, "not a
    regular file"`.
  - **8. bootstrap.work_dir variants (3 подсценария).**
    Существующая директория →
    `bootstrap_work_dir_exists` severity=ok.
    Файл (не директория) →
    `bootstrap_work_dir_not_a_dir` severity=error,
    `error_count >= 1`. Несуществующий путь →
    `bootstrap_work_dir_missing` severity=warning.
  - **9. require_python=False** — finding
    `python_check_disabled` severity=warning;
    `python_on_path` / `python_not_on_path` отсутствуют
    (отключение видно, но check не запускается). Это
    проверка дисциплины «никакого silent skipping».
  - **10. malformed http_base_url** —
    `http_base_url="not-a-url"` →
    `http_base_url_malformed` severity=warning,
    confidence=presumed; recommended_actions содержит
    указание исправить URL. Ни одного исключения
    наружу.
- **Dev-check после Step 2 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools`
  = 23 (не тронут), **`intelligence_server_tools` — 16
  tool'ов** (не тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`. Selfcheck.py
  намеренно не дёргает `onec_platform` — продуктовый
  слой опционален для dev-check'а; интеграция в
  selfcheck (если понадобится) — отдельный шаг после
  Step 3.

### Phase 5 / Step 3 — runtime orchestration / single entry point (завершён)

- **Архитектурная честность Step 3.** Step 3 строит
  **product-level launcher contract**, а не выдумывает MCP
  transport за read/write/intelligence. Сами три сервера
  по-прежнему живут как in-process модули; их встроенный
  CLI / `__main__` / production transport — отдельный
  track, не Step 3. Product layer управляет **только теми
  argv-командами**, которые оператор явно описал в
  `ProductConfig.runtime.services`. Это решение зафиксировано
  и в коде (docstring'и `runtime.py` и `__init__.py`), и в
  README продуктового слоя.
- **`reload` — это controlled stop-then-start, не hot
  reload.** В коде (`reload_product_runtime`) и в README
  явно зафиксировано: PID'ы после reload гарантированно
  новые. Никаких ложных заявлений о zero-downtime поведении.
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/process_control.py` —
    cross-platform PID/proc primitives на чистом stdlib.
    POSIX: `os.kill(pid, 0)` для liveness и
    `signal.SIGTERM` для terminate. Windows: `OpenProcess`
    + `WaitForSingleObject` / `TerminateProcess` через
    `ctypes`. На Windows `os.kill(pid, 0)` намеренно
    **не** используется (некоторые сборки CPython при
    `os.kill(pid, sig)` на Windows фактически вызывают
    `TerminateProcess` — это было бы катастрофой для
    liveness-пробы). `spawn_service` детачит stdio в
    `DEVNULL` и стартует ребёнка в своей process group /
    session.
  - `apps/platform/src/onec_platform/state.py` — атомарный
    state-store под `<work_dir>/.runtime/runtime-state.json`.
    Запись через tmp-файл + `os.fsync` + `os.replace`.
    Read fail-closed через `ValueError` на битый JSON и на
    неизвестную `schema_version`. Schema version = 1 на
    Step 3.
  - `apps/platform/src/onec_platform/runtime.py` — четыре
    boundary-функции (`start_product_runtime`,
    `stop_product_runtime`, `get_product_runtime_status`,
    `reload_product_runtime`) + их `_from_json_file`
    варианты. **Никогда не бросают.** Resolve config →
    resolve work_dir → load persisted state → materialize
    services из текущего spec'а (spec — authoritative для
    enabled/configured/command, persisted overlay — для
    pid/status/started_at) → refresh stale PIDs → apply
    `only=…` фильтр → выполнить операцию → атомарно
    сохранить state. `only=` — surgical-фильтр; неизвестное
    имя → warning, не abort.
  - `apps/platform/src/onec_platform/models.py` — добавлены
    `ProductServiceSpec`, `ProductRuntimeSettings`,
    `RuntimeServiceState`, `RuntimeStateFile`,
    `RuntimeOperationResult`, `RuntimeStatusResult`;
    `ProductConfig` расширен полем
    `runtime: ProductRuntimeSettings = field(default_factory=...)`,
    что сохраняет полную backward compatibility со Step 2.
    Также добавлены константы `RUNTIME_STATUSES` и
    `RUNTIME_STATE_SCHEMA_VERSION` как единый источник
    правды для тестов / README / runtime-кода.
  - `apps/platform/src/onec_platform/loader.py` — добавлены
    private helper'ы `_parse_runtime` и
    `_parse_service_spec`. `runtime` секция опциональна;
    отсутствие → пустой `ProductRuntimeSettings`.
    Тип-проверки строгие: `command` — non-empty list[str],
    не shell-строка; `working_dir` — string или
    отсутствует; `env_overrides` — dict[str, str].
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 16 новыми
    именами (модели + boundary helpers + `runtime_dir` /
    `state_file_path` для path discovery). package
    docstring переписан под совместное Step 2 + Step 3
    surface с явными honesty-комментариями про MCP
    transport и hot reload.
- **Чего на Step 3 намеренно ещё нет (зафиксировано в
  README пакета).** Production-grade MCP transport внутри
  read/write/intelligence; hot reload (только controlled
  restart); daemon / service manager (нет регистрации
  Windows Service / systemd unit); захват stdout/stderr
  дочерних процессов (DEVNULL — для предсказуемости
  pipe-буфферов); авто-restart упавших сервисов; реального
  HTTP / health probe (Step 4); installer'а под ОС;
  интерактивного wizard'а; реальной 1cv8-binary
  интеграции (Step 7); workflow runner'а (Step 5);
  rollback assistant'а (Step 6); запуска write-операций
  из `onec_platform` (никогда).
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`start_product_runtime`,
    `stop_product_runtime`, `get_product_runtime_status`,
    `reload_product_runtime`, плюс `_from_json_file`
    варианты) **никогда не бросают**: на любую проблему
    отдают `RuntimeOperationResult(ok=False, ..., findings=[...])`
    или `RuntimeStatusResult(ok=False, ...)` с
    error-finding'ом.
  - `ok=True` означает «шаг отработал», не «всё в желаемом
    состоянии». Реальный статус сервисов — в
    `result.services[*].status`. Per-service сбои попадают
    в findings по конвенции `<event>:<service>` (например
    `runtime_started:read`, `runtime_command_missing:write`,
    `runtime_pid_stale:read`).
  - Inner helper'ы (`load_product_config`,
    `load_product_config_from_json_file`, `read_state`,
    `write_state`, `spawn_service`) бросают
    `ValueError` / `OSError` fail-closed, но **только
    внутри** — boundary всегда оборачивает.
  - `confirmed`/`presumed` дисциплина из Phase 4 + Step 2
    doctor'а сохранена: каждый finding несёт
    `confidence`, и `is_pid_alive` даёт **confirmed**
    статус, а не presumed (мы реально пробуем системный
    вызов).
- **Safety guarantees Phase 2–4 — что сохраняется.**
  - `mcp-read-server` registry — те же 15 tool'ов, не
    тронут.
  - `mcp-write-server` registry — те же 23 tool'а, не
    тронут. `run_write_flow` остаётся единственным путём
    к mutating операциям. `onec_platform` **не** обходит
    его — он **не вызывает** ни write-tool'ов, ни
    `run_write_flow`, ни audit-API.
  - `mcp-intelligence-server` registry — те же 16 tool'ов,
    не тронут. Read-only контракт сохранён:
    `onec_policy_engine` не импортируется ни в нём, ни в
    `onec_platform`.
  - `onec-config`, `onec-policy-engine`, `pyproject.toml`,
    `.github/`, `selfcheck.py`, `bootstrap_paths.ps1` —
    не тронуты на Step 3 (PYTHONPATH `apps\platform\src`
    был добавлен ещё в Step 2).
  - `onec_platform` сам **не выполняет write-операций
    в 1С**. Он управляет PID-ами тех процессов, которые
    оператор описал, и точка. Любая mutating операция
    по-прежнему идёт через write-server и его
    `run_write_flow`.
- **Persisted state file contract.**
  - путь — `<work_dir>/.runtime/runtime-state.json`;
  - `schema_version=1`; неизвестная версия → fail-closed
    через `ValueError`, который boundary оборачивает в
    error-finding `runtime_state_unreadable`;
  - `env_override_keys` — это **ключи** override'ов, не
    значения, чтобы state-файл не утаскивал секреты;
  - запись атомарная (tmp + `os.fsync` + `os.replace`);
  - `.runtime/` — платформенно-владенный подкаталог,
    создаётся автоматически. Сам `work_dir` создаёт
    оператор; платформа его **не** создаёт и **не**
    переиспользует молча.
- **Ручная проверка (13 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step3_check.py`
  использует `tempfile.mkdtemp` и **реальные subprocess'ы**
  (`python -c "import time; time.sleep(120)"`) для
  честной проверки PID-liveness. Сценарии: registry
  invariants; happy path start→status→stop с реально
  живыми PID'ами; идемпотентный start (без дубликатов);
  reload даёт новые PID'ы и реально убивает старые;
  `disabled` сервис не стартует; missing command →
  `status=missing`+error finding; stale-PID detection
  (state-файл при этом **не** переписывается);
  bad work_dir в трёх вариантах (None / missing /
  is-file); JSON-file flow эквивалентен dict-flow;
  backward compatibility со Step 2 (config без секции
  `runtime` грузится и работает с warning-finding'ом
  `runtime_contract_empty`); `only=` surgical-фильтр
  с известным и неизвестным именем; битый/отсутствующий
  JSON; битый state-файл (boundary не падает, отдаёт
  finding); финальные registry invariants. Все 13
  сценариев прошли с первой попытки. Каждый спавненный
  subprocess реально reaped через `terminate_pid` до
  завершения скрипта.
- **MVP-компромиссы Step 3 (зафиксированы честно).**
  - **`reload` — controlled stop-then-start.** Не hot
    reload; PID'ы после reload новые. Это в README и в
    коде явно.
  - **Stdio дочерних процессов идёт в `DEVNULL`.**
    Operator должен сам логировать в файл из
    argv-команды. Captured logs с ротацией — possible
    follow-up Step 4 / Step 8.
  - **Нет watch-and-restart.** Если дочерний процесс
    умер вне `stop`, он становится `stale`; чтобы его
    поднять, нужен явный `start`. Auto-restart policy —
    отдельный track.
  - **PID-based supervision, не daemon manager.** Никакой
    регистрации Windows Service / systemd unit на этом
    шаге.
  - **Best-effort `terminate_pid`.** Если SIGTERM /
    `TerminateProcess` вернул ошибку, состояние сервиса
    помечается `error`; следующий `start` всё равно
    спавнит свежий процесс — старый PID может остаться
    жить. Operator handles it. README это фиксирует.
  - **State-файл не переписывается чистым `status`.**
    Stale-detection попадает в результат, но on-disk
    остаётся как есть до следующего `start`/`stop`/`reload`.
    Это намеренное разделение read-only и mutating
    операций.
  - **Команды примера в README** (`python -m
    mcp_read_server` и т.п.) приведены как иллюстрация
    формата. Phase 5 / Step 3 **не утверждает**, что
    у read/write/intelligence уже есть рабочий
    `__main__` / CLI — добавление их остаётся
    follow-up'ом.
- **Dev-check после Step 3 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools`
  = 23 (не тронут), **`intelligence_server_tools` — 16**
  (не тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`. Selfcheck.py
  намеренно не дёргает `onec_platform.runtime` — runtime
  ops опциональны для dev-check'а.

### Phase 5 / Step 4 — environment doctor / health dashboard (завершён)

- **Архитектурная честность Step 4.** Step 4 — это
  **product-уровневый aggregation contract**, а не новый
  MCP-сервер и не UI. В пакете `onec_platform` появляется
  одна boundary-функция `build_environment_dashboard(...)`
  (плюс `_from_json_file` вариант), которая собирает в
  один read-only snapshot **уже существующие** сигналы:
  bootstrap doctor (Step 2), runtime status (Step 3),
  `read.check_runtime_health`, `read.diagnose_connectivity_issue`,
  `intelligence.analyze_runtime_issue`,
  `intelligence.summarize_configuration_risk`. Никакой
  новой диагностической логики не изобретается — только
  агрегация.
- **Один источник на секцию.** Фиксированные six sections и
  явные provenance-маркеры:
  - `bootstrap` ← `platform.bootstrap_product`;
  - `runtime` ← `platform.get_product_runtime_status`;
  - `read_health` ← `read.check_runtime_health`;
  - `read_diagnosis` ← `read.diagnose_connectivity_issue`;
  - `intelligence_runtime` ← `intelligence.analyze_runtime_issue`;
  - `intelligence_risk` ← `intelligence.summarize_configuration_risk`.
  `read.health_summary` намеренно **не** включён: это
  легаси-stub helper с булевыми флагами, и его честное
  включение либо дублирует `check_runtime_health`, либо
  даёт ложное «всё ок». Решение явно зафиксировано в
  README продуктового слоя.
- **Verdict — deterministic, hand-written.** Полный
  ruleset документирован в docstring'е `_compute_verdict`
  и в README.
  - **`blocked`** если: bootstrap section ok=False;
    bootstrap doctor имеет error-finding; runtime section
    ok=False; required runtime service в статусе
    `missing` или `error`; read-side health codes содержат
    `dump_missing` или `gateway_down`.
  - **`degraded`** если не blocked, но: runtime service
    в `stale`; read-side health codes содержат любой
    не-ok код вне blocking-списка; bootstrap doctor
    имеет warning; intelligence risk_level
    `medium`/`high`; runtime контракт пуст; любая
    секция помимо уже учтённых отдала ok=False;
    connectivity diagnosis сообщил непустой problem_code.
  - **`healthy`** иначе.
  - `ready_for_workflows = (overall_status == "healthy")`
    — жёсткое правило для Step 5.
- **Required service rule.** Сервис считается обязательным
  для verdict-правил **только** если `enabled=True` и
  `command` непуст. Disabled сервис не валит verdict.
  Сервис без команды → собственный
  `runtime_command_missing:<svc>` finding на runtime-уровне,
  но **не** делает verdict автоматически blocked: оператор
  мог явно решить «этим сервисом я управляю снаружи».
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/dashboard.py` — новая
    boundary + 6 секционных runner'ов + `_compute_verdict`
    + хелперы агрегации/нормализации/тагирования. Cross-app
    импорты идут только в правильном направлении: product
    layer → read, product layer → intelligence. Никакого
    обратного направления.
  - `apps/platform/src/onec_platform/models.py` — добавлены
    `DashboardSectionResult`, `DashboardVerdict`,
    `EnvironmentDashboardResult` + константа
    `DASHBOARD_OVERALL_STATUSES`. Step 2/3 модели не
    тронуты.
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 6 новыми
    именами (3 модели + константа + 2 boundary-функции);
    package docstring обновлён описанием Step 4 surface.
- **Чего на Step 4 намеренно ещё нет (зафиксировано в
  README).** UI / web-dashboard / push subscription;
  кэширования sub-tool вызовов (sub-tools зовутся каждый
  раз, в т.ч. транзитивно — например, `analyze_runtime_issue`
  внутри intelligence-секции сам зовёт
  `check_runtime_health` и `diagnose_connectivity_issue`,
  которые также зовутся read-секцией; это сознательный
  MVP-компромисс ради простоты failure mode); ML-оценок
  риска / здоровья (всё rule-based); собственного
  health-probe внутри dashboard'а (используем уже готовые
  read-tool'ы); Step 5 guided workflows (dashboard их не
  заменяет — он только описывает «что сейчас»).
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`build_environment_dashboard`,
    `build_environment_dashboard_from_json_file`)
    **никогда не бросают**.
  - Полный `ok=False` — только когда product config не
    загружается. В остальных случаях — partial dashboard
    with honest degradation: индивидуальный sub-tool сбой
    помечается на уровне секции (`section.ok=False` +
    error-finding в `confirmed_findings` + понятный
    `message`), но dashboard остаётся `ok=True`.
  - Confirmed/presumed дисциплина из Phase 4 + Step 2 не
    размывается. Каждый finding несёт собственный
    `confidence`. На уровне aggregated `confirmed_findings`
    / `presumed_findings` каждый код префиксован именем
    секции (`<section>/<original_code>`) для трассируемой
    provenance.
- **Safety guarantees Phase 2–4 + Step 2/3 — что
  сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в нём, ни в
    `onec_platform`. Это явно проверено программным
    assert'ом в manual check.
  - `run_write_flow` остаётся единственным путём к
    mutating операциям. `onec_platform` его **не
    обходит** и **не вызывает write-tool'ов**.
  - `onec-config`, `onec-policy-engine`, `onec-audit`,
    `onec-health`, `onec-process-runner`, `pyproject.toml`,
    `.github/`, `selfcheck.py`, `bootstrap_paths.ps1` —
    не тронуты на Step 4.
  - Read-server и intelligence-server вызываются через
    публичный Python API их `tools.py` модулей —
    cross-app направление `product layer → read /
    intelligence`, как и было заложено для Phase 5.
- **Ручная проверка (10 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step4_check.py`
  использует `tempfile.mkdtemp` + локальный
  `http.server.HTTPServer` на свободном порту (`127.0.0.1`)
  для честных read-side вызовов + реальные subprocess'ы
  через Step 3 surface. Сценарии:
  - **0. Registry invariants (sanity)** — read=15,
    write=23, intelligence=16; assert.
  - **A. Happy path** — валидный config, существующие
    base/dump, стартованные runtime-сервисы, живой HTTP →
    `ok=True`, `overall_status=healthy`,
    `ready_for_workflows=True`. Все 6 sources_used
    присутствуют и совпадают с ожидаемым множеством.
    Confirmed/presumed split реально присутствует в
    aggregated lists.
  - **B. Bootstrap degraded — base/dump missing** —
    bootstrap doctor находит `base_path_missing` и
    `dump_path_missing` (severity=error) → verdict
    `blocked`, `ready_for_workflows=False`. read-side
    тоже падает с `dump_missing` (так как `dump_path` не
    существует на диске). Dashboard остаётся `ok=True`,
    sections заполнены.
  - **C. Runtime stale** — реально стартуем runtime,
    извне убиваем PIDs (`terminate_pid`), затем
    `build_environment_dashboard`. Runtime section
    показывает services со статусом `stale`, verdict
    `degraded` с warnings `runtime_service_stale:read`
    и `runtime_service_stale:write`.
  - **D. Dead read-side endpoint** — http_url указывает
    на свободный порт без listener'а. read_health
    section ok=False, `gateway_down` в blocking_issues,
    overall_status=blocked. Dashboard сам не падает.
  - **E. Empty runtime contract** — Step 2 config без
    секции `runtime`. Dashboard `ok=True`, verdict
    `degraded` с warning `runtime_contract_empty`. Ни
    одного блокирующего runtime_required_service
    finding'а (потому что нет required services).
  - **F. Bad config JSON (3 sub-сценария).** Malformed
    JSON → `ok=False`, `Product config rejected: ... not
    valid JSON`. Missing file → `ok=False, ... not found`.
    Root not dict → `ok=False, ... must be a dict or a
    pre-loaded ProductConfig`. Никаких исключений
    наружу.
  - **G. Registry invariants (final).** read=15,
    write=23, intelligence=16 — после всех сценариев
    без изменений.
  - **H. Cross-app import contract.** Программный grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/platform/src/**/*.py` и
    `apps/mcp-intelligence-server/src/**/*.py` →
    **0 реальных импортов** (assert).
  - **I. Aggregation provenance.** Программный assert,
    что каждый код в `dash.confirmed_findings +
    dash.presumed_findings` содержит `/` (тег секции).
  - **J. JSON-file flow.** `build_environment_dashboard_from_json_file`
    эквивалентен dict-flow.
  Все 10 сценариев прошли. Каждый спавненный subprocess
  очищен через `terminate_pid` до выхода скрипта; локальный
  HTTPServer останавливается в `finally`-блоке.
- **MVP-компромиссы Step 4 (зафиксированы честно в README).**
  - **Sub-tool вызовы не кэшируются.** В одной dashboard-операции
    `check_runtime_health` и `diagnose_connectivity_issue`
    вызываются дважды — один раз read-секцией,
    второй раз внутри `analyze_runtime_issue` (которая
    сама их вызывает). Это сознательно: shared cache
    усложнил бы failure mode и провенанс.
  - **`health_summary` намеренно не включён.** Это
    легаси-stub helper; его включение либо дублирует
    `check_runtime_health`, либо даёт нечестное «ок».
  - **Connectivity-diagnosis section всегда `ok=True`.**
    Read-side `diagnose_connectivity_issue` сам по себе
    возвращает `ok=False` только при наличии проблемы;
    мы интерпретируем «проблема обнаружена» как
    successful diagnosis run, а не как сбой sub-tool'а.
    Соответствующий warning попадает в presumed_findings
    и в verdict через rule «connectivity_problem:<code>».
  - **`ready_for_workflows = healthy only`.** Это
    жёсткое правило: даже degraded не пускает workflow
    без оператора. Возможный override-флаг — отдельный
    enhancement Step 5.
  - **Подключаем только по умолчанию выбранные sub-tools.**
    `analyze_event_log_patterns` намеренно не включён —
    его включение требовало бы фильтров периода
    (period_start/end), а это уже product-policy решение,
    которое относится скорее к Step 5/6.
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `onec_policy_engine`,
    `onec-config`, `onec-audit`, `onec-health`,
    `onec-process-runner`.
  - Никакого UI / web-dashboard.
  - Никакого write-канала из `onec_platform`.
  - Никакого хот-мониторинга / push subscription.
  - Никаких ML-оценок.
  - Никакого Step 5 guided workflow runner.
  - Никаких изменений `selfcheck.py` /
    `bootstrap_paths.ps1` — эти были обновлены ещё в
    Step 2.
- **Dev-check после Step 4 зелёный.** `imports_ok =
  true`, `read_server_tools` = 15 (не тронут),
  `write_server_tools` = 23 (не тронут),
  **`intelligence_server_tools` — 16** (не тронут),
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает `onec_platform.dashboard` —
  dashboard опционален для dev-check'а.

### Phase 5 / Step 5 — guided workflow layer (завершён)

- **Архитектурная честность Step 5.** Workflow layer — это
  **product-уровневая оркестрация** уже существующих
  intelligence- и write-surfaces. Никакого собственного
  write channel в `onec_platform` не появилось: каждый
  mutating step идёт через **реальный публичный
  write-tool** (`add_catalog_attribute`,
  `add_document_attribute`, `append_module_method`),
  который сам внутри проходит через `run_write_flow`
  (preflight → backup snapshot → dump snapshot →
  operation → verify → audit). Workflow runner **не
  обходит** ни один из этих шагов.
- **Дисциплина precondition'а.** Mutating workflow'ы
  (`safe-add-attribute`, `safe-add-module-method`)
  стартуют только при выполнении **двух** условий
  одновременно: оператор передал `confirm_execute=True`
  И dashboard.verdict.ready_for_workflows == True. Без
  любого из них workflow возвращает `mode=preview` или
  `mode=blocked`. `stand-health-check` — read-only
  диагностика, она работает даже на degraded/blocked
  окружении (специально вынесено отдельным правилом).
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/workflow.py` — новая
    boundary + три приватных runner'а
    (`_run_safe_add_attribute`, `_run_safe_add_module_method`,
    `_run_stand_health_check`) + helpers для агрегации
    findings, нормализации foreign ToolResult'ов и
    программной фильтрации tool-имён через живые registries.
    Cross-app импорты идут только в правильном
    направлении: product layer → read, product layer →
    intelligence, product layer → write. Никакого
    `onec_policy_engine`-импорта.
  - `apps/platform/src/onec_platform/models.py` — добавлены
    `WorkflowStepResult`, `WorkflowPlan`, `WorkflowRunResult`,
    плюс константы `WORKFLOW_NAMES` и `WORKFLOW_MODES`.
    Step 2/3/4 модели не тронуты.
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 7 новыми
    именами; package docstring расширен описанием
    Step 5 surface.
- **Три текущих workflow.**
  - **`safe-add-attribute`.** Поток: build dashboard →
    verdict gate → intelligence
    (`estimate_change_impact`, `suggest_safe_change_order`,
    `suggest_metadata_patch_plan`,
    `summarize_configuration_risk`) → assemble plan →
    confirm gate → реальный
    `add_catalog_attribute` / `add_document_attribute` →
    `verify_attribute_exists` →
    `describe_last_write_operation` →
    `prepare_rollback_hint`. Поддерживаемые `target_kind`:
    `catalog` и `document`.
  - **`safe-add-module-method`.** Поток: build dashboard →
    verdict gate → intelligence (`estimate_change_impact`,
    `find_affected_modules`, `suggest_safe_change_order`,
    `suggest_metadata_patch_plan`,
    `summarize_configuration_risk`) → assemble plan →
    confirm gate → реальный `append_module_method` →
    `verify_module_contains` →
    `describe_last_write_operation` →
    `prepare_rollback_hint`.
  - **`stand-health-check`.** Read-only diagnostic:
    `build_environment_dashboard` + `analyze_runtime_issue`
    + `summarize_configuration_risk`. **Не требует**
    `ready_for_workflows=True`. Никогда не выполняет
    write-side операций. `mode=diagnostic`.
- **Чего на Step 5 намеренно ещё нет (зафиксировано в
  README пакета).** Реального rollback assistant'а
  (Step 6); UI / web-app поверх workflow runner'а;
  hot reload / hot apply / push subscription;
  собственного write channel в `onec_platform`;
  silent apply; параметризованного
  `prepare_intelligence_report` внутри stand-health-check
  (его контракт требует non-empty subject, которого у
  read-only диагностики нет — добавлять синтетический
  subject было бы нечестно); автоматического retry
  упавших mutating step'ов; параметра override-флага для
  `degraded` dashboard'а (это — возможный enhancement
  более позднего шага, не Step 5).
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`run_guided_workflow`,
    `run_guided_workflow_from_json_file`) **никогда не
    бросают**. Любая непредвиденная ошибка runner'а
    оборачивается в `ok=False`, `mode=rejected`, finding
    `workflow_unexpected_error`.
  - `mode` ∈ `{preview, executed, diagnostic, blocked,
    rejected}` — единый источник правды
    `WORKFLOW_MODES`. `ok` плюс `execution_performed`
    дают честную картину: `executed + ok=False` означает
    «mutating step выполнялся и провалился; план и
    intelligence steps сохранены».
  - При сбое mutating step'а workflow runner **не**
    запускает verify (нечего верифицировать), но всё
    равно подтягивает `describe_last_write_operation`
    как best-effort — `audit/.../audit_describe_last_write_operation`
    может вернуть ok=False, если audit-файла ещё нет;
    это нормально и не флипает overall verdict.
  - `confirmed`/`presumed` дисциплина из Phase 4 + Step 4
    сохраняется. Каждый aggregated finding тагирован
    префиксом step name'а (например
    `intelligence_estimate_change_impact/impact_estimate`)
    для трассируемой провенансы.
- **Real-tool-name discipline.** В `WorkflowPlan`
  `suggested_tools` и `suggested_write_tools` фильтруются
  через приватный `_allow_only_real_tools(...)`, который
  проверяет каждое имя по живому объединению трёх
  registries (`mcp_read_server.list_tools()`,
  `mcp_write_server.list_tools()`,
  `mcp_intelligence_server.list_tools()`) плюс
  фиксированному whitelist платформенных
  boundary-функций. Имена, которых нет в этом множестве,
  молча отбрасываются — план не утверждает наличие
  выдуманных tool'ов. Эта дисциплина программно
  проверяется в manual-check сценарии (`assert_real_tool_names`).
- **Safety guarantees Phase 2–4 + Step 2/3/4 — что
  сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в нём, ни в
    `onec_platform` (программный grep + assert в manual
    check).
  - `run_write_flow` остаётся единственным путём к
    mutating операциям. `onec_platform` его **не
    обходит** и не вызывает write-tool'ов в обход
    публичных функций. Каждый mutating step workflow'а
    идёт через `add_catalog_attribute` /
    `add_document_attribute` / `append_module_method`,
    которые сами зовут `run_write_flow`.
  - Audit / snapshots / verify не обходятся: mutating
    write-tool'ы выполняют их сами; workflow runner
    только читает результаты через
    `describe_last_write_operation` /
    `prepare_rollback_hint`.
  - `onec-config`, `onec-policy-engine`, `onec-audit`,
    `onec-health`, `onec-process-runner`,
    `onec-troubleshooting`, `mcp-common`,
    `pyproject.toml`, `.github/`, `selfcheck.py`,
    `bootstrap_paths.ps1` — **не тронуты на Step 5**.
- **Ручная проверка (11 сценариев + 5 sub-сценариев K,
  все зелёные).** Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step5_check.py`
  использует `tempfile.mkdtemp` + локальный
  `http.server.HTTPServer` на свободном `127.0.0.1:<port>`
  для честных read-side вызовов + реальные subprocess'ы
  через Step 3 surface (запускаются при необходимости) +
  реальные write-tool'ы, исполняющиеся против synthetic
  Catalog/Document XML и BSL модулей в tempdir.
  Сценарии:
  - **I. Registry invariants (sanity)** — read=15,
    write=23, intelligence=16; assert.
  - **A. preview safe-add-attribute** — `confirm_execute=False`
    → `mode=preview`, `execution_performed=False`,
    plan содержит реальные tool-имена,
    `write_results=[]`, `last_write_operation=None`.
    Программный assert: ни одного `kind="mutating"` /
    `"verify"` / `"audit"` step'а в preview.
  - **B. execute safe-add-attribute** —
    `confirm_execute=True` → `mode=executed`,
    `execution_performed=True`, write_results[0].ok=True,
    verify_results[0].ok=True, last_write_operation
    populated с реальным `operation_id`, rollback_hint
    populated. Файл XML на диске **реально содержит**
    `name="Title"` и `<Type>String</Type>`.
  - **C1+C2. preview + execute safe-add-module-method**
    — модуль на диске реально содержит имя добавленного
    метода (`PrepareReport`); rollback_hint и
    last_write_operation populated.
  - **D. stand-health-check** — `mode=diagnostic`,
    `execution_performed=False`, suggested_write_tools
    пустой, ни одного mutating step'а.
  - **E. blocked by dashboard** — dump_path не
    существует → dashboard блокирует mutating workflow:
    `mode=blocked`, `ok=False`, `execution_performed=False`,
    в steps только precondition. **E2** проверяет, что
    `stand-health-check` всё равно проходит на
    degraded/dead-HTTP окружении — `mode=diagnostic`,
    `execution_performed=False`.
  - **F. confirm missing → preview only** — без
    `confirm_execute` запуск без всяких write-эффектов:
    catalog XML на диске не модифицирован, audit-каталог
    `.audit/` не создан.
  - **G. underlying write failure** — `attribute_spec.type=
    "BogusType"` → write-tool сам fail-closed'ится
    (whitelisted типы только String/Number/Date) →
    `mode=executed`, `execution_performed=True`,
    `ok=False`. Plan и intelligence steps сохранены;
    verify step **не** добавлен (нет смысла верифицировать
    провалившийся write).
  - **H. registry invariants (final)** — read=15,
    write=23, intelligence=16 после всех сценариев.
  - **J. import discipline** — программный grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/platform/src/**/*.py` → **0 реальных импортов**.
  - **K. rejection paths (5 sub-сценариев)** —
    unknown workflow name; invalid params (target_kind
    не "catalog" / "document"); root config not a dict;
    JSON-file flow happy path (`mode=diagnostic`);
    missing JSON file (`mode=rejected`).
  Все assert'ы прошли с первой попытки (после двух
  cosmetic правок: ASCII arrows вместо `→` для cp1251
  console; включение non-empty `runtime.services` в
  тестовом config'е, чтобы dashboard был `healthy`, а
  не `degraded` из-за `runtime_contract_empty`).
- **MVP-компромиссы Step 5 (зафиксированы честно в
  README).**
  - **Mutating workflow'ы требуют `dashboard.verdict.
    overall_status == "healthy"`** (через
    `ready_for_workflows`). Это значит: пустой
    `runtime.services` → degraded → workflow blocked.
    Это **корректное поведение**: оператор должен
    декларировать runtime контракт. Override-флаг для
    `degraded` — отдельный enhancement, не Step 5.
  - **`stand-health-check` не зовёт
    `prepare_intelligence_report`.** Контракт того
    requires non-empty `subject`, которого у read-only
    диагностики стенда нет; добавлять синтетический
    subject было бы нечестно. Соответствующие сигналы
    уже видны через dashboard и через
    `analyze_runtime_issue` / `summarize_configuration_risk`,
    которые workflow вызывает явно.
  - **При сбое mutating step'а verify не запускается.**
    Сознательно: нет смысла верифицировать
    неприменившееся изменение. `audit/...` step'ы
    остаются best-effort и могут вернуть ok=False,
    если audit-файла ещё нет.
  - **Нет автоматического retry.** Сбой → честный
    `ok=False` с сохранённым планом; решение
    «повторить» — за оператором.
  - **`safe-add-module-method` использует имя метода
    как needle в `estimate_change_impact` /
    `find_affected_modules` /
    `summarize_configuration_risk`.** Это намеренно:
    impact для добавления метода — это где этот символ
    сейчас уже встречается в дампе. Если оператор
    добавляет ранее-не-существующее имя, impact будет
    `none` — это и есть честный сигнал.
  - **Workflow runner не делает структурную валидацию
    `attribute_spec.type` отдельно** — это уже
    делает write-tool. Workflow только формирует
    preview, передаёт в write-tool и честно отображает
    его failure (сценарий G).
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `onec_policy_engine`,
    `onec-config`, `onec-audit`, `onec-health`,
    `onec-process-runner`, `onec-troubleshooting`,
    `mcp-common`.
  - Никакого собственного write channel в `onec_platform`.
  - Никакого silent apply.
  - Никакого UI / web-dashboard / push subscription.
  - Никакого Step 6 rollback / recovery UX (только
    подтягиваем `describe_last_write_operation` и
    `prepare_rollback_hint` для surface их операторам).
  - Никаких изменений `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`, `.github/`.
- **Dev-check после Step 5 зелёный.** `imports_ok =
  true`, `read_server_tools` = 15 (не тронут),
  `write_server_tools` = 23 (не тронут),
  **`intelligence_server_tools` — 16** (не тронут),
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает `onec_platform.workflow` —
  workflow runner опционален для dev-check'а.

### Phase 5 / Step 6 — rollback / recovery / audit UX (завершён)

- **Архитектурная честность Step 6.** Rollback / recovery
  / audit UX — это **read-only product-layer обёртка**
  над уже существующим audit JSONL (write-side append-only
  store) плюс
  `prepare_rollback_hint` /
  `describe_last_write_operation`. Никакого собственного
  write channel в `onec_platform` не появилось: для класса
  операций, у которых **нет** публичного `delete_*`
  write-tool'а (а это сейчас все операции), assistant
  честно отдаёт `mode=unsupported` под `confirm_execute=True`.
  Product layer **не модифицирует** audit JSONL и **не
  переписывает** dump в обход `run_write_flow`.
- **Дисциплина preview / execute.**
  - History viewer и inspect — read-only **всегда**, в
    т.ч. на degraded окружении.
  - Rollback assistant **preview** — read-only всегда; даже
    на degraded окружении preview строится, чтобы оператор
    видел план.
  - Rollback assistant **execution** (`confirm_execute=True`)
    — два независимых gate'а:
    1. Dashboard ready_for_workflows должен быть True;
       иначе → `mode=blocked, ok=False`, preview сохранён.
    2. Tool family должен быть в whitelist
       `_AUTOMATIC_RECOVERY_SUPPORTED`; иначе →
       `mode=unsupported, ok=True`, honest сообщение про
       manual snapshot-restore.
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/recovery.py` — новый
    модуль с тремя boundary-функциями + их `_from_json_file`
    вариантами. Внутри: read-only audit-парсер
    (`_read_audit_lines`, `_parse_audit_lines`), фильтрация
    (`_filter_entries`), сводка (`_summarize`), helper
    `_rollback_hint_payload` для безопасного вызова
    write-server `prepare_rollback_hint`, plan builder
    (`_build_rollback_plan`). Cross-app импорты идут только
    в правильном направлении: product → write (read-only
    helpers `prepare_rollback_hint`,
    `describe_last_write_operation`). **Никакого**
    мутирующего write-tool'а recovery не импортирует.
    Дисциплина имён tool'ов делегирована приватной
    `_allow_only_real_tools(...)` из `workflow.py` Step 5
    — единый источник правды.
  - `apps/platform/src/onec_platform/models.py` — добавлены
    `OperationHistoryEntry`, `OperationHistorySummary`,
    `OperationHistoryResult`, `OperationInspectResult`,
    `RollbackPlan`, `RollbackAssistantResult` + константа
    `RECOVERY_MODES = ("preview", "executed", "blocked",
    "unsupported", "rejected")`. Step 2/3/4/5 модели не
    тронуты.
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 13 новыми
    именами (6 моделей + 1 константа + 6 boundary-функций);
    package docstring расширен описанием Step 6 surface
    с явным указанием на пустой
    `_AUTOMATIC_RECOVERY_SUPPORTED` whitelist.
- **Что Step 6 делает (три boundary-функции).**
  - **`get_operation_history(data, *, limit=None,
    only_status=None)`** — operator-visible audit
    history. Read-only. `ok=True` одинаково покрывает
    «N операций загружено» и «audit файла ещё нет»
    (чистое окружение). Каждая запись normalised в
    `OperationHistoryEntry(position, operation_id,
    tool_name, environment, base_id, status, message,
    raw_line)`. Summary: `total / ok_count / error_count
    / other_count`. Малформированные строки → warning
    findings, не crash.
  - **`inspect_operation(data, *, operation_id)`** —
    focus на одну запись. Подтягивает `prepare_rollback_hint`
    через write-server. Operator summary включает
    `automatic_recovery_supported` явно и snapshot paths.
    Missing operation → `ok=False, operation_found=False`
    (caller ветвится по `operation_found`, не по
    message).
  - **`run_rollback_assistant(data, *, operation_id,
    confirm_execute=False)`** — preview / advisory
    assistant. Mode resolution описан в README продуктового
    слоя; `mode=executed` на Step 6 **недостижим** —
    whitelist пуст.
- **Чего на Step 6 намеренно ещё нет (зафиксировано в
  README пакета).** Автоматического content-level
  rollback'а ни для одного write-tool'а (нет публичных
  `delete_*`); filesystem snapshot-restore тоже **не**
  исполняется автоматически — только surface'ятся
  snapshot-paths и операторские подсказки; модификации
  audit JSONL (он append-only); UI / web frontend / push
  subscription; параллельного writer'а в product layer;
  intelligence-вызовов сверх dashboard'а; CLI / production
  transport у read/write/intelligence; Step 7
  real-stand / 1cv8 integration.
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`get_operation_history`,
    `inspect_operation`, `run_rollback_assistant`, плюс
    `_from_json_file` варианты) **никогда не бросают**.
  - `ok=True` covers honest happy paths: history loaded
    (incl. empty), operation inspected, preview built,
    `mode=unsupported` вернулся честно (assistant
    отказался, не упал).
  - `ok=False` reserved for: invalid inputs, missing
    operation_id in audit, unreadable audit file,
    `mode=blocked` (execution requested but environment
    not ready). Boundary-finding всегда несёт `code` +
    `severity` + `confidence`.
  - Confirmed/presumed дисциплина из Phase 4 + Step 4 + 5
    сохранена. Каждый finding несёт собственный
    `confidence`. Малформированные audit lines идут как
    `severity=warning, confidence=confirmed` (мы реально
    видели битую строку в файле).
- **Real-tool-name discipline.** В `RollbackPlan`
  `suggested_tools` и `suggested_write_tools` фильтруются
  через приватный `_allow_only_real_tools(...)` (импортирован
  из Step 5 workflow-слоя — одна точка истины). Имена
  вне registries молча отбрасываются, чтобы план не
  утверждал наличие выдуманных tool'ов. Эта дисциплина
  программно проверяется в manual-check сценариях C, E.
- **Safety guarantees Phase 2–5 — что сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - `run_write_flow` остаётся единственным путём к
    mutating операциям. Recovery-модуль его **не зовёт**
    и **не обходит**.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в нём, ни в
    `onec_platform` (программный grep + assert в manual
    check, Сценарий M).
  - Audit JSONL — append-only, recovery-модуль только
    читает.
  - `onec-config`, `onec-policy-engine`, `onec-audit`,
    `onec-health`, `onec-process-runner`,
    `onec-troubleshooting`, `mcp-common`,
    `pyproject.toml`, `.github/`, `selfcheck.py`,
    `bootstrap_paths.ps1` — **не тронуты на Step 6**.
- **Ручная проверка (13 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step6_check.py`
  использует `tempfile.mkdtemp` + локальный
  `http.server.HTTPServer` на свободном порту для
  honest health probes + **реальные write-tool вызовы**
  через публичный `add_catalog_attribute`, чтобы audit
  JSONL, который читает recovery, был **настоящий**, а
  не hand-crafted. Сценарии:
  - **L. Registry invariants (sanity)** — read=15,
    write=23, intelligence=16; assert.
  - **A. History viewer happy path с реальными audit
    lines.** Два real-write вызовов
    `add_catalog_attribute` (с distinct snapshot
    label'ами, чтобы избежать collision'ов на уровне
    `_snapshots/backup-…`) → audit JSONL содержит реальные
    JSON-строки. Reading через `get_operation_history` →
    `ok=True`, summary.total>=2, ok_count>=2, оба
    operation_id присутствуют, position монотонна.
  - **N. Filtering** — `only_status="ok"` + `limit=1`
    → ровно 1 запись со status="ok"; `only_status="error"`
    → 0 записей (rejection write3 произошёл pre-flow,
    audit row не появился — это и есть ожидаемое
    поведение).
  - **B. История без audit-файла** — `ok=True, entries=[],
    summary.total=0`, message говорит «empty or absent»
    одинаково.
  - **C. Inspect operation happy path** — найдена запись,
    rollback_hint подтянут, `automatic_recovery_supported=False`,
    operator_summary не пуст, suggested_tools и
    suggested_write_tools проходят real-name assert.
  - **D. Inspect operation: id не в audit log** —
    `ok=False, operation_found=False`. Также: пустой
    `operation_id` → `ok=False, operation_found=False`.
  - **E. Rollback assistant preview** — `mode=preview,
    execution_performed=False, write_results=[],
    plan.automatic_recovery_supported=False`.
    suggested_tools и suggested_write_tools — real names.
  - **F. Confirm missing → preview only** — повторный
    preview-запуск **не модифицирует** ни catalog XML
    на диске, ни audit-файл (длина строк не меняется,
    snapshot файла до и после совпадает).
  - **G. Blocked by dashboard** — `confirm_execute=True`
    + http_url указывает на dead-port → dashboard
    не ready → `mode=blocked, ok=False,
    execution_performed=False`. Preview всё равно
    построен (plan и history_entry присутствуют).
  - **H. Unsupported automatic rollback** —
    `confirm_execute=True` + healthy dashboard + tool
    `add_catalog_attribute` не в whitelist →
    `mode=unsupported, ok=True, execution_performed=False`,
    write_results=[], verify_results=[]. Honest message
    про manual snapshot-restore.
  - **I. Skipped — no executable recovery path** на
    Step 6 (by design).
  - **J. Malformed audit lines** — добавляем в
    реальный audit-файл сначала `{ this is not valid json`,
    потом `"a string, not a dict"`. History viewer
    остаётся `ok=True`, real запись присутствует, две
    warning-finding (`audit_line_invalid_json:1` +
    `audit_line_not_a_dict:2`). Boundary не падает.
  - **K. Suggested-tool discipline** — assert'нуто
    inline в C и E через `assert_real_tool_names(...)`.
  - **M. Import discipline** — программный grep по
    `apps/platform/src/**` + `apps/mcp-intelligence-server/src/**`
    на `^\s*(from|import)\s+onec_policy_engine\b` →
    **0 импортов**.
  - **P. JSON-file flow + rejection paths** —
    `get_operation_history_from_json_file` happy →
    `ok=True`; `inspect_operation_from_json_file` на
    missing JSON → `ok=False`; `run_rollback_assistant`
    на не-dict root → `ok=False, mode=rejected`.
  Все assert'ы прошли (после двух cosmetic правок:
  ASCII arrows вместо `→` для cp1251 console;
  distinct write-tool labels чтобы snapshot
  directory не коллидировал между двумя последовательными
  real-write вызовами).
- **MVP-компромиссы Step 6 (зафиксированы честно в
  README).**
  - **Whitelist `_AUTOMATIC_RECOVERY_SUPPORTED` пуст.**
    Step 6 ship'ит advisory-only. Это **корректное**
    поведение: автоматический content-level rollback без
    публичных `delete_*` write-tool'ов означал бы
    back-door write channel в product layer мимо
    `run_write_flow` / audit / verify. Whitelist
    оставлен в коде как frozenset — будущий шаг
    (или enhancement, когда `delete_*` появятся)
    расширит его без изменения скелета.
  - **Audit JSONL не имеет timestamp'а** — recovery
    использует line-position как стабильный монотонный
    порядок. Это документировано в `OperationHistoryEntry`
    docstring.
  - **Малформированные audit lines пропускаются с
    warning'ом, не abort'ятся.** Operator видит реальные
    записи + честный список «что было пропущено».
  - **Snapshot-restore не автоматизирован.** Suggested
    snapshot paths surface'ятся в plan/operator summary;
    `shutil.copytree`-обратное копирование оператор
    делает сам. Product layer не имеет write channel на
    `dump_path` / `base_path`.
  - **`_allow_only_real_tools` импортирован из
    Step 5 workflow.py** как private symbol. Это
    cross-module import одного помощника между двумя
    sibling-модулями `onec_platform` — не идеальная
    инкапсуляция, но позволяет иметь **один источник
    правды** для tool-name дисциплины. Альтернативы
    (дублирование constants, выделение отдельного
    `_internal.py` module) увеличили бы surface ради
    нулевого product-выигрыша на Step 6.
  - **Connectivity diagnosis / runtime issue / risk
    intelligence** Step 6 берёт через dashboard
    summary, не вызывая sub-tools повторно. Это
    matched сознательное решение Step 4 — sub-tool
    dedup не реализован.
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `onec_policy_engine`,
    `onec-config`, `onec-audit`, `onec-health`,
    `onec-process-runner`, `onec-troubleshooting`,
    `mcp-common`.
  - Никакого собственного write channel в `onec_platform`.
  - Никакого автоматического content-level rollback.
  - Никакого автоматического snapshot-restore.
  - Никакой модификации audit JSONL.
  - Никакого UI / web-dashboard / push subscription.
  - Никакого Step 7 real-stand / 1cv8 integration.
  - Никаких изменений `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`, `.github/`.
- **Dev-check после Step 6 зелёный.** `imports_ok =
  true`, `read_server_tools` = 15 (не тронут),
  `write_server_tools` = 23 (не тронут),
  **`intelligence_server_tools` — 16** (не тронут),
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает `onec_platform.recovery` —
  recovery опционален для dev-check'а.

### Phase 5 / Step 7 — real-stand / 1cv8 binary integration track (завершён)

- **Архитектурная честность Step 7.** Step 7 — это
  **product-layer контракт** для реальной 1cv8 binary
  интеграции и **первый controlled smoke test**, не
  подмена Phase 2 stub'ов и не «полная интеграция за один
  шаг». Phase 2 write-tools (`create_dump_snapshot`,
  `apply_config_from_files`,
  `update_database_configuration`) на Step 7 **не**
  переписываются — флипать их на binary-backed branch
  это параллельный track, не scope этого шага.
- **Дисциплина preview / execute.**
  - Readiness boundary — read-only **всегда**.
  - Smoke test **preview** — read-only всегда; даже на
    not-ready конфиге preview строится.
  - Smoke test **execute** (`confirm_execute=True`) —
    два независимых gate'а:
    1. Readiness verdict должен быть `ready_for_real_stand_smoke=True`;
       иначе → `mode=blocked, ok=False`, plan и steps
       сохранены.
    2. Если readiness ready → execute mode **всегда**
       делает filesystem probe (stat) и **дополнительно**
       стартует subprocess через
       `onec_process_runner.run_process` тогда и только
       тогда, когда оператор задал
       `onec_binary_probe_args`. Платформа не подсказывает
       значения этих аргументов и не «угадывает» 1cv8
       CLI: оператор знает свой стенд.
- **Что реально появилось в коде.**
  - `packages/onec-config/src/onec_config/models.py` —
    `EnvironmentConfig` расширен двумя опциональными
    полями: `onec_binary_path: str | None = None` и
    `onec_binary_probe_args: list[str] | None = None`.
    Default `None` → полная backward compatibility.
  - `packages/onec-config/src/onec_config/loader.py` —
    `load_project_config` парсит обе опциональные строки/
    списки с строгой типовой проверкой: bad shape →
    `ValueError` fail-closed (Сценарий Q manual check'а).
  - `packages/onec-config/README.md` — оба новых поля
    задокументированы.
  - `apps/platform/src/onec_platform/realstand.py` —
    новый модуль с двумя boundary-функциями + их
    `_from_json_file` вариантами + private helper'ами:
    `_inspect_binary` (filesystem-only), `_excerpt`
    (truncate output), `_build_plan_summary`,
    `_readiness_to_step`, `_dashboard_step`. Cross-app
    импорты идут только в правильном направлении:
    product → onec-config, product → onec-process-runner,
    product → дашборд / workflow Step 4/5. **Никакого**
    мутирующего write-tool'а recovery не импортирует.
    `onec_policy_engine` не импортируется.
    `_allow_only_real_tools` импортируется из
    `workflow.py` Step 5 — единая точка истины для
    tool-name дисциплины.
  - `apps/platform/src/onec_platform/models.py` —
    добавлены `RealStandReadinessResult`,
    `RealStandSmokeResult` + константа
    `REAL_STAND_SMOKE_MODES = ("preview", "executed",
    "blocked", "rejected")`. Step 2/3/4/5/6 модели не
    тронуты.
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 7 новыми
    именами (2 модели + 1 константа + 4 boundary-функции);
    package docstring расширен Step 7 surface description
    с явным указанием что Phase 2 stub'ы не
    переписываются.
- **Что Step 7 делает (две boundary-функции).**
  - **`get_real_stand_readiness(data)`** — read-only
    doctor. Проверяет:
    1. `onec_binary_path` declared (не `None`);
    2. файл существует;
    3. это файл, не директория;
    4. на POSIX — есть хоть один executable bit; на
       Windows — любой regular file принимается;
    5. `base_path` существует;
    6. `dump_path` существует;
    7. dashboard verdict не `blocked`.
    Возвращает `ready_for_real_stand_smoke: bool` как
    единый AND-вердикт. Confirmed/presumed findings
    разделены. `presumed_findings` несёт honest signals
    (degraded dashboard, отсутствующие probe args).
  - **`run_real_stand_smoke_test(data, *, confirm_execute=False)`**
    — preview / executed / blocked / rejected. В
    `mode=executed` всегда делает filesystem probe;
    дополнительно стартует subprocess через
    `onec_process_runner.run_process(ProcessRunRequest(...))`
    с timeout 30s и captured output (excerpts cap 1024
    chars). `binary_invoked` — отдельный флаг,
    отличающий «metadata-only execute» от «real subprocess
    execute»: `execution_performed=True, binary_invoked=False`
    означает «filesystem probe прошёл, но probe args не
    заданы — subprocess не стартовал».
- **Уровень реальности на Step 7.** Уровень **2** по
  градации задания: ship'ится **partial binary-backed
  integration**. Real-stand readiness + filesystem probe
  + controlled subprocess invocation (когда operator
  declared) — это настоящие, проверяемые, не-fake
  binary-backed шаги. Phase 2 stub'ы (`create_dump_snapshot`,
  `apply_config_from_files`, `update_database_configuration`)
  на Step 7 **не** переписываются. Полный
  DESIGNER → BackupCfg → DumpCfg → ENTERPRISE round-trip
  **не** реализован — это требует реальной инфобазы и
  больше operator-контракта, чем Step 7 готов ship'ить
  честно.
- **Чего на Step 7 намеренно ещё нет (зафиксировано в
  README пакета).** Перевода Phase 2 stub'ов на
  binary-backed dispatch (параллельный track);
  валидации 1cv8-CLI семантики (operator-driven);
  открытия 1С GUI; full DESIGNER → DumpCfg → ENTERPRISE
  round-trip против реальной инфобазы; новых MCP
  tool'ов в read/write/intelligence; CLI / production
  transport у трёх MCP-серверов; UI / web frontend;
  Step 8 final integration pass.
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`get_real_stand_readiness`,
    `run_real_stand_smoke_test` + `_from_json_file`
    варианты) **никогда не бросают**.
  - `ok=True` covers honest happy paths: readiness
    reported (даже когда `ready=False`), preview built,
    metadata-only executed (без subprocess), real
    subprocess завершился с exit_code=0.
  - `ok=False` reserved for: invalid input / unloadable
    config (`mode=rejected`); execute-mode blocked by
    readiness gate (`mode=blocked`); execute-mode когда
    subprocess вернул non-zero exit или filesystem probe
    провалился (`mode=executed, ok=False`).
  - `ProcessExecutionError` от `onec-process-runner`
    (binary не запустился) обработана внутри: попадает
    в step result + finding, не пробрасывается.
  - Confirmed/presumed дисциплина из Phase 4 + Step 4 +
    5 + 6 сохранена. Каждый finding несёт собственный
    `confidence`. POSIX executable-bit check — confirmed
    fact. Probe-args absence — presumed warning (это
    operator choice, не блокер).
- **Real-tool-name discipline.** В readiness и smoke
  результатах `suggested_tools` и
  `suggested_write_tools` фильтруются через приватный
  `_allow_only_real_tools(...)` (импортирован из Step 5
  workflow-слоя — одна точка истины). Имена вне
  registries молча отбрасываются. На Step 7
  `suggested_write_tools` ограничен read-side audit
  surface'ами (`describe_last_write_operation`,
  `prepare_rollback_hint`) — никаких mutating write-tool
  имён в плане realstand'а нет, потому что real-stand
  smoke сам по себе не делает mutating операций.
- **Safety guarantees Phase 2–6 — что сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - `run_write_flow` остаётся единственным путём к
    mutating операциям в инфобазе. Real-stand boundary
    его **не зовёт** и **не обходит**. Subprocess
    invocation в smoke test'е — это вызов
    operator-declared binary с operator-declared argv,
    вне infobase write surface полностью.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в нём, ни в
    `onec_platform` (программный grep + assert в manual
    check, Сценарий L).
  - `onec-config` — расширен **минимально и backward-compat**
    (две опциональные строки/списка); `selfcheck.py`
    не тронут (он строит env через kwargs которые
    остаются валидными).
  - `onec-policy-engine`, `onec-audit`, `onec-health`,
    `onec-process-runner` (используется как public API,
    без изменений), `onec-troubleshooting`, `mcp-common`,
    `pyproject.toml`, `.github/`, `selfcheck.py`,
    `bootstrap_paths.ps1` — **не тронуты на Step 7**.
- **Ручная проверка (16 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step7_check.py`
  использует `tempfile.mkdtemp` + локальный
  `http.server.HTTPServer` для honest read-side health
  + **`sys.executable` как реальный binary** —
  `python.exe` стал operator-declared `onec_binary_path`,
  а `onec_binary_probe_args=["--version"]` дал
  предсказуемый subprocess. Это честно: реальный binary,
  реальный subprocess, реальный exit code. Сценарии:
  - **K. Registry invariants (sanity)** — read=15,
    write=23, intelligence=16; assert.
  - **M. Backward compat** — продакт-конфиг **без**
    `onec_binary_*` грузится и проходит bootstrap;
    `EnvironmentConfig.onec_binary_path` /
    `onec_binary_probe_args` имеют дефолт `None`.
  - **A. Readiness happy path** — binary configured +
    probe args set + healthy dashboard → `ready=True`.
    Все 4 ok-finding'а present (binary_path_exists,
    binary_probe_args_configured, base_path_exists,
    dump_path_exists, dashboard_healthy).
  - **B. Readiness failure: binary missing** — путь
    указывает на несуществующий файл → `ready=False`,
    `binary_path_missing` error finding,
    recommended_actions не пуст.
  - **B'. Readiness failure: not configured** —
    `onec_binary_path=None` → `ready=False`,
    `binary_path_not_configured` error finding.
  - **C. Readiness failure: dir** — путь указывает на
    директорию → `ready=False, binary_present=True,
    executable_like=False, binary_path_is_directory`.
  - **D. Smoke preview on ready config** —
    `mode=preview, execution_performed=False, binary_invoked=False`.
    Plan summary не пуст. Ни одного `executed` step'а в
    preview.
  - **E. Smoke preview on not-ready config** — preview
    всё равно строится; `ready=False`,
    `execution_performed=False`, никаких subprocess.
  - **F. Confirm missing → preview only**.
  - **G. Blocked by readiness** — `confirm_execute=True`
    + binary missing → `mode=blocked, ok=False,
    execution_performed=False, binary_invoked=False`.
  - **H. Confirmed execution metadata-only** — ready +
    no probe args → `mode=executed,
    execution_performed=True, binary_invoked=False`.
    Filesystem probe step ok=True. Subprocess не
    стартовал.
  - **I. Confirmed execution: real subprocess** —
    `[sys.executable, "--version"]` через
    `onec_process_runner` → `mode=executed, ok=True,
    execution_performed=True, binary_invoked=True,
    binary_exit_code=0`. `binary_stdout_excerpt`
    содержит "Python 3.14.4\n". binary_probe step
    ok=True. **Это настоящий subprocess invocation, не
    fake.**
  - **J. Underlying binary failure** —
    `[sys.executable, "-c", "import sys; sys.exit(7)"]`
    → `mode=executed, ok=False, binary_invoked=True,
    binary_exit_code=7`. Plan и steps preserved;
    binary_probe step ok=False.
  - **L. Import discipline** — grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/platform/src/**` + `apps/mcp-intelligence-server/src/**`
    → **0 импортов** ✓.
  - **P. JSON-file flow + rejection paths** —
    `get_real_stand_readiness_from_json_file` happy →
    `ok=True, ready=True`;
    `run_real_stand_smoke_test_from_json_file` preview →
    `mode=preview`; missing JSON → `ok=False`;
    non-dict root → `ok=False, mode=rejected`.
  - **Q. Shape validation** — bad
    `onec_binary_probe_args` (`[42, "ok"]`) → loader
    рейзит `ValueError` с конкретным указанием на
    `onec_binary_probe_args` и тип `int`.
  Все assert'ы прошли с первой попытки.
- **MVP-компромиссы Step 7 (зафиксированы честно в
  README).**
  - **Phase 2 stub'ы (`create_dump_snapshot`,
    `apply_config_from_files`,
    `update_database_configuration`) не переписаны.**
    Их evolution на binary-backed dispatch с
    `onec_binary_path` — параллельный track, не Step 7.
    Это сознательный compromise: Step 7 ship'ит
    **product-layer контракт + smoke test**, а не
    одновременно invasive write-tool refactor.
  - **Платформа не валидирует семантику
    `onec_binary_probe_args`.** Operator owns the
    choice. Если probe args открывают GUI или
    блокируют — таймаут 30s принудительно завершит
    subprocess, но платформа не пытается «угадать»
    safe args для произвольной версии 1cv8.
  - **На Windows executable-bit check не делается.**
    Windows не экспонирует POSIX-биты; любой regular
    file принимается. На POSIX отсутствие executable
    bit'а даёт warning, не blocking-error (operator
    может намеренно использовать interpreter-style
    binary).
  - **Smoke test ловит только один subprocess
    invocation.** Multi-step smoke (DESIGNER → DumpCfg
    → ENTERPRISE) требует state-machine и реальной
    инфобазы; это out-of-scope.
  - **Output excerpts cap 1024 chars.** Полные логи —
    operator's responsibility (через свой observability
    стек). Платформа не транслирует arbitrary subprocess
    output upstream.
  - **Timeout 30s — fixed**, не настраивается из
    config. Если operator'у нужен другой таймаут — это
    enhancement future-step'а; на Step 7 фиксированный
    cap честнее, чем шириной surface ради «гибкости».
  - **`_allow_only_real_tools` импортирован из Step 5
    `workflow.py`** как private symbol — sibling-модули
    `onec_platform` шарят один источник правды для
    tool-name дисциплины. Та же oversight, что и в
    Step 6: продолжаем тот же compromise, не вводя
    новый `_internal.py` ради нулевого выигрыша.
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `onec_policy_engine`,
    `onec-audit`, `onec-health`, `onec-troubleshooting`,
    `mcp-common`. `onec-config` расширен **минимально**
    (две опциональные строки/списка), backward-compat
    полная.
  - Никакого собственного write channel в `onec_platform`.
  - Никакой записи в инфобазу из realstand boundary.
  - Никакого UI / web-dashboard / push subscription.
  - Никакого Step 8 final integration pass.
  - Никаких изменений `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`, `.github/`.
  - Не переписаны Phase 2 stub'ы (`create_dump_snapshot`
    / `apply_config_from_files` /
    `update_database_configuration`). Это
    **сознательное** out-of-scope, явно зафиксированное
    в README + plan_summary каждого smoke test'а.
- **Dev-check после Step 7 зелёный.** `imports_ok =
  true`, `read_server_tools` = 15 (не тронут),
  `write_server_tools` = 23 (не тронут),
  **`intelligence_server_tools` — 16** (не тронут),
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает `onec_platform.realstand` —
  realstand опционален для dev-check'а.

### Phase 5 / Step 8 — final integration pass (завершён, Phase 5 закрыт)

- **Step 8 — закрывающий, документационный по сути шаг.**
  Сквозной интеграционный прогон прошёл **без правок
  кода** в репозитории: всё, что собиралось на Step 2–7,
  реально склеилось в один продуктовый контур поверх
  существующих read/write/intelligence-серверов.
  Кодовых изменений на Step 8 нет; обновлены только
  `apps/platform/README.md`, корневой `README.md`,
  `PROJECT-STATUS.md`.
- **Что подтвердил интеграционный прогон.** Один
  сквозной Scenario A на временном synthetic-окружении
  (`tempfile.mkdtemp` + локальный in-process
  `http.server.HTTPServer` + реальные subprocess'ы для
  runtime-сервисов и real-stand smoke probe). Реальный
  стенд **не трогался**.
  - **A.1 `bootstrap_product`** → `ok=True`,
    `doctor.error_count=0`.
  - **A.2 `start_product_runtime`** → 3 сервиса реально
    стартовали (`running × 3`), PID'ы реально живые
    (`is_pid_alive` проверен). `get_product_runtime_status`
    отдаёт `running × 3`.
  - **A.3 `build_environment_dashboard`** (Step 4
    boundary) → 6 секций, verdict `healthy`,
    `ready_for_workflows=True`.
  - **A.4 `run_guided_workflow safe-add-attribute`
    `confirm_execute=True`** → реально дописал атрибут
    `Title` в `Catalogs/Items.xml` через **существующий**
    public write-tool `add_catalog_attribute`, который
    сам прошёл через `run_write_flow` (preflight →
    snapshot → operation → verify → audit).
    `verify_attribute_exists` подтвердил наличие на
    диске. `last_write_operation` и `rollback_hint`
    populated.
  - **A.5 `get_operation_history`** → видит реальную
    audit запись с тем же `operation_id`.
  - **A.6 `inspect_operation`** → `operation_found=True`,
    rollback hint приложен, `automatic_recovery_supported=False`
    (Step 6 advisory-only).
  - **A.7 `run_rollback_assistant`** preview → `mode=preview`,
    `execution_performed=False`, никаких write-эффектов.
  - **A.8 `get_real_stand_readiness`** →
    `ready_for_real_stand_smoke=True`,
    `binary_present=True`, `has_probe_args=True`.
  - **A.9 `run_real_stand_smoke_test`
    `confirm_execute=True`** → **реальный** subprocess
    через `onec_process_runner.run_process` запустился
    (`binary_invoked=True, binary_exit_code=0`,
    stdout содержит `Python`).
  - **A.10 `stop_product_runtime`** → все три PID'а
    реально мертвы.
- **Failure paths (4 сценария, все зелёные).**
  - **F1 — workflow blocked by dashboard.** `dump_path`
    отсутствует → `mode=blocked, ok=False,
    execution_performed=False`. Ни одного `mutating /
    verify / audit` step'а в steps.
  - **F2 — rollback assistant unsupported.**
    `confirm_execute=True` на здоровом окружении →
    `mode=unsupported, ok=True,
    execution_performed=False`,
    `automatic_recovery_supported=False`. Catalog XML
    после попытки **не изменился** (программный
    assert на содержимое файла до и после).
  - **F3 — broken JSON config.** Все 9
    `_from_json_file` boundary-функций (`bootstrap`,
    `start`, `dashboard`, `workflow`, `history`,
    `inspect`, `rollback`, `readiness`, `smoke`)
    одинаково отдают `ok=False`. Никаких исключений
    наружу.
  - **F4 — malformed audit line.** В реальный audit
    JSONL дописали `{ this is not valid json` и
    `"a string, not a dict"`; history viewer остаётся
    `ok=True`, реальная запись присутствует, malformed
    строки попадают в `findings` как warnings
    (`audit_line_invalid_json:*`,
    `audit_line_not_a_dict:*`). Boundary не упал.
- **Discipline asserts (программно подтверждены).**
  - **Registry invariants:** `read=15`, `write=23`,
    `intelligence=16` до и после интеграционного
    прогона.
  - **Real-tool-name discipline:** все имена в
    `suggested_tools` / `suggested_write_tools`
    workflow plan, inspect result, rollback plan,
    readiness, smoke result — реальные имена, живущие
    в одном из трёх registries или whitelist'е
    product-layer boundary-функций. Программные
    `assert_only_real_tool_names(...)` для каждого
    payload'а.
  - **Import discipline:** grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/platform/src/**` и
    `apps/mcp-intelligence-server/src/**` — **0
    реальных импортов** (assert).
  - **No exception leakage:** boundary-функции
    product layer ни в одном из 14+ под-сценариев не
    выбросили исключение наружу.
- **Что Step 8 не делал (намеренно).**
  - **Не правил код.** Интеграционный прогон прошёл
    out-of-the-box; кодовые изменения не потребовались.
  - **Не расширял scope.** Никаких новых MCP tool'ов,
    никаких новых модулей, никаких изменений в
    registries трёх MCP-серверов.
  - **Не переписывал Phase 2 stub'ы.** Step 7 уже
    зафиксировал текущий уровень реальности; Step 8 —
    интеграция, не новый binary track.
  - **Не вводил новый write channel в `onec_platform`.**
    Все mutating-эффекты по-прежнему идут через
    публичные write-tool'ы → `run_write_flow`.
  - **Не «полировал» документацию ради красоты.**
    Обновлены только три файла (`apps/platform/README.md`,
    корневой `README.md`, `PROJECT-STATUS.md`), и
    только по сути: маркировка Phase 5 как закрытой,
    Step 8 record, явный список оставшихся
    стратегических хвостов.
- **Safety guarantees Phase 2–7 — что сохраняется.**
  - Read=15, write=23, intelligence=16 — без изменений.
  - `run_write_flow` остаётся единственным путём к
    mutating операциям в инфобазе.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в
    intelligence-server, ни в product layer (программно
    проверено grep'ом).
  - Audit JSONL append-only; product layer его только
    читает.
  - Никакого silent apply, никакого обхода snapshots /
    verify / audit.
- **Dev-check после Step 8 зелёный.** `imports_ok=true`,
  `read_server_tools` = 15, `write_server_tools` = 23,
  `intelligence_server_tools` = 16, `selfcheck_status=ok`,
  `Dev check completed successfully.`.

## Phase 5 закрыт

Phase 5 / Product Layer **закрыт** на Step 8 final
integration pass.

В составе закрытой фазы:

- **Step 1** — planning Product Layer (документационный
  вход).
- **Step 2** — installer / bootstrap contract:
  product-config schema, JSON loader, prereqs doctor,
  bootstrap entrypoint.
- **Step 3** — runtime orchestration / single entry
  point: декларативный runtime-контракт, атомарный
  state-файл, cross-platform PID-liveness, четыре
  boundary-функции (`start_product_runtime` /
  `stop_product_runtime` / `get_product_runtime_status` /
  `reload_product_runtime`).
- **Step 4** — environment doctor / health dashboard:
  единый read-only aggregator над bootstrap +
  runtime + read.check_runtime_health +
  read.diagnose_connectivity_issue +
  intelligence.analyze_runtime_issue +
  intelligence.summarize_configuration_risk;
  rule-based verdict (`healthy` / `degraded` /
  `blocked`) + `ready_for_workflows`.
- **Step 5** — guided workflow layer: три
  end-to-end workflow'а (`safe-add-attribute`,
  `safe-add-module-method`, `stand-health-check`) с
  обязательным confirm gate, mutating-исполнение
  через существующие public write-tool'ы → `run_write_flow`.
- **Step 6** — rollback / recovery / audit UX: три
  boundary-функции (`get_operation_history`,
  `inspect_operation`, `run_rollback_assistant`),
  preview / advisory by default, **advisory-only**
  для всех current write-tool families
  (`_AUTOMATIC_RECOVERY_SUPPORTED` whitelist пуст:
  нет публичных `delete_*` write-tool'ов).
- **Step 7** — real-stand / 1cv8 binary integration
  track: optional contract в `onec-config`
  (`onec_binary_path`, `onec_binary_probe_args`),
  readiness boundary + smoke test boundary с
  **реальным** controlled subprocess через
  `onec_process_runner`. Phase 2 stub'ы не
  переписываются — это параллельный track.
- **Step 8** — final integration pass: один
  сквозной Scenario A + 4 failure paths, без
  правок кода.

**Закрытие Phase 5 не означает**, что продукт уже
полностью industrial-grade / enterprise-ready. Это
означает, что у платформы теперь есть цельный
**product-layer контур** поверх существующих
read/write/intelligence-серверов, с честно
зафиксированными границами и безопасными
гарантиями.

### Phase 6 / Step 1 — planning Industrialization & Completion Track (завершён)

- **Стратегический сдвиг.** После закрытых Phase 1–5
  у платформы есть полное инженерное ядро (read/
  write/intelligence) и работающий product-layer
  контур (bootstrap, runtime, dashboard, workflows,
  recovery, real-stand smoke). Это **не** ещё
  финальный индустриальный продукт. Phase 6 —
  специально выделенная фаза доведения продукта до
  finished / deployable состояния, а не очередное
  расширение MCP tool surface. Это закрытие
  разрыва между «у нас сильное ядро + работающий
  product-layer контур» и «это можно установить,
  запустить, использовать, поддерживать и передать
  другому человеку как реальный индустриальный
  продукт».
- **Создано два новых документа в
  `docs/architecture/`.**
  - `docs/architecture/phase-6-industrialization-plan.md`
    — основной план фазы. Содержит: назначение
    фазы (почему после закрытых Phase 1–5 нужна
    именно отдельная фаза industrialization /
    completion); целевой результат в терминах
    finished product behavior на reference stand'е
    (8-пунктовый нарратив от release artifact до
    operator handoff); прямой mapping 10
    стратегических разрывов на блоки фазы (что
    закрывается полностью, что частично, что
    сознательно выносится за пределы); сравнение
    Phase 6 с Phase 1–5 (адресат — человек +
    reference stand, фокус — завершённость, не
    surface expansion); шесть продуктовых блоков
    (A — real 1cv8 execution; B — full rollback /
    recovery; C — installer / packaging; D —
    metadata completion / structural editing; E —
    runtime hardening; F — operator UX / docs;
    G — enterprise foundation); guardrails;
    явный «что НЕ входит в фазу»; **10**
    проверяемых критериев приёмки; раздел
    открытых вопросов для Step 2+.
  - `docs/architecture/phase-6-step-map.md` —
    стартовая карта фазы из 8 шагов в едином
    формате (Цель / Что меняем / Затронутые зоны /
    Результат): Step 1 — planning; Step 2 — real
    1cv8 execution contract; Step 3 — installer /
    packaging / setup fast path; Step 4 — rollback
    execution track; Step 5 — metadata completion
    / structural editing; Step 6 — runtime
    hardening / supervision / logs; Step 7 —
    real-stand end-to-end validation + docs /
    runbooks; Step 8 — final integration pass и
    закрытие Phase 6.
- **Ключевые продуктовые блоки, зафиксированные в
  плане (A–G).**
  - **A. Real 1cv8-backed execution track.** Замена
    одного Phase 2 stub-backed пути
    (`create_dump_snapshot` /
    `apply_config_from_files` /
    `update_database_configuration`) на реальный
    binary-backed dispatch через `onec_binary_path`
    + `onec-process-runner`. Stub-режим остаётся
    как honest fallback. **Полное замещение всех
    stub'ов в одной фазе не обещается** — это
    parallel track после Phase 6.
  - **B. Full rollback / recovery track.**
    Перевод rollback assistant из advisory-only в
    реально исполнимый хотя бы для одного класса
    write-tool'ов. `_AUTOMATIC_RECOVERY_SUPPORTED`
    whitelist пополняется хотя бы одним именем.
    Mutating recovery — через существующую
    write-дисциплину или её честное эволюционное
    расширение, без back-door channel'а.
  - **C. Installer / packaging / operator startup
    polish.** Документированный install runbook ≤
    5 ручных шагов; declarative product-config
    template; release artifact format фиксируется
    в Step 3.
  - **D. Metadata completion / structural editing
    track.** Точечный добор metadata coverage и
    первый шаг к настоящему structural editing
    (один whitelisted DOM-edit для XML-блока).
    Полный AST остаётся out of scope.
  - **E. Runtime hardening / process supervision.**
    Лог-capture с ротацией для дочерних сервисов
    (вместо текущего `DEVNULL`); базовая restart
    policy (operator-driven, не automatic
    supervisor); более внятный runtime UX. Hot
    reload остаётся out of scope.
  - **F. Operator UX / docs / runbooks.** Standalone
    `docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`, user-facing
    message style guide, runbooks для типовых
    сценариев — **вне README**, пригодные для
    передачи другому инженеру.
  - **G. Enterprise / production hardening
    foundation.** Только foundation: declarative
    policy surface поверх существующего
    `onec-policy-engine`, audit retention policy,
    deployment discipline. **Полная
    enterprise-вселенная** (SSO/RBAC, multi-tenant,
    secrets vault, federated audit, policy-as-code
    DSL, multi-instance HA) — out of Phase 6.
- **Какие стратегические разрывы закрывает
  Phase 6.** Полностью закрываются: разрыв (2)
  installer/setup, (7) operator/admin/developer
  UX уровня «можно отдать другому человеку»,
  (10) «всё это поверх готового ядра, не ломая
  его» (фиксируется как guardrail). Частично
  закрываются: (1) реальная 1cv8 binary
  integration — **один** stub-backed путь
  переводится; (3) полная rollback / recovery —
  **один** класс становится исполнимым; (4) full
  metadata coverage — точечный добор; (5) full
  XML/BSL structural editing — первый шаг,
  не AST-парсер; (6) stable real-stand
  end-to-end — один сценарий проходит на
  reference stand'е; (8) runtime hardening —
  логи + базовая restart policy. Сознательно
  выносится за пределы: (9) полный enterprise
  super-set — отдельный enterprise track после
  Phase 6.
- **Guardrails Phase 6 (зафиксированы в плане).**
  Никакого размывания safety guarantees Phase 2–5;
  никакого back-door write channel в product
  layer; mutating путь только через существующую
  write-дисциплину или её честное эволюционное
  расширение; intelligence остаётся read-only;
  `onec_policy_engine` не импортируется ни в
  intelligence, ни в product layer; fail-closed
  по умолчанию; никакой фальшивой
  enterprise-ready риторики; честно отделять
  finished product behavior от parallel
  follow-up / enterprise track; dev-check
  зелёный после каждого кодового шага; registry
  трёх MCP-серверов меняется только при реальной
  необходимости (Step 4 / Step 5 могут добавить
  один-два новых write-tool'а — это документируется
  честно).
- **Что не входит в Phase 6 (зафиксировано
  явно).** Полный enterprise super-set; полностью
  автономный агент; полный AST-парсер XML / BSL;
  web-UI / dashboard frontend; полная замена всех
  Phase 2 stub'ов одновременно; полная
  rollback-вселенная для всех write-tool family'й;
  полное metadata coverage; production MCP
  transport / `__main__` / CLI у трёх серверов;
  hot reload без рестарта; OS-level service
  supervision (Windows Service / systemd unit);
  GUI installer / wizard; многосторонний
  end-to-end на матрице 1С версий и стендов.
- **10 проверяемых критериев приёмки Phase 6.**
  (1) Один Phase 2 stub-backed путь имеет
  binary-backed dispatch при наличии
  `onec_binary_path`; явный маркер `mode` в
  payload. (2) `_AUTOMATIC_RECOVERY_SUPPORTED`
  whitelist содержит ≥ 1 имя; `confirm_execute=True`
  достигает `mode=executed`; verify проверен;
  audit row написан. (3) Install runbook ≤ 5
  ручных шагов от «получил релиз» до «bootstrap
  doctor зелёный». (4) Один end-to-end real-stand
  сценарий проходит от setup до smoke с реальной
  binary-backed apply. (5) Standalone
  operator/admin/developer manuals + runbooks
  существуют **вне** README. (6) read=15+ /
  write=23+ / intelligence=16 (intelligence —
  hard guarantee). (7) dev-check зелёный после
  каждого кодового шага. (8) Safety guarantees
  Phase 2–5 сохранены (программный grep). (9)
  Honest fallback дисциплина: никакого silent
  skip / fake success. (10) Документированные
  ограничения честны: каждый шаг явно указывает,
  что parallel-track'ом, какие MVP-компромиссы.
- **Что изменилось в коде Step 1.** **Ничего.**
  Ни одной строчки. `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `.github/`,
  `.claude.json` — не тронуты. Registry'ы read
  (15), write (23), intelligence (16) не
  менялись. Dev-check остаётся в том же зелёном
  состоянии, что и после Phase 5 / Step 8.
- **Обновлены документы.**
  - Корневой `README.md`: Phase 5 остаётся в
    блоке закрытых фаз; Phase 6 помечена как
    активная фаза с подробным описанием цели
    (Industrialization & Completion Track,
    шесть блоков A–G, 10 критериев приёмки,
    явное «не очередное расширение MCP tool
    surface»); добавлены ссылки на оба новых
    документа (`phase-6-industrialization-plan.md`,
    `phase-6-step-map.md`); абзац про Phase 6 в
    блоке «Текущий статус по фазам» явно
    подчёркивает, что закрытие Phase 6 не
    означает полностью industrial-grade /
    enterprise-ready состояние.
  - `PROJECT-STATUS.md`: обновлены шапка
    (текущий шаг → Phase 6 / Step 1, статус →
    in progress); Step 8 Phase 5 остаётся
    помеченным как «завершён, Phase 5 закрыт»;
    добавлен подробный Step 1 record (этот
    блок); обновлена секция «Следующий шаг» под
    Phase 6 / Step 2; в нижних «Крупные этапы»
    Phase 6 → «Активная фаза».
- **Открытые вопросы Step 1 (для Step 2+).** В
  плане явно зафиксированы вопросы, на которые
  Step 1 не даёт окончательного ответа: какой
  Phase 2 stub-backed путь переводится первым;
  контракт 1cv8 CLI (режимы / args / timeout);
  формат релизного артефакта (zip / tar / wheel
  / git tag / standalone-script); какой класс
  recovery ship'ится первым; какие
  metadata-tool'ы добавляются (или ни одного);
  формат лог-файлов runtime services; уровень
  structural editing в block D; глубина
  enterprise foundation в block G. Step 1 не
  делает вид, что ответы уже найдены.

### Phase 6 / Step 2 — contract for real 1cv8 execution / config surface (завершён)

- **Архитектурное решение Step 2.** Из трёх кандидатов
  (`create_dump_snapshot` / `apply_config_from_files` /
  `update_database_configuration`) первым переведён на
  binary-backed dispatch именно **`create_dump_snapshot`**.
  Причины: он наиболее изолирован (создаёт каталог под
  `_snapshots`, не правит сам dump / infobase); его
  поведение естественно связано со snapshot discipline;
  он менее опасен, чем сразу лезть в apply / update-db.
  `apply_config_from_files` и `update_database_configuration`
  на Step 2 **не** тронуты — это будут отдельные шаги
  Phase 6 / parallel track'и после.
- **Что реально появилось в коде.**
  - `packages/onec-config/src/onec_config/models.py` —
    `EnvironmentConfig` расширен одним опциональным полем
    `onec_dumpcfg_command_template: list[str] | None = None`.
    Default `None`. Полная backward compatibility.
  - `packages/onec-config/src/onec_config/loader.py` —
    `load_project_config` парсит новое поле с **строгой
    типовой валидацией**: bad shape (не list / non-string
    item / пустой list) → `ValueError` fail-closed на
    этапе загрузки.
  - `packages/onec-config/README.md` — задокументировано
    новое поле + добавлена секция «Философия
    binary-related полей» (operator-owned execution
    contract; платформа не угадывает 1cv8 CLI grammar;
    fail-closed на любую ошибку в этих полях).
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`:
    - добавлены константы:
      - `_DUMPCFG_TEMPLATE_PLACEHOLDERS = frozenset({
        "binary_path", "output_path", "base_path",
        "base_id", "publication_name", "http_base_url"})`;
      - `_DUMPCFG_OUTPUT_EXCERPT_LIMIT = 1024`;
      - `_DUMPCFG_DEFAULT_TIMEOUT_SECONDS = 300` (cap
        выше Phase 5 / Step 7 30s, потому что real
        DumpCfg может идти заметно дольше).
    - private helper'ы:
      - `_render_dumpcfg_command(template, *,
        environment, binary_path, output_path)` —
        безопасный per-item `str.format_map`-style
        рендер. Через `_PlaceholderProxy`-dict с
        `__missing__`, который рейзит
        `_UnknownPlaceholderError` для unknown
        placeholder'ов. Boundary конвертит это в
        `ValueError` с понятным сообщением и списком
        allowed placeholders.
      - `_excerpt(text)` — обрезает stdout/stderr до
        cap'а с маркером `...[truncated]`.
    - private dispatch helper'ы:
      - `_create_dump_snapshot_stub(...)` — оригинальный
        Phase 2 / Step 5 путь (marker file +
        dump-meta.json), payload теперь несёт явный
        `mode = "stub"`, `binary_invoked = False`;
      - `_create_dump_snapshot_binary_backed(...)` —
        новый путь: рендер argv → run_process с
        timeout 300s → captured exit_code +
        stdout/stderr excerpts → запись
        `dump-meta.json` с `mode = "binary-backed"` +
        `command_preview`.
    - public `create_dump_snapshot(environment, label)`
      превратилась в тонкий dispatcher:
      preflight → resolve target_dir → if (
      `environment.onec_binary_path` AND
      `environment.onec_dumpcfg_command_template`)
      → binary-backed branch; иначе → stub branch.
      Внешний контракт `ToolResult` сохранён.
  - `apps/mcp-write-server/README.md` — обновлён раздел
    `create_dump_snapshot`: оба режима задокументированы
    с явным указанием, что между ними есть **только
    config-time fallback** (одно из полей отсутствует
    → stub); **runtime fallback запрещён** (если
    binary-backed subprocess вернул non-zero,
    `ok=False`, никакого silent перезапуска). Также
    явно зафиксировано, что `apply_config_from_files`
    и `update_database_configuration` на Step 2 **не**
    тронуты.
  - Корневой `README.md` — Phase 6 абзац дополнен
    кратким описанием Step 2 (новый partial slice,
    operator-owned argv template, whitelisted
    placeholders, fixed timeout 300s, no
    runtime-fallback).
- **Расширение payload (внешний контракт сохранён).**
  `ToolResult` shape не менялся, но `payload.data` теперь
  всегда несёт:
  - `mode: "stub" | "binary-backed"`;
  - `binary_invoked: bool`;
  - `snapshot_path` (как и раньше);
  - в binary-backed режиме дополнительно:
    `exit_code`, `completed`, `command_preview`
    (рендерённый argv), `stdout_excerpt`,
    `stderr_excerpt`.
  Excerpts cap 1024 chars: операторские полные логи
  остаются ответственностью самого operator'а через его
  observability стек.
- **Дисциплина fallback'а.**
  - **Config-time fallback:** если хотя бы одно из
    полей (`onec_binary_path`,
    `onec_dumpcfg_command_template`) не задано —
    stub mode. Это **сохраняет полную backward
    compatibility** с Phase 1–5: все существующие
    конфиги, не объявляющие новые поля, работают
    как и раньше.
  - **Runtime-fallback запрещён.** Если operator
    объявил binary-backed контракт и subprocess
    завершился non-zero (или не стартовал) — `ok=False`,
    `mode="binary-backed"`, никакого silent перезапуска
    stub'а. Это явная требование задания Step 2 и
    зафиксировано в коде / README.
  - **Render fail-closed.** Unknown placeholder в
    template → `ok=False`, `binary_invoked=False`,
    subprocess не стартует, message включает список
    allowed placeholders.
- **Safety guarantees Phase 2–5 — что сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - `run_write_flow` остаётся единственной точкой входа
    к mutating операциям. `create_dump_snapshot` —
    обычный public write-tool группы A; mutating
    write-tool'ы группы B автоматически наследуют
    binary-backed snapshot stage через свой штатный
    `run_write_flow` (это подтверждено integration
    smoke сценарием F: `update_module_code` через
    flow реально использовал binary-backed branch и
    flow завершился `stage=completed`).
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` в продуктовом слое и
    intelligence-server по-прежнему не импортируется.
  - Никакого собственного write channel вне
    write-server'а.
  - Никакой `shell=True` — argv list only через
    `onec_process_runner.run_process`.
  - Никакого 1cv8-CLI guessing: render placeholder'ов
    жёстко whitelisted; argv item'ы — operator
    declaration as-is; платформа не добавляет
    «полезных» дефолтов.
  - `selfcheck.py` не тронут.
  - `apps/`, `scripts/`, `pyproject.toml`, `.github/`,
    `apps/mcp-read-server/**`,
    `apps/mcp-intelligence-server/**`,
    `apps/platform/**` — **не трогали** (только
    `apps/mcp-write-server/{tools.py,README.md}` +
    `packages/onec-config/{models.py,loader.py,README.md}`
    + `README.md` + `PROJECT-STATUS.md`).
- **Ручная проверка (7 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\phase6_step2_check.py`
  использует `tempfile.mkdtemp` + локальный in-process
  HTTP server + **`sys.executable` как реальный
  binary** с argv `python -c "..."`. Сценарии:
  - **A. Backward compat** — конфиг без
    `onec_dumpcfg_command_template` → `mode="stub"`,
    `ok=True`, `binary_invoked=False`. Marker
    `dump-created.txt` создан как раньше.
  - **B. Happy binary-backed path** — argv template:
    `[{binary_path}, "-c", "...write binary-marker.txt
    inside {output_path}...", {output_path},
    {base_id}]` → `ok=True, mode="binary-backed",
    binary_invoked=True, exit_code=0`. Файл
    `binary-marker.txt` реально создан subprocess'ом
    внутри snapshot-каталога. `dump-meta.json`
    помечен `mode="binary-backed"`. `command_preview`
    содержит реальный путь к python.exe и
    подставленные `{output_path}` / `{base_id}`.
    `stdout_excerpt = "snapshot for local-dev\n"`.
  - **C. Binary-backed runtime failure** — argv
    `[{binary_path}, "-c", "import sys;
    sys.exit(7)", {output_path}]` → `ok=False,
    mode="binary-backed", binary_invoked=True,
    exit_code=7`. **No fallback to stub**: внутри
    snapshot-каталога **нет** `dump-created.txt` и
    **нет** `dump-meta.json` (stub-marker'ы не
    создаются после binary-backed failure).
  - **D. Bad template shape rejected by loader** —
    три sub-сценария: `"string-not-a-list"` →
    `ValueError "must be a list of strings"`;
    `[42, "ok"]` → `ValueError "must contain only
    strings; got int"`; `[]` → `ValueError "must not
    be empty"`. Все fail-closed на этапе loader'а.
  - **E. Unknown placeholder** —
    `[{binary_path}, "-c", "print('hi')",
    {not_a_real_placeholder}]` → `ok=False,
    binary_invoked=False`. Subprocess не стартовал.
    Message: `Unknown placeholder
    {not_a_real_placeholder} in
    onec_dumpcfg_command_template; allowed
    placeholders are: ['base_id', 'base_path',
    'binary_path', 'http_base_url', 'output_path',
    'publication_name']`. Внутри snapshot-каталога —
    никаких marker'ов.
  - **F. Integration smoke через `run_write_flow`** —
    `update_module_code(env, "CommonModules/Helpers
    /Ext/Module.bsl", new_text=...)` с
    binary-backed конфигом. Результат:
    `ok=True`, `tool_name="update_module_code"`
    (tool_name discipline preserved),
    `flow_data.stage="completed"`. Snapshot
    каталог `_snapshots/dump-local-dev-*` реально
    содержит `flow-marker.txt` (= proof, что
    binary-backed branch ran inside the flow);
    **отсутствует** `dump-created.txt` (= proof,
    что stub branch не использовался). Audit row
    `tool_name="update_module_code", status="ok"`
    написан в `dump/.audit/audit.jsonl`.
  - **G. Registry invariants** до и после: read=15,
    write=23, intelligence=16. assert.
- **MVP-компромиссы Step 2 (зафиксированы честно).**
  - **Только один stub переведён.**
    `create_dump_snapshot` — единственный путь, который
    Step 2 переводит на binary-backed dispatch.
    `apply_config_from_files` /
    `update_database_configuration` остаются как
    stub'ы; их перевод — отдельные будущие шаги
    Phase 6 (или parallel-track после), как явно
    задокументировано в README write-server'а.
  - **Литеральные `{`/`}` в operator argv не
    поддерживаются.** `str.format_map`-style рендер
    не позволяет легко передать литеральные
    фигурные скобки в значения; на MVP-уровне это
    приемлемо, потому что 1cv8 в документированных
    DumpCfg-флагах их не использует. Если когда-нибудь
    оператору это понадобится — он pre-render'ит
    argv сам перед декларацией. Зафиксировано в
    docstring'е `_render_dumpcfg_command`.
  - **Timeout фиксированный 300 секунд.** Не
    конфигурируется на Step 2 — это простой honest
    cap для MVP. Possible enhancement: вынести в
    config (`onec_dumpcfg_timeout_seconds`) когда
    появятся реальные стенды с понятным SLA.
  - **`command_preview` — раскрытый argv.** В нём
    видны все placeholder'ные значения после
    подстановки (например, путь к base_path).
    Operator должен помнить: если он положил в
    base_path / dump_path что-то секретное, оно
    окажется в payload'е. На Step 2 это
    accept-as-is; secrets vault — отдельный
    enterprise track.
  - **Excerpts cap 1024 chars.** Полные subprocess
    логи — operator's responsibility (его
    observability stack), как и в Phase 5 / Step 7.
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `apply_config_from_files` /
    `update_database_configuration` — это будут
    отдельные шаги Phase 6 (или parallel track после).
  - Никаких изменений `apps/mcp-read-server/**`,
    `apps/mcp-intelligence-server/**`,
    `apps/platform/**`, `scripts/**`, `.github/**`,
    `pyproject.toml`, `.claude.json`.
  - Никакого `shell=True`, никакого 1cv8-CLI
    guessing.
  - Никакого silent runtime fallback с binary-backed
    в stub.
  - Никакого product-layer write channel.
- **Dev-check после Step 2 зелёный.**
  `imports_ok = true`, `read_server_tools` = 15
  (не тронут), `write_server_tools` = 23 (не
  тронут), `intelligence_server_tools` = 16 (не
  тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`.

### Phase 6 / Step 3 — installer / packaging / setup fast path (завершён)

- **Архитектурное решение Step 3.** Это **fast path**,
  не настоящий industrial installer. Step 3 не делает
  GUI installer, MSI/deb, packaging ecosystem,
  release-artifact-builder, signed binary distribution —
  всё это явно out-of-scope. Сделан минимальный,
  честный, проверяемый product-level install/setup
  contract поверх уже существующего `apps/platform`,
  без изменений MCP server registries и без write
  channel.
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/templates.py` —
    новый модуль с одной boundary-функцией:
    - `build_product_config_template(*, product_name,
      profile_name, default_environment, base_path,
      dump_path, http_base_url, ...optional...)` →
      `ProductConfigTemplateResult`. Возвращает
      JSON-serialisable dict, не пишет на диск. Bad
      input → `ok=False` с `template_input_rejected`
      finding (boundary не бросает наружу). Внутренняя
      валидация через приватные `_require_non_empty_str`
      / `_require_int_or_float` /
      `_validate_optional_str_list` /
      `_validate_optional_str` помощников; они
      рейзят `ValueError`, который boundary
      перехватывает.
    - Опциональные binary-related поля
      (`onec_binary_path`,
      `onec_binary_probe_args`,
      `onec_dumpcfg_command_template`) emit'ятся в
      template только когда заданы; absent fields
      просто опускаются — это matched contract'у
      loader'а, который их трактует как optional.
    - Если `work_dir` не указан или binary-backed
      путь не сконфигурирован — добавляются
      **presumed warnings** (не блокирующие):
      `template_work_dir_absent` /
      `template_binary_backed_inactive`.
  - `apps/platform/src/onec_platform/installer.py` —
    новый модуль с тремя boundary-функциями:
    - `inspect_release_layout(root_path)` — read-only
      проверка top-level entries
      (`apps/`, `packages/`, `docs/`, `README.md`,
      `PROJECT-STATUS.md`). `ok=True` даже когда
      какие-то entries отсутствуют (это honest
      finding, не boundary failure). `ok=False`
      только когда сам root path не существует или
      не директория.
    - `run_install_fast_path(data, *,
      output_config_path, confirm_write=False)` —
      главный Step 3 boundary. Поток:
      load_product_config → inspect_release_layout (на
      ближайшем существующем ancestor'е
      `output_config_path`) → bootstrap_product
      (pre-write) → projection в
      JSON-serialisable dict → confirm gate. На
      `confirm_write=False` (default) → `mode="preview"`,
      ничего на диск. На `confirm_write=True` +
      target свободен → атомарная запись (`*.tmp`
      + `Path.replace`), затем
      `bootstrap_product_from_json_file` round-trip
      → `mode="executed"`. На existing target →
      `mode="rejected"` без silent overwrite.
    - `run_install_fast_path_from_json_file(path, *,
      output_config_path, confirm_write=False)` —
      JSON-входной вариант. На missing / malformed
      JSON → `mode="rejected", ok=False`, без
      исключения наружу.
    - `_write_product_config_template(...)` — private
      helper для атомарной записи; сам по себе тоже
      не бросает (возвращает `(bool, error_str|None)`).
      Создаёт parent директорию (часть «уменьшения
      ритуала» — operator не делает `mkdir -p`
      руками).
    - `_infer_layout_root(output_path)` — выбирает
      ближайшего существующего предка
      `output_config_path` для layout inspection,
      чтобы fast path терпимо работал даже когда
      operator показывает на ещё не существующую
      директорию.
  - `apps/platform/src/onec_platform/models.py` —
    добавлены `ProductConfigTemplateResult`,
    `ReleaseLayoutReport`, `InstallFastPathResult`,
    плюс константа `INSTALL_MODES = ("preview",
    "executed", "rejected")`. Step 5/6/7-модели и
    Phase 5 модели не тронуты.
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 8
    новыми именами (4 модели + 1 константа + 3
    boundary-функции + `build_product_config_template`).
- **Дисциплина installer'а.**
  - **Никакого silent overwrite.** Existing
    `output_config_path` → `mode="rejected"` с
    finding'ом `output_config_path_exists`. Operator
    выбирает другой путь или удаляет существующий
    файл руками.
  - **Атомарная запись.** Через `<file>.tmp` +
    `Path.replace`. Никакого «полу-записанного»
    config'а на диске даже при сбое.
  - **Создание parent-директории — да** (часть
    сокращения ритуала). Создаются только директории,
    ведущие к `output_config_path`; никаких записей
    вне этого пути.
  - **Round-trip подтверждение.** После записи
    `bootstrap_product_from_json_file` повторно
    читает JSON и прогоняет doctor — это honest
    проверка, что записанный файл валиден как
    product-config.
  - **Никакого запуска runtime / workflows /
    write-tool'ов.** Helper не зовёт
    `start_product_runtime`, `run_guided_workflow`,
    любые MCP write-tool'ы или `onec-process-runner`.
    Запуск runtime — отдельный шаг оператора через
    уже существующие boundary-функции.
  - **Никакого shell.** Никаких `subprocess(shell=True)`,
    никаких CLI-команд из installer helper'а.
- **Короткий install runbook (≤ 5 ручных шагов,
  закрывает критерий приёмки 3 Phase 6).**
  1. Получить релиз (clone репозитория или скачать
     архив).
  2. Запустить `scripts/dev/bootstrap_paths.ps1`
     (PYTHONPATH в текущей PowerShell-сессии).
  3. Подготовить минимальный input dict.
  4. Вызвать `run_install_fast_path(input_dict,
     output_config_path=..., confirm_write=True)`.
  5. После `mode="executed"` запустить runtime /
     dashboard / workflow / real-stand smoke как
     отдельные шаги через существующие
     boundary-функции.
  Это документировано в `apps/platform/README.md`
  как раздел «Короткий install runbook».
- **Чего на Step 3 намеренно ещё нет (зафиксировано
  в README).** GUI installer; release packaging
  ecosystem (`.msi`/`.deb`/`.dmg`/wheel/PyPI release
  artefact); запуск MCP-серверов из helper'а;
  изменения инфобазы; silent overwrite; подмена
  Step 2 binary integration; format релизного
  артефакта как formal contract (Step 1 plan-level
  question); signed binary distribution; multi-version
  release matrix; auto-launcher; setup-wizard.
- **Failure-style — единая дисциплина.**
  - Boundary-функции (`inspect_release_layout`,
    `run_install_fast_path`,
    `run_install_fast_path_from_json_file`,
    `build_product_config_template`) **никогда не
    бросают**.
  - `ok=True` covers honest happy paths: layout
    inspected; preview built; executed write +
    round-trip; template assembled.
  - `ok=False` reserved for: invalid input config,
    layout cannot be inspected (root absent / not
    a dir), existing target file (refusal to
    overwrite), I/O write error, malformed JSON
    input.
  - Confirmed/presumed дисциплина из Phase 4 + Step 4
    + 5 + 6 + 7 сохранена. Каждый finding несёт
    собственный `confidence`. Layout-inspection
    findings — confirmed (мы реально проверили
    наличие entry); template warnings (отсутствие
    work_dir / binary-backed контракта) — presumed.
- **Safety guarantees Phase 2–6 — что сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - `run_write_flow` остаётся единственной точкой
    входа к mutating операциям. Installer helper его
    **не зовёт** и **не обходит**.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в нём,
    ни в `onec_platform` (программный grep + assert
    в manual check, Сценарий L).
  - Никакого собственного write channel в `onec_platform`
    к инфобазе. Запись на диск ограничена единственным
    target-файлом (operator-указанный
    `output_config_path`) и его parent-директорией.
  - `onec-config`, `onec-policy-engine`, `onec-audit`,
    `onec-health`, `onec-process-runner`,
    `onec-troubleshooting`, `mcp-common`,
    `pyproject.toml`, `.github/`, `selfcheck.py`,
    `bootstrap_paths.ps1`, `apps/mcp-read-server/**`,
    `apps/mcp-write-server/**`,
    `apps/mcp-intelligence-server/**`, `scripts/**`,
    `.claude.json` — **не тронуты на Step 3**.
- **Ручная проверка (12 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\phase6_step3_check.py`
  использует `tempfile.mkdtemp` + synthetic
  release-like директории + synthetic input
  product-configs. Сценарии:
  - **K (start). Registry invariants** — read=15,
    write=23, intelligence=16; assert.
  - **A. inspect_release_layout happy path** —
    synthetic release с пятью expected entries →
    `ok=True, missing_entries==[]`, у каждого
    entry есть `release_entry_present:*` finding.
  - **A'. inspect_release_layout с partial layout** —
    только `README.md` → `ok=True`, остальные в
    `missing_entries`; присутствующий помечен
    confirmed-ok-finding'ом.
  - **B. inspect_release_layout: non-existent root**
    → `ok=False`, `release_root_missing` finding.
  - **C. inspect_release_layout: root-is-file** →
    `ok=False`, `release_root_not_directory` finding.
  - **D. run_install_fast_path preview** —
    `confirm_write=False`. `mode="preview", ok=True,
    config_written=False`. `output_config_path` **не
    существует** на диске после вызова.
    `template_preview` populated и round-trip'ится
    через `load_project_config`. `bootstrap_pre.ok=True,
    bootstrap_post=None`.
  - **E. run_install_fast_path executed** —
    `confirm_write=True`. `mode="executed", ok=True,
    config_written=True`. JSON реально записан;
    содержит ожидаемые поля. `bootstrap_post.ok=True`
    (round-trip подтверждён).
  - **F. overwrite refusal** — повторный вызов с
    `confirm_write=True` на тот же путь →
    `mode="rejected", ok=False`. Существующий файл
    **на диске не изменился** (assert на
    содержимое до и после).
  - **G. broken input config** — dict без
    обязательных ключей → `mode="rejected", ok=False`,
    output_path **не создан**. Также проверен
    non-dict input (`["not", "a", "dict"]`) → тот же
    `mode="rejected"`.
  - **H. JSON-file flow happy** — записать input
    config как JSON, вызвать `_from_json_file` с
    `confirm_write=True` → `mode="executed", ok=True`.
  - **I. JSON-file flow missing / broken** —
    несуществующий path → `mode="rejected", ok=False`;
    битый JSON → то же. Никаких исключений наружу.
  - **J. build_product_config_template** — happy
    path даёт template, который round-trip'ится
    через `load_product_config`. Bad input
    (empty `product_name`) → `ok=False, template={}`,
    finding `template_input_rejected`. Boundary не
    бросает.
  - **L. Import discipline** — grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/platform/src/**` +
    `apps/mcp-intelligence-server/src/**` →
    **0 импортов** ✓.
  - **K (final). Registry invariants** — read=15,
    write=23, intelligence=16 после всех сценариев.
  Все assert'ы прошли с первой попытки.
- **MVP-компромиссы Step 3 (зафиксированы честно в
  README).**
  - **Layout inspection — только top-level.** Не
    walk'ит subtrees, не открывает файлы, не
    проверяет содержимое. Operator видит, что
    `apps/` есть; что внутри — отдельный шаг.
  - **Release artifact format не зафиксирован.**
    Phase 6 Step 1 plan ставил это как open
    question; Step 3 ship'ит fast path над
    «оператор клонировал репо или распаковал
    архив», не выбирает между zip/tar/wheel/git
    tag formal contract'ом. Это enhancement
    дальнейших шагов Phase 6.
  - **Helper не делает atomic install/upgrade
    sequencing.** Если operator уже что-то
    запустил, helper просто не перезаписывает
    config; full upgrade choreography (stop runtime
    → re-write config → start runtime) — это
    operator-driven последовательность, не один
    boundary call.
  - **Шаблон не валидирует cross-field
    consistency.** Например, не проверяет, что
    `base_path` существует на диске — это
    компетенция bootstrap doctor'а (вызывается
    после записи). Template builder honest о том,
    что он только собирает dict.
  - **Создание parent-директории.** Это
    deliberate compromise в пользу UX: operator
    не должен делать `mkdir -p` руками. Никаких
    других директорий вне parent path не
    создаётся.
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `apply_config_from_files` /
    `update_database_configuration` (это
    parallel-track, не Step 3).
  - Никаких изменений
    `apps/mcp-read-server/**`,
    `apps/mcp-write-server/**`,
    `apps/mcp-intelligence-server/**`,
    `packages/**`, `scripts/**`, `.github/**`,
    `pyproject.toml`, `.claude.json`.
  - Никакого собственного write channel в `onec_platform`
    к инфобазе.
  - Никакого silent overwrite.
  - Никакого GUI / MSI / deb / wheel / PyPI release
    artifact builder'а.
  - Никакого MCP transport / `__main__` / CLI у
    серверов; никакого hot reload; никакого
    auto-launcher'а.
  - Никаких setup-wizard'ов или интерактивных
    диалогов.
  - Никаких изменений `selfcheck.py`,
    `bootstrap_paths.ps1`.
- **Dev-check после Step 3 зелёный.** `imports_ok =
  true`, `read_server_tools` = 15 (не тронут),
  `write_server_tools` = 23 (не тронут),
  `intelligence_server_tools` = 16 (не тронут),
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает `onec_platform.installer` —
  installer helper опционален для dev-check'а.

### Phase 6 / Step 4 — rollback execution track (завершён)

- **Архитектурное решение Step 4.** Это **первый
  honestly-executable rollback** для **минимально
  узкой** полосы write-tool'ов: только
  `add_catalog_attribute` и `add_document_attribute`,
  то есть mutating-операции над **одним** XML-card
  файлом, чьё содержимое полностью описывается этим
  файлом и обратимо ровно копированием
  snapshot-копии этого файла. Step 4 не делает
  full rollback-универсум для всех write-tool family'й
  (это parallel track после Phase 6) и не вводит
  публичные `delete_*` write-tool'ы (это требует
  отдельного решения по семантике удаления в 1С).
  Остальные mutating-инструменты остаются
  advisory-only — продуктовый recovery-ассистент
  показывает snapshot hints, но автоматически
  откатить отказывается.
- **Что реально появилось в коде.**
  - `packages/onec-audit/src/onec_audit/models.py` —
    `AuditRecord` получил optional `details: dict |
    None = None`. Field положен **в конец** dataclass'а,
    после старых полей; backward-compat для
    keyword-конструкторов сохранён.
  - `packages/onec-audit/src/onec_audit/writer.py` —
    `format_audit_record` теперь явно `pop`'ает ключ
    `"details"` из serialised JSON, когда он `None`.
    Это даёт байт-идентичные строки с pre-Step-4
    форматом — старые лог-файлы не «портятся»
    добавлением `"details": null`. Когда `details`
    — dict (даже пустой), он сохраняется как есть.
  - `packages/onec-policy-engine/src/onec_policy_engine/engine.py` —
    `_MUTATING_OPERATIONS` пополнен одним именем:
    `restore_dump_file_from_snapshot`. Решение
    `allowed_mutating` / `require_snapshots=True` —
    тот же путь, что у `update_module_code` и
    остальных Phase 2 mutating-tool'ов.
  - `apps/mcp-write-server/src/mcp_write_server/tools.py` —
    добавлена ровно одна новая public-tool:
    - **`restore_dump_file_from_snapshot(environment,
      relative_path, snapshot_file_path,
      label="restore-dump-file")`**. Mutating, идёт
      через `run_write_flow(...)`. Контракт:
      - `relative_path` — non-empty string без
        leading/trailing whitespace; абсолютные пути
        и `..` сегменты отвергаются fail-closed
        **до** preflight'а;
      - `snapshot_file_path` — обязан указывать на
        existing regular file; non-existent /
        non-regular → `ok=False`;
      - parent-directories целевого файла создаются
        по необходимости (только в пределах
        dump-дерева; containment check через
        `Path.relative_to` гарантирует это);
      - in-flow `verify` сравнивает содержимое
        живого target-файла с snapshot-файлом
        byte-for-byte;
      - запись делается atomically: `*.tmp` рядом с
        целевым файлом + `Path.replace`. На failure
        в середине промежуточный частичный файл не
        остаётся внутри dump-дерева.
  - `apps/mcp-write-server/src/mcp_write_server/server.py` —
    регистрация нового tool'а в `REGISTERED_TOOLS`.
    Алфавитный `list_tools()` теперь возвращает 24
    имени (был 23). Read-server (15) и
    intelligence-server (16) **не тронуты**.
  - `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py` —
    `_append_audit` принимает новый optional
    keyword-arg `details: dict | None = None` и
    передаёт его в `AuditRecord(...)`. Step 6 success-path
    `run_write_flow` теперь собирает structured
    `success_details = {"operation_name",
    "rollback_supported", опционально
    "backup_snapshot_path", "dump_snapshot_path",
    "relative_path"}`. Поле `rollback_supported` —
    bool, `True` ровно когда `operation_name` в
    приватной frozenset'е
    `_ROLLBACK_SUPPORTED_OPERATIONS = {
    "add_catalog_attribute",
    "add_document_attribute"}`. Это **зеркало**
    whitelist'а из `onec_platform.recovery`; держится
    вручную в синхроне (для Step 4 — две позиции).
    Pre-Step-4 audit-строки приобретают `details`
    автоматически на следующих write'ах; readers
    видят либо новый dict, либо отсутствие ключа —
    обе формы валидны.
  - `apps/platform/src/onec_platform/recovery.py` —
    `_AUTOMATIC_RECOVERY_SUPPORTED` переехал из
    пустого frozenset'а в frozenset из ровно двух
    имён: `{"add_catalog_attribute",
    "add_document_attribute"}`. Добавлены приватные
    `_entry_details(entry)` (читает `details` из raw
    audit line; pre-Step-4 строка → `None` без
    raise) и `_details_indicate_rollback_supported(
    entry, details)` (тройной AND: tool в
    whitelist'е, details есть, в details
    `dump_snapshot_path` и `relative_path` —
    непустые строки). Любой из трёх отсутствующих
    факторов → honest degrade до `mode='unsupported'`,
    без write'а. Suggested-write-tools и
    suggested-tools поверхности
    `inspect_operation` / `_build_rollback_plan` /
    `RollbackPlan` теперь добавляют
    `restore_dump_file_from_snapshot` и
    `diff_dump_fragment` — **только** когда
    `automatic_recovery_supported=True`.
  - `apps/platform/src/onec_platform/recovery.py`,
    `run_rollback_assistant` — на
    `confirm_execute=True` с healthy dashboard'ом и
    whitelisted tool'ом теперь действительно
    исполняется автоматический rollback:
    1. Защитная re-валидация
       `details["dump_snapshot_path"]` /
       `details["relative_path"]` — оба обязаны
       быть непустыми строками; иначе degrade в
       `unsupported` без write'а.
    2. Existence-check `snapshot_file_path =
       Path(dump_snapshot_path) / relative_path` —
       missing → `mode='executed', ok=False,
       execution_performed=False` с явным
       error-finding'ом, без write'а.
    3. Чтение snapshot baseline text вверху —
       чтобы post-rollback verify сравнивал со
       стабильной копией. `OSError` тут — снова
       без write'а.
    4. Зов public write-tool'а
       `restore_dump_file_from_snapshot(env,
       relative_path, snapshot_file_path,
       label=f"rollback-{operation_id[:8]}")`. Это
       идёт через `run_write_flow` со всей
       дисциплиной (preflight + snapshot +
       operation + verify + audit). `write_results`
       наполняется dict'ом ToolResult'а.
    5. Refresh `last_write_operation` через
       существующий read-only
       `describe_last_write_operation(env)`, чтобы
       клиент видел свежую audit row, написанную
       рестором.
    6. Обязательный post-rollback verify через
       `diff_dump_fragment(env, relative_path,
       baseline)`. Success criterion жёсткий:
       `restore.ok=True` AND `diff.ok=True` AND
       `diff.payload.data.changed=False`. Иначе
       `mode='executed', ok=False` с
       соответствующим сообщением, но
       `execution_performed=True` (попытка реально
       была).
  - **Никаких back-door write-каналов.**
    `recovery.py` не пишет в файловую систему
    напрямую — все mutating effects идут через
    public write-tool. Импорт
    `mcp_write_server.tools.{diff_dump_fragment,
    restore_dump_file_from_snapshot}` добавлен
    рядом с уже имеющимся
    `prepare_rollback_hint` /
    `describe_last_write_operation` (forward-only
    cross-app: product → write).
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase6_step4_check.py`
  прогоняет 14 сценариев на synthetic tempdir + local
  HTTPServer (gateway). Сценарии: A — `details=None`
  байт-идентичен старому формату; B — `details=dict`
  preserved; C — policy engine знает
  `restore_dump_file_from_snapshot` как
  `allowed_mutating`, unknown op остаётся
  `unknown_intent`; D — restore tool отвергает
  empty / non-string / `..` / missing-snapshot inputs
  fail-closed без касания live target; E — happy-path
  `add_catalog_attribute` пишет audit row с полными
  `details` и snapshot-файл байт-равен pre-add
  baseline; F — `inspect_operation` отдаёт
  `automatic_recovery_supported=True` и surface'ит
  два rollback-tool'а в `suggested_write_tools`; G —
  preview без write'ов; H — confirm_execute=True →
  `mode='executed', ok=True, execution_performed=True`,
  ровно один `write_result` (рестор) и один
  `verify_result` с `data.changed=False`, live XML
  байт-равен pre-add; I — то же для
  `add_document_attribute`; J — pre-Step-4 audit row
  (без `details`) → `mode='unsupported'`, no write;
  K — tool вне whitelist'а (`update_module_code`) →
  `mode='unsupported'`, no write (даже если details
  есть); L — gateway остановлен → dashboard не
  ready → `mode='blocked', ok=False`, no write,
  пост-add файл остаётся в post-add состоянии.
  M — registry invariants `read=15 / write=24 /
  intelligence=16`. N — нулевой импорт
  `onec_policy_engine` в product / intelligence
  поверхностях (тонкая проверка реальных import
  statement'ов, не docstring'ов).
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным. Вывод последнего прогона:
  `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 24 имени включая
  `restore_dump_file_from_snapshot`,
  `intelligence_server_tools` — 16 имён без
  изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает recovery executed branch —
  manual check покрывает её на synthetic стенде без
  настоящего 1cv8.

### Phase 6 / Step 5 — metadata completion / structural editing (завершён)

- **Архитектурное решение Step 5.** Это **первый
  настоящий structural XML edit slice**: одно
  точечное расширение metadata-поверхности на одном
  объекте (form-level Attributes), сделанное через
  `xml.etree.ElementTree`, а не через
  substring/`rfind` патчинг. Step 5 не ship'ит full
  metadata-вселенную и не переписывает существующие
  Phase 3 mutating tool'ы (`add_catalog_attribute`,
  `add_document_attribute`, form/module-level tools)
  на DOM-edit — это сознательное узкое решение,
  чтобы не размывать scope. Также Step 5 не делает
  `delete_*`-tool'ов, не расширяет rollback whitelist
  Step 4, не вводит BSL AST-парсер, не трогает
  `apply_config_from_files` /
  `update_database_configuration` (это отдельные
  будущие шаги Phase 6).
- **Что реально появилось в коде.**
  - `apps/mcp-write-server/src/mcp_write_server/runtime/metadata_ops.py`
    — добавлены **шесть новых internal helper'ов** на
    stdlib `xml.etree.ElementTree` (без новых runtime-файлов):
    - `parse_xml_file(path) -> ET.ElementTree` —
      обёртка над `ET.parse`; `OSError` /
      `ET.ParseError` пропагируют (fail-loud, как
      того требует helper layer);
    - `write_xml_file(path, tree) -> None` —
      сериализация UTF-8 + `xml_declaration=True` +
      `short_empty_elements=False`. Последний
      параметр критичен: пустые контейнеры остаются
      в форме `<Tag></Tag>`, не collapse'ятся в
      `<Tag/>`, и downstream substring-based tool'ы
      (например, `add_form_element` со
      своим `</Elements>` lookup'ом) продолжают
      работать;
    - `find_form_element(root, form_name) ->
      ET.Element | None` — рекурсивный поиск
      `<Form name="form_name">`. Поддерживает и flat
      shape (тестовые fixture'ы), и nested shape
      (`<ChildObjects><Forms>` в production-картах);
    - `get_or_create_form_attributes_block(form_elem)
      -> ET.Element` — возвращает существующий
      `<Attributes>` или создаёт новый как
      `SubElement` в конце form'ы. Mutates form_elem
      in place при создании;
    - `add_attribute_to_form_attributes_block(
      attributes_block, name, attr_type, synonym)`
      — структурный append `<Attribute name="..."><Type>...</Type>[<Synonym>...]</Attribute>`;
      без de-dup (вызывающая сторона сама проверяет
      уникальность);
    - `form_has_attribute(form_elem, attribute_name)
      -> bool` — поиск по атрибуту `name="..."`,
      **только** внутри form's own `<Attributes>`
      (object-level Attributes намеренно не
      consult'ятся — это другая metadata surface).
    Helper layer остаётся **internal**: никаких
    ToolResult'ов, никакого `run_write_flow`, никаких
    snapshot/audit обязательств — всё это лежит на
    tool layer и flow.
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — добавлен **один новый public mutating tool**:
    - **`add_form_attribute(environment, object_name,
      form_name, attribute_spec, label="add-form-attribute")`**.
      Идёт строго через `run_write_flow(...)`. Pre-flow
      validation: `object_name` через тот же
      `_resolve_object_xml_path` (поддерживает
      `Справочник.<name>` / `Документ.<name>`);
      `form_name` через существующий `_MODULE_NAME_RE`
      (`\w+`); `attribute_spec` — `name` non-empty без
      whitespace, `type` ∈ `_ALLOWED_ATTR_TYPES`
      (`String` / `Number` / `Date`), `synonym`
      опционален. Bad-input возврат — без `runtime` в
      payload, без stage marker'а, без
      backup/dump-snapshot (flow не запускался). В
      operation: парсит XML, ищет форму через
      `find_form_element`, dup-check через
      `form_has_attribute` (по `name=` атрибуту, не
      substring), `<Attributes>` создаётся
      structurally если отсутствует
      (`get_or_create_form_attributes_block`), новый
      `<Attribute>` добавляется через
      `add_attribute_to_form_attributes_block`, дерево
      пишется обратно через `write_xml_file`. Form
      missing → `ValueError` → `stage="operation",
      ok=False`, файл не тронут; duplicate →
      `FileExistsError` → тот же fail-closed путь.
      `operation_payload` несёт
      `attributes_block_created: bool` — True ровно
      когда блок был создан с нуля. Verify в flow
      повторно парсит файл и проверяет
      `form_has_attribute(form, attr_name)`
      structurally, а не substring. Никаких новых
      обязательных параметров у других tool'ов.
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`,
    `verify_metadata_change(...)` — добавлена **одна
    новая read-only ветка** dispatcher'а:
    `kind="form_attribute_exists"` (поля expectation:
    `object_name`, `form_name`, `attribute_name`).
    Tool name результата остаётся
    `verify_metadata_change`;
    `payload.data.verification_kind =
    "form_attribute_exists"`. Реализация — приватный
    helper `_verify_form_attribute_exists_internal`
    в том же файле (без новых runtime-файлов): идёт
    через существующий `read_dump_file`,
    `ET.fromstring` на содержимом, `find_form_element`
    + `form_has_attribute`. PlatformError из dump
    adapter'а и `ET.ParseError` на malformed XML
    оба → `ok=False` с конкретным сообщением (не
    crash). Новый standalone public verify-tool
    **не** добавляется — это сознательное решение,
    чтобы public surface оставалась узкой.
  - `apps/mcp-write-server/src/mcp_write_server/server.py`
    — регистрация нового tool'а в
    `REGISTERED_TOOLS`. Алфавитный `list_tools()`
    теперь возвращает 25 имён (был 24). Read-server
    (15) и intelligence-server (16) **не тронуты**.
  - `packages/onec-policy-engine/src/onec_policy_engine/engine.py`
    — **не тронут**. `add_form_attribute` уже был
    зарегистрирован в `_METADATA_MUTATING_OPERATIONS`
    в Phase 3 (как часть планового whitelist'а Phase 3
    metadata-tools) и просто переходит из «namespace
    зарезервирован» в «реализован». Policy decision
    остаётся `allowed_metadata_mutating`,
    `require_snapshots=True`.
- **Что НЕ переписано на structural edit.**
  - `add_catalog_attribute` / `add_document_attribute`
    (object-level Attributes) — продолжают работать
    через `insert_fragment_into_named_block` без
    изменений. Step 5 ship'ит structural edit
    точечно — для form-level Attributes — а не
    сметает все старые tool'ы одним проходом.
  - Form/module level tools Phase 3 / Step 6
    (`create_managed_form`, `add_form_element`,
    `append_module_method`,
    `replace_module_method_body`) — без изменений.
  - `apply_config_from_files` /
    `update_database_configuration` — снова не
    тронуты, это отдельные шаги Phase 6 (или
    parallel-track после).
- **Честные ограничения slice'а.**
  - Нет XML namespace handling. Production-карты 1С
    обычно несут
    `xmlns="http://v8.1c.ru/8.3/MDClasses"`;
    namespaced cards — out of scope для этого slice.
    Tools и helper'ы рассчитаны на un-namespaced XML,
    который используют тестовые fixture'ы и Phase 3
    substring-based tools. Поддержка namespaced cards
    — отдельный будущий step.
  - ElementTree **не** preserves whitespace /
    pretty-print byte-for-byte. После записи файл
    может выглядеть слегка иначе (например, без
    оригинальных переносов строк), хотя
    XML-эквивалентен. Это не ломает downstream
    tool'ы, но честно фиксируется в documentation.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase6_step5_check.py`
  прогоняет 9 сценариев на synthetic tempdir + local
  HTTPServer (gateway). Сценарии: A — registry
  invariants `read=15 / write=25 / intelligence=16`;
  B — form already has `<Attributes>` block →
  `ok=True, stage=completed,
  attributes_block_created=False`, audit row
  `tool_name='add_form_attribute' status='ok'`,
  structural recheck подтверждает атрибут внутри
  нужной формы; C — form has NO `<Attributes>`
  block → tool создаёт блок structurally,
  `attributes_block_created=True`, structural
  recheck тоже подтверждает; D — duplicate в той
  же форме → `ok=False, stage='operation'`, файл
  byte-identical до post-first-add baseline'а,
  audit row `status='error'`; E — form missing →
  `ok=False, stage='operation'`, файл untouched,
  audit row `status='error'`; F — bad
  `attribute_spec.type` → pre-flow rejection (нет
  `runtime` в payload, нет stage marker'а, нет
  audit row на диске, нет `_snapshots` директории);
  G — `verify_metadata_change(kind=
  "form_attribute_exists")` positive → `ok=True,
  verification_kind='form_attribute_exists',
  exists=True`, tool_name `verify_metadata_change`;
  H — то же negative (форма есть, атрибута нет) →
  `ok=False, exists=False`; H' — то же с missing
  form → `ok=False, exists=False` (degrade без
  crash'а на отсутствующей форме); I — registry
  counts (proxy для dev-check invariant'а; реальный
  `run_dev_check.ps1` запускался отдельно).
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным. Вывод последнего прогона:
  `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 25 имён включая
  `add_form_attribute`,
  `intelligence_server_tools` — 16 имён без
  изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`.
  `selfcheck.py` намеренно не дёргает
  `add_form_attribute` — manual check покрывает
  все ветки на synthetic стенде.

### Phase 6 / Step 6 — runtime hardening / supervision / logs (завершён)

- **Архитектурное решение Step 6.** Это **первый
  честный slice runtime hardening** поверх уже
  существующего product runtime contract из Phase 5 /
  Step 3. Step 6 **не** делает Windows Service / systemd
  unit registration, **не** background watcher /
  supervisor / daemon manager / timer-loop, **не** hot
  reload, **не** journald / log aggregation /
  forwarding, **не** logging framework. Step 6 не
  добавляет ни одного нового MCP tool'а. Все изменения
  локальны в продуктовом слое
  `apps/platform/src/onec_platform/`.
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/models.py` —
    добавлена константа `RESTART_POLICIES = ("never",
    "restart-if-stale")`, константа
    `DEFAULT_LOG_MAX_BYTES = 1 MiB`. Класс
    `ProductServiceSpec` получил три optional поля:
    `restart_policy: str = "never"`,
    `logs_enabled: bool = True`,
    `log_max_bytes: int = DEFAULT_LOG_MAX_BYTES`.
    `RUNTIME_STATE_SCHEMA_VERSION` поднят `1 → 2`;
    введена `RUNTIME_STATE_READABLE_SCHEMA_VERSIONS =
    (1, 2)`. Класс `RuntimeServiceState` расширен
    семью persisted-полями: `restart_policy`,
    `restart_attempts: int`, `last_exit_code: int |
    None`, `stdout_log_path: str | None`,
    `stderr_log_path: str | None`,
    `last_started_at: str | None`,
    `last_stopped_at: str | None`. Все default'ы
    consistent — старые dataclass-конструкторы Step 3
    остаются валидны.
  - `apps/platform/src/onec_platform/loader.py` —
    `_parse_service_spec` строго валидирует три новых
    поля: `restart_policy` через whitelist
    `RESTART_POLICIES`, `logs_enabled` как чистый
    `bool` (не bool-ish), `log_max_bytes` как
    положительный `int` с явным отвержением `bool`
    (т.к. `bool ⊂ int` в Python). Bad shape →
    `ValueError`, который boundary-слой переводит в
    `ok=False`. Старые конфиги без этих полей
    продолжают грузиться без изменений.
  - `apps/platform/src/onec_platform/state.py` —
    reader принимает обе `RUNTIME_STATE_READABLE_SCHEMA_VERSIONS`.
    Pre-Step-6 (schema=1) файлы читаются с дефолтами
    для новых полей: `restart_policy="never"`,
    `restart_attempts=0`, остальные `None`. В памяти
    schema нормализуется к текущей версии (2) сразу
    при чтении, чтобы downstream-код видел
    consistent shape. Writer всегда эмитит version=2.
    Unsupported schema versions по-прежнему
    fail-closed.
  - `apps/platform/src/onec_platform/process_control.py`
    — добавлен `get_pid_exit_code(pid)` (Windows: через
    `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)` +
    `GetExitCodeProcess`; POSIX: всегда возвращает
    `None` — orchestrator не spawn'ил PID как child
    текущего процесса, поэтому `waitpid` недоступен;
    честная деградация). `spawn_service(...)` получил
    optional kwargs `stdout_handle: IO[bytes] | int |
    None` / `stderr_handle: IO[bytes] | int | None`.
    `None` сохраняет старое Step 3 поведение
    (`DEVNULL`); открытый file handle / int FD
    маршрутизирует поток. `stdin` всегда `DEVNULL`.
    `shell=True` **никогда** не используется.
    `start_new_session=True` (POSIX) /
    `CREATE_NEW_PROCESS_GROUP` (Windows) сохранены без
    изменений.
  - `apps/platform/src/onec_platform/runtime_logs.py`
    (новый, **internal helper module**, ~150 строк) —
    `logs_dir(work_dir)` / `get_log_paths(work_dir,
    service_name)` (path arithmetic, no I/O),
    `prepare_log_dir(work_dir)` (mkdir
    `<work_dir>/.runtime/logs/`, fail-closed на
    отсутствующий work_dir / permission'ы),
    `rotate_log_if_oversized(path, max_bytes)`
    (одна generation: переименовывает в `<file>.1`
    через `os.replace`; old `.1` перезаписывается;
    возвращает `True` ровно когда rotation реально
    случилась), `open_log_handles(stdout_path,
    stderr_path)` (открывает пару в режиме `"ab"`
    binary append, `buffering=0`; на failure второго
    open закрывает первый и пробрасывает `OSError`).
    Никаких ToolResult'ов, никакой stream
    мультиплексации.
  - `apps/platform/src/onec_platform/runtime.py` —
    `_service_state_from_spec` берёт `restart_policy`
    из spec'а; `_merge_persisted_into_spec_state`
    переносит persisted `restart_attempts` /
    `last_exit_code` / log paths / timestamps в
    materialized state, при этом `restart_policy`
    остаётся spec-driven (current config
    authoritative). `_refresh_running_against_pid` при
    обнаружении stale PID best-effort вызывает
    `get_pid_exit_code` и стампит `last_stopped_at` =
    UTC ISO. Добавлен приватный
    `_prepare_logs_for_spawn(spec, work_dir)`,
    собирающий лог-handles + finding'и про rotation /
    log-dir-failed; `_start_one(spec, current,
    work_dir)` (новая сигнатура — третий аргумент
    `work_dir`) использует его, передаёт handles в
    `spawn_service`, при success'е populate'ит
    `stdout_log_path` / `stderr_log_path` /
    `last_started_at`, на любом log-side failure
    (mkdir / rotate / open) возвращает
    `status="error"` без silent-fallback'а на
    DEVNULL. `_start_one` теперь возвращает
    `tuple[RuntimeServiceState, list[DoctorFinding]]`
    (раньше один finding; multiple фактические
    finding'и нужны для отдельного surface'инга
    `runtime_log_paths` / `runtime_log_rotated`).
    `_stop_one` стампит `last_stopped_at`. Добавлен
    `_apply_restart_if_stale(config, services,
    work_dir)` — boundary-only restart path, который
    инкрементит `restart_attempts`, зовёт обычный
    `_start_one` и эмитит `runtime_restart_attempted` /
    `runtime_restart_succeeded` /
    `runtime_restart_failed`. Этот helper зовётся из
    `get_product_runtime_status` (после
    `_refresh_running_against_pid`; persist делается,
    только если что-то реально перезапустилось — иначе
    status остаётся read-only) и из `_run_operation`
    после фазы start/reload. На `stop` помечен явно
    как **не** срабатывающий — оператор только что
    попросил остановить, восстановление было бы
    surprise.
  - **Никаких других runtime-файлов не добавлялось.**
    `dashboard.py` / `workflow.py` / `recovery.py` /
    `realstand.py` / `installer.py` / `templates.py` —
    без изменений. `mcp-read-server` /
    `mcp-write-server` / `mcp-intelligence-server` /
    `onec-policy-engine` / `onec-config` —
    без изменений.
- **Operator-visible findings.** Новые коды:
  `runtime_log_paths:<svc>` (ok), `runtime_log_rotated:<svc>`
  (ok), `runtime_log_dir_failed:<svc>` /
  `runtime_log_open_failed:<svc>` /
  `runtime_log_rotate_failed:<svc>` (error,
  fail-closed для конкретного service'а),
  `runtime_restart_attempted:<svc>` (warning),
  `runtime_restart_succeeded:<svc>` (ok),
  `runtime_restart_failed:<svc>` (error). Существующий
  `runtime_pid_stale:<svc>` обогащён: текст содержит
  `last_exit_code=N` когда он известен, или
  «exit code unavailable on this platform» когда
  POSIX-fallback вернул `None`.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase6_step6_check.py`
  прогоняет 12 сценариев A–K на synthetic tempdir с
  реальными `subprocess.Popen`-вызовами:
  - A — registry invariants (`read=15 / write=25 /
    intelligence=16`);
  - B — happy path start/status/stop с реальным
    long-lived Python sleeper'ом, log paths
    populated, status показывает stdout/stderr-paths
    и `last_started_at`, stop реально kill'ит PID и
    стампит `last_stopped_at`;
  - C — содержимое логов: child пишет маркеры в
    stdout/stderr, после короткого ожидания файлы
    содержат маркеры (sleeper script
    материализуется как файл, не передаётся через
    `python -c` — на Windows multi-line `-c`
    payload'ы могут портиться command-line
    quoting'ом);
  - D — pre-create oversized `.out.log`, start
    эмитит `runtime_log_rotated:svc`,
    `<svc>.out.log.1` создан, новый активный лог
    свежий и меньше старого;
  - E — restart_policy=`"never"` + dead PID в state:
    status reports `stale`, `runtime_pid_stale`
    finding есть, **никаких** restart-attempt-finding'ов,
    `restart_attempts=0`;
  - F — restart_policy=`"restart-if-stale"` + dead PID
    в state: status автоматически перезапускает —
    new PID alive, `restart_attempts=1`,
    `runtime_restart_attempted` +
    `runtime_restart_succeeded` finding'и есть,
    persisted state обновлён (новый PID, счётчик);
  - G — `<work_dir>/.runtime/logs` существует как
    регулярный файл (не директория), start
    fail-closed: `runtime_log_dir_failed:svc`
    finding, `status="error"`, `pid=None`, **никакого**
    silent fallback'а на DEVNULL;
  - H1 — старый config без `restart_policy` /
    `logs_enabled` / `log_max_bytes` всё ещё валиден
    (default'ы применяются);
  - H2 — schema_version=1 persisted state читается
    без crash'а; в памяти schema нормализуется к 2;
    boundary call работает;
  - I — JSON-file flow happy path:
    `start_product_runtime_from_json_file` +
    `get_product_runtime_status_from_json_file`
    срабатывают end-to-end;
  - J — 7 bad-config вариантов
    (`restart_policy="garbage"`, `restart_policy=1`,
    `logs_enabled="true"`, `log_max_bytes=0`,
    `log_max_bytes=-1`, `log_max_bytes=True`,
    `log_max_bytes="1k"`) — все возвращают `ok=False`
    без exception'а наружу, message содержит
    конкретное объяснение;
  - K — registry-counts proxy под dev-check.
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным. Вывод последнего прогона:
  `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 25 имён без изменений,
  `intelligence_server_tools` — 16 имён без
  изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`.
  `selfcheck.py` намеренно не дёргает Step 6
  runtime-flow'ы — manual check покрывает все
  ветки на synthetic subprocess'ах.

### Phase 6 / Step 7 — real-stand end-to-end validation + standalone docs/runbooks (завершён)

- **Архитектурное решение Step 7.** Это **validation + docs**
  step. Никакого расширения surface'а: ни одной новой MCP-tool'и,
  ни одного нового product-layer execution slice'а, ни одного
  нового runtime hardening behavior'а. Цель — подтвердить, что
  Phase 6 (Step 2–6) сходится в один связный сценарий на
  synthetic стенде, и вынести operator/admin/developer
  knowledge из READMEов в standalone-документы.
- **Кодовых правок не было.** Все изменения этого шага — только
  под `docs/`. `apps/` и `packages/` тронуты ровно одним блоком
  (заголовок и pointer-блок в `apps/platform/README.md`),
  чтобы операторы и администраторы видели, куда переехала
  ежедневная документация. Остальные README обновлены только в
  части registry counts / Step переходов, без изменения
  surface'а.
- **Что реально появилось в коде / документации.**
  - `docs/operator-manual.md` (новый) — короткий путь
    install/bootstrap/start/status/dashboard/workflow/history/
    rollback/smoke; что означают `healthy`/`degraded`/`blocked`/
    `preview`/`executed`/`unsupported`/`rejected`; как читать
    rollback preview; честные ограничения Phase 6 списком.
  - `docs/administrator-manual.md` (новый) — product-config
    keys (top-level + per-environment + per-service runtime),
    runtime services / restart_policy / logs / work_dir;
    binary-related поля и их честная семантика; где лежат
    `runtime-state.json` и логи; типовые сбои и что делать;
    что нельзя ожидать от текущей версии.
  - `docs/developer-manual.md` (новый) — архитектурная карта
    read/write/intelligence/platform; куда добавлять новый
    capability какого класса; safety invariants, которые
    нельзя ломать (run_write_flow единственный mutating путь;
    intelligence read-only по конструкции; 0 imports
    onec_policy_engine в product/intelligence; no shell=True;
    atomic writes; boundary helpers never raise); slice map
    Phase 6 (Step 1–7); как правильно писать manual-check
    скрипты (тонкие grit-правила: сценарии без `python -c`
    multi-line на Windows, чтение логов до stop'а, ASCII в
    print'ах для cp1251).
  - `docs/runbooks.md` (новый) — шесть recipes в формате
    Symptom/Cause/Diagnose/Fix/Confirm: RB-1 bootstrap doctor
    red, RB-2 runtime stale pid, RB-3 workflow blocked, RB-4
    rollback preview/executed/unsupported, RB-5 real-stand
    smoke failed, RB-6 malformed audit log lines.
  - `apps/platform/README.md` — заголовок «Что сейчас внутри»
    обновлён до **Step 1–7**; добавлен короткий
    pointer-блок с ссылками на все четыре standalone docs.
    Существующий технический контент сохранён без изменений.
  - `README.md` (root) — Phase 6 параграф расширен Step 7
    sentence (Scenario A end-to-end без правок кода + 5
    failure paths + standalone docs); «Следующий шаг»
    переключён на **Step 8 — foundation for enterprise
    track**.
  - `PROJECT-STATUS.md` — текущий шаг переключён на Step 7;
    Step 6 помечен `(завершён)`; добавлен полный Step 7
    detail block; «Следующий шаг» переписан на Step 8.
- **Что НЕ тронуто.** `apps/mcp-read-server/` /
  `apps/mcp-write-server/` / `apps/mcp-intelligence-server/`
  / `packages/onec-*/` / `apps/platform/src/` (кроме того, что
  ничего не редактировалось в коде, точка) — все без правок.
  Existing `docs/runbooks/local-dev-check.md` не тронут.
  `selfcheck.py`, `scripts/dev/`, `pyproject.toml`,
  `.github/` — без изменений.
- **Manual verification — Scenario A + F1–F5 + discipline.**
  Скрипт `C:/Users/user/AppData/Local/Temp/phase6_step7_check.py`
  собирает один связный сценарий и пять honest failure paths
  на synthetic tempdir + local HTTPServer (gateway) + реальные
  `subprocess.Popen` вызовы (sleeper-сервис в runtime, smoke
  через `sys.executable`).
  - **Scenario A.1–A.13.** `bootstrap_product` →
    `run_install_fast_path(confirm_write=True)` →
    `start_product_runtime` → `get_product_runtime_status`
    (status=`running`, log paths populated) →
    `build_environment_dashboard` (overall_status=`healthy`,
    `ready_for_workflows=True`) →
    `run_guided_workflow(safe-add-attribute,
    target_kind=catalog, confirm_execute=True)`. Mutating
    workflow выбран **именно** под Step 4 whitelist
    (`add_catalog_attribute`); operation_id извлекается из
    `wf_res.last_write_operation["operation_id"]` и
    реально проходит сквозь `get_operation_history` (entry
    есть в списке) + `inspect_operation`
    (`operation_found=True, automatic_recovery_supported=True`)
    + `run_rollback_assistant(confirm_execute=True)`
    (`mode='executed', ok=True, execution_performed=True`,
    one write_result + one verify_result с
    `data.changed=False`). **Post-rollback verify** —
    re-parse XML через `xml.etree.ElementTree` и assert
    что `ScenarioField` исчез structurally **И** что live
    text byte-equals pre-add baseline. Затем
    `get_real_stand_readiness`
    (`ready_for_real_stand_smoke=True`) →
    `run_real_stand_smoke_test(confirm_execute=True)`
    (`mode='executed', binary_invoked=True,
    binary_exit_code=0`) → `stop_product_runtime`
    (PID реально умирает). Все 13 шагов прошли с
    реальными subprocess'ами.
  - **F1.** Workflow blocked — gateway не поднят →
    dashboard не `healthy` → `mode='blocked',
    execution_performed=False`, файл untouched.
  - **F2.** Rollback unsupported — `update_module_code`
    написан напрямую через write-server → audit row есть,
    но `tool_name='update_module_code'` вне Step 4
    whitelist'а → `mode='unsupported', ok=True,
    execution_performed=False, write_results=[],
    verify_results=[]`.
  - **F3.** Broken JSON product-config (`{ this is not
    valid JSON `) — все шесть `*_from_json_file`
    boundary'ев вернули `ok=False` без exception'а наружу:
    `bootstrap_product_from_json_file`,
    `get_product_runtime_status_from_json_file`,
    `build_environment_dashboard_from_json_file`,
    `get_operation_history_from_json_file`,
    `get_real_stand_readiness_from_json_file`,
    `run_real_stand_smoke_test_from_json_file`.
  - **F4.** Malformed audit lines — первая строка
    audit.jsonl сломанная JSON, вторая — корректный
    `AuditRecord`. `get_operation_history` вернул
    `ok=True` с findings'ом
    `audit_line_invalid_json:0` и реальным entry для
    второй строки; `inspect_operation` для
    operation_id `'real-row-1'` отдал
    `tool_name='add_catalog_attribute'`. Boundary не
    упал.
  - **F5.** Real-stand smoke failure path — probe args
    `["-c", "import sys; sys.exit(7)"]` →
    `mode='executed', binary_invoked=True,
    binary_exit_code=7, ok=False`. Никакого fake'а и
    никакого silent fallback'а на «metadata-only ok».
  - **D1.** Registry invariants pre-/post-: `read=15,
    write=25, intelligence=16` — без drift'а.
  - **D2.** Suggested tools/suggested write tools: union
    из 54 реальных registered-имён + 10
    `_KNOWN_PLATFORM_FUNCTIONS`. Made-up имя
    `"totally_made_up_tool_xyz"` корректно отвергнуто
    `_allow_only_real_tools`.
  - **D3.** 0 import'ов `onec_policy_engine` под
    `apps/platform/src/` и
    `apps/mcp-intelligence-server/src/` (тонкая
    проверка реальных `import` / `from ... import ...`
    statement'ов, не docstring'ов).
  - **D4.** Step 7 прошёл без code changes —
    зафиксировано в этом detail block'е и в комментариях
    скрипта.
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным. Вывод последнего прогона:
  `imports_ok = true`, registry counts (`read=15,
  write=25, intelligence=16`) — без изменений,
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  не тронут.

### Phase 6 / Step 8 — foundation for enterprise track (завершён)

- **Архитектурное решение Step 8.** Это **узкий honest
  foundation slice**, не enterprise version. Задача — дать
  будущему enterprise track реальную опору, не врать про
  enterprise-readiness, не плодить новые MCP tool'ы и не
  расширять surface ради surface. Шаг **не** делает SSO/RBAC,
  multi-tenant, secrets vault, policy-as-code, federated audit
  storage, multi-instance HA, web-UI, новые MCP tool'ы, новые
  runtime supervision slices, новые write tools. Всё это явно
  вынесено в parallel enterprise track ПОСЛЕ Phase 6.
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/models.py` — добавлены
    две константы и две модели:
    - `DEPLOYMENT_TIERS = ("dev", "test", "stage", "prod-like")`
      — ровно четыре whitelisted tier'а;
    - `FOUNDATION_LEVELS = ("absent", "minimal", "partial",
      "strong")` — четыре уровня детерминистического verdict'а;
    - `EnterpriseFoundationSettings` (dataclass; шесть
      optional-полей: `deployment_tier: str | None`,
      `instance_id: str | None`, `config_owner: str | None`,
      `change_control_required: bool = False`,
      `require_operator_identity: bool = False`,
      `runbook_reference: str | None = None`);
    - `EnterpriseFoundationResult` (dataclass; стандартная shape
      с `ok`, `foundation_level`, `ready_for_enterprise_track`,
      зеркалами всех шести полей секции, плюс
      `confirmed_findings` / `presumed_findings` /
      `recommended_actions` / `suggested_tools` /
      `suggested_write_tools` / `message`).
    - `ProductConfig` получил новое optional поле
      `enterprise: EnterpriseFoundationSettings`
      (`field(default_factory=lambda: ...())` — Step 1–7
      конфиги остаются валидны).
  - `apps/platform/src/onec_platform/loader.py` — добавлен
    приватный `_parse_enterprise(...)`. Strict-validation:
    unknown keys reject (typo `deplyoment_tier` → `ValueError`),
    `deployment_tier` whitelisted, `instance_id` /
    `config_owner` / `runbook_reference` non-empty string или
    `None`, два bool-поля строго `bool` (не bool-ish). Missing
    section → empty `EnterpriseFoundationSettings()` (Step 1–7
    backward compat).
  - `apps/platform/src/onec_platform/templates.py` —
    `build_product_config_template(...)` принял **шесть** новых
    optional kwargs: `enterprise_deployment_tier`,
    `enterprise_instance_id`, `enterprise_config_owner`,
    `enterprise_change_control_required`,
    `enterprise_require_operator_identity`,
    `enterprise_runbook_reference`. Pre-flow validation
    зеркалит loader'у: whitelist tier, non-empty strings, strict
    bools. Block эмитится **только** когда хотя бы один
    enterprise_* kwarg передан — Step 1–7 templates остаются
    байт-идентичными.
  - `apps/platform/src/onec_platform/enterprise.py` (новый,
    ~470 строк, **internal+public**) —
    `inspect_enterprise_foundation(data)` /
    `inspect_enterprise_foundation_from_json_file(path)`.
    Read-only по конструкции: не пишет в audit, не зовёт
    `run_write_flow`, не стартует / стопает runtime, не
    вызывает MCP tool'ы. Никогда не raise'ит. Проверяет
    четыре секции:
    - **A. Identity / config discipline.** `deployment_tier`
      declared, `instance_id`, `config_owner`,
      `change_control_required`, `require_operator_identity`.
      Для prod-like (declared OR detected по visible-полям)
      отсутствие `instance_id` / `config_owner` — `error`
      severity.
    - **B. Operability foundation.** `bootstrap.work_dir`,
      `runtime.services` non-empty, `logs_enabled=True` для
      всех enabled-сервисов, `restart_policy` в whitelist'е.
    - **C. Traceability / recovery foundation.** Standalone
      manuals Step 7 (`docs/operator-manual.md`,
      `docs/administrator-manual.md`,
      `docs/developer-manual.md`, `docs/runbooks.md`)
      physically present (через ancestor-walk от модуля до
      repo root); recovery boundaries
      (`get_operation_history`, `inspect_operation`,
      `run_rollback_assistant`) реально callable на
      `onec_platform`. Узкий automatic-rollback whitelist Step 4
      явно отмечен как **honest constraint**, не gap.
    - **D. Real-stand / binary foundation.**
      `onec_binary_path` declared, `onec_dumpcfg_command_template`
      declared. Inspection **контракта**, не probing бинаря —
      ничего не запускается; smoke-test'ы остаются территорией
      `run_real_stand_smoke_test`.
    Verdict через детерминистический `_classify_foundation_level`:
    `"absent"` если секция отсутствует; `"strong"` ровно когда
    все четыре section_score'а на максимуме И нет error-finding'ов;
    `"partial"` для identity ≥ 2 / operability ≥ 2; иначе
    `"minimal"`. `ready_for_enterprise_track` = (`level ==
    "strong"` AND `errors == 0`).
  - `apps/platform/src/onec_platform/__init__.py` — добавлен
    re-export новой поверхности: `inspect_enterprise_foundation`
    / `inspect_enterprise_foundation_from_json_file` /
    `EnterpriseFoundationSettings` / `EnterpriseFoundationResult`
    / `DEPLOYMENT_TIERS` / `FOUNDATION_LEVELS`.
- **Что НЕ тронуто.** `mcp-read-server`, `mcp-write-server`,
  `mcp-intelligence-server`, `onec-policy-engine`, `onec-config`,
  `onec-audit`, `onec-health`, `onec-process-runner`,
  `onec-troubleshooting`, `mcp-common`, `selfcheck.py`,
  `bootstrap_paths.ps1`, `pyproject.toml`, `.github/`,
  `docs/runbooks/local-dev-check.md` — все без правок.
  Никаких новых MCP tool'ов; никакого нового runtime supervision
  slice'а; никакого нового write-tool'а; никакого probing 1cv8
  binary'а.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase6_step8_check.py`
  прогоняет 13 сценариев на synthetic tempdir:
  - **R1** registry invariants pre/post — `read=15, write=25,
    intelligence=16`, без drift'а.
  - **R2** zero `onec_policy_engine` real imports под
    `apps/platform/src/` и `apps/mcp-intelligence-server/src/`.
  - **A1** Step 1–7 config без enterprise секции грузится;
    `bootstrap_product` ok=True.
  - **A2** `build_product_config_template(...)` без
    enterprise_* kwargs **не** эмитит блок; round-trip через
    `load_product_config` валиден.
  - **A2'** template **с** enterprise_* kwargs эмитит блок;
    round-trip восстанавливает все шесть полей.
  - **B1** strong, fully-set foundation:
    `foundation_level='strong'`,
    `ready_for_enterprise_track=True`, sections=(identity=3/3,
    operability=3/3, traceability=2/2, binary=2/2), errors=0.
  - **C1** enterprise секция absent →
    `foundation_level='absent'`, ready=False, finding
    `foundation_enterprise_section_absent`.
  - **C2** prod-like без `instance_id` / `config_owner` →
    ready=False, error-findings
    `foundation_instance_id_missing_on_prod` +
    `foundation_config_owner_missing_on_prod`.
  - **C3** enabled service с `logs_enabled=False` →
    `foundation_level != "strong"`, finding
    `foundation_logs_disabled_on_enabled_services`.
  - **C4** prod-like без binary contract → ready=False,
    error-findings `foundation_onec_binary_path_missing_on_prod` +
    `foundation_onec_dumpcfg_template_missing_on_prod`.
  - **C5** manuals presence detection — exactly one of
    `foundation_manuals_present` / `foundation_manuals_missing`
    fires.
  - **D1** malformed enterprise shape (7 cases:
    `deployment_tier="garbage"`, `deployment_tier=int`,
    `change_control_required="true"`,
    `require_operator_identity=int`, `instance_id=""`, unknown
    key, `enterprise as list`) — все возвращают `ok=False`
    без exception'а наружу.
  - **D2** bad JSON file → `_from_json_file` ok=False.
  - **D3** non-dict root (string / list) → boundary ok=False
    без crash'а.
  - **E1** `suggested_tools` / `suggested_write_tools`
    содержат только реальные имена из live registries +
    `_KNOWN_PLATFORM_FUNCTIONS` whitelist.
- **dev-check.** `scripts/dev/run_dev_check.ps1` остаётся
  зелёным. Registry counts: `read=15, write=25,
  intelligence=16`. `imports_ok = true`,
  `selfcheck_status = ok`. `selfcheck.py` намеренно не дёргает
  Step 8 enterprise-foundation flow — manual check покрывает
  все ветки на synthetic стенде.

### Phase 6 / Step 9 — final integration pass (завершён, Phase 6 закрыта)

- **Архитектурное решение Step 9.** Это не planning-step, не
  расширение surface'а. Это **закрывающий integration прогон
  всей Phase 6** одним связным сценарием + honest failure paths
  + discipline asserts. Brief требовал, чтобы все Phase 6
  slice'ы реально сходились в работающий контур; чтобы
  `add_form_attribute` (Step 5) был exercised именно через
  guided workflow; чтобы binary-backed `create_dump_snapshot`
  (Step 2) был доказан как реальный subprocess-путь, а не stub
  fallback; чтобы post-rollback verify был **содержательный**,
  а не «tool ok=True». Все эти требования сошлись.
- **Кодовые правки Step 9 — две минимальные.** Brief разрешает
  правки, если без них честный прогон невозможен; обе правки
  production-уровня, локальные, без MCP-surface drift'а:
  - `apps/platform/src/onec_platform/workflow.py` +
    `apps/platform/src/onec_platform/models.py`. Добавлен один
    тонкий guided-wrapper `safe-add-form-attribute` над уже
    существующим public `add_form_attribute`. Без него
    brief'овский «`run_guided_workflow → add_form_attribute`»
    структурно невозможен (Step 5 ship'нул только
    write-tool'ный slice без guided-обёртки). `WORKFLOW_NAMES`
    стал из 3 имён 4-мя; `_WORKFLOW_RUNNERS` получил один новый
    runner (`_run_safe_add_form_attribute`); внутри тот же
    pattern, что у `safe-add-attribute`: dashboard-precondition,
    intelligence-сигналы (`estimate_change_impact` +
    `summarize_configuration_risk`), confirm gate, mutating
    write через public `add_form_attribute` (которое само идёт
    через `run_write_flow`), verify через
    `verify_metadata_change(kind="form_attribute_exists")`.
    Plan summary честно говорит, что rollback будет advisory-
    only (whitelist Step 4 не покрывает `add_form_attribute`).
  - `apps/platform/src/onec_platform/installer.py` —
    `_config_to_dict` был **багом-носителем** real Step 6 / 8
    регрессии: helper не эмитил Step 6 service-level поля
    (`restart_policy` / `logs_enabled` / `log_max_bytes`) и
    Step 8 enterprise-блок при install-fast-path round-trip'е.
    То есть оператор пишет в input config'е enterprise-секцию,
    зовёт `run_install_fast_path(confirm_write=True)`, JSON
    материализуется на диск без enterprise-блока, и затем
    `inspect_enterprise_foundation_from_json_file` на этом
    materialised JSON отдаёт `foundation_level='absent'`. Это
    был silent gap между Step 3 и Step 6 / 8. Step 9 закрыл
    его минимально: каждый из новых fields эмитится только
    когда отличается от dataclass default'а (значит, Step 1–5
    конфиги по-прежнему round-trip'ят byte-identical).
  - Никаких других кодовых правок. **MCP registries не
    изменены**: `read=15, write=25, intelligence=16` — без
    drift'а. `onec-policy-engine`, `mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`, все
    `packages/onec-*/` — не тронуты.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase6_step9_check.py`
  (~600 строк) на synthetic tempdir + local HTTPServer +
  реальные `subprocess.Popen` (sleeper в runtime, copytree
  для binary-backed snapshot, `print('ok')` / `sys.exit(7)`
  для smoke). Никакого реального 1cv8 binary, никакого
  внешнего интернета.
  - **Scenario A — 16 связных шагов:** A.1 `bootstrap_product`
    → A.2 `run_install_fast_path(confirm_write=True)` (Step 3,
    JSON атомарно записан, round-trip ok) → A.3
    `start_product_runtime_from_json_file` (Step 6, реальный
    PID alive) → A.4 status (PID, log paths, last_started_at)
    → A.5 dashboard `overall_status='healthy'`,
    `ready_for_workflows=True` (Step 4) → A.6
    `run_guided_workflow(safe-add-attribute, target_kind=catalog,
    confirm_execute=True)` — реальный
    `add_catalog_attribute` через `run_write_flow`, real
    binary-backed `create_dump_snapshot` (snapshot directory
    физически содержит **скопированный**
    `Catalogs/SampleCatalog.xml` — это структурное
    доказательство binary-backed mode, а не stub'а; в stub
    режиме была бы только `dump-created.txt` marker'а),
    `operation_id` извлечён из `wf_cat.last_write_operation`
    → A.7 `run_guided_workflow(safe-add-form-attribute,
    confirm_execute=True)` — Step 5 structural slice через
    новый guided-wrapper; ElementTree-путь structurally создаёт
    пустой `<Attributes>` блок внутри `<Form name="MainForm">`
    и вставляет туда новый `<Attribute>`; second snapshot тоже
    binary-backed → A.8 history (обе operation_id'и видны) →
    A.9 inspect (catalog op'а;
    `automatic_recovery_supported=True`) → A.10
    `run_rollback_assistant(confirm_execute=True)` —
    `mode='executed', ok=True, execution_performed=True`,
    идёт через public `restore_dump_file_from_snapshot` (то
    есть через тот же `run_write_flow` — НЕ back-door
    filesystem write); один `write_result` (ok=True) + один
    `verify_result` от `diff_dump_fragment`
    (`data.changed=False`) → A.11 **post-rollback verify** —
    re-parse XML через ElementTree, **структурно** подтверждено
    что нет ни `Step9CatalogField`, ни `Step9FormField`; live
    XML byte-equals оригинальной fixture (snapshot catalog
    op'а был сделан до обоих writes — это honest semantics
    rollback'а: «restore the file to the moment the
    rolled-back operation started», не selective undo) →
    A.12 `get_real_stand_readiness` (Step 7,
    `ready_for_real_stand_smoke=True`) → A.13
    `run_real_stand_smoke_test(confirm_execute=True)` — Step 7
    реальный subprocess через `sys.executable` с probe args
    `["-c", "print('ok')"]`, `binary_invoked=True,
    binary_exit_code=0` → A.14
    `inspect_enterprise_foundation_from_json_file` — Step 8 на
    том же materialised JSON-config'е (после fix'а в
    `_config_to_dict`),
    `foundation_level='strong',
    ready_for_enterprise_track=True` → A.15
    `stop_product_runtime` — PID реально умирает
    (`is_pid_alive(pid)=False` после polling'а) → A.16 log
    files `<work_dir>/.runtime/logs/demo.{out,err}.log`
    physically present.
  - **Шесть honest failure paths (F1–F6):**
    - F1 — workflow blocked by unhealthy dashboard (no
      gateway → `mode='blocked', execution_performed=False`,
      файл untouched);
    - F2 — rollback unsupported для `add_form_attribute`
      (вне Step 4 whitelist'а): сначала запустили workflow
      `safe-add-form-attribute(confirm_execute=True)` чтобы
      получить реальный operation_id; затем
      `run_rollback_assistant(confirm_execute=True)` →
      `mode='unsupported', ok=True,
      execution_performed=False, write_results=[],
      verify_results=[]`;
    - F3 — broken JSON config (`{ this is not json`) через
      **девять** `_from_json_file` boundary'ев (включая
      Step 8 `inspect_enterprise_foundation_from_json_file`,
      Step 7 `run_real_stand_smoke_test_from_json_file`,
      Step 3 `run_install_fast_path_from_json_file`,
      Step 5 `run_guided_workflow_from_json_file`,
      Step 6 `get_product_runtime_status_from_json_file`,
      Step 4 `build_environment_dashboard_from_json_file`,
      Step 2 `bootstrap_product_from_json_file`,
      Step 6 `get_operation_history_from_json_file`,
      Step 7 `get_real_stand_readiness_from_json_file`) —
      все возвращают `ok=False` без exception'а наружу;
    - F4 — real-stand smoke с реальным non-zero exit (probe
      = `["-c", "import sys; sys.exit(7)"]`) →
      `mode='executed', binary_invoked=True,
      binary_exit_code=7, ok=False`;
    - F5 — enterprise foundation на prod-like config'е без
      `instance_id` / `config_owner` / `onec_binary_path` /
      `onec_dumpcfg_command_template` →
      `foundation_level='minimal', ready=False`,
      четыре error-finding'а (`*_missing_on_prod`);
    - F6 — binary-backed `create_dump_snapshot` падает с
      operator-declared template'ом, который exit'ит 7 →
      workflow `ok=False, stage='dump_snapshot'` (т.е. flow
      честно остановился на снапшот-стадии), без silent
      stub fallback'а; live XML untouched (Step 2 «no
      runtime fallback once binary contract is declared»
      contract).
  - **Discipline asserts (D1–D5):**
    - D1 registry invariants pre/post — `read=15, write=25,
      intelligence=16` без drift'а;
    - D2 — 0 реальных import'ов `onec_policy_engine` под
      `apps/platform/src/` и
      `apps/mcp-intelligence-server/src/` (тонкий scan
      только настоящих `import` / `from … import …`
      statement'ов, без docstring-noise'а);
    - D3 — 14 списков `suggested_tools` /
      `suggested_write_tools` собраны со всех Scenario A
      результатов; все имена входят в union live registries
      + `_KNOWN_PLATFORM_FUNCTIONS`; made-up name отвергнут
      `_allow_only_real_tools`;
    - D4 — каждый boundary-вызов в скрипте обёрнут в
      `must_not_raise(...)`; ни один не сработал — ни одна
      product-layer boundary не raise'нула наружу;
    - D5 — отсутствие back-door write channel'а структурно
      следует из D2 (product layer не импортирует
      policy-engine; единственный mutating путь — через
      public write-tools, идущие через `run_write_flow`).
  - Финальная строка скрипта: `All Phase 6 / Step 9
    scenarios passed.`
- **dev-check.** `scripts/dev/run_dev_check.ps1` остаётся
  зелёным после Step 9. Registry counts: `read=15, write=25,
  intelligence=16` — без изменений; `imports_ok = true`,
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`,
  `bootstrap_paths.ps1`, `pyproject.toml`, `.github/` не
  тронуты.

### Parallel Track A / Step 1 — planning Full Real 1cv8-backed Write Path (завершён)

- **Почему этот трек открыт.** Phase 6 закрыла product
  contour (install / runtime / dashboard / guided
  workflows / rollback / real-stand smoke / enterprise
  foundation). Это **finished product behavior** на
  reference stand'е в **smoke**-форме. Это **не**
  finished real-write product behavior на реальной 1cv8
  binary'е. Самый жирный незакрытый разрыв сейчас — не
  все mutating-write-path'ы доведены до настоящего
  real 1cv8-backed исполнения:
  `apply_config_from_files` и
  `update_database_configuration` остаются Phase 2
  stub-backed; `create_dump_snapshot` имеет binary-backed
  branch (Phase 6 / Step 2), но это partial generic
  slice, не finished contract; на reference stand'е нет
  настоящего multi-step round-trip'а с реальным 1cv8;
  operator-facing contract для binary-backed write
  execution размыт. Track A открыт как первый из
  parallel / completion tracks **после** закрытой
  Phase 6 чтобы доводить именно эту узкую зону —
  real execution layer для apply / update-db / dumpcfg
  — до honest finished behavior. Это **не** Phase 7;
  Phase 7 как отдельная крупная интеграционная фаза не
  запланирована.
- **Какие два документа созданы.**
  - `docs/architecture/track-a-real-write-path-plan.md`
    (новый, ~285 строк): назначение трека, целевой
    результат (семь пунктов operator-facing нарратива
    после закрытия трека), что именно закрывает трек и
    что НЕ закрывает, чем трек отличается от закрытой
    Phase 6, пять крупных блоков (A — real binary-backed
    dump/apply/update contract; B — reference stand
    execution choreography; C — product-layer
    integration over real write path; D —
    operator-facing diagnostics and honest mode
    reporting; E — final validation and closure),
    guardrails (одиннадцать жёстких инвариантов), явный
    список «что НЕ входит в трек», 10 критериев
    приёмки, 9 открытых вопросов Step 1.
  - `docs/architecture/track-a-real-write-path-step-map.md`
    (новый, ~250 строк): семь шагов трека в едином
    формате (Цель / Что меняем / Затронутые зоны /
    Результат) — Step 1 documentation-only entry → Step
    2 real binary-backed `apply_config_from_files` → Step
    3 real binary-backed `update_database_configuration`
    → Step 4 unify / finish `create_dump_snapshot` real
    path + payload discipline → Step 5 product-layer
    integration over real write path → Step 6 reference
    stand multi-step round-trip → Step 7 final
    integration pass and Track A closure.
- **Что обновлено в README / status.**
  - Корневой `README.md` — добавлен раздел **«Active
    parallel track»** после блока «Активных фаз нет»;
    Track A объявлен; даны ссылки на оба новых
    документа; явно сказано «Это **post-phase
    completion track**, **не** новая Phase 7»; список
    того, что НЕ входит в Track A, продублирован
    кратко. В разделе документов архива добавлен
    подраздел «Документы parallel-track'ов» со
    ссылками на оба новых документа.
  - `PROJECT-STATUS.md` (этот файл) — заголовок
    «Текущий шаг» переключён на **Parallel Track A /
    Step 1**; статус → `in progress`; полный detail
    block (этот раздел); «Phase 6 закрыта» внизу
    остаётся как окончательная фиксация закрытия
    Phase 6.
- **Кода ничего не менялось.** Это намеренно
  documentation-only opening step. `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `.github/`,
  `.claude.json` — все без правок. Никаких новых MCP
  tool'ов. Никаких новых product-layer boundary'ев.
  Никакого расширения registry. Никакого нового
  payload-поля у write-tool'ов. Никакого нового
  workflow'а / readiness-check'а / inspector'а. Все
  изменения — только в `docs/architecture/` (два
  новых файла) + корневой `README.md` + этот файл.
- **Registry counts без изменений.** read = 15;
  write = 25; intelligence = 16. dev-check остаётся
  зелёным (потому что в коде ничего не менялось —
  специально для documentation-only-шага запускать
  dev-check необязательно, но он по-прежнему зелёный).
- **Какой следующий шаг.** **Parallel Track A / Step 2
  — real binary-backed `apply_config_from_files`
  contract.** Step 2 закроет часть критерия приёмки 1
  трека: первый из двух Phase 2 stub-backed-путей
  переходит на honest dual-mode contract с real
  execution. Затрагиваемые зоны Step 2: точечно
  `apps/mcp-write-server/src/mcp_write_server/tools.py`
  + (возможно) shared helper в `runtime/`; точечно
  `packages/onec-config/src/onec_config/models.py` +
  `loader.py` (одно новое optional-поле в
  `EnvironmentConfig` + strict-validation,
  fail-closed на bad shape). Read- и intelligence-
  серверы Step 2 не трогает. `onec_policy_engine`
  не трогает. Registries Step 2 не растит — это та
  же операция с расширенным dispatch'ем, как
  Phase 6 / Step 2 расширил `create_dump_snapshot`.
  По умолчанию решение по Q1 (одно поле
  `onec_apply_command_template` или общий словарь
  `onec_command_templates`) фиксируется именно в
  Step 2 трека.
- **Что осталось до закрытия трека.** Шесть шагов
  (Step 2–7):
  - Step 2 — real binary-backed
    `apply_config_from_files` contract (часть
    критерия приёмки 1 + 4 + 5);
  - Step 3 — real binary-backed
    `update_database_configuration` contract
    (полное закрытие критерия 1);
  - Step 4 — unify / finish `create_dump_snapshot`
    real path + payload discipline (полное закрытие
    критерия 5);
  - Step 5 — product-layer integration через
    существующие boundary'и без правок их логики
    (критерий 3 + часть критерия 9);
  - Step 6 — reference stand multi-step round-trip с
    настоящим 1cv8 binary'ом (критерий 2);
  - Step 7 — final integration pass + закрытие трека
    (критерии 6, 7, 8, 9, 10).
  По умолчанию каждый шаг (после Step 1) имеет
  собственный manual integration check вне проекта
  (`phase-tracka-stepN-check.py` или эквивалент по
  существующей конвенции `phase6_stepN_check.py`).
  dev-check остаётся зелёным после каждого
  кодового шага.

### Parallel Track A / Step 2 — real binary-backed `apply_config_from_files` contract (завершён)

- **Цель шага.** Перевести существующий public write-tool
  `apply_config_from_files(...)` с чисто stub-backed
  поведения на honest dual-mode contract — симметрично с
  тем, что Phase 6 / Step 2 сделал для
  `create_dump_snapshot(...)`. При наличии полного
  binary contract'а у environment'а (`onec_binary_path` +
  `onec_applycfg_command_template`) — реальный subprocess
  через `onec_process_runner.run_process`. При
  отсутствии — старое stub-backed поведение (Phase 2 /
  Step 7) **без изменений**. Runtime failure в
  binary-backed ветке = honest failure без silent
  fallback'а на stub. Закрывает часть критериев приёмки
  трека 1, 4, 5; полностью **не закрывает** критерий 1
  (Step 3 закроет оставшийся `update_database_configuration`)
  и **не закрывает** критерии 2, 3, 6, 7, 8, 9, 10
  (это работа Step 3–7 трека).
- **Что реально появилось в коде.**
  - `packages/onec-config/src/onec_config/models.py` —
    `EnvironmentConfig` получил одно новое optional-поле
    `onec_applycfg_command_template: list[str] | None =
    None`. Default `None` сохраняет backward compatibility:
    Phase 1–6 конфиги без поля грузятся без изменений.
    Docstring расширен абзацем про Track A / Step 2 с
    явной фиксацией философии «platform does not invent
    1cv8 CLI grammar».
  - `packages/onec-config/src/onec_config/loader.py` —
    `load_project_config` строго валидирует новое поле
    fail-closed: `None` или `non-empty list[str]`,
    остальное → `ValueError` с понятным сообщением.
    Mirror discipline уже-имеющегося
    `onec_dumpcfg_command_template` validation'а.
  - `packages/onec-config/README.md` — добавлен
    подраздел про новое поле (whitelist placeholders:
    `binary_path` / `source_dump_path` / `base_path` /
    `base_id` / `publication_name` / `http_base_url`) +
    усиленный абзац «Философия binary-related полей»
    (явно сказано «platform does not guess 1cv8 CLI
    grammar», «no shell strings», «unknown placeholder
    fail-closed на render-time»).
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — добавлены три module-level константы:
    `_APPLYCFG_TEMPLATE_PLACEHOLDERS` (frozenset
    из шести whitelisted имён),
    `_APPLYCFG_OUTPUT_EXCERPT_LIMIT = 1024`,
    `_APPLYCFG_DEFAULT_TIMEOUT_SECONDS = 300`.
    Mirror констант, уже имеющихся для dumpcfg.
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — добавлены три приватных helper'а:
    `_render_applycfg_command(...)` (whitelisted
    placeholder substitution, fail-closed на unknown
    placeholder),
    `_build_apply_stub_callables(source_dump_path)`
    (возвращает `(operation, verify)` для legacy stub
    branch'а; обёртывает существующий
    `run_stub_apply_process` чтобы добавить Track A /
    Step 2 honest-mode поля без изменений в самом legacy
    stub helper'е),
    `_build_apply_binary_backed_callables(command,
    source_dump_path)` (возвращает `(operation,
    verify)` для binary-backed branch'а: operation
    спавнит subprocess через `run_process` с captured
    stdout/stderr, **всегда** возвращает dict с
    honest-mode полями; verify проверяет
    `completed=True, exit_code=0` и raise'ит
    `AssertionError` иначе — это и есть
    no-silent-fallback discipline).
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — `apply_config_from_files(...)` переписан как
    тонкий dispatcher: проверяет наличие обоих полей
    binary contract'а; при unknown placeholder в
    binary-backed branch'е возвращает `ok=False`
    **до** входа в `run_write_flow` (никаких
    snapshots, никаких audit rows для render-failed
    вызовов); при полном contract'е выбирает
    binary-backed callables; при отсутствии — stub
    callables; в обоих случаях идёт через
    `run_write_flow(...)` (preflight + snapshot +
    operation + verify + audit обязательны для обеих
    веток). Tool name результата возвращается через
    существующий `_with_tool_name` — `apply_config_from_files`,
    не внутреннее имя flow'а.
  - **Не тронуто.** `runtime/dump_ops.py` (legacy stub
    helper) не редактировался ни в одной строке — Track
    A / Step 2 обёртывает его, не переписывает.
    `create_dump_snapshot(...)` не редактировался —
    финальная унификация payload-discipline между
    тремя binary-backed write-tool'ами это работа Step
    4 трека. `update_database_configuration` не
    редактировался — это Step 3 трека. Никаких новых
    MCP tool'ов; никакого нового product-layer
    slice'а; никаких изменений в `mcp-read-server`,
    `mcp-intelligence-server`, `apps/platform/`,
    `onec-policy-engine`, `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`,
    `.github/`, `.claude.json`.
- **Operator-facing payload-контракт (симметрия с
  `create_dump_snapshot`).** В обоих режимах
  `operation_payload` несёт один и тот же набор полей:
  `mode ∈ {"stub", "binary-backed"}`, `binary_invoked: bool`,
  `exit_code: int | None`, `command_preview: list[str] |
  None`, `stdout_excerpt: str | None`,
  `stderr_excerpt: str | None`. Stub-режим эмитит `None`
  / `False` для тех полей, которые ему неприменимы;
  никакой магии, никакого скрытого поведения —
  оператор видит честную картину.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase-tracka-step2-check.py`
  прогоняет 7 сценариев на synthetic tempdir + local
  HTTPServer (gateway). Все семь зелёные:
  - **A** — registry invariants `read=15 / write=25 /
    intelligence=16` без drift'а; `apply_config_from_files`
    в registry; никаких новых tool names не
    проскочило (полный whitelist 25 имён сравнён
    set'ом).
  - **B** — backward compatibility: env без
    `onec_applycfg_command_template` →
    `apply_config_from_files` работает в stub-режиме
    как раньше; `operation_payload.mode='stub'`,
    `binary_invoked=False`; legacy `apply-stub.txt`
    + `apply-meta.json` создаются в `source_dump_path`.
  - **C** — happy binary-backed path: env с binary
    contract'ом + operator-declared template'ом
    (`python -c <script>` + marker path); subprocess
    реально запускается; `mode='binary-backed',
    binary_invoked=True, exit_code=0`;
    `command_preview` corretto; **operator-declared
    marker file** physically на диске (доказательство
    реального subprocess'а, не fake'а); legacy stub
    marker `apply-stub.txt` отсутствует в этом
    режиме.
  - **D** — binary-backed runtime failure (template
    exits 7): `ok=False`, `mode='binary-backed',
    binary_invoked=True, exit_code=7`,
    `stage='verify'`; `operation_payload`
    сохраняется (run_write_flow preserves it on
    verify-stage failures); legacy stub marker
    отсутствует — **никакого silent fallback'а**.
  - **E** — loader fail-closed на пять bad-shape
    вариантов (`"not a list"` / `[binary, 1, "-c"]`
    int item / `[]` empty / `[[binary, "-c"]]`
    nested list / `{"argv": [...]}` dict-not-list)
    — все пять `ValueError` с понятным сообщением.
    Positive control: `None` принимается loader'ом
    (legacy compat).
  - **F** — unknown placeholder (`{not_in_whitelist}`
    в template'е): tool возвращает `ok=False` **до**
    запуска subprocess'а; `binary_invoked=False`,
    `command_preview=None`; message содержит список
    allowed placeholders (`binary_path`,
    `source_dump_path`, ...); никакая `_snapshots`
    директория не создаётся.
  - **G** — integration через `run_write_flow`:
    standard flow shape preserved
    (`stage='completed'`, `operation_id`,
    `audit_path`, `backup_snapshot_path`,
    `dump_snapshot_path`, `operation_payload`,
    `verify_payload`); audit row пишется с
    `tool_name='apply_config_from_files'`,
    `status='ok'`; binary-backed branch реально
    отрабатывает (а не silent stub) —
    `operation_payload.mode='binary-backed'` +
    operator-declared marker physically на диске.
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным после Step 2. Вывод последнего
  прогона: `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 25 имён без изменений
  (`apply_config_from_files` уже там, не появился
  как новый), `intelligence_server_tools` — 16 имён
  без изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`,
  `bootstrap_paths.ps1`, `pyproject.toml`,
  `.github/` не тронуты.
- **Что осталось до закрытия Track A.** Пять шагов
  (Step 3–7):
  - Step 3 — real binary-backed
    `update_database_configuration` contract (полное
    закрытие критерия 1);
  - Step 4 — unify / finish `create_dump_snapshot`
    real path + payload discipline (полное закрытие
    критерия 5);
  - Step 5 — product-layer integration через
    существующие boundary'и без правок их логики
    (критерий 3);
  - Step 6 — reference stand multi-step round-trip с
    настоящим 1cv8 binary'ом (критерий 2);
  - Step 7 — final integration pass + закрытие трека
    (критерии 6, 7, 8, 9, 10).
- **Следующий шаг.** **Parallel Track A / Step 3 —
  real binary-backed `update_database_configuration`
  contract.** Симметричная Step 2 правка для второго
  оставшегося Phase 2 stub-backed-пути. Затрагиваемые
  зоны Step 3: точечно
  `apps/mcp-write-server/src/mcp_write_server/tools.py`
  (использовать helper'ы из Step 2 если они применимы;
  иначе мелкая duplication до Step 4 финальной
  унификации) + `packages/onec-config/` (одно новое
  optional-поле `onec_updatedb_command_template`).
  Read- и intelligence-серверы Step 3 не трогает.
  `onec_policy_engine` не трогает. Registries Step 3
  не растит — это та же операция с расширенным
  dispatch'ем.

### Parallel Track A / Step 3 — real binary-backed `update_database_configuration` contract (завершён)

- **Цель шага.** Перевести существующий public write-tool
  `update_database_configuration(...)` с чисто
  stub-backed поведения на honest dual-mode contract —
  симметрично с тем, что Step 2 трека сделал для
  `apply_config_from_files(...)` и Phase 6 / Step 2 для
  `create_dump_snapshot(...)`. При наличии полного
  binary contract'а у environment'а (`onec_binary_path`
  + `onec_updatedb_command_template`) — реальный
  subprocess через `onec_process_runner.run_process`.
  При отсутствии — старое stub-backed поведение
  (Phase 2 / Step 9) **без изменений**. Runtime failure
  в binary-backed ветке = honest failure без silent
  fallback'а на stub. Закрывает оставшуюся часть
  критерия приёмки 1 трека (после Step 2 закрылась
  apply-часть; теперь updatedb-часть тоже закрыта) и
  часть критериев 4 и 5. Полностью **не закрывает**
  критерии 2, 3, 6, 7, 8, 9, 10 (это работа Step 4–7
  трека).
- **Что реально появилось в коде.**
  - `packages/onec-config/src/onec_config/models.py` —
    `EnvironmentConfig` получил одно новое
    optional-поле `onec_updatedb_command_template:
    list[str] | None = None`. Default `None` сохраняет
    backward compatibility: Phase 1–6 + Track A / Step 2
    конфиги без поля грузятся без изменений. Docstring
    расширен абзацем про Track A / Step 3 с явной
    фиксацией философии «platform does not invent 1cv8
    CLI grammar» и tighter-whitelist (нет
    `{output_path}` / `{source_dump_path}` — UpdateDBCfg
    операционно работает на живой инфобазе).
  - `packages/onec-config/src/onec_config/loader.py` —
    `load_project_config` строго валидирует новое поле
    fail-closed: `None` или `non-empty list[str]`,
    остальное → `ValueError` с понятным сообщением.
    Mirror discipline уже-имеющихся
    `onec_dumpcfg_command_template` /
    `onec_applycfg_command_template` validation'ов.
  - `packages/onec-config/README.md` — добавлен
    подраздел про новое поле (whitelist placeholders:
    `binary_path` / `base_path` / `base_id` /
    `publication_name` / `http_base_url` — пять имён,
    более узкий surface, чем у dumpcfg / applycfg);
    раздел «Философия binary-related полей» обновлён
    под пять полей; явно зафиксирован принцип
    отсутствия premature generalization («Track A /
    Step 3 переводит на binary-backed dispatch
    **только** `update_database_configuration` —
    финальная унификация payload-discipline между
    всеми тремя binary-backed write-tool'ами это
    задача Track A / Step 4»).
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — добавлены три module-level константы:
    `_UPDATEDB_TEMPLATE_PLACEHOLDERS` (frozenset
    из пяти whitelisted имён, без `output_path` /
    `source_dump_path`), `_UPDATEDB_OUTPUT_EXCERPT_LIMIT
    = 1024`, `_UPDATEDB_DEFAULT_TIMEOUT_SECONDS = 300`.
    Mirror констант, уже имеющихся для dumpcfg /
    applycfg.
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — добавлены три приватных helper'а:
    `_render_updatedb_command(...)` (whitelisted
    placeholder substitution через тот же
    `_PlaceholderProxy`-механизм, что у dumpcfg /
    applycfg; fail-closed на unknown placeholder с
    update-db-specific сообщением, перечисляющим
    `_UPDATEDB_TEMPLATE_PLACEHOLDERS`),
    `_build_updatedb_stub_callables()` (возвращает
    `(operation, verify)` для legacy stub branch'а;
    inline-логика стаба сохранена и обёрнута в
    Track A / Step 3 honest-mode поля без изменений в
    самих side-effect'ах stub'а — `.update-db-stub.txt`
    и `.update-db-meta.json` пишутся как раньше),
    `_build_updatedb_binary_backed_callables(command)`
    (возвращает `(operation, verify)` для
    binary-backed branch'а: operation спавнит
    subprocess через `run_process` с captured
    stdout/stderr, **всегда** возвращает dict с
    honest-mode полями; verify проверяет
    `completed=True, exit_code=0` и raise'ит
    `AssertionError` иначе — это и есть
    no-silent-fallback discipline).
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — `update_database_configuration(...)` переписан
    как тонкий dispatcher: проверяет наличие обоих
    полей binary contract'а; при unknown placeholder в
    binary-backed branch'е возвращает `ok=False`
    **до** входа в `run_write_flow` (никаких snapshots,
    никаких audit rows для render-failed вызовов); при
    полном contract'е выбирает binary-backed
    callables; при отсутствии — stub callables; в
    обоих случаях идёт через `run_write_flow(...)`
    (preflight + snapshot + operation + verify + audit
    обязательны для обеих веток). Tool name
    результата возвращается через существующий
    `_with_tool_name` —
    `update_database_configuration`, не внутреннее имя
    flow'а.
  - **Не тронуто.** `apply_config_from_files(...)` уже
    переведён на Step 2 — здесь не редактировался ни в
    одной строке. `create_dump_snapshot(...)` тоже не
    редактировался — финальная унификация
    payload-discipline между всеми тремя
    binary-backed write-tool'ами это работа Step 4
    трека. Никаких новых MCP tool'ов; никакого
    нового product-layer slice'а; никаких изменений в
    `mcp-read-server`, `mcp-intelligence-server`,
    `apps/platform/`, `onec-policy-engine`,
    `onec-audit`, `onec-health`,
    `onec-process-runner`, `onec-troubleshooting`,
    `mcp-common`, `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`,
    `.github/`, `.claude.json`.
- **Operator-facing payload-контракт (симметрия с Step 2
  и Phase 6 / Step 2).** В обоих режимах
  `operation_payload` несёт один и тот же набор полей:
  `mode ∈ {"stub", "binary-backed"}`,
  `binary_invoked: bool`, `exit_code: int | None`,
  `command_preview: list[str] | None`,
  `stdout_excerpt: str | None`,
  `stderr_excerpt: str | None`. Stub-режим эмитит
  `None` / `False` для тех полей, которые ему
  неприменимы. Это тот же набор полей, который уже
  эмитят `create_dump_snapshot` (Phase 6 / Step 2) и
  `apply_config_from_files` (Track A / Step 2) —
  единый ментальный шаблон оператора «как читать
  binary-backed write payload».
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase-tracka-step3-check.py`
  прогоняет 7 сценариев на synthetic tempdir + local
  HTTPServer (gateway). Все семь зелёные:
  - **A** — registry invariants `read=15 / write=25 /
    intelligence=16` без drift'а;
    `update_database_configuration` в registry; полный
    whitelist 25 имён сравнён set'ом — никаких новых
    tool names и никаких missing names.
  - **B** — backward compatibility: env без
    `onec_updatedb_command_template` →
    `update_database_configuration` работает в
    stub-режиме как раньше;
    `operation_payload.mode='stub',
    binary_invoked=False`; honest-mode поля
    `exit_code/command_preview/stdout_excerpt/stderr_excerpt`
    все `None`; legacy `.update-db-stub.txt` (`'updated'`)
    и `.update-db-meta.json` (`mode: "stub-update-db"`,
    `base_id: "local-dev"`) создаются в `dump_path`.
  - **C** — happy binary-backed path: env с binary
    contract'ом + operator-declared template'ом
    (`python -c <script>` + marker path); subprocess
    реально запускается; `mode='binary-backed',
    binary_invoked=True, exit_code=0`;
    `command_preview` corretto (argv list с
    `sys.executable`); operator-declared marker file
    (`'updatedb ok'`) physically на диске
    (доказательство реального subprocess'а, не fake'а);
    legacy stub markers `.update-db-stub.txt` и
    `.update-db-meta.json` отсутствуют в этом
    режиме.
  - **D** — binary-backed runtime failure (template
    exits 7): `ok=False`, `mode='binary-backed',
    binary_invoked=True, exit_code=7`,
    `stage='verify'`; `operation_payload`
    сохраняется (run_write_flow preserves it on
    verify-stage failures); legacy stub markers
    отсутствуют — **никакого silent fallback'а**.
  - **E** — loader fail-closed на семь bad-shape
    вариантов (`"not a list"` / `[bin, 1, "-c"]` int
    item / `[bin, True, "-c"]` bool item /
    `[bin, {"k": "v"}, "-c"]` dict item / `[]` empty /
    `[[bin, "-c"]]` nested list / `{"argv": [...]}`
    dict-not-list) — все семь `ValueError` с понятным
    сообщением. Positive controls: `None` принимается
    loader'ом (legacy compat); valid `[bin, "-c",
    "pass"]` сохраняется как
    `EnvironmentConfig.onec_updatedb_command_template`.
  - **F** — unknown placeholder
    (`{not_in_whitelist}` в template'е): tool
    возвращает `ok=False` **до** запуска
    subprocess'а; `binary_invoked=False`,
    `command_preview=None`; message содержит список
    allowed placeholders (`binary_path`, `base_id`,
    ...); никакая `_snapshots` директория не
    создаётся. **Дополнительно:**
    `{output_path}` и `{source_dump_path}` (которые
    в whitelist'е dumpcfg / applycfg, но **не** в
    update-db whitelist'е) тоже отвергнуты —
    подтверждает tighter-whitelist для UpdateDBCfg.
  - **G** — integration через `run_write_flow`:
    standard flow shape preserved
    (`stage='completed'`, `operation_id`,
    `audit_path`, `backup_snapshot_path`,
    `dump_snapshot_path`, `operation_payload`,
    `verify_payload`); audit row пишется с
    `tool_name='update_database_configuration'`,
    `status='ok'`; binary-backed branch реально
    отрабатывает (а не silent stub) —
    `operation_payload.mode='binary-backed'` +
    operator-declared marker physically на диске.
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным после Step 3. Вывод последнего
  прогона: `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 25 имён без изменений
  (`update_database_configuration` уже там, не
  появился как новый), `intelligence_server_tools` —
  16 имён без изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`,
  `bootstrap_paths.ps1`, `pyproject.toml`,
  `.github/` не тронуты.
- **Что осталось до закрытия Track A.** Четыре шага
  (Step 4–7):
  - Step 4 — unify / finish `create_dump_snapshot`
    real path + payload discipline (полное закрытие
    критерия 5 трека; финальная унификация helper'ов
    между всеми тремя binary-backed write-tool'ами);
  - Step 5 — product-layer integration через
    существующие boundary'и без правок их логики
    (критерий 3);
  - Step 6 — reference stand multi-step round-trip с
    настоящим 1cv8 binary'ом (критерий 2);
  - Step 7 — final integration pass + закрытие трека
    (критерии 6, 7, 8, 9, 10).
- **Следующий шаг.** **Parallel Track A / Step 4 —
  unify / finish `create_dump_snapshot` real path +
  payload discipline.** Задача — привести
  payload-поля и shared helper'ы к одному
  contract'у между тремя binary-backed write-tool'ами
  (`create_dump_snapshot`, `apply_config_from_files`,
  `update_database_configuration`). Решает Q3
  открытого вопроса Step 1 плана: где живут shared
  helper'ы (новый module `runtime/process_dispatch.py`
  или private helpers внутри `tools.py`). Затрагиваемые
  зоны Step 4: точечно
  `apps/mcp-write-server/src/mcp_write_server/`
  (рефакторинг внутрь, **не** наружу — operator-
  declared контракт не ломается; placeholders
  остаются те же; argv-grammar остаётся та же).
  Read-, intelligence- и product-серверы Step 4 не
  трогает. Registries Step 4 не растит.

### Parallel Track A / Step 4 — unify / finish create_dump_snapshot real path + payload discipline (завершён)

- **Цель шага.** Закрыть Q3 открытого вопроса Step 1
  плана трека (где живут shared helper'ы) и привести
  внутреннюю реализацию трёх binary-backed write-tool'ов
  (`create_dump_snapshot`, `apply_config_from_files`,
  `update_database_configuration`) к единой shared
  internal-only mechanic'е без расширения surface'а,
  без новых MCP tool'ов, без изменений operator-facing
  argv grammar / placeholder whitelist'ов / ToolResult
  shape. Также — закрыть payload-discipline gap у
  `create_dump_snapshot` (несколько ветвей до Step 4
  не несли всех шести honest-mode полей).
- **Что реально появилось в коде.**
  - **Новый internal-only module:**
    `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`
    (~280 строк). Не public API, не registered MCP
    tool, не product-layer surface — используется
    только тремя public binary-backed write-tool'ами и
    больше никем. Содержит:
    - `BINARY_OUTPUT_EXCERPT_LIMIT = 1024` — единая
      константа cap'а excerpt'ов;
    - `BINARY_DEFAULT_TIMEOUT_SECONDS = 300` — единый
      default timeout subprocess invocation;
    - `UnknownPlaceholderError` /
      `PlaceholderProxy` — внутренняя механика
      placeholder substitution (раньше жила в
      `tools.py` под underscore-prefix именами);
    - `excerpt(text)` — единый excerpt cap helper;
    - `render_command_template(template, *,
      substitutions, allowed_placeholders,
      template_field_name)` — generic placeholder
      substitution engine. **Whitelist остаётся
      per-tool**: каждый tool передаёт свой
      `allowed_placeholders` set + свой
      `template_field_name` для error message;
    - `stub_honest_mode_fields()` — возвращает unified
      dict шести honest-mode полей для stub-branch'а
      (`mode='stub'`, `binary_invoked=False`,
      остальные четыре `None`);
    - `binary_backed_render_failure_fields()` — для
      случая render-fail до spawn'а
      (`binary_invoked=False`, `command_preview=None`);
    - `binary_backed_start_failure_fields(command)` —
      для случая `PlatformError` от runner'а
      (`binary_invoked=False`, но `command_preview`
      есть);
    - `binary_backed_payload_fields(command,
      process_result)` — для случая, когда subprocess
      реально отработал (`binary_invoked=True`,
      все шесть полей populated, плюс ещё
      `completed` 7-м полем для shape verify check);
    - `is_binary_subprocess_successful(payload)` —
      единый shape verify helper
      (`completed && exit_code == 0`);
    - `honest_mode_keys() -> tuple[str, ...]` —
      utility для тестов / документации.
  - **Refactor `tools.py`:**
    - Удалены три duplicated константы
      `_DUMPCFG_OUTPUT_EXCERPT_LIMIT` /
      `_APPLYCFG_OUTPUT_EXCERPT_LIMIT` /
      `_UPDATEDB_OUTPUT_EXCERPT_LIMIT` (все три =
      1024) — теперь единый
      `BINARY_OUTPUT_EXCERPT_LIMIT` в
      `binary_dispatch`.
    - Удалены три duplicated константы
      `_DUMPCFG_DEFAULT_TIMEOUT_SECONDS` /
      `_APPLYCFG_DEFAULT_TIMEOUT_SECONDS` /
      `_UPDATEDB_DEFAULT_TIMEOUT_SECONDS` (все три =
      300) — теперь единый
      `BINARY_DEFAULT_TIMEOUT_SECONDS` в
      `binary_dispatch`.
    - Удалены `_PlaceholderProxy`,
      `_UnknownPlaceholderError`, `_excerpt` из
      `tools.py` — переехали в `binary_dispatch`.
    - Три `_render_*_command` стали тонкими
      tool-specific wrapper'ами вокруг shared
      `render_command_template`. Каждый передаёт свой
      substitutions dict + свой whitelist + свой
      template field name. **Whitelistы остаются
      per-tool** (намеренно, не объединены в superset):
      6 имён у dumpcfg, 6 имён у applycfg, 5 имён у
      updatedb (tighter — без `output_path` /
      `source_dump_path`).
    - Stub-branch payloads трёх tool'ов теперь
      spread'ят `**stub_honest_mode_fields()` вместо
      inline-копии шести `None` / `False`.
    - Binary-backed-branch payloads трёх tool'ов
      теперь spread'ят
      `**binary_backed_payload_fields(command,
      process_result)` вместо inline-копии семи
      полей.
    - Render-failure payloads (`apply` /
      `update_database_configuration` диспетчеры,
      `create_dump_snapshot` binary-backed branch)
      используют `**binary_backed_render_failure_fields()`.
    - Start-failure payload (`create_dump_snapshot`
      `PlatformError` ветка) использует
      `**binary_backed_start_failure_fields(command)`.
    - Verify callable'ы apply / updatedb используют
      общий `is_binary_subprocess_successful(...)`
      predicate.
  - **Закрытие payload-discipline gap у
    `create_dump_snapshot`.** До Step 4 dump-snapshot
    stub branch (success path, render-fail path,
    PlatformError-fail path, dump-meta-fail path,
    mkdir-fail path) и binary-backed branch
    (render-fail path, mkdir-fail path,
    internal-defensive-check path) **не несли** всех
    шести honest-mode полей: некоторые ветки имели
    только `mode` + `binary_invoked` + tool-specific
    extras, без `exit_code` / `command_preview` /
    `stdout_excerpt` / `stderr_excerpt`. Step 4
    закрыл этот gap — теперь **каждая** ветка
    **каждого** из трёх binary-backed write-tool'ов
    несёт все шесть полей честно (`None` / `False` где
    не применимо, populated в binary-backed success).
- **Что НЕ тронуто.**
  - **Operator-facing surface:** argv grammar,
    placeholder whitelistы (per-tool), ToolResult
    shape, public tool names, registry counts,
    behaviour Step 2 (apply) и Step 3 (updatedb) —
    всё без изменений.
  - **Legacy stub helpers:** `runtime/dump_ops.py`
    (для apply) не тронут — Track A / Step 2 обёртывал
    его, Step 4 не вмешивается. Stub-логика для
    update-db (inline в `tools.py`) и stub-логика для
    `create_dump_snapshot` в принципе сохранили свои
    side-effect'ы (legacy markers / meta files); Step 4
    только нормализовал payload shape вокруг них.
  - **Whitelist placeholders НЕ объединены в superset.**
    Каждый tool сохранил свой собственный whitelist —
    это намеренное анти-расползание surface'а.
  - **`packages/onec-config/` не тронут.** Step 4 —
    refactor внутри write-server, новых config
    surface'ов не добавляет.
  - **Никакого generic helper framework "для всех
    будущих binary-backed write-tools".** Module
    `binary_dispatch` обслуживает ровно три текущих
    binary-backed-tool'а; расширять его surface впрок
    — не задача Step 4.
  - **Никаких новых MCP tool'ов** (registries
    `read=15 / write=25 / intelligence=16` строго
    сохранены).
  - Никаких изменений в `mcp-read-server`,
    `mcp-intelligence-server`, `apps/platform/`,
    `onec-policy-engine`, `onec-audit`,
    `onec-health`, `onec-process-runner`,
    `onec-troubleshooting`, `mcp-common`,
    `selfcheck.py`, `bootstrap_paths.ps1`,
    `pyproject.toml`, `.github/`, `.claude.json`.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase-tracka-step4-check.py`
  прогоняет 10 сценариев на synthetic tempdir + local
  HTTPServer. Все десять зелёные:
  - **A** — registry invariants `read=15 / write=25 /
    intelligence=16` без drift'а; полный whitelist 25
    имён сравнён set'ом — никаких новых tool names
    или missing names.
  - **J** — sanity check shared module: `honest_mode_keys()`
    возвращает ровно шесть имён brief'а;
    `BINARY_DEFAULT_TIMEOUT_SECONDS == 300`;
    `BINARY_OUTPUT_EXCERPT_LIMIT == 1024`.
  - **B** — `create_dump_snapshot` stub branch без
    binary contract'а: `ok=True, mode='stub',
    binary_invoked=False`; legacy
    `dump-created.txt` + `dump-meta.json` markers
    создаются; **все шесть honest-mode полей
    присутствуют** — это gap, закрытый Step 4.
  - **C** — `create_dump_snapshot` binary-backed
    happy path: `ok=True, mode='binary-backed',
    binary_invoked=True, exit_code=0`;
    operator-declared marker physically на диске.
  - **D** — `create_dump_snapshot` binary-backed
    runtime failure (template exits 7): `ok=False,
    mode='binary-backed', binary_invoked=True,
    exit_code=7`; никакого silent fallback'а.
  - **E** — `apply_config_from_files` regression
    через refactor: 4 sub-сценария (E1 stub / E2
    happy binary / E3 binary fail / E4 unknown
    placeholder) — все ведут себя как и до Step 4.
  - **F** — `update_database_configuration`
    regression через refactor: 4 sub-сценария
    (F1 stub / F2 happy binary / F3 binary fail /
    F4 tighter whitelist — `{output_path}` +
    `{source_dump_path}` отвергаются для updatedb,
    подтверждает что whitelist'ы остались per-tool).
  - **G** — payload shape parity: для всех трёх
    public tools во всех трёх ветках (stub success,
    binary-backed success, binary-backed fail)
    payload содержит **все шесть** unified
    honest-mode keys.
  - **H** — integration через `run_write_flow`: один
    mutating call для каждого из трёх tool'ов;
    standard flow shape (stage='completed',
    operation_id, audit_path, snapshot refs) для
    apply / updatedb (которые идут через
    run_write_flow); audit row пишется с правильным
    tool_name; binary-backed branch реально
    отрабатывает (verified через
    operation_payload.mode + operator-declared marker
    на диске).
  - **I** — render-time rejection short-circuit для
    apply и updatedb: unknown placeholder →
    `ok=False` **до** subprocess'а;
    `binary_invoked=False`; `command_preview=None`;
    `_snapshots/` директория не создаётся.
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным после Step 4. Вывод последнего
  прогона: `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 25 имён без изменений
  (никакого drift'а surface'а),
  `intelligence_server_tools` — 16 имён без
  изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`,
  `bootstrap_paths.ps1`, `pyproject.toml`,
  `.github/` не тронуты.
- **Что осталось до закрытия Track A.** Три шага
  (Step 5–7):
  - Step 5 — product-layer integration через
    существующие boundary'и без правок их логики
    (критерий 3 трека);
  - Step 6 — reference stand multi-step round-trip с
    настоящим 1cv8 binary'ом (критерий 2 трека);
  - Step 7 — final integration pass + закрытие трека
    (критерии 6, 7, 8, 9, 10).
- **Следующий шаг.** **Parallel Track A / Step 5 —
  product-layer integration over real write path** —
  закрыт (см. ниже).

### Parallel Track A / Step 5 — product-layer integration over real write path (завершён)

- **Цель шага.** Закрыть Q7 и Q8 открытых вопросов
  Step 1 плана трека: привести surface двух
  product-layer boundary'ев (`run_real_stand_smoke_test`
  и `inspect_enterprise_foundation`) к honest состоянию
  после того, как Track A / Steps 2–4 уже дали real
  binary-backed write contract всем трём binary-backed
  write-tool'ам в `mcp-write-server`. Само Track A
  Steps 2–4 жили внутри write-server'а; Step 5 — это
  **surface-only** product-layer update, не кодовый
  back-port внутрь write-server'а и не новый
  MCP-tool slice.
- **Что реально появилось в коде.**
  - **`apps/platform/src/onec_platform/enterprise.py`
    (Q8 closure).** В `_check_real_stand_contract`
    раньше score жил в диапазоне 0..2 и проверял только
    `onec_binary_path` + `onec_dumpcfg_command_template`.
    Теперь функция симметрично проверяет все три
    command template'а (dumpcfg / applycfg / updatedb)
    рядом с binary path; score range расширен до 0..4.
    На prod-like config'ах отсутствие любого из трёх
    template'ов превращается в **error** finding
    с code'ами `foundation_onec_applycfg_template_missing_on_prod`
    / `foundation_onec_updatedb_template_missing_on_prod`
    (симметрично уже существовавшему
    `foundation_onec_dumpcfg_template_missing_on_prod`)
    и соответствующим recommended-action'ом, перечисляющим
    placeholder whitelist per-tool. На non-prod —
    presumed warning'и `foundation_onec_<op>_template_missing`
    (без error'ов и без блокировки `ok=True`). При
    полном contract'е (binary + 3 template'а) появляется
    presumed-finding `foundation_real_write_path_contract_complete`;
    при только `binary + dumpcfg` сабсете — старое
    `foundation_real_stand_smoke_contract_available`
    остаётся как валидный fallback advisory (now in an
    `elif` branch). `_SECTION_MAX_SCORE['binary']`
    поднят с 2 до 4. Логика
    `_classify_foundation_level` без изменений —
    `'strong'` автоматически требует full contract
    в section D, потому что `max_total = sum(...)`
    учитывает обновлённый максимум. Docstring
    `inspect_enterprise_foundation` дополнен
    параграфом про Track A integration.
  - **`apps/platform/src/onec_platform/realstand.py`
    (Q7 closure).** В `_build_plan_summary` удалена
    stale advisory строка «Phase 2 stubs … are NOT
    rewritten on this step — that is a parallel
    track». Вместо неё — три новых блока: (1) три
    binary-backed write-tool'а названы по имени
    (`create_dump_snapshot`, `apply_config_from_files`,
    `update_database_configuration`) с явным
    указанием honest dual-mode контракта через unified
    internal `binary_dispatch` helper после Track A /
    Steps 2–4; (2) явное напоминание оператору, что
    smoke сам по себе остаётся **bounded probe** и
    **не** chain'ит dump → apply → updatedb на
    реальном binary'е (multi-step round-trip — это
    Track A / Step 6, не данный surface); (3)
    подтверждение, что infobase не мутируется и
    никакие MCP write-tool'ы из smoke не вызываются.
    Module-docstring `realstand.py` обновлён
    симметрично: «не переписывает Phase 2 stub'ы»
    заменено на честное описание Track A history +
    bounded-probe boundary. В package-docstring'е
    `apps/platform/src/onec_platform/__init__.py`
    Step 7-блок тоже обновлён: убрана фраза «no
    Phase 2 stub … is rewritten — flipping those
    onto a binary-backed branch is a parallel
    track»; вместо неё — Track A-aware
    формулировка.
- **Что НЕ тронуто.**
  - **Никаких изменений** в `apps/mcp-write-server/`
    (binary-backed dispatch уже был там после
    Step 2–4 трека), в `apps/mcp-read-server/`,
    `apps/mcp-intelligence-server/`,
    `packages/onec-policy-engine/`,
    `packages/onec-config/` (full contract уже
    был добавлен в EnvironmentConfig после Track A
    Steps 2–3 — Step 5 только начал **использовать**
    его в product surface'е), `packages/onec-audit/`,
    `packages/onec-health/`, `packages/onec-process-runner/`,
    `packages/onec-troubleshooting/`,
    `packages/mcp-common/`, `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`,
    `.github/`, `.claude.json`.
  - **Никаких новых product-layer boundary'ев.**
    Все правки — внутри двух уже существующих
    функций (`run_real_stand_smoke_test`,
    `inspect_enterprise_foundation`).
  - **`RealStandSmokeResult` и `EnterpriseFoundationResult`
    shape'ы** — без изменений (те же dataclass-поля,
    те же `_from_json_file` варианты). Добавились
    только новые finding-code'ы на готовых списках
    `confirmed_findings` / `presumed_findings` и
    новые recommended-action'ы.
  - **Operator-facing argv grammar / placeholder
    whitelist'ы per-tool / public ToolResult
    shape** — без изменений.
  - **Никаких новых MCP tool'ов** (registries
    `read=15 / write=25 / intelligence=16` строго
    сохранены).
  - **Никакого back-door write channel'а** из
    продуктового слоя: Step 5 ничего не пишет на
    диск, не зовёт `run_write_flow`, не открывает
    subprocess'ы — это **surface-only** update.
  - **`onec_policy_engine` не импортируется** ни
    из `apps/platform/src`, ни из
    `apps/mcp-intelligence-server/src` (отдельно
    проверено сканированием в manual-check
    сценарии G).
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase-tracka-step5-check.py`
  прогоняет 7 сценариев (с раскрытием C на четыре
  под-кейса). Все зелёные:
  - **A** — registry invariants `read=15 / write=25 /
    intelligence=16` без drift'а; полный whitelist 25
    write-имён сравнён set'ом — никаких новых tool
    names или missing names.
  - **B** — backward compatibility: Step 1–4
    product-config (без apply/updatedb template'ов)
    загружается через `inspect_enterprise_foundation`
    с `ok=True`; missing apply/updatedb template'ы
    surface'ятся как presumed warnings
    (`foundation_onec_applycfg_template_missing` /
    `foundation_onec_updatedb_template_missing`); ни
    один из новых `*_missing_on_prod` error code'ов
    не fire'ится.
  - **C1** — enterprise section absent →
    `foundation_level='absent'`,
    `ready_for_enterprise_track=False`.
  - **C2** — только dumpcfg на prod-like → applycfg
    и updatedb missing-on-prod errors,
    `binary=2/4`, `foundation_level != 'strong'`,
    recommended_actions содержат строки про оба
    отсутствующих template'а.
  - **C3** — dumpcfg + applycfg, без updatedb на
    prod-like → updatedb missing-on-prod error
    fire'ится, applycfg missing-on-prod НЕ fire'ится,
    `binary=3/4`, `foundation_level != 'strong'`;
    presumed `foundation_real_write_path_contract_complete`
    ещё не выставлено.
  - **C4** — full contract на prod-like + чистые
    остальные секции (identity / operability /
    traceability) → `binary=4/4`, presumed
    `foundation_real_write_path_contract_complete`
    fire'ится; `foundation_real_stand_smoke_contract_available`
    НЕ fire'ится (это else-branch);
    `foundation_level='strong'`,
    `ready_for_enterprise_track=True`, ноль
    error finding'ов.
  - **D** — real-stand smoke advisory: plan_summary
    упоминает все три binary-backed tool'а
    (`create_dump_snapshot` / `apply_config_from_files`
    / `update_database_configuration`), Track A /
    Steps 2–4, dual-mode contract, bounded probe
    semantics, multi-step round-trip принадлежит
    Track A / Step 6; запрещённые устаревшие фразы
    («Phase 2 stubs», «are NOT rewritten», fake
    chain claims) отсутствуют.
  - **E** — broken JSON paths: оба
    `*_from_json_file` boundary'я возвращают
    `ok=False` без exception'ов — и на
    несуществующем path'е (foundation_rejected /
    mode='rejected'), и на синтаксически битом JSON'е.
  - **F** — suggested-tools discipline: имена в
    `EnterpriseFoundationResult.suggested_tools` /
    `suggested_write_tools` и
    `RealStandSmokeResult.suggested_tools` /
    `suggested_write_tools` все принадлежат union'у
    live registries +
    `_KNOWN_PLATFORM_FUNCTIONS`; made-up имя
    отвергается `_allow_only_real_tools`.
  - **G** — нулевой импорт `onec_policy_engine`
    под `apps/platform/src/` и
    `apps/mcp-intelligence-server/src/`
    (сканирование 26 `.py`-файлов, 0 offender'ов).
- **dev-check.** `scripts/dev/selfcheck.py`
  остаётся зелёным после Step 5 (`imports_ok = true`,
  `read_server_tools` 15 имён без изменений,
  `write_server_tools` 25 имён без изменений,
  `intelligence_server_tools` 16 имён без
  изменений, `selfcheck_status = ok`).
- **Что осталось до закрытия Track A.** Два шага
  (Step 6–7):
  - Step 6 — reference stand multi-step round-trip
    с настоящим 1cv8 binary'ом (real DumpCfg →
    real apply (LoadCfg) → real UpdateDBCfg на
    reference stand'е, фиксируется как
    воспроизводимый runbook; критерий 2 трека);
  - Step 7 — final integration pass + закрытие
    трека (критерии 6, 7, 8, 9, 10).
- **Следующий шаг.** **Parallel Track A / Step 6 —
  reference stand multi-step round-trip** — открыт
  частично (см. ниже). Не закрыт.

### Parallel Track A / Step 6 — reference stand multi-step round-trip (закрыт honestly)

- **Цель шага.** Подтвердить на **реальном** 1cv8 binary
  и **реальной** инфобазе связный сценарий
  `create_dump_snapshot` → `apply_config_from_files` →
  `update_database_configuration`, где все три tool'а
  идут по binary-backed branch'у с
  `mode='binary-backed'`, `binary_invoked=True`,
  `exit_code=0`, без silent fallback'а на stub. Это
  **operator-driven exercise** на reference stand'е;
  Step 6 **не** добавляет MCP tool'ов, **не**
  расширяет registries, **не** требует production-
  правок (dual-mode contract уже введён Steps 2–4,
  product-layer surface уже обновлён Step 5).
- **Что реально появилось.**
  - **Один новый runbook:**
    `docs/runbooks/track-a-reference-stand-round-trip.md`
    — operator-reproducible инструкция: цель, prereq'ы
    (real binary, real infobase, DESIGNER credentials,
    source dump, опциональный gateway), reference
    stand assumptions, точная последовательность
    шагов A.1–A.6 через public write-server tools
    (`mcp_write_server.tools.create_dump_snapshot`
    → `apply_config_from_files` →
    `update_database_configuration`) с примерами
    operator-declared template'ов
    (`/F`, `/N`, `/P`, `/DumpCfg`,
    `/LoadConfigFromFiles`, `/UpdateDBCfg`,
    `/DisableStartupMessages`), критерии «реально
    пошло binary-backed» (`mode`, `binary_invoked`,
    `exit_code`, `command_preview`), пять типовых
    failure cases (missing binary contract / unknown
    placeholder / non-zero exit / stand unavailable /
    silent stub fallback), список ожидаемых
    артефактов (`_snapshots/<id>/Configuration.xml`,
    `audit.jsonl` с тремя `operation_id`-ами,
    шесть unified honest-mode полей в каждом payload),
    что доказывает / не доказывает успешный
    round-trip.
  - **Один новый manual-verification скрипт:**
    `C:/Users/user/AppData/Local/Temp/phase-tracka-step6-prereq-inventory.py`
    — operator-runnable prereq inventory. Шесть
    блоков проверок (P1 registry invariants,
    P2 1cv8 binary discovery, P3 render-pipeline для
    всех трёх template'ов, P4 placeholder whitelist
    enforcement negative, P5 reference stand
    artifacts, P6 discipline asserts).
    Скрипт **не** запускает 1cv8.exe, **не**
    создаёт subprocess'ов — это honest static
    inventory. Exit codes: `0` все prereq'ы готовы,
    `1` partial (binary OK, stand prereq'ы missing),
    `2` discipline broken.
  - **Никаких production-правок.** Полный список
    untouched зон: `apps/mcp-read-server/`,
    `apps/mcp-write-server/`, `apps/mcp-intelligence-server/`,
    `apps/platform/`, `packages/mcp-common/`,
    `packages/onec-process-runner/`,
    `packages/onec-policy-engine/`,
    `packages/onec-audit/`, `packages/onec-health/`,
    `packages/onec-troubleshooting/`,
    `packages/onec-config/`, `scripts/`,
    `selfcheck.py`, `bootstrap_paths.ps1`,
    `pyproject.toml`, `.github/`, `.claude.json`.
- **Результат прогона prereq-inventory в текущем
  dev-окружении.**
  - **P1 — registry invariants: PASS.** read=15,
    write=25, intelligence=16 без drift'а после
    Step 6.
  - **P2 — 1cv8 binary discovery: PASS.** Найдены два
    реальных DESIGNER-capable binary'я:
    - `C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe`
      (1.8 MB, file=True, executable_like=True)
    - `C:/Program Files (x86)/1cv8/8.3.27.1936/bin/1cv8.exe`
      (1.5 MB, file=True, executable_like=True)
  - **P3 — render-pipeline: PASS.** Все три
    template'а (dumpcfg / applycfg / updatedb) с
    реальным binary path'ом и synthetic placeholder
    values корректно рендерятся через
    `runtime/binary_dispatch.render_command_template`
    в 11-аргументный subprocess argv (без `subprocess`,
    без shell). Это unit-style проверка render-
    pipeline'а, не реальный invocation 1cv8.
  - **P4 — placeholder whitelist enforcement: PASS.**
    Unknown placeholder отвергается `ValueError`-ом
    **до** старта subprocess'а во всех трёх tool'ах
    (с `binary_invoked=False`,
    `command_preview=None`). Tighter whitelist у
    updatedb честно отвергает `{output_path}` и
    `{input_path}` (которые валидны для dumpcfg /
    applycfg).
  - **P5 — reference stand artifacts: MISSING (×4).**
    - `P5.a` MISSING: ноль declared product-config'ов
      с full real-write contract'ом в `examples/`
      или в корне репо (grep по `onec_binary_path` +
      три template'а). Оператор должен
      материализовать config по runbook'у.
    - `P5.b` MISSING: `examples/demo-infobase/`
      пуст — нет реальной целевой инфобазы для
      `base_path`.
    - `P5.c` MISSING: `examples/demo-dumps/`
      пуст — нет source dump tree для apply шага.
    - `P5.d` MISSING:
      `ONEC_DESIGNER_USER` / `ONEC_DESIGNER_PASSWORD`
      env vars не выставлены — DESIGNER credentials
      out-of-band.
  - **P6 — discipline asserts: PASS.** Ноль реальных
    импортов `onec_policy_engine` под
    `apps/platform/src/` и
    `apps/mcp-intelligence-server/src/`.
  - **Verdict prereq-inventory'я в исходном dev-окружении
    был partial (real 1cv8 binary present + render-pipeline
    OK, но stand prereq'ы missing).** Это была честная
    остановка по контракту шага. Позже, когда оператор
    подготовил InfoBase6 + DESIGNER credentials через
    local-only writable config (`%TEMP%/infobase6-writable.config.json`,
    cleartext, never committed), real multi-step round-trip
    был выполнен и Step 6 закрыт honestly — см. блок
    «Step 6 closure on InfoBase6» ниже.
- **Step 6 closure on InfoBase6.**
  - Operator-driven round-trip A.1–A.6 прошёл на real
    1cv8 binary'е (8.3.27.1859) и real file-based
    инфобазе `C:/Users/user/Documents/InfoBase6` через
    local-only writable config с DESIGNER credentials
    out-of-band (cleartext в `%TEMP%`, никогда не
    коммитится).
  - **A.2** `create_dump_snapshot` через
    `/DumpConfigToFiles`: `mode='binary-backed'`,
    `binary_invoked=True`, `exit_code=0`, snapshot tree
    физически на диске под
    `examples/demo-dumps/_snapshots/dump-infobase6-file-step6-A2-...`.
  - **A.4** `apply_config_from_files` через
    `/LoadConfigFromFiles`: `stage='completed'`,
    `mode='binary-backed'`, `exit_code=0`, mutating
    audit row написан с `details.dump_snapshot_path=...`
    указывающим на pre-apply snapshot, созданный
    `run_write_flow`'ом.
  - **A.5** `update_database_configuration` через
    `/UpdateDBCfg`: `stage='completed'`,
    `mode='binary-backed'`, `exit_code=0`, mutating
    audit row написан с `details.dump_snapshot_path=...`
    указывающим на pre-updatedb snapshot.
  - Audit honest по факту: `examples/demo-dumps/infobase6/.audit/audit.jsonl`
    содержит **ровно 2** append-only row'и (для A.4 и
    A.5), не три. Standalone `create_dump_snapshot`
    audit row не пишет by design — он не идёт через
    `run_write_flow`; pre-mutating dump подтверждается
    через `details.dump_snapshot_path` mutating row'и.
    Это намеренная архитектура `runtime/flow.py`
    (snapshot stage запускает internal
    `create_dump_snapshot` без отдельного audit-write,
    success_details mutating row'и захватывает
    `dump_snapshot_path`).
  - **Doc/expectation cleanup без code change.**
    Runbook
    `docs/runbooks/track-a-reference-stand-round-trip.md`
    обновлён в трёх местах: A.2 артефакты, A.6
    post-check item 4, раздел «Ожидаемый минимум
    артефактов» — все три места теперь говорят про
    «две audit row для двух mutating операций +
    `details.dump_snapshot_path`», не про «три audit
    row». Local-only закрытие logic в
    `%TEMP%/infobase6-step6-chain.py` (post-check
    блок A.6) переписан под honest expectation:
    `required = {"apply_config_from_files",
    "update_database_configuration"}` плюс проверка
    `details.dump_snapshot_path` в каждой mutating
    row'е.
  - **Production-кода Step 6 не правил.** `apps/`,
    `packages/`, registries, `examples/demo-infobase/infobase6.config.json`
    (repo candidate config без credentials),
    selfcheck — без изменений. Все правки локализованы
    в repo runbook'е + local-only chain script'е.
- **Что НЕ сделано (намеренно).**
  - **Не запускался synthetic round-trip через
    `sys.executable`.** Step 4 manual-check уже
    подтвердил binary-backed branch на synthetic
    binary'е (`sys.executable` плюс fake marker
    script); Step 6 **должен** быть real или
    partial, third option'а нет.
  - **Не запускался реальный 1cv8.exe** даже с
    headless probe argv'ом. На пустой пробе
    (`/?`) 1cv8.exe открывает GUI dialog (это
    воспроизведено и убито вручную); запуск без
    осмысленной операции по reference stand'у
    был бы тратой ресурсов и потенциально GUI-
    blocker'ом.
  - **Не сгенерирована демо-инфобаза.** Это
    operator-task: invocation `/CreateInfobase`
    запросов и flag'ов выходит за honest рамки
    Step 6 (платформа binary-CLI семантику не
    угадывает, см. Step 7 README); кроме того,
    development-окружение ограничено `\sandbox`-
    профилем без elevated privileges на
    1cv8 install dir.
  - **Не тронут `apps/mcp-write-server/README.md`.**
    Step 6 не меняет write-server surface; ничего
    нового write-server'у сообщить.
- **dev-check.** `scripts/dev/selfcheck.py`
  остаётся зелёным после Step 6 (никакой
  production-код не правился).
  `imports_ok = true`, `read_server_tools` 15 имён,
  `write_server_tools` 25 имён, `intelligence_server_tools`
  16 имён, `selfcheck_status = ok`.
- **Что осталось до закрытия Track A.** Только
  Step 7 — final integration pass + закрытие трека
  (документационный pass).
- **Следующий шаг.** **Parallel Track A / Step 7 —
  final integration pass and Track A closure** —
  открыт сразу после honest closure'а Step 6, не
  потребовал новых binary runs.

### Parallel Track A / Step 7 — final integration pass and Track A closure (закрыт)

- **Цель шага.** Зафиксировать closure всего
  Parallel Track A после того, как Step 6 уже
  отработал honestly на real 1cv8 + real
  InfoBase6: подтвердить, что Track A acceptance
  criteria 1–10 закрыты existing evidence'ом, и
  обновить README/PROJECT-STATUS под closed status.
  По step-map'у это закрывающий, по сути
  documentation-only шаг (по аналогии с
  Phase 5 / Step 8 и Phase 6 / Step 9 final
  integration pass'ами).
- **Никаких новых binary-backed запусков.** Step 7
  целенаправленно **не** перезапускал A.2 / A.4 /
  A.5 — это было бы расточительным повторным
  использованием ресурсов и противоречило бы
  принципу «closure на already proven evidence»;
  все необходимые артефакты от Step 6 уже на диске:
  - `examples/demo-dumps/_snapshots/` — 7 dump
    snapshot директорий (A.2 + A.2 retries +
    A.4 pre-apply + A.5 pre-updatedb);
  - `C:/Users/user/Documents/_snapshots/` —
    2 backup snapshot'а (pre-apply + pre-updatedb);
  - `examples/demo-dumps/infobase6/.audit/audit.jsonl`
    — две append-only mutating audit row'и (A.4 +
    A.5), обе со `status='ok'` и populated
    `details.dump_snapshot_path`.
- **Closure-check на existing evidence.** Read-only
  прогон против уже существующего `audit.jsonl`
  (без вызовов `create_dump_snapshot` /
  `apply_config_from_files` /
  `update_database_configuration`) подтвердил все
  acceptance criteria:
  - **AC 1** (full real binary-backed contract для
    всех трёх write-tool'ов) — закрыт production
    code'ом Steps 2–4: dual-mode dispatcher в
    `tools.py`, unified `binary_dispatch` helper,
    per-tool placeholder whitelists.
  - **AC 2** (multi-step real round-trip на
    reference stand) — закрыт Step 6 evidence'ом
    на InfoBase6.
  - **AC 3** (product-layer integration over real
    write path) — закрыт Step 5 surface'ом и
    подтверждён Step 6 round-trip'ом (A.4 / A.5
    шли через `run_write_flow` со всеми его
    стадиями preflight + snapshot + operation +
    verify + audit).
  - **AC 4** (no silent fallback) — закрыт Steps
    2–4 кодом; в `tools.py` нет ветки fallback'а
    из binary-backed на stub при non-zero exit.
  - **AC 5** (honest payload discipline) — закрыт
    Step 4; evidence Step 6: все шесть unified
    honest-mode полей populated в каждой из трёх
    Step 6 операций.
  - **AC 6** (registries без drift'а) — verified:
    `read_server_tools = 15`,
    `write_server_tools = 25`,
    `intelligence_server_tools = 16`,
    `imports_ok = true`, `selfcheck_status = ok`.
  - **AC 7** (`onec_policy_engine` не импортируется
    в product/intelligence) — invariant сохранён
    (Phase 6 / Step 9 уже его подтвердил, Track A
    кода не правил под `apps/platform/src` и
    `apps/mcp-intelligence-server/src`).
  - **AC 8** (no back-door write channel в product
    layer) — by construction: Step 6 round-trip
    шёл через public write-server tools, A.4 /
    A.5 — через `run_write_flow`.
  - **AC 9** (operator-facing messages честные) —
    runbook + local chain expectation выровнены
    Step 6'ом под фактическое поведение audit
    канала.
  - **AC 10** (Track A closed как documented
    status) — закрывается этим Step'ом
    (README + PROJECT-STATUS обновлены).
- **Какие repo-файлы Step 7 правил.**
  - `README.md` — раздел «Active parallel track»
    переименован в «Closed parallel track»; Step 6
    и Step 7 отмечены как closed; добавлен явный
    блок «Что Track A реально закрыл» и «Что
    Track A не делает индустриальным продуктом
    после closure» (honest constraints).
  - `PROJECT-STATUS.md` — header (Текущий шаг +
    Статус) обновлён под closed; Step 6 секция
    дополнена блоком «Step 6 closure on InfoBase6»
    с фактическими evidence; добавлена эта Step 7
    секция.
- **Что Step 7 НЕ правил.**
  - **Никаких production-правок.** `apps/mcp-write-server/`,
    `apps/mcp-read-server/`, `apps/mcp-intelligence-server/`,
    `apps/platform/`, `packages/mcp-common/`,
    `packages/onec-process-runner/`,
    `packages/onec-policy-engine/`,
    `packages/onec-audit/`, `packages/onec-health/`,
    `packages/onec-troubleshooting/`,
    `packages/onec-config/`, `scripts/`,
    `selfcheck.py`, `bootstrap_paths.ps1`,
    `pyproject.toml`, `.github/`, `.claude.json`
    — без изменений.
  - **Никаких registry изменений.** read=15 /
    write=25 / intelligence=16 без drift'а.
  - **Никаких новых runbook'ов.** Step 6 уже
    ship'нул один operator-reproducible runbook;
    Step 7 ничего нового не добавляет — он только
    финализирует closure-status трека.
  - **`docs/architecture/track-a-real-write-path-plan.md`
    и `track-a-real-write-path-step-map.md` не
    тронуты** — они уже описывают Track A
    корректно; closure-статус по контракту проекта
    живёт в README + PROJECT-STATUS, не в
    plan/step-map.
  - **Никаких новых запусков 1cv8.exe.** Existing
    Step 6 evidence полностью покрывает acceptance
    criteria 1–5; повторный round-trip был бы
    избыточным.
  - **`docs/operator-manual.md` /
    `docs/administrator-manual.md` /
    `docs/developer-manual.md` /
    `docs/runbooks.md` /
    `apps/*/README.md`** — не тронуты. Write-server
    behaviour не изменился ни на единый байт после
    Step 6; эти документы уже честны после
    Steps 2–5.
- **Что Track A реально закрыл (final summary).**
  - **Real binary-backed dump/apply/updatedb path**:
    все три ранее stub-backed write-tool'а
    (`create_dump_snapshot`,
    `apply_config_from_files`,
    `update_database_configuration`) теперь имеют
    honest dual-mode contract с real binary-backed
    dispatch'ем при наличии operator-declared
    argv-template'а; production-code visible в
    `apps/mcp-write-server/src/mcp_write_server/tools.py`
    (Steps 2–4) и в shared
    `runtime/binary_dispatch.py` (Step 4).
  - **Final contract correctness**: один shared
    `binary_dispatch` helper, per-tool placeholder
    whitelists (включая tighter whitelist у
    updatedb), fail-closed на unknown placeholder
    до старта subprocess'а, fixed timeout cap
    (300 s default).
  - **No silent fallback**: при non-zero exit
    binary-backed branch'а возвращается honest
    `ok=False` с populated `mode='binary-backed'` /
    `binary_invoked=True` / `exit_code != 0`, без
    тихого downgrade'а на stub. Fallback — только
    config-time, при отсутствии binary contract'а.
  - **Honest payload discipline**: каждая ветка
    каждого из трёх tool'ов несёт все шесть
    unified honest-mode полей (`mode`,
    `binary_invoked`, `exit_code`,
    `command_preview`, `stdout_excerpt`,
    `stderr_excerpt`).
  - **Reference-stand execution layer proven**:
    real multi-step round-trip отработал на
    InfoBase6 (real file-based 1С база), audit
    honest, snapshot trees физически на диске,
    runbook + closure logic выровнены под
    фактическое поведение `run_write_flow`'а.
- **Что Track A НЕ делает «готовым индустриальным
  продуктом» после closure (honest constraints).**
  - **Operator credentials остаются out-of-band** —
    DESIGNER user/password не в product config;
    в Step 6 closure они хранились в local-only
    `%TEMP%/infobase6-writable.config.json`
    (cleartext, никогда не коммитится). Production-
    grade secrets management — out of Track A.
  - **Multi-version matrix не пройдена** — Step 6
    закрылся на single-version smoke
    (8.3.27.1859); другие версии 1С в матрицу
    не входили.
  - **Production runbook ecosystem не построен** —
    Track A ship'нул один reference-stand runbook;
    полная operator runbook collection — отдельный
    track.
  - **Packaging / installer / signed distribution
    / GUI wizard / `.msi` / `.deb`** — не сделано
    (это Phase 6 / parallel track).
  - **Полный enterprise super-set** (SSO/RBAC,
    multi-tenant, secrets vault как сервис,
    federated audit, policy-as-code DSL,
    multi-instance HA) — не открывался.
  - **Web-UI / dashboard frontend** — не сделан.
  - **Полная rollback/delete-вселенная** — whitelist
    остаётся на двух tool'ах
    (`add_catalog_attribute`,
    `add_document_attribute`), как Phase 6 / Step 4
    его и оставил.
  - **Полный AST-парсер XML/BSL** — не написан;
    XML edits идут через `xml.etree.ElementTree`
    DOM-стиль, BSL — substring/regex MVP-патчинг.
  - **Production-grade MCP transport / `__main__` /
    CLI у трёх MCP-серверов** — не сделано.
  - **Hot reload без рестарта процесса**, OS-level
    service supervision (Windows Service / systemd
    unit) — не сделано (Phase 6 / Step 6 ship'нул
    минимальный restart-policy contract).
  - **Полный version-matrix smoke на всех 1С
    версиях и стендах** — не пройден.

  Эти ограничения зафиксированы как **honest
  constraints**: Track A **не** претендовал на
  enterprise-ready / production-ready статус.
  Closure Track A означает буквально «full real
  1cv8-backed write path работает end-to-end на
  reference stand'е», не «продукт готов к prod».
- **Dev-check после Step 7.** Зелёный без правок:
  `imports_ok = true`,
  `read_server_tools = 15` имён,
  `write_server_tools = 25` имён,
  `intelligence_server_tools = 16` имён,
  `selfcheck_status = ok`. (Замечание:
  `health_summary_problem = gateway_down` —
  ожидаемое состояние dev-окружения без HTTP-
  публикации; Step 6 round-trip шёл с локальным
  gateway stub'ом, который сейчас не запущен.
  selfcheck'у он не нужен.)
- **Следующий шаг.** Track A полностью закрыт.
  Никаких новых треков параллельно с Track A не
  открывалось; никаких новых треков closure'ом
  Track A автоматически не открывается. Открытие
  следующего parallel track'а — отдельное решение
  оператора проекта; Phase 7 как линейная фаза
  по-прежнему не запланирована.

### Parallel Track B / Step 1 — planning Productization & Delivery Polish (завершён)

- **Цель шага.** Зафиксировать документационный вход
  в **Parallel Track B — Productization & Delivery
  Polish**: назначение трека, целевой результат, что
  закрывает трек и что НЕ закрывает, чем отличается от
  Phase 6 и Track A, guardrails, явный список «что НЕ
  входит», 10 критериев приёмки, открытые вопросы
  Step 2+. Кода не писать. Никаких изменений registry.
  Никаких новых MCP tool'ов. Никакого расширения
  product-layer surface'а.
- **Назначение трека.** После closure'а Track A
  execution layer real binary-backed write path'а
  доказан. Самый жирный незакрытый разрыв сейчас —
  **не execution layer**, а делiver-сторона:
  репозиторий не git-репозиторий (нет `.git`);
  `.gitignore` минимальный и не покрывает реалии
  проекта (snapshot trees Track A Step 6, audit-
  директории, локальные writable-конфиги); нет
  `LICENSE`, нет `CHANGELOG.md`, нет верхнеуровневого
  «5-минутного quickstart'а» в README; у трёх
  MCP-серверов нет `__main__.py`; `scripts/release/`
  пустая. Track B доводит существующий продукт до
  удобного **install / run / repo / release**
  состояния — не открывая нового execution-core
  sprint'а и не входя в enterprise super-set.
- **Что реально появилось в Step 1.**
  - **Один новый план трека:**
    `docs/architecture/track-b-productization-polish-plan.md`
    — назначение Track B, целевой результат (6
    пунктов), что Track B **не** закрывает, guardrails
    (никакого расширения MCP surface, никакого
    back-door write channel, никакого `shell=True`,
    никаких credentials в repo, не претендуем на
    enterprise-ready / production-ready статус),
    10 критериев приёмки, 7 открытых вопросов,
    раздел «связь с Phase 6 / Track A», honest
    constraints после closure.
  - **Один новый step-map:**
    `docs/architecture/track-b-productization-polish-step-map.md`
    — шесть шагов: Step 1 (planning, этот),
    Step 2 (repo hygiene + legal layer), Step 3
    (install fast path operator-discoverable),
    Step 4 (local launch ergonomics), Step 5
    (README + docs polish), Step 6 (final
    integration pass and Track B closure). Каждый
    шаг описан в едином формате (Цель / Что меняем /
    Затронутые зоны / Результат).
- **Что НЕ сделано (намеренно).**
  - **Никаких изменений production-кода.** `apps/`,
    `packages/`, `scripts/`, `pyproject.toml`,
    `.github/`, `.editorconfig`, `.python-version`,
    `.gitignore`, `examples/` — без изменений.
  - **Никаких изменений в `mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`,
    `apps/platform/`, `onec-policy-engine`,
    `onec-audit`, `onec-health`,
    `onec-process-runner`, `onec-troubleshooting`,
    `mcp-common`, `onec-config`, `selfcheck.py`,
    `bootstrap_paths.ps1`.** Track B / Step 1 это
    documentation-only.
  - **Никакой `git init`** на этом шаге. Это
    Step 2.
  - **Никакого LICENSE / CHANGELOG / SECURITY.**
    Это Step 2.
  - **Никаких новых runbook'ов / manualов.**
- **Что сказали явно в плане трека.**
  - Track B **не** закрывает: production-grade MCP
    transport (auth, multi-tenant, federated
    audit), полный installer ecosystem (`.msi` /
    `.deb` / GUI wizard / signed distribution),
    web-UI / dashboard frontend, полный enterprise
    super-set (SSO/RBAC, multi-tenant, secrets
    vault как сервис, federated audit storage,
    policy-as-code DSL, multi-instance HA), hot
    reload / OS-level service supervision,
    multi-version matrix smoke на всех 1С версиях,
    полный AST-парсер XML/BSL, полная
    rollback/delete-вселенная, новые MCP tools
    (registries `read=15 / write=25 /
    intelligence=16` остаются без drift'а),
    production code rewrite.
  - **GitHub remote push** — operator action, не
    часть трека. Track B доводит до состояния
    «репозиторий готов к выкладке»; нажатие
    `git remote add origin ...` + `git push -u
    origin main` — отдельный operator step.
- **Открытые вопросы Step 2+.** Q1 (лицензия:
  Apache-2.0 как default-предложение, окончательно
  — operator call), Q2 (`main` vs `master`), Q3
  (scope `__main__.py`'ев у MCP-серверов), Q4
  (`__main__.py` для `onec_platform`), Q5
  (`CONTRIBUTING.md` / `SECURITY.md` — нужны ли),
  Q6 (что делать с `examples/demo-dumps/_snapshots/`
  от Track A Step 6 round-trip'а), Q7 (версия
  проекта в `pyproject.toml` — оставить `0.1.0` или
  bump'нуть в `0.2.0`).
- **Selfcheck после Step 1.** Зелёный без правок:
  `imports_ok = true`,
  `read_server_tools = 15` имён,
  `write_server_tools = 25` имён,
  `intelligence_server_tools = 16` имён,
  `selfcheck_status = ok`. Track B / Step 1 не
  правил production-кода, поэтому drift'а быть не
  должно — и его нет.
- **Следующий шаг.** Parallel Track B / Step 2 —
  закрыт; см. секцию ниже.

### Parallel Track B / Step 2 — repo hygiene + legal layer (завершён)

- **Цель шага.** Превратить рабочую директорию в
  git-репозиторий, выровнять `.gitignore` под реалии
  проекта, добавить `LICENSE` / `CHANGELOG.md` /
  `SECURITY.md`, сделать первый meaningful commit.
  Resolve Q1 (license), Q2 (`main` vs `master`), Q5
  (CONTRIBUTING / SECURITY), Q6
  (`examples/demo-dumps/` artifacts), Q7
  (version в `pyproject.toml`).
- **Что сделано.**
  - `git init -b main` в корне `C:\Tools\1c-agent-platform`.
  - `.gitignore` расширен (Python / IDE / OS + 1С DB-
    файлы и locks `*.1CD` / `*.cfl` + Track A
    round-trip evidence (`examples/demo-dumps/_snapshots/`,
    `examples/demo-dumps/infobase6/`) + audit dirs
    `**/.audit/` + runtime state `.runtime/` /
    `**/.runtime/` + bootstrap work dir
    `examples/demo-infobase/_work/` + local writable /
    fixed configs `*-writable.config.json` /
    `*.config.fixed.json` / `*.config.json.bak` +
    scratch `scratch/` / `.scratch/` + editor scratch).
  - `LICENSE` (Apache-2.0, полный стандартный текст —
    header + 9 numbered TERMS + END OF TERMS AND
    CONDITIONS + APPENDIX).
  - `CHANGELOG.md` (заголовок `## 0.1.0 — initial public
    snapshot (in preparation)`; перечень что закрыто до
    0.1.0 — Phases 1–6 + Track A; registry invariant
    15/25/16; honest constraints).
  - `SECURITY.md` (private reporting flow + honest
    constraints — pre-1.0, credentials out-of-band, no
    production transport, single-version smoke, no
    installer ecosystem, limited rollback coverage —
    + safety guarantees: `run_write_flow` единственный
    mutating-путь, intelligence read-only, no
    `shell=True`, append-only audit, fail-closed
    defaults).
  - Initial meaningful commit `85a4a7e` —
    `Initial public snapshot — repo hygiene and legal
    baseline` — 126 файлов, 0 dangerous matches на
    safety scan'е.
- **Что НЕ сделано.** Production-код вообще не
  трогали. `apps/`, `packages/`, `scripts/dev/`,
  `pyproject.toml`, `.github/`, `examples/`, `docs/`
  — без изменений. Registries `read=15 / write=25 /
  intelligence=16` без drift'а. Никакого remote
  push'а.

### Parallel Track B / Step 3 — install fast path operator-discoverable (завершён)

- **Цель шага.** Сделать существующий
  `onec_platform.run_install_fast_path_from_json_file`
  operator-discoverable через тонкий PowerShell
  wrapper в каноническом `scripts/release/`, без
  правки production-installer-core.
- **Что сделано.**
  - `scripts/release/install.ps1` — operator-facing
    PowerShell wrapper. Params: `-ConfigPath`
    (mandatory), `-OutputConfigPath` (mandatory),
    `-Confirm` (switch). Dot-source'ит
    `scripts/dev/bootstrap_paths.ps1`, форвардит
    вызов в Python helper, мапит outcome в exit code
    (`0` preview/executed, `2` rejected, `3` other
    failure, `64` bad args).
  - `scripts/release/_install_runner.py` — тонкий
    Python helper. Underscore-prefixed (не для
    импорта). Принимает 3 positional args, валидирует
    confirm-флаг, вызывает
    `run_install_fast_path_from_json_file`, печатает 7
    ключевых полей результата + findings +
    recommended_actions.
  - `scripts/release/README.md` — operator-facing
    документация: usage (preview + execute),
    параметры, exit codes, явный список «что wrapper
    НЕ делает» (no MCP server start, no write-tools,
    no infobase touch, no `shell=True`, no packaging
    ecosystem, не подменяет launch ergonomics
    Step 4).
  - End-to-end preview-mode прогон verified: `ok=True`,
    `mode=preview`, `config_written=False`,
    bootstrap_pre OK, recommended action — re-run с
    `-Confirm`. Bad-args path возвращает usage и
    exit 64. Selfcheck registries без drift'а.
  - Commit `bce8966` — `Track B / Step 3 —
    operator-discoverable install fast path wrapper`,
    3 файла, 264 insertions.
- **Что НЕ сделано.** Production-код не правили
  (`apps/platform/installer.py` не тронут).
  Registries без drift'а. Никакого packaging
  ecosystem'а.

### Parallel Track B / Step 4 — operator/dev local launch umbrella (завершён)

- **Цель шага.** Снять с оператора/разработчика
  ритуал ручного PYTHONPATH bootstrap'а для типовых
  локальных задач. Один очевидный umbrella entry в
  каноническом `scripts/dev/`.
- **Что сделано.**
  - `scripts/dev/launch.ps1` — PowerShell умbrella с
    четырьмя subcommands: `selfcheck` (delegate в
    существующий `run_dev_check.ps1`), `repl`
    (dot-source bootstrap + interactive `python`),
    `run <script.py> [args…]` (dot-source bootstrap +
    `python @args`), `help` (default at no-args).
    Exit codes: `0` success / help; делегированный
    `$LASTEXITCODE` для `selfcheck` / `run`; `64` —
    unknown command или missing args.
  - `scripts/dev/README.md` — UPDATE одной добавочной
    секцией про `launch.ps1` сверху (без удаления /
    реструктуризации существующих описаний
    `bootstrap_paths.ps1` / `selfcheck.py` /
    `run_dev_check.ps1`).
  - Verification: parse OK, help / selfcheck / `run
    scripts/dev/selfcheck.py` happy paths возвращают
    exit 0 с корректным выводом (registries 15/25/16,
    `selfcheck_status=ok`); unknown command + `run`
    без args возвращают exit 64; `run nope.py`
    propagatе'ит python's exit code (2).
  - Commit `fd92477` — `Track B / Step 4 —
    operator/dev local launch umbrella`, 2 файла, 152
    insertions, 1 deletion.
- **Что НЕ сделано.** Никаких `__main__.py` в
  server-package'ах. Production-код вообще не
  тронут. Никакого MCP-server-launch ритуала
  (production transport — out of Track B). Никакого
  pytest (нет test suite'а). Registries без drift'а.

### Parallel Track B / Step 5 — root README quickstart and docs polish (завершён)

- **Цель шага.** Сделать root README нормальной
  «входной дверью» для нового человека: ≤ 50 строк
  основного текста с 1–2 строками о проекте,
  системными требованиями, install / check / launch
  командами, картой deeper docs, и явным «что
  Quickstart НЕ обещает».
- **Что сделано.**
  - `README.md` — добавлен блок `## Quickstart`
    между intro-параграфом и `## Идея`. Содержит:
    quote-блок «Что это» с current honest state
    (Phases 1–6 + Track A закрыты; Track B in
    progress; обновлён в Step 6 на «закрыт»);
    `### Системные требования`;
    `### Install` (PowerShell-команда + ссылка на
    `scripts/release/README.md`); `### Check`
    (`launch.ps1 selfcheck` + ссылка на
    `run_dev_check.ps1`); `### Local dev launch`
    (четыре umbrella-команды); `### Куда идти
    дальше` (5 pointer'ов на `apps/platform/README.md`,
    `docs/operator-manual.md`, `docs/runbooks/`,
    `docs/architecture/`, `PROJECT-STATUS.md`);
    `### Что Quickstart **не** обещает` (явно: no
    production transport, no installer ecosystem, no
    web UI, no enterprise deployment, no hot reload).
  - +81 insertion, 0 deletion — pure addition; ничего
    не удалено и не реструктурировано.
  - 15 referenced paths валидны (verified `test -e`).
  - Commit `0f65c58` — `Track B / Step 5 — root
    README quickstart and docs polish`, 1 файл.
- **Что НЕ сделано.** `scripts/release/README.md`,
  `scripts/dev/README.md`, `apps/platform/README.md`,
  `docs/operator-manual.md`, `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md` — не
  трогали. Никаких широких docs rewrite'ов.
  Registries без drift'а.

### Parallel Track B / Step 6 — final integration pass and Track B closure (завершён)

- **Цель шага.** Закрыть весь Track B как documented
  status. Read-only final integration check уже
  закрытых Steps 2–5, потом минимальные
  closure-docs/status updates, потом final closure
  commit.
- **Read-only final integration check.**
  - Working tree clean перед началом
    (`git status --short` пуст).
  - Git history линейная и читаемая: `85a4a7e`
    (Step 2) → `bce8966` (Step 3) → `fd92477`
    (Step 4) → `0f65c58` (Step 5).
  - Все Step 2 deliverables на диске: `.git`,
    `.gitignore`, `LICENSE`, `CHANGELOG.md`,
    `SECURITY.md`. Все Step 3 deliverables на месте.
    Все Step 4 deliverables на месте. Step 5
    Quickstart-блок в README присутствует.
  - Production-код вообще не тронут на всём треке —
    подтверждено отсутствием `apps/` / `packages/` в
    diff'ах ни одного из четырёх Track B commit'ов.
- **Что сделано в этом шаге.** Только closure
  docs/status updates (минимальный scope):
  - `README.md` — секция «Active parallel track»
    переработана в «Closed parallel tracks»
    (множественное число) + «Track B detail
    (закрыт)» с per-step описанием Steps 1–6 и
    summary outcomes; явный список «что Track B НЕ
    делает индустриальным продуктом» (honest
    constraints); явное «активного трека сейчас
    нет».
  - `PROJECT-STATUS.md` — header (Текущий шаг +
    Статус) обновлён под Track B closed; добавлены
    пять новых per-step секций (Steps 2/3/4/5/6).
  - `CHANGELOG.md` — entry `## 0.1.0` приведён в
    соответствие фактическому состоянию (Track B
    Steps 1–6 закрыты, не «in preparation»;
    `## 0.1.0 — initial public snapshot`).
  - Commit `Track B / Step 6 — final integration
    pass and track closure` зафиксирует closure event
    в git history.
- **Что НЕ сделано.** Никакого нового feature work,
  никаких production-правок, никаких новых MCP
  tool'ов, никакого remote push'а. `apps/`,
  `packages/`, `scripts/`, `examples/`,
  `docs/architecture/`, `docs/runbooks/`,
  `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md`,
  `pyproject.toml`, `.github/`, `.editorconfig`,
  `.python-version`, `.gitignore`, `LICENSE`,
  `SECURITY.md` — **не тронуты** в этом шаге.
- **Что Track B в сумме дал проекту.**
  - Repo стал git-репозиторием на ветке `main` с
    чистой линейной history, легко выкладываемой на
    любой git remote.
  - `.gitignore` корректно покрывает project-specific
    опасные / тяжёлые / локальные артефакты, защищая
    от случайного коммита cleartext credentials или
    snapshot tree'ев.
  - Apache-2.0 license, CHANGELOG, SECURITY на месте
    — legal/doc baseline для honest публикации.
  - Operator-discoverable install:
    `scripts/release/install.ps1` — без знания
    internal Python module path и без ручного
    PYTHONPATH ритуала.
  - Operator/dev local launch umbrella:
    `scripts/dev/launch.ps1` — `selfcheck` / `repl` /
    `run` / `help` за одну команду.
  - Root README имеет верхний Quickstart-блок:
    новый человек за 1–2 минуты понимает что это,
    как поставить, как проверить, куда идти дальше.
  - Production-код не трогали ни разу за весь
    Track B. Registry-инвариант сохранён точно
    `read=15 / write=25 / intelligence=16`.
- **Honest constraints, оставшиеся после closure
  Track B.** Track B **не сделал** проект «глубоким
  индустриальным продуктом». По-прежнему отсутствуют:
  production-grade MCP transport (auth /
  authorisation / network hardening), полный
  installer ecosystem (`.msi` / `.deb` / GUI wizard /
  signed binary distribution), web-UI / dashboard
  frontend, полный enterprise super-set (SSO/RBAC,
  multi-tenant, secrets vault как сервис, federated
  audit storage, policy-as-code DSL, multi-instance
  HA), hot reload / OS-level service supervision,
  multi-version matrix smoke на всех 1С версиях,
  полный AST-парсер XML/BSL, полная rollback/delete-
  вселенная (whitelist остаётся на двух tool'ах),
  production-grade transport / `__main__` / CLI у
  трёх MCP-серверов с auth. Эти направления остаются
  за пределами Track A + Track B.
- **Следующий шаг.** Активного трека нет. Открытие
  следующего parallel track'а — **отдельное решение
  оператора проекта**; Phase 7 как линейная фаза не
  запланирована. Possible candidates (только
  recommendations, без авто-открытия): operator
  credentials hardening track (env-substitution или
  OS keychain integration); multi-version 1С smoke
  track; полный rollback whitelist track. Менее
  рекомендуемые — full enterprise super-set, web-UI,
  packaging ecosystem (более широкий scope, выше
  риск).

### Parallel Track C / Step 1 — planning Packaging & Installer Delivery (завершён)

- **Цель шага.** Зафиксировать документационный вход
  в **Parallel Track C — Packaging & Installer
  Delivery**: назначение трека, целевой результат, что
  закрывает трек и что НЕ закрывает, чем отличается от
  Track A и Track B, guardrails, явный список «что НЕ
  входит», 10 acceptance criteria, открытые вопросы
  Step 2+. Кода не писать. Никаких изменений registry.
  Никаких новых MCP tool'ов. Никакого расширения
  product-layer surface'а.
- **Назначение трека.** Track B закрыл базовую
  productization-полировку (git baseline + install
  wrapper + launch umbrella + README quickstart).
  Самый жирный незакрытый разрыв сейчас — **не
  execution layer и не базовая ergonomics, а
  delivery/packaging слой**: `scripts/release/install.ps1`
  это тонкий wrapper над одной функцией, а не
  полноценный release-facing layer; нет release
  handoff документа для receive-side оператора; нет
  reproducible install-sequence checklist'а с
  системными зависимостями; `pyproject.toml` имеет
  `packages = []` в hatch wheel target (wheel build
  по сути no-op); нет single canonical release
  entrypoint map'а; нет release-time pre-handoff
  sanity check'а. Track C доводит существующий продукт
  до состояния, в котором его удобно передать другому
  человеку как packaged unit'ом — не открывая нового
  execution-core sprint'а и не входя в enterprise
  super-set.
- **Что реально появилось в Step 1.**
  - **Один новый план трека:**
    `docs/architecture/track-c-packaging-installer-delivery-plan.md`
    — назначение Track C, целевой результат
    (5-шаговый narrative для receive-side оператора),
    что Track C **не** закрывает (GUI installer
    wizard, signed binary distribution, package-
    manager publication, systemd / Windows Service
    registration, web-UI, full enterprise super-set,
    production-grade MCP transport, multi-version 1С
    matrix, AST-парсер, hot reload, новые MCP tools,
    production code rewrite), guardrails, 10
    acceptance criteria, 6 открытых вопросов
    (Q1—Q6), раздел «связь с Phase 6 / Track A /
    Track B», honest constraints после closure.
  - **Один новый step-map:**
    `docs/architecture/track-c-packaging-installer-delivery-step-map.md`
    — шесть шагов: Step 1 (planning, этот),
    Step 2 (release-facing scripts/release/ layout
    полишинг — `verify-release.ps1` + UPDATE
    `scripts/release/README.md`), Step 3 (packaging-
    facing install flow — `pyproject.toml` honest
    review), Step 4 (release handoff documentation —
    `docs/release-handoff.md`), Step 5 (integration
    & polish), Step 6 (final integration pass and
    Track C closure). Каждый шаг описан в едином
    формате (Цель / Что меняем / Затронутые зоны /
    Результат).
- **Что НЕ сделано (намеренно).**
  - **Никаких изменений production-кода.** `apps/`,
    `packages/`, `scripts/`, `pyproject.toml`,
    `.github/`, `.editorconfig`, `.python-version`,
    `.gitignore`, `examples/`, `LICENSE`,
    `SECURITY.md`, `CHANGELOG.md` — без изменений.
  - **Никаких изменений в `mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`,
    `apps/platform/`, `onec-policy-engine`,
    `onec-audit`, `onec-health`,
    `onec-process-runner`, `onec-troubleshooting`,
    `mcp-common`, `onec-config`.** Track C / Step 1
    это documentation-only.
  - **Никакого нового `verify-release.ps1`** на этом
    шаге. Это Step 2.
  - **Никакого `pyproject.toml` review.** Это
    Step 3.
  - **Никакого `release-handoff.md`.** Это Step 4.
  - **Никакого CHANGELOG update.** По симметрии с
    Track B (CHANGELOG обновляется один раз на
    closure трека) Track C по default'у будет
    обновлять CHANGELOG только в Step 6.
- **Что сказали явно в плане трека.**
  - Track C **не** закрывает: enterprise super-set,
    web-UI, полный AST-парсер, полную
    rollback/delete-вселенную, production-grade
    MCP transport, multi-version matrix, GUI
    installer wizard, signed binary distribution,
    publication к package managers, systemd /
    Windows Service registration, hot reload,
    новые MCP tools (registries `read=15 / write=25
    / intelligence=16` без drift'а), production
    code rewrite.
  - **GitHub remote push** — operator action, не
    часть трека. Track C готовит repo к handoff'у;
    нажатие `git remote add origin ...` +
    `git push -u origin main` — отдельный operator
    step.
- **Открытые вопросы Step 2+.** Q1 (где живёт
  release-handoff doc — default `docs/release-handoff.md`),
  Q2 (pre-handoff sanity check — отдельный
  `verify-release.ps1` vs `launch.ps1` extension —
  default отдельный скрипт по симметрии с
  `install.ps1`), Q3 (`pyproject.toml`
  `[tool.hatch.build.targets.wheel] packages` — fill
  honestly или explicit no-op comment — default fill
  honestly), Q4 (Windows-only vs cross-platform —
  default Windows-first), Q5 (release entrypoint map
  — отдельный документ vs раздел в root README —
  default отдельный документ), Q6 (CHANGELOG update
  cadence — default один раз на closure Track C).
- **Selfcheck после Step 1.** Зелёный без правок:
  `imports_ok = true`, registries `read=15 /
  write=25 / intelligence=16`, `selfcheck_status =
  ok`. Track C / Step 1 не правил production-кода,
  поэтому drift'а быть не должно — и его нет.
- **Следующий шаг.** **Parallel Track C / Step 2 —
  release-facing `scripts/release/` layout
  полишинг.** Step 2 включает: создание
  `scripts/release/verify-release.ps1` (pre-handoff
  sanity check над уже существующими entry points),
  возможно тонкий `_verify_runner.py` helper, UPDATE
  `scripts/release/README.md` (расширение, не
  переписывание). **Никаких изменений** в
  `scripts/release/install.ps1` (Track B / Step 3
  sealed) и в `scripts/dev/launch.ps1` (Track B /
  Step 4 sealed). Production-код не правится.
  Step 2 я открываю отдельным заходом, не в этом.

### Parallel Track C / Step 2 — release-facing verify path and layout polish (завершён)

- **Цель шага.** Расширить existing `scripts/release/`
  слой одним новым read-only entrypoint'ом —
  `verify-release.ps1` (pre-handoff sanity check над
  уже существующими entry points) — и UPDATE
  `scripts/release/README.md` под трёх-entrypoint
  surface (`install.ps1` + `verify-release.ps1` +
  `launch.ps1`). Никакого расширения write-поверхности,
  никаких изменений в `install.ps1` или `launch.ps1`,
  никакого production-кода.
- **Что реально появилось.**
  - `scripts/release/verify-release.ps1` — read-only
    pre-handoff sanity check: проверяет наличие
    install entrypoint'ов, dev-check workflow, planning
    docs, печатает компактный human-readable отчёт.
    Никаких subprocess'ов 1cv8, никаких side effects.
  - `scripts/release/README.md` — расширен под
    объяснение verify-release.ps1 и трёх-entrypoint
    surface'а. Existing install-секции не переписаны.
- **Что НЕ сделано (намеренно).** `apps/`, `packages/`,
  `pyproject.toml`, `scripts/release/install.ps1`,
  `scripts/dev/launch.ps1`, `docs/architecture/`,
  registries — без изменений. Никакого нового MCP
  surface'а; никакого нового write path'а.
- **Commit.** `ef087c8` — `Track C / Step 2 — release-
  facing verify path and layout polish`.

### Parallel Track C / Step 3 — packaging-facing install flow honest review (завершён)

- **Цель шага.** Честный review packaging-facing части
  `pyproject.toml`: явно зафиксировать, что Phase 6
  продукт **намеренно** не предназначен для publication
  как single Python wheel из-за multi-app monorepo
  shape. Никакого фиктивного wheel build'а; никакого
  package-manager publication'а.
- **Что реально появилось.**
  - `pyproject.toml` — добавлен явный block-комментарий
    рядом с `[tool.hatch.build.targets.wheel]
    packages = []`: это намеренный no-op, операторы
    устанавливают продукт через `scripts/release/install.ps1`
    (Phase 6 boundary `run_install_fast_path`), а не
    через `pip install`. Версия 0.1.0 без bump'а.
  - `scripts/release/README.md` — небольшая secция
    «Packaging story», которая ссылается на
    pyproject-комментарий и явно отвергает GUI
    installer wizard / signed binary distribution /
    package-manager publication как out-of-scope.
- **Что НЕ сделано (намеренно).** Никакого fix'а
  hatch wheel target'а, никакого отдельного `setup.py`,
  никаких GitHub Releases, никаких Docker images,
  никаких `.msi` / `.deb`. Это **review**, не
  packaging-фиксация.
- **Commit.** `a4f42f9` — `Track C / Step 3 — packaging-
  facing install flow honest review`.

### Parallel Track C / Step 4 — release handoff documentation (завершён)

- **Цель шага.** Зафиксировать **один** release handoff
  документ для receive-side оператора. Никакой broad
  docs rewrite; никакого переписывания operator/
  administrator/developer manual'ов; ничего из Phase 6
  / Step 7 manual'ов не дублировать.
- **Что реально появилось.**
  - `docs/release-handoff.md` — новый документ,
    адресованный receive-side оператору, который
    получил репозиторий проекта: что вы получили,
    system prerequisites (Windows + PowerShell + Python
    3.11; `1cv8.exe` опционально и только для real
    write path), reproducible install sequence
    (verify-release.ps1 → install.ps1 preview →
    install.ps1 -Confirm), verify sequence (dev launch
    selfcheck), known limitations honest table
    (production-grade transport / GUI installer /
    enterprise super-set / multi-version matrix —
    out of scope). Без новых обещаний.
- **Что НЕ сделано (намеренно).** `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `README.md`,
  `PROJECT-STATUS.md`, `CHANGELOG.md`,
  `docs/architecture/`, `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks*` — без
  изменений. Только один новый файл.
- **Commit.** `7ca9b3f` — `Track C / Step 4 — release
  handoff documentation`.

### Parallel Track C / Step 5 — integration and handoff polish (завершён)

- **Цель шага.** Минимально и честно интегрировать
  `docs/release-handoff.md` в верхнеуровневую
  навигацию проекта: receive-side handoff story должна
  стать discoverable из root README, без раздувания
  документации.
- **Что реально появилось.**
  - `README.md` — четырёхстрочный pointer на
    `docs/release-handoff.md` добавлен в Quickstart
    раздел «Куда идти дальше». Существующая
    структура Quickstart не переписана.
- **Что НЕ сделано (намеренно).** Никакого
  переписывания `docs/release-handoff.md`, никакого
  переписывания `scripts/release/README.md`, никакого
  трогания `PROJECT-STATUS.md`, никакого broad docs
  cleanup. Этот шаг — single high-leverage navigation
  edit.
- **Commit.** `8ccecf6` — `Track C / Step 5 —
  integration and handoff polish`.

### Parallel Track C / Step 6 — final integration pass and Track C closure (завершён)

- **Цель шага.** Закрыть весь Track C как documented
  status. Read-only final integration check уже
  закрытых Steps 1–5, потом минимальные closure-docs/
  status updates, потом final closure commit.
- **Read-only final integration check.**
  - Working tree clean перед началом
    (`git status` пуст).
  - Git history линейная и читаемая: `af2d7f4`
    (Step 1) → `ef087c8` (Step 2) → `a4f42f9` (Step 3)
    → `7ca9b3f` (Step 4) → `8ccecf6` (Step 5).
  - Все Step 1 deliverables на диске
    (`docs/architecture/track-c-*`); Step 2 deliverables
    на диске (`scripts/release/verify-release.ps1`,
    обновлённый `scripts/release/README.md`); Step 3
    deliverables на диске (honest comment в
    `pyproject.toml`, packaging story в release/README);
    Step 4 deliverable на диске (`docs/release-handoff.md`,
    331 строка); Step 5 deliverable на диске (pointer
    в Quickstart README:62-65).
  - Production-код вообще не тронут на всём треке —
    подтверждено отсутствием `apps/` / `packages/` в
    diff'ах ни одного из пяти Track C commit'ов.
- **Что сделано в этом шаге.** Только closure
  docs/status updates (минимальный scope):
  - `README.md` — Quickstart intro обновлён под
    «Активного трека сейчас нет»; «Active parallel
    track» заменён добавлением Track C в «Closed
    parallel tracks» list; новая секция «Track C
    detail (закрыт)» с per-step описанием Steps 1–6
    и явным списком «что Track C НЕ делает
    индустриальным продуктом»; pointer на planning
    docs обновлён («включая Track B и Track C
    planning»).
  - `PROJECT-STATUS.md` — header (Текущий шаг +
    Статус) обновлён под Track C closed; stale
    параграф «Track B сейчас documentation-only»
    заменён на post-Track-C closure narrative;
    добавлены пять новых per-step секций (Steps
    2/3/4/5/6).
  - `CHANGELOG.md` — entry `## 0.1.0` дополнен
    bullet'ом про Parallel Track C closed (Steps
    1–6); honest constraints и registry invariant
    остались без изменений (Track C их не меняет);
    «Active work: None» остаётся корректным после
    Track C closure.
  - Commit `Track C / Step 6 — final integration
    pass and track closure` зафиксирует closure
    event в git history.
- **Что НЕ сделано.** Никакого нового feature work,
  никаких production-правок, никаких новых MCP
  tool'ов, никакого remote push'а. `apps/`,
  `packages/`, `scripts/`, `examples/`,
  `docs/architecture/`, `docs/runbooks/`,
  `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md`,
  `docs/release-handoff.md`,
  `pyproject.toml`, `.github/`, `.editorconfig`,
  `.python-version`, `.gitignore`, `LICENSE`,
  `SECURITY.md` — **не тронуты** в этом шаге.
- **Что Track C в сумме дал проекту.**
  - Release-facing entrypoint surface стал
    трёх-частным (`install.ps1` + `verify-release.ps1`
    + `launch.ps1`) с человеко-читаемым
    `scripts/release/README.md`.
  - `pyproject.toml` packaging limitation теперь
    явно задокументирована inline комментарием —
    больше не выглядит как «забытый no-op».
  - Receive-side оператор имеет один entry document
    (`docs/release-handoff.md`) с reproducible
    install/verify sequence и honest known
    limitations.
  - Root README quickstart честно ведёт на
    receive-side handoff story (Step 5 pointer).
  - Production-код не трогали ни разу за весь
    Track C. Registry-инвариант сохранён точно
    `read=15 / write=25 / intelligence=16`.
- **Honest constraints, оставшиеся после closure
  Track C.** Track C **не сделал** проект «глубоким
  индустриальным продуктом». По-прежнему отсутствуют:
  GUI installer wizard, `.msi` / `.deb` / signed
  binary distribution, publication к package
  managers (PyPI / Chocolatey / winget / apt),
  systemd / Windows Service registration, hot reload,
  web-UI / dashboard frontend, полный enterprise
  super-set (SSO/RBAC, multi-tenant, secrets vault
  как сервис, federated audit storage, policy-as-code
  DSL, multi-instance HA), production-grade MCP
  transport, multi-version 1С matrix, полный
  AST-парсер XML/BSL, полная rollback/delete-
  вселенная, новые MCP tools, production code
  rewrite. Эти направления остаются за пределами
  Track A + Track B + Track C.
- **Следующий шаг.** Активного трека нет. Открытие
  следующего parallel track'а — **отдельное решение
  оператора проекта**; Phase 7 как линейная фаза не
  запланирована. Possible candidates (только
  recommendations, без авто-открытия): operator
  credentials hardening track (env-substitution или
  OS keychain integration); multi-version 1С smoke
  track; полный rollback whitelist track. Менее
  рекомендуемые — full enterprise super-set, web-UI,
  packaging ecosystem (более широкий scope, выше
  риск).

## Phase 6 закрыта

**Phase 6 закрыта на Step 9.**

Что закрыто честно (Phase 1–5 + Phase 6 / Step 1–9 в
одном связном продуктовом контуре):

- Phase 1 — read MVP.
- Phase 2 — write MVP с `run_write_flow` дисциплиной как
  единственным mutating-путём.
- Phase 3 — Phase 3 metadata changes (object/attribute/form/
  module-level mutating tools и verify-tools на substring-патч'е).
- Phase 4 — intelligence MVP (read-only по конструкции).
- Phase 5 — product layer (bootstrap / install / runtime /
  dashboard / workflows / rollback / real-stand) на восьми
  шагах с финальным integration pass'ом.
- **Phase 6 — Industrialization & Completion Track:**
  - Step 2: один real binary-backed slice
    (`create_dump_snapshot`); operator-declared argv-template
    с whitelisted placeholder'ами; runtime failure НЕ
    падает в silent stub fallback.
  - Step 3: install / setup fast path сокращает manual
    ritual до одной boundary-функции; атомарная запись
    JSON; round-trip через `bootstrap_product_from_json_file`.
  - Step 4: первый исполняемый rollback path для двух
    tool'ов whitelist'а (`add_catalog_attribute`,
    `add_document_attribute`); реализация **только** через
    public `restore_dump_file_from_snapshot` (не back-door);
    обязательный post-rollback verify через
    `diff_dump_fragment`; audit-row `details` дополнение
    backward-compatible.
  - Step 5: первый structural XML edit slice
    (`add_form_attribute`); шесть DOM-style helper'ов в
    `metadata_ops.py`; новая verify-ветка
    `kind="form_attribute_exists"`; на Step 9 добавлен
    минимальный guided-wrapper `safe-add-form-attribute`
    (см. выше) — это не новый MCP tool, а thin guide над
    существующим write-tool'ом.
  - Step 6: structured runtime logs +
    rotate-if-exceeds-size в одно поколение, узкий
    `restart_policy ∈ {"never","restart-if-stale"}`
    (boundary-only, no daemon); enriched
    `RuntimeServiceState` + `runtime-state.json` schema 2
    с backward-compat reader'ом.
  - Step 7: standalone manuals + runbooks
    (`docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`, `docs/runbooks.md`); сам
    Step 7 — documentation-only.
  - Step 8: узкий enterprise-foundation contract + read-only
    `inspect_enterprise_foundation` boundary; четыре
    проверяемые секции; верт `foundation_level ∈
    {"absent","minimal","partial","strong"}` плюс
    отдельный `ready_for_enterprise_track`. Никакого
    fake `enterprise_ready` флага.
  - Step 9: integration pass всего вышеперечисленного в
    одном связном сценарии + шесть honest failure paths +
    пять discipline asserts. Две минимальные кодовые
    правки (`safe-add-form-attribute` workflow +
    `_config_to_dict` round-trip fix).

Что осталось до состояния finished industrial product
(парallel / enterprise tracks **после** Phase 6):

- **Полное замещение Phase 2 stub'ов:** Phase 6 закрыла
  один binary-backed путь (`create_dump_snapshot`).
  `apply_config_from_files` и `update_database_configuration`
  остаются stub-backed (process apply / process update,
  не настоящие `1cv8 LoadConfigFromFiles` / `UpdateDBCfg`).
  Полный набор binary-backed dispatch'ей —
  parallel track.
- **Полная rollback-вселенная:** Phase 6 закрыла rollback
  для двух tool'ов из 25 в registry write-server'а.
  Расширение whitelist'а (включая нетривиальные case'ы
  типа `delete_*` write-tool'ов, у которых пока нет
  семантики удаления в 1С) — parallel track.
- **Полное metadata coverage и AST-парсер:** Phase 6
  ship'нула один structural edit (`add_form_attribute`).
  Полный DOM-edit для всех metadata-операций, BSL
  AST-парсер, namespaced 1cv8 cards — отдельные
  технологические track'и.
- **Production-grade process supervision:** Windows
  Service / systemd unit registration, hot reload, real
  background watcher, exponential backoff / max-restarts,
  multi-generation log rotation, journald / log
  aggregation / forwarding — parallel track.
- **Полный enterprise super-set:** SSO/RBAC, multi-tenant,
  secrets vault как сервис, federated audit storage,
  policy-as-code DSL, multi-instance HA, web-UI /
  dashboard frontend, federated identity. Step 8 шипнул
  только foundation; полная enterprise-вселенная —
  parallel track.
- **Production-grade MCP transport:** `__main__` / CLI у
  трёх MCP-серверов; production-grade transport
  (HTTP/stdio); auth между orchestrator'ом и MCP клиентами.
  Parallel track.
- **GUI installer / wizard / `.msi` / `.deb` / signed
  binary distribution / packaging ecosystem:** parallel
  track. Phase 6 ship'нул только short install script +
  declarative template.
- **Полный version-matrix smoke на всех 1С версиях и
  стендах:** parallel track. Phase 6 ship'нул только
  controlled smoke contract.
- **Полная intelligence-вселенная:** ML / clustering
  поверх `analyze_event_log_patterns`; настоящий
  topo-sort `suggest_safe_change_order` по графу
  зависимостей. Parallel track.
- **Operator runbook coverage:** Phase 6 / Step 7
  ship'нул шесть recipes. Production runbook
  ecosystem — parallel track.

Эти ограничения зафиксированы как **honest constraints**:
платформа НЕ претендует на enterprise-ready / production-
ready статус. `ready_for_enterprise_track=True` (Step 8)
означает буквально «foundation under next-step enterprise
work собран», не «готовы к prod».

Non-blocking follow-ups, явно вынесенные за пределы
Phase 6 (или в parallel / enterprise tracks):

- **Полное замещение всех Phase 2 stub'ов
  одновременно** на сетку режимов
  `DESIGNER` / `ENTERPRISE` / `DumpCfg` —
  parallel track после Phase 6. Phase 6
  ship'ит **один** binary-backed путь, не три
  одновременно.
- **Полная rollback-вселенная** для всех
  write-tool family'й — parallel track. Phase 6
  ship'ит исполнимый rollback хотя бы для
  одного класса.
- **Полное metadata coverage** (все возможные
  `delete_*`, `replace_*`, `refactor_*`) —
  parallel track. Phase 6 — точечный добор.
- **Полный AST-парсер XML / BSL** — отдельный
  технологический track. Phase 6 — один шаг к
  structural editing.
- **Полный enterprise super-set:** SSO/RBAC,
  multi-tenant, secrets vault как сервис,
  federated audit storage, policy-as-code DSL,
  multi-instance HA — отдельный
  enterprise-track после Phase 6.
- **Production-grade MCP transport / `__main__`
  / CLI у трёх MCP-серверов** — отдельный
  track.
- **Hot reload без рестарта процесса**, OS-level
  service supervision (Windows Service / systemd
  unit), automatic-restart-supervisor —
  отдельный track.
- **Web-UI / dashboard frontend / workflow
  runner UI / rollback assistant UI** —
  отдельный track после Phase 6.
- **Многосторонний end-to-end на матрице 1С
  версий и стендов** — отдельный track.
- **Настоящий topo-sort
  `suggest_safe_change_order` по графу
  зависимостей; ML / clustering поверх
  `analyze_event_log_patterns`** — оба
  остаются parallel tracks.
- **GUI installer / wizard** — out of Phase 6
  scope (Phase 6 ship'ит short install script
  + declarative template).
- **Override-флаг для запуска mutating
  workflow'ов на `degraded` dashboard'е**;
  **автоматический retry transient mutating
  step'ов**; **shared sub-tool cache внутри
  dashboard-операции**; **настраиваемый
  timeout для smoke probe** — все возможные
  enhancements, не входят в Phase 6.

## Крупные этапы проекта (что ещё осталось)

- **Phase 0 — инфраструктурная база.** Каркас монорепо, базовые конфиги,
  общие пакеты-заглушки, CI-скелет. **Закрыта.**
- **Phase 1 — read MVP.** Минимальный рабочий `mcp-read-server`: чтение метаданных,
  конфигурации и данных 1С через MCP. **Закрыта.**
- **Phase 2 — write MVP.** Минимальный рабочий `mcp-write-server`: безопасные
  операции изменения с политиками и аудитом. **Закрыта.**
- **Phase 3 — metadata changes.** Полноценные операции над метаданными
  конфигурации 1С (объекты, реквизиты, формы, модули). **Закрыта.**
- **Phase 4 — intelligence layer.** `mcp-intelligence-server`: read-only
  intelligence-tools поверх read/write слоёв — dependency / impact
  analysis, troubleshooting, рекомендации. **Закрыта** (16 public
  tools, группы A/B/C/D полностью покрыты, integration pass
  Step 7 пройден).
- **Phase 5 — product layer.** Переход от набора серверов и tool'ов
  к цельному продуктовому контуру: bootstrap, runtime orchestration,
  health dashboard, guided workflows, rollback / recovery / audit
  UX, real-stand / 1cv8 binary integration track. **Закрыта**
  (Step 1–8 завершены; final integration pass пройден без
  правок кода; product-layer контур end-to-end отрабатывает на
  synthetic-окружении; см. `docs/architecture/phase-5-step-map.md`).
  Закрытие Phase 5 **не означает** полностью industrial-grade /
  enterprise-ready продукт — крупные хвосты адресованы Phase 6
  (точечно) и parallel-track'ами после.
- **Phase 6 — industrialization & completion track.** Доведение
  продукта до finished / deployable состояния поверх готового
  ядра Phase 1–5: реальный 1cv8-backed dispatch (хотя бы для
  одного Phase 2 stub-backed пути), исполнимый rollback хотя
  бы для одного класса write-tool'ов, короткий install/setup
  сценарий (≤ 5 ручных шагов), real-stand end-to-end smoke на
  reference stand'е, runtime hardening (логи + базовая restart
  policy), operator/admin/developer manuals + runbooks как
  standalone docs, foundation для enterprise-трека.
  **Активная фаза** (Step 1 — planning Industrialization &
  Completion Track — в процессе; всего планируется 8 шагов,
  см. `docs/architecture/phase-6-step-map.md`). Закрытие
  Phase 6 **не означает** полностью enterprise-ready
  продукт — полная enterprise-вселенная (SSO/RBAC,
  multi-tenant, secrets vault, federated audit, policy-as-code
  DSL, multi-instance HA), полный AST-парсер, web-UI,
  multi-instance HA остаются за пределами фазы как parallel
  track'и / enterprise track после Phase 6.
