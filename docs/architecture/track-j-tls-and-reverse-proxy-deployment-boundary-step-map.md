# Parallel Track J — TLS and Reverse-Proxy Deployment Boundary (step map)

> **Companion file:**
> `track-j-tls-and-reverse-proxy-deployment-boundary-plan.md`
> (план трека). Этот файл — пошаговый map. Каждый шаг
> открывается отдельным заходом, не комбинируется в один
> commit с другим step'ом.

> **Track invariants** (повтор из плана §6; нарушение любого
> = stop and surface, не silent fix):
> - registries `read=15 / write=25 / intelligence=16` без
>   drift'а на каждом step;
> - никаких новых MCP tools;
> - Track H + Track I auth surfaces (`ProductAuthSettings`,
>   `ProductConfig.auth`, `_parse_auth`,
>   `_AUTH_ENV_TOKEN_RE`, `_resolve_token_sources`,
>   `_resolve_env_token`, `Authorization` header parsing,
>   case-insensitive scheme, `hmac.compare_digest`,
>   failure-equivalence rule, fail-closed startup gate,
>   redaction discipline, install fast-path round-trip
>   integrity) preserved byte-identical;
> - `mcp_common/__init__.py` `__all__` byte-identical
>   (10 names);
> - existing `_stdio_transport.py` byte-identical;
> - existing 3 `__main__.py` byte-identical (Step 4 PATH B/C
>   may make narrow additive change only if absolutely
>   justified by Step 3 contract; default PATH A docs-only
>   leaves them untouched);
> - existing `[project.scripts]` block byte-identical;
> - `[tool.hatch.build.targets.wheel] packages = []`
>   preserved (Track C honest constraint carried through);
> - никакого `[project.dependencies]` / `[project.optional-
>   dependencies]` block changes;
> - никакого back-door write channel; `run_write_flow`
>   discipline для write-tools preserved;
> - read-only-by-construction discipline для intelligence-
>   server preserved;
> - **Track H Step 3 §13.1 in-process-TLS-forbidden
>   invariant inherited and NOT reversed**; Track J
>   formalizes the reverse-proxy alternative, не
>   reverses TLS forbid;
> - никаких 1cv8.exe runs ни на одном шаге трека;
> - production code touched **только в Step 4** и только
>   если Step 3 contract resolves to PATH B/C; PATH A
>   docs-only leaves all production code byte-identical;
> - никаких real credentials в repo / docs / commit
>   messages;
> - никакого secret storage / vault / KMS / OS keychain
>   integration;
> - никакого packaging ecosystem (`.msi` / `.deb` / signed
>   distribution / PyPI publication / wheel publication)
>   beyond existing `[project.scripts]`;
> - никакого supervisor / service registration / hot reload
>   / web UI / standalone `apps/platform` entrypoint в
>   текущем scope трека;
> - никакого enterprise identity stack
>   (SSO / OIDC / RBAC / multi-tenant);
> - GitHub remote push — operator action, не часть трека.

---

## Step 1 — planning TLS and reverse-proxy deployment boundary (этот шаг)

**Цель.** Зафиксировать документационный вход в Track J:
назначение трека (formalize "trusted-network behind
operator-owned reverse proxy" general-policy в operator-
facing deployment-boundary contract), целевой результат,
что закрывает / не закрывает Track J, чем отличается от
Tracks A–I, guardrails, acceptance criteria, открытые
вопросы Q1–Q7 с default recommendations. Кода не писать.

**Что меняем.** Только два planning-документа:

- `docs/architecture/track-j-tls-and-reverse-proxy-deployment-boundary-plan.md`
  (новый, plan-уровень).
- `docs/architecture/track-j-tls-and-reverse-proxy-deployment-boundary-step-map.md`
  (новый, step-map; этот файл).

Плюс минимальные status-правки в `README.md` и
`PROJECT-STATUS.md` под открытие active track'а J:

