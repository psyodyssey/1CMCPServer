# Runbook: Parallel Track A reference-stand multi-step round-trip

## Цель

Дать оператору **воспроизводимую** инструкцию для одного честного
сквозного прогона трёх binary-backed write-tool'ов на **реальном**
1cv8 binary и **реальной** инфобазе:

1. `mcp_write_server.tools.create_dump_snapshot(...)` — реальный
   DumpCfg против целевой инфобазы;
2. `mcp_write_server.tools.apply_config_from_files(...)` — реальный
   LoadCfg/обновление конфигурации БД исходниками;
3. `mcp_write_server.tools.update_database_configuration(...)` —
   реальный UpdateDBCfg.

Это runbook для шага **Parallel Track A / Step 6** платформы. Шаг
**не** требует никаких изменений production-кода: dual-mode
contract уже добавлен в Track A / Steps 2–4, unified internal
helper `runtime/binary_dispatch.py` уже на месте, product-layer
surface уже обновлён в Step 5. Step 6 — это **operator-driven
exercise** на reference stand'е.

> **Важно.** Этот runbook **не** превращает 1cv8 в подвид Python.
> Платформа **не** угадывает 1cv8-CLI семантику — оператор сам
> владеет argv-template'ами для своего стенда и своей версии
> платформы. Все примеры ниже — типовые формы, которые встречаются
> на тонком клиенте 8.3, но **проверьте свою документацию 1С**
> перед использованием.

## Чего этот runbook **не** даёт

