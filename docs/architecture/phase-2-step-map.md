# Phase 2 Step Map

Стартовый implementation map для входа в Phase 2 Write MVP. Покрывает
первые шаги, после которых у платформы появляется рабочий preflight,
рабочий audit, runtime-слой `mcp-write-server`, цельный
backup/dump/apply/verify flow, первые write-tools и первые
verification-tools. Вся фаза сюда не входит — это карта старта.

## Step 1

**`onec-policy-engine`: из stub в реальный write-preflight / policy
слой.**

- **Цель.** Получить рабочее правило принятия write-решений на
  уровне пакета: проверять окружение и намерение операции, а не
  только булев `allow_write`.
- **Что меняем.** `PolicyDecision` получает поле
  `reason_code: str`. `check_write_allowed(environment, intent)`
  расширяется до принятия `EnvironmentConfig` и описания
  намерения (kind операции, target). Добавляется
  `require_snapshots: bool` как часть решения. Ни один
  write-tool ещё не реализован.
- **Затронутые файлы/пакеты.** `packages/onec-policy-engine/src/...`,
  README пакета. Никаких изменений в `mcp-common` и других пакетах.
- **Результат.** `check_write_allowed(...)` теперь отдаёт
  осмысленный `PolicyDecision` (allow/deny, reason_code,
  require_snapshots). `dev-check` зелёный; поведение
  покрывается ручной проверкой на трёх входах
  (prod+allow_write, local-dev+allow_write, local-dev без
  allow_write).

## Step 2

**`onec-audit`: подключение рабочего append-хранилища.**

- **Цель.** Получить реальный, append-only JSONL-store для
  аудита write-операций текущего окружения, не трогая публичный
  контракт `AuditRecord`/`format_audit_record`.
- **Что меняем.** В `onec-audit` добавляются тонкие функции
  `append_record(audit_dir: str, record: AuditRecord) -> Path`
  и `read_last_record(audit_dir: str) -> AuditRecord | None`,
  а также каноническая сериализация через
  `format_audit_record(...)`. В `onec-config.EnvironmentConfig`
  опционально появляется `audit_dir` (позже, мягко).
- **Затронутые файлы/пакеты.** `packages/onec-audit/src/...`,
  README пакета. `packages/onec-config/...` затрагивается
  минимально — только при добавлении `audit_dir`; если для
  MVP достаточно композиции `dump_path/.audit`, то
  `onec-config` можно не трогать.
- **Результат.** Любой шаг Phase 2 может положить
  `AuditRecord` в JSONL и прочитать последнюю запись. Ошибки
  файловой системы аккуратно превращаются в
  `PlatformError`/`ToolResult(ok=False, ...)` на уровне tool'а.

## Step 3

**Skeleton `mcp-write-server.runtime`.**

- **Цель.** Завести внутренний runtime-слой `mcp-write-server`,
  аналогичный `mcp_read_server.runtime`, но ориентированный на
  write-контекст. Пока без реальных write-команд.
- **Что меняем.** Внутри `apps/mcp-write-server/src/mcp_write_server`
  создаётся подпакет `runtime/` c `RuntimeContext`
  (`environment`, `health_results`, `health_codes`,
  `policy_decision`, `audit_dir`), `build_runtime_context(...)`
  и тонким write-specific helper'ом
  `require_write_preconditions(context, intent)`, который
  поднимает структурированную ошибку (но не кидает наружу).
  Никаких adapter-модулей и никаких новых tool'ов.
- **Затронутые файлы/пакеты.** `apps/mcp-write-server/src/...`,
  README сервера. `mcp-common` и пакеты не меняются.
- **Результат.** У write-server есть единая точка сбора
  контекста операции; preflight-данные и policy-решение
  лежат в одном месте и готовы к использованию tool'ами.

## Step 4

**Backup/dump snapshot helper и safety/preflight tools (группа A).**

- **Цель.** Получить рабочие инструменты для первой из трёх
  групп Phase 2 — safety/preflight. Это база для всех
  последующих write-операций.
- **Что меняем.** В `apps/mcp-write-server/src/...` появляются:
  - внутренний helper `make_backup_snapshot(ctx, label)` —
    копирует каталог `environment.base_path` в
    `environment.base_path + '.snapshots/<timestamp>-<label>'`
    через стандартный `shutil.copytree`, без 1С;
  - внутренний helper `make_dump_snapshot(ctx, label)` —
    запускает `1cv8 DumpCfg` через `onec-process-runner` в
    выделенный подкаталог dump-root;
  - три tool'а: `check_write_preconditions`,
    `create_backup_snapshot`, `create_dump_snapshot`.
- **Затронутые файлы/пакеты.**
  `apps/mcp-write-server/src/mcp_write_server/{tools.py,
  server.py, runtime/}`, README сервера. Использует уже готовые
  `onec-process-runner`, `onec-policy-engine`, `onec-health`,
  `onec-config`.
