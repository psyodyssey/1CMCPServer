# mcp-intelligence-server

Сервер платформы **1C Agent Platform**, отвечающий за **аналитику и
диагностику**: анализ поведения системы, журналов, зависимостей,
подсказки и troubleshooting. Этот сервер не изменяет систему, но помогает
агенту рассуждать о ней.

## Что сейчас внутри

Начиная с Phase 4 / Step 6 у сервера есть **четыре** группы public
intelligence-tools: A (dependency / reference analysis, Step 4),
C (diagnostics / troubleshooting, Step 5), B (impact / affected
scope, Step 6) и D (recommendations / planning, Step 6). Registry
содержит **шестнадцать** инструментов:

- `ping()` — liveness-маркер;
- **группа A — Step 4:**
  - `find_references_to_object(environment, object_name,
    max_matches=None)` — substring-скан `*.xml` и `*.bsl` дампа;
  - `find_module_method_usages(environment, method_name,
    max_matches=None)` — substring-скан только `*.bsl`, с
    presumed-классификацией declaration / usage;
  - `analyze_object_dependencies(environment, object_name)` —
    извлечение зависимостей объекта из его собственной XML-карточки
    (confirmed) и собственного BSL-модуля (presumed);
- **группа C — Step 5:**
  - `analyze_runtime_issue(environment)` — high-level aggregator
    поверх `check_runtime_health` + `diagnose_connectivity_issue`
    из read-server и runtime Step 3;
  - `analyze_event_log_patterns(environment, period_start=None,
    period_end=None, level=None, user=None)` — агрегация событий
    `get_event_log` в простые паттерны (топ уровней / пользователей
    / событий, error spike);
  - `diagnose_broken_form_binding(environment, object_name,
    form_name=None)` — диагностика broken binding'а формы:
    отсутствующие элементы / обработчики / методы;
  - `diagnose_missing_method_or_attribute(environment, *,
    object_name=None, module_relative_path=None, method_name=None,
    attribute_name=None)` — бинарный verdict «есть ли метод
    в модуле / атрибут в XML-карточке» с объяснением причины
    отсутствия;
- **группа B — Step 6:**
  - `estimate_change_impact(environment, object_name)` —
    компактная оценка масштаба изменения (счётчики ссылок +
    deterministic impact band);
  - `find_affected_forms(environment, object_name)` — формы,
    структурно завязанные на объект (path-эвристика
    `Forms/` / form / форма);
  - `find_affected_modules(environment, object_name)` — BSL
    модули, упоминающие объект (confirmed по `*.bsl` +
    presumed по `*.xml`);
  - `suggest_safe_change_order(environment, object_name)` —
    рекомендательный 6-шаговый план изменения (read-baseline
    → impact-сканы → preflight snapshots → metadata mutation
    → verify → audit/rollback hint);
- **группа D — Step 6:**
  - `suggest_fix_for_issue(environment, issue_code,
    context_data=None)` — rule-based рекомендация по 11
    типовым `issue_code` (gateway_down, dump_missing,
    handler_method_missing, …) с probable cause и списком
    реальных public tool'ов на следующий шаг;
  - `suggest_metadata_patch_plan(environment, target_kind,
    target_name, change_goal)` — упорядоченный список
    **существующих** write-tool'ов под цель; для
    `target_kind`-ов вне Phase 2/3 surface честно отдаёт
    пустой план + `presumed_findings`;
  - `summarize_configuration_risk(environment, object_name=None)`
    — короткое rule-based резюме риска (low/medium/high) на
    основе `health_codes` и количества ссылок;
  - `prepare_intelligence_report(environment, subject,
    include_tools=None)` — read-only orchestrator поверх
    whitelisted intelligence-tool'ов; собирает компактный
    payload с `sections`, `confirmed_findings`,
    `presumed_findings`, `recommended_checks`,
    `suggested_tools`.

Все public tools возвращают `ToolResult` (унифицированный конверт
из `mcp-common`). Registry и lookup — через `build_tool_registry`,
`list_registered_tools`, `get_registered_tool` из `mcp-common`.

## Чего здесь намеренно ещё нет

