# Parallel Track D — Operator Credentials Hardening (step map)

> **Companion file:** `track-d-operator-credentials-hardening-plan.md`
> (план трека). Этот файл — пошаговый map. Каждый шаг открывается
> отдельным заходом, не комбинируется в один commit с другим
> step'ом.

> **Track invariants** (повтор из плана):
> - registries `read=15 / write=25 / intelligence=16` без drift'а;
> - никаких новых MCP tools;
> - никакого `shell=True`;
> - `run_write_flow` остаётся единственным mutating-путём;
> - intelligence-server остаётся read-only;
> - нет real credentials в repo / docs / commit messages.

---

## Step 1 — planning operator credentials hardening (этот шаг)

**Цель.** Зафиксировать документационный вход в Track D: назначение,
целевой результат, что входит / не входит, guardrails, acceptance
criteria, открытые вопросы Step 2+.

**Что меняем.** Только два planning-документа:

- `docs/architecture/track-d-operator-credentials-hardening-plan.md`
- `docs/architecture/track-d-operator-credentials-hardening-step-map.md`

Плюс минимальные status-правки в `README.md` и
`PROJECT-STATUS.md` (открытие active track).

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `.github/`, `.editorconfig`, `.python-version`,
`.gitignore`, `examples/`, `LICENSE`, `SECURITY.md`,
`CHANGELOG.md`, `docs/release-handoff.md`,
`docs/operator-manual.md`, `docs/administrator-manual.md`,
`docs/developer-manual.md`, `docs/runbooks/*` — без изменений на
Step 1.

**Результат.** Track D открыт как active planning-only трек.
Implementation Step 2 не открывается в этом же заходе.

---

## Step 2 — credentials-flow audit and contract (docs-only)

**Цель.** Честно описать **существующий** credentials surface и
зафиксировать **минимальный contract** на env-substitution и
redaction. Никакой implementation. Никаких code changes.

**Что меняем.**

1. Новый short документ
   `docs/architecture/track-d-credentials-flow-audit.md`:
   - где `/P "<password>"` физически появляется в
     `onec_*_command_template`-массивах;
   - какие payload-поля видят rendered argv (`command_preview`,
     `stdout_excerpt`, `stderr_excerpt`);
   - какие audit-поля могут отражать password (если оператор
     положил cleartext);
   - как `.gitignore` (Track B / Step 2) ловит local writable
     config'и;
   - что значит «out-of-band» сейчас и почему это аспирация, а
     не enforced контракт.
2. Новый short документ
   `docs/architecture/track-d-credentials-contract.md`:
   - синтаксис env-substitution: `${ENV:NAME}` (default из плана,
     resolve финально здесь);
   - resolution order: render-time, после structural-placeholder
     substitution, до запуска subprocess'а;
   - fail-closed semantics: missing env → render-time `ok=False`
     с honest payload (`mode='binary-backed'`,
     `binary_invoked=False`, render-fail branch);
   - redaction contract: argv element после `/P` или `/Pwd`
     (case-insensitive) → редактируется в `command_preview` и
     trimmed excerpts; **actual subprocess argv остаётся
     unredacted** (иначе binary не аутентифицируется);
   - backward-compat: literal cleartext password остаётся
     supported, не fail; only `verify-release.ps1` heuristic
     (Step 5) репортит его.
3. Optional research note внутри audit-документа: «could-be-
   tier-2 via OS keychain (`keyring`)» — **research-only**,
   deliberately not in scope Track D.

**Что НЕ меняем.** Никакого `apps/`, `packages/`, `scripts/`,
`pyproject.toml`. Никаких изменений в SECURITY.md / release-
handoff.md (это Step 4). Никакого CHANGELOG update.

**Результат.** Step 3 имеет honest contract как input. Step 4
имеет audit-документ как single source of truth для operator-
facing migration.

---

## Step 3 — env-substitution implementation and redaction

**Цель.** Реализовать env-substitution и redaction discipline в
write-server'е, оставаясь backward-compatible с cleartext-template.

**Что меняем.**

