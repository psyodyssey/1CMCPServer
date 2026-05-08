# Parallel Track E — Multi-Version 1C Smoke Matrix (step map)

> **Companion file:** `track-e-multi-version-smoke-matrix-plan.md`
> (план трека). Этот файл — пошаговый map. Каждый шаг открывается
> отдельным заходом, не комбинируется в один commit с другим
> step'ом.

> **Track invariants** (повтор из плана):
> - registries `read=15 / write=25 / intelligence=16` без drift'а;
> - никаких новых MCP tools;
> - никаких новых code path'ов в платформе;
> - никакого version-sniffing в платформе (architectural choice
>   сохраняется);
> - никаких real credentials в repo / docs / commit messages;
> - 1cv8.exe запускается **только** на operator-driven Step 4 на
>   operator infrastructure;
> - evidence фиксируется только по фактическим прогонам, никакой
>   имитации.

---

## Step 1 — planning multi-version 1C smoke matrix (этот шаг)

**Цель.** Зафиксировать документационный вход в Track E:
назначение, целевой результат, что входит / не входит,
guardrails, acceptance criteria, открытые вопросы Q1–Q7.

**Что меняем.** Только два planning-документа:

- `docs/architecture/track-e-multi-version-smoke-matrix-plan.md`
- `docs/architecture/track-e-multi-version-smoke-matrix-step-map.md`

Плюс минимальные status-правки в `README.md` и
`PROJECT-STATUS.md` под открытие active track'а E.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `.github/`, `.editorconfig`, `.python-version`,
`.gitignore`, `examples/`, `LICENSE`, `SECURITY.md`,
`CHANGELOG.md`, `docs/release-handoff.md`,
`docs/operator-manual.md`, `docs/administrator-manual.md`,
`docs/developer-manual.md`, `docs/runbooks/*` — без изменений на
Step 1.

**Результат.** Track E открыт как active planning-only трек.
Implementation Step 2 не открывается в этом же заходе.

---

## Step 2 — current evidence baseline audit + version selection criteria + smoke scenario freeze (docs-only)

**Цель.** Честно описать **существующую** single-version
evidence base, зафиксировать **principle-based criteria** отбора
target версий (без привязки к конкретным номерам — список
target версий — operator gate), и **freeze'нуть** узкий smoke
scenario, который будет считаться достаточной evidence-единицей.
Никакая implementation. Никаких code changes. Никакого
1cv8.exe.

**Что меняем.**

1. Новый short документ
   `docs/architecture/track-e-current-evidence-audit.md`:
   - что именно доказано на reference version `8.3.27.1859` —
     полный список Track A / Step 6 артефактов, audit-row
     references, snapshot-tree paths;
   - что **не** доказано — argv-grammar dependency, exit-code
     semantics, Configuration.xml format на других versions;
   - архитектурный context: platform не делает
     version-sniffing; multi-version поддержка живёт на
     operator side через operator-declared
     `onec_binary_path` и `onec_*_command_template`.
2. Новый short документ
   `docs/architecture/track-e-smoke-scenario.md`:
   - **Frozen smoke scenario** — точные шаги, которые
     считаются одной evidence-единицей (default candidate:
     cut-down — `create_dump_snapshot` через
     `/DumpConfigToFiles` only, на operator-supplied
     read-only test infobase; optional extended — full A.2 →
     A.4 → A.5 round-trip симметрично Track A);
   - какие payload-поля проверяются (`mode='binary-backed'`,
     `binary_invoked=True`, `exit_code=0`, audit-row presence);
   - acceptance / failure verdicts для одной evidence-row;
   - resolve Q2 (smoke scenario depth — default cut-down).
3. Resolve Q1 (version selection breadth) внутри
   `track-e-current-evidence-audit.md`: principle-based
   criteria, минимум 1 additional, рекомендуемо 2, максимум 3.
   Конкретные version-номера НЕ в plan — operator gate Step 4.

**Что НЕ меняем.** Никакого `apps/`, `packages/`, `scripts/`,
`pyproject.toml`. Никаких изменений в SECURITY.md /
release-handoff.md / README / CHANGELOG (это Step 5 / Step 6).
Никакого реального прогона 1cv8.exe.

**Результат.** Step 3 имеет honest evidence baseline и frozen
scenario как input. Step 4 имеет formal version selection
criteria.

---

## Step 3 — matrix scaffolding (docs-only)

