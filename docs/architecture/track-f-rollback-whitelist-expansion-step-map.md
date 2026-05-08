# Parallel Track F — Rollback Whitelist Expansion (step map)

> **Companion file:** `track-f-rollback-whitelist-expansion-plan.md`
> (план трека). Этот файл — пошаговый map. Каждый шаг открывается
> отдельным заходом, не комбинируется в один commit с другим
> step'ом.

> **Track invariants** (повтор из плана):
> - registries `read=15 / write=25 / intelligence=16` без drift'а;
> - никаких новых MCP tools;
> - `restore_dump_file_from_snapshot` public API без изменений;
> - audit row `details` format без изменений;
> - никакого back-door filesystem write channel в product layer'е;
> - per-tool eligibility (a/b/c) обязательна перед include в
>   whitelist;
> - production code touched только в Step 4 и **только**
>   `apps/platform/src/onec_platform/recovery.py`;
> - никаких 1cv8.exe runs ни на одном шаге трека;
> - никаких real credentials в repo / docs / commit messages.

---

## Step 1 — planning rollback whitelist expansion (этот шаг)

**Цель.** Зафиксировать документационный вход в Track F:
назначение, целевой результат, что входит / не входит,
guardrails, acceptance criteria, открытые вопросы Q1–Q7.

**Что меняем.** Только два planning-документа:

- `docs/architecture/track-f-rollback-whitelist-expansion-plan.md`
- `docs/architecture/track-f-rollback-whitelist-expansion-step-map.md`

Плюс минимальные status-правки в `README.md` и
`PROJECT-STATUS.md` под открытие active track'а F.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `.github/`, `.editorconfig`, `.python-version`,
`.gitignore`, `examples/`, `LICENSE`, `SECURITY.md`,
`CHANGELOG.md`, `docs/release-handoff.md`,
`docs/operator-manual.md`, `docs/administrator-manual.md`,
`docs/developer-manual.md`, `docs/runbooks/*`,
`apps/platform/README.md` — без изменений на Step 1.

**Результат.** Track F открыт как active planning-only трек.
Implementation Step 4 не открывается в этом же заходе.

---

## Step 2 — rollback baseline audit and candidate selection (docs-only)

**Цель.** Честно описать **существующий** rollback baseline и
выбрать Step 4 target set по eligibility criteria, **без code
changes**.

**Что меняем.**

1. Новый short документ
   `docs/architecture/track-f-rollback-baseline-audit.md`:
   - exact текущий whitelist (`add_catalog_attribute`,
     `add_document_attribute`) с источником истины
     (`recovery.py:126-131`);
   - existing eligibility comment из `recovery.py:118-125`
     цитируется verbatim;
   - per-tool evaluation против criteria a/b/c для всех
     11 tools из `_KNOWN_WRITE_TOOL_FAMILIES` плюс
     `add_form_attribute` (Phase 6 / Step 5);
   - разделение **Tier 1 (strong candidates)** /
     **Tier 2 (нужна доп. evaluation)** / **Tier 3
     (categorically excluded)** / **Tier 4 (already in
     whitelist)** с per-tool rationale (какой criterion
     pass'ит, какой fail'ит, почему);
   - resolve **Q2** — точный target set Step 4 (Tier 1
     subset, обычно 2–3 tools).
2. Verification (read-only): для каждого Tier 1 кандидата
   найти место в `apps/mcp-write-server/src/` где tool
   определён, и зафиксировать в audit'е, что
   `operation_payload` carries `relative_path` (один
   string field). Это **manual code review**, не runtime
   test; никакого `1cv8.exe` или подобного.

