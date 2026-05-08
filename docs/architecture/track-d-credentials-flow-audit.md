# Track D — Credentials-flow audit (current baseline)

> **Status.** Track D / Step 2 — docs-only. Этот файл описывает
> credentials flow **как он реально работает сегодня**, до
> implementation Track D. Никакого кода не меняется. Все ссылки на
> credentials используют только abstract / redacted formы:
> `<user>`, `<password>`, `${ENV:NAME}`, `"redacted"`. Реальных
> значений в этом документе нет и не должно появиться.
>
> **Companion file:** `track-d-credentials-contract.md` (target
> contract). Этот файл — descriptive (current state); companion —
> normative (target state).

## Purpose / scope

Зафиксировать честную карту того, как DESIGNER credentials сейчас
попадают в платформу, как через неё проходят, и где остаются
наблюдаемые artefacts. Карта нужна как input для:

- Track D / Step 3 (env-substitution + redaction implementation),
- Track D / Step 4 (operator docs / migration alignment),
- Track D / Step 5 (release-verify credential-hygiene heuristic).

Out-of-scope этого документа: prescribing a fix. Предписания
живут в companion `track-d-credentials-contract.md`.

## Current baseline (one paragraph)

DESIGNER credentials попадают в систему как **литеральные
позиционные элементы** внутри operator-declared
`onec_*_command_template`-массивов. Эти массивы хранятся в
product-config JSON (часто в `%TEMP%/*-writable.config.json` для
local-only flow), валидируются `onec_config` loader'ом как
`list[str]`, передаются в write-server'ные tool'ы, и
рендерятся через `render_command_template(...)` со structural-
placeholder substitution. Никакая ступень в этой цепочке
**не делает env-substitution**, **не делает redaction**, и
**не лечит** то, что cleartext-password literal в template
остаётся cleartext во всех downstream observable артефактах.

## Where credentials enter the flow

1. **Operator authoring.** Оператор пишет product-config JSON.
   Внутри `environments.<env>.onec_dumpcfg_command_template` /
   `onec_applycfg_command_template` /
   `onec_updatedb_command_template` он размещает массив argv
   формы:

   ```jsonc
   [
     "{binary_path}",
     "DESIGNER",
     "/F", "{base_path}",
     "/N", "<user>",
     "/P", "<password>",
     "/DumpCfg", "{output_path}",
     "/DisableStartupMessages"
   ]
   ```

   Структурные позиции (`{binary_path}`, `{base_path}`,
   `{output_path}` и т.д.) — это whitelisted placeholder'ы Track A.
   Позиции `<user>` и `<password>` — это **именно те места**, где
   оператор сегодня вынужден положить literal value, потому что
   платформа не предоставляет другого input mechanism'а.

2. **Файловое хранение.** Product-config JSON живёт где оператор
   сам решит. Track A runbook рекомендует repo-tracked
   `examples/demo-infobase/<name>.config.json` **без** credentials,
   и отдельный local-only overlay вида
   `%TEMP%/<name>-writable.config.json` **с** credentials,
   накрытый правилом из `.gitignore` (Track B / Step 2 baseline:
   `*-writable.config.json`).

3. **Реальный today's path.** На практике, как зафиксировано в
   `PROJECT-STATUS.md` Track A / Step 6 closure, на reference
   stand'е использовался именно `%TEMP%/infobase6-writable.config.json`
   — cleartext, never committed. То есть «out-of-band»,
   декларированный в `SECURITY.md` и `docs/release-handoff.md`,
   фактически реализован как **«положи cleartext в файл вне
   репозитория»**, а не как «передай через secrets-механизм».

## Where they are loaded

`packages/onec-config/src/onec_config/loader.py` (
`load_project_config(...)`) валидирует каждый
`onec_*_command_template`:

- проверяет, что это `list`;
- проверяет, что список не пуст, если поле объявлено;
- проверяет, что каждый элемент — `str`;
- ничего больше: **никакой env-substitution, никакого
  pattern-matching по `/P`, никакого специального handling
  password-like-значений**.

Templates landing'аются как-есть в
`EnvironmentConfig.onec_*_command_template: list[str] | None`
(см. `packages/onec-config/src/onec_config/models.py:103-105`).

## Where they are rendered / propagated

