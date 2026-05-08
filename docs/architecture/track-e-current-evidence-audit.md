# Track E — current evidence audit

> **Companion files:**
> `track-e-multi-version-smoke-matrix-plan.md`,
> `track-e-multi-version-smoke-matrix-step-map.md`,
> `track-e-smoke-scenario.md` (Step 2 partner — frozen scenario
> definition).

> **Status:** Track E / Step 2 deliverable. Documentation-only.
> Read-only описание текущей evidence base — без новых прогонов
> 1cv8.exe и без фантазий о matrix'е, которой ещё нет.

---

## 1. Purpose / scope

Этот документ отвечает на **один** вопрос:

> «Что у нас на сегодня **реально** доказано по 1С version
> evidence — какая версия, каким сценарием, какими физическими
> артефактами?»

Документ **не** отвечает на вопросы про будущие прогоны
(см. `track-e-smoke-scenario.md`), про matrix-table формат
(см. Step 3 deliverable), про operator runbook (см. Step 3
deliverable), про support statement в SECURITY.md /
release-handoff.md (см. Step 5 deliverable).

Документ **строго отделяет** четыре категории:

- **Proven** — есть прямой artefact на диске или audit-row,
  который можно показать.
- **Inferred** — следует из архитектуры или из honest reasoning,
  но прямого evidence row нет.
- **Not yet run** — сознательно не запускалось ни оператором, ни
  платформой.
- **Operator-supplied future inputs** — выходит за пределы repo;
  зависит от operator infrastructure / decisions на Step 4.

Эти категории нельзя смешивать. Track E считается честным
ровно настолько, насколько строго это разделение держится.

---

## 2. Current evidence baseline

### 2.1 Proven reference version

| Параметр | Значение |
|---|---|
| 1С version family | `8.3.27` |
| Build | `1859` (Windows x64) |
| Full path установленного binary | `C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe` |
| Stand | `C:/Users/user/Documents/InfoBase6` (file-based, real `1Cv8.1CD`) |
| Stand type | local file-based 1С infobase, modifiable, реальный конфиг |
| Доказано на дату | Track A / Step 6 closure (см. PROJECT-STATUS Track A detail) |

**Это единственная** version family, по которой у нас сейчас
есть прямое evidence. Никаких других версий не запускалось ни
руками, ни платформой.

### 2.2 Proven smoke scope

Прямое evidence на reference version покрывает **полный**
Track A multi-step round-trip (это **больше**, чем «smoke»):

- **A.2 — `create_dump_snapshot`** через
  `/DumpConfigToFiles` → `mode='binary-backed'`,
  `binary_invoked=True`, `exit_code=0`. Реальный dump-tree
  записан под dump path InfoBase6.
- **A.4 — `apply_config_from_files`** через
  `/LoadConfigFromFiles` → `stage='completed'`. Mutating
  audit row написана. Pre-mutating dump-snapshot создан
  `run_write_flow`'ом автоматически.
- **A.5 — `update_database_configuration`** через
  `/UpdateDBCfg` → `stage='completed'`. Mutating audit row
  написана. Pre-mutating dump-snapshot создан.

**Honest payload discipline:** все шесть unified honest-mode
полей (`mode`, `binary_invoked`, `exit_code`,
`command_preview`, `stdout_excerpt`, `stderr_excerpt`)
populated в каждом ответе binary-backed write-tool'ов.

### 2.3 Existing artifacts / evidence sources

Все артефакты ниже **физически** на диске на момент написания
этого документа:

- **Reference dump tree:**
  `examples/demo-dumps/infobase6/` — содержит реальный
  `Configuration.xml`, `ConfigDumpInfo.xml`, `1Cv8.cf` и
  директории `Catalogs/`, `CommonModules/`, `Enums/`. Это
  output `/DumpConfigToFiles` на reference version.
- **Reference audit:**
  `examples/demo-dumps/infobase6/.audit/audit.jsonl` —
  ровно **2 mutating row** (`apply_config_from_files` +
  `update_database_configuration`), обе с populated
  `details.dump_snapshot_path`. Standalone
  `create_dump_snapshot` audit row не пишет by design — он
  не идёт через `run_write_flow`; pre-apply / pre-updatedb
  dump подтверждается через `details.dump_snapshot_path`
  mutating row'и.