- реальной MCP-обвязки и транспорта;
- полноценного `build_dependency_subgraph` с настраиваемой глубиной
  и ограничениями размера (минимальный граф уже возвращает
  `analyze_object_dependencies`; impact-tools группы B опираются на
  тот же substring-фундамент, без отдельного subgraph BFS);
- реального AST-парсинга XML / BSL (MVP остаётся substring +
  regex + path-эвристика; в `find_affected_*` это особенно
  заметно — мы честно отделяем `confirmed_findings` от
  `presumed_findings`);
- кластеризации / ML-анализа event log (MVP — подсчёт повторов и
  простые spike-эвристики);
- настоящего topo-sort `suggest_safe_change_order` по графу
  зависимостей: возвращается фиксированный 6-шаговый template
  + impact-band; решение, какой именно write-tool из шага 4
  применять, остаётся за каллером.

## Public tools группы A (Phase 4 / Step 4)

Все три новых инструмента **строго read-only**: не пишут файлы, не
трогают инфобазу, не вызывают `run_write_flow`, не создают
snapshot'ов, не пишут audit и не импортируют `onec_policy_engine`.
Исключения из runtime-слоя (отсутствующий dump-root, пустой
`needle`, ошибка чтения файла) перехватываются внутри инструмента и
конвертируются в `ok=False` — наружу не пробрасываются.

В payload каждого инструмента confirmed-данные явно отделены от
presumed-данных:

- **confirmed** — факты, извлечённые напрямую из конкретного
  файла (подстрочное совпадение в конкретной строке, токен из
  XML-карточки).
- **presumed** — эвристические выводы (например, классификация
  `declaration` vs `usage` по шаблону `Процедура <name>(`;
  зависимости, извлечённые из BSL-модуля, где токен может быть
  в комментарии или строковом литерале).

Failure-style един: `ok=False` **только** при реальной проблеме
(dump-root недоступен, объект не найден в дампе, пустой аргумент).
Пустой-но-валидный результат поиска (нет совпадений) — это
`ok=True` с пустым списком и честным message «No references found».

### `find_references_to_object(environment, object_name, max_matches=None)`

Substring-скан `*.xml` + `*.bsl` под `environment.dump_path`.
Payload: `object_name`, `total_matches`, `confirmed_matches` (список
`{relative_path, source, line_number, preview}`), `confirmed_sources`
(уникальные пути), `sources_used` (`dump_xml` / `dump_bsl`),
`max_matches_applied`. `runtime.health_codes` — как у остальных
инструментов.

### `find_module_method_usages(environment, method_name, max_matches=None)`

Substring-скан только `*.bsl`. Дополнительно эвристически разделяет
совпадения на `presumed_declarations` (строка-объявление
`Процедура/Функция/Procedure/Function <name>(`) и `presumed_usages`
(все остальные совпадения). `confirmed_matches` содержит все
находки без фильтрации; классификация — отдельные списки.

### `analyze_object_dependencies(environment, object_name)`

Локализует XML-карточку объекта (файл с совпадающим stem) и его
собственные BSL-модули (путь содержит `simple_name` как сегмент).
Извлекает из каждого known-prefix ссылки вида `Справочник.Foo`,
`CommonModule.Bar` и т.д. Self-references отфильтрованы.

- `confirmed_dependencies` — токены из XML-карточки: XML-структура
  несёт высокий сигнал, `<Type>` / `<Reference>` — явные ссылки.
- `presumed_dependencies` — токены из BSL-модуля: могут быть в
  комментариях / строковых литералах, поэтому surfaces как
  эвристика.

В payload дополнительно возвращается минимальный `graph` с
`nodes`, `edges` и `adjacency` — пригоден как основа для будущих
impact-tools группы B.

Если объект не найден нигде в дампе (нет XML-карточки и нет
BSL-модуля) — `ok=False`, честный fail-closed.

## Public tools группы C (Phase 4 / Step 5)

Diagnostics / troubleshooting. Те же контрактные инварианты, что и
у группы A: **строго read-only** (ничего не пишут, не идут через
`run_write_flow`, не создают snapshot'ов, не пишут audit и не
импортируют `onec_policy_engine`). Все исключения runtime-слоя и
cross-app вызовов перехватываются и превращаются либо в
`ok=False`, либо в findings.

