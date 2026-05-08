# Parallel Track D — Operator Credentials Hardening (план трека)

> **Status.** Step 1 (planning) — этот документ + step-map. Кода
> не правит. Production-код не трогается. Никаких новых MCP tools.
> Registry-инвариант `read=15 / write=25 / intelligence=16`
> сохраняется без изменений.

## Назначение трека

Phase 1–6 закрыты; Track A закрыл real binary-backed write path;
Track B закрыл базовую productization-полировку; Track C закрыл
delivery / packaging / handoff слой. После Track C самый узкий и
честно зафиксированный незакрытый разрыв — **operator credentials
flow**.

Сегодня DESIGNER credentials попадают в систему через
`onec_*_command_template` массивы внутри product-config'а. Каждый
такой template содержит **литеральные позиционные аргументы**
`"/N"` `"<user>"` `"/P"` `"<password>"`. Платформа не делает
env-substitution в этих template'ах — placeholder-движок
поддерживает только whitelisted **structural** placeholder'ы
(`{binary_path}`, `{output_path}`, `{base_path}`, `{base_id}`,
`{publication_name}`, `{http_base_url}`). Это значит, что в
текущем baseline:

- Самый прямой путь, описанный в runbook'е Track A, — оператор
  пишет cleartext password прямо в JSON template.
- "Out-of-band" документирован в `SECURITY.md`, `docs/release-
  handoff.md`, `CHANGELOG.md` и Track B / Track C plan'ах как
  набор возможностей (env vars / OS keychain / local-only writable
  config), но **сама платформа** ни одной из этих опций не
  реализует — она просто принимает любой массив строк и подаёт
  его в `subprocess`.
- Local-only writable config flow (`%TEMP%/*-writable.config.json`)
  остаётся cleartext по design'у; `.gitignore` (Track B / Step 2)
  ловит accidental commit таких файлов, но не убирает риск.
- `command_preview` excerpt в payload'ах write-tool'ов и audit
  rows показывает rendered argv. Если operator положил cleartext
  пароль литералом — он попадает в `command_preview`.

Этот разрыв был honestly зафиксирован уже трижды:

- `docs/architecture/track-c-packaging-installer-delivery-plan.md`
  явно называет «operator credentials hardening track» как
  отдельный логический трек.
- `PROJECT-STATUS.md` в Track B / Step 6 closure и Track C / Step
  6 closure перечисляет «operator credentials hardening track
  (env-substitution или OS keychain integration)» как
  recommended-but-not-auto-opened candidate.
- `SECURITY.md` фиксирует "operator credentials are out-of-band"
  как honest constraint.

Track D переводит этот honest constraint в **узкий реализованный
hardening-trek**, не превращая проект в enterprise-secrets
программу.

## Целевой результат

Receive-side оператор:

1. Может выставить DESIGNER credentials через **документированный
   env-substitution путь** в template'ах product-config'а — без
   правки самого config-файла под каждую новую базу или машину.
2. Видит из repo, что cleartext-password-literal в template — это
   **legacy / explicit-opt-in fallback**, а не «нормальный
   baseline».
3. Получает от платформы **redacted** `command_preview` /
   `stdout_excerpt` / `stderr_excerpt`, в которых resolved
   password value не воспроизводится — даже если оператор сам
   положил cleartext в template как fallback.
4. Получает honest миграционный путь: как существующий
   cleartext-template превратить в env-substitution-template
   за один шаг.
5. Получает узкий **credential-hygiene heuristic** в
   `verify-release.ps1`, который ловит наиболее очевидный
   паттерн утечки — литеральный `/P "<value>"` в
   tracked `*.config.json` без env-substitution-формы.

И **не получает** ничего из enterprise-secrets вселенной (см.
ниже).

## Что Track D **не** закрывает (явно)