- `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`
  (default location per Q2):
  - расширяется `render_command_template(...)`:
    - после structural-placeholder substitution выполняется второй
      pass — env-substitution для literal `${ENV:NAME}` элементов;
    - missing env var → render-fail branch
      (`mode='binary-backed'`, `binary_invoked=False`,
      `command_preview=None`, honest reason); fail-closed по
      аналогии с unknown-placeholder discipline;
  - расширяется `_assemble_command_preview(...)`:
    - сканирует rendered argv list;
    - для argv элементов после `/P` / `/Pwd` (case-insensitive)
      подменяет value на `<redacted>`;
    - возвращает redacted preview; actual subprocess argv не
      трогается.
  - новые internal helper'ы (`_resolve_env_token`,
    `_redact_password_args`) живут в том же файле, не в новом
    package'е, чтобы не раздувать surface.
- Тесты (если в проекте есть test-harness под write-server) —
  узкие unit-тесты на: `${ENV:NAME}` resolved → render OK;
  missing env → render fail; redaction `/P` → preview редактирован;
  literal cleartext → render OK + preview redacted.

**Что НЕ меняем.**

- `run_write_flow` discipline.
- structural-placeholder whitelists per tool (Track A sealed).
- `subprocess` без `shell=True`.
- Public surface write-server'а — никаких новых tools, никаких
  изменений в JSON shapes для уже existing tools.
- registries (`read=15 / write=25 / intelligence=16`).
- onec-config loader semantics (substitution живёт в render-time,
  не в load-time per Q2 default).

**Результат.** Operator может писать
```
"/N", "${ENV:ONEC_DESIGNER_USER}",
"/P", "${ENV:ONEC_DESIGNER_PASSWORD}",
```
в template'е и получать render-time substitution из env vars. Если
env vars не выставлены — honest render-fail. `command_preview` не
показывает cleartext password ни в env-substitution, ни в legacy-
literal формах.

---

## Step 4 — operator docs / migration / handoff alignment

**Цель.** Перевести operator-facing документацию на
env-substitution как **default рекомендованный путь**. Cleartext
literal становится legacy fallback'ом, который остаётся
supported, но не рекомендуется.

**Что меняем.**

- `docs/runbooks/track-a-reference-stand-round-trip.md`:
  - в product-config example форма `/P "<password>"` заменяется
    на `/P "${ENV:ONEC_DESIGNER_PASSWORD}"` (и аналогично для
    `/N`); существующая `<password>` placeholder-форма
    остаётся в short legacy paragraph как «works, but not
    recommended».
- `SECURITY.md`:
  - Honest-constraints секция переформулируется: «Operator
    credentials are out-of-band» теперь имеет конкретную
    реализацию (env-substitution) + перечень того что
    **по-прежнему** out-of-scope (vault, KMS, SSO, encrypted-at-
    rest, OS keychain).
- `docs/release-handoff.md`:
  - "Known limitations" секция: DESIGNER credentials bullet
    обновляется под env-substitution как default.
- `docs/operator-manual.md`:
  - короткая новая секция (или существующая обновляется) с
    пошаговым: «как задать env vars (PowerShell / bash) и как
    написать template'ы под них».