Единый failure-style:

- `ok=True` — анализ завершён (findings могут быть пустыми).
- `ok=False` — анализ провести не удалось (некорректный вход,
  критическая зависимость вернула ошибку, dump/модуль недоступен
  там, где он критически нужен).

`confirmed_findings` — факты, которые можно связать с конкретным
артефактом (health-код из `check_runtime_health`, verdict
`method_exists`/`method_missing` поверх реально прочитанного
модуля, handler, на который в форме есть явная привязка).
`presumed_findings` — эвристическое объяснение: probable cause,
pattern-метка.

### `analyze_runtime_issue(environment)`

High-level aggregator поверх read-server диагностики.
`check_runtime_health` + `diagnose_connectivity_issue` + intelligence
runtime Step 3. Каждый non-`ok` health-код превращается в
`confirmed_findings` с детерминированным hint (`gateway_down`,
`dump_missing`, `index_lock`). Rule-based интерпретация
`diagnose_connectivity_issue` идёт в `presumed_findings`. Raw
per-check snapshot — в `health_checks`. `recommended_checks` —
короткие next-step'ы под каждый код. Сам по себе runtime никогда
не трогается — только уже собранная картина. `ok=True` при любом
состоянии здоровья; `ok=False` только при отсутствующем
`environment` или внутренней ошибке.

### `analyze_event_log_patterns(environment, period_start=None, period_end=None, level=None, user=None)`

Делегирует в `read.get_event_log` (который сам ходит в live HTTP
через `urllib`). Фильтры пробрасываются как есть. Если read-server
вернул `ok=False` — tool fail-closed'ится с тем же message.
Успешно полученные entries группируются через
`collections.Counter`:

- `confirmed_findings.total_entries`,
- `top_levels` / `top_users` / `top_events` (top-N),
- `error_samples` (первые 5 error/critical записей).

`presumed_findings` добавляет pattern `error_spike`, если набралось
≥ 2 error/critical записей. Никакой ML, никакой кластеризации —
честный подсчёт повторов.

### `diagnose_broken_form_binding(environment, object_name, form_name=None)`

`read.get_form_structure` (live HTTP) → ожидаемая форма полезной
нагрузки: `{"elements": [...], "handlers": [{"event": ...,
"handler_method": ...}], "module_relative_path": "..."}`. Если
endpoint/форма недоступны — `ok=False` с пояснением.

Когда форма получена, tool собирает:

- `confirmed_findings` — `form_has_no_elements`,
  `form_has_no_handlers`, `handler_method_missing`,
  `module_not_readable`. Каждый содержит source, на который
  опирается verdict.
- `presumed_findings` — вероятная причина для каждого symptom'а
  (переименован/удалён, stale binding, dump устарел).

Для проверки handler method используется **pure read-only helper**
`mcp_write_server.runtime.metadata_ops.module_contains_method`
(кейс allowed cross-app направления `intelligence → write` через
pure helpers). Если module_relative_path указан, но файл не
читается — tool честно помечает module_not_readable и
рекомендует re-generate dump.

### `diagnose_missing_method_or_attribute(environment, *, object_name=None, module_relative_path=None, method_name=None, attribute_name=None)`

Два режима, комбинируемые:

- **Method mode** — `module_relative_path` + `method_name`. Модуль
  читается из дампа, проверяется `module_contains_method` (тот же
  pure helper write-runtime). Verdicts: `method_exists` /
  `method_missing` / `module_file_missing`.
- **Attribute mode** — `object_name` + `attribute_name`. XML-карточка
  ищется по совпадению stem'а с simple-name. Над ней — regex поверх
  типовых `<Attribute>` форм (`name="..."` и вложенный `<Name>`).
  Verdicts: `attribute_exists` / `attribute_missing` /
  `xml_card_missing`.

