# Multi-Version 1C Smoke Matrix — operator runbook

> **Track:** Parallel Track E — Multi-Version 1C Smoke Matrix.
> **Step:** Step 3 deliverable (operator scaffolding). Companion
> file: [`docs/version-support-matrix.md`](../version-support-matrix.md).
> Frozen contract: [`docs/architecture/track-e-smoke-scenario.md`](../architecture/track-e-smoke-scenario.md).
> Current evidence: [`docs/architecture/track-e-current-evidence-audit.md`](../architecture/track-e-current-evidence-audit.md).

> **Status:** docs-only scaffolding. Этот runbook **сам** по
> себе ничего не запускает; он описывает, как оператор
> прогоняет `frozen-smoke-v1` на дополнительной 1С версии в
> рамках Track E / Step 4. Никаких 1cv8.exe runs не делается на
> Step 3.

---

## 1. Purpose / scope

Этот runbook отвечает на **один** вопрос:

> «Как именно оператор прогоняет frozen-smoke-v1 на operator-
> supplied 1С версии и записывает evidence в
> `docs/version-support-matrix.md` — без расширения сценария и
> без новых платформенных изменений?»

Runbook **не**:
- запускает что-либо «from repo» — он только описывает
  procedure, оператор сам решает прогнать;
- расширяет frozen-smoke-v1 (ровно одна операция:
  `create_dump_snapshot` через `/DumpConfigToFiles`);
- предписывает operator infrastructure (operator выбирает
  binary path, test infobase, OS, env management);
- делает support claims на конкретные 1С версии до того, как
  фактическая evidence row появится в matrix.

Runbook предполагает Windows-first environment — это
соответствует current evidence baseline и Phase 6 / Track B
delivery scaffolding.

---

## 2. Preconditions

### 2.1 Repository state

- Working tree clean. Если есть незакоммиченные изменения — не
  смешивайте их с Track E / Step 4 evidence run.
- HEAD на ветке, где Track E / Step 3 уже закрыт (т.е.
  существуют `docs/runbooks/track-e-multi-version-smoke-matrix.md`
  и `docs/version-support-matrix.md`).
- `verify-release.ps1 -AllowDirtyTree -SkipSelfcheck` GREEN
  (проверка, что repo invariants не сломаны).

### 2.2 Operator-side install

- `1cv8.exe` нужной target version family и build установлен
  локально или доступен по UNC-пути; absolute path известен.
- Test 1С infobase, file-based, на которой оператор готов
  открыть DESIGNER session. Рекомендация — **throwaway test
  base**, не production. Скрипт `frozen-smoke-v1` read-only
  из перспективы 1С базы (только dump), но DESIGNER session
  обычно требует, чтобы база не была занята другим клиентом.
- Disk space под dump output — обычно несколько MB на запуск.

### 2.3 Operator-side credentials

- DESIGNER user / password для test base заданы как env vars
  через Track D / Step 3 contract:
  ```powershell
  $env:ONEC_DESIGNER_USER     = '<your designer user>'
  $env:ONEC_DESIGNER_PASSWORD = '<your designer password>'
  ```
- **Никаких** cleartext credentials в JSON-config'е. Если
  оператор скоммитит cleartext в tracked `*.config.json`,
  Track D / Step 5 8-й check (`Credential template hygiene`)
  в `verify-release.ps1` поднимет WARN.

### 2.4 Tooling

- PowerShell 5.1+ или PowerShell 7+.
- Python 3.11.
- `git` для repo state checks.
- PYTHONPATH bootstrap'ом подгружены 11 internal `src/`
  директорий (через `scripts/dev/bootstrap_paths.ps1` или
  через `scripts/dev/launch.ps1`).

---

## 3. What this runbook does NOT do

- **Не** расширяет `frozen-smoke-v1` сценарий (см. section 4
  ниже).
- **Не** запускает `apply_config_from_files` или
  `update_database_configuration` на operator-side базах.
  Никаких mutating операций.
- **Не** проверяет performance, latency, throughput, memory
  use или resource consumption.
- **Не** запускает stress / load / fuzzing.
- **Не** делает регрессионных проверок поверх dump'а.
- **Не** проверяет server-mode стенды (только file-based).
- **Не** проверяет pre-`8.3` major families (только `8.3.<N>`
  versions).
- **Не** делает feature parity claims между versions.
- **Не** делает «universal version support» marketing.
- **Не** автоматизирует прогон через CI runner (нет такой
  infra в repo; physical operator territory).
- **Не** меняет MCP registries (`read=15 / write=25 /
  intelligence=16`).

---

## 4. Frozen scenario reference

Полный контракт сценария — в
[`docs/architecture/track-e-smoke-scenario.md`](../architecture/track-e-smoke-scenario.md).
Краткое резюме здесь — **не** заменяет frozen contract, только
быстрая навигация:

