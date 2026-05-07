# Phase 1 Entry — Read MVP

## Цель фазы

Собрать первый технический MVP платформы: рабочий `mcp-read-server`
с реальными read-only инструментами поверх тестовой инфобазы 1С.
После Phase 1 у платформы появляется реальная, наблюдаемая ценность:
агент может читать конфигурацию, метаданные и данные 1С через MCP.

## Что уже готово на входе

- `mcp-read-server` skeleton (`ping`, `health_summary`, registry).
- Общие пакеты: `mcp-common`, `onec-process-runner` (stub),
  `onec-policy-engine`, `onec-audit`, `onec-health`, `onec-troubleshooting`,
  `onec-config`.
- Shared контракты: `ToolResult`, registry helpers, `OperationContext`,
  общая иерархия исключений.
- Config / health / troubleshooting contracts: `EnvironmentConfig`,
  `ProjectConfig`, `HealthCheckResult`, `summarize_health`,
  `diagnose_from_health`.
- Dev-check локально (`scripts/dev/run_dev_check.ps1`) и CI workflow
  (`.github/workflows/dev-check.yml`).
- Runbook локальной проверки (`docs/runbooks/local-dev-check.md`).

## Что должно быть сделано в рамках Phase 1

Первое приближение набора реальных read-tools:

- `get_configuration_info` — базовые сведения о конфигурации
  (имя, версия, совместимость, поставщик).
- `get_metadata_tree` — дерево объектов метаданных с фильтрами по типу.
- `get_metadata_object` — карточка конкретного объекта метаданных.
- `get_object_structure` — реквизиты, табличные части, формы, модули
  объекта.
- `get_form_structure` — структура формы (реквизиты, элементы,
  обработчики).
- `read_module_code_from_dump` — чтение модуля по имени из выгрузки
  конфигурации.
- `search_code` — поиск по коду (в том числе по dump).
- `search_metadata` — поиск по именам/синонимам объектов метаданных.
- `validate_query` — синтаксическая валидация запроса 1С.
- `execute_read_query` — выполнение безопасного read query на тестовой
  базе.
- `get_event_log` — чтение журнала регистрации с фильтрами.
- `check_runtime_health` — агрегированная диагностика живой базы
  (HTTP-gateway, публикация, индекс, выгрузка).
- `diagnose_connectivity_issue` — human-readable диагностика проблем
  соединения с live-базой/dump.

## Что считать MVP фазы

- `mcp-read-server` подключается к тестовой базе через реальный
  HTTP-adapter;
- читает `get_configuration_info` и `get_metadata_tree` на живой базе;
- ищет по dump (`search_code`, `read_module_code_from_dump`);
- валидирует и выполняет безопасный read query
  (`validate_query` + `execute_read_query`);
- различает проблемы live vs dump и даёт корректный
  `TroubleshootingReport` через `diagnose_connectivity_issue` /
  `check_runtime_health`.

При одновременном выполнении этих пунктов Phase 1 MVP считается
достигнутым.

## Какие риски войдут в Phase 1

- **Отсутствие реального MCP runtime.** Три skeleton-сервера пока не
  поднимаются как MCP-процессы — это отдельный кусок работы
  (транспорт, регистрация инструментов во внешнем MCP-хосте).
- **Реализация `onec-process-runner`.** Сейчас stub, поднимает
  `NotImplementedError`. В Phase 1 нужна безопасная реализация запуска
  внешних процессов (`1cv8`, unpacker'ы) с корректным stdout/stderr,
  timeouts и exit codes.
- **Live HTTP-adapter.** Подключение к публикации 1С через Apache,
  аутентификация, обработка нестабильных соединений.
- **Различие transport / domain ошибок.** Важно, чтобы сетевые сбои,
  ошибки публикации и ошибки запроса 1С не сваливались в одну кучу —
  иначе `TroubleshootingReport` бесполезен.
- **Импортный wiring при реальном запуске.** Текущий `PYTHONPATH`
  bootstrap хорош для selfcheck, но для реального MCP-процесса
  потребуется нормальный packaging / workspace setup (editable install,
  entry points).
- **Тестовая инфобаза.** Нужна стабильная demo-база + dump-снимок для
  воспроизводимости инструментов (`examples/demo-infobase`,
  `examples/demo-dumps`).