Если не передан ни один валидный mode → `ok=False, invalid_input`.
Если dump-root недоступен → `ok=False`. Во всех остальных случаях
`ok=True` с verdicts в `confirmed_findings` и probable-cause narrative
в `presumed_findings` (только для *missing*-verdict'ов).

## Public tools группы B (Phase 4 / Step 6)

Impact / affected scope. Те же контрактные инварианты, что и у
групп A и C: **строго read-only**, без `run_write_flow`, без
audit, без `onec_policy_engine`. Все исключения runtime/cross-app
вызовов перехватываются и превращаются в `ToolResult(ok=False, ...)`
либо в findings.

`confirmed_findings` — точные счётчики ссылок и пути из dump-сканов;
`presumed_findings` — эвристические выводы (impact band,
form-path heuristic, weak signals). `suggested_tools` /
`suggested_write_tools` ссылаются **только** на уже
зарегистрированные public-tool'ы read-/write-/intelligence-server'ов
(см. `_WRITE_TOOL_DESCRIPTIONS` в `tools.py` для полного списка
известных имён).

### `estimate_change_impact(environment, object_name)`

Композиция `find_references` + `list_xml_files` + `list_bsl_files`
из runtime Step 3.

- `confirmed_findings`: `reference_count`, `xml_references`,
  `bsl_references`, `own_xml_cards`, `own_bsl_modules`,
  `simple_name`, `referenced_paths`.
- `presumed_findings`: всегда содержит pattern `impact_estimate`
  с `impact_level` ∈ {none, low, medium, high} (deterministic
  thresholds 0/5/20). Дополнительно: `module_impact_possible`
  если есть BSL hits, `form_impact_possible` если хоть один
  путь похож на форму.
- `suggested_tools`: `find_references_to_object`,
  `analyze_object_dependencies`, `find_affected_forms`,
  `find_affected_modules`.
- Empty `object_name` или отсутствующий dump_root → `ok=False`.
  «0 ссылок» — `ok=True` с `level=none`.

### `find_affected_forms(environment, object_name)`

`find_references` + path-эвристика `_is_form_path` (наличие
сегмента `Forms`, либо `form` / `форма` в stem).

- `confirmed_findings`: матчи в form-подобных путях.
- `presumed_findings`: остальные матчи с pattern
  `weak_form_signal` и пояснением, что объект упомянут в
  не-form-артефакте, но это может быть metadata-XML, который
  ссылается на форму.
- `suggested_tools`: `diagnose_broken_form_binding`,
  `find_references_to_object`.

### `find_affected_modules(environment, object_name)`

`find_references` + разбивка по `source`.

- `confirmed_findings`: каждый матч в `*.bsl` (любой `.bsl` —
  это по определению модуль).
- `module_summary`: per-module `match_count`, отсортирован по
  убыванию.
- `presumed_findings`: матчи в `*.xml` с pattern
  `module_signal_via_xml`.
- `suggested_tools`: `find_module_method_usages`,
  `find_references_to_object`.

### `suggest_safe_change_order(environment, object_name)`

Рекомендательный orchestrator. Дёргает `analyze_object_dependencies`
и `estimate_change_impact` (read-only, без побочных эффектов) и
возвращает фиксированный 6-шаговый `recommended_sequence`:

1. read-baseline (`get_object_structure`);
2. impact / dependency сканы (`analyze_object_dependencies`,
   `find_references_to_object`, `estimate_change_impact`,
   `find_affected_forms`, `find_affected_modules`);
3. preflight snapshots (`check_write_preconditions`,
   `create_backup_snapshot`, `create_dump_snapshot`);
4. metadata mutation — pick один из реальных write-tool'ов:
   `create_catalog`, `add_catalog_attribute`,
   `add_document_attribute`, `create_managed_form`,
   `add_form_element`, `append_module_method`,
   `replace_module_method_body`;
5. verification (`verify_metadata_change`,
   `verify_attribute_exists`, `verify_module_contains`,
   `verify_object_exists`, `diff_dump_fragment`,
   `get_object_structure`, `get_form_structure`);
6. audit / rollback hint (`describe_last_write_operation`,
   `prepare_rollback_hint`).

`presumed_findings` адаптируется под состояние: `cascade_risk`
если есть зависимости, `object_not_in_dump` если объект не
найден (sequence отдаётся как generic template),
`high_blast_radius` для `impact_level=high`. Никаких
авто-выполнений — это рекомендация для каллера.

## Public tools группы D (Phase 4 / Step 6)

Recommendations / planning / summarization. Те же read-only
инварианты. `suggested_tools` / `suggested_write_tools` —
**только реальные** имена существующих public-инструментов;
будущие capability помечаются как отсутствующие через
`presumed_findings` (а не выдумываются).

### `suggest_fix_for_issue(environment, issue_code, context_data=None)`

Rule-based mapping `_ISSUE_FIX_RULES`. Поддерживаемые
`issue_code`: `gateway_down`, `dump_missing`, `index_lock`,
`form_has_no_elements`, `form_has_no_handlers`,
`handler_method_missing`, `method_missing`,
`module_file_missing`, `attribute_missing`, `xml_card_missing`,
`error_spike`.

Каждый recipe содержит `probable_cause` (→ `presumed_findings`),
упорядоченные `steps` (→ `recommended_checks`),
`suggested_tools` и `suggested_write_tools` — список реальных
public tool names. `context_data` пробрасывается verbatim в
`confirmed_findings` (MVP не параметризует recipe по контексту).

Unknown `issue_code` → **fail-closed** через `ok=False` с
сообщением `Unknown issue_code '...'. Known codes: [...]`.

### `suggest_metadata_patch_plan(environment, target_kind, target_name, change_goal)`

Table-driven plan generator. Поддерживаемые `target_kind`:
`catalog`, `common_module`, `catalog_attribute`,
`document_attribute`, `managed_form`, `form_element`,
`module_method`, `module_method_body`. Каждый recipe — упорядоченный
список реальных write-tool'ов: preconditions → backup →
dump snapshot → metadata mutation → (опционально)
`update_database_configuration` → verify.

Honest unsupported-pattern (никаких выдуманных tool'ов):

- `target_kind` ∈ {`document`, `information_register`, `role`,
  `report`, `data_processor`} → `ok=True`, пустой план,
  `presumed_findings=[{pattern: kind_unsupported, ...}]`;
- неизвестный kind → `ok=True`, `unknown_kind`;
- `change_goal` содержит ключевые слова удаления (`delete`,
  `remove`, `drop`, `удалить`, `удалять`, `убрать`) →
  `ok=True`, `deletion_not_supported` (write-server
  Phase 2/3 не имеет `delete_*` tool'ов).

`recommended_sequence` строится из recipe через
`_step_description(...)` — короткие пояснения каждого
write-tool из `_WRITE_TOOL_DESCRIPTIONS`.

### `summarize_configuration_risk(environment, object_name=None)`

Короткое rule-based резюме риска. Глобальный режим
(`object_name is None`) опирается только на
`runtime.health_codes`: `dump_missing` → high, `gateway_down`
или `index_lock` → medium, иначе low.

Пер-объектный режим дополнительно вызывает `find_references` и
добавляет `reference_count` в `confirmed_findings`. Правила:

- `dump_missing` → high (доминирует);
- `gateway_down` или `index_lock` → medium (доминирует);
- иначе по `reference_count`: > 20 → medium, иначе low;
- 0 ссылок → low + `presumed_findings` с
  `object_not_referenced` («либо изолированный, либо
  misspelled»).

`risk_level` всегда возвращается в верхнем уровне payload, и
дополнительно в `presumed_findings` как pattern `risk_summary`
с reasoning. Никаких категоричных утверждений — только
правила.

### `prepare_intelligence_report(environment, subject, include_tools=None)`

Read-only orchestrator над whitelisted сабсетом
intelligence-tool'ов (`_REPORT_KNOWN_TOOLS`):
`analyze_runtime_issue`, `analyze_event_log_patterns`,
`analyze_object_dependencies`, `find_references_to_object`,
`find_module_method_usages`, `estimate_change_impact`,
`find_affected_forms`, `find_affected_modules`,
`summarize_configuration_risk`. Имена вне whitelist падают в
`skipped_unknown_tools`.

Дефолтный набор (`include_tools is None`):
`(analyze_runtime_issue, analyze_object_dependencies,
estimate_change_impact, summarize_configuration_risk)`.

Каждый sub-tool вызывается с `subject` через таблицу режимов
(`no_subject`, `subject_as_object_name`,
`subject_as_method_name`, `subject_as_object_name_optional`).
Sub-tool, бросивший исключение, превращается в
`sections[name]={ok:False, message,...}` — наружу никогда не
пробрасывается.

Aggregate в payload: `sections`, `confirmed_findings`,
`presumed_findings`, `recommended_checks`, `suggested_tools`
(set, отсортирован), каждый item помечен своим `tool` для
трассируемости. Empty `subject` → `ok=False`. Этот tool
**ничего не пишет на диск**, не создаёт временных файлов и не
вызывает `run_write_flow`.

## Internal runtime helper layer (Phase 4 / Step 3)

Подпакет
`apps/mcp-intelligence-server/src/mcp_intelligence_server/runtime/`
— **внутренний** helper-слой, на котором будут стоять будущие
public intelligence-tools Step 4–6. Это **не** public tools:
`ToolResult` здесь не возвращается, в `server.REGISTERED_TOOLS`
ничего не регистрируется.

Состав:

- `models.py` — `IntelligenceRuntimeContext(environment,
  health_results, health_codes, dump_root)`. Data snapshot окружения
  и его health-состояния для одного вызова intelligence-инструмента.
- `context.py` — `build_runtime_context(environment)`: собирает
  `check_environment_health(...) + summarize_health(...)` из
  `onec-health`, резолвит `dump_root = Path(environment.dump_path)`,
  на диск не пишет и `onec_policy_engine` не трогает.
- `dump_scanner.py` — тонкие intelligence-ориентированные обёртки
  над `mcp_read_server.runtime`: `list_xml_files`, `list_bsl_files`,
  `list_files_by_extensions`, `read_utf8_text`. Существуют, чтобы
  intelligence-helper'ы вызывали осмысленно-именованный API, а не
  generic read-server примитивы напрямую.
- `reference_finder.py` — substring поиск по `*.xml` и `*.bsl`
  дампа: `find_references(dump_root, needle, extensions=...,
  max_matches=...)` возвращает `list[ReferenceMatch]`
  (`relative_path`, `source`, `line_number`, `preview`); пустой
  `needle` fail-closed через `ValueError`. Вспомогательный
  `count_references` — счётчик без хранения совпадений.
- `graph.py` — минимальный каркас dependency-графа:
  `DependencyNode`, `DependencyEdge`, `DependencyGraph`,
  `empty_graph`, `add_node`, `add_edge`, `neighbors`. Идемпотентные
  `add_node` / `add_edge` + adjacency map. Это именно маленький
  честный фундамент; реальный subgraph-обход с ограничением глубины
  появится в Step 4+ в public tool `build_dependency_subgraph`.

Cross-app import этого подпакета — **строго вперёд**:
`intelligence → read` (напрямую через `mcp_read_server.runtime`) и
`intelligence → write` только через pure / read-only helpers (на
Step 3 такие импорты ещё не нужны). `onec_policy_engine` не
импортируется.

## Read-only контракт Phase 4

Начиная с Phase 4, intelligence-server строго **read-only**:

- не пишет файлы, не трогает инфобазу, не вызывает
  `run_write_flow`, не создаёт snapshot'ов и не пишет audit. Любые
  правки остаются за `mcp-write-server`.
- **не проходит** через `onec_policy_engine.check_write_allowed`.
  Пакет `mcp_intelligence_server` намеренно **не импортирует**
  `onec_policy_engine`. Это повторяет существующий паттерн
  `mcp-read-server` (read-side тоже не роутится через
  write-policy) и держит поверхность write-policy узкой —
  движок решает **write**, не read.
- allowed cross-app import — **только вперёд**:
  `intelligence → read` (напр. `mcp_read_server.runtime.*`) и
  `intelligence → write` через pure / read-only helpers
  (напр. `mcp_write_server.runtime.metadata_ops.module_contains_method`
  без побочных эффектов). Обратное направление запрещено, чтобы
  read/write оставались независимыми и без циклов.
- fail-closed при недостатке данных: если dump-файл, XML-блок
  или live-endpoint недоступны, tool возвращает
  `ToolResult(ok=False, ...)` с понятным reason, а не догадку.

Contract detail: если intelligence-operation name когда-нибудь
случайно попадёт в `WriteIntent` и будет проверен на write-стороне,
`onec-policy-engine` честно вернёт `unknown_intent` (fail-closed).
Это страховка, а не штатный путь.