- **Enterprise secrets-as-a-service** — HashiCorp Vault, AWS KMS /
  Secrets Manager, Azure Key Vault, GCP Secret Manager. Track D
  не интегрирует ни одно из этих хранилищ как baseline. Если
  оператор хочет такое — env-substitution honestly остаётся точкой
  входа: оператор сам разрешает env vars из своего vault'а
  (например, через `vault kv get | export`).
- **SSO / RBAC / multi-user identity / multi-tenant secret
  brokerage** — это другая вселенная (parallel track для
  enterprise super-set'а), которая в Track D не открывается.
- **Cloud KMS как обязательная база** — Track D остаётся
  applicable к local single-operator workflow.
- **Encrypted-at-rest secrets file format / age / sops / pass /
  GPG-encrypted overlays** — оптом не вводятся; env-substitution
  это **input mechanism**, не storage mechanism.
- **OS keychain integration как baseline** — Windows Credential
  Manager / macOS Keychain / Linux Secret Service возможны как
  **optional research note** в Step 2, но не входят в core
  Track D. Они были бы tier-2 расширением, требующим dependency
  (`keyring`) и cross-platform тестов.
- **Replacement of `subprocess` argv discipline** — `subprocess`
  без `shell=True` остаётся; argv-list форма не меняется. Track D
  не вводит env=... через `subprocess.Popen(env=...)` потому, что
  1cv8 CLI требует пароль именно как `/P <value>` позиционно.
- **Production-grade MCP transport / authentication / network
  hardening** — это совсем другой track.
- **Полная rollback/delete-вселенная, AST-парсер, multi-version 1С
  matrix, web-UI, hot reload** — out of scope, как и в Track A /
  B / C.
- **Новые MCP tools.** Registries `read=15 / write=25 /
  intelligence=16` сохраняются точно. Никаких новых boundaries в
  product layer'е.
- **Remote push / GitHub publishing.** Operator decision, не
  часть трека.

## Guardrails

- **Никаких реальных credentials в repo / docs / commit message /
  отчётах.** Всё описание — через abstract placeholder forms
  (`<password>`, `${ENV:ONEC_DESIGNER_PASSWORD}`, `<user>`).
- **Никаких изменений в registry / surface.** Никаких новых MCP
  tools на Track D. Все шаги ниже не расширяют public surface
  (`run_write_flow` discipline carrier, intelligence-server stays
  read-only, etc.).
- **Backward-compat для legacy cleartext template.** Существующие
  product-config'и с cleartext password literal'ом продолжают
  работать после implementation step'а. Migration — это
  recommended path, не breaking change.
- **Fail-closed на unresolved env-substitution.** Если template
  ссылается на env var, которая не выставлена, — render-time
  `ok=False` honest failure до запуска subprocess'а, по аналогии с
  unknown-placeholder discipline'ом Track A.
- **Redaction-by-default в `command_preview`.** Любая часть argv,
  которая идёт сразу после `/P` или `/Pwd` (case-insensitive
  match по 1С CLI conventions), редактируется в excerpt'ах
  payload'а и audit row'и. Это **observation-side** redaction;
  фактический argv для `subprocess` остаётся unredacted (иначе
  binary не аутентифицируется), но excerpt — нет.
- **Никаких `shell=True`.** Phase 1–6 invariant сохраняется.
- **No new files in `apps/*/src` или `packages/*/src` без
  обоснования.** Если env-substitution живёт в `onec-config`
  loader'е — это minimal, focused change, не новый сервис.
- **No remote push.** Track D не пушит ничего на GitHub. Repo
  state остаётся local после closure.

## Критерии приёмки

Track D считается closed, когда честно выполнены все 10:

1. Step-map ship'нут (этот документ + step-map.md).
2. Credentials-flow audit (Step 2) задокументирован: точные места
   где cleartext password может появиться, точные payload-поля
   которые видят rendered argv.
3. Credentials contract (Step 2) формализован: синтаксис
   `${ENV:NAME}` (или эквивалентный), resolution order, fail-
   closed semantics, redaction contract.
4. Env-substitution implementation (Step 3) шипнут в loader'е /
   dispatcher'е write-server'а: literal `${ENV:NAME}` в template
   → resolved at render time → fail-closed на missing env.
5. Redaction implementation (Step 3) активна: `command_preview`,
   `stdout_excerpt`, `stderr_excerpt` редактируют value сразу
   после `/P` / `/Pwd` literal.
6. Operator docs (Step 4) обновлены так, что **default**
   рекомендованный путь — env-substitution, а не cleartext: Track
   A runbook, `SECURITY.md`, `docs/release-handoff.md`,
   `docs/operator-manual.md` пересогласованы.
7. Migration note (Step 4) ship'нут: один short paragraph для
   операторов, у которых уже есть cleartext-config.
8. `verify-release.ps1` credential-hygiene heuristic (Step 5)
   добавлен: ловит литеральный `/P "<value>"` в tracked
   `*.config.json`, где `<value>` не env-substitution-формы.
   Узкая heuristic, не full DLP.
9. Registry-инвариант сохранён: `read=15 / write=25 /
   intelligence=16`, `selfcheck_status=ok`, `verify-release.ps1`
   GREEN на closure.
10. Closure pass (Step 6) обновляет README / PROJECT-STATUS /
    CHANGELOG; honest constraints чётко перечисляют, что
    остаётся out-of-scope (enterprise vault, SSO/RBAC, cloud KMS
    baseline, encrypted-at-rest config).

## Открытые вопросы (resolve в Step 2+)

- **Q1.** Точный синтаксис env-substitution. Кандидаты:
  `${ENV:NAME}` (явный namespace, легко grep'нуть), `$NAME`
  (compatible с большинством shell traditions, но коллизии с
  literal '$' в template'ах), `<<env:NAME>>` (ничего не
  рекомендует автоматически). **Default recommend: `${ENV:NAME}`**
  — explicit и не пересекается с whitelisted structural
  placeholders Track A `{binary_path}` etc.
- **Q2.** Где живёт substitution: в `onec-config` loader'е (на
  load-time, до того как template попадает в `binary_dispatch`)
  или внутри `binary_dispatch.render_command_template` (на
  render-time, рядом с structural placeholder'ами). **Default
  recommend: render-time в `binary_dispatch`** — единая
  fail-closed дисциплина, единый код redaction'а.
- **Q3.** Redaction pattern. Какой ровно literal перед value
  считается password-marker'ом: только `/P`, или `{`/Pwd`/`/PWD`}
  тоже, и нужен ли case-insensitive match. **Default recommend:
  `/P` and `/Pwd` (case-insensitive)** — покрывает 1С CLI
  conventions, не fабрикует false positive на других флагах.
- **Q4.** Backward-compat semantics: при наличии cleartext literal
  в template — warning в payload meta или silent? **Default
  recommend: silent в payload (legacy не ломаем), но Step 5
  credential-hygiene heuristic репортит это в `verify-release.ps1`
  finding'е.**
- **Q5.** OS keychain integration scope. **Default recommend:
  research-only note в Step 2** (короткая секция «could-be-tier-2
  via `keyring` Python lib, deliberately not in scope»). Никакой
  implementation в Track D.
- **Q6.** CHANGELOG cadence. **Default recommend: один update на
  closure Track D**, симметрично Track B / Track C.
- **Q7.** Версия `pyproject.toml`. **Default recommend: bump до
  `0.2.0`** на closure Track D — это первый трек, который меняет
  observable behaviour write-server'а (даже если backward-
  compatible). Альтернатива: оставить `0.1.0` и дописать в
  CHANGELOG как "0.1.0 development line". **Default recommend
  bump до 0.2.0**, но resolve финально в Step 6.

## Связь с Phase 6 / Track A / Track B / Track C

- **Phase 1–6.** Single mutating path discipline (`run_write_flow`)
  не трогается. Audit append-only остаётся. Fail-closed defaults
  расширяются ещё одним классом: unresolved env-substitution.
- **Track A.** Real binary-backed write contract сохраняется без
  изменений. Operator-declared argv-templates остаются
  authoritative. Track D **не** меняет structural-placeholder
  whitelist (`{binary_path}` etc.) — он добавляет ортогональный
  механизм env-substitution для **значений**, не для
  **структурных полей**.
- **Track B.** `.gitignore` для `*-writable.config.json` остаётся
  как is. Repo hygiene baseline уже покрывает «не закоммитить
  local writable config случайно».
- **Track C.** `verify-release.ps1` credential-leak guard
  (PEM/AWS-token check) сохраняется. Step 5 Track D **расширяет**
  его новой heuristic'ой, не заменяет existing checks.
- **Что Track D **не** делает индустриальным продуктом** — см.
  ниже.

## Что Track D **не делает** «глубоким индустриальным продуктом» после closure (honest constraints)

Даже после полного closure Track D, по-прежнему отсутствуют:

- Production-grade MCP transport (нет authentication / authorisation
  / network hardening / mTLS).
- Полный enterprise super-set (SSO/RBAC, multi-tenant, secrets
  vault как сервис, federated audit storage, policy-as-code DSL,
  multi-instance HA).
- GUI installer wizard / `.msi` / `.deb` / signed binary
  distribution / publication к package managers.
- Web-UI / dashboard frontend.
- Multi-version 1С matrix smoke (single-version `8.3.27.1859`).
- Полный AST-парсер XML/BSL.
- Полная rollback/delete-вселенная (whitelist остаётся small).
- Hot reload / OS-level service supervision / `__main__` /
  CLI у трёх MCP-серверов с auth.
- Encrypted-at-rest secrets file format.
- Vault / KMS integration как baseline.
- OS keychain integration (deliberately optional / out-of-scope).
- Cross-OS smoke (Track D Windows-first, по симметрии с Track C
  Q4).

Эти направления остаются за пределами Track A + Track B + Track
C + Track D — открытие отдельных тематических parallel track'ов
под них — operator decision.

## Структура шагов

См. отдельный файл `track-d-operator-credentials-hardening-step-map.md`.
Шесть шагов:

1. Step 1 — planning (этот документ + step-map).
2. Step 2 — credentials-flow audit and contract (docs-only).
3. Step 3 — env-substitution implementation + redaction.
4. Step 4 — operator docs / migration / handoff alignment.
5. Step 5 — release-verify credential-hygiene heuristic.
6. Step 6 — final integration pass and Track D closure.

## Что **не** входит в Track D (повтор для ясности)

- enterprise vault platform / cloud KMS baseline,
- SSO / RBAC / multi-tenant identity,
- federated audit storage,
- production-grade MCP transport / auth,
- multi-version 1С matrix,
- web-UI / dashboard,
- GUI installer / signed distribution / package-manager
  publication,
- new MCP tools (registries 15/25/16 invariant),
- 1cv8 binary changes,
- OS keychain implementation (optional research note only),
- encrypted-at-rest secrets format,
- remote push / GitHub publishing,
- production code rewrite за пределами locator'а env-substitution
  и redaction discipline.

**GitHub remote push** — operator action, не часть трека.

## Pre-resolve recommendation для Step 2+

Default'ные ответы на Q1–Q7 (Step 2 может их override'нуть с
обоснованием):

- Q1: env-substitution syntax = `${ENV:NAME}`.
- Q2: substitution живёт в `binary_dispatch.render_command_template`
  (render-time, единая fail-closed discipline).
- Q3: redaction marker = `/P` and `/Pwd` (case-insensitive).
- Q4: cleartext literal — silent в payload, репортится только
  `verify-release.ps1` heuristic'ой.
- Q5: OS keychain — research-only note, no implementation.
- Q6: один CHANGELOG update на closure.
- Q7: version bump 0.1.0 → 0.2.0 на closure (resolve финально в
  Step 6).
