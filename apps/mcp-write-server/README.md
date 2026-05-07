# mcp-write-server

Сервер платформы **1C Agent Platform**, отвечающий за **операции записи**:
изменение конфигурации, объектов, кода и данных инфобазы. Все действия
этого сервера в перспективе проходят через политики безопасности и аудит.

## Что сейчас внутри

На текущем этапе здесь только **skeleton server bootstrap** — без реальной
write-логики. Реализовано:

- `ToolResult` — стандартный конверт ответа инструмента
  (`ok`, `tool_name`, `message`, `payload`);
- инструмент `ping()` — liveness-маркер сервера;
- server registry skeleton: `REGISTERED_TOOLS`, `list_tools()`, `get_tool(name)`.

Registry и response envelope унифицированы через `mcp-common` (`ToolResult`,
`build_tool_registry`, `list_registered_tools`, `get_registered_tool`).

## Safety / preflight tools (Phase 2 / Step 5)

Первая группа реальных write-side инструментов. Все они поверх
`runtime` слоя: собирают `WriteRuntimeContext`, обязательно проходят
через `require_write_preconditions(...)`, и на ошибке возвращают
`ToolResult(ok=False, ...)` вместо того, чтобы ронять исключение:

- **`check_write_preconditions(environment, intent)`** — тонкая
  tool-обёртка над runtime guard. При успехе — `ok=True`,
  `message="Write preconditions satisfied."`; при
  `PolicyDeniedError` / `HealthCheckError` — `ok=False` с
  оригинальным текстом причины. `payload.runtime` содержит
  `health_codes`, `policy.{allowed, reason_code, require_snapshots}`,
  `data.audit_dir`.
- **`create_backup_snapshot(environment, label)`** — **реальный**
  файловый snapshot базы через `shutil.copytree(environment.base_path,
  <base_path.parent>/_snapshots/backup-<base_id>-<safe_label>)`.
  `safe_label` — санитизация до ascii-букв/цифр/`-_`; пустой
  результат подставляется как `"snapshot"`. Если целевой snapshot
  уже существует, tool возвращает `ok=False` без перезаписи.
