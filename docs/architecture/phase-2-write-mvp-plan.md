# Phase 2 Write MVP Plan

## Назначение фазы

В Phase 2 у платформы впервые появляется контролируемая возможность
менять тестовую инфобазу и её конфигурацию. До этой фазы агент умел
только читать; после этой фазы — умеет делать ограниченные,
аудируемые изменения с обязательным preflight и verify. Это
принципиальная граница доверия к платформе.

## Целевой результат

Рабочий `mcp-write-server`, который против тестовой 1С (та же
публикация и dump, что и у `mcp-read-server`) умеет:

- выполнять безопасные preflight-проверки и создавать snapshot-копии
  (backup файловой базы и dump конфигурации);
- совершать ограниченный набор write-операций над конфигурацией и
  кодом (создание общего модуля, обновление текста модуля,
  добавление реквизита справочника, применение конфигурации из
  файлов, обновление конфигурации базы);
- верифицировать результат каждого изменения отдельным инструментом;
- записывать аудит каждой write-операции через `onec-audit`;
- подсказывать, как откатить последнюю операцию.

Всё — через общий `ToolResult` envelope, через `REGISTERED_TOOLS` по
тем же shared helpers `mcp-common`, через `OperationContext` из
`mcp-common`. Реальный MCP-транспорт и production policy engine
остаются вне рамок Phase 2.

## Первый набор инструментов Phase 2

### A. Safety / preflight

- **`check_write_preconditions(environment, operation_intent)`** —
  агрегированный preflight: `allow_write=True`, живое окружение,
  наличие актуального dump, свободное место, сигнал
  `onec-policy-engine`.
  Слой: `onec-policy-engine` + `onec-health` + `onec-config`.
  Зачем: единая точка, после которой write-операция имеет право
  начаться. Ограничения: отказывает при любом `error` в health,
  при `allow_write=False`, при policy-deny.
- **`create_backup_snapshot(environment, label)`** — файловый
  snapshot инфобазы перед изменением.
  Слой: `onec-process-runner` + `onec-config`.
  Зачем: точка восстановления до write-операции. Ограничения:
  отказывает, если целевой каталог для snapshot'а недоступен или
  превышает лимит свободного места.
- **`create_dump_snapshot(environment, label)`** — `ConfigurationDump`
  конфигурации в выделенный каталог перед изменением кода/
  метаданных.
  Слой: `onec-process-runner` + `onec-config`.
  Зачем: чтобы сравнение до/после и rollback на уровне конфигурации
  имели основу. Ограничения: никогда не переписывает существующий
  snapshot.

### B. Controlled write operations

- **`apply_config_from_files(environment, source_dump_path)`** —
  `LoadConfigFromFiles` из указанного каталога выгрузки.
  Слой: `onec-process-runner` + `onec-policy-engine` + `onec-audit`.
  Зачем: базовый путь применения изменений метаданных/кода через
  файловую выгрузку. Ограничения: только из контролируемого пути
  под `environment.dump_path_root`, только при пройденном preflight.
- **`update_database_configuration(environment)`** —
  `UpdateDBCfg` после apply'я конфигурации.
  Слой: `onec-process-runner` + `onec-policy-engine` + `onec-audit`.
  Зачем: без этого изменения метаданных не применяются к live-базе.
  Ограничения: только при `allow_write=True` и свежем preflight;
  всегда аудируется.
- **`create_common_module(environment, module_name, initial_text="")`**
  — добавить новый `ОбщийМодуль` с заданным именем в dump + подать
  его на apply.
  Слой: dump-adapter + `onec-process-runner` + `onec-audit`.
  Зачем: первый целостный write-сценарий «добавить новый артефакт
  конфигурации». Ограничения: имя должно быть уникальным;
  `module_name` валидируется на допустимые символы.