**Что НЕ меняем.** Никакого code change. `recovery.py` не
тронут (это Step 4). `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, registries, `SECURITY.md`,
`docs/release-handoff.md`, `README.md`, `apps/platform/README.md`,
operator runbooks — всё untouched (alignment — Step 5; closure —
Step 6).

**Результат.** Step 3 имеет formal Tier breakdown как input;
Step 4 имеет точный target set с per-tool sanity-check artifact'ом.

---

## Step 3 — rollback eligibility contract (docs-only)

**Цель.** Formalize existing `recovery.py:118-125` comment в
отдельный contract document. Никакого code change.

**Что меняем.**

1. Новый short документ
   `docs/architecture/track-f-rollback-eligibility-contract.md`:
   - **Eligibility criteria (a/b/c)** — formalized: payload
     shape (single `relative_path`), restorability shape
     (overwrite single file), inverse semantics shape (snapshot
     restore captures pre-state honestly);
   - **Runtime gates** — три условия одновременно:
     (1) tool name in whitelist; (2) audit row carries `details`;
     (3) `details` содержит non-empty `dump_snapshot_path` AND
     `relative_path`;
   - **Mechanism** — public `restore_dump_file_from_snapshot`
     через `run_write_flow` (preflight + snapshot + operation
     + verify + audit); никакого back-door filesystem write
     channel в product layer'е;
   - **Post-rollback verify** — `diff_dump_fragment` обязателен;
     success = `restore.ok=True AND diff.data.changed=False`;
   - **Backward compatibility** — pre-Track-F audit rows
     (без `details` или с `details=None`) → `mode='unsupported'`
     honest degrade; никакого audit format break;
   - **Non-goals** — explicit list: `delete_*` tools, multi-file
     restore, DB schema rollback, transactional rollback,
     `apply_config_from_files` / `update_database_configuration`
     family, `create_*` family (Tier 3 categorical
     exclusion).
2. Resolve **Q3** (`restore_dump_file_from_snapshot` API без
   изменений) и **Q4** (audit row `details` format без
   изменений) явно в этом документе.

**Что НЕ меняем.** Никакого code change. `recovery.py`,
`apps/mcp-write-server/`, `apps/mcp-read-server/`,
`apps/mcp-intelligence-server/`, `packages/*/src/` — all
untouched. `pyproject.toml`, `SECURITY.md`,
`docs/release-handoff.md`, `README.md` без изменений (alignment —
Step 5; closure — Step 6).

**Результат.** Step 4 имеет formal eligibility contract как
trusted input; Step 5 имеет contract document для cross-reference
из operator-facing docs.

---

## Step 4 — narrow whitelist implementation

**Цель.** Расширить `_AUTOMATIC_RECOVERY_SUPPORTED` frozenset до
точного Step 2 target set. **Это единственный шаг Track F с
production code change.**

**Что меняем.**

- `apps/platform/src/onec_platform/recovery.py`:
  - `_AUTOMATIC_RECOVERY_SUPPORTED` frozenset расширяется до
    Step 2 / Q2 target set;
  - existing 2 tools (`add_catalog_attribute`,
    `add_document_attribute`) остаются в whitelist'е без
    изменений;
  - **никаких других изменений в `recovery.py`** —
    `_KNOWN_WRITE_TOOL_FAMILIES`, `restore_dump_file_from_snapshot`
    invocation logic, post-verify discipline,
    runtime gates — всё untouched;
  - per-tool sanity-check (manual code review):
    operation_payload каждого нового tool'а действительно
    carries `relative_path`; результат фиксируется в commit
    message.
- Optional: тонкий update комментария перед whitelist'ом
  (`recovery.py:118-125`), если new tools требуют уточнения
  rationale за пределы existing comment'а.

**Что НЕ меняем.**

- `_KNOWN_WRITE_TOOL_FAMILIES` (это informational set,
  отдельный от whitelist'а; не меняется автоматически);
- `restore_dump_file_from_snapshot` public API в
  `apps/mcp-write-server/`;
- audit row `details` format;
- Phase 6 / Step 5 `add_form_attribute` write-tool definition;
- любой другой write-tool definition;
- `apps/mcp-read-server/`, `apps/mcp-intelligence-server/`,
  `packages/*/src/`, `scripts/`, `examples/`,
  `pyproject.toml`;
- registries (`read=15 / write=25 / intelligence=16` без
  drift'а — verified через verify-release.ps1 selfcheck);
- никаких новых MCP tools.

**Verification (post-Step-4):**

- `verify-release.ps1 -AllowDirtyTree` GREEN на 8 checks;
- registries без drift'а;
- (manual) read code path: `run_rollback_assistant` для нового
  tool'а с healthy dashboard и proper audit row → would-return
  `mode='executed'` (не `'unsupported'`);
- никакого 1cv8.exe не запускалось.

**Результат.** Whitelist ship'нут. Step 5 имеет фактический
size whitelist'а как input для docs alignment.

---

## Step 5 — operator/docs alignment

**Цель.** Точечно выровнять operator-facing wording под
фактический whitelist size после Step 4.

**Что меняем.**

- `apps/platform/README.md`:
  - sections `### Modes (RECOVERY_MODES)`,
    `### Почему _AUTOMATIC_RECOVERY_SUPPORTED пуст` (если
    title больше не точен — переименовать),
    `### Phase 6 / Step 4 — первый исполняемый rollback (узкая
    полоса)` — wording обновлён под фактический whitelist
    size; Phase 6 / Step 4 historical context сохранён, Track
    F обновление добавлено как continuation;
  - explicit list whitelisted tools updated.
- `README.md`:
  - Track A detail (закрыт) bullet «whitelist остаётся на
    двух tool'ах» обновлён под фактический size; никакого
    переписывания Track A detail block'а beyond этой строки;
  - Quickstart «Что Quickstart **не** обещает» fragment если
    rollback там упоминается — точечно aligned.