**Цель.** Подготовить operator-runnable matrix infrastructure
полностью на documentation-уровне: operator runbook + matrix
table template. Никакого реального прогона 1cv8.exe. Никакой
implementation в платформе.

**Что меняем.**

1. Новый operator runbook
   `docs/runbooks/track-e-multi-version-smoke-matrix.md`:
   - prerequisites: operator-supplied `1cv8.exe` другой
     version family + writable test infobase + `${ENV:NAME}`
     credentials path (Track D / Step 3 contract);
   - точные шаги прогона smoke scenario (по Step 2 freeze'у);
     symmetric с `docs/runbooks/track-a-reference-stand-round-trip.md`,
     но **узкий**;
   - где фиксировать evidence (matrix-table row + optional
     audit.jsonl reference);
   - failure modes (binary not found, version mismatch in
     argv grammar, exit_code != 0);
   - честный disclaimer: один passed run = одна evidence-row,
     не «version supported».
2. Новый matrix-table doc
   `docs/version-support-matrix.md` (top-level):
   - top-level support statement: «Smoke evidence collected
     on N versions per Track E scope. Это **не** universal
     version support.»;
   - таблица evidence-row'ов с колонками: Version family /
     Build / OS arch / Binary path / Scenario (cut-down /
     extended) / Verdict / Audit row reference / Date;
   - **одна row уже заполнена** — reference `8.3.27.1859`
     (read-only копирование из Track A / Step 6 audit, новый
     прогон 1cv8 не нужен);
   - operator-supplied additional row'ы — placeholder под
     Step 4.
3. Resolve Q3 (matrix-table location) — top-level
   `docs/version-support-matrix.md`.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, registries. Никаких изменений в существующих
Track A runbook, SECURITY.md, release-handoff.md, README,
CHANGELOG (это Step 5 / Step 6). Никакого реального прогона
1cv8.exe.

**Результат.** Operator имеет готовые runbook + matrix-table
template для прогона на дополнительных versions. Reference row
уже заполнена.

---

## Step 4 — operator-driven smoke runs (operator gate)

**Цель.** Operator прогоняет matrix runbook на доступных у него
дополнительных 1С version family'ах и фиксирует evidence-row'ы.
Если operator не может предоставить additional versions —
честно фиксируется operator-supplied gap, без имитации
evidence.

**Что меняем (если operator ship'ит evidence).**

- `docs/version-support-matrix.md`:
  - дописываются evidence-row'ы по факту операторских
    прогонов (одна row на одну version family);
  - каждая row ссылается на real audit-row в operator's
    audit.jsonl или на real-stand snapshot tree;
  - никаких real credentials в значениях row'ов
    (`${ENV:NAME}` substitution path был использован
    оператором; здесь только evidence, не secret).

**Что меняем (если operator не может ship'ить evidence).**

- `docs/version-support-matrix.md`:
  - явно фиксируется «operator-supplied gap: additional
    version evidence pending — matrix template ready,
    awaiting operator infrastructure»;
  - reference row остаётся единственной заполненной;
  - track продолжается на Step 5 / Step 6 honestly как
    «matrix scaffolding closed; reference-only evidence»;
  - этот сценарий **не** считается track failure — он
    считается honest closure под фактический evidence-уровень.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, registries. Никаких изменений в платформе.
Никаких новых runbook'ов / planning-документов. SECURITY.md /
release-handoff.md / README / CHANGELOG не трогаются на
Step 4 (это Step 5).

**Результат.** Matrix-table заполнена либо real
operator-supplied evidence-row'ами, либо явно зафиксированным
operator-supplied gap. Resolve Q4 (operator-supplied gap
fallback) — closure honestly работает в обоих сценариях.

---

## Step 5 — support statement / docs alignment

**Цель.** Перевести operator-facing документацию с
«single-version evidence» на **фактически собранный**
evidence-уровень. Если ship'нуто N additional rows — поддержка
documented per-row matrix; если только reference row —
документация остаётся single-version, но pointer'ует на matrix
template + Track E как процесс.

**Что меняем.**

- `SECURITY.md`:
  - «Single-version 1С evidence» bullet переписывается под
    реальный evidence-уровень + pointer на
    `docs/version-support-matrix.md`. Если additional row'ы
    есть — формулировка «smoke evidence on N versions»; если
    только reference — «smoke evidence on `8.3.27.1859`;
    matrix template ready for operator-supplied additional
    evidence».
- `docs/release-handoff.md`:
  - Known limitations bullet про multi-version smoke
    переписывается симметрично SECURITY.md;
  - в Verify/Local check sections добавляется pointer на
    `docs/version-support-matrix.md` как single-source-of-truth
    для актуального evidence-уровня.
- `README.md`:
  - Quickstart-блок упоминает `docs/version-support-matrix.md`
    в «Куда идти дальше» bullet'е (одна строка).
  - «Что Quickstart не обещает» обновляется минимально под
    actual evidence-уровень.
- Resolve Q6 (SECURITY.md / release-handoff.md tone) — короткий
  narrative + pointer на matrix-table.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, registries. Никаких новых runbook'ов или
planning-документов. CHANGELOG не трогаем — это Step 6.
Никакого реального прогона 1cv8.exe.

**Результат.** Все operator-facing статусные docs honestly
отражают **фактический** evidence-уровень. Receive-side
оператор читает SECURITY.md или release-handoff.md → видит
точный support statement → читает
`docs/version-support-matrix.md` → видит per-version evidence-row.

---

## Step 6 — final integration pass and Track E closure

**Цель.** Закрыть весь Track E как documented status. Read-only
final integration check уже закрытых Steps 1–5, потом минимальные
closure-docs/status updates, потом final closure commit.

**Read-only final integration check.**

- working tree clean перед началом;
- git history линейная: Step 1 → Step 2 → Step 3 → Step 4 →
  Step 5 → Step 6;
- planning + step-map + audit + scenario + runbook +
  matrix-table все на диске;
- registries `read=15 / write=25 / intelligence=16` без drift'а;
- selfcheck PASS;
- verify-release.ps1 GREEN на 8 checks (без новых checks);
- no real credentials в diff'ах ни одного из шести Track E
  commit'ов.

**Что меняем (только closure docs/status updates).**

- `README.md`:
  - «Closed parallel tracks» дополняется Track E bullet'ом
    (четыре → пять закрытых трека);
  - «Active parallel track» секция возвращается к «нет
    активного трека»;
  - Quickstart-блок упоминает Track E как closed;
  - добавляется «Track E detail (закрыт)» секция симметрично
    Track A/B/C/D detail блокам.
- `PROJECT-STATUS.md`:
  - header (Текущий шаг + Статус) обновляется под Track E
    closed;
  - добавляются пять новых per-step секций (Steps 2/3/4/5/6).
- `CHANGELOG.md`:
  - новый раздел `## 0.3.0 — Parallel Track E` (если Q5
    resolved bump 0.2.0 → 0.3.0; иначе follow-up под 0.2.0)
    с per-step outcomes, registry invariant, honest constraints
    update;
  - resolve Q5 финально (bump или не bump).
- `pyproject.toml`:
  - version bump 0.2.0 → 0.3.0 (если Q5 resolved bump на
    Step 6); иначе не трогаем.

**Что НЕ меняем.**

- никакого нового feature work;
- никаких новых MCP tools;
- никакого remote push'а;
- `apps/`, `packages/`, `scripts/`, `examples/`,
  `docs/architecture/track-e-*` (planning docs остаются как
  written), `docs/runbooks/track-e-*` (operator runbook
  остаётся как written), `docs/version-support-matrix.md`
  (заполнена на Steps 3/4), `.github/`, `.editorconfig`,
  `.python-version`, `.gitignore`, `LICENSE` —
  не тронуты в этом шаге **за пределами** closure-narrative
  updates.
- Resolve Q7 (post-closure evidence cadence) — doc-only update
  против `version-support-matrix.md` без re-open Track E.

**Результат.** Track E полностью закрыт как documented status.
Активного трека нет. Открытие следующего parallel track'а —
отдельное operator-решение.

---

## Out-of-scope шагов (deliberately)

- никакая полная QA-программа (test pyramid, performance
  benchmarking, stress/load testing, fuzzing);
- никакая enterprise certification claims;
- никакая «universal / full version support» marketing;
- никакие feature additions для конкретных 1С версий;
- никакое version-sniffing в платформе;
- никакие новые MCP tools (registries `read=15 / write=25 /
  intelligence=16`);
- никакие 1cv8 binary changes;
- никакая CI matrix runner-инфраструктура для multi-version
  1cv8 (physical operator territory);
- никакие новые execution-core sprint'ы;
- никакой remote push / GitHub publishing;
- никакой production-grade MCP transport / auth;
- никакая полная rollback / delete-вселенная или AST-парсер.

**GitHub remote push** — operator action, не часть Track E.
