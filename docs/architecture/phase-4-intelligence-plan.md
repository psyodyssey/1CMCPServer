# Phase 4 Intelligence Plan

## Назначение фазы

Phase 0–3 дали платформе read/write foundation: `mcp-read-server`
умеет собрать конфигурацию, метаданные, код и журналы (15 tools);
`mcp-write-server` умеет вносить ограниченные и аудируемые
изменения (23 tools), в том числе metadata-level правки. До сих пор
`mcp-intelligence-server` оставался skeleton-сервером с одним `ping`.

Phase 4 превращает его в рабочий **intelligence layer** поверх уже
существующего read/write фундамента. Смысл фазы — **не «магический
reasoning engine»**, а набор осмысленных, **read-only** инструментов,
которые помогают агенту рассуждать о конфигурации:

- где используется конкретный объект, метод или реквизит;
- какие формы и модули затронет предстоящее изменение;
- какая последовательность изменений безопаснее;
- что, вероятно, сломалось по журналу регистрации и структуре;
- какую подсказку дать пользователю до применения правки;
- где в конфигурации подозрительные места или очевидные риски.

Phase 4 не создаёт новых write-операций и не принимает решений от
имени пользователя. Она собирает и интерпретирует то, что уже
доступно через read- и write-helper-слои.

## Целевой результат

К моменту закрытия Phase 4:

- `mcp-intelligence-server` становится содержательным сервером.
  У него появляется собственный `runtime` слой для анализа
  dump/metadata и набор public tools, покрывающих dependency
  analysis, impact analysis, troubleshooting и recommendations.
- Все intelligence-tools **read-only** и никогда не запускают
  write-flow. Любые правки остаются прерогативой write-server'а.
- Cross-app import идёт строго в сторону `intelligence → read` и
  `intelligence → write` (только read-only / pure helpers).
  Обратное направление запрещено, чтобы read/write остались
  независимыми и без циклов импорта.
- Agent получает ответ в форме осмысленного структурированного
  `ToolResult`: поля для confirmed-фактов, поля для presumed-
  гипотез, явные источники данных (dump path, live endpoint,
  event log). Никакого скрытого reasoning — прослеживаемая
  цепочка.
- Phase 1 read-tools и Phase 2–3 write-tools продолжают работать
  без деградации. `dev-check` остаётся зелёным на каждом шаге.

## Набор инструментов фазы

Ниже — предлагаемый стартовый набор. Конкретные сигнатуры и
форма payload уточняются в Step 1 (intelligence operation
contract) и при необходимости пересматриваются в Step 2. Это план
фазы, а не декларация готового продукта.

### A. Dependency / structure analysis

Read-only инструменты, которые ищут связи внутри dump и через
live-адаптер read-server.

- **`analyze_object_dependencies(environment, object_name)`** —
  перечислить объекты и модули, на которые ссылается заданный
  объект (через XML-карточки и BSL-текст).
  Слой: read-side dump adapter + intelligence runtime.
  MVP: список `relative_path` + `source` (`xml` / `bsl`) +
  короткий preview.
- **`build_dependency_subgraph(environment, root_object_name,
  depth=1)`** — ограниченный подграф зависимостей вокруг
  корневого объекта.
  Слой: intelligence runtime поверх `analyze_object_dependencies`.
  MVP: словарь `nodes`/`edges` с жёстким лимитом глубины (по
  умолчанию 1–2) и ограничением размера.
- **`find_references_to_object(environment, object_name)`** —
  обратный поиск: кто ссылается на заданный объект. Substring-
  поиск по dump XML и BSL.
  Слой: read-side dump / search helpers + intelligence filter.
  MVP: список match'ей с `relative_path`, `source`, коротким
  preview.
- **`find_module_method_usages(environment, module_relative_path,
  method_name)`** — где вызывают заданный метод модуля.
  Слой: read-side dump + lightweight BSL regex (те же принципы,
  что у `module_contains_method` из Phase 3 helper layer).
  MVP: список `matches` (`relative_path`, `preview`).