- **`create_dump_snapshot(environment, label)`** — два режима,
  выбираемые по конфигу окружения, **внешний контракт
  (`ToolResult`) одинаков**:
  - **stub mode** (Phase 2 / Step 5 default; backward-compat с
    Phase 1–5). Включён, если **хотя бы одно** из
    `environment.onec_binary_path` /
    `environment.onec_dumpcfg_command_template` не задано. Tool
    создаёт каталог
    `<dump_path.parent>/_snapshots/dump-<base_id>-<safe_label>`,
    запускает через `onec_process_runner.run_process` маленький
    Python-процесс с маркером `dump-created.txt`, и пишет
    `dump-meta.json`. `payload.data.mode = "stub"`,
    `payload.data.binary_invoked = False`. Это **не** настоящий
    1cv8 DumpCfg — это честная связка preflight + process runner
    + snapshot path, которая остаётся как fallback пока operator
    не сконфигурирует binary-backed путь.
  - **binary-backed mode** (Phase 6 / Step 2). Включён, если
    **оба** поля заданы. Tool рендерит operator-declared
    `onec_dumpcfg_command_template` через whitelisted-placeholder
    substitution (доступны: `{binary_path}`, `{output_path}`,
    `{base_path}`, `{base_id}`, `{publication_name}`,
    `{http_base_url}`), запускает реальный subprocess через
    `onec_process_runner.run_process` с timeout 300 секунд,
    captured stdout/stderr (excerpts cap 1024 символа). Operator
    сам выбирает grammar 1cv8 CLI — write-server **не угадывает**
    флаги. `payload.data.mode = "binary-backed"`,
    `payload.data.binary_invoked = True/False` (False только
    если был отказ в render'е placeholder'ов или при стартовой
    ошибке subprocess'а). Дополнительно: `command_preview`
    (рендерённый argv), `exit_code`, `stdout_excerpt`,
    `stderr_excerpt`. `dump-meta.json` в этом режиме помечается
    `mode: "binary-backed"`.
  - **Fallback discipline.** Между режимами есть **только
    config-time fallback**: если контракт не полный (одно из
    полей отсутствует) — tool работает в stub mode. **Runtime
    fallback запрещён**: если binary-backed subprocess вернул
    non-zero, tool возвращает `ok=False` с сохранённым
    `mode = "binary-backed"`; никакого silent-перезапуска stub
    после реального failure'а нет.
  - **Где это используется.** Все mutating-tools, которые внутри
    проходят `run_write_flow`, при `policy_decision.require_snapshots
    = True` зовут `create_dump_snapshot` как часть стандартного
    snapshot stage. Они автоматически наследуют binary-backed
    режим, если operator его сконфигурировал.
  - **Что Step 2 НЕ делает.** Phase 2 stub'ы
    `apply_config_from_files` и `update_database_configuration`
    остаются **без изменений**. Phase 6 / Step 2 — это **первый
    partial slice** Industrialization Track: переведён один путь
    (dump snapshot), а не все три. Полное замещение остальных
    stub'ов на binary-backed dispatch — отдельные шаги Phase 6 и
    parallel-track'и после Phase 6.

Registry write-server'а теперь — 4 инструмента: `ping`,
`check_write_preconditions`, `create_backup_snapshot`,
`create_dump_snapshot`.

## Single-file restore from snapshot (Phase 6 / Step 4)

Phase 6 / Step 4 добавляет **одну новую public mutating-tool** —
`restore_dump_file_from_snapshot` — и расширяет audit-row
структурными `details`, без перекройки внешнего контракта прочих
write-tools. Это самый узкий из возможных rollback-примитивов: копия
**одного** оператор-указанного файла из snapshot-дерева обратно в
живой dump. Whole-tree restore из этого tool сделать **нельзя**, и
это намеренно.

- **`restore_dump_file_from_snapshot(environment, relative_path,
  snapshot_file_path, label="restore-dump-file")`** — mutating tool,
  идёт через `run_write_flow(...)`: preflight + snapshot +
  operation + verify + audit как у любого другого mutating-инструмента.
  Контракт:
  - `relative_path` обязан резолвиться **внутрь** `environment.dump_path`.
    Абсолютные пути и сегменты `..` отвергаются fail-closed **до**
    вызова subprocess'а / преcondition'а;
  - `snapshot_file_path` обязан указывать на существующий regular
    file. Отсутствие или non-regular path → `ok=False` (тоже
    fail-closed, никаких мягких пропусков);
  - parent-directories целевого файла создаются по необходимости в
    пределах dump-дерева; никакие посторонние пути не трогаются;
  - in-flow `verify` проверяет **byte-equality** между живым
    target-файлом и snapshot-файлом после копии (сравнение полного
    содержимого, не размер/мтайм);
  - запись в дампе делается atomically: `*.tmp` рядом с целевым
    файлом + `Path.replace`. Промежуточный частичный файл не
    остаётся в dump-дереве.
- **`AuditRecord.details`** теперь несёт необязательный
  JSON-сериализуемый dict для structured-артефактов, которые
  recovery / rollback требуют от write-flow:
  - `operation_name` — имя public-инструмента
    (`add_catalog_attribute`, …);
  - `rollback_supported` — bool, отражает попадание `operation_name`
    в Phase 6 / Step 4 whitelist (текущий состав — две позиции:
    `add_catalog_attribute`, `add_document_attribute`);
  - `backup_snapshot_path` / `dump_snapshot_path` / `relative_path`
    — пути, которые позволяют recovery-ассистенту найти исходный
    файл и снапшот.
  Pre-Step-4 audit-строки **остаются байт-идентичны** — `details=None`
  явно вырезается из JSON, чтобы старые лог-файлы не приобретали
  ключ `"details": null`. Reader-слой
  (`onec_audit.read_last_record`) совместим с обоими форматами.
- **Whitelist Step 4 — реальные исполняемые откаты — состоит из двух
  tools**: `add_catalog_attribute` и `add_document_attribute`. Это
  объекты, чьё содержание полностью описывается одним XML-файлом и
  обратимо ровно копированием snapshot-копии этого файла. Для всех
  остальных mutating-инструментов `details.rollback_supported = False`,
  и продуктовый recovery-ассистент честно говорит, что
  автоматический откат не поддержан (advisory-only). Расширение
  whitelist'а — отдельные шаги Phase 6.
- **Никаких back-door write-каналов.** Восстановление файла из
  snapshot'а в продуктовом слое идёт **только** через этот public
  write-tool — `onec_platform.recovery` не пишет в файловую систему
  напрямую. Поэтому rollback наследует ту же policy / preflight /
  snapshot / verify / audit дисциплину, что и forward write.

Registry write-server'а теперь — **24 инструмента** (был 23). Новый
tool — `restore_dump_file_from_snapshot`. Состав остального registry
не изменился; ни один существующий tool не получил новых
обязательных параметров.

## First structural XML edit slice (Phase 6 / Step 5)

Phase 6 / Step 5 добавляет **одну новую public mutating-tool** —
`add_form_attribute` — и **расширяет** существующий dispatcher
`verify_metadata_change(...)` одной новой read-only веткой
`kind="form_attribute_exists"`. Это **первый честный structural XML
edit slice**: tool редактирует XML-карту через
`xml.etree.ElementTree`, а не через substring/`rfind` патчинг,
который используют долго существующие `add_catalog_attribute` /
`add_document_attribute`.

- **`add_form_attribute(environment, object_name, form_name,
  attribute_spec, label="add-form-attribute")`** — mutating tool,
  идёт строго через `run_write_flow(...)`. Контракт:
  - `object_name` — поддерживаемый префикс
    (`Справочник.<name>` → `Catalogs/<name>.xml`,
    `Документ.<name>` → `Documents/<name>.xml`); тот же
    `_resolve_object_xml_path`, что и у уже существующих
    form/module tool'ов;
  - `form_name` — `\w+` (Latin/Cyrillic letters, digits,
    underscore; non-empty; no spaces);
  - `attribute_spec` — dict с обязательными `name` (non-empty
    без leading/trailing whitespace) и `type` (whitelist:
    `String`, `Number`, `Date`); опциональный `synonym`;
  - **structural** локализация формы: tool парсит XML
    через `xml.etree.ElementTree`, ищет
    `<Form name="form_name">` через
    `find_form_element(root, form_name)` (рекурсивно от
    root'а — поддерживаются и flat-cards тестовых
    fixture'ов, и nested-cards `<ChildObjects><Forms>`),
    проверяет дубль через `form_has_attribute` (по
    атрибуту `name="..."`, не substring), создаёт
    `<Attributes>` блок при необходимости через
    `get_or_create_form_attributes_block` (no `rfind("</")`
    fallback), добавляет новый `<Attribute>` через
    `add_attribute_to_form_attributes_block`, пишет дерево
    обратно через `write_xml_file` (UTF-8 + XML
    declaration, `short_empty_elements=False` чтобы
    пустые контейнеры оставались в форме `<Tag></Tag>` и
    не ломали substring-based downstream tool'ы);
  - in-flow `verify` повторно парсит XML и подтверждает
    структурно, что атрибут реально появился внутри
    нужной формы — substring-наличие в файле **не**
    считается за подтверждение;
  - fail-closed branches:
    - форма не найдена → `ok=False`, `stage=operation`,
      файл не тронут;
    - атрибут уже есть в форме → `ok=False`,
      `stage=operation`, файл не тронут;
    - bad whitelist type / bad name / bad object prefix →
      pre-flow rejection (без `runtime` в payload, без
      snapshot'ов, без audit row).
- **`verify_metadata_change(..., {"kind": "form_attribute_exists",
  "object_name": ..., "form_name": ..., "attribute_name": ...})`**
  — новая read-only ветка существующего dispatcher'а. Tool
  name результата остаётся `verify_metadata_change`;
  `payload.data.verification_kind = "form_attribute_exists"`;
  внутри использует тот же `find_form_element` / `form_has_attribute`,
  что и mutating tool, поверх `read_dump_file`. **Не** ship'ит
  отдельный standalone public verify-tool — это сознательное
  решение, чтобы public surface оставалась узкой.

### Что НЕ переписано на structural edit

- `add_catalog_attribute` и `add_document_attribute` (object-level
  Attributes) **не** переписаны на DOM-edit на этом шаге. Они
  продолжают использовать `insert_fragment_into_named_block`
  (substring helper), как и раньше. Step 5 ship'ит structural
  edit точечно — для form-level Attributes — а не сметает все
  старые tool'ы одним проходом.
- Form/module level tools Phase 3 / Step 6 (`create_managed_form`,
  `add_form_element`, `append_module_method`,
  `replace_module_method_body`) тоже не тронуты — они продолжают
  работать через свои существующие helper'ы.
- `apply_config_from_files` / `update_database_configuration`
  снова не тронуты на Step 5 — это будущие шаги Phase 6 (или
  parallel-track после).

### Честные ограничения structural edit slice

- Нет XML namespace handling. Production-карты 1С обычно несут
  `xmlns="http://v8.1c.ru/8.3/MDClasses"`; namespaced cards —
  out of scope для этого slice. Tools и helper'ы рассчитаны на
  un-namespaced XML, который используют тестовые fixture'ы и
  Phase 3 substring-based tools.
- ElementTree **не** preserves whitespace / pretty-print
  byte-for-byte. После записи файл может выглядеть слегка
  иначе (например, без оригинальных переносов строк), хотя
  XML-эквивалентен. Это не ломает downstream tool'ы, но честно
  фиксируется в documentation.
- helper layer `runtime/metadata_ops.py` остаётся **internal**
  и не stably-public — никаких ToolResult'ов, никаких
  snapshot/audit обязательств; всё это лежит на tool layer
  и flow.

Registry write-server'а теперь — **25 инструментов** (был 24).
Новый tool — `add_form_attribute`. Состав остального registry
не изменился; ни один существующий tool не получил новых
обязательных параметров. `read-server` (15) и
`intelligence-server` (16) — без изменений.

## Real binary-backed `apply_config_from_files` (Parallel Track A / Step 2)

Parallel Track A / Step 2 переводит существующий public
write-tool `apply_config_from_files(...)` с чисто
stub-backed поведения на **honest dual-mode contract** —
симметрично с тем, что Phase 6 / Step 2 сделал для
`create_dump_snapshot(...)`. Никаких новых MCP tool'ов
не добавляется; registry write-server'а остаётся
**25** (`apply_config_from_files` уже в registry с Phase 2 /
Step 7). Read- и intelligence-серверы не тронуты.

### Два режима, один внешний контракт

- **stub** (Phase 2 / Step 7 default; backward-compat) —
  активен, когда хотя бы одно из
  `environment.onec_binary_path` /
  `environment.onec_applycfg_command_template`
  отсутствует. Поведение идентично legacy-стабу:
  `run_stub_apply_process(source_dump_path)` пишет
  `apply-stub.txt` + `apply-meta.json` внутрь
  `source_dump_path` через
  `onec_process_runner.run_process` + preflight + snapshot
  path. `operation_payload.mode = "stub"`,
  `operation_payload.binary_invoked = False`. Никаких
  изменений в legacy stub helper'е (`runtime/dump_ops.py`)
  не сделано.
- **binary-backed** (Parallel Track A / Step 2) —
  активен, когда **оба** поля заданы. Tool рендерит
  operator-declared `onec_applycfg_command_template`
  через whitelisted-placeholder substitution (доступны:
  `{binary_path}`, `{source_dump_path}`, `{base_path}`,
  `{base_id}`, `{publication_name}`, `{http_base_url}`),
  запускает реальный subprocess через
  `onec_process_runner.run_process` с timeout
  `_APPLYCFG_DEFAULT_TIMEOUT_SECONDS = 300`, captures
  stdout/stderr (excerpts cap 1024 символа). Operator
  сам выбирает grammar 1cv8 CLI — write-server **не
  угадывает** флаги. `operation_payload.mode =
  "binary-backed"`,
  `operation_payload.binary_invoked = True/False`
  (`False` только в двух случаях: render unknown-
  placeholder отверг template до spawn'а, или subprocess
  не смог стартовать — `PlatformError`). Дополнительно:
  `command_preview` (рендерённый argv после
  substitution'а), `exit_code`, `stdout_excerpt`,
  `stderr_excerpt`.

### Fallback discipline

Между режимами есть **только config-time fallback**:
если контракт не полный (одного из полей нет) — tool
работает в stub mode. **Runtime fallback запрещён**:
если binary-backed subprocess вернул non-zero
(`completed=True, exit_code != 0`) или
не завершился (`completed=False`) — tool возвращает
`ok=False` с сохранённым `mode = "binary-backed"`,
никакого silent-перезапуска stub после реального
failure'а. Это та же дисциплина, что у
`create_dump_snapshot` Phase 6 / Step 2.

### Payload-контракт (симметрия с `create_dump_snapshot`)

В обоих режимах `operation_payload` (и `verify_payload`)
несёт один и тот же набор honest-mode полей. Stub-режим
эмитит `None` / `False` для тех полей, которые ему
неприменимы — никакой магии, оператор всегда видит
честную картину:

| Поле | stub | binary-backed |
|---|---|---|
| `mode` | `"stub"` | `"binary-backed"` |
| `binary_invoked` | `False` | `True` (или `False` при render-fail / start-fail) |
| `exit_code` | `None` | int (`0` на happy path) |
| `command_preview` | `None` | rendered argv list |
| `stdout_excerpt` | `None` | str (≤ 1024 символа) |
| `stderr_excerpt` | `None` | str (≤ 1024 символа) |

Эти поля symmetric и `apply_config_from_files`, и
`create_dump_snapshot` (Phase 6 / Step 2 уже эмитит то же
самое), что даёт оператору единый ментальный шаблон
«как читать binary-backed write payload». Финальная
унификация helper'ов между двумя tool'ами — задача Track A
/ Step 4; сейчас render-функция и operation/verify-callable
у apply отдельные, без преждевременной generalization.

### `run_write_flow` discipline

Public `apply_config_from_files(...)` по-прежнему идёт
через `run_write_flow(...)`: preflight → snapshot →
operation → verify → audit. На failure path стадии
честно различимы:
- unknown placeholder в template'е → tool возвращает
  `ok=False` **до** входа в `run_write_flow` (никакие
  snapshots не делаются, audit row не пишется);
- start-fail subprocess'а (`PlatformError`) → flow
  возвращает `stage='operation'`, `operation_payload` не
  попадает в payload (subprocess не отработал, captured
  output отсутствует);
- non-zero exit / non-completed subprocess →
  `stage='verify'`, `operation_payload` **сохраняется**
  в payload (captured output есть; verify
  отверг exit code).

Tool name результата — `apply_config_from_files` (не
внутреннее `run_write_flow`); audit row пишется с тем же
`tool_name`. Ничего из write-flow дисциплины не
размывается; никакого back-door write channel'а из
write-server'а / product layer'а не вводится.

### Что **не** сделано на этом шаге (Step 2 трека)

- `update_database_configuration` **по-прежнему
  stub-backed** — это Step 3 Track A, не сейчас.
- `create_dump_snapshot` не переписан — он уже имеет
  binary-backed branch с Phase 6 / Step 2; финальная
  унификация payload-discipline и shared helper'ов
  между всеми тремя binary-backed tool'ами — задача
  Track A / Step 4.
- Никакого реального multi-step round-trip'а на
  reference stand'е (real DumpCfg → real LoadCfg → real
  UpdateDBCfg) — это Step 6 Track A.
- Никакого расширения rollback whitelist'а Phase 6 /
  Step 4 (`apply_config_from_files` остаётся
  advisory-only с точки зрения rollback assistant'а;
  whitelist остаётся `add_catalog_attribute` +
  `add_document_attribute`).
- Никаких новых MCP tool'ов; registry counts остаются
  read=15 / write=25 / intelligence=16.
- Это **partial slice**, а не full real write path
  closure. Trek закроется на Step 7.

## Real binary-backed `update_database_configuration` (Parallel Track A / Step 3)

Parallel Track A / Step 3 переводит существующий public
write-tool `update_database_configuration(...)` с чисто
stub-backed поведения на **honest dual-mode contract** —
симметрично с тем, что Step 2 трека сделал для
`apply_config_from_files(...)` и Phase 6 / Step 2 для
`create_dump_snapshot(...)`. Никаких новых MCP tool'ов
не добавляется; registry write-server'а остаётся **25**
(`update_database_configuration` уже в registry с
Phase 2 / Step 9). Read- и intelligence-серверы не
тронуты.

### Два режима, один внешний контракт

- **stub** (Phase 2 / Step 9 default; backward-compat) —
  активен, когда хотя бы одно из
  `environment.onec_binary_path` /
  `environment.onec_updatedb_command_template`
  отсутствует. Поведение идентично legacy-стабу:
  inline через `onec_process_runner.run_process` пишет
  `.update-db-stub.txt` + `.update-db-meta.json`
  внутрь `environment.dump_path`.
  `operation_payload.mode = "stub"`,
  `operation_payload.binary_invoked = False`. Старые
  значения `.update-db-meta.json` (включая
  `mode: "stub-update-db"` поле в самом meta-файле)
  сохранены без изменений — backward compatibility для
  любого external reader'а meta-файла.
- **binary-backed** (Parallel Track A / Step 3) —
  активен, когда **оба** поля заданы. Tool рендерит
  operator-declared `onec_updatedb_command_template`
  через whitelisted-placeholder substitution
  (доступны: `{binary_path}`, `{base_path}`,
  `{base_id}`, `{publication_name}`,
  `{http_base_url}`), запускает реальный subprocess
  через `onec_process_runner.run_process` с timeout
  `_UPDATEDB_DEFAULT_TIMEOUT_SECONDS = 300`, captures
  stdout/stderr (excerpts cap 1024 символа). Operator
  сам выбирает grammar 1cv8 CLI — write-server **не
  угадывает** флаги. `operation_payload.mode =
  "binary-backed"`,
  `operation_payload.binary_invoked = True/False`
  (`False` только в двух случаях: render
  unknown-placeholder отверг template до spawn'а, или
  subprocess не смог стартовать — `PlatformError`).
  Дополнительно: `command_preview` (рендерённый argv
  после substitution'а), `exit_code`, `stdout_excerpt`,
  `stderr_excerpt`.

### Whitelist placeholders (более узкий, чем у dumpcfg / applycfg)

Update-db whitelist специально tighter:
`{binary_path}`, `{base_path}`, `{base_id}`,
`{publication_name}`, `{http_base_url}` — пять имён
вместо шести. UpdateDBCfg операционно работает на
живой инфобазе с уже-применённым config'ом, поэтому
ни `{output_path}` (нечего дампить), ни
`{source_dump_path}` (нечего читать из source-tree)
ему не нужны. Если оператор по ошибке поставит один
из них в template — это будет render-time fail-closed
**до** spawn'а subprocess'а с понятным сообщением.
Это сознательное анти-расползание surface'а.

### Fallback discipline

Между режимами есть **только config-time fallback**:
если контракт не полный (одного из полей нет) — tool
работает в stub mode. **Runtime fallback запрещён**:
если binary-backed subprocess вернул non-zero
(`completed=True, exit_code != 0`) или не завершился
(`completed=False`) — tool возвращает `ok=False` с
сохранённым `mode = "binary-backed"`, никакого
silent-перезапуска stub после реального failure'а.
Это та же дисциплина, что у `apply_config_from_files`
Track A / Step 2 и `create_dump_snapshot` Phase 6 /
Step 2.

### Payload-контракт (симметрия с Step 2 / Phase 6 Step 2)

В обоих режимах `operation_payload` (и
`verify_payload`) несёт один и тот же набор
honest-mode полей. Stub-режим эмитит `None` / `False`
для тех полей, которые ему неприменимы — никакой
магии, оператор всегда видит честную картину:

| Поле | stub | binary-backed |
|---|---|---|
| `mode` | `"stub"` | `"binary-backed"` |
| `binary_invoked` | `False` | `True` (или `False` при render-fail / start-fail) |
| `exit_code` | `None` | int (`0` на happy path) |
| `command_preview` | `None` | rendered argv list |
| `stdout_excerpt` | `None` | str (≤ 1024 символа) |
| `stderr_excerpt` | `None` | str (≤ 1024 символа) |

Это тот же набор полей, который уже эмитят
`create_dump_snapshot` (Phase 6 / Step 2) и
`apply_config_from_files` (Track A / Step 2) — единый
ментальный шаблон оператора «как читать binary-backed
write payload». Финальная унификация helper'ов между
тремя tool'ами — задача Track A / Step 4; сейчас
render-функция и operation/verify-callable у updatedb
отдельные, без преждевременной generalization.

### `run_write_flow` discipline

Public `update_database_configuration(...)` по-прежнему
идёт через `run_write_flow(...)`: preflight →
snapshot → operation → verify → audit. На failure path
стадии честно различимы:
- unknown placeholder в template'е → tool возвращает
  `ok=False` **до** входа в `run_write_flow` (никакие
  snapshots не делаются, audit row не пишется);
- start-fail subprocess'а (`PlatformError`) → flow
  возвращает `stage='operation'`, `operation_payload`
  не попадает в payload (subprocess не отработал,
  captured output отсутствует);
- non-zero exit / non-completed subprocess →
  `stage='verify'`, `operation_payload` **сохраняется**
  в payload (captured output есть; verify отверг exit
  code).

Tool name результата — `update_database_configuration`
(не внутреннее `run_write_flow`); audit row пишется с
тем же `tool_name`. Ничего из write-flow дисциплины
не размывается; никакого back-door write channel'а из
write-server'а / product layer'а не вводится.

### Что **не** сделано на этом шаге (Step 3 трека)

- `apply_config_from_files` уже переведён (Step 2);
  здесь не трогается.
- `create_dump_snapshot` уже имеет binary-backed
  branch (Phase 6 / Step 2); финальная унификация
  payload-discipline и shared helper'ов между всеми
  тремя binary-backed tool'ами — задача Track A /
  Step 4. Сейчас три render-функции и три набора
  callable'ов живут параллельно — это сознательно.
- Никакого реального multi-step round-trip'а на
  reference stand'е (real DumpCfg → real LoadCfg →
  real UpdateDBCfg) — это Step 6 Track A.
- Никакого расширения rollback whitelist'а
  Phase 6 / Step 4 (`update_database_configuration`
  остаётся advisory-only с точки зрения rollback
  assistant'а; whitelist остаётся
  `add_catalog_attribute` + `add_document_attribute`).
- Никаких новых MCP tool'ов; registry counts остаются
  read=15 / write=25 / intelligence=16.
- Это **partial slice**, а не full real write path
  closure. Trek закроется на Step 7.

## Internal unification of binary-backed write contract (Parallel Track A / Step 4)

Parallel Track A / Step 4 — **internal-only** unification.
Никакого нового MCP tool surface, никаких изменений в
operator-facing argv grammar / placeholder whitelistах /
ToolResult shape. Step 4 решает Q3 открытого вопроса Step 1
плана трека: где живут shared helper'ы для binary-backed
write execution.

### Что появилось

Один внутренний модуль:
**`apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`**

Этот модуль — **internal**: не public API, не registered
MCP tool, не product-layer surface. Используется только тремя
public binary-backed write-tool'ами и больше никем:

- `create_dump_snapshot(...)` (Phase 6 / Step 2 binary-backed
  branch)
- `apply_config_from_files(...)` (Track A / Step 2
  binary-backed branch)
- `update_database_configuration(...)` (Track A / Step 3
  binary-backed branch)

Содержит:

- `BINARY_OUTPUT_EXCERPT_LIMIT = 1024` — единая константа cap'а
  excerpt'ов stdout / stderr (раньше каждый из трёх tool'ов
  имел свою копию).
- `BINARY_DEFAULT_TIMEOUT_SECONDS = 300` — единый default
  timeout для subprocess invocation (раньше каждый из трёх
  tool'ов имел свою копию).
- `UnknownPlaceholderError` / `PlaceholderProxy` — внутренняя
  механика placeholder substitution (раньше жила в
  `tools.py` как `_UnknownPlaceholderError` / `_PlaceholderProxy`).
- `excerpt(text)` — единый excerpt cap helper (раньше был
  `_excerpt` в `tools.py`).
- `render_command_template(template, *, substitutions,
  allowed_placeholders, template_field_name)` — generic
  placeholder substitution engine. **Whitelist остаётся
  per-tool**: каждый tool передаёт свой
  `allowed_placeholders` set и свой `template_field_name`
  для error message. Никакой автоматической generalization
  whitelist'ов в superset не делается — намеренно.
- `stub_honest_mode_fields()` — возвращает unified dict шести
  honest-mode полей для stub-branch'а
  (`mode='stub'`, `binary_invoked=False`,
  `exit_code=None`, `command_preview=None`,
  `stdout_excerpt=None`, `stderr_excerpt=None`).
- `binary_backed_render_failure_fields()` — для случая, когда
  render template'а упал до spawn'а subprocess'а
  (`mode='binary-backed', binary_invoked=False, ...`).
- `binary_backed_start_failure_fields(command)` — для случая,
  когда `PlatformError` от runner'а не дал стартовать
  subprocess (`binary_invoked=False`, но
  `command_preview` уже есть — render успел).
- `binary_backed_payload_fields(command, process_result)` —
  для случая, когда subprocess реально отработал
  (`binary_invoked=True`, exit_code / command_preview /
  excerpts полностью populated; ещё `completed` 7-м полем для
  shape verify check).
- `is_binary_subprocess_successful(payload_fields)` — единый
  shape verify helper (`completed && exit_code == 0`).
- `honest_mode_keys() -> tuple[str, ...]` — utility для
  тестов / документации; возвращает шесть имён ключей.

### Как изменился `tools.py`

Все три public binary-backed write-tool'а сидят теперь на
shared mechanics:

- Удалены три duplicated константы `_DUMPCFG_OUTPUT_EXCERPT_LIMIT`
  / `_APPLYCFG_OUTPUT_EXCERPT_LIMIT` /
  `_UPDATEDB_OUTPUT_EXCERPT_LIMIT` (все три были = 1024).
- Удалены три duplicated константы
  `_DUMPCFG_DEFAULT_TIMEOUT_SECONDS` /
  `_APPLYCFG_DEFAULT_TIMEOUT_SECONDS` /
  `_UPDATEDB_DEFAULT_TIMEOUT_SECONDS` (все три были = 300).
- Удалены `_PlaceholderProxy`, `_UnknownPlaceholderError`,
  `_excerpt` — переехали в `binary_dispatch`.
- Три `_render_*_command` стали тонкими tool-specific
  wrapper'ами вокруг shared `render_command_template`. Каждый
  передаёт свой substitutions dict + свой whitelist + свой
  template field name. Whitelistы **остаются per-tool**:
  - `_DUMPCFG_TEMPLATE_PLACEHOLDERS` — 6 имён (Phase 6 / Step 2)
  - `_APPLYCFG_TEMPLATE_PLACEHOLDERS` — 6 имён (Track A / Step 2)
  - `_UPDATEDB_TEMPLATE_PLACEHOLDERS` — 5 имён, tighter
    (Track A / Step 3, без `output_path` / `source_dump_path`)
- Stub-branch payloads трёх tool'ов теперь spread'ят
  `**stub_honest_mode_fields()` вместо inline-копии.
- Binary-backed-branch payloads трёх tool'ов теперь
  spread'ят `**binary_backed_payload_fields(command, ...)`
  (или его render/start-failure варианты) вместо inline-копии.
- Verify callable'ы apply / updatedb используют общий
  `is_binary_subprocess_successful(...)` predicate.

### Закрытие payload-discipline gap у `create_dump_snapshot`

До Step 4 dump-snapshot stub branch (success path,
render-fail path, PlatformError-fail path, dump-meta-fail
path) и binary-backed branch (render-fail path, mkdir-fail
path, internal-defensive-check path) **не несли всех шести
honest-mode полей** в payload.data: некоторые ветки имели
только `mode` + `binary_invoked` + tool-specific extras.
Step 4 закрыл этот gap — теперь **каждая** ветка
**каждого** из трёх tool'ов несёт все шесть полей честно
(`None` / `False` где не применимо, populated в
binary-backed success). Operator получает единый ментальный
шаблон «как читать payload binary-backed write-tool'а»
независимо от того, какой это tool и какая ветка
сработала.

### Что **не** сделано на этом шаге

- **Не унифицирован whitelist placeholders.** Каждый tool
  имеет свой собственный whitelist (намеренно — сужение /
  расширение surface'а решается per-tool, не общим
  superset'ом).
- **Не сделан generic helper framework "для всех будущих
  binary-backed write-tools".** Module `binary_dispatch`
  обслуживает ровно три текущих binary-backed-tool'а;
  расширять его surface впрок — не задача Step 4.
- **Не изменён operator-facing argv grammar.** Все три
  template'а принимают тот же синтаксис placeholders,
  что и до refactor'а; шесть / шесть / пять имён в
  whitelist'ах те же, что были.
- **Не изменён ToolResult shape.** Внешний контракт payload'а
  для всех трёх tool'ов сохранён. Tool-specific extras
  (`snapshot_type` / `snapshot_path` / `source_dump_path` /
  `marker_path` / …) живут на тех же местах. Шесть
  honest-mode полей теперь присутствуют **всегда** во всех
  ветках (раньше у dump_snapshot были разрывы) —
  это improvement, не breaking change.
- **Не тронут legacy stub helper `runtime/dump_ops.py`** (его
  обёрнули, не переписали).
- **Не расширен rollback whitelist Phase 6 / Step 4.**
- **Не сделан reference stand multi-step round-trip** — это
  Step 6 трека.
- **Не тронуты `mcp-read-server`, `mcp-intelligence-server`,
  `apps/platform/`, `onec-policy-engine`, `onec-audit`,
  `onec-health`, `onec-process-runner`,
  `onec-troubleshooting`, `mcp-common`,
  `onec-config`** (Step 4 — refactor внутрь
  `apps/mcp-write-server/`).

Registries без drift'а: read=15 / write=25 / intelligence=16.
Trek ещё не закрыт; следующий шаг — Step 5
(product-layer integration over real write path).

## Phase 3 Metadata Changes закрыт (Phase 3 / Step 7 — final integration pass)

Metadata-контур Phase 3 подтверждён end-to-end одним сквозным
сценарием на временном окружении:

**preflight → snapshots → operation → verify → audit**

отработала на цепочке из 5 mutating + 3 verification + 1 audit reader
+ 1 rollback hint; ошибка операции (`create_managed_form` на XML без
`<Forms>`) и ошибка прав (`replace_module_method_body` без
`confirm_replace=True`) отработали fail-closed без побочных эффектов.

### Состав metadata-контура

- **Object/attribute level** (group B mutating, через flow):
  `create_catalog`, `create_common_module`, `add_catalog_attribute`,
  `add_document_attribute`.
- **Form/module level** (group B mutating, через flow):
  `create_managed_form`, `add_form_element`, `append_module_method`,
  `replace_module_method_body` (с обязательным `confirm_replace=True`
  — отвергается до flow).
- **Metadata shape verification** (group C, самостоятельные
  read-only tools, **не** через flow, не пишут audit, не снимают
  snapshots):
  `verify_attribute_exists`, `diff_dump_fragment`, расширенный
  `verify_metadata_change` (`kind ∈ {object_exists, module_contains,
  attribute_exists, form_exists, method_exists}`).
- **Audit / rollback support** (group D, read-only для внешнего
  мира, только append для audit store): `write_audit_record`,
  `describe_last_write_operation`, `prepare_rollback_hint`.
- Существующая Phase 2 safety/preflight group A
  (`check_write_preconditions`, `create_backup_snapshot`,
  `create_dump_snapshot`) используется всеми mutating tools
  автоматически внутри `run_write_flow`.

### Гарантии, подтверждённые интеграционным прогоном

- Все mutating metadata-tools идут через `run_write_flow(...)`:
  оставляют уникальный `operation_id`, `backup_snapshot_path`,
  `dump_snapshot_path`, `audit_path` в `payload.data`.
- `AuditRecord.tool_name` равен имени public-инструмента, не
  внутреннему `run_write_flow`: интеграционный `describe_last_write_operation`
  по итогу цепочки вернул `append_module_method`.
- Verification-tools и audit/rollback support действительно
  read-only: не создают snapshots, не пишут в audit при вызове.
- `prepare_rollback_hint` находит запись по `operation_id`, возвращает
  `audit_status`, осмысленные `suggested_backup_root` /
  `suggested_dump_root` и непустой `hint_text`.
- Scenario C подтверждает, что `replace_module_method_body` без
  `confirm_replace=True` **не запускает flow вовсе**: нет `runtime`
  в payload, нет snapshot refs, нет `audit_path`, файл `.audit/audit.jsonl`
  не создаётся.

### Registry write-server = 23

`ping`, `check_write_preconditions`, `create_backup_snapshot`,
`create_dump_snapshot`, `apply_config_from_files`, `update_module_code`,
`create_common_module`, `verify_module_contains`, `verify_object_exists`,
`verify_metadata_change`, `update_database_configuration`,
`add_catalog_attribute`, `write_audit_record`,
`describe_last_write_operation`, `prepare_rollback_hint`,
`create_catalog`, `add_document_attribute`, `verify_attribute_exists`,
`diff_dump_fragment`, `create_managed_form`, `add_form_element`,
`append_module_method`, `replace_module_method_body`.

### Минимальная правка, внесённая во время Step 7

Единственный кодовый фикс — `create_catalog` stub дополнен пустым
`<Forms></Forms>` блоком, симметрично добавленному в Step 6 пустому
`<Elements></Elements>` внутри `build_form_fragment`. Без этого
свежий каталог не принимал `create_managed_form` (композабильность
был сломана). Правка обратно-совместимая: ранее зафиксированные
assertions Step 4 (`<Name>`, `<Synonym>` substring-проверки) не
изменяются.

### Что остаётся временным / stub-backed (не блокирует закрытие Phase 3)

- `apply_config_from_files` — stub-backed process apply, не
  настоящий `1cv8 LoadConfigFromFiles`.
- `update_database_configuration` — stub-backed process update, не
  настоящий `1cv8 UpdateDBCfg`.
- `create_dump_snapshot` — process-backed stub, не настоящий
  `1cv8 DumpCfg`.
- `prepare_rollback_hint` — подсказка для ручного отката, не
  исполнитель.
- `add_catalog_attribute` / `add_document_attribute` — pragmatic text
  patch, не full 1C XML DOM editor.
- Настоящий `1cv8`-integration требует пути к бинарю в
  `onec-config.EnvironmentConfig` — отдельный parallel follow-up,
  не MVP-блокирующий для Phase 3 и Phase 4.

## Form/module level metadata tools (Phase 3 / Step 6)

Первая волна **public mutating metadata tools уровня форм и модулей**.
Все четыре — тонкие обёртки над `run_write_flow(...)` (preflight →
snapshots → operation → verify → audit) и используют helper layer
Step 3 там, где он подходит. Resolver объектных имён `Справочник.` /
`Документ.` берётся из Step 5 (`_resolve_object_xml_path`).

- **`create_managed_form(environment, object_name, form_name,
  label="create-managed-form")`** — вставляет `build_form_fragment(
  form_name)` внутрь блока `<Forms>` resolved-XML объекта через
  `insert_fragment_into_named_block`. Предусловия: `object_name` —
  поддерживаемый префикс, `form_name` — валидное имя (`\w+`), XML
  объекта имеет парный `<Forms>...</Forms>`, `<Form name="form_name">`
  в файле ещё нет. Иначе — fail-closed. **Silent fallback к
  `rfind("</")` отсутствует.** На этом шаге
  `build_form_fragment` в metadata_ops.py слегка расширен:
  добавлен пустой `<Elements></Elements>` блок внутрь формы, чтобы
  последующий `add_form_element` имел детерминированную точку
  вставки.
- **`add_form_element(environment, object_name, form_name,
  element_spec, label="add-form-element")`** — добавляет элемент
  внутрь существующей формы. Pragmatic structural patch:
  приватный helper `_find_form_block_bounds` локализует
  `<Form name="form_name">...</Form>` по имени, затем внутри этого
  блока ищет `</Elements>` и вставляет fragment перед ним.
  Fail-closed, если формы по имени нет, внутри формы отсутствует
  парный `<Elements>` блок, или в форме уже есть элемент с тем же
  именем (коллизия проверяется по маркеру
  `<Element name="element_name">` именно в границах этой формы).
  Контракт `element_spec`: `name`, `type` (обязательные non-empty
  строки), опциональный `title`.
- **`append_module_method(environment, module_relative_path,
  method_spec, label="append-module-method")`** — добавляет новый
  BSL-метод в модуль через helper layer Step 3:
  `build_module_method_fragment` → `append_method_to_module` →
  `patch_text_file`. Коллизия метода проверяется через
  `module_contains_method`. Контракт `method_spec`: `name`
  (валидация `\w+`), `body` (non-empty non-whitespace),
  `export: bool` по умолчанию `False`. Fail-closed, если модуль
  отсутствует или метод уже объявлен.
- **`replace_module_method_body(environment, module_relative_path,
  method_name, new_body, *, confirm_replace=False, label=...)`**
  — **намеренно опасная** операция. Требует явного
  `confirm_replace=True` — иначе rejected до flow без snapshots /
  audit. Находит подпись метода осторожной regex
  `(Процедура|Функция|Procedure|Function)\s+method_name\s*\(...\)
  (\s+(Экспорт|Export))?\s*\n`, затем ближайшее `КонецПроцедуры` /
  `КонецФункции` (или Latin-эквивалент), совпадающее по роду
  объявления (процедура/функция), и заменяет body между ними. Если
  structure не распознаётся (нет сигнатуры или нет парного end) —
  fail-closed. `module_contains_method` выступает честным
  pre-check'ом. Verify: метод на месте, новый body — в файле.

Registry write-server'а теперь — **23 инструмента** (group A = 3,
group B mutating = 5 Phase 2 + 2 Phase 3/Step 4 + 4 Phase 3/Step 6,
group C verification = 4 Phase 2/3, group D audit/rollback = 3,
plus `ping`).

## Verification-tools для metadata shape (Phase 3 / Step 5)

Первая волна **read-only verification-tools** для metadata shape.
Все три — **самостоятельные public tools**: не меняют состояние,
не снимают snapshots, не пишут audit, **не идут через
`run_write_flow(...)`**. Cross-app import по-прежнему строго
`write → read` (`mcp_read_server.runtime.read_dump_file`).

- **`verify_attribute_exists(environment, object_name,
  attribute_name)`** — dump-only substring-проверка наличия
  атрибута в XML-карточке объекта. Resolver (`Справочник.<name>`
  → `Catalogs/<name>.xml`; `Документ.<name>` →
  `Documents/<name>.xml`) — MVP-уровень; другой префикс →
  `ok=False` с понятным reason. Файл отсутствует или
  `PlatformError` от dump adapter → `ok=False`, исключение
  наружу не выходит. Payload: `object_name`, `attribute_name`,
  `relative_path`, `exists`.
- **Расширенный `verify_metadata_change(environment, expectation)`**
  — в dispatcher добавлены три новые ветки `kind`:
  - `"attribute_exists"` с полями `object_name`, `attribute_name`
    — делегирует в `verify_attribute_exists`;
  - `"form_exists"` с полями `object_name`, `form_name` —
    inline (через `_verify_form_exists_internal`): read-only
    dump-level substring-поиск `form_name` в XML-карточке
    resolved объекта. Отдельного public `verify_form_exists`
    tool'а на этом шаге не добавлялось — только ветка
    dispatcher'а, как требует ТЗ;
  - `"method_exists"` с полями `module_relative_path`,
    `method_name` — inline (через
    `_verify_method_exists_internal`): читает модуль через
    `read_dump_file`, проверяет наличие объявления метода через
    `module_contains_method` из helper layer Step 3.
  Итоговый `tool_name` всегда `"verify_metadata_change"`,
  `payload.data.verification_kind` отражает ветку. Старые
  ветки `"object_exists"` и `"module_contains"` не тронуты.
- **`diff_dump_fragment(environment, relative_path, baseline)`** —
  unified-diff dump-файла против переданного baseline'а через
  `difflib`. `ok=True`, если файл удалось прочитать, **независимо
  от того, есть ли различия**: diff — это информация, а не ошибка.
  При различиях `changed=True` и `diff_preview` — компактный
  unified-diff (первые 40 строк с маркером truncation при
  переполнении). При равенстве — `changed=False`,
  `diff_preview=""`. Если файл недоступен — `ok=False`.
  Payload: `relative_path`, `changed`, `current_text_length`,
  `baseline_length`, `diff_preview`.

Registry write-server'а теперь — **19 инструментов** (добавлены
`verify_attribute_exists` и `diff_dump_fragment`; `verify_metadata_change`
уже был в registry и получил только новые ветки внутри).

## Object/attribute level metadata tools (Phase 3 / Step 4)

Первая волна public **metadata mutating tools** поверх helper layer
из Step 3. Все три — тонкие обёртки над `run_write_flow(...)` и
соответственно получают preflight → snapshots → operation → verify →
audit без дублирования этой логики.

- **`create_catalog(environment, catalog_name, spec,
  label="create-catalog")`** — создаёт новый файл
  `Catalogs/<catalog_name>.xml` с минимальным stub-карточкой
  `<MetaData><Name>...</Name>[<Synonym>...</Synonym>]<Attributes></Attributes></MetaData>`.
  Pre-flow валидация: `catalog_name` по regex `\w+` (как у
  `create_common_module`), `spec` — dict, `spec.synonym` — `str | None`.
  Если файл уже существует — `FileExistsError` в operation → flow
  отдаёт `ok=False, stage=operation`, audit пишется `status=error`.
  Stub включает пустой `<Attributes></Attributes>`, чтобы
  последующий `add_catalog_attribute` сразу работал.
- **`add_document_attribute(environment, document_name,
  attribute_spec, label="add-document-attribute")`** — добавляет
  атрибут в `Documents/<document_name>.xml` через
  `build_attribute_fragment(...)` + `insert_fragment_into_named_block(
  xml_text, "Attributes", fragment)` внутри `patch_xml_file(...)`.
  Pre-flow валидация: `document_name` непустой, `attribute_spec` —
  dict, `name` без edge-whitespace, `type` из whitelist'а
  `{"String", "Number", "Date"}`. Если уже есть упоминание имени в
  XML — `FileExistsError`. Если нет парного `<Attributes>` блока —
  `ValueError` из helper'а, flow отдаёт `ok=False, stage=operation`
  (никакого silent fallback к последнему `</...>`).
- **`add_catalog_attribute(environment, catalog_name,
  attribute_spec, label="add-catalog-attribute")`** — **внутренняя
  реализация переведена на helper layer из Step 3.** Внешний
  контракт (сигнатура, pre-flow валидация, whitelist типов, форма
  `payload.data`, verify-проверки) сохранён. Внутри теперь тот же
  путь, что и у `add_document_attribute`:
  `build_attribute_fragment(...)` + `insert_fragment_into_named_block(
  xml_text, "Attributes", fragment)` + `patch_xml_file(...)`.
  Старый грубый `rfind("</")` убран; если целевая карточка не
  содержит `<Attributes>` блока — fail-closed через `ValueError`.

Registry write-server'а теперь — **17 инструментов** (5 group A +
5 group B mutating + 3 group C verification + 3 group D audit/rollback
+ 1 `ping`; два новых имени — `create_catalog` и
`add_document_attribute`).

## Internal metadata patch helper layer (Phase 3 / Step 3)

Внутренний runtime-слой для Phase 3 metadata operations. **Это не
public tool layer** и registry write-server'а на этом шаге не
меняется; tools.py / server.py не тронуты. Layer будет использован
будущими metadata tools Phase 3 / Step 4–6.

Файл: `apps/mcp-write-server/src/mcp_write_server/runtime/metadata_ops.py`.

### XML / text structural helpers

- **`load_xml_text(path)`** — чтение XML как UTF-8 строки.
- **`insert_before_last_closing_tag(xml_text, fragment)`** —
  fallback-helper: вставить фрагмент перед последним `</...>`.
  Используется только когда конкретный именованный блок неизвестен.
  Без closing tag — `ValueError`.
- **`insert_fragment_into_named_block(xml_text, block_name, fragment)`**
  — **основной structural helper**: найти
  `<block_name>...</block_name>` и вставить фрагмент перед его
  закрывающим тегом. Требует именно парную открыв/закрыв пару
  (self-closing `<block_name/>` не подходит). Если блок не найден —
  `ValueError` с понятным сообщением.

### Fragment builders

- **`build_attribute_fragment(name, attr_type, synonym=None)`** —
  минимальный `<Attribute>` XML-фрагмент.
- **`build_form_fragment(form_name)`** — минимальный `<Form>` stub
  (не полная 1C managed form card — это внутренняя заготовка).
- **`build_module_method_fragment(method_name, body, export=False)`**
  — BSL-фрагмент метода в **единственном канонически зафиксированном
  формате**: `Процедура <name>() [Экспорт]\n<body>\nКонецПроцедуры\n`.
  Функции / директивы / аннотации в контракт Step 3 не входят.

### BSL helpers

- **`module_contains_method(module_text, method_name)`** — lenient
  обнаружение объявления метода через regex
  `\b(Процедура|Функция|Procedure|Function)\s+<name>\s*\(` с
  `re.IGNORECASE`. Не полноценный BSL-парсер, достаточно для
  smoke-level verify.
- **`append_method_to_module(module_text, method_fragment)`** —
  безопасное добавление метода в конец модуля с предсказуемыми
  разделителями строк.

### File patch helpers

- **`patch_xml_file(path, patcher)`** — read-transform-write в один
  шаг; `OSError` пробрасывается.
- **`patch_text_file(path, patcher)`** — то же для обычного текста
  (BSL-модули и пр.).

### Что этот layer НЕ делает

- Не возвращает `ToolResult`.
- Не ходит в HTTP / не поднимает subprocess / не пишет audit / не
  снимает snapshots — это tool layer и write-flow pipeline.
- Не пытается быть full 1C XML DOM editor. Structural helpers
  работают на уровне строк, но с осмысленной точкой вставки (по
  имени блока), а не «всегда перед последним `</...>`».
- Не экспортируется через `runtime/__init__.py` (как и
  `dump_ops.py` из Phase 2 / Step 5): будущие tools импортируют
  нужные helper'ы напрямую через
  `from .runtime.metadata_ops import ...`.

## Write MVP закрыт (Phase 2 / Step 10 — final integration pass)

Контур Write MVP собран end-to-end:

**preflight → snapshots → operation → verify → audit.**

Registry write-server'а — **15 инструментов**, разбитых на четыре группы:

- **Safety / preflight (group A)** — `check_write_preconditions`,
  `create_backup_snapshot`, `create_dump_snapshot`. Работают на
  `WriteRuntimeContext`, вызываются самостоятельно либо встроенно из
  `run_write_flow`.
- **Controlled write operations (group B)** — `apply_config_from_files`,
  `update_module_code`, `create_common_module`,
  `update_database_configuration`, `add_catalog_attribute`. **Все
  проходят строго через `run_write_flow(...)`**: preflight через
  `require_write_preconditions`, обязательные backup+dump snapshots,
  operation_callable, verify_callable, запись `AuditRecord`. Pre-flow
  валидация входов (пустой/whitespace `new_text`, регулярка
  `\w+` для `module_name`, whitelist типов атрибута) отвергает
  очевидно плохие вызовы до снятия snapshot'ов.
- **Verification (group C)** — `verify_module_contains`,
  `verify_object_exists`, `verify_metadata_change`. Самостоятельные
  public tools, **не идут через `run_write_flow`**, состояние не
  меняют, audit не пишут. Используют `mcp_read_server.runtime`
  (cross-app import строго write→read). `verify_metadata_change` —
  dispatcher-facade, всегда возвращает `tool_name=verify_metadata_change`
  и `verification_kind` в payload.
- **Audit / rollback support (group D)** — `write_audit_record`,
  `describe_last_write_operation`, `prepare_rollback_hint`.
  Самостоятельные tools, не через flow; `write_audit_record` — только
  append, `describe_last_write_operation` — только read,
  `prepare_rollback_hint` — только read + построение подсказки. **Ни
  один из них не выполняет rollback реально.**

### Гарантии контура (подтверждены интеграционным прогоном)

- Все mutating tools группы B возвращают `ToolResult` с `tool_name` =
  имя public-инструмента (rewrap через `_with_tool_name`).
- Audit-запись, которую кладёт `run_write_flow`, несёт
  `tool_name = intent.operation_name`, то есть соответствует public-
  инструменту (например, `update_module_code`, а не общий
  `run_write_flow`).
- На ошибке operation или verify flow всё равно пишет audit со
  `status="error"` и возвращает `ToolResult(ok=False, ..., stage=...)`,
  исключение наружу не выпадает.
- Cross-app import — только write → read; read-server остался
  read-only и не деградировал (15 read-tools).

### Что остаётся временным / stub-backed

- `apply_config_from_files` — **честный stub-backed process apply**
  (пишет marker + meta через `onec-process-runner` Python-процесс),
  не настоящий `1cv8 LoadConfigFromFiles`.
- `update_database_configuration` — **честный stub-backed
  process update** (marker + meta), не настоящий `1cv8 UpdateDBCfg`.
- `create_dump_snapshot` — **process-backed stub** (Python-marker +
  meta), не настоящий `1cv8 DumpCfg`.
- `prepare_rollback_hint` — только подсказка, **не откат**.
- `add_catalog_attribute` — pragmatic XML text patch, не full 1C
  DOM editor.

Настоящие `1cv8`-интеграции требуют пути к бинарю в
`onec-config.EnvironmentConfig` — это отдельный follow-up, **не
MVP-блокирующий**.

## Оставшиеся group B + audit/rollback helpers (Phase 2 / Step 9)

На этом шаге закрыт почти весь функциональный контур Write MVP.
Добавлено 5 новых public tools: 2 из группы B (через
`run_write_flow`) и 3 из группы D (самостоятельные, без flow).

**Остаток группы B (через `run_write_flow`):**

- **`update_database_configuration(environment,
  label="update-database-configuration")`** — запуск процесса
  «обновления конфигурации БД» через write-flow pipeline.
  **Apply пока честный stub-backed update-db process**, а не
  настоящий `1cv8 UpdateDBCfg`: operation через
  `onec-process-runner` пишет в корень dump маркер
  `.update-db-stub.txt`, tool дополняет `.update-db-meta.json`.
  Verify проверяет, что и marker, и meta на месте. Настоящий
  `UpdateDBCfg` придёт после появления пути к бинарю в
  `onec-config`.
- **`add_catalog_attribute(environment, catalog_name,
  attribute_spec, label="add-catalog-attribute")`** — **реальный**
  патч XML-карточки справочника в dump-дереве.
  `attribute_spec` — dict с обязательными `name` / `type` и
  опциональным `synonym`. До flow валидируется: catalog_name
  непустой, attribute_spec — dict, name без edge whitespace, type
  из whitelist'а `{"String", "Number", "Date"}`. Operation
  читает `Catalogs/<catalog_name>.xml`, проверяет, что атрибут не
  присутствует ранее, вставляет XML-фрагмент
  `<Attribute name="..."><Type>...</Type>[<Synonym>...</Synonym>]</Attribute>`
  перед последним закрывающим тегом документа и пишет обратно в
  UTF-8. **Это pragmatic text patch, не full 1C XML schema DOM
  editor.** Verify перечитывает файл и проверяет наличие имени
  и типа.

**Группа D (самостоятельные, не через `run_write_flow`):**

- **`write_audit_record(environment, record)`** — явная запись
  аудита. `record: dict` обязан содержать ненулевые строковые
  `operation_id`, `tool_name`, `status`, `message`; поля
  `environment` / `base_id` `AuditRecord`'а заполняются из
  `environment`. `audit_dir` вычисляется как
  `<environment.dump_path>/.audit`, запись идёт через
  `append_record(...)` из `onec-audit`. На `OSError` — `ok=False`
  с пояснением; запись не выбрасывается наружу.
- **`describe_last_write_operation(environment)`** — reader
  поверх `read_last_record(...)`. При отсутствии записей —
  `ok=False, "No audit records found."`; при успехе — `ok=True` с
  полным паспортом последней записи (`operation_id`, `tool_name`,
  `environment`, `base_id`, `status`, `message`).
- **`prepare_rollback_hint(environment, operation_id)`** —
  human-readable подсказка по ручному откату. **Не выполняет
  rollback.** Сканирует `<dump_path>/.audit/audit.jsonl` от
  последней строки к первой, находит запись с нужным
  `operation_id`; при отсутствии файла или записи — `ok=False`.
  При успехе возвращает `suggested_backup_root` и
  `suggested_dump_root` (корни snapshot-директорий, вычисленные
  из `environment`) плюс `hint_text` вида «Locate the backup/dump
  snapshot created around this operation and use it as the
  rollback source for a future apply/update step.»

Registry write-server'а теперь — **15 инструментов**: `ping`,
`check_write_preconditions`, `create_backup_snapshot`,
`create_dump_snapshot`, `apply_config_from_files`,
`update_module_code`, `create_common_module`,
`verify_module_contains`, `verify_object_exists`,
`verify_metadata_change`, `update_database_configuration`,
`add_catalog_attribute`, `write_audit_record`,
`describe_last_write_operation`, `prepare_rollback_hint`.

## Verification-tools, группа C (Phase 2 / Step 8)

Первые public verification-tools. Они ничего не меняют, не снимают
snapshots, не пишут audit и **не** идут через `run_write_flow(...)`.
Их задача — самостоятельно проверить последствия уже выполненной
операции. Cross-app import разрешён только в сторону write→read:
`mcp_read_server.runtime.fetch_json_from_environment`,
`read_dump_file`, `resolve_dump_path`, `find_files_by_pattern`,
`read_text_file`.

- **`verify_module_contains(environment, module_relative_path,
  expected_substring)`** — dump-level verify: через
  `read_dump_file(...)` читает файл модуля и проверяет подстроку.
  `ok=True` + `contains=True`, если найдено; `ok=False` +
  `contains=False`, если нет. Пустой/whitespace-only substring
  отвергается до чтения. `PlatformError` от dump adapter
  заворачивается в `ToolResult(ok=False, ...)`.
- **`verify_object_exists(environment, object_name)`** —
  **cross-check live + dump**: live-сторона делает
  `fetch_json_from_environment(env,
  "metadata/object?name=<urlencoded>")`, при ошибке
  `live_exists=False` и `live_error` попадает в payload; dump-
  сторона ищет `object_name` substring'ом по всем `*.xml` файлам
  выгрузки. `ok=True` только когда `live_exists AND dump_exists`.
  В payload кладутся `object_name`, `live_exists`, `dump_exists`,
  `dump_match_count` и (опционально) `live_error` / `dump_error`.
- **`verify_metadata_change(environment, expectation)`** —
  общий facade над минимальным expectation contract:
  `expectation["kind"]` определяет ветку. Поддержаны
  `"object_exists"` (делегирует в `verify_object_exists`) и
  `"module_contains"` (делегирует в `verify_module_contains`).
  В итоговом `ToolResult` `tool_name` всегда
  `"verify_metadata_change"`, а `payload.data.verification_kind`
  указывает, какая ветка отработала. Неизвестный `kind` → `ok=False`.

Verification теперь существует в двух формах одновременно:
встроенные callback'и внутри `run_write_flow` (Step 7) и
самостоятельные public tools для отдельного запуска (Step 8).

Registry write-server'а теперь — 10 инструментов: `ping`,
`check_write_preconditions`, `create_backup_snapshot`,
`create_dump_snapshot`, `apply_config_from_files`,
`update_module_code`, `create_common_module`,
`verify_module_contains`, `verify_object_exists`,
`verify_metadata_change`.

## Controlled write-tools, группа B (Phase 2 / Step 7)

Первые реальные public write-tools платформы. Все трое — тонкие
обёртки над `run_write_flow(...)`: каждый задаёт свой `WriteIntent`,
свой `label`, свой `operation_callable` и свой `verify_callable`, а
preflight / snapshots / audit приходят готовыми из flow. `tool_name`
в `ToolResult` после flow переписывается на имя public-инструмента.

- **`apply_config_from_files(environment, source_dump_path,
  label="apply-config")`** — подаёт `source_dump_path` в apply-
  сценарий. **Apply пока честный stub-backed process apply**, а не
  настоящий `1cv8 LoadConfigFromFiles`: operation проверяет, что
  `source_dump_path` — существующий каталог, через
  `onec-process-runner` запускает Python-процесс, который пишет в
  `source_dump_path` маркер `apply-stub.txt`, а затем tool кладёт
  рядом `apply-meta.json`. Verify проверяет, что маркер реально
  создан. Это временно — реальный `1cv8 LoadConfigFromFiles` придёт
  после появления пути к бинарю в `onec-config`.
- **`update_module_code(environment, module_relative_path, new_text,
  label="update-module-code")`** — **реально** перезаписывает файл
  модуля внутри `environment.dump_path` текстом `new_text` (UTF-8).
  До запуска flow tool отвергает пустой или whitespace-only
  `new_text`. Verify перечитывает файл и сверяет побайтно.
- **`create_common_module(environment, module_name, initial_text="",
  label="create-common-module")`** — **реально** создаёт
  `CommonModules/<module_name>/Ext/Module.bsl` в dump-дереве.
  `module_name` валидируется регуляркой `\w+` (латиница / кириллица
  / цифры / underscore; без пробелов; не пустой). Если файл уже
  существует — operation raises → flow возвращает
  `ok=False, stage="operation"`. При пустом `initial_text`
  записывается минимальный шаблон `// <module_name>\n`. Verify
  проверяет существование и побайтное совпадение.

Verification на этом шаге ещё **не вынесена в отдельные public
tools** — она встроена в callback'и `run_write_flow`. Отдельные
public verification-tools (`verify_metadata_change`,
`verify_module_contains`, `verify_object_exists`) появятся
в Step 8.

Registry write-server'а теперь — 7 инструментов: `ping`,
`check_write_preconditions`, `create_backup_snapshot`,
`create_dump_snapshot`, `apply_config_from_files`,
`update_module_code`, `create_common_module`.

## Write-flow pipeline (Phase 2 / Step 6)

Внутри `mcp_write_server.runtime.flow` появился единый внутренний
helper `run_write_flow(...)` — общая «труба», через которую пойдут
все будущие write-tools группы B (`apply_config_from_files`,
`update_module_code`, `create_common_module` и т.д.).

- **`WriteFlowArtifacts`** — dataclass-контракт (`backup_snapshot_path`,
  `dump_snapshot_path`, `audit_path`, `operation_payload`,
  `verify_payload`) для артефактов одного запуска flow.
- **`run_write_flow(environment, intent, *, label, operation_callable,
  verify_callable) -> ToolResult`** — последовательно выполняет:
  preflight (`require_write_preconditions`) → snapshots
  (`create_backup_snapshot` + `create_dump_snapshot`, если
  `policy.require_snapshots`) → `operation_callable(context)` →
  `verify_callable(context, operation_payload)` → запись
  `AuditRecord` через `append_record`. На любой стадии при ошибке
  возвращает `ToolResult(ok=False, ...)` с `payload.data.stage`,
  указывающим, где именно всё сорвалось, и сохраняет уже снятые
  snapshot'ы, `operation_id`, `audit_path`.

Это **не public tool** — регистр `REGISTERED_TOOLS` на этом шаге не
меняется. `run_write_flow` — внутренняя инфраструктура, поверх
которой будут собираться будущие write-tools. Dump snapshot
внутри flow пока остаётся временным process-backed stub'ом из
Step 5; настоящий `1cv8 DumpCfg` придёт отдельным step'ом,
когда появится путь к бинарю в `onec-config`.

## Runtime слой (Phase 2 / Step 4)

Внутри `mcp_write_server.runtime` живёт внутренний слой,
собирающий контекст каждой потенциальной write-операции. Tool'ы
пока его ещё не вызывают — это подготовка основы.

- **`WriteRuntimeContext`** — dataclass-snapshot операции:
  `environment` (`EnvironmentConfig`), `intent` (`WriteIntent`),
  `health_results` (`list[HealthCheckResult]`), `health_codes`,
  `policy_decision` (`PolicyDecision`), `audit_dir`.
- **`build_runtime_context(environment, intent)`** — запускает
  `check_environment_health(...)` → `summarize_health(...)` →
  `check_write_allowed(environment, intent)` и возвращает
  `WriteRuntimeContext`. `audit_dir` выводится как
  `<environment.dump_path>/.audit` — временное правило до
  появления отдельного поля в `onec-config`.
- **`require_write_preconditions(context)`** — fail-fast guard:
  сначала проверяет `policy_decision.allowed` (при deny —
  `PolicyDeniedError` из `mcp-common`), затем `health_codes`
  (при не-`["ok"]` — `HealthCheckError`). Ничего не возвращает.

Слой сознательно держится ниже tool-уровня и не знает про
конкретные write-операции — это общий контракт сборки контекста,
на котором будет стоять вся группа A (safety/preflight) и далее.

## Чего здесь намеренно ещё нет

- реальной MCP-обвязки и транспорта;
- policy enforcement через `onec-policy-engine`;
- операций backup / dump / apply / verify;
- аудита через `onec-audit`;
- любых write-инструментов, меняющих конфигурацию или данные 1С.

Эти возможности появятся на следующих этапах (Phase 2 и далее).
