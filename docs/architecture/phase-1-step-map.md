# Phase 1 Step Map

Стартовый implementation map для входа в Phase 1. Покрывает первые
шаги, после которых у платформы появляется рабочий live-adapter,
рабочий dump-adapter и первые реальные read-инструменты. Вся фаза
сюда не входит — это карта старта, а не полный план до MVP.

## Step 1

**`onec-process-runner` из stub в реальный runner.**

- **Цель.** Получить безопасный и предсказуемый запуск внешних
  процессов (1cv8/unpacker) с корректной обработкой таймаутов,
  stdout/stderr и exit code. Без этого шага невозможны ни live-вызовы,
  ни работа с dump-источником.
- **Что меняем.** Замена stub `run_process` в `packages/onec-process-runner`
  на реальную реализацию на стандартной библиотеке (`subprocess`).
  Уточняем `ProcessRunRequest` / `ProcessRunResult` под фактические
  потребности (cwd, timeout, env subset, stdin feed).
- **Затронутые файлы/пакеты.** `packages/onec-process-runner/src/...`,
  README пакета. Никаких изменений в `mcp-common`.
- **Результат.** Любой шаг Phase 1 может поднять внешний процесс
  предсказуемым способом. `dev-check` остаётся зелёным; поведение
  `run_process` покрывается локальной ручной проверкой на простом
  внешнем вызове.

## Step 2

**`onec-config` — рабочая модель окружения тестовой базы.**

- **Цель.** Зафиксировать единое описание окружения тестовой инфобазы,
  которое используют и live-, и dump-инструменты.
- **Что меняем.** В `packages/onec-config` добавить/расширить
  `EnvironmentConfig` — публикация (HTTP base URL), каталог dump,
  таймауты, режим доступа (`allow_write`), идентификатор базы.
  Дополнить `load_project_config` валидацией обязательных полей.
- **Затронутые файлы/пакеты.** `packages/onec-config/src/...`,
  README пакета. Возможно — пример конфигурации в `examples/` (без
  секретов).
- **Результат.** В коде появляется единственная точка, откуда
  read-server и все пакеты берут параметры окружения. Дальнейшие шаги
  не придумывают «где взять URL» каждый раз заново.

## Step 3

**Реальные live-health-checks в `onec-health`.**

- **Цель.** Перевести stub-проверки в рабочие проверки, чтобы
  `check_runtime_health` и `diagnose_connectivity_issue` имели
  реальный сигнал.
- **Что меняем.** В `packages/onec-health` заменить
  `check_http_gateway_available`, `check_search_index_available`,
  `check_dump_path_exists` на фактические проверки: HTTP-probe
  публикации, существование/читаемость каталога dump и индекса.
  `summarize_health` и `HealthCheckResult` остаются как есть по
  контракту.
- **Затронутые файлы/пакеты.** `packages/onec-health/src/...`,
  README пакета. Прямая связь с `onec-config` (берёт оттуда URL и
  путь).
- **Результат.** `health_summary` read-server'а перестаёт быть
  демо-сценарием на булевых входах и начинает опираться на реальные
  проверки окружения.

## Step 4

**Базовый runtime/adapter слой для `mcp-read-server`.**

- **Цель.** Ввести общий слой, через который live-tools ходят по
  HTTP в публикацию 1С, а dump-tools читают локальную выгрузку.
  Отделить «как ходить» от «что спрашивать».
- **Что меняем.** В `apps/mcp-read-server` появляется внутренний
  подпакет с live HTTP-adapter'ом и dump-adapter'ом. Контракты ошибок
  транспорта/домена зашиваются через общую иерархию `mcp-common`
  (`PlatformError`, `ProcessExecutionError`, `HealthCheckError` и
  новые transport-специфичные исключения, если действительно понадобятся).
  Adapter'ы получают окружение из `onec-config`.
- **Затронутые файлы/пакеты.** `apps/mcp-read-server/src/...`,
  частично `packages/mcp-common` (только если потребуется добавить
  transport-specific исключение — не расширять зря).
- **Результат.** У read-server появляется единый способ говорить с
  live и dump. Инструменты становятся тонкими: описание намерения +
  вызов adapter'а.

## Step 5

**Первые live-read инструменты.**

- **Цель.** Получить первые реально работающие live-tools и
  подтвердить, что adapter слой жизнеспособен.
- **Что меняем.** В `apps/mcp-read-server/src/mcp_read_server/tools.py`
  (или соседнем модуле, если разнесём по файлам) появляются
  `get_configuration_info`, `get_metadata_tree`, `get_metadata_object`.
  Они регистрируются в `REGISTERED_TOOLS` через уже существующий
  `build_tool_registry(...)`. Envelope — shared `ToolResult`.
- **Затронутые файлы/пакеты.** `apps/mcp-read-server/src/...`.
  Других пакетов не трогаем.
- **Результат.** Агент (через ручной вызов/скрипт) может прочитать
  имя/версию конфигурации и дерево метаданных тестовой базы.
  Это первый наблюдаемый «read работает» момент.

## Step 6

**Первые dump-read инструменты.**

- **Цель.** Добавить быстрый способ читать код и искать по dump,
  без обращения к live-базе.
- **Что меняем.** В `apps/mcp-read-server` регистрируются
  `read_module_code_from_dump`, `search_code`, `search_metadata`
  поверх dump-adapter'а из Step 4. Проверка пути dump идёт через
  уже рабочий `check_dump_path_exists` из Step 3.
- **Затронутые файлы/пакеты.** `apps/mcp-read-server/src/...`,
  пример dump в `examples/demo-dumps` (только как тестовая данность,
  не как код).
- **Результат.** Read-server покрывает два ключевых источника
  Phase 1 — live и dump — первыми реальными инструментами. Дальнейшие
  шаги фазы (`validate_query` + `execute_read_query`, `get_event_log`,
  `get_object_structure` / `get_form_structure`, `check_runtime_health`,
  `diagnose_connectivity_issue`) выносятся в отдельный step map
  следующего этапа Phase 1.