- **Reference snapshot trees:**
  `examples/demo-dumps/_snapshots/` содержит несколько
  per-stage snapshot директорий, включая:
  `dump-infobase6-file-step6-A2-dump`,
  `dump-infobase6-file-step6-A4-apply-*`,
  `dump-infobase6-file-step6-A5-updatedb-*`. Это physical
  evidence того, что `run_write_flow` записал реальные
  pre-mutating snapshot'ы перед mutating операциями A.4 и
  A.5.
- **Reference config-shape sample:**
  `examples/demo-infobase/infobase6.config.json` — declared
  candidate config, namespace operators-supplied environment
  параметры (без credentials в JSON; для real-stand'а
  Track D / Step 3 contract задаёт `${ENV:NAME}`).
- **Reference runbook:**
  `docs/runbooks/track-a-reference-stand-round-trip.md` —
  step-by-step операторская инструкция, проверенная на
  reference version'е.

### 2.4 Reference architectural context

Платформа **не делает** version-sniffing. Оператор сам
указывает абсолютный путь к `1cv8.exe` нужной версии в
`onec_binary_path` и пишет полный operator-declared argv-template
с whitelisted placeholder'ами (`{binary_path}`, `{output_path}`,
`{base_path}`, `{base_id}`, `{publication_name}`,
`{http_base_url}`; `updatedb` whitelist tighter, без
`output_path`). Это уже **многоверсионно совместимо
архитектурно** — Track E не требует rewrite execution
layer'а.

Track A runbook сам уже отмечает honest version-difference
(стр. 244–248): «`/DisableStartupMessages` обычно достаточно
для современных версий; на старых может понадобиться
`/AppAutoCheckMode`-стиль flags — это область ответственности
оператора». То есть argv-grammar drift между версиями уже
**назван** в репо как известный риск, ещё до Track E.

---

## 3. What is NOT yet evidenced

Эти пункты — **direct gap'ы**, которые Track E попытается
закрыть в части evidence (а не платформенным rewrite'ом):

- **Никакая** другая 1С version family кроме `8.3.27` не
  запускалась ни оператором, ни платформой. Никаких evidence
  row'ов для `8.3.<other>` не существует. Никаких argv-grammar
  замечаний по другим версиям не зафиксировано.
- `8.3.27.1936` x86 build присутствует на dev-машине (упомянут
  в исторических заметках Track A), но **не использовался**
  для evidence. Это same version family `8.3.27` —
  он не был бы additional version family в любом случае.
- Никакая matrix-table документация ещё не существует
  (`docs/version-support-matrix.md` — Step 3 deliverable).
- Никакой operator runbook для multi-version smoke ещё не
  существует (`docs/runbooks/track-e-multi-version-smoke-matrix.md`
  — Step 3 deliverable).
- Никакой comparability protocol между versions не
  зафиксирован — без frozen smoke scenario (см.
  `track-e-smoke-scenario.md` Step 2 partner) сравнивать
  результаты нельзя.
- Никакой support-statement в SECURITY.md /
  release-handoff.md / README не поднимается выше
  «single-version evidence» — это Step 5 deliverable,
  и подъём произойдёт **только** по фактическому evidence
  Step 4, не до него.

### Inferred (есть архитектурное основание, но прямого evidence row нет)

- **Argv-grammar совместимость на близких minor-версиях
  (`8.3.<N>`, где N близко к 27).** На основании того, что
  1С обычно сохраняет совместимость DESIGNER-ключей в
  пределах одной major (8.3.x), можно ожидать, что
  `/DumpConfigToFiles`, `/LoadConfigFromFiles`,
  `/UpdateDBCfg` работают одинаково на `8.3.<N>` для соседних
  N. Это **inferred**, не proven — ровно поэтому Track E и
  нужен.
- **Совместимость x86 vs x64 на одной family.** Архитектурно
  ничто не зависит от bitness'а — оператор задаёт path. Но
  evidence для x86 не запускался.
- **Совместимость server-based stand'ов (vs file-based).**
  Track A round-trip прошёл на file-based стенде. Server-based
  стенды отличаются `/Server` ключом и публикацией; evidence
  для них не запускался. Это **inferred** — out-of-scope
  Track E (Track E фиксирует scenario для **file-based**
  стендов как baseline).

### Not yet run (сознательно не запускалось)

- Полный round-trip (apply / updatedb) на additional versions —
  это **out-of-scope** narrow smoke scenario'я Track E (см.
  `track-e-smoke-scenario.md`). Запускать full mutating
  round-trip на каждой target version — лишний риск для
  operator stand'а.