- **Результат.** Registry `mcp-write-server` впервые расширяется
  сверх `ping` — 4 инструмента (`ping`, `check_write_preconditions`,
  `create_backup_snapshot`, `create_dump_snapshot`). Backup и
  dump snapshot воспроизводимо ложатся на диск; preflight
  корректно отказывает при `allow_write=False` и при проблемах
  окружения.

## Step 5

**Единый `write_flow` helper (preflight → snapshot → operation →
verify → audit).**

- **Цель.** Централизовать последовательность, через которую
  пройдёт каждый write-tool группы B. Write-tools после этого
  шага — тонкие wrapper'ы над `write_flow`.
- **Что меняем.** В `mcp-write-server.runtime` появляется
  функция вида:
  `run_write_flow(ctx, intent, operation_callable) -> ToolResult`,
  которая:
  1. вызывает `check_write_preconditions` и прерывается при
     deny;
  2. снимает backup+dump snapshot и запоминает их пути в
     контексте;
  3. вызывает переданный `operation_callable(ctx) -> dict`;
  4. вызывает соответствующий verify-callable;
  5. пишет `AuditRecord` через append-store из Step 2 вне
     зависимости от успеха/неуспеха;
  6. возвращает единый `ToolResult` с обязательными полями
     payload: `operation_id`, `backup_ref`, `dump_ref`,
     `verify_result`, `audit_ref`.
- **Затронутые файлы/пакеты.**
  `apps/mcp-write-server/src/mcp_write_server/runtime/...`,
  README сервера.
- **Результат.** Появляется единая «труба», через которую
  обязаны пройти все будущие write-операции. Гарантирует
  «никакого silent apply» на уровне кода, а не только
  договорённости.

## Step 6

**Первые write-tools группы B: `apply_config_from_files`,
`update_module_code`, `create_common_module`.**

- **Цель.** Получить первые реально работающие write-tools и
  подтвердить, что truba `write_flow` жизнеспособна.
- **Что меняем.** В `apps/mcp-write-server/src/...`
  регистрируются три tool'а. Каждый:
  - описывает свой `WriteIntent` (kind, target);
  - предоставляет `operation_callable`, работающий либо через
    `onec-process-runner` (`LoadCfg`, `UpdateDBCfg`, apply),
    либо через dump-adapter (правка текста модуля, добавление
    XML);
  - предоставляет соответствующий `verify_callable` (см. Step 7).
  Registry `mcp-write-server` расширяется до 7 инструментов
  (`ping`, три группы A, три группы B).
- **Затронутые файлы/пакеты.**
  `apps/mcp-write-server/src/mcp_write_server/{tools.py,
  server.py}`, README сервера. Возможно — мелкий helper
  в `mcp-read-server.runtime.dump_adapter` для создания/
  обновления файлов (но **только** после явного подтверждения:
  предпочтительно держать write-путь к dump внутри write-server,
  чтобы read-server оставался read-only по контракту).
- **Результат.** Агент может через write-server реально
  применить правку кода или добавить общий модуль в тестовую
  конфигурацию, с обязательным preflight/backup/dump/apply/
  verify/audit. Это первый наблюдаемый «write работает» момент.

## Step 7

**Первые verification-tools группы C:
`verify_metadata_change`, `verify_module_contains`,
`verify_object_exists`.**

- **Цель.** Замкнуть цикл apply → verify и сделать verify
  доступным как самостоятельные tool'ы, а не только как внутреннюю
  часть `write_flow`.
- **Что меняем.** В `apps/mcp-write-server/src/...` регистрируются
  три verification-tool'а. Они используют:
  - read-server live-адаптер через cross-app вызов
    (`mcp_read_server.runtime.fetch_json_from_environment`) для
    `verify_metadata_change` и `verify_object_exists`;
  - `mcp_read_server.runtime.dump_adapter` (read-only) для
    `verify_module_contains` — substring-поиск в dump-файле.
  Cross-app import идёт одной стороной: `mcp-write-server`
  импортирует read-server runtime, не наоборот — это сохраняет
  read-server чистым read-only.
- **Затронутые файлы/пакеты.**
  `apps/mcp-write-server/src/...`, README сервера. Registry
  `mcp-write-server` расширяется до 10 инструментов.
- **Результат.** Агент получает независимый способ проверить
  реальность изменения как на dump-уровне, так и на live-уровне;
  Phase 2 переходит от отдельных write-операций к замкнутому
  циклу. Дальнейшие шаги Write MVP (группа D: audit readers,
  rollback hints, `add_catalog_attribute`, `update_database_configuration`,
  итоговый integration pass) выносятся в отдельный step map
  следующего этапа Phase 2.