1. **Tool dispatch.** Когда запускается binary-backed write-tool
   (`create_dump_snapshot`, `apply_config_from_files`,
   `update_database_configuration`), его helper в
   `apps/mcp-write-server/src/mcp_write_server/tools.py` вызывает
   `render_command_template(template, substitutions=...,
   allowed_placeholders=...)`.

2. **Render.**
   `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`,
   функция `render_command_template(...)`:

   - итерирует элементы template'а;
   - на каждый строковый элемент применяет
     `raw.format_map(PlaceholderProxy(substitutions))`;
   - `PlaceholderProxy` fail-close'ит на unknown structural
     placeholder;
   - возвращает `list[str]` rendered argv;
   - **никакой второй pass для `${ENV:NAME}` не выполняется**;
   - **никакая password-marker логика не применяется**.

   Результат: для template-элемента `"<password>"` (literal) —
   rendered value тот же `<password>` (literal). Для
   `"${ENV:ONEC_DESIGNER_PASSWORD}"` — тот же literal `${ENV:...}`
   (никто его не интерпретирует).

3. **Subprocess.** Rendered argv list передаётся в
   `onec_process_runner.run_process(...)`, и оттуда — в
   `subprocess` без `shell=True`. Argv-форма сохраняется (Phase
   1–6 invariant).

4. **Payload assembly.** В `binary_dispatch.py`:

   - `binary_backed_payload_fields(command, process_result)` —
     возвращает `command_preview = list(command)` (полный
     rendered argv, **unredacted**), `stdout_excerpt =
     excerpt(process_result.stdout)`, `stderr_excerpt =
     excerpt(process_result.stderr)`;
   - `binary_backed_start_failure_fields(command)` — возвращает
     `command_preview = list(command)` (тоже **unredacted**);
   - `binary_backed_render_failure_fields()` — `command_preview =
     None` (render не успел сложить argv);
   - `stub_honest_mode_fields()` — `command_preview = None`
     (stub branch).

5. **Tool result.** Эти payload-поля попадают в JSON-результат
   write-tool'а, который видит вызывающий MCP-клиент.

6. **Audit row.** Для mutating-tool'ов `run_write_flow`
   discipline записывает audit row, в `details` которого
   попадают payload-поля (включая `command_preview`,
   `stdout_excerpt`, `stderr_excerpt`).

## What is currently redacted and what is not

**Currently redacted: nothing.**

- `command_preview` — copy of rendered argv list, **as-is**.
- `stdout_excerpt` / `stderr_excerpt` — truncated до
  `BINARY_OUTPUT_EXCERPT_LIMIT` через `excerpt()`, но без
  pattern-redaction. Если 1cv8 binary написал что-нибудь
  password-like в stdout/stderr (обычно не пишет, но
  гарантии нет), это останется в excerpt'е.
- audit row's `details` — те же поля, тоже **as-is**.
- ошибочные/диагностические сообщения, если бы они
  embedded'или argv — тоже **as-is** (на практике
  `render_command_template` сообщает только имя поля и
  whitelist, не ren'ит rendered value, но это не contract,
  только сегодняшнее поведение).

То есть если оператор написал `"/P", "<password>"` (literal
value) и сделал binary-backed run, то `<password>` будет
наблюдаем во всех четырёх местах:

- ToolResult JSON (clear),
- audit row на диске (clear),
- product-config файл на диске (clear),
- `%TEMP%/*-writable.config.json` файл на диске (clear).

`.gitignore` ловит только последнее accidental commit (Track
B / Step 2 baseline) — но не убирает наблюдаемость самого
value на диске оператора.

## Why current baseline is risky

Не теоретический list, а конкретные observable risks:

1. **Cleartext landing in audit log.** Audit append-only
   (Phase 1–6 invariant). Любое mutating round-trip оператора
   с literal `<password>` в template'е → **password-видимая**
   запись остаётся в audit-файле навсегда (до ручного
   pruning'а / rotation'а). Это противоречит ожидаемому
   read-side смыслу audit-trail (compliance / forensic
   review).

2. **Cleartext landing in tool result.** MCP-клиенты видят
   rendered argv. Если клиент логирует ToolResult, либо
   hands off в transcript-store (Claude Code session log,
   etc.), cleartext value распространяется уже за пределы
   платформы.

3. **«Out-of-band» как fiction.** Документация говорит
   credentials are «out-of-band», но реальный
   recommended-by-runbook путь = «положи cleartext в JSON,
   ridge'нутый из репо через `.gitignore`». Это аспирация,
   не enforced контракт. Оператор, который буквально следует
   runbook'у Track A, **получает cleartext** на нескольких
   layer'ах одновременно.