### B. Change impact / pre-change intelligence

Preflight-уровень. Инструменты только наблюдают, не запускают
write-flow и не имеют права его провоцировать.

- **`estimate_change_impact(environment, intent)`** — по
  предполагаемому `WriteIntent` оценить радиус потенциальных
  эффектов. Использует `build_dependency_subgraph` +
  `find_references_to_object`.
  MVP: общий счётчик затронутых артефактов + список «горячих»
  связей с их типами.
- **`find_affected_forms(environment, object_name)`** — какие
  формы привязаны к объекту или его модулям.
  Слой: `get_object_structure` / `get_form_structure` из
  read-server + intelligence aggregation.
  MVP: список форм с коротким описанием связи
  (attribute / handler / representation).
- **`find_affected_modules(environment, object_name)`** — какие
  модули упоминают объект (как ссылку по имени или через API).
  Слой: dump scanner + lightweight BSL scanner.
  MVP: список `module_relative_path` + `match_count`.
- **`suggest_safe_change_order(environment, intents)`** — по
  списку планируемых `WriteIntent`-ов предложить безопасный
  порядок их применения (сначала создать объект, затем реквизит,
  затем форму и т.д.).
  MVP: упорядоченный список с пояснением, почему именно такой
  порядок.

### C. Troubleshooting / diagnostics

Работа «после факта»: агент знает, что-то идёт не так, и хочет
понять, что именно.

- **`analyze_runtime_issue(environment, symptom)`** — общая
  точка входа диагностики. `symptom` описывает наблюдаемую
  проблему (строка или структура).
  Слой: intelligence + cross-app read (`check_runtime_health`,
  `diagnose_connectivity_issue` из read-server).
  MVP: простая rule-based интерпретация → `problem_code`,
  `probable_cause`, `next_step`, `sources`.
- **`analyze_event_log_patterns(environment, period_filters)`** —
  агрегировать события из `get_event_log` в простые паттерны:
  топ событий, топ пользователей, топ уровней ошибок.
  Слой: read-server `get_event_log` + intelligence aggregation.
  MVP: счётчики + 3–5 репрезентативных примеров + окно времени.
- **`diagnose_broken_form_binding(environment, object_name,
  form_name)`** — проверить, что обработчики формы ссылаются на
  реально существующие методы модуля.
  Слой: `get_form_structure` + `module_contains_method` (pure
  helper из write-runtime).
  MVP: список привязок + статус каждой
  (`linked` / `missing_method` / `unknown`).
- **`diagnose_missing_method_or_attribute(environment,
  expectation)`** — вариация `verify_metadata_shape`, но с
  диагностической подачей: не просто `True`/`False`, а
  объяснение причины отсутствия (нет файла, файл есть но нет
  блока, блок есть но нет ожидаемого имени).
  MVP: `reason_code` из маленького фиксированного набора +
  `details` с путями / блоками.

### D. Recommendation / assistant layer

Выход к пользователю. Все рекомендации — подсказки, а не команды.

