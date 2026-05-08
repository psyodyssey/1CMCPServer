# Track E — frozen smoke scenario and version selection criteria

> **Companion files:**
> `track-e-multi-version-smoke-matrix-plan.md`,
> `track-e-multi-version-smoke-matrix-step-map.md`,
> `track-e-current-evidence-audit.md` (Step 2 partner — current
> evidence baseline).

> **Status:** Track E / Step 2 deliverable. **FROZEN**.
> Documentation-only. После этого commit'а scenario не должен
> изменяться по ходу будущих прогонов; иначе comparability
> между evidence row'ами ломается. Любая будущая корректировка
> scenario — отдельный change через явный track / step, **не**
> ad-hoc правка во время Step 4 runs.

---

## 1. Purpose / scope

Этот документ отвечает на **один** вопрос:

> «Какой exact smoke-сценарий и какие version-selection criteria
> мы замораживаем для всех будущих прогонов в рамках Track E
> (и любых post-closure additional row'ов)?»

Документ **не** описывает текущее evidence (см.
`track-e-current-evidence-audit.md`), не определяет matrix-table
формат (Step 3 deliverable), не описывает operator runbook
(Step 3 deliverable), не корректирует support-statement
(Step 5 deliverable), не делает реальных прогонов 1cv8.exe
(Step 4 — operator gate).

### Что значит «frozen» в этом документе

- Scenario / acceptance criteria / required evidence fields —
  фиксированы на момент closure Step 2 и **не** меняются
  при добавлении новых evidence row'ов.
- Если на Step 4 / post-closure обнаружится, что scenario
  объективно не работает на target version family (например,
  `/DumpConfigToFiles` переименован), это **failure row**
  (`FAIL` verdict) для этой version, **не** изменение scenario.
- Расширение scenario (например, добавить full round-trip как
  «extended» smoke) — отдельный track / step, не in-flight
  правка во время Step 4.

---

## 2. Candidate version-selection criteria

Эти criteria **principle-based** и не привязаны к точным
номерам. Точные номера для конкретного operator's matrix
определяются на Step 4 на основании того, что у operator'а
реально доступно (operator gate).

### 2.1 Какие версии подходят как evidence row

**Обязательно** — reference row:
- 1С version family `8.3.27`, build `1859`, Windows x64. Это
  **уже** есть как proven (`track-e-current-evidence-audit.md`
  section 2). Reference row не требует нового прогона на
  Step 4 — она копируется из existing audit'а.

**Рекомендуемые additional row'ы** (operator gate, Step 4):
- **Одна newer version family** (`8.3.<N>` где N > 27, если
  operator'у такой бинарь доступен) — даёт forward-compat
  evidence.
- **Одна older version family** (`8.3.<N>` где N < 27, если
  operator'у такой бинарь доступен) — даёт backward-compat
  evidence.

**Default target N additional rows:** 2 (one newer + one
older).

**Минимум для closure Track E с non-gap result:** 1 additional
row (хотя бы одна другая `8.3.<minor>`). Если operator
дополнительные binary'и не предоставит — Track E закрывается
с явным operator-supplied gap (см. `track-e-multi-version-smoke-matrix-plan.md`
Q4 / Step 4).

**Максимум для одного захода Track E:** 3 additional rows.
Больше — это уже отдельный extended track post-closure.

### 2.2 Какие версии **не** подходят как additional row

- **Различные builds одной и той же minor family.** Например,
  `8.3.27.1859` (proven reference) vs `8.3.27.1936` (x86 build
  на dev-машине). Это **same** version family — не
  засчитывается за additional evidence. Build difference
  внутри `8.3.<N>` обычно — patch-level, без argv-grammar
  changes.
- **Pre-`8.3` major families** (`8.2.x`, `8.1.x`, `8.0.x`).
  Out-of-scope baseline: archaic argv-grammar, существенно
  отличающийся DESIGNER mode, missing required flags,
  отсутствие современных placement assumptions. Если такие
  стенды у operator'а есть — это отдельный legacy track,
  не Track E.
- **Pre-release / dev / nightly builds.** Out-of-scope:
  argv-grammar может расходиться с production releases.
  Только released stable versions.
- **Server-based stand'ы как primary smoke target.**
  Out-of-scope: Track E фиксирует scenario для **file-based**
  стендов (см. section 4 ниже). Server-based — отдельный
  track.

### 2.3 Что фиксирует principle, а не precise numbers

Принципиальный wording:

- «one newer minor`8.3.<N>` family» — конкретный N **не**
  фиксируется в plan; точное значение operator выбирает на
  Step 4 на основании наличия binary'а;
- «one older minor`8.3.<N>` family» — то же самое;
- repo не делает claims на specific version numbers до того,
  как Step 4 ship'ит фактические evidence row'ы.

---

## 3. Proposed matrix shape

Matrix-table doc (`docs/version-support-matrix.md`) — Step 3
deliverable, не Step 2. Здесь фиксируется только **shape**
ожидаемой таблицы, чтобы Step 3 не переизобретал колонки.

**Required columns** для каждой evidence row:

| # | Column | Что |
|---|---|---|
| 1 | Version family | `8.3.<minor>` (e.g. `8.3.27`) |
| 2 | Build | full build number (e.g. `1859`) |
| 3 | OS arch | `x64` / `x86` |
| 4 | Binary path | absolute path к 1cv8.exe (operator-supplied; в plan'е без credentials) |
| 5 | Stand type | `file-based` (only baseline shape для Track E) |
| 6 | Scenario | `frozen-smoke-v1` (см. section 4) |
| 7 | Run date | `YYYY-MM-DD` |
| 8 | Verdict | `PASS` / `FAIL` / `NOT RUN` (см. section 5) |
| 9 | Audit row reference | path к operator's audit.jsonl + line N (или `none` для reference row, потому что reference row копируется из Track A / Step 6 audit) |
| 10 | Snapshot tree path | path к dump output на operator-side диске |
| 11 | Key deviations | argv-grammar изменения (e.g. «added `/AppAutoCheckMode`») или `none` |
| 12 | Notes | краткий free-text комментарий, не PII / not credentials |

**Что НЕ должно быть в колонках:**
- никаких real credentials (DESIGNER user / password / cleartext
  env value);
- никаких internal stand IP / hostname / publication URL'ов
  (если они leakable secrets);
- никаких customer / client identifiers;
- никаких 1С configuration-specific business data.

---

## 4. Frozen smoke scenario

Это **THE** scenario для Track E. Один и тот же сценарий
прогоняется на каждой target version. Comparability —
обязательное свойство; именно поэтому scenario frozen.

### 4.1 Scenario name

`frozen-smoke-v1` — версионное имя, чтобы любая будущая
корректировка scenario явно требовала bump до `frozen-smoke-v2`
(через отдельный track / step, не ad-hoc).

### 4.2 What it does

**Cut-down вариант Track A round-trip'а — только A.2 (dump-only).**

Operator на target version выполняет ровно одну операцию:

```
create_dump_snapshot(environment_name="<target>")
```

через `/DumpConfigToFiles` argv. Это **read-only** из
перспективы 1С базы — dump просто экспортирует конфиг во
внешние файлы; ни metadata, ни данные базы **не мутируются**.

**Почему именно cut-down, а не full round-trip:**
- **Read-only из перспективы 1С базы** — operator может
  прогнать на production-like base без риска. Full round-trip
  (apply / updatedb) меняет data state и требует write-allowed
  config, который operator может не хотеть открывать на
  каждой target version.
- **Минимальная sufficient evidence-единица** — доказывает
  argv-grammar compatibility + binary subprocess execution +
  output format compatibility одним вызовом. Этого достаточно
  для честного support-statement по этой версии.
- **Узкий сценарий = чистая comparability** — одна операция
  на всех версиях, никакой room для interpretation drift.
- Full round-trip purity уже покрыт reference row (Track A /
  Step 6 evidence). Track E расширяет **breadth across
  versions**, не **depth on each version**.

### 4.3 What it does NOT do

- **Не** запускает `apply_config_from_files`. Никаких
  config-mutating операций на operator-side базах.
- **Не** запускает `update_database_configuration`. Никаких
  database schema changes.
- **Не** делает feature parity claims между версиями
  (никаких сравнений `Catalogs/SampleCatalog.xml` byte-by-byte
  между output'ами разных versions; output может legitimately
  отличаться).
- **Не** замеряет performance (timings irrelevant; smoke —
  binary verdict, не latency).
- **Не** запускает stress / load / fuzzing.
- **Не** проверяет regression suites поверх dump'а.
- **Не** проверяет server-mode стенды.
- **Не** проверяет backwards compatibility всей платформы на
  старых stack'ах (Python 3.10-, Windows 8, etc.).

### 4.4 Required prerequisites (operator side)

Operator перед прогоном должен иметь:

1. Installed `1cv8.exe` нужной version family и build —
   absolute path известен оператору.
2. Test 1С infobase, file-based, на которой operator
   готов прогнать DESIGNER session. Recommendation —
   throwaway test base, не production. (Scenario read-only
   из перспективы базы, но **в сторону** 1С GUI открытие
   DESIGNER session обычно требует, чтобы база не была занята
   другим клиентом.)
3. DESIGNER credentials для этой test base — задаются через
   Track D / Step 3 env-substitution
   (`${ENV:ONEC_DESIGNER_USER}`,
   `${ENV:ONEC_DESIGNER_PASSWORD}`); **никаких** cleartext
   в config'е, который коммитится в operator's repo /
   shared infrastructure.
4. Disk space под dump output (обычно несколько MB).
5. PowerShell session с PYTHONPATH bootstrap'ом
   (`scripts/dev/bootstrap_paths.ps1`).

### 4.5 Steps oversight

Точная step-by-step операторская инструкция — Step 3
deliverable (`docs/runbooks/track-e-multi-version-smoke-matrix.md`).
Здесь только sense:

1. Operator подготавливает product-config для target version
   (дублируя shape `examples/demo-infobase/infobase6.config.json`
   с подменённым `onec_binary_path` + `base_path` + `dump_path`).
2. Operator выставляет env vars для DESIGNER credentials.
3. Operator вызывает `create_dump_snapshot` через
   product-layer API (через Python helper, не через MCP
   transport — production-grade transport out-of-scope).
4. Operator проверяет payload поля
   (`mode='binary-backed'`, `binary_invoked=True`,
   `exit_code=0`).
5. Operator проверяет, что dump tree физически записан под
   `dump_path` и содержит хотя бы `Configuration.xml`.
6. Operator записывает evidence row в matrix-table.

---

## 5. PASS / FAIL / NOT RUN semantics

### 5.1 PASS verdict

Все нижеперечисленные условия должны выполниться **одновременно**:

- payload `mode='binary-backed'` (binary-backed branch выбран,
  не stub fallback);
- payload `binary_invoked=True` (subprocess реально стартовал);
- payload `exit_code=0` (1cv8 завершился без ошибки);
- output dump tree существует на диске под operator's
  `dump_path`;
- output dump tree содержит как минимум `Configuration.xml`
  (любая ненулевая длина — sufficient; byte-level content
  comparison **не** часть scenario);
- никаких unexpected stderr-сообщений с уровнем error /
  fatal в `stderr_excerpt` (warnings допустимы).

### 5.2 FAIL verdict

Любой из:

- payload `mode='binary-backed'` но `exit_code != 0`
  (subprocess стартовал, но упал) — **FAIL: binary-backed
  run failed на этой версии**. Honest formulation: «версия
  не отработала по этому scenario'ю», **не** «версия не
  поддерживается».
- payload `mode='binary-backed'` но subprocess hung > timeout
  (300s default per `binary_dispatch.py`) — **FAIL: timeout**.
  Возможная причина — argv-grammar reject и платформа повисла
  на startup dialog'е (особенно если `/DisableStartupMessages`
  не работает на target version).
- output dump tree пустой или отсутствует после `exit_code=0`
  — **FAIL: silent no-op**. Это редкое, но возможное
  поведение, если 1cv8 проглатывает unknown flag без error.
- payload `command_preview=None` + `mode='binary-backed'`
  с `binary_invoked=False` — **FAIL: render-fail**. Обычно
  значит env-substitution token не разрешился (Track D /
  Step 3 contract: missing / empty / partial env). Это
  **operator setup issue**, не version issue, но row пишется
  как `FAIL` с пометкой «operator setup» в Notes.

**FAIL row фиксируется в matrix-table так же честно, как
PASS row.** Track E не скрывает failures; FAIL row — это
**information**, а не повод не записывать row.

### 5.3 NOT RUN verdict

- Operator не предоставил binary этой version family —
  `NOT RUN`. Honest: не делать вид, что версия проверена.
- Operator не имел доступа к test-base подходящего shape'а —
  `NOT RUN`.
- Operator принял решение не запускать на этой версии в этой
  итерации — `NOT RUN`.

`NOT RUN` row может быть включена в matrix как honest
placeholder, чтобы Q&A reader видел, что версия осознанно
рассмотрена, но не покрыта evidence'ом. Это **не** failure —
это **honest gap notation**.

### 5.4 Что **никогда** не считается PASS

- Inferred / argued / theoretically-should-work — **никогда не
  PASS**. PASS требует physical artifact (dump tree + payload
  fields).
- «Прогоняли когда-то на похожей версии» — **никогда не PASS**.
  Каждая version family требует своей evidence row.
- Build-level extrapolation (e.g. «`8.3.27.1859` PASS, значит
  `8.3.27.1936` тоже PASS») — **никогда не PASS** на основании
  этого extrapolation'а одиночно. Это, опять же, **same** version
  family — она и не считалась бы за additional evidence row в
  любом случае (см. section 2.2).

---

## 6. Required evidence to record

Ровно **что** должно быть зафиксировано на диске в результате
PASS row на target version:

1. **Dump output tree** — operator's `dump_path/<target-version-name>/`
   (или эквивалентный per-target subpath) должен содержать
   хотя бы `Configuration.xml`. Tree остаётся на operator-side
   диске; в repo он **не** коммитится (target operator stand'ы —
   это operator infrastructure, не shared evidence).
2. **Audit.jsonl line** — для cut-down `create_dump_snapshot`
   audit row **не** пишется по конструкции (см.
   `track-e-current-evidence-audit.md` section 2.3:
   standalone `create_dump_snapshot` через `run_write_flow`
   не идёт). Поэтому evidence для PASS row для
   smoke scenario — это:
   - operator's manual log of payload fields
     (`mode`, `binary_invoked`, `exit_code`,
     `command_preview`, `stdout_excerpt`,
     `stderr_excerpt`); operator может скопировать
     payload в текстовый файл рядом с dump tree;
   - физический dump tree существует.
3. **Matrix-table row** в `docs/version-support-matrix.md`
   (Step 3 deliverable заполняет этот файл).
   Reference row — копируется из существующего
   Track A / Step 6 audit без нового прогона.

**Что НЕ должно попадать в repo как evidence:**

- Реальные credentials.
- Operator's full `1cv8.exe` дамп.
- Содержимое operator's test infobase'ы (`1Cv8.1CD`).
- Operator's audit.jsonl полностью (только reference на путь
  + line, если operator решит ship'нуть).
- Identifiable customer / business data.

---

## 7. Non-goals

Track E **не** делает (повтор для ясности):

- никаких performance / latency / throughput замеров;
- никакого stress / load testing;
- никакого fuzzing / mutation testing;
- никакого full regression suite;
- никаких feature parity claims между versions;
- никакого «support all 1С versions» marketing;
- никаких enterprise certification claims;
- никакого backwards-compat guarantee для будущих 1С
  версий, которые ещё не вышли;
- никакого CI matrix runner для multi-version 1cv8 (нет
  такой infra; operator territory);
- никаких новых MCP tools (registries `read=15 / write=25 /
  intelligence=16` без drift'а);
- никаких production code changes в платформе.

---

## 8. Step 4 execution boundary

Step 4 — единственный шаг Track E, который **запускает
1cv8.exe**. И только operator-driven, на operator
infrastructure.

Step 4 **обязан** держаться внутри границ этого документа:

- использовать **только** `frozen-smoke-v1` scenario из
  section 4;
- использовать **только** version-selection criteria из
  section 2;
- использовать **только** PASS / FAIL / NOT RUN semantics из
  section 5;
- записывать **только** required evidence fields из section 6;
- **не** расширять scenario (например, не добавлять
  `apply_config_from_files` «потому что у меня была свободная
  test база»);
- **не** менять column shape матрицы (section 3);
- если возникает соблазн отступить от scenario — это сигнал,
  что нужен отдельный track / step, не in-flight правка
  Step 4.

Step 4 closure для одной additional version family — это
ровно одна row в `docs/version-support-matrix.md`, заполненная
по этому документу. Для Track E closure достаточно: reference
row + ≥1 additional row (или, если operator не смог
предоставить additional version, явно зафиксированный
operator-supplied gap).

---

## 9. Honest summary (one paragraph)

Track E фиксирует **frozen** smoke scenario `frozen-smoke-v1`:
один cut-down `create_dump_snapshot` через
`/DumpConfigToFiles` на operator-supplied test infobase'е, на
каждой operator-supplied target 1С version family, с явным
PASS / FAIL / NOT RUN verdict'ом и фиксированным набором
evidence-полей. Reference row (`8.3.27.1859`) копируется из
existing Track A / Step 6 evidence без нового прогона.
Additional row'ы — operator-driven Step 4 на operator
infrastructure. Scenario **не меняется** между прогонами;
любая корректировка — отдельный track. Scope deliberately
узкий: cross-version comparability + binary-backed argv-grammar
sanity, **не** full QA / performance / certification. Track E
после closure даёт **evidence на N версиях по одному узкому
сценарию**, не «universal version support».