- **`update_module_code(environment, module_relative_path, new_text)`**
  — обновить текст существующего модуля в dump + apply.
  Слой: dump-adapter + `onec-process-runner` + `onec-audit`.
  Зачем: базовый «поменять код функции» сценарий. Ограничения:
  файл должен существовать в dump; `new_text` не может быть
  пустым; guardrail против write-only символов вне BSL.
- **`add_catalog_attribute(environment, catalog_name, attribute_spec)`**
  — добавить реквизит в XML карточки справочника и подать на apply.
  Слой: dump-adapter + `onec-process-runner` + `onec-audit`.
  Зачем: первый целостный «изменить метаданные объекта» сценарий.
  Ограничения: `catalog_name` должен существовать; `attribute_spec`
  ограничен whitelist'ом типов и длин.

### C. Verification

- **`verify_metadata_change(environment, expectation)`** —
  пост-verify через existing live read-tools
  (`get_metadata_object`, `get_object_structure`), проверяет, что
  ожидаемое изменение действительно на живой базе.
  Слой: read-server runtime (вызывается из write-server как
  cross-app helper).
  Зачем: закрывает цикл apply → verify; без него write-операция
  не считается завершённой.
- **`verify_module_contains(environment, module_relative_path,
  expected_substring)`** — по dump проверяет, что нужный кусок
  кода реально попал в модуль.
  Слой: dump-adapter.
  Зачем: простая, быстрая проверка правки кода без live HTTP.
  Ограничения: substring-проверка, без regex (как и `search_code`).
- **`verify_object_exists(environment, object_name)`** — проверяет,
  что объект с таким полным именем действительно отдаётся live
  endpoint'ом и присутствует в dump.
  Слой: live-adapter + dump-adapter.
  Зачем: post-check после создания нового объекта.

### D. Audit / rollback-oriented support

- **`write_audit_record(environment, record)`** — явная запись
  события в журнал аудита через `onec-audit.format_audit_record`
  и write-server local store.
  Слой: `onec-audit` + локальное audit-хранилище write-server'а.
  Зачем: центральный механизм трассировки write-операций.
  Ограничения: запись идёт только append; read/rotate — не в MVP.
- **`describe_last_write_operation(environment)`** — вернуть
  последнюю запись аудита текущего окружения
  (`operation_id`, `tool_name`, `status`, `message`).
  Слой: audit store reader.
  Зачем: агент после ошибки должен уметь «посмотреть что
  последним делали». Ограничения: только последняя запись,
  только текущее окружение, никакого search.
- **`prepare_rollback_hint(environment, operation_id)`** —
  human-readable подсказка: какой snapshot/dump использовать и
  какой `apply_config_from_files` аргумент нужен, чтобы откатить
  данную операцию.
  Слой: audit store reader + `onec-config`.
  Зачем: минимальный помощник для ручного отката. Ограничения:
  **не выполняет** rollback автоматически — это за пределами MVP.

## Базовые guardrails Phase 2

- **Запрет записи в production по умолчанию.** Любое окружение
  трактуется как не-writable, пока явно не помечено
  `allow_write=True` в `EnvironmentConfig` и пока
  `onec-policy-engine` не подтвердил решение.
- **Write только при `allow_write=True`.** Этот флаг проверяется
  дважды: в `check_write_preconditions` и внутри каждого
  write-tool'а непосредственно перед запуском внешнего процесса.
- **Обязательный backup/dump перед изменением.** Для любой
  операции группы B перед её стартом должен существовать
  свежий backup (файловая копия) и актуальный dump конфигурации
  текущего окружения. Без этого `check_write_preconditions`
  отказывает.
- **Audit обязателен.** Любая успешная и неуспешная write-операция
  обязана породить `AuditRecord` через `write_audit_record`.
  Tool, который завершился без записи аудита, считается
  некорректно реализованным.
- **Verify после изменения обязателен.** После операции группы B
  должен быть вызван хотя бы один инструмент группы C. Write-tool
  не считается успешным, если соответствующий verify не прошёл.
