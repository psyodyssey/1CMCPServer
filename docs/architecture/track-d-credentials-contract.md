# Track D — Credentials contract (target)

> **Status.** Track D / Step 2 — docs-only. Этот файл — normative
> target contract для Step 3 implementation. Никакого кода не
> меняется здесь и сейчас. Все примеры используют только abstract
> formы: `<user>`, `<password>`, `${ENV:NAME}`, `"redacted"`. Реальных
> значений в этом документе нет и не должно появиться.
>
> **Companion file:** `track-d-credentials-flow-audit.md` (current
> baseline). Audit описывает «как сейчас», этот файл — «как должно
> быть» после Step 3.

## Purpose / scope

Зафиксировать минимальный safer contract на:

- **input mechanism** для DESIGNER credentials в
  `onec_*_command_template`: env-substitution форма
  `${ENV:NAME}`;
- **resolution semantics** во время render'а argv: order,
  fail-closed, backward-compat;
- **redaction discipline** в observable artefacts:
  `command_preview`, payload excerpt'ы, audit row's
  `details`.

Out-of-scope этого документа: implementation, line-level patch
note, тестовый план. Это contract document. Implementation идёт
на Step 3 строго по этому контракту.

## Target syntax

**Единственная новая форма в template-элементе — `${ENV:NAME}`.**

```jsonc
[
  "{binary_path}",
  "DESIGNER",
  "/F", "{base_path}",
  "/N", "${ENV:ONEC_DESIGNER_USER}",
  "/P", "${ENV:ONEC_DESIGNER_PASSWORD}",
  "/DumpCfg", "{output_path}",
  "/DisableStartupMessages"
]
```

Правила синтаксиса:

- Token имеет **строго** форму `${ENV:NAME}`. Префикс `${ENV:` —
  явный namespace, чтобы не пересекаться со structural
  placeholder'ами Track A (`{binary_path}` etc.).
- `NAME` — non-empty, символы `[A-Za-z_][A-Za-z0-9_]*` (стандартное
  POSIX env-var name shape). Нижнее подчёркивание разрешено;
  цифры в начале — нет.
- Token может быть **только полным значением argv-элемента**, не
  substring'ом. То есть `"${ENV:ONEC_DESIGNER_PASSWORD}"` — OK;
  `"prefix-${ENV:NAME}"` — **не** поддерживается на этом slice'е
  (явный non-goal: keep substitution surface narrow и предсказуемой
  для redaction).
- В одном template-элементе не более одного env-token'а. Литерал
  smешанный со структурным placeholder'ом в одном элементе тоже
  не поддерживается (`"{binary_path}-${ENV:X}"` не resolved). Это
  явное упрощение — оператор всегда может разделить на два argv-
  элемента.
- Никакие другие env-substitution syntaxes (`$NAME`, `<<env:NAME>>`,
  shell-style `${NAME:-default}`) **не** поддерживаются. Узкая
  surface уменьшает false-positive scan'а Step 5 heuristic'и.

## Resolution rules

Resolution живёт **в render-time, внутри
`render_command_template(...)`**, а не в load-time
`onec_config.loader`. Обоснование: единая fail-closed дисциплина с
existing structural-placeholder discipline; единый код для
redaction, который наблюдает уже rendered argv.

**Order of operations** на каждый template-элемент:

1. **Structural-placeholder substitution** — текущая логика
   `format_map(PlaceholderProxy(substitutions))` (Track A
   sealed). Unknown structural placeholder → `ValueError` →
   render-fail branch (как сейчас).
2. **Env-substitution pass** — выполняется **после** structural
   substitution, на уже-substituted элементе.
   - Если элемент **не** содержит `${ENV:` — оставляется
     как есть (literal cleartext path: backward-compat).
   - Если элемент **точно** соответствует `${ENV:NAME}`
     pattern'у — `NAME` извлекается, делается lookup в
     `os.environ`, и:
     - если `NAME` присутствует и value `!= ""` — элемент
       заменяется на value;
     - если `NAME` отсутствует или value пустой — render-fail
       branch (см. Fail-closed semantics).
3. **Redaction pass для preview** — выполняется **после**
   полного rendering'а argv list'а, на копии rendered list, для
   `command_preview` поля payload'а. Actual subprocess argv
   остаётся **unredacted** (иначе binary не аутентифицируется).