- Новый узкий short документ
  `docs/operator-credentials.md` (опционально, если в operator-
  manual'е не помещается без раздувания), содержащий:
  - default рекомендованный путь (env-substitution);
  - migration paragraph для существующих cleartext-config'ов;
  - honest «what is NOT covered» (vault, KMS, SSO, OS keychain).

**Что НЕ меняем.**

- `apps/`, `packages/`, `scripts/`, `pyproject.toml` — Step 4 это
  docs-only.
- `README.md` Quickstart corpus — Quickstart остаётся install /
  check / launch oriented; pointer на operator-credentials может
  быть добавлен в "Куда идти дальше" одним bullet'ом — но это
  **maximum** одна правка, не reшейп Quickstart'а.
- runbook structure (только example template line меняется + one
  legacy paragraph добавляется).

**Результат.** Receive-side оператор читает release-handoff →
operator-manual / operator-credentials → пишет template с
`${ENV:...}` → выставляет env vars → запускает install / verify /
real-stand round-trip без cleartext password в config-файле.

---

## Step 5 — release-verify credential-hygiene heuristic

**Цель.** Расширить `scripts/release/verify-release.ps1` узкой
heuristic'ой, которая ловит наиболее очевидный паттерн утечки —
literal `/P "<value>"` в tracked `*.config.json`, где `<value>`
не env-substitution-формы и не `<password>` placeholder'а.

**Что меняем.**

- `scripts/release/verify-release.ps1`:
  - добавляется новый named check (например, "Credential
    template hygiene") — отдельный от существующего
    "Credential leak guard";
  - heuristic сканирует tracked `*.config.json` файлы (через
    `git ls-files`), ищет паттерн вокруг `"/P"` followed by
    next argv element value;
  - если value матчит `${ENV:...}` или абстрактный placeholder
    `<password>` — PASS;
  - если value — literal-non-empty-string без env-substitution-
    формы — WARN (не FAIL), с указанием exact file и line;
  - heuristic deliberately узкая: false-positive минимизирован
    (не сканирует runbook'ы, не сканирует non-config файлы);
  - none of the heuristic patterns include real credentials —
    проверка работает по форме, не по содержимому value.
- `scripts/release/README.md`:
  - короткая update-секция про новый check;
  - явное «это heuristic, не full DLP».
- `docs/release-handoff.md`:
  - таблица verify-release checks обновляется (добавляется
    8-й check).

**Что НЕ меняем.**

- existing checks 1-7 в `verify-release.ps1`.
- exit-code semantics: WARN vs FAIL — default WARN, чтобы не
  ломать receive-side flow для legacy-config'ов.
- `apps/`, `packages/`, `pyproject.toml`, registries.

**Результат.** Receive-side оператор, запустив
`verify-release.ps1`, видит 8 checks; check 8 предупреждает, если
config содержит cleartext password literal. Это **best-effort
heuristic**, явно не претендующая на полноту.

---

## Step 6 — final integration pass and Track D closure

**Цель.** Закрыть весь Track D как documented status. Read-only
final integration check уже закрытых Steps 1–5, потом минимальные
closure-docs/status updates, потом final closure commit.

**Read-only final integration check.**

- working tree clean перед началом;
- git history линейная: Step 1 → Step 2 → Step 3 → Step 4 →
  Step 5;
- все Step 2 docs на диске (audit + contract);
- env-substitution + redaction присутствуют в
  `binary_dispatch.py` (Step 3);
- operator docs обновлены (Step 4);
- 8-й check присутствует в `verify-release.ps1` (Step 5);
- registries `read=15 / write=25 / intelligence=16`;
- selfcheck PASS;
- no real credentials в diff'ах ни одного из пяти Track D
  commit'ов (verified by manual scan + grep heuristic).

**Что меняем (только closure docs/status updates).**

- `README.md` — секция «Closed parallel tracks» дополняется Track
  D bullet'ом; «Track D detail (закрыт)» секция добавляется
  симметрично «Track C detail (закрыт)»; Quickstart intro
  упоминает Track D как closed; «Куда идти дальше» получает
  pointer на operator-credentials docs (если Step 4 ship'нул
  отдельный документ).
- `PROJECT-STATUS.md` — header (Текущий шаг + Статус) обновляется
  под Track D closed; добавляются пять новых per-step секций
  (Steps 2/3/4/5/6).
- `CHANGELOG.md` — Parallel Track D bullet под current release
  line; per-step outcomes; honest constraints update (если Q7
  resolved bump 0.1.0 → 0.2.0 — bump делается здесь).

**Что НЕ меняем.**

- никакого нового feature work;
- никаких новых MCP tools;
- никакого remote push'а;
- `apps/`, `packages/`, `scripts/`, `examples/`,
  `docs/architecture/`, `docs/runbooks/`,
  `docs/operator-manual.md`, `docs/developer-manual.md`,
  `docs/administrator-manual.md`, `docs/release-handoff.md`,
  `pyproject.toml` (если version bump уже сделан в этом же шаге —
  этот один файл единственное исключение), `.github/`,
  `.editorconfig`, `.python-version`, `.gitignore`, `LICENSE`,
  `SECURITY.md` — не тронуты в этом шаге **за пределами**
  closure-narrative updates.

**Результат.** Track D полностью закрыт как documented status.
Активного трека нет. Открытие следующего parallel track'а —
отдельное operator-решение.

---

## Out-of-scope шагов (deliberately)

- никакого vault / KMS / SSO / RBAC implementation;
- никакого encrypted-at-rest secrets file format;
- никакого OS keychain (`keyring`) integration в core path;
- никакого нового MCP tool (registries `read=15 / write=25 /
  intelligence=16`);
- никакого 1cv8 binary changes;
- никакого new execution-core sprint;
- никакого remote push / GitHub publishing;
- никакого production-grade MCP transport / auth.

**GitHub remote push** — operator action, не часть Track D.