- Не разворачивает demo-инфобазу за оператора. Reference stand
  оператор готовит сам (см. prereq'ы ниже).
- Не управляет credentials. Имя пользователя / пароль для DESIGNER
  оператор хранит в своём secrets-механизме.
- Не делает rollback за оператора. Если что-то пошло не так на
  шаге UpdateDBCfg — это оперативная задача стенда, а не
  платформенная.
- Не валидирует семантику 1cv8 CLI. Платформа просто рендерит
  argv по placeholder-template'ам и запускает `subprocess`.

## Prerequisites

### 1. Реальный 1cv8 binary

- Абсолютный путь к `1cv8.exe` (Windows) или `1cv8` (Linux). На
  Windows типовые места:
  - `C:/Program Files/1cv8/<версия>/bin/1cv8.exe` (64-bit)
  - `C:/Program Files (x86)/1cv8/<версия>/bin/1cv8.exe` (32-bit)
- Не указывайте `1cv8c.exe` (тонкий клиент), `1cv8a.exe`
  (агент сервера), `1cv8s.exe` — нужен именно DESIGNER-capable
  `1cv8.exe`.

### 2. Реальная целевая инфобаза

- **Файловая база:** путь к каталогу с `1Cv8.1CD` (или `1Cv8.1CD`
  + блок `1CV8.1CD.lck`).
- **Серверная база:** connection-строка
  `Srvr=<host>;Ref=<infobase>` (или эквивалент в DESIGNER-grammar
  вашей версии).
- На стенде должна быть включена возможность DESIGNER-входа.
- Размер инфобазы — любой; рекомендуется dedicated reference
  stand, не production. **Никогда не запускайте этот runbook
  против production без отдельного operator approval.**

### 3. Operator credentials для DESIGNER

- Имя пользователя 1С с правами **Designer** на целевой
  инфобазе и пароль.
- Не коммитьте credentials в product-config. Возможные
  механизмы: переменные окружения, secret manager, ad hoc
  CLI prompt при подготовке argv-template'а.

### 4. Source dump tree для apply (если делается meaningful diff)

Apply нуждается в директории с разложенной конфигурацией
(`Configuration.xml` + поддиректории `Catalogs/`, `Documents/`,
…). Безопасные способы получить такой tree:

- **No-op round-trip** (рекомендуется на первом прогоне):
  использовать тот же source dump, что только что выгрузил
  DumpCfg. Round-trip тогда подтверждает execution layer и
  choreography, но не вносит meaningful metadata delta.
  В разделе «Что доказывает» это явно зафиксировано.
- **Минимальное контролируемое изменение:** взять snapshot,
  сделать локальное микро-изменение в одном XML (например,
  безопасный комментарий в `Configuration.xml` или
  изменение synonym одного reference-поля), убедиться что
  diff виден через `mcp_write_server.tools.diff_dump_fragment`
  до запуска apply.

### 5. Health / gateway (опционально, но рекомендуется)

`run_write_flow` дисциплина включает preflight-gate через
`onec_health.summarize_health(...)`. Если ваш stand не имеет
HTTP-публикации, можно отключить gateway-чек на уровне
EnvironmentConfig (см. документацию пакета `onec-config`) или
поднять минимальный stub-листенер. Вне reference stand'а это
делать **не** надо.

### 6. Product-config c полным real-write contract'ом

```jsonc
{
  "product_name": "trackA-step6-reference",
  "profile_name": "reference-stand",
  "default_environment": "stand",
  "project": {
    "environments": {
      "stand": {
        "name": "stand",
        "base_id": "stand-1c",
        "base_path": "C:/path/to/your/infobase",
        "publication_name": "stand",
        "http_base_url": "http://127.0.0.1:8080/stand",
        "dump_path": "C:/path/to/dump-source-tree",
        "timeout_seconds": 600,
        "allow_write": true,

        "onec_binary_path": "C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe",

        "onec_dumpcfg_command_template": [
          "{binary_path}",
          "DESIGNER",
          "/F", "{base_path}",
          "/N", "Designer",
          "/P", "<password>",
          "/DumpCfg", "{output_path}",
          "/DisableStartupMessages"
        ],
        "onec_applycfg_command_template": [
          "{binary_path}",
          "DESIGNER",
          "/F", "{base_path}",
          "/N", "Designer",
          "/P", "<password>",
          "/LoadConfigFromFiles", "{input_path}",
          "/DisableStartupMessages"
        ],
        "onec_updatedb_command_template": [
          "{binary_path}",
          "DESIGNER",
          "/F", "{base_path}",
          "/N", "Designer",
          "/P", "<password>",
          "/UpdateDBCfg",
          "-Server",
          "/DisableStartupMessages"
        ]
      }
    }
  },
  "servers": {"read": true, "write": true, "intelligence": true},
  "bootstrap": {"work_dir": "C:/path/to/work"},
  "enterprise": {
    "deployment_tier": "stage",
    "instance_id": "trackA-stand-eu",
    "config_owner": "ops@example.org",
    "change_control_required": true,
    "require_operator_identity": true,
    "runbook_reference": "docs/runbooks/track-a-reference-stand-round-trip.md"
  }
}
```

> **Placeholder whitelist per tool.** Платформа **жёстко**
> ограничивает плейсхолдеры:
> - `dumpcfg_template`: `{binary_path}`, `{output_path}`,
>   `{base_path}`, `{base_id}`, `{publication_name}`,
>   `{http_base_url}`.
> - `applycfg_template`: `{binary_path}`, `{input_path}`,
>   `{base_path}`, `{base_id}`, `{publication_name}`,
>   `{http_base_url}`.
> - `updatedb_template`: `{binary_path}`, `{base_path}`,
>   `{base_id}`, `{publication_name}`, `{http_base_url}`
>   (без `output_path` / `input_path` / `source_dump_path` —
>   tighter, потому что UpdateDBCfg не оперирует файлами).
>
> Любой неизвестный плейсхолдер — render-time `ok=False` **до**
> старта `subprocess`'а. Это намеренно.

### 7. Reference stand assumptions

- Версия 1cv8 фиксирована в `onec_binary_path`. Платформа
  **не** делает version-sniffing — оператор выбирает binary
  под свой стенд.
- DESIGNER должен запускаться с заданными ключами без
  открытия GUI (`/DisableStartupMessages` обычно достаточно
  для современных версий; на старых может понадобиться
  `/AppAutoCheckMode`-стиль flags — это область
  ответственности оператора).
- `base_path` существует, читаем оператором, и инфобаза
  не залочена другим клиентом на момент DumpCfg.
- `dump_path` существует и пуст, либо содержит ровно ту
  configuration tree, которую вы хотите apply'ить.
- На stand'е есть достаточно места под snapshot
  (`<dump_path>/_snapshots/<operation>`); platform делает
  full file-tree копию dump'а перед каждой mutating операцией.

## Точная последовательность действий

Все три tool'а вызываются **через public write-server surface**
(`mcp_write_server.tools.*`); ни один не bypass'ит `run_write_flow`
(preflight → snapshot → operation → verify → audit). Никакого
back-door write channel'а из product layer'а — есть единственный
mutating путь.

### Шаг A.1 — prereq inventory

```python
import json, sys
from pathlib import Path

# Bootstrap PYTHONPATH (см. scripts/dev/bootstrap_paths.ps1).
# В PowerShell:
#   . scripts\dev\bootstrap_paths.ps1
# В bash:
#   export PYTHONPATH="apps/mcp-read-server/src;apps/mcp-write-server/src;..."

import onec_platform as platform
config_path = Path(r"C:\path\to\reference-stand-config.json")

found = platform.inspect_enterprise_foundation_from_json_file(config_path)
print("foundation:", found.foundation_level,
      "ready:", found.ready_for_enterprise_track,
      "errors:", sum(1 for f in found.confirmed_findings if f.severity == "error"))

ready = platform.get_real_stand_readiness_from_json_file(config_path)
print("real-stand readiness:", ready.ready_for_real_stand_smoke,
      "binary_present:", ready.binary_present,
      "executable_like:", ready.binary_executable_like)
```

**Что должно быть видно перед запуском round-trip'а:**

- `foundation.foundation_level == "strong"` (или хотя бы
  `"partial"` без error'ов в section D);
- `foundation.ready_for_enterprise_track == True`;
- presumed-finding `foundation_real_write_path_contract_complete`
  — все три template'а declared;
- `readiness.binary_present == True`;
- `readiness.binary_executable_like == True`;
- `readiness.ready_for_real_stand_smoke == True`.

Если что-то из этого `False` / `error` — **не** запускайте
шаги A.2–A.5. Сначала закройте prereq'ы.

### Шаг A.2 — real `create_dump_snapshot`

```python
from mcp_write_server.tools import create_dump_snapshot
from onec_config import load_project_config
import json

with open(config_path, "r", encoding="utf-8") as f:
    raw = json.load(f)

project = load_project_config(raw["project"])
env = project.environments[raw["default_environment"]]

result = create_dump_snapshot(env, "step6-A2-dump")
print("ok:", result.ok)
print("data:", json.dumps(result.payload["data"], indent=2, default=str))
```

**Как понять, что path действительно binary-backed (а не stub):**

- `payload["data"]["mode"] == "binary-backed"` (**не** `"stub"`);
- `payload["data"]["binary_invoked"] == True`;
- `payload["data"]["exit_code"] == 0`;
- `payload["data"]["command_preview"]` — список аргументов,
  начинающийся с вашего реального `onec_binary_path`;
- `payload["data"]["snapshot_path"]` указывает на директорию
  под `<dump_path>/_snapshots/`, физически содержащую
  выгруженную configuration tree (не stub-marker
  `dump-created.txt`!).

**Артефакты на диске:**

- `<dump_path>/_snapshots/<snapshot-id>/Configuration.xml` (и
  поддиректории) — это **реальная** выгрузка;
- `<dump_path>/.audit/audit.jsonl` — **отдельной audit row для
  standalone `create_dump_snapshot` намеренно НЕ создаётся**:
  эта функция не идёт через `run_write_flow`, она — read-only-style
  snapshot helper. Audit-fingerprint pre-mutating dump'а
  появляется позже, на шагах A.4 / A.5, как
  `details.dump_snapshot_path` у mutating audit row'ов
  (`run_write_flow` сам делает pre-apply / pre-updatedb dump
  и фиксирует его в success-деталях соответствующей строки,
  без отдельной audit-записи).

### Шаг A.3 — подготовка source dump для apply

Два варианта:

**A.3a. No-op round-trip (рекомендуется на первый прогон).**
Просто скопируйте только что созданный snapshot обратно в
`dump_path` (или укажите `<dump_path>/_snapshots/<snapshot-id>`
как `source_dump_path` на следующем шаге). Это подтверждает
execution-layer choreography без meaningful diff'а.

**A.3b. Минимальное контролируемое изменение.** Возьмите
snapshot, сделайте микро-изменение (например, измените synonym
одного безопасного объекта), убедитесь что diff виден:

```python
from mcp_write_server.tools import diff_dump_fragment

dx = diff_dump_fragment(env, "Configuration.xml")
print("changed:", dx.payload["data"]["changed"])
```

`changed=True` означает, что platform увидела ваш diff и apply
будет иметь что вносить.

### Шаг A.4 — real `apply_config_from_files`

```python
from mcp_write_server.tools import apply_config_from_files

result = apply_config_from_files(
    env,
    str(env.dump_path),       # или путь к подготовленному tree из A.3
    label="step6-A4-apply",
)
print("ok:", result.ok, "stage:", result.payload["data"].get("stage"))
op = result.payload["data"]["operation_payload"]
print("mode:", op["mode"], "binary_invoked:", op["binary_invoked"],
      "exit_code:", op["exit_code"])
```

**Критерии «реально пошло binary-backed»:**

- `result.ok == True`;
- `payload["data"]["stage"] == "completed"` (полный
  preflight → snapshot → operation → verify → audit круг);
- `operation_payload["mode"] == "binary-backed"`;
- `operation_payload["binary_invoked"] == True`;
- `operation_payload["exit_code"] == 0`;
- `operation_payload["command_preview"]` — argv с
  `/LoadConfigFromFiles` и реальным `binary_path`;
- audit row с `tool_name="apply_config_from_files"`,
  `status="ok"`.

**Если apply отвалился с non-zero exit'ом:**

- `result.ok == False`;
- `operation_payload["mode"] == "binary-backed"` (**не**
  silent fallback на stub!);
- `operation_payload["binary_invoked"] == True`;
- `operation_payload["exit_code"]` — реальный exit;
- `operation_payload["stderr_excerpt"]` — обрезанный stderr
  до 1024 символов, типично содержит человекочитаемое
  сообщение DESIGNER об ошибке.

### Шаг A.5 — real `update_database_configuration`

```python
from mcp_write_server.tools import update_database_configuration

result = update_database_configuration(env, label="step6-A5-updatedb")
print("ok:", result.ok, "stage:", result.payload["data"].get("stage"))
op = result.payload["data"]["operation_payload"]
print("mode:", op["mode"], "binary_invoked:", op["binary_invoked"],
      "exit_code:", op["exit_code"])
```

**Критерии «реально пошло binary-backed»:**

- `result.ok == True`;
- `payload["data"]["stage"] == "completed"`;
- `operation_payload["mode"] == "binary-backed"`;
- `operation_payload["binary_invoked"] == True`;
- `operation_payload["exit_code"] == 0`;
- `operation_payload["command_preview"]` — argv с
  `/UpdateDBCfg` и реальным `binary_path`. **Не** должно быть
  плейсхолдеров `{input_path}` / `{output_path}` /
  `{source_dump_path}` — это запрещено tighter whitelist'ом
  для updatedb (валидируется render'ом до subprocess'а);
- audit row с `tool_name="update_database_configuration"`,
  `status="ok"`.

### Шаг A.6 — post-check интерпретация

Что именно доказывает успешный round-trip:

1. **Render-pipeline корректен.** Реальный operator-declared
   argv проходит whitelist-валидацию для всех трёх tool'ов;
   `command_preview` показывает финальный subprocess argv.
2. **`onec-process-runner` запускает реальный 1cv8 без
   `shell=True`.** Никакой shell-injection поверхности нет.
3. **`run_write_flow` choreography honestly работает на реальном
   стенде.** Preflight → snapshot → operation → verify → audit
   проходит для apply / updatedb, snapshot физически создан
   до операции.
4. **Audit append-only.** **Две** audit row'а с двумя разными
   `operation_id`-ами — по одной на каждую mutating операцию
   (`apply_config_from_files`, `update_database_configuration`).
   Standalone `create_dump_snapshot` (A.2) audit row не пишет
   by design — он не идёт через `run_write_flow`. Pre-apply /
   pre-updatedb dump подтверждается через
   `details.dump_snapshot_path` соответствующей mutating row'и:
   `run_write_flow` создаёт pre-mutating snapshot сам и
   фиксирует его в success-деталях. Каждая из двух audit row'ей
   содержит `tool_name`, `status`, timestamp, без перетирания.
5. **Никакого silent fallback'а.** Ни в одной payload-ветке
   не должно быть `mode == "stub"` — если binary-backed branch
   падает, она падает honestly.

Что **не** доказывает успешный round-trip:

- Что произвольный structural diff в configuration tree
  apply'ится корректно (это зависит от семантики UpdateDBCfg
  на конкретной версии 1cv8 и конкретной операции, не от
  платформы).
- Что rollback от нежелательного UpdateDBCfg возможен
  автоматически (Phase 6 / Step 4 ограничил executable
  rollback whitelist'ом из двух atomic-tool'ов;
  UpdateDBCfg вне этого whitelist'а — это by design).
- Что credentials, передаваемые через `/N` `/P`, не
  попадают в логи (`onec-process-runner` не санитайзит argv;
  оператор сам отвечает за безопасное окружение).

## Типовые failure cases

### F1. Missing / broken binary contract

**Симптом:** `inspect_enterprise_foundation` фиксирует error
`foundation_onec_binary_path_missing_on_prod` (или
`foundation_onec_<op>_template_missing_on_prod`);
`get_real_stand_readiness.binary_present == False` или
`binary_executable_like == False`.

**Действие:** заполнить `onec_binary_path` и три template'а
до запуска шагов A.2–A.5. Шаги **не** должны запускаться,
если prereq inventory красный.

### F2. Unknown placeholder в template

**Симптом:** `result.ok == False` **до** старта subprocess'а;
`payload["data"]["binary_invoked"] == False`;
`payload["data"]["command_preview"] is None`;
`result.message` содержит unknown placeholder name.

**Действие:** убрать unknown placeholder из template'а или
заменить на whitelist-член. Это намеренная защита —
платформа **не** добавляет неизвестные placeholder'ы в
substitutions.

### F3. Real binary non-zero exit

**Симптом:** `result.ok == False`;
`operation_payload["mode"] == "binary-backed"`;
`operation_payload["binary_invoked"] == True`;
`operation_payload["exit_code"] != 0`; в `stderr_excerpt`
типично — человекочитаемая ошибка DESIGNER (логин не подошёл,
инфобаза залочена, расхождение метаданных, недостаточно
прав, и т.д.).

**Действие:** разобраться с самим стендом. Платформа не
должна делать silent fallback'а на stub mode — этой ветки
в коде нет.

### F4. Reference stand unavailable

**Симптом:** `binary_present == False`, или нет инфобазы по
`base_path`, или DESIGNER не пускает credentials, или
gateway/health blocked.

**Действие:** Step 6 honestly **не** закрывается. Зафиксируйте
отсутствующие prereq'ы, не запускайте шаги A.2–A.5,
**не** маскируйте это под success.

### F5. Один из трёх tool'ов всё ещё stub-backed

**Симптом:** `operation_payload["mode"] == "stub"` после того,
как product-config задал соответствующий template, и
`get_real_stand_readiness` показал ready.

**Действие:** это **failure**, не acceptable partial success.
Проверить, что path config'а реально загружается тем же
process'ом, который запускает write-server (один process,
одна `EnvironmentConfig`-инстанция, `onec_binary_path` и
`onec_<op>_command_template` оба не `None`). Если оба
заполнены, а `binary_invoked == False` — это баг
`runtime/binary_dispatch.py` или `tools.py`, заводите
issue.

## Ожидаемый минимум артефактов после успешного round-trip'а

- `<dump_path>/_snapshots/<A2-snapshot>/Configuration.xml`
  и поддиректории — реальный DumpCfg output.
- `<dump_path>/_snapshots/<A4-pre-apply>/...` — pre-apply
  snapshot, созданный `run_write_flow` перед apply.
- `<dump_path>/_snapshots/<A5-pre-updatedb>/...` — pre-updatedb
  snapshot, созданный `run_write_flow` перед UpdateDBCfg.
- `<dump_path>/.audit/audit.jsonl` — **две** append-only audit
  row'и с двумя разными `operation_id`-ами:
  - `tool_name="apply_config_from_files"`, `status="ok"`,
    `details.dump_snapshot_path=<A4-pre-apply>`;
  - `tool_name="update_database_configuration"`, `status="ok"`,
    `details.dump_snapshot_path=<A5-pre-updatedb>`.

  Отдельной audit row для standalone `create_dump_snapshot`
  (A.2) **не** создаётся — это зафиксировано в шаге A.2 выше
  и в post-check'е A.6 пункт 4.
- В каждом payload-ответе шесть unified honest-mode полей
  (`mode`, `binary_invoked`, `exit_code`, `command_preview`,
  `stdout_excerpt`, `stderr_excerpt`) populated по контракту
  Track A / Step 4.

## Что этот runbook доказывает

При успешном прогоне:

- честный **execution layer** трёх binary-backed
  write-tool'ов работает на реальном 1cv8 binary;
- `run_write_flow` choreography (preflight → snapshot →
  operation → verify → audit) выполняется на реальном
  стенде, а не только в synthetic-тестах с
  `sys.executable`;
- **dual-mode contract** Track A / Steps 2–4 действительно
  переключается на binary-backed branch в реальной среде;
- placeholder whitelist'ы per tool **держат** на render-time —
  невалидный argv не попадает в `subprocess`.

## Что этот runbook **не** доказывает

- Что **любой** structural diff в configuration tree пройдёт
  apply / UpdateDBCfg. Семантика 1С — за оператором.
- Что **любая** версия 1cv8 поддерживает указанные ключи.
  Platform binary-version-sniffing не делает.
- Что **production** stand готов к этому сценарию. Reference
  stand специально дешёвый и dedicated — production prerolls
  выходят за рамки Track A.
- Что rollback после неудачного UpdateDBCfg делается
  автоматически — platform этой возможности не открывает
  (executable rollback ограничен whitelist'ом из двух
  atomic write-tool'ов; см. Phase 6 / Step 4).

## Связанные документы

- `docs/runbooks.md` — общие Phase 6 / Step 7 recipes (один файл,
  legacy формат).
- `apps/mcp-write-server/README.md` — описание Track A
  binary-backed write-tool'ов и unified `binary_dispatch`
  helper'а.
- `apps/platform/README.md` — описание product-layer surface'а
  (`run_real_stand_smoke_test`, `inspect_enterprise_foundation`),
  обновлённого в Track A / Step 5.
- `docs/architecture/track-a-real-write-path-plan.md` —
  оригинальный план Track A.
- `docs/architecture/track-a-real-write-path-step-map.md` —
  step map трека.