- **`suggest_fix_for_issue(environment, issue)`** — по
  обнаруженной проблеме (типично — результат tool'а группы C)
  сформировать один или несколько human-readable шагов починки.
  Intelligence их **не выполняет**.
  MVP: текстовые `hints` + `suggested_tools` — имена существующих
  public инструментов write-server (Phase 2/3) с набросками
  аргументов. Несуществующих tool имён в списке быть не должно.
- **`suggest_metadata_patch_plan(environment, goal)`** — по
  пользовательской цели (описание словами или структурированная
  спецификация) сформировать план из `WriteIntent`-ов в
  безопасном порядке.
  MVP: упорядоченный список `intents` + краткое пояснение к
  каждому шагу + почему такой порядок.
- **`summarize_configuration_risk(environment)`** — обзорное
  резюме подозрительных мест: пустые модули, дубликаты имён,
  объекты без форм, модули без экспортов и т. п.
  MVP: несколько простых rule-check'ов + короткий совет по
  каждой найденной проблеме.
- **`prepare_intelligence_report(environment, scope)`** —
  общий отчётный tool: агрегирует результаты выбранного набора
  intelligence-инструментов в единый читаемый payload.
  MVP: `sections` (по одному на вид анализа) + `summary`.

## Guardrails фазы

- **Intelligence-tools ничего не меняют.** Не существует
  intelligence-операции, которая пишет на диск, в audit, в live
  endpoint или где-либо ещё в состоянии системы. Любые правки
  идут только через write-server; Phase 4 его не трогает.
- **Read-only by construction.** Все public intelligence-tools
  возвращают `ToolResult` с данными и/или подсказками. Никаких
  snapshot'ов, никакого `run_write_flow`, никакого audit:
  audit — это след изменений, а intelligence изменений не делает.
- **Cross-app import — только вперёд.** Разрешено:
  `intelligence → read` (напр. `mcp_read_server.runtime.*`) и
  `intelligence → write` через **pure / read-only** helpers
  (напр. `mcp_write_server.runtime.metadata_ops.module_contains_method`
  без побочных эффектов). **Запрещено** обратное: ни
  read-server, ни write-server не должны импортировать из
  intelligence. Это сохраняет их независимость и исключает циклы.
- **Fail-closed при недостатке данных.** Если для ответа
  недостаточно dump-файла, XML-блока или доступа к live-endpoint'у,
  tool возвращает `ToolResult(ok=False, ...)` с понятным reason, а
  не догадку. Никаких silent-default'ов.
- **Честные отчёты.** В каждом payload должно быть видно, что
  получено из прямых данных (dump substring, XML tag, event-log
  row) и что — presumed inference. Отдельные поля
  `confirmed` / `presumed` или эквивалентные маркеры источника.
- **Рекомендации ≠ авто-применение.** `suggest_*` tools отдают
  советы и (где уместно) `suggested_tools` — список имён
  существующих public write-tool'ов с набросками аргументов. Сам
  запуск этих инструментов остаётся ответственностью вызывающего
  кода или человека.
- **Производительность дешевле точности в MVP.** Допустимы
  substring-поиск, `rglob`, lightweight BSL-regex (как в Phase 3
  helper layer). Полноценные AST, индексы или graph databases —
  за рамками Phase 4.

## Что не входит в эту фазу

- **Fully autonomous self-healing.** Intelligence не чинит
  конфигурацию сама по себе.
- **Auto-apply fixes.** Даже когда `suggest_fix_for_issue` назвал
  конкретный write-tool, запуск — не автоматический.
- **Production decision making.** Phase 4 продолжает опираться
  на prod-block guardrails Phase 2/3; intelligence не
  «переубеждает» policy engine.
- **Multi-agent orchestration.** Никаких цепочек агентов,
  делегирующих работу друг другу.
- **Настоящий reasoning engine / ML-модели.** Все эвристики —
  rule-based и прозрачные, с явно названными источниками.
- **Product workflows Phase 5.** Сценарии для конечных
  пользователей поверх платформы — не тема Phase 4.
- **Замена stub'ов Phase 2/3** (`apply_config_from_files`,
  `update_database_configuration`, `create_dump_snapshot`) на
  настоящий `1cv8`-integration — параллельный follow-up, не
  блокирующий Phase 4.

## Критерии приёмки

Phase 4 считается закрытой, когда:

- реализованы и зарегистрированы **не менее 4–5** public
  intelligence-tools, покрывающих хотя бы **две** группы из
  A / B / C / D;
- имеется **не менее 2–3** рабочих troubleshooting-сценариев
  (например, broken form binding, missing attribute, event-log
  spike);
- подтверждён **хотя бы один end-to-end intelligence scenario**
  (например, запросил зависимости → оценил impact → получил
  рекомендованный порядок правок → сформировал intelligence
  report);
- `dev-check` остаётся зелёным на каждом шаге;
- `mcp-read-server` (15 tools) и `mcp-write-server` (23 tools)
  **не деградировали**;
- каждый intelligence-tool честно маркирует `confirmed` vs
  `presumed` в payload.