- `README.md` — Quickstart paragraph (после Track I closure
  говорит «Активного трека сейчас нет» — переводим в
  «Активный трек: Track J planning-only, Step 1»);
  «Active parallel track» секция (после Track I closure
  компактна — добавляем minimal Track J opening block с
  pointer'ом на planning docs).
- `PROJECT-STATUS.md` — header `Текущий шаг` + `Статус`
  переводим из «Активного шага нет» / `closed` для Track I
  в `in progress` для Track J / Step 1; добавляем одну
  новую per-step opening section
  `### Parallel Track J / Step 1 — planning TLS and
  reverse-proxy deployment boundary (завершён)`
  симметрично Track I / Step 1 / Track H / Step 1
  patterns.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `.github/`, `.editorconfig`,
`.python-version`, `.gitignore`, `examples/`, `LICENSE`,
`SECURITY.md`, `CHANGELOG.md`, `docs/release-handoff.md`,
`docs/operator-manual.md`, `docs/administrator-manual.md`,
`docs/developer-manual.md`, `docs/runbooks/*`,
`apps/platform/README.md`, `apps/*/src/**`,
`packages/*/src/**`, `_stdio_transport.py`,
`_network_transport.py`, three `__main__.py`,
`installer.py` — без изменений на Step 1.

**Результат.** Track J открыт как active planning-only
трек. Implementation Step 4 не открывается в этом же
заходе. Никаких production code changes; никаких registry
changes; никаких 1cv8.exe runs.

---

## Step 2 — deployment-boundary baseline audit (docs-only)

**Цель.** Честно описать current state network/deployment
surface с точки зрения formalized-vs-not-formalized
deployment-boundary contract. Resolve Q1 (TLS posture
target = hybrid reverse-proxy-first), Q2 (Step 4 PATH
choice based on evidence), Q3 (deployment threat model),
Q4 (deployment surfaces enumerated). Никакого code change.
Никакого 1cv8.exe.

**Что меняем.** Один новый descriptive audit-документ:

- `docs/architecture/track-j-deployment-boundary-baseline-audit.md`
  (новый, descriptive read-only audit).

Плюс минимальные status-правки в `PROJECT-STATUS.md` под
закрытие Step 2 (новая `### Parallel Track J / Step 2 —
deployment-boundary baseline audit (завершён)` section).

**Содержимое audit-документа** (минимальный obligatory
shape):

1. **Inventory existing TLS / reverse-proxy / bind-host
   text** in:
   - `track-h-network-transport-and-auth-contract.md` §13
     (in-process TLS forbidden + operator deployment model
     + mTLS out-of-scope);
   - `SECURITY.md` "Honest constraints" "Local stdio plus
     narrow HTTP+bearer transport baseline" block (threat
     model wording);
   - `docs/release-handoff.md` "What is in this handoff" /
     "What is NOT in this handoff" / "Local check / launch
     sequence" / "Known limitations";
   - `apps/platform/README.md» «Hostile-network transport /
     enterprise auth / supervisor» item;
   - `scripts/dev/launch.ps1` + `scripts/dev/README.md`
     header-comment / Show-Usage / parenthetical wording
     про trusted-network deployment behind reverse proxy.
2. **Inventory `_network_transport.py` runtime behaviour**:
   - `_parse_bind` validation rules (`gethostbyname` +
     1..65535 port range);
   - `_serve_http` listener creation
     (`ThreadingHTTPServer((bind_host, bind_port), ...)`);
   - `_MCPHandler` HTTP method routing (POST `/mcp` /
     non-POST → 405 / non-`/mcp` → 404);
   - forwarded-header treatment (X-Forwarded-* пропускаются,
     не consult'ятся для auth);
   - response shape for unauthenticated request (401 +
     `WWW-Authenticate` + JSON-RPC `-32001`).
3. **4-class breakdown** of deployment-boundary surfaces:
   - **CLASS 1 — already formalized at general-policy
     level**: Track H §13 in-process-TLS-forbidden +
     reverse-proxy-deployment-model + mTLS-out-of-scope;
     SECURITY.md threat-model wording.
   - **CLASS 2 — partially documented, scattered across
     multiple files**: bind-host SHOULD-recommendation
     (Track H §13.2 + SECURITY.md but not single-source);
     reverse-proxy header treatment (not explicitly stated
     anywhere, only inferable from auth model).
   - **CLASS 3 — clearly missing**: single-source-of-truth
     operator-facing deployment recipe; concrete
     reverse-proxy config snippets; exposure-rules matrix
     for three scenarios; explicit `/healthz` endpoint
     resolution.
   - **CLASS 4 — explicitly out-of-scope**: in-process TLS
     / mTLS / OAuth / OIDC / SAML / SCIM / RBAC /
     multi-tenant / WAF / IDS / rate-limit / observability
     stack / service supervisor / packaging ecosystem /
     web UI / standalone `apps/platform` / new MCP tools /
     1cv8 / rollback / multi-version expansion / GitHub
     remote push.
4. **Q1 resolution** (final): hybrid = reverse-proxy-first
   default + in-process TLS deferred (carry-over Track H
   §13.1 forbidden Step 4 baseline).
5. **Q2 resolution** (directional): PATH choice based on
   audit evidence. The audit must surface whether bind-
   host warning, `/healthz` endpoint, или other narrow
   additions materially help operator-facing reverse-proxy
   integration vs being just-doc-able.
6. **Q3 resolution**: trusted internal network behind
   operator-owned reverse proxy (operator owns DNS / TLS
   / firewall / proxy config; network между proxy и
   listener trusted; explicitly NOT hostile-internet by
   default).
7. **Q4 resolution**: enumerate exact deployment surfaces
   for Step 3 contract — bind host/port choice, reverse-
   proxy headers, TLS termination point, forwarded-
   identity assumptions, exposure rules, three-scenario
   matrix.
8. **Open questions для Step 3 contract**: точная shape
   reverse-proxy config snippets (nginx + Caddy minimal
   examples? только prose?); точная shape `/healthz`
   endpoint decision (ship in PATH B/C or defer with
   rationale?); точная shape PATH B/C scope если
   chosen.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `SECURITY.md`, `CHANGELOG.md`,
`docs/release-handoff.md`, `apps/platform/README.md`,
`README.md` (после Step 1 уже открыл active track —
дополнительно не правим), three `__main__.py`,
`_stdio_transport.py`, `_network_transport.py`,
`installer.py`. Production-код не правится.

**Результат.** Q1 / Q2 / Q3 / Q4 resolved; Step 3 contract
имеет фактическую basis. Production-код не правится.
Registries `15/25/16` без drift'а. Никаких 1cv8.exe runs.

---

## Step 3 — TLS / reverse-proxy / exposure contract (docs-only)

**Цель.** Зафиксировать exact prescriptive normative
contract для Step 4 — точные deployment-boundary rules,
exact PATH choice (A/B/C) или conditional rules, точные
allowed/forbidden Step 4 file surfaces, точный
verification protocol. Никакого code change. Никакого
1cv8.exe.

**Что меняем.** Один новый prescriptive normative document:

- `docs/architecture/track-j-deployment-boundary-contract.md`
  (новый, RFC 2119-style; MUST / MUST NOT / SHALL /
  SHOULD / MAY).

Плюс минимальные status-правки в `PROJECT-STATUS.md` под
закрытие Step 3 (новая `### Parallel Track J / Step 3 —
deployment-boundary contract (завершён)` section).

**Минимальный obligatory shape contract'а** (~12 sections):

1. **Purpose / scope.** Что contract нормирует, что не
   нормирует.
2. **Relationship to Step 1 plan and Step 2 audit.**
   Descriptive vs normative split.
3. **Inherited fixed decisions** from Step 2 audit + plan
   §5 carry-over + Track H §13 in-process-TLS-forbidden
   carry-over.
4. **Bind-host contract**: three-scenario matrix
   (loopback / private subnet / public-facing-through-
   proxy), recommended defaults, validation rules, optional
   warning behaviour decision.
5. **Reverse-proxy header contract**: explicit policy that
   `_MCPHandler` does NOT trust / consume X-Forwarded-*
   headers for authentication or authorization; auth is
   bearer-token-only.
6. **TLS termination contract**: operator's reverse proxy
   only; in-process TLS forbidden carry-over from Track H
   §13.1; `_network_transport.py` MUST NOT add `ssl`
   imports или certificate-loading code.
7. **Exposure rules contract**: explicit per-scenario
   guidance.
8. **Health / readiness endpoint contract**: either
   explicit `/healthz` endpoint shape (PATH B/C ship)
   или explicit deferral with rationale (PATH A docs-
   only).
9. **Step 4 implementation surface**: PATH A docs-only OR
   PATH B/C narrow code; exact file allowed list per
   chosen PATH; exact diff shape if PATH B/C.
10. **Step 4 forbidden surfaces**: exhaustive list of
    files that MUST NOT be touched.
11. **Verification protocol**: required positive checks +
    required negative checks + insufficient-verification
    exclusions.
12. **Honest non-goals + Step 4 handoff note**.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `SECURITY.md`, `CHANGELOG.md`,
`docs/release-handoff.md`, `apps/platform/README.md`,
`README.md`, three `__main__.py`, `_stdio_transport.py`,
`_network_transport.py`, `installer.py`. Production-код
не правится. Registries `15/25/16` без drift'а.

**Результат.** Step 3 contract на диске; Step 4
implementation имеет точные allowed / forbidden file
lists, exact PATH choice (A/B/C), exact verification
protocol.

---

## Step 4 — deployment boundary deliverable (PATH A docs-only OR PATH B/C narrow code)

**Цель.** Закрыть Track J Step 4 deliverable per Step 3
contract: либо docs-only operator-facing deployment guide
(PATH A), либо narrow code addition в
`_network_transport.py` (PATH B), либо hybrid (PATH C).
Никакого scope creep, никаких новых MCP tools, никакого
1cv8.exe. **Step 4 is the only Track J step that may
touch production code, и только если Step 3 contract
chooses PATH B/C.**

**PATH A — docs-only operationalization (default narrow
honest path):**

- Один новый `docs/runbooks/track-j-deployment.md` или
  `docs/operator-deployment-guide.md` (точное имя — Step 3
  contract):
  - reverse-proxy minimal config snippets (nginx /
    Caddy);
  - bind-host decision tree;
  - exposure-scenario matrix (loopback / private /
    public-through-proxy);
  - explicit `/healthz` deferral statement с rationale;
  - operator-facing risk-acceptance language for each
    scenario.
- Production code byte-identical через Track J.
- No `pyproject.toml` change.
- No `[project.dependencies]` / `[project.scripts]`
  change.

**PATH B — minimal code addition (only if Step 3 contract
proves it):**

- ≤ 15 LOC additive change в `packages/mcp-common/src/mcp_common/_network_transport.py`:
  - optionally bind-host warning или refusal на public
    interface без explicit override flag;
  - and/or `GET /healthz` endpoint that returns 200 plain
    text "ok\n" without auth;
  - and/or extended `--help` output mentioning reverse-
    proxy expectation.
- No new imports beyond existing stdlib (`http.server`,
  `socketserver`, `hmac`, `os`, `re`, `socket`, `sys`,
  `signal`, `email.message`, `json`, `argparse`,
  `logging`).
- `_stdio_transport.py` byte-identical;
  `mcp_common/__init__.py` `__all__` byte-identical;
  three `__main__.py` byte-identical (no SERVER_VERSION
  bump unless Step 3 contract requires).
- Optional small `docs/runbooks/track-j-deployment.md`
  pointing operator to use it.

**PATH C — hybrid:** PATH A docs + PATH B narrow code.

**Что меняем (default expected; финал — Step 3 contract).**

- PATH A: один новый docs file in `docs/runbooks/` или
  `docs/`.
- PATH B: один modified file in `packages/mcp-common/src/mcp_common/_network_transport.py`.
- PATH C: both.

Плюс Step 4 commit body MUST include verification artefact
summary per Step 3 contract verification protocol.

**Что НЕ меняем (forbidden Step 4 surfaces; финальный
список — Step 3 contract).**

- `apps/platform/src/onec_platform/*.py` — все байт-
  identical (Track I `installer.py` byte-identical;
  models.py / loader.py / bootstrap.py / etc. byte-
  identical);
- `apps/*/src/**` — все 3 MCP server packages byte-
  identical (server.py / tools.py / models.py /
  runtime/* / three `__main__.py` if PATH A; three
  `__main__.py` only if PATH B/C and only with narrow
  additive change per contract);
- `packages/*/src/**` other than maybe
  `_network_transport.py` if PATH B/C;
- `_stdio_transport.py` byte-identical;
- `mcp_common/__init__.py` `__all__` byte-identical;
- `scripts/*` byte-identical (no operator-script
  changes; Step 5 territory if needed);
- `pyproject.toml` byte-identical (Q7 = Step 6);
- `examples/*`;
- documentation за пределами the chosen PATH deliverable
  + status-only `PROJECT-STATUS.md` per-step closure
  section: `SECURITY.md`, `CHANGELOG.md`,
  `docs/release-handoff.md`, `apps/platform/README.md`,
  `README.md` (Step 5/6 territory); все Track J
  planning / audit / contract docs (frozen Step 1/2/3
  anchors); все Track A-I architecture docs (frozen
  anchors).

**Verification (минимально obligatory per Step 3
contract).**

- PATH A: документ exists; structurally complete;
  passes review of three deployment-scenario matrix +
  reverse-proxy snippet correctness;
- PATH B: code change passes verify-release.ps1 GREEN +
  selfcheck OK + smoke harness (depends on what was
  added; e.g., `/healthz` endpoint test + bind-host
  warning regression check);
- PATH C: both.
- `verify-release.ps1 -AllowDirtyTree` GREEN на 8
  checks pre-commit; `verify-release.ps1` GREEN на
  clean tree post-commit.
- Selfcheck registries `read=15 / write=25 /
  intelligence=16; status=ok`; `imports_ok=true`.
- Никаких 1cv8.exe runs.
- Никаких real credentials в commit / diff.

**Результат.** Deployment-boundary deliverable ship'ed
per Step 3 contract; existing Track G/H/I surfaces
preserved per chosen PATH constraints; registries без
drift'а.

---

## Step 5 — operator/security/release docs alignment (docs-only)

**Цель.** Точечно выровнять operator-facing / security-
facing / release-facing документацию под фактический
post-Step-4 deployment-boundary state. Docs-only;
никакого production code change; никакого pyproject.toml;
никаких registry changes; никакого 1cv8.exe.

**Что меняем (predicted scope; финальный список — Step 5
inventory).**

1. **`SECURITY.md`** — обновить «Local stdio plus narrow
   HTTP+bearer transport baseline» block с pointer на
   new operator-facing deployment guide (если PATH A/C);
   возможно update threat-model wording на explicit
   three-scenario matrix mention.
2. **`docs/release-handoff.md`** — обновить «What is in
   this handoff» (новый bullet про deployment guide если
   PATH A/C); обновить «What is NOT in this handoff»
   carry-forward; обновить «Known limitations» if
   applicable.
3. **`apps/platform/README.md`** — обновить «Hostile-
   network transport / enterprise auth / supervisor»
   item с pointer на deployment guide if applicable.
4. **`README.md`** — обновить Quickstart paragraph +
   "Что Quickstart **не** обещает" под фактический
   post-Step-4 state; «Active parallel track» section
   enumerates closed Steps 1-4 + actual deliverable.
5. **`scripts/dev/launch.ps1`** + **`scripts/dev/README.md`**
   — только если operator-facing wording реально
   drift'ует; default expectation: не trogать.
6. **`scripts/release/install.ps1`** + **`scripts/release/README.md`**
   — только если direct factual drift.

Плюс минимальные status-правки в `PROJECT-STATUS.md`
под закрытие Step 5.

**Что НЕ меняем.** Production code (`apps/*/src`,
`packages/*/src` — Step 5 docs-only by contract);
`pyproject.toml` (Q7 = Step 6 territory); registries /
new MCP tools (`read=15 / write=25 / intelligence=16`
invariant); `CHANGELOG.md` (новая `## 0.5.2 — Track J`
или `## 0.6.0 —` section — Q7 / Step 6 closure
deliverable); все Track J planning / audit / contract /
deployment-guide docs (frozen Step 1 / 2 / 3 / 4
anchors); Track A-I docs.

**Результат.** Operator-facing docs не лгут об actual
post-Step-4 deployment-boundary state. Никакой premature
Track J closure language. Никаких false claims про zero-
trust / hostile-internet ready / WAF-solved /
enterprise-ready ingress / observability solved. verify-
release.ps1 остаётся GREEN. Registries без drift'а.
Никаких 1cv8.exe runs.

---

## Step 6 — final integration pass and Track J closure

**Цель.** Закрыть весь Track J как documented status.
Read-only final integration check уже закрытых Steps 1-5,
потом минимальные closure-docs/status updates +
`pyproject.toml` version bump (Q7 resolve), потом final
closure commit. Никакого нового feature work, никаких
новых MCP tools, никакого remote push'а, никакого
1cv8.exe run.

**Pre-closure read-only check (mandatory gate).**

- working tree clean перед началом — gate PASS;
- git history линейная Step 1 → 2 → 3 → 4 → 5 → 6 (все
  commit'ы на месте; никаких accidental extra commits
  inside Track J scope);
- все Step 1–5 deliverables на диске: 3 architecture
  docs (plan + step-map + audit + contract; точное
  количество 4) + Step 4 deliverable (docs-only PATH A
  ИЛИ code change PATH B ИЛИ hybrid PATH C); Step 5
  docs alignment confirmed; existing Track G + Track H
  + Track I artefacts preserved per Step 3 contract
  constraints;
- registries `read=15 / write=25 / intelligence=16` без
  drift'а;
- `verify-release.ps1 -AllowDirtyTree` GREEN на 8
  checks с full selfcheck;
- no real credentials в diff'ах ни одного из Track J
  commit'ов;
- никаких 1cv8.exe runs ни на одном шаге Track J.

**Q7 resolve (closure decision).** Default:

- PATH A docs-only → likely PATCH (`0.5.1 → 0.5.2`),
  Track I precedent;
- PATH B narrow code → likely PATCH unless ship'нул new
  external capability (e.g. `/healthz` endpoint);
- PATH C hybrid → depends on code component scope and
  external-capability framing.

Final reasoning anchored в фактическом Step 4 functional
/ docs delta.

**Что меняем (closure-docs only; финальный scope =
symmetric с Track A-I closure pattern).**

- `pyproject.toml` — version bump per Q7 resolution.
- `README.md` — Quickstart paragraph переписан под
  «Активного трека сейчас нет — Track J закрыт десятым
  по счёту post-phase треком»; «Closed parallel tracks»
  list дополнен Track J bullet'ом (девять → десять
  закрытых треков); «Active parallel track» секция
  сжата под «нет активного трека» с pointer'ом на
  Track J detail; добавлена «Track J detail (закрыт)»
  секция полным блоком симметрично Track A/B/C/D/E/F/G/H/I
  detail (per-step bullets с commit hashes; что Track J
  реально закрыл — formalized deployment-boundary
  contract; что Track J **не делает** — explicit list:
  не zero-trust, не hostile-internet ready, не enterprise-
  ready ingress, не WAF/IDS/rate-limit, не observability,
  не auth redesign, не in-process TLS, не mTLS, не
  enterprise identity, не service supervision, не
  packaging ecosystem, не web UI, не new MCP tools, не
  1cv8 work, не standalone apps/platform; registry
  invariant).
- `PROJECT-STATUS.md` — header (`Текущий шаг` +
  `Статус`) обновлён под Track J closed + Q7 resolution
  явное упоминание + 6 commit hashes + factual Step 4
  PATH choice + closure-narrative; общий narrative-блок
  переписан под closure; добавлены пять новых per-step
  секций (Steps 2/3/4/5/6).
- `CHANGELOG.md` — добавлен новый раздел `## 0.5.2 —
  Parallel Track J — TLS and Reverse-Proxy Deployment
  Boundary` (или `## 0.6.0 —` если Q7 = MINOR) с per-
  step outcomes, actual deployment-boundary surface,
  registry invariant carried through, honest constraints
  update, Active work = None.

**Что НЕ меняем (закрытый scope).** `apps/`, `packages/`,
`scripts/`, `examples/`, `.github/`, `.editorconfig`,
`.python-version`, `.gitignore`, `LICENSE`; `SECURITY.md`,
`docs/release-handoff.md`, `apps/platform/README.md`,
`scripts/dev/*`, `scripts/release/*` (Step 5 уже
выровнял); Track J planning / audit / contract docs
(frozen Step 1 / 2 / 3 anchors); Track A-I docs;
runbooks (кроме возможно нового `docs/runbooks/track-j-
deployment.md` если PATH A/C). `1cv8.exe` не запускался
ни на одном шаге Track J.

**Результат.** Track J закрыт как documented status.
Все 11 acceptance criteria из плана §7 выполнены.
Активного трека нет; десять post-phase parallel
track'ов (A, B, C, D, E, F, G, H, I, J) закрыты
последовательно; открытие следующего трека — отдельное
operator decision. **GitHub remote push не часть
Track J — repo готов к выкладке, но пушить —
operator action.**
