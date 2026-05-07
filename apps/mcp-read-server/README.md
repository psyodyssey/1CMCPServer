# mcp-read-server

Первый сервер платформы **1C Agent Platform**, отвечающий **только за чтение**:
конфигурация, метаданные, данные и журналы 1С. Ни один инструмент этого
сервера не должен изменять систему — это read-only зона.

## Что сейчас внутри

Серверный bootstrap + первая волна реальных read-tools поверх
runtime/adapter слоя. MCP-транспорт ещё не подключён — tools
вызываются напрямую как функции. Реализовано:

- `ToolResult` — стандартный конверт ответа инструмента
  (`ok`, `tool_name`, `message`, `payload`);
- liveness и skeleton-tools:
  - `ping()` — liveness-маркер сервера;
  - `health_summary(dump_path, gateway_available, search_index_available)` —
    собирает результаты health-проверок, агрегирует через
    `summarize_health` и, при наличии проблем, дополняет ответ
    `TroubleshootingReport` от `diagnose_from_health`;
- первые реальные live-read инструменты (Phase 1 / Step 6):
  - `get_configuration_info(environment)` — читает configuration info
    с `<http_base_url>/configuration`;
  - `get_metadata_tree(environment, filter_value=None)` — читает
    дерево метаданных с `<http_base_url>/metadata`, опциональный
    фильтр передаётся как `?filter=<urlencoded>`;
  - `get_metadata_object(environment, object_name)` — читает карточку
    объекта с `<http_base_url>/metadata/object?name=<urlencoded>`;
- первые реальные dump-read инструменты (Phase 1 / Step 7):
  - `read_module_code_from_dump(environment, relative_path)` —
    читает текст одного файла из каталога выгрузки;
  - `search_code(environment, query)` — простой substring-поиск
    по всем `*.bsl` файлам выгрузки с preview вокруг первого
    попадания;
  - `search_metadata(environment, query)` — substring-поиск по
    всем `*.xml` выгрузки; попадание по имени файла или по
    содержимому XML;
- query path (Phase 1 / Step 8):
  - `validate_query(environment, query)` — синтаксическая валидация
    запроса через `<http_base_url>/query/validate?text=<urlencoded>`;
  - `execute_read_query(environment, query, row_limit=100)` —
    выполнение безопасного read query через
    `<http_base_url>/query/execute?text=<urlencoded>&limit=<row_limit>`.
    Содержит **временный read-only guardrail**: до обращения к live
    endpoint запрос приводится к верхнему регистру и отвергается,
    если в нём встречаются ключевые слова `INSERT`, `UPDATE`,
    `DELETE`, `DROP`, `ALTER`, `CREATE`, `TRUNCATE`. Это stop-gap до
    полноценного policy-слоя.
- event log и структура объектов/форм (Phase 1 / Step 9):
  - `get_event_log(environment, period_start=None, period_end=None,
    level=None, user=None)` — чтение журнала регистрации через
    `<http_base_url>/event-log`; переданные фильтры передаются
    query-параметрами `start`/`end`/`level`/`user` в URL-encoded виде;
  - `get_object_structure(environment, object_name)` — структура
    объекта (реквизиты, табличные части, формы, модули) через
    `<http_base_url>/object/structure?name=<urlencoded>`;
  - `get_form_structure(environment, object_name, form_name=None)` —
    структура формы (реквизиты, элементы, привязки обработчиков)
    через `<http_base_url>/form/structure?object=<urlencoded>`
    (+ `&form=<urlencoded>` если задано).
- diagnostics wrapping (Phase 1 / Step 10):
  - `check_runtime_health(environment)` — агрегированный снимок
    здоровья окружения поверх `build_runtime_context(...)`:
    `ok=True` при `health_codes == ["ok"]`, иначе `ok=False`.
    payload содержит краткий slice окружения и полный список
    `checks` из `HealthCheckResult` каждой проверки.
  - `diagnose_connectivity_issue(environment)` — human-readable
    обёртка над `onec_troubleshooting.diagnose_from_health(...)`:
    отдаёт `problem_code` / `probable_cause` /
    `recommended_action` для первой сработавшей проблемы;
    при `["ok"]` — `ok=True` с тройкой `None`.
- server registry: `REGISTERED_TOOLS` на пятнадцать инструментов
  (`ping`, `health_summary`, `get_configuration_info`,
  `get_metadata_tree`, `get_metadata_object`,
  `read_module_code_from_dump`, `search_code`, `search_metadata`,
  `validate_query`, `execute_read_query`,
  `get_event_log`, `get_object_structure`, `get_form_structure`,
  `check_runtime_health`, `diagnose_connectivity_issue`),
  `list_tools()`, `get_tool(name)`;
- wiring к общим пакетам: `onec-health`, `onec-troubleshooting`,
  `onec-config`, и к локальному runtime-подпакету.

Все реальные tools (live и dump) работают по единой схеме: собирают
`build_runtime_context(environment)`, кладут `health_codes` в
`payload.runtime`, вызывают нужный adapter (`fetch_json_from_environment`
или `read_dump_file` / `find_files_by_pattern` + `read_text_file`) и
оборачивают результат в shared `ToolResult`. Любая `PlatformError` от
adapter-слоя заворачивается в `ToolResult(ok=False, ...)` — наружу
исключение не уходит.

Сервер использует shared contracts из `mcp-common`: `ToolResult` как единый
response envelope и registry helpers (`build_tool_registry`,
`list_registered_tools`, `get_registered_tool`).

## Runtime / adapters layer

Внутри `mcp_read_server.runtime` живёт внутренний adapter-слой, на
который будут опираться реальные read-tools Phase 1:

- **runtime context builder** — `RuntimeContext` и
  `build_runtime_context(environment)`: снимок окружения плюс
  результат `check_environment_health(...)` и агрегированные коды
  `summarize_health(...)`.
- **live HTTP adapter** — `fetch_json(url, timeout_seconds)` и
  `fetch_json_from_environment(environment, relative_path)`: GET →
  UTF-8 → JSON → dict через `urllib.request`. Все транспортные и
  decode-ошибки унифицированно заворачиваются в `PlatformError` из
  `mcp-common`.
- **dump file adapter** — `resolve_dump_path`, `read_text_file`,
  `find_files_by_pattern`, `read_dump_file`: чтение UTF-8 файлов из
  каталога выгрузки с `errors="replace"` и сортированный `rglob(...)`
  по шаблону; ошибки файловой системы тоже заворачиваются в
  `PlatformError`.

Слой сознательно держится ниже tool-уровня: он ничего не знает про
конкретные инструменты — только про окружение, HTTP и dump-каталог.

## Чего здесь намеренно ещё нет

- реальной MCP-обвязки и транспорта;
- реальных сетевых/файловых проверок (все health-checks сейчас stub);
- реального взаимодействия с 1С, Apache, dump или индексом;
- инструментов чтения конфигурации и данных 1С — это появится в Phase 1.