4. **No redaction discipline.** Даже если оператор завтра
   ввёл некий локальный shell-trick (например, экспортирует
   env var и делает `envsubst` перед записью JSON), сам
   resolved value снова landing'ается literal'ом в template
   → audit/preview show clear → no benefit от его trick'а.

5. **Backward-compat fiction.** Существующее правило в
   `verify-release.ps1` "Credential leak guard" ловит только
   PEM-блоки и one well-known cloud secret-token. Оно
   намеренно узкое (Track C / Step 2 design) и **не
   рассчитано** ловить «оператор положил literal `/P
   "<value>"` в `*-writable.config.json` и забыл удалить».
   Это honestly зафиксировано в `scripts/release/README.md` —
   но gap остаётся.

## What is explicitly NOT solved yet (will not be solved by Track D either)

Track D — это узкий hardening, не security-program. Поэтому
даже после полного closure Track D, по-прежнему **не решены**:

- **Storage encryption.** No encrypted-at-rest secrets file
  format. Env vars в shell history оператора — separate
  problem; vault / KMS / sops / GPG-encrypted overlays —
  separate problem.
- **Vault / KMS as a baseline.** No HashiCorp Vault, AWS KMS /
  Secrets Manager, Azure Key Vault, GCP Secret Manager
  integration.
- **OS keychain.** Windows Credential Manager / macOS
  Keychain / Linux Secret Service — deliberately optional
  research-only note (см. `track-d-credentials-contract.md`,
  раздел Non-goals); Track D их **не** реализует.
- **SSO / RBAC / multi-user identity.** No federated
  authentication; no role separation; no per-tool RBAC.
- **Federated audit storage.** Audit остаётся local
  append-only. Redaction (Step 3) делает audit safer, но не
  меняет topology audit-storage'а.
- **Network-side hardening.** No production-grade MCP
  transport, no auth on three MCP servers, no mTLS.
- **Prevention of operator self-leak.** Если оператор сам
  подставит literal cleartext в template **и** проигнорирует
  Step 5 heuristic warning, платформа всё равно его запустит
  (backward-compat).

## Step 3 handoff note (no changes here, only enumeration)

Track D / Step 3 (см. `track-d-operator-credentials-hardening-step-map.md`)
будет менять exact три места внутри **одного** файла:

1. `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`,
   `render_command_template(...)` — добавить второй pass для
   `${ENV:NAME}` substitution **после** structural substitution,
   с fail-closed на missing env (по симметрии с
   `UnknownPlaceholderError` discipline).

2. `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`,
   payload-сборщики
   (`binary_backed_start_failure_fields`,
   `binary_backed_payload_fields`) — заменить
   `command_preview = list(command)` на redacted preview через
   новый internal helper (например, `_redact_password_args`).

3. `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`,
   новые internal helper'ы (`_resolve_env_token`,
   `_redact_password_args`) — local to file, не выносятся в
   public surface, не публикуются как новые tools.

**За пределами этого файла Step 3 не должен трогать:**

- `packages/onec-config/src/onec_config/loader.py` — env
  substitution живёт в render-time, не load-time (Q2 default
  из плана трека);
- `packages/onec-config/src/onec_config/models.py` — типы
  template'а остаются `list[str] | None`;
- `apps/mcp-write-server/src/mcp_write_server/tools.py` —
  call-site rendering остаётся прежним;
- `run_write_flow` discipline — единственный mutating-путь;
- structural-placeholder whitelists per tool (Track A
  sealed);
- public surface write-server'а — никаких новых tools
  (registries `read=15 / write=25 / intelligence=16`).

Подробный normative contract — в `track-d-credentials-contract.md`.

## Что этот документ **не** делает

- Не fixирует поведение. Это descriptive doc.
- Не вводит новые abstractions. Их вводит companion contract.
- Не показывает реальных credentials. Только abstract forms
  (`<user>`, `<password>`, `${ENV:NAME}`, `"redacted"`).
- Не претендует на полный security-audit платформы.
  Audit-scope узкий: только credentials flow в trinity
  «product-config → render → preview / audit excerpt».
- Не обещает enterprise-vault / cloud-KMS / OS-keychain. Это
  permanent out-of-scope Track D (см. companion).