- **Scenario name:** `frozen-smoke-v1`.
- **What it does:** одна операция —
  `create_dump_snapshot(environment_name="<target>")` через
  `/DumpConfigToFiles` argv. Read-only из перспективы 1С базы.
- **PASS criteria** (все одновременно):
  - payload `mode='binary-backed'`,
  - payload `binary_invoked=True`,
  - payload `exit_code=0`,
  - dump tree существует на диске под `dump_path`,
  - dump tree содержит как минимум `Configuration.xml`,
  - никаких error / fatal stderr-сообщений.
- **FAIL criteria:** `exit_code != 0`, или timeout (300s
  default), или silent no-op (пустой output после
  `exit_code=0`), или render-fail (env-token issue).
- **NOT RUN:** binary недоступен / test base нет / operator
  decision.

Если возникает соблазн отступить от frozen-smoke-v1 — это
сигнал, что нужна отдельная корректировка через явный track /
step (через bump до `frozen-smoke-v2`), **не** in-flight
правка во время Step 4.

---

## 5. Required operator inputs

Перед прогоном operator определяет (для записи в matrix
позже):

| # | Input | Пример | Notes |
|---|---|---|---|
| 1 | Target version family | `8.3.<minor>` (e.g. `8.3.26`) | `8.3.<other>` чем reference `8.3.27` |
| 2 | Target build | `1234` | full build number |
| 3 | OS arch | `x64` или `x86` | по installed binary |
| 4 | Absolute binary path | `C:/Program Files/1cv8/8.3.<v>/bin/1cv8.exe` | без credentials |
| 5 | Test infobase path | `C:/path/to/test-base` | file-based, throwaway |
| 6 | Dump output path | `C:/path/to/dump-output/<target-version>/` | пустая или несуществующая директория |
| 7 | Work dir | `C:/path/to/work/<target-version>/` | под bootstrap |

**Все** эти inputs operator-supplied. Repo не содержит
operator stand'ов; матрица фиксирует только evidence rows.

---

## 6. Execution procedure

### Step 6.1 — Подготовка product config

Скопируйте shape из
[`examples/demo-infobase/infobase6.config.json`](../../examples/demo-infobase/infobase6.config.json)
в operator-private location (например, `%TEMP%/track-e-<version>.config.json`),
**не** в repo. Подмените:

- `default_environment` → имя environment'а (любое read-only-
  ish имя, не credentials, e.g. `track-e-8327` для
  `8.3.27`-aligned target);
- environment block:
  - `base_path` → operator's test infobase path;
  - `dump_path` → operator's dump output path;
  - `onec_binary_path` → absolute path к target version
    1cv8.exe;
  - `http_base_url` → keep `http://...invalid/no-publication`
    placeholder (Track A pattern; платформа не обращается
    к HTTP в `frozen-smoke-v1`);
  - `publication_name` → любое placeholder-имя;
  - `timeout_seconds` → `600` (default);
  - `allow_write` → `false` (frozen-smoke-v1 не пишет в базу);
- `bootstrap.work_dir` → operator's work dir;
- **Только один** template field — `onec_dumpcfg_command_template`:
  ```jsonc
  "onec_dumpcfg_command_template": [
    "{binary_path}",
    "DESIGNER",
    "/F", "{base_path}",
    "/N", "${ENV:ONEC_DESIGNER_USER}",
    "/P", "${ENV:ONEC_DESIGNER_PASSWORD}",
    "/DumpCfg", "{output_path}",
    "/DisableStartupMessages"
  ]
  ```
  `applycfg` / `updatedb` template'ы **не** добавлять —
  frozen-smoke-v1 их не использует.

**Никаких real credentials в JSON-файле.** Только
`${ENV:NAME}` substitution из Track D / Step 3 contract.

> **Note про argv-grammar drift.** На некоторых старых versions
> `/DisableStartupMessages` может быть недостаточен — runbook
> `track-a-reference-stand-round-trip.md` стр. 244–248
> упоминает, что может понадобиться `/AppAutoCheckMode`-стиль
> flag. Если это применимо, добавьте дополнительный argv
> элемент **в этот же template** (зафиксируйте отклонение в
> matrix column 11 «Key deviations»). Если требуется
> переименование основного `/DumpCfg` ключа — это уже **другой
> scenario name** (значит target version не покрывается
> frozen-smoke-v1), запишите как FAIL с пометкой о
> argv-grammar incompatibility.

### Step 6.2 — Выставление env vars

В PowerShell session (та же, в которой будет запуск):

```powershell
$env:ONEC_DESIGNER_USER     = '<your designer user>'
$env:ONEC_DESIGNER_PASSWORD = '<your designer password>'
```