- `docs/release-handoff.md`:
  - Known limitations bullet «Limited rollback coverage —
    automatic rollback whitelist is small» обновлён под
    фактический size + pointer на Track F audit/contract docs.
- Resolve **Q6** (operator-facing docs scope) — финал.

**Что НЕ меняем.** `apps/platform/src/onec_platform/recovery.py`
(Step 4 уже сделал code change); `apps/mcp-*/`, `packages/*/`,
`scripts/`, `pyproject.toml`, registries; `SECURITY.md` —
trogаем только если есть direct rollback mention (по умолчанию
нет; rollback не security-direct surface); `CHANGELOG.md` — это
closure (Step 6).

**Результат.** Operator-facing docs honestly отражают
фактический whitelist size; reader видит точные supported tools
и точные out-of-scope categories.

---

## Step 6 — final integration pass and Track F closure

**Цель.** Закрыть весь Track F как documented status.
Read-only final integration check уже закрытых Steps 1–5,
потом минимальные closure-docs/status updates, потом final
closure commit.

**Read-only final integration check.**

- working tree clean перед началом;
- git history линейная Step 1 → 6;
- Step 2 audit doc на диске;
- Step 3 contract doc на диске;
- Step 4 whitelist expansion в `recovery.py` присутствует;
- Step 5 operator-facing alignment в
  `apps/platform/README.md` / `README.md` /
  `docs/release-handoff.md`;
- registries `read=15 / write=25 / intelligence=16` без
  drift'а; selfcheck_status=ok;
- verify-release.ps1 GREEN на 8 checks;
- no real credentials в diff'ах ни одного из пяти Track F
  commit'ов;
- никаких 1cv8.exe runs за весь трек.

**Что меняем (только closure docs/status updates).**

- `README.md` — «Closed parallel tracks» дополняется Track F
  bullet'ом (пять → шесть закрытых тreков); «Active parallel
  track» секция возвращается к «нет активного трека»;
  Quickstart-блок упоминает Track F как closed; добавляется
  «Track F detail (закрыт)» секция симметрично Track A/B/C/D/E
  detail блокам.
- `PROJECT-STATUS.md` — header (Текущий шаг + Статус)
  обновляется под Track F closed; добавляются пять новых
  per-step секций (Steps 2/3/4/5/6).
- `CHANGELOG.md` — новый раздел `## 0.3.0 — Parallel Track F —
  Rollback Whitelist Expansion` (если Q5 resolved YES; default
  ДА — Step 4 ship'ит real code change с functional delta) с
  per-step outcomes, registry invariant, honest constraints
  update; alternatively closure follow-up под 0.2.0 если Q5
  resolved NO.
- `pyproject.toml` — version bump 0.2.0 → 0.3.0 (если Q5
  resolved YES); иначе не трогаем.

**Что НЕ меняем.**

- никакого нового feature work;
- никаких новых MCP tools;
- никакого remote push'а;
- `apps/`, `packages/`, `scripts/`, `examples/`,
  `docs/architecture/track-f-*` (planning / audit / contract
  docs остаются как written), `apps/platform/README.md` (Step 5
  уже выровнял), `docs/release-handoff.md` (Step 5 уже
  выровнял), `SECURITY.md` (если Step 5 не задействовал),
  `.github/`, `.editorconfig`, `.python-version`, `.gitignore`,
  `LICENSE` — не тронуты в этом шаге **за пределами**
  closure-narrative updates.
- Resolve **Q5** финально (bump или follow-up под 0.2.0).

**Результат.** Track F полностью закрыт как documented status.
Активного трека нет. Открытие следующего parallel track'а —
отдельное operator-решение.

---

## Out-of-scope шагов (deliberately)

- никакая универсальная rollback / arbitrary reverse engine;
- никакая AST-based semantic reverse logic для BSL / XML;
- никакие public `delete_*` write-tools;
- никакой multi-file / full filesystem snapshot-restore;
- никакой rollback для `apply_config_from_files` /
  `update_database_configuration` (categorically violate
  eligibility criteria);
- никакой rollback для `create_*` family (Tier 3
  categorical exclusion);
- никакие новые MCP tools (registries `read=15 / write=25 /
  intelligence=16`);
- никакие 1cv8 binary changes;
- никакие изменения write-tool surface в `apps/mcp-write-server/`;
- никакие новые execution-core sprint'ы;
- никакой production-grade MCP transport / auth;
- никакая enterprise governance / policy / RBAC track;
- никакая web UI / dashboard;
- никакой remote push / GitHub publishing;
- никакие 1cv8.exe runs ни на одном шаге трека.

**GitHub remote push** — operator action, не часть Track F.