- Performance / load / stress / fuzzing — out-of-scope
  Track E полностью.

### Operator-supplied future inputs

- Какие именно дополнительные 1С version family'и доступны у
  оператора (бинарники + test infobase'ы под каждую) — **не
  знаем** на момент Step 2. Это operator decision Step 4.
- Network-mounted / portable / non-standard install layout'ы
  — operator может предложить, но это **out-of-scope** baseline
  (Track E фиксирует только path-based binary).
- DESIGNER credentials для operator stand'ов — обязательно
  через Track D / Step 3 contract (`${ENV:NAME}`), никаких
  cleartext в repo.

---

## 4. Why single-version evidence is insufficient

**Скрытая дрожь argv-grammar'а между версиями.** Operator-
declared command templates содержат позиционные argv
(`/DumpConfigToFiles`, `/LoadConfigFromFiles`, `/UpdateDBCfg`,
`/DisableStartupMessages`, `/F`, `/N`, `/P`). На отличающихся
minor / major версиях возможны:
- переименование флагов (особенно для startup-message-
  suppression — runbook сам это упоминает);
- изменение exit-code семантики;
- изменение output-формата `Configuration.xml` (не структурно
  ломающее, но потенциально влияющее на consumer'ы).

Single-version evidence **не отвечает** на эти вопросы. Позиция
«не должно отличаться» — это assumption, не доказательство.

**Скрытая зависимость от particular install layout'а.** Все
текущие evidence ship'нуты с install path'ом
`C:/Program Files/1cv8/<version>/bin/`. Real-world варианты —
x86 install, network-mounted install, portable build — реальной
evidence не имеют. Архитектурно это **должно** работать (path
operator-supplied), но evidence row'а для этого нет.

**Скрытая зависимость от particular stand-shape'а.** InfoBase6
— file-based, modifiable, реальный конфиг. Server-based стенды,
read-only stand'ы (для smoke без write-prerequisites), пустые
test stand'ы — все **out-of-scope** текущего evidence base.

**Track E закрывает первые два риска** ровно настолько,
насколько достаточно для честного support-statement: documented
matrix с N версий по одному узкому сценарию. Server-based
стенды и full QA-программа — out-of-scope трека.

---

## 5. Step 3 handoff note

Этот audit-документ — **input** для Step 3 (matrix scaffolding)
и Step 4 (operator-driven smoke runs). Он:

- фиксирует **reference row** matrix-table'ы (Step 3
  deliverable заполнит первую строку из этого audit
  документа без новых прогонов 1cv8 — copy-only);
- фиксирует **what NOT to claim** в любых будущих
  support-statement'ах до того, как Step 4 ship'ит реальные
  additional row'ы;
- фиксирует список **physical artifact paths** (`examples/demo-dumps/`,
  `examples/demo-dumps/_snapshots/`, audit.jsonl) на которые
  Step 3 matrix-table будет ссылаться через
  `details.dump_snapshot_path` / audit-row reference / file
  paths.

Step 3 **не должен** перепроверять evidence из section 2 —
оно уже proven. Step 3 строит scaffolding (runbook + matrix
table template) поверх этого audit'а как trusted baseline.

Step 4 **не должен** выходить за пределы frozen scenario из
`track-e-smoke-scenario.md` (Step 2 partner doc) — только
ровно тот scenario на additional versions, без расширения
смыслом.

---

## 6. Honest summary (one paragraph)

На сегодня (Track E / Step 2 closure) проект имеет direct
evidence **полного** Track A round-trip'а на **одной** 1С
version family `8.3.27` (build `1859`, Windows x64), на одном
file-based reference stand'е InfoBase6, с физически
сохранёнными artifact'ами (dump tree, audit.jsonl с двумя
mutating rows, snapshot trees под `_snapshots/`). Архитектурно
платформа multi-version-friendly (operator-supplied binary
path; whitelisted placeholder'ы; env-substitution из Track D /
Step 3). Никакая другая version family прямого evidence не
имеет. Multi-version matrix будет построена на Step 3
(scaffolding) и Step 4 (operator-driven runs) — не раньше.
Никакого multi-version support claim до Step 4 evidence
нет.