Никогда не сохранять эту session с history dump'ом в shared
location.

### Step 6.3 — Bootstrap PYTHONPATH

```powershell
. C:\Tools\1c-agent-platform\scripts\dev\bootstrap_paths.ps1
```

Или через umbrella:
```powershell
.\scripts\dev\launch.ps1 selfcheck
```
для проверки, что imports green перед прогоном.

### Step 6.4 — Pre-check: working tree clean & verify

```powershell
git -C C:\Tools\1c-agent-platform status
.\scripts\release\verify-release.ps1 -SkipSelfcheck
```

Working tree должен быть clean **до** evidence run, чтобы
любой output не смешался с unrelated changes.

### Step 6.5 — Запуск frozen-smoke-v1

В PowerShell session с выставленными env vars:

```powershell
.\scripts\dev\launch.ps1 run -- - @'
import json
from onec_platform.bootstrap import bootstrap_product_from_json_file
from mcp_write_server.tools.snapshots import create_dump_snapshot

config_path = r"%TEMP%\track-e-<version>.config.json"
ctx = bootstrap_product_from_json_file(config_path)
result = create_dump_snapshot(
    environment_name=ctx.product_config.default_environment,
)
print(json.dumps(result, indent=2, default=str))
'@
```

(Точный API import paths могут варьироваться по версии
платформы; смотрите `apps/mcp-write-server/src/mcp_write_server/`
структуру в текущем checkout'е. Operator может также
использовать REPL через `.\scripts\dev\launch.ps1 repl`.)

`subprocess` запускается через `onec_process_runner` с
timeout 300s (фиксированный cap из Track A / Step 4
unification). Никакого `shell=True` нигде.

### Step 6.6 — Post-run проверки

Проверить **все** одновременно:

1. Печать `result` содержит:
   - `mode='binary-backed'`,
   - `binary_invoked=True`,
   - `exit_code=0`,
   - `command_preview` с `<redacted>` после `/P`
     (Track D / Step 3 redaction discipline),
   - `stdout_excerpt` без error-сообщений,
   - `stderr_excerpt` без error / fatal сообщений
     (warnings допустимы).
2. На диске под `dump_path` появилась директория с:
   - `Configuration.xml` (хотя бы),
   - типично также `ConfigDumpInfo.xml`, `1Cv8.cf` и
     директории объектов конфигурации.
3. `subprocess` завершился сам, без timeout-kill'а.

Если хотя бы один пункт не выполняется — это **FAIL** или
**timeout** verdict (см. раздел 8).

### Step 6.7 — Cleanup (optional)

После записи evidence в matrix (раздел 7) operator может
удалить dump output локально. Repo не хранит operator
dump trees — это operator infrastructure.

`%TEMP%/track-e-<version>.config.json` следует удалить /
очистить, особенно если в этом сеансе env vars содержали
real credentials.

---

## 7. What to record after each run

Operator заполняет **одну** новую row в
[`docs/version-support-matrix.md`](../version-support-matrix.md)
по 12-column frozen contract из Step 2 scenario doc:

1. **Version family** — `8.3.<minor>` target (e.g. `8.3.26`).
2. **Build** — full build number (e.g. `1936`).
3. **OS arch** — `x64` / `x86`.
4. **Binary path** — absolute path к `1cv8.exe`. Operator
   выбирает, нужно ли прятать internal-only path: если path
   leakable secret (UNC к internal share) — заменить на
   sanitised summary (`<UNC share — operator infra>`).
5. **Stand type** — `file-based` (frozen-smoke-v1 не
   покрывает server-mode).
6. **Scenario** — `frozen-smoke-v1` (только это значение для
   additional rows; reference row может иметь
   `stronger-than-frozen-smoke-v1` formulation — см.
   `docs/version-support-matrix.md` reference row).
7. **Run date** — `YYYY-MM-DD` (день фактического прогона).
8. **Verdict** — `PASS` / `FAIL` / `NOT RUN` (см. раздел 8).
9. **Audit row reference** — для frozen-smoke-v1 standalone
   `create_dump_snapshot` audit row не пишется by design
   (он не идёт через `run_write_flow`). Operator может
   указать `none (smoke-v1 — no audit row)` либо ссылку на
   manual log of payload fields, если оператор сохранил.
10. **Snapshot tree path** — относительный или absolute path
    к operator-side dump output. Обычно operator-private,
    может быть `<operator infra — not committed>` если
    operator не делится этим публично.
11. **Key deviations** — argv-grammar изменения, добавленные
    flags (e.g. «added `/AppAutoCheckMode`»), special
    timeout settings, etc. Если ничего не отклонялось —
    `none`.
12. **Notes** — короткий free-text: например, «timeout
    extended to 600s out of caution» или «test base создана
    из шаблона X». Никаких PII / credentials.