- **Никакого silent apply.** Ни один write-tool не имеет права
  скрытно применять изменения: каждое действие отражается в
  `ToolResult.payload` (`pre_snapshot_ref`, `operation_id`,
  `verify_result`), чтобы снаружи было видно, что именно
  произошло.

## Порядок реализации

1. **`onec-policy-engine`: stub → реальный preflight слой.**
   Расширить `check_write_allowed(environment, intent)` до
   реальных правил (allow_write, environment kind, наличие
   свежих снимков) и ввести `PolicyDecision.reason_code`.
2. **`onec-audit`: подключение рабочего append-хранилища.**
   Добавить простой JSONL-store под `audit_dir` из окружения;
   `format_audit_record` и `AuditRecord` оставить как контракт.
3. **Skeleton `mcp-write-server.runtime`.** Аналогично
   `mcp_read_server.runtime`: `RuntimeContext`, `build_runtime_context`,
   при необходимости — write-specific helper'ы (но без adapters на
   отдельные бизнес-команды).
4. **Safety/preflight tools (группа A).** `check_write_preconditions`,
   `create_backup_snapshot`, `create_dump_snapshot`. Здесь впервые
   используется реальный `onec-process-runner` для `DumpIB` и
   копирования файловой базы.
5. **Backup/dump/apply/verify flow как внутренний helper.**
   Тонкая функция внутри write-server, которая запускает:
   preflight → snapshot → операция → verify → audit. Все
   write-tools группы B обязаны идти через неё.
6. **Write-tools группы B.** По одному: `apply_config_from_files`,
   `update_database_configuration`, `create_common_module`,
   `update_module_code`, `add_catalog_attribute`. Каждый tool
   проходит flow из шага 5.
7. **Verification tools (группа C).** `verify_metadata_change`,
   `verify_module_contains`, `verify_object_exists`. После этого
   цикл apply → verify замыкается.
8. **Audit / rollback support (группа D).** `write_audit_record`,
   `describe_last_write_operation`, `prepare_rollback_hint` поверх
   append-store из шага 2.
9. **Final integration pass.** Убедиться, что все B-инструменты
   идут строго через preflight → backup → apply → verify → audit;
   удалить любые «короткие пути», накопившиеся в процессе.

## Что не входит в Write MVP

- Массовые refactoring workflows (bulk rename, multi-object move).
- Сложная оркестрация миграций (поэтапные миграции данных,
  transactional cross-base operations).
- Intelligence-based auto-fix (правки кода/метаданных на основе
  анализа журнала ошибок).
- Multi-step autonomous write agents (агент, сам решающий цепочку
  write-операций без подтверждения человека).
- Production-grade rollback automation (автоматический откат по
  audit-записи без ручного вмешательства).

## Критерии приёмки Phase 2

- `mcp-write-server` реально подключается к тестовой базе через
  тот же адресный ряд, что и `mcp-read-server`.
- Все 3 инструмента группы A (safety/preflight) работают и
  корректно отсекают небезопасные сценарии
  (`allow_write=False`, нездоровое окружение, отсутствие свежих
  snapshot'ов).
- Хотя бы 3 инструмента группы B
  (`apply_config_from_files`, `update_module_code`,
  `create_common_module`) успешно выполняются на тестовой базе
  и проходят verify в единой схеме
  preflight → backup → apply → verify → audit.
- Все 3 verification tool'а возвращают `ToolResult(ok=True)` на
  корректных сценариях и `ok=False` на рассогласовании ожидания
  и реальности.
- Любая успешная или неуспешная write-операция оставляет
  `AuditRecord` в append-store;
  `describe_last_write_operation` действительно возвращает
  только что записанную запись.
- `prepare_rollback_hint` по `operation_id` возвращает
  согласованные `backup_ref` и `dump_ref`, на которые можно
  вручную откатиться.
- `dev-check` остаётся зелёным на каждом шаге.
- Read-server (15 tools Phase 1) не деградирует и продолжает
  работать; cross-app зависимость `verify_metadata_change` на
  read-runtime не ломает контракт read-server'а.