Структурно это два отдельных passа над одним элементом
(structural → env), плюс третий pass над собранным argv
list'ом (redaction для preview).

## Fail-closed semantics

Missing env var **не** превращается в empty value (`""`) и **не**
логируется как warning. Это **render-failure** — то же honest
fail-closed, что и unknown-structural-placeholder.

Конкретно:

- Tool возвращает `ok=False` payload.
- `mode = "binary-backed"` (оператор объявил binary-backed
  contract — env-substitution-token говорит ровно это).
- `binary_invoked = False` (никакого subprocess'а не
  запущено).
- `command_preview = None` (render-fail branch — argv list не
  собран до конца).
- `exit_code = None`.
- `stdout_excerpt = None`, `stderr_excerpt = None`.
- Honest reason в payload (точное сообщение — design Step 3,
  но обязательно: имя поля template, имя missing env-var'а
  как ключ-индикатор, **без** value lookup, **без**
  раскрытия других env-var'ов).

Empty-string value (`os.environ["NAME"] == ""`) **тоже**
fail-closed. Causes too many subtle failure modes
(authentication против 1cv8 binary с пустым `/P` имеет
платформо-зависимое поведение). Лучше явный fail.

Эта дисциплина симметрична существующему
`UnknownPlaceholderError` flow в `render_command_template`.

## Redaction contract

**Что редактируется:**

- В `command_preview` — value, идущее **позиционно сразу
  после** argv-элемента, который case-insensitive равен `/P`
  или `/Pwd`, заменяется на literal строку `"<redacted>"`
  (или эквивалентный sentinel — final wording в Step 3).
- В `stdout_excerpt` / `stderr_excerpt` — **не редактируется
  на Step 3.** Truncation остаётся через `excerpt(...)`.
  Pattern-redaction в captured 1cv8 output — отдельный, более
  широкий heuristic, который намеренно out-of-scope: 1cv8
  стандартно не пишет password в stdout/stderr, и
  pattern-matching в free-form binary output даст
  непредсказуемые false positives. Если в будущем reference
  stand покажет cleartext password в output — это будет
  open follow-up, не Track D.

**Что НЕ редактируется:**

- **Actual subprocess argv list.** Тот, который передаётся
  в `subprocess` runner. Иначе 1cv8 binary не
  аутентифицируется. Redaction — **observation-side**,
  не **execution-side**.
- **Audit row's `details`.** На Step 3 audit row будет
  получать **уже-редактированный** `command_preview`
  через payload-сборщик. То есть audit row тоже видит
  redacted preview, не unredacted argv.
- **Other argv elements.** Token, идущий после argv-элементов,
  **не** равных `/P` / `/Pwd` (case-insensitive), не
  редактируется. Например, token после `/N` (`<user>`) —
  не считается password по этому contract'у. Username не
  имеет той же sensitivity, и его redaction давал бы
  ложное чувство security при отсутствии действительного
  password redaction'а.

**Markers (case-insensitive):**

- `/P`
- `/Pwd`
- `/PWD`

Проверка — case-insensitive equal на argv-элемент целиком.
Substring-match (`-Password`, `--pass`) намеренно не
поддерживается: 1cv8 CLI conventions используют ровно `/P`
и `/Pwd`, и расширение pattern'а размывает контракт.

## Backward compatibility contract

**Legacy cleartext path остаётся supported.**

- Template-элемент `<password>` (literal value, не
  `${ENV:...}`) — render-time проходит как сейчас (literal
  passes through structural substitution unchanged, env-
  substitution pass его не трогает).
- Subprocess запускается успешно (если все остальные
  prereq'ы зелёные).
- Tool returns `ok=True` (если binary вернул `exit_code=0`).
- Никакого warning'а в payload не появляется.

**Но:**

- `command_preview` всё равно проходит через redaction pass.
  Если literal `<password>` стоит в argv-позиции сразу после
  `/P` / `/Pwd`, в preview он будет заменён на
  `"<redacted>"`. То есть legacy literal **тоже получает
  observation-side redaction** — это backward-compat для
  execution path'а, но не для observability path'а.
- Step 5 (release-verify credential-hygiene heuristic)
  репортит наличие cleartext literal в tracked
  `*.config.json` как WARN (не FAIL по default). Operator
  может explicitly opt-in / proceed; гарантия
  detect-best-effort, не enforce.

**No breaking change.** Существующие product-config'и,
прошедшие через cleartext literal, после Step 3 продолжают
работать без правки. Migration на `${ENV:...}` —
recommended path, не requirement.

## Non-goals

Этот contract **не**:

- вводит storage encryption (no encrypted-at-rest secrets
  file format);
- интегрирует HashiCorp Vault, AWS KMS / Secrets Manager,
  Azure Key Vault, GCP Secret Manager как baseline;
- интегрирует OS keychain (Windows Credential Manager,
  macOS Keychain, Linux Secret Service / `keyring` Python
  lib) — deliberately optional research-only note в Step
  2 audit doc, не имплементируется в Track D;
- меняет `subprocess` argv discipline (no `subprocess.Popen(
  env=...)` для password — 1cv8 CLI требует password
  позиционно, как `/P <value>`);
- меняет structural-placeholder whitelist per tool (Track A
  sealed);
- меняет registry counts (`read=15 / write=25 /
  intelligence=16` invariant);
- вводит новые MCP tools;
- меняет `run_write_flow` discipline (single mutating path);
- расширяет redaction на stdout/stderr binary output
  (deliberate out-of-scope);
- редактирует username (`/N` token) — see Redaction contract;
- предотвращает self-leak оператора (оператор может
  игнорировать Step 5 heuristic; платформа не блокирует);
- вводит SSO / RBAC / multi-user identity / federated audit
  / production-grade MCP transport / network hardening.

## Step 3 implementation boundary

Step 3 будет реализовывать этот contract внутри **одного**
файла:

`apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`

Конкретно:

- `render_command_template(...)` — добавляется второй pass
  (env-substitution) после structural substitution; missing
  / empty env → render-fail branch с honest reason.
- payload helpers — `binary_backed_start_failure_fields(...)`
  и `binary_backed_payload_fields(...)` начинают строить
  `command_preview` через новый internal helper
  `_redact_password_args(rendered_argv)` вместо
  `list(command)` напрямую.
- новые internal helpers (`_resolve_env_token(token)`,
  `_redact_password_args(argv)`) — local to file, не
  публикуются как public surface.

Step 3 **не должен** трогать:

- `packages/onec-config/src/onec_config/loader.py` —
  template'ы остаются `list[str] | None`, без env-handling
  на load time;
- `packages/onec-config/src/onec_config/models.py` — shape
  без изменений;
- `apps/mcp-write-server/src/mcp_write_server/tools.py` —
  call-sites не меняются (они передают template и
  substitutions как раньше);
- existing structural-placeholder whitelists per tool;
- `run_write_flow` flow;
- intelligence-server / read-server (read = 15,
  intelligence = 16 — invariant);
- product-layer surface (`apps/platform/`) — не зависит от
  этого slice'а;
- runbook / SECURITY.md / release-handoff.md / operator-
  manual.md — это Step 4;
- `verify-release.ps1` — это Step 5;
- `pyproject.toml` version — резолвится в Step 6.

**Tests/dev-check expectations** (для Step 3, не здесь):

- `${ENV:NAME}` resolved → render OK; rendered argv для
  subprocess содержит resolved value;
- missing env → render fail-closed (`mode=binary-backed`,
  `binary_invoked=False`, `command_preview=None`);
- empty env value → render fail-closed (same);
- `command_preview` после `/P` / `/Pwd` (case-insensitive)
  редактируется на `"<redacted>"`;
- token, идущий после `/N` (username), не редактируется;
- legacy literal cleartext: render OK, preview редактирован
  по позиции (если стоит после `/P`);
- registries `read=15 / write=25 / intelligence=16` без
  drift'а;
- `selfcheck_status=ok`.

## Что этот документ **не** делает

- Не имплементирует ни одного из правил выше — implementation
  идёт на Step 3 строго по этому контракту.
- Не обещает enterprise-vault / cloud-KMS / OS keychain (см.
  Non-goals).
- Не показывает реальных credentials.
- Не специфицирует exact wording для error message'а или
  log line'а — это Step 3 polish.
- Не вводит redaction для stdout/stderr binary output (out
  of scope).