**Что НЕ должно попасть в row:**
- real credentials (DESIGNER user / password / cleartext env
  values);
- internal stand IP / hostname / publication URL'ы, если
  они leakable secrets;
- customer / client identifiers;
- 1С configuration-specific business data.

---

## 8. PASS / FAIL / NOT RUN handling

### PASS

Все шесть условий из section 4 + dump tree содержит хотя бы
`Configuration.xml`. Записать row с `Verdict = PASS`.

### FAIL

Любое из:
- `exit_code != 0` после `mode='binary-backed' /
  binary_invoked=True` — записать `FAIL`, в Notes пометить
  «binary-backed run failed на этой версии». Honest
  formulation: версия **не отработала** по этому scenario'ю,
  не «версия не поддерживается».
- timeout (subprocess hung > 300s) — `FAIL`, Notes
  «timeout; possibly /DisableStartupMessages не достаточен».
- silent no-op (пустой output при `exit_code=0`) — `FAIL`,
  Notes «1cv8 проглотил unknown flag без error».
- render-fail (`mode='binary-backed'`, `binary_invoked=False`,
  `command_preview=None`) — `FAIL`, Notes «operator setup
  issue (env-token resolution); not a version issue».

**FAIL row фиксируется в matrix так же честно, как PASS row.**

### NOT RUN

- Operator не предоставил binary этой version family — `NOT RUN`.
- Operator не имеет test base подходящего shape'а — `NOT RUN`.
- Operator решил не запускать в этой итерации — `NOT RUN`.

`NOT RUN` row может быть включена как honest placeholder,
чтобы reader matrix'ы видел осознанное рассмотрение версии
без evidence. Это **не** failure — это **gap notation**.

---

## 9. Evidence capture rules

### Что попадает в repo
- Одна evidence row в `docs/version-support-matrix.md` (12
  columns, sanitised).

### Что **не** попадает в repo
- Operator's dump tree (это operator infrastructure;
  reference dump tree исторически в repo — Track A artifact,
  не norm для Track E additional rows).
- Operator's audit.jsonl — frozen-smoke-v1 standalone audit
  row не пишет; отдельно operator logs это его дело.
- Real credentials или env values.
- Operator's full product config JSON (operator-private,
  stays local).
- Performance / timing data (out-of-scope).

### Если operator решит делиться full evidence

Operator может, по собственному решению, поделиться dump
tree через separate side channel (issue tracker, internal
share). Но `docs/version-support-matrix.md` row — это
**single source of truth** для evidence claim. Без row в
matrix'е — нет claim'а.

---

## 10. Common stop conditions

Остановиться и **не** записывать row, если:

- Working tree dirty с unrelated changes — может загрязнить
  matrix commit.
- `.\scripts\release\verify-release.ps1 -SkipSelfcheck`
  возвращает RED по причинам не связанным с Track E run —
  чинить отдельным заходом.
- Real credentials попали в command_preview (это означает
  Track D / Step 3 redaction broken — это уже security
  incident, не Track E proceeding).
- Subprocess запустил GUI dialog (DESIGNER startup screen
  или error window) — kill, добавить flag, повторить с
  отметкой в Key deviations. Если повтор GUI — записать
  `FAIL` с Notes «GUI startup; argv-grammar adjustment
  needed».
- Test base заблокирована другим клиентом — закрыть клиент,
  повторить. Если воспроизводится — `NOT RUN` с Notes
  «base contention».

---

## 11. Honest constraints

Этот runbook ship'ит **процесс**, не **evidence**. Сам по
себе он не доказывает совместимость ни с одной additional
версией. Доказательство — в matrix-table after Step 4
operator runs.

Track E после closure даст «smoke evidence на N версиях по
одному узкому сценарию». Это:

- **не** «universal version support»,
- **не** enterprise certification,
- **не** performance characteristics на разных версиях,
- **не** long-tail backwards compatibility guarantee,
- **не** substitute для full QA-программы.

`frozen-smoke-v1` как design — проверка **argv-grammar
sanity** + **binary subprocess execution** + **output format
sanity**, ничего больше. Любые более широкие claims требуют
отдельного track / scope.

---

## 12. Step 4 closure boundary (на что operator опирается)

Track E / Step 4 закрывается, когда:

- ≥ 1 additional row ship'нута в `docs/version-support-matrix.md`
  с PASS / FAIL / NOT RUN verdict; **либо**
- operator явно зафиксировал operator-supplied gap (не смог
  предоставить additional binary'и) с notation в matrix —
  без имитации evidence. Это **не** track failure, это
  honest closure под фактический evidence-уровень.

Step 5 после этого выровнит SECURITY.md / release-handoff.md /
README / CHANGELOG support statement под **фактически
собранный** evidence-уровень, не больше.
