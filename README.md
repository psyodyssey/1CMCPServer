# 1C Agent Platform

Проект **1C Agent Platform** — собственная MCP-платформа (Model Context Protocol) для работы
ИИ-агентов с конфигурацией и инфобазами 1С:Предприятие.

## Quickstart

> **Что это.** MCP-платформа для работы AI-агентов с конфигурацией и
> инфобазами 1С:Предприятие. На сегодня закрыты Phases 1–6 (read /
> write / metadata / intelligence / product layer / industrialization),
> Parallel Track A — full real binary-backed write path
> (DumpCfg → LoadConfigFromFiles → UpdateDBCfg), отработанный на
> reference stand'е, Parallel Track B — productization & delivery
> polish, Parallel Track C — packaging & installer delivery
> (release-facing layout, verify path, release handoff document),
> Parallel Track D — operator credentials hardening
> (env-substitution `${ENV:NAME}` path с render-time fail-closed,
> password-position redaction в `command_preview`, 8-й
> credential-template-hygiene check в `verify-release.ps1`; **не**
> enterprise security platform), и Parallel Track E —
> multi-version 1C smoke matrix scaffolding (frozen
> `frozen-smoke-v1` scenario, operator runbook, matrix-table doc
> с reference row на `8.3.27.1859`; см.
> [`docs/version-support-matrix.md`](docs/version-support-matrix.md)).
> Additional version evidence rows не добавлены — Step 4 закрыт
> через honest operator-supplied gap (на operator machine
> отсутствуют 1С minor families помимо `8.3.27`); это **не**
> «поддержка всех версий», **не** full QA program и **не**
> blanket multi-version support claim. И Parallel Track F —
> rollback whitelist expansion: `_AUTOMATIC_RECOVERY_SUPPORTED`
> расширен с 2 до 6 tools (`add_catalog_attribute`,
> `add_document_attribute` уже были; добавлены
> `add_form_attribute`, `add_form_element`,
> `append_module_method`, `replace_module_method_body`).
> Coverage broader, но **по-прежнему узкий**: 6 of 25
> mutating registry tools = 24% surface. **Не** universal
> rollback, **не** public `delete_*`, **не** multi-file
> restore, **не** AST-based semantic reverse. Tier 3
> categorical exclusions (`create_*` family,
> `apply_config_from_files`,
> `update_database_configuration`) остаются вне whitelist'а
> by design. Parallel Track G — Production-Grade MCP
> Transport and CLI: три canonical `__main__.py`
> entrypoint'а (`python -m mcp_read_server`,
> `python -m mcp_write_server`,
> `python -m mcp_intelligence_server`), minimum-viable
> stdio JSON-RPC 2.0 transport (line-delimited, stdlib-only,
> no third-party SDK), original CLI surface (`--help`,
> `--config-path`, `--transport`, `--log-level`),
> `[project.scripts]` console entries в `pyproject.toml`.
> И Parallel Track H — Network-Grade MCP Transport and
> Authentication Boundary: добавлен второй transport family
> поверх того же `list_tools()` / `get_tool(name)`
> boundary — single HTTP/1.1 `/mcp` endpoint, POST only,
> `application/json`, 1 MiB body cap, static bearer
> authentication (`Authorization: <case-insensitive-Bearer>
> <token>`, constant-time compare, fail-closed on
> missing/empty/malformed/invalid), token sources via
> `ProductConfig.auth.tokens` (`${ENV:NAME}` env-substitution
> only, literal cleartext rejected at config-load) или
> `--auth-token-env <VARNAME>` CLI flag (CLI wins, replace
> not merge); two new CLI flags `--bind <HOST>:<PORT>` и
> `--auth-token-env <VARNAME>`. Threat model = local trusted
> stdio для `--transport stdio`; trusted-network behind
> operator-owned reverse proxy для `--transport http`.
> Это **не** in-process TLS / HTTPS termination, **не**
> mTLS / client certificate auth, **не** JWT / OAuth 2.0 /
> OIDC / SAML / SCIM, **не** RBAC / ABAC / per-tool ACL /
> per-tenant isolation / multi-tenant, **не** WebSocket /
> SSE / TCP / Unix-socket / named-pipe transports, **не**
> supervisor daemon / systemd unit / Windows Service
> registration / hot reload / restart watcher, **не** web
> UI / dashboard, **не** packaging ecosystem (`.msi` /
> `.deb` / GUI installer / signed distribution / wheel
> publication beyond `[project.scripts]` declarations),
> **не** standalone `apps/platform` entrypoint, **не**
> новые MCP tools (registries `read=15 / write=25 /
> intelligence=16` invariant carried through). И
> **Parallel Track I — Installer Auth Round-Trip
> Integrity**: узкий defect-fix follow-up к Track H,
> закрывший один honest gap из Track H closure
> narrative. Step 4 ship'нул +15 LOC additive emit branch
> в `installer.py:_config_to_dict` symmetric к existing
> Phase 6 / Step 8 enterprise-block emit-only-when-
> divergent pattern; auth.tokens теперь preserved через
> install fast path round-trip byte-identical (Q6 = PATCH
> bump `0.5.0 → 0.5.1`). И **Parallel Track J — TLS
> and Reverse-Proxy Deployment Boundary** —
> intentionally docs-only deployment-boundary
> formalization track, который перевёл "trusted-network
> behind operator-owned reverse proxy" general-policy
> statement из Track H Step 3 contract §13 в
> operator-facing single-source-of-truth recipe
> ([`docs/operators/deployment-boundary.md`](docs/operators/deployment-boundary.md))
> с per-scenario MUST/SHOULD/MAY matrix для трёх
> scenarios (loopback / private subnet / public-facing-
> through-reverse-proxy), explicit Forwarded-header
> MUST-NOT-consume policy для `X-Forwarded-*` /
> `Forwarded` / `X-Real-IP` / `True-Client-IP` /
> `CF-Connecting-IP`, `/healthz` non-shipping с
> rationale, два reverse-proxy snippet'а (nginx +
> Caddy) с abstract placeholders only, восемь operator
> decision-point Q&A, honest non-goals. **Q7 = NO-BUMP**
> (Track J закрыт под existing 0.5.1, без further bump):
> production code не правился ни в одном из шести
> Track J шагов; ноль defect-class fixes; ноль new
> external capability; ноль new public API surface;
> ноль registry change. Это **не** in-process TLS /
> mTLS (carry-over Track H §13 forbid), **не**
> enterprise identity stack (SSO/OIDC/RBAC/multi-
> tenant), **не** service supervision, **не**
> packaging ecosystem, **не** web UI, **не**
> observability stack, **не** `/healthz` endpoint,
> **не** `0.0.0.0` runtime warning, **не** новые MCP
> tools, **не** registry change (registries
> `read=15 / write=25 / intelligence=16` invariant
> carried through). И **Parallel Track K — Real MCP
> Client Integration Test** — intentionally diagnostic-
> tooling-only track, который закрыл один из последних
> честных gaps проекта (отсутствие real MCP-client-
> facing end-to-end proof для already-existing
> stdio/HTTP transport surfaces). Step 3 contract
> pinned **PATH B (narrow harness)**, и Step 4
> ship'нул [`scripts/dev/mcp_client_smoke.py`](scripts/dev/mcp_client_smoke.py)
> — 341-LOC stdlib-only stand-alone harness, который
> exercise'ит `initialize` + `tools/list` +
> read-only `tools/call` round-trip по обоим
> transports (`--transport stdio` + `--transport
> http`) против `mcp-read-server` (mandatory
> closure-gate target) с дополнительным HTTP
> missing-`Authorization` probe asserting 401 +
> `WWW-Authenticate: Bearer realm="mcp"` + JSON-RPC
> `-32001`. **Q7 = NO-BUMP** (Track K закрыт под
> existing 0.5.1, без further bump): production code
> не правился ни в одном из шести Track K шагов;
> ноль defect-class fixes; harness — operator-runnable
> diagnostic file под `scripts/dev/`, симметрично
> существующему `selfcheck.py`, не consumer-visible
> runtime capability; ноль new public API surface;
> ноль registry change. Это **не** new transport
> family, **не** auth-scheme redesign, **не** new
> MCP tools, **не** packaging ecosystem, **не**
> service supervisor, **не** enterprise identity,
> **не** web UI, **не** observability stack, **не**
> 1cv8 work, **не** rollback / AST / multi-version
> expansion, **не** "client integration solved
> forever" / "all clients supported" / "production-
> ready client compatibility" / "interop fully
> proven" claim — Track K's gate exercises только
> narrow minimum scenario против одного primary
> server (`mcp-read-server`) с двумя spot-checks,
> не all-clients-supported matrix. И **Parallel
> Track L — Service Supervision and OS Service
> Registration** — intentionally docs-and-template-
> only track, который закрыл следующий честный
> эксплуатационный gap: у продукта уже были рабочие
> MCP entrypoints, HTTP/stdio transports, bearer
> auth, installer integrity, deployment-boundary
> recipe и real MCP client smoke proof, но не было
> взрослой service-supervision story. Step 3
> contract pinned **PATH B (docs + one declarative
> template)**, и Step 4 ship'нул ровно две новых
> файла под
> [`docs/operators/service/`](docs/operators/service/):
> operator-facing recipe
> [`service-supervision.md`](docs/operators/service/service-supervision.md)
> со всеми пятью lifecycle verbs (start / stop /
> restart / status / logs) end-to-end на systemd
> плюс cross-OS prose для Windows (NSSM) и macOS
> (launchd), и declarative systemd unit-file template
> [`mcp-server.service`](docs/operators/service/mcp-server.service)
> с `Type=simple`, placeholders only, RECOMMENDED
> defaults (`Restart=on-failure`, `KillSignal=SIGINT`
> чтобы route service stop в существующий
> `KeyboardInterrupt` graceful path).
> **Q7 = NO-BUMP** (Track L закрыт под existing
> 0.5.1, без further bump): production code не
> правился ни в одном из шести Track L шагов; ноль
> defect-class fixes; `runtime.py` byte-identical и
> **не** превращён в service manager; ноль new
> public API surface; ноль registry change.
> Это **не** packaging ecosystem, **не** transport /
> auth redesign, **не** deployment-boundary
> redesign (Track J §13 / §6 / §7 / §8 carry-
> forward unchanged), **не** enterprise identity
> stack, **не** clustering / HA / orchestration
> platforms, **не** web UI, **не** full
> observability stack, **не** new MCP tools, **не**
> registry change, **не** 1cv8 work, **не**
> Windows Service / launchd implementation, **не**
> in-repo daemon framework, **не** "service
> supervision solved forever" / "production-ready
> service supervision" / "all OS families
> supported" / "clustered HA" / "zero-downtime
> restart" claim — Track L's closure-gate target =
> одна OS-family implementation slice (systemd)
> плюс cross-OS prose для двух других; broader
> matrices recommended-only. И **Parallel Track M —
> Packaging Ecosystem and Distribution Boundary** —
> intentionally narrow packaging-boundary track,
> закрывший long-standing Track C / Step 3 honest
> constraint о intentionally-empty wheel build. Step 3
> contract pinned **PATH B (narrow declarative flip +
> operator recipe)**, и Step 4 ship'нул ровно два
> файла: новый operator-facing recipe под
> [`docs/operators/packaging/`](docs/operators/packaging/)
> ([`distribution-boundary.md`](docs/operators/packaging/distribution-boundary.md))
> со всеми пятью lifecycle verbs (`build` / `install`
> / `uninstall` / `upgrade` / `verify`) end-to-end +
> точное enumeration of 11-package wheel contents и
> non-contents + Windows/POSIX cross-OS posture, плюс
> narrow `pyproject.toml` wheel-build flip
> (`[tool.hatch.build.targets.wheel] packages =
> [...]` теперь содержит 11 src-layout пакетов;
> comment block указывает на recipe). Supported
> artefact class теперь — один buildable
> pure-Python wheel
> (`1c_agent_platform-<VERSION>-py3-none-any.whl`,
> `py3-none-any` platform tag, 11 src-layout packages
> + три locked `[project.scripts]` console entries +
> `dist-info/` metadata — никаких credentials,
> `.env`, real ProductConfig JSON, Track J/L recipe
> content, `docs/` / `examples/` / `scripts/`
> excluded by construction).
> **Q7 = PATCH** (`0.5.1 → 0.5.2`): Step 4 закрыл
> defect-class declared-but-non-functional surface —
> `[project.scripts]` console entries декларировались
> с Track G (`0.4.0`), но `pip install <wheel>`
> previously не работал, потому что
> `[tool.hatch.build.targets.wheel] packages = []`
> делал `python -m build` бесполезным. Step 4
> declarative flip восстанавливает functionality
> already-declared surface; Track I PATCH precedent
> applies directly (declared-but-broken → declared-
> and-working = PATCH); MINOR rejected by step-map
> invariant #15 (no new declared surface, no new CLI
> flag, no new tool); MAJOR forbidden by track scope.
> Это **не** broad packaging ecosystem (`.msi` /
> `.deb` / `.rpm` / `.dmg` / `.pkg` / `.snap` /
> `.flatpak`), **не** multi-package-manager
> publication (wheel buildable but **не** published в
> PyPI / Chocolatey / Homebrew / apt / conda-forge /
> NuGet), **не** signed-distribution chain
> (`cosign` / `sigstore` / Authenticode /
> Notarisation / SBOM / SLSA), **не** GUI installer /
> wizard, **не** transport / auth / deployment-
> boundary / service-supervision redesign, **не**
> enterprise identity, **не** clustering / HA /
> orchestration, **не** web UI, **не** full
> observability stack, **не** new MCP tools, **не**
> new CLI flag на existing servers, **не** new
> `[project.scripts]` entries (три existing entries
> locked), **не** new dependencies, **не** 1cv8
> work, **не** "packaging solved forever" / "PyPI
> release ready" / "signed binary distribution" /
> "all package managers supported" / "production-
> ready packaging" / "enterprise-ready packaging"
> claim — Track M's closure-gate covers только один
> narrow distribution-boundary slice; broader
> matrices recommended-only. И **Parallel Track N —
> Observability and Diagnostics Boundary** —
> intentionally narrow docs-only track, закрывший
> следующий честный gap: у платформы уже были рабочие
> MCP entrypoints (Track G), HTTP/stdio transports
> (G/H), bearer auth (H), installer integrity (I),
> deployment-boundary recipe (J), real MCP client
> smoke proof (K), service-supervision recipe +
> systemd template (L), и packaging/distribution
> boundary + buildable wheel (M), но не было
> first-class operator-facing observability/
> diagnostics boundary document — Track J / Track L /
> Track M каждый denying "full observability stack" в
> своём scope; никто не определял позитивно, что
> supported diagnostic surface IS. Step 3 contract
> pinned **PATH A docs-only** (PATH B selfcheck
> --json / PATH C log-shape contract slice / PATH D
> diagnostic-bundle helper все explicitly rejected с
> grounded justification), и Step 4 ship'нул ровно
> один файл —
> [`docs/operators/observability.md`](docs/operators/observability.md)
> (1043 lines): operator-facing observability/
> diagnostics recipe с supported signals
> classification (**7 first-class signals FC1–FC7** —
> stderr via Python `logging` at --log-level INFO /
> three-bucket exit codes 0/1/2 / HTTP response
> envelope с failure-equivalence на 401 / selfcheck.py
> 11-key=value output / verify-release.ps1 8-check
> gate / install fast-path findings / journalctl on
> systemd hosts; **4 recommended-only signals R1–R4**;
> **10-item out-of-scope list** carry-forward
> denials), log-level-to-event mapping (inheriting
> Track L `service-supervision.md` §9.3 verbatim),
> exit-code-meaning table (0 clean / 1 unhandled
> exception with traceback / 2 startup-time
> operator-readable failure) с file:line citations,
> HTTP response envelope summary (Track H §8.4
> failure-equivalence на 401 + non-auth failures
> 400/413/415 с -32600/-32700), triage recipe с
> **тремя mandatory canonical failure modes** (T1
> startup-code-2 / T2 universal-401 / T3 selfcheck-
> FAIL) + двумя optional (T4 smoke-FAIL / T5
> systemd-restart-loop), cross-OS posture (Linux/
> systemd/journald primary implementation-covered;
> Windows NSSM + macOS launchd + non-supervised
> execution prose-only — no fake parity), `/healthz`
> non-shipping carry-forward (quotes Track J §6
> verbatim), authoritative non-goals (9 sub-sections
> aggregating Track J §10 + Track L §9.5/§13 + Track
> M §13), operator-side verification (7 copy-
> pasteable steps), и **9 mandatory explicit denials
> of forbidden maturity claims**. **Q6 = NO-BUMP**
> (Track N закрыт под existing `0.5.2`, без further
> bump): production code не правился ни в одном из
> шести Track N шагов; ноль defect-class fixes;
> recipe documents existing signals — does **not**
> make them work; ноль new public API surface; ноль
> registry change. Track J / Track K / Track L
> NO-BUMP precedents apply directly — Track N — purest-
> form Track J analogue (pure docs-only operator-facing
> recipe; no template, no helper, no code). Это **не**
> full observability stack rollout, **не** OpenTelemetry
> program, **не** Prometheus / OpenMetrics / Grafana /
> Tempo / Loki / Jaeger platform, **не** SIEM/SOC
> integration, **не** distributed tracing, **не**
> alerting / paging / on-call program, **не**
> `/healthz` endpoint, **не** log-aggregation
> forwarder, **не** structured-logging library
> dependency, **не** transport/auth/deployment/
> service/packaging redesign, **не** новые MCP tools,
> **не** registry change, **не** 1cv8 work, **не**
> remote push, **не** "observability solved
> forever" / "production-ready observability" /
> "enterprise-ready observability" / "alerting
> solved" / "all signals covered" claim — Track N's
> closure-gate covers **только** одну integration-
> and-naming slice; broader observability matrices
> remain recommended-only. И **Parallel Track O —
> Dev-Time Editable Install and Workspace
> Discovery** — intentionally narrow docs-only
> track, закрывший следующий честный gap: после
> Track M ввёл узкий supported deploy-time wheel
> distribution boundary (`pip install <WHEEL_PATH>`),
> у проекта всё ещё не было formal **dev-time**
> boundary — нет documented `pip install -e .` flow
> для contributors editing the repo, нет supported
> workspace discovery story за пределами PowerShell-
> only `scripts/dev/bootstrap_paths.ps1`, нет cross-
> OS bootstrap parity. Gap явно acknowledged в репо:
> `scripts/dev/README.md:5-11` verbatim говорил
> "editable install и workspace discovery всё ещё
> out of scope" (теперь заменено на pointer к
> recipe в Step 5). Track O **orthogonal to Track M**:
> deploy-time wheel distribution остался в scope
> Track M; dev-time editable workflow для
> contributors — новая, отдельная axis. Step 3
> contract pinned **PATH A docs-only** (PATH B
> narrow declarative slice / PATH C dev-onboarding
> helper script все explicitly rejected с grounded
> justification), и Step 4 ship'нул ровно один
> файл —
> [`docs/dev/editable-install-and-workspace-discovery.md`](docs/dev/editable-install-and-workspace-discovery.md)
> (586 lines): contributor-facing dev-time recipe
> со всеми contract-required elements (supported
> install verbs LOCKED: **first-class
> `pip install -e .`** run from repo root in Python
> 3.11 environment, mechanically supported by
> hatchling's PEP 660 default against Track M's
> populated 11-element `[tool.hatch.build.targets.
> wheel] packages` array; **recommended-only Windows-
> only alternative** dot-source
> `scripts/dev/bootstrap_paths.ps1`; supported
> tooling preconditions Python 3.11 + pip mandatory
> with venv tool recommended; workspace-discovery
> answer naming the 11 src-layout package roots
> verbatim from `pyproject.toml:51-63` with dual-
> role explanation; verification step
> `python scripts/dev/selfcheck.py` →
> `selfcheck_status = ok` inheriting Track N FC4;
> orthogonal-and-complementary statement к Track M
> deploy-time wheel workflow; 7-sub-section
> authoritative non-goals; 6 mandatory cross-
> references; cross-OS posture Windows primary +
> POSIX served by editable install only + non-3.11
> out of scope; 8 mandatory explicit denials of
> forbidden maturity claims). **Q7 = NO-BUMP**
> (Track O закрыт под existing `0.5.2`, без further
> bump): production code не правился ни в одном из
> шести Track O шагов; recipe documents existing
> latent hatchling PEP 660 capability — does **not**
> make it work; ноль defect-class fixes; ноль new
> public API surface; ноль registry change. Track J
> / Track K / Track L / Track N NO-BUMP precedents
> apply directly — Track O is the **purest-form
> Track N analogue** (pure docs-only contributor-
> facing recipe; no template, no helper, no code).
> Это **не** containerised dev environment, **не**
> IDE-specific integration, **не** remote-dev
> workflow, **не** multi-Python-version matrix,
> **не** formatter / linter / test-runner policy
> redesign, **не** alternative build-backend
> evaluation, **не** transport / auth / deployment /
> service / packaging / observability redesign,
> **не** новые MCP tools, **не** registry change,
> **не** 1cv8 work, **не** remote push, **не**
> installable-from-git-URL story, **не** "developer
> workflow solved forever" / "all IDE integrations
> supported" / "all package managers supported for
> dev install" / "containerised dev environment
> shipped" / "remote-dev shipped" / "enterprise
> developer experience" / "production-ready DX" /
> "DX matrix complete" claim — Track O's closure-
> gate covers **только** одну narrow integration-
> and-naming slice (contributor-facing recipe
> documenting existing latent capabilities); broader
> DX matrices remain recommended-only. Пятнадцать
> post-phase parallel track'ов (A, B, C, D, E, F, G,
> H, I, J, K, L, M, N, O) полностью закрыты
> последовательно; Phase 7 как линейная фаза не
> запланирована. **Активные параллельные треки —
> Parallel Track P — Test Suite Shipping and
> Verification Boundary** (открыт первым, commit
> `d6f1936`) **и Parallel Track Q — Windows
> Installer Path and setup.exe Delivery** (открыт
> сейчас как семнадцатый post-phase parallel track),
> оба на Step 1 (planning only). Track P открыт
> после Track O closure (commit `720ac54`,
> `0.5.2`). Step 1 Track P — planning-only:
> ship'нул две новых architecture doc'и
> ([`plan`](docs/architecture/track-p-test-suite-shipping-and-verification-boundary-plan.md)
> +
> [`step-map`](docs/architecture/track-p-test-suite-shipping-and-verification-boundary-step-map.md))
> с Q1–Q7 directional defaults; никакого production
> code, `pyproject.toml`, `scripts/*`, `SECURITY.md`,
> `docs/release-handoff.md`, `apps/platform/
> README.md`, `CHANGELOG.md`, manuals, или registry
> change. Track P закрывает следующий честный gap:
> у проекта есть три working verification gates
> (`selfcheck.py` pre-flight, `verify-release.ps1`
> release-side 8-check, `mcp_client_smoke.py`
> transport-boundary smoke), но **shipped automated
> test suite** как in-repo surface отсутствует.
> `pyproject.toml:31-32` declares
> `[tool.pytest.ini_options] testpaths = ["tests"]`
> aspirationally — but the `tests/` directory does
> not exist at HEAD `720ac54`, and `scripts/dev/
> launch.ps1:28` / `:86` explicitly state "no test
> suite yet" / "It does NOT run pytest". Track P is
> the dedicated narrow track that materialises (or
> honestly re-frames) that long-standing aspirational
> declaration. Это **не** performance / load /
> stress / fuzz / browser / mutation / snapshot /
> live-1С / SaaS / multi-Python-matrix / containerised-
> CI / coverage-gate-absolutism / verification-
> philosophy-rewrite, **не** transport / auth /
> deployment / service / packaging / observability /
> dev-time-recipe redesign, **не** новые MCP tools,
> **не** registry change, **не** 1cv8 work, **не**
> remote push, **не** новые `[project.scripts]`
> entries, **не** новые runtime dependencies, **не**
> "testing solved forever" / "full QA stack shipped"
> / "complete confidence matrix" / "production-grade
> certification" / "enterprise test infrastructure"
> / "100% coverage achieved" / "all behaviours
> covered" claim. Tracks A–O closed state carried
> byte-identical. Открытие следующих Track P шагов
> (Step 2 baseline audit / Step 3 normative contract
> / Step 4 narrow implementation / Step 5 docs
> alignment / Step 6 closure) — отдельное operator
> decision. Registries `read=15 / write=25 /
> intelligence=16` invariant carried through.
>
> **Parallel Track Q — Windows Installer Path and
> setup.exe Delivery** открыт как семнадцатый
> post-phase parallel track, тоже на Step 1
> (planning only). Track Q закрывает **другой**
> честный gap: у проекта есть wheel/pip
> distribution boundary (Track M:
> `1c_agent_platform-0.5.2-py3-none-any.whl`,
> `pip install <WHEEL_PATH>`) и install fast-path
> PowerShell wrapper (Track B / Track I:
> `scripts/release/install.ps1`) — но оба
> presuppose, что на машине **уже стоит** Python
> 3.11 + pip (+ для git-based flow — Git).
> **Обычный Windows-пользователь** этого не имеет.
> Сегодня нет ни одного surface, который позволяет
> такому пользователю: скачать `setup.exe` →
> двойной клик → **Next** / **Install** / **Finish**
> → программа установлена. Никакого `setup.exe`,
> никакого installer-technology definition file
> (`.iss` / `.wxs` / `.nsi`), никакого bundled
> Python runtime artefact в репо нет. Anchors,
> которые этот gap прямо acknowledge:
> `scripts/release/install.ps1:1-11` ("No `.msi`,
> no `.deb`, no GUI wizard, no signed
> distribution"),
> `docs/operators/packaging/distribution-boundary.md`
> §7 non-goals ("no GUI installer"),
> `pyproject.toml` Track M comment block ("no GUI
> installer", "no Chocolatey / Homebrew / apt /
> conda-forge / NuGet"). Track Q — dedicated
> **narrow** track, который закрывает именно эту
> боль: один Windows `setup.exe`, ordinary-user
> install experience без preinstalled Python /
> pip / Git, uninstall через стандартный Windows
> Add/Remove Programs surface. Step 1 — planning-
> only: ship'нул две новых architecture doc'и
> ([`plan`](docs/architecture/track-q-windows-installer-path-and-setup-exe-delivery-plan.md),
> [`step-map`](docs/architecture/track-q-windows-installer-path-and-setup-exe-delivery-step-map.md))
> с Q1–Q7 directional defaults. **Центральная
> честная константа Track Q** (плана §4): платформа
> — pure-Python codebase; "install без preinstalled
> Python" структурно требует **bundled Python
> runtime** внутри installer'а (default
> expectation — python.org embeddable CPython 3.11
> distribution, ~10 MB, pulled at build time, **не
> committed as binary в git**). Без bundled runtime
> честного setup.exe path не существует — это
> называется прямо, не в сноске. Expected
> installed footprint — около 10–15 MB. Это **не**
> Linux installer / macOS installer / широкая
> `.msi`/`.deb`/`.rpm`/`.dmg`/`.pkg`/`.snap`/`.flatpak`
> ecosystem / PyPI publication / package-manager
> matrix (Chocolatey / winget / Scoop / NuGet) /
> code signing / Authenticode / EV cert /
> notarization / SBOM / SLSA / auto-update / OTA /
> GUI dashboard / browser UI / service supervision
> redesign / auth redesign / transport redesign /
> new MCP tools / new CLI flags / new
> `[project.scripts]` entries / new runtime
> dependencies / remote-dev / IDE integration /
> enterprise installer platform / MDM /
> containerisation / cluster-HA / "all Windows
> distributions supported" / "one-click everything
> solved forever" / "enterprise-grade installer" /
> "production-ready desktop app" / "GUI config
> wizard" / "Windows service auto-magic by default"
> claim. Default installer technology — Inno Setup
> (baseline; Step 3 contract — lock point;
> directional, не finalised). Default Step 4 PATH
> — PATH B (operator recipe + один `.iss` Inno
> Setup script + опционально один PowerShell build-
> helper), PATH A docs-only в резерве; PATH
> explicitly **не locked** на Step 1. Q7 SemVer —
> directional framing only: NO-BUMP под PATH A,
> PATCH defensible под PATH B как defect-class
> delivery-channel repair (mirror Track I / Track M
> precedent), MINOR defensible под PATH B как new
> operator-visible delivery channel (mirror Track H
> precedent); lock на Step 6. Tracks A–O closed
> state и Track P / Step 1 planning surface
> сохраняются byte-identical. Открытие следующих
> Track Q шагов — отдельное operator decision.
> Registries `read=15 / write=25 / intelligence=16`
> invariant carried through.

### Системные требования

- Windows + PowerShell 5.1 / 7+ (текущие entrypoints — PowerShell-скрипты);
- Python 3.11 (см. `.python-version`);
- (опционально) `1cv8.exe` — нужен только для real binary-backed
  write path; без него работают read-only / synthetic режимы.

### Install — материализовать product config

```powershell
.\scripts\release\install.ps1 `
    -ConfigPath examples\demo-infobase\infobase6.config.json `
    -OutputConfigPath C:\path\to\target\product.config.json
```

По умолчанию запускается в **preview** режиме (ничего не пишется на
диск). Чтобы реально записать config — добавьте `-Confirm`. Подробности
параметров и exit-кодов: [`scripts/release/README.md`](scripts/release/README.md).

### Check — local selfcheck

```powershell
.\scripts\dev\launch.ps1 selfcheck
```

Печатает компактный отчёт с registry counts (`read=15 / write=25 /
intelligence=16`), `imports_ok=true`, `selfcheck_status=ok`.
Эквивалент [`scripts/dev/run_dev_check.ps1`](scripts/dev/run_dev_check.ps1)
(используется в `.github/workflows/dev-check.yml`).

### Local dev launch — operator / dev umbrella

```powershell
.\scripts\dev\launch.ps1 help                 # usage
.\scripts\dev\launch.ps1 selfcheck            # см. выше
.\scripts\dev\launch.ps1 repl                 # interactive Python с PYTHONPATH
.\scripts\dev\launch.ps1 run <script.py> ...  # ad-hoc Python script
```

Подробности и список того, что `launch.ps1` сознательно **не**
делает (не стартует MCP-серверы, не запускает pytest, не дублирует
install fast path, не трогает инфобазу): [`scripts/dev/README.md`](scripts/dev/README.md).

### Куда идти дальше

- [`docs/release-handoff.md`](docs/release-handoff.md) —
  release handoff для receive-side оператора: что вы получили,
  prerequisites, reproducible install sequence, verify sequence,
  known limitations.
- [`apps/platform/README.md`](apps/platform/README.md) — product
  layer: bootstrap, runtime, dashboard, guided workflows, rollback
  assistant, real-stand smoke, enterprise foundation inspector.
- [`docs/operator-manual.md`](docs/operator-manual.md) —
  operator-facing reference.
- [`docs/runbooks/`](docs/runbooks/) — воспроизводимые сценарии,
  включая `track-a-reference-stand-round-trip.md` (real binary-backed
  round-trip) и `track-e-multi-version-smoke-matrix.md` (operator
  runbook для `frozen-smoke-v1` на operator-supplied 1С версиях).
- [`docs/version-support-matrix.md`](docs/version-support-matrix.md) —
  evidence table с frozen 12-column shape (Track E); single source
  of truth для актуального уровня multi-version evidence — **не**
  blanket support claim.
- [`docs/architecture/`](docs/architecture/) — phase- и track-plans
  + step maps (включая Track B, Track C, Track D и Track E
  planning).
- [`PROJECT-STATUS.md`](PROJECT-STATUS.md) — детальный статус фаз
  и треков с per-step deliverables.

### Что Quickstart **не** обещает

Этот entry — про **локальный** install и check. Track G / Step 4
ship'нул узкий local stdio MCP transport baseline (три
`python -m <server>` entrypoint'а + minimum-viable JSON-RPC 2.0
stdio loop). Track H / Step 4 добавил **второй transport family**
поверх того же registry boundary: single HTTP/1.1 `/mcp` endpoint
с static bearer authentication (case-insensitive scheme,
constant-time compare, fail-closed on missing/invalid token,
required-when-`--transport http` startup gate), плюс два новых
CLI флага (`--bind <HOST>:<PORT>` + `--auth-token-env <VARNAME>`).
Этот совокупный baseline (stdio + narrow HTTP+bearer) — **не**
in-process TLS / HTTPS termination (operator's reverse proxy
ответственен за TLS termination перед HTTP listener'ом), **не**
mTLS / client certificate authentication, **не** JWT / OAuth 2.0
/ OIDC / SAML / SCIM (token introspection / refresh / rotation
endpoints из этого набора тоже out-of-scope), **не** RBAC / ABAC
/ per-tool ACL / multi-tenant isolation, **не** WebSocket / SSE /
TCP / Unix-socket / named-pipe transports, **не** session cookies
/ rate limiting, **не** installer ecosystem (`.msi` / `.deb` /
GUI wizard / signed binary distribution / wheel publication — wheel
теперь buildable через Track M, но **не** published в PyPI / Chocolatey
/ Homebrew / apt / conda-forge / NuGet; supported boundary документирован
в [`docs/operators/packaging/distribution-boundary.md`](docs/operators/packaging/distribution-boundary.md)),
**не** web UI / dashboard frontend,
**не** enterprise-ready deployment (SSO/RBAC, multi-tenant,
secrets vault, federated audit storage, multi-instance HA), **не**
hot reload / OS-level service supervision (systemd unit / Windows
Service / automatic restart watcher), **не** standalone
`apps/platform` entrypoint. Threat model HTTP transport — **trusted-
network deployment** behind operator-owned reverse proxy; не
hostile-internet zero-trust posture. Эти направления — out of
scope активных треков; см. honest constraints в
[`SECURITY.md`](SECURITY.md), [`CHANGELOG.md`](CHANGELOG.md) и
[`docs/architecture/`](docs/architecture/).

## Идея

Платформа строится как единая система, через которую ИИ-агенты (Claude Code и другие)
в перспективе смогут безопасно и структурированно:

- читать конфигурацию и метаданные 1С;
- изменять объекты конфигурации и данные инфобазы;
- анализировать поведение системы, журналы и состояние;
- решать прикладные задачи разработчика и аналитика 1С.

Эти возможности — целевое направление развития платформы, а не уже реализованная
функциональность: на текущем этапе создан только каркас проекта.

## Архитектура

Платформа делится на три изолированных MCP-сервера и продуктовый слой
поверх них:

- **mcp-read-server** — чтение конфигурации, метаданных, данных, журналов (только чтение).
- **mcp-write-server** — изменение конфигурации, объектов, кода, миграций (операции записи).
- **mcp-intelligence-server** — аналитика, диагностика, подсказки, troubleshooting.
- **platform** (`apps/platform/`, пакет `onec_platform`) — продуктовый
  слой Phase 5: product-config, prereqs doctor, bootstrap entrypoint.
  Не MCP-сервер; обвязка над тремя серверами выше.

Разделение на read / write / intelligence позволяет гибко управлять правами,
безопасностью и политиками применения операций. Продуктовый слой не
размывает эти границы — он только собирает их в продуктовую
поверхность.

## Текущий статус по фазам

- **Phase 0** — инфраструктурная база завершена.
- **Phase 1** — Read MVP завершён. `mcp-read-server` содержит 15
  инструментов чтения (configuration, metadata, dump/code,
  query path, event log, diagnostics).
- **Phase 2** — Write MVP завершён. `mcp-write-server` содержит 15
  инструментов: группа A (preflight/snapshot), группа B
  (controlled write через единый `run_write_flow`), группа C
  (verification), группа D (audit / rollback hint). Остаются
  временные stub'ы поверх `onec-process-runner` для apply /
  update-db / dump snapshot — до появления пути к `1cv8` в
  `onec-config`.
- **Phase 3** — Metadata Changes завершён. `mcp-write-server`
  содержит 23 инструмента: object/attribute level
  (`create_catalog`, `add_catalog_attribute`,
  `add_document_attribute`, `create_common_module`),
  form/module level (`create_managed_form`, `add_form_element`,
  `append_module_method`, `replace_module_method_body` с
  обязательным `confirm_replace=True`), metadata shape verification
  (`verify_attribute_exists`, расширенный `verify_metadata_change`
  с `kind ∈ {object_exists, module_contains, attribute_exists,
  form_exists, method_exists}`, `diff_dump_fragment`) — плюс
  сохранившиеся группы A (preflight/snapshot) и D (audit/rollback
  hint). Mutating metadata-tools строго идут через единый
  `run_write_flow(...)`; real-`1cv8` binary integration остаётся
  parallel follow-up.
- **Phase 4** — Intelligence Layer завершён. `mcp-intelligence-server`
  содержит 16 **read-only** public tool'ов в четырёх группах:
  group A (dependency / reference analysis —
  `find_references_to_object`, `find_module_method_usages`,
  `analyze_object_dependencies`); group B (impact / affected scope —
  `estimate_change_impact`, `find_affected_forms`,
  `find_affected_modules`, `suggest_safe_change_order`); group C
  (diagnostics / troubleshooting — `analyze_runtime_issue`,
  `analyze_event_log_patterns`, `diagnose_broken_form_binding`,
  `diagnose_missing_method_or_attribute`); group D (recommendations
  / planning — `suggest_fix_for_issue`,
  `suggest_metadata_patch_plan`, `summarize_configuration_risk`,
  `prepare_intelligence_report`). Контракт: intelligence-server
  никогда не пишет, не идёт через `run_write_flow`, не пишет audit
  и не импортирует `onec_policy_engine`. Read- и write-серверы на
  Phase 4 не деградировали (15 и 23 tool'а соответственно).
  Step 7 — final integration pass — пройден.
- **Phase 5** — Product Layer **завершён** на Step 8 final
  integration pass. Цель — **Product Layer**: переход от
  набора серверов и tool'ов к цельному продуктовому
  контуру, который можно установить, поднять, подключить
  к 1С, безопасно использовать, сопровождать, откатывать,
  диагностировать. Это **не** означает, что продукт уже
  достиг финального industrial-grade / enterprise-ready
  состояния — крупные хвосты честно перечислены в
  `PROJECT-STATUS.md` (полное замещение Phase 2 stub'ов
  реальным 1cv8-backed write path, multi-step real-stand
  smoke, public `delete_*` write-tools, hot reload,
  production MCP transport, web-UI, full enterprise
  hardening и т.п.). Phase 5 закрывает именно
  product-layer контур поверх существующих read/write/
  intelligence-серверов. Phase 5 строится **поверх** уже готовых
  read/write/intelligence слоёв и **не** добавляет новые MCP
  tool'ы ради расширения tool surface. Шесть продуктовых
  блоков: installation/bootstrap, runtime orchestration,
  guided workflows, rollback/recovery/audit UX, real-stand /
  1cv8 binary integration track, operator/admin/developer
  docs. Safety guarantees Phase 2–4 (никакого silent prod
  write, обязательные snapshots, обязательный verify,
  обязательный audit, read-only intelligence) сохраняются и
  на product-уровне не размываются. После Phase 5 / Step 3
  у продуктового слоя `apps/platform/` (пакет
  `onec_platform`) есть и **bootstrap contract** Step 2
  (product-config schema + JSON loader, prereqs doctor,
  bootstrap entrypoint), и **runtime orchestration
  contract** Step 3: декларативные argv-команды на сервис
  в `runtime.services`, единые boundary-функции
  `start_product_runtime` / `stop_product_runtime` /
  `get_product_runtime_status` / `reload_product_runtime`,
  атомарный state-файл под `<work_dir>/.runtime/runtime-state.json`,
  cross-platform проверка PID-liveness на чистом stdlib.
  Это **не** означает, что у read/write/intelligence
  серверов уже есть production-grade MCP transport — Step 3
  даёт **product-level launcher contract** над тем, что
  оператор объявил, а не подменяет собой будущую
  серверную transport-обвязку. `reload` сейчас — это
  controlled stop-then-start, не hot reload. После
  Phase 5 / Step 4 у продуктового слоя есть и
  **environment doctor / health dashboard**: единая
  read-only функция `build_environment_dashboard(...)`,
  агрегирующая в один снимок секции `bootstrap` +
  `runtime` + `read_health` + `read_diagnosis` +
  `intelligence_runtime` + `intelligence_risk` поверх уже
  существующих read- и intelligence-tool'ов. Dashboard
  выдаёт rule-based вердикт `healthy` / `degraded` /
  `blocked` и флаг `ready_for_workflows`, который Step 5
  guided workflows используют как pre-condition.
  После Phase 5 / Step 5 у продуктового слоя есть и
  **guided workflow layer**: единая boundary-функция
  `run_guided_workflow(...)` поверх трёх готовых сценариев
  — `safe-add-attribute` (через
  `add_catalog_attribute` / `add_document_attribute` +
  `verify_attribute_exists`), `safe-add-module-method`
  (через `append_module_method` + `verify_module_contains`)
  и `stand-health-check` (read-only diagnostic). Каждый
  mutating workflow строит план через intelligence
  (`estimate_change_impact`, `suggest_safe_change_order`,
  `suggest_metadata_patch_plan`), показывает оператору и
  **не исполняется без `confirm_execute=True`**;
  фактическое mutating-исполнение идёт через существующие
  public write-tool'ы, которые сами проходят через
  `run_write_flow` (preflight → snapshot → operation →
  verify → audit). Никакого silent apply, никакого
  обхода audit/snapshots. После Phase 5 / Step 6 у
  продуктового слоя есть и **rollback / recovery / audit
  UX**: три read-only boundary-функции
  (`get_operation_history`, `inspect_operation`,
  `run_rollback_assistant`), которые работают над уже
  существующим audit JSONL и `prepare_rollback_hint`
  / `describe_last_write_operation`. Assistant строит
  preview всегда (даже на degraded окружении); на
  `confirm_execute=True` он либо `mode=blocked` (если
  dashboard не ready), либо `mode=unsupported` (если для
  этого write-tool family нет supported automatic recovery
  path). На Step 6 supported automatic recovery whitelist
  пуст: автоматический content-level rollback не
  ship'ится без публичных `delete_*` write-tool'ов —
  product layer не делает back-door write channel в
  dump. Operator получает honest operator summary +
  snapshot paths и решает сам. После Phase 5 / Step 7
  у продуктового слоя есть и **real-stand / 1cv8
  binary integration track**: новый optional contract
  в `onec-config` (`onec_binary_path` /
  `onec_binary_probe_args`), две boundary-функции
  (`get_real_stand_readiness`, `run_real_stand_smoke_test`),
  reference stand spec в README продуктового слоя, и
  **настоящий** controlled smoke test: на
  `confirm_execute=True` с готовым окружением platform
  стартует реальный subprocess через `onec_process_runner`
  с operator-declared argv (cap timeout 30s, output
  excerpts обрезаны до 1024 chars). Phase 2 stub'ы
  (`create_dump_snapshot` / `apply_config_from_files` /
  `update_database_configuration`) на Step 7 **не**
  переписываются — это параллельный track. Никаких новых
  MCP tool'ов; никакого back-door write channel в
  infobase; никакого 1cv8-CLI guessing — оператор
  владеет probe args. **Step 8** — final integration
  pass — пройден без правок кода: один сквозной
  Scenario A через bootstrap → runtime → dashboard →
  guided workflow → recovery UX → real-stand smoke
  отработал out-of-the-box на synthetic-окружении
  (реальный стенд не трогался). Failure paths —
  workflow blocked by dashboard, rollback assistant
  unsupported, broken JSON config, malformed audit
  line — все деградировали честно без единого
  исключения наружу. Registry'ы read=15 / write=23 /
  intelligence=16 не менялись; `onec_policy_engine` не
  импортируется ни в product layer, ни в
  intelligence-server. **Phase 5 закрыт**.
- **Phase 6** — **закрыта на Step 9 — final integration pass**.
  **Industrialization & Completion Track**: специально
  выделенная фаза доведения продукта до finished /
  deployable состояния. После **Step 2** у платформы
  есть первый честный binary-backed slice:
  `create_dump_snapshot` теперь имеет два режима —
  classic **stub** (backward-compat default) и
  **binary-backed** (включается, когда оператор задал
  оба поля `EnvironmentConfig.onec_binary_path` +
  `EnvironmentConfig.onec_dumpcfg_command_template`).
  Платформа **не угадывает** 1cv8 CLI grammar:
  оператор пишет полный argv-template с whitelisted
  placeholder'ами (`{binary_path}` / `{output_path}` /
  `{base_path}` / `{base_id}` / `{publication_name}` /
  `{http_base_url}`); render — безопасный
  `str.format_map` с fail-closed на unknown
  placeholder; subprocess идёт через
  `onec_process_runner` с timeout 300 s; captured
  output обрезан до 1024 chars; runtime failure
  binary-backed subprocess'а **не** падает в silent
  fallback на stub — только config-time развилка.
  Phase 2 stub'ы `apply_config_from_files` и
  `update_database_configuration` на Step 2 **не**
  тронуты — это первый partial slice
  Industrialization Track, не полная замена. После
  **Step 3** в `apps/platform/onec_platform` появился
  install / setup fast path: read-only
  `inspect_release_layout`, declarative
  `build_product_config_template`, и главный boundary
  `run_install_fast_path(data, *, output_config_path,
  confirm_write)` с двумя режимами (preview / executed)
  и одним fail-closed (`rejected`). Helper материализует
  JSON product-config атомарно (`*.tmp` + `os.replace`),
  отказывается перезаписывать существующий файл, и
  после записи делает round-trip
  `bootstrap_product_from_json_file` для подтверждения
  читаемости. Это **не** GUI installer и **не** release
  packaging ecosystem — это product-layer fast path,
  который сокращает manual install ritual до ≤ 5
  ручных шагов; helper не запускает MCP-серверы, не
  модифицирует инфобазу, не вызывает write-tool'ы.
  После **Step 4** платформа получила первый
  **исполняемый rollback path**: `_AUTOMATIC_RECOVERY_SUPPORTED`
  переехал из пустого frozenset'а в whitelist из ровно двух
  tool'ов — `add_catalog_attribute` и `add_document_attribute`,
  то есть объектов, чьё содержание полностью описывается одним
  XML-файлом и обратимо ровно копированием snapshot-копии этого
  файла. Чтобы это сделать честно, в audit запись добавлен
  optional `details` dict (`operation_name`, `rollback_supported`,
  `backup_snapshot_path`, `dump_snapshot_path`, `relative_path`);
  pre-Step-4 строки **байт-идентичны** (`details=None` явно
  вырезается из JSON). В write-server registry добавлен ровно
  один новый mutating tool —
  **`restore_dump_file_from_snapshot(environment, relative_path,
  snapshot_file_path, label)`** — single-file restore, отвергающий
  абсолютные пути и `..` сегменты fail-closed, идущий через тот
  же `run_write_flow` (preflight + snapshot + operation + verify
  + audit), что и forward write. Recovery-ассистент в
  product-layer'е (`run_rollback_assistant`) на
  `confirm_execute=True` для whitelisted tool'а с healthy
  dashboard'ом теперь возвращает `mode='executed'` и
  ответственно вызывает этот public write-tool — никаких
  back-door filesystem write'ов из продуктового слоя по-прежнему
  нет; rollback наследует policy / preflight / snapshot / verify /
  audit дисциплину «настоящего» write'а. Сразу после рестора
  ассистент делает обязательный post-rollback verify через
  существующий read-only `diff_dump_fragment` и считает успехом
  только сочетание `restore.ok=True` AND
  `diff.data.changed=False`. Whitelist умышленно остался узким:
  расширять его — отдельные шаги Phase 6, не Step 4. Registry'ы
  read=15 / write=**24** (был 23) / intelligence=16; Phase 4
  intelligence-server остаётся read-only по конструкции.
  После **Step 5** платформа получила первый честный
  **structural XML edit slice**: добавлен один новый public
  mutating tool **`add_form_attribute(environment, object_name,
  form_name, attribute_spec, label)`**, идущий строго через
  `run_write_flow` и редактирующий XML-карту через
  `xml.etree.ElementTree`, а не через substring/`rfind`
  патчинг. В internal helper layer
  (`runtime/metadata_ops.py`) появились шесть DOM-style
  helper'ов на stdlib (`parse_xml_file`, `write_xml_file`,
  `find_form_element`, `get_or_create_form_attributes_block`,
  `add_attribute_to_form_attributes_block`,
  `form_has_attribute`); если у формы ещё нет блока
  `<Attributes>`, tool создаёт его structurally, а не падает
  и не делает rfind-fallback'а. Существующий public
  dispatcher `verify_metadata_change(...)` получил одну
  новую read-only ветку `kind="form_attribute_exists"` —
  без нового standalone verify-tool'а, чтобы public surface
  оставалась узкой. `add_catalog_attribute` /
  `add_document_attribute` намеренно **не** переписаны на
  DOM-edit на этом шаге — Step 5 ship'ит structural edit
  точечно, не sweep'ом. Registry'ы read=15 / write=**25**
  (был 24) / intelligence=16. После **Step 6** платформа
  получила первый честный slice **runtime hardening**
  поверх existing Phase 5 / Step 3 runtime contract:
  каждый long-lived product service теперь логирует
  `stdout` / `stderr` в файлы под
  `<work_dir>/.runtime/logs/<service>.{out,err}.log`
  (вместо старого безусловного `DEVNULL`); добавлена
  rotate-if-exceeds-size в одно поколение (`.1`-файл) с
  настраиваемым `log_max_bytes` (default 1 MiB);
  введена узкая `restart_policy ∈ {"never",
  "restart-if-stale"}` (default `"never"`), причём
  `"restart-if-stale"` срабатывает **только** на
  boundary-вызовах `start` / `reload` / `status` — нет
  никакого фонового watcher'а, нет timer-loop'а, нет
  daemon-supervisor'а; persisted `runtime-state.json`
  расширен (schema bumped 1 → 2) полями
  `restart_policy` / `restart_attempts` /
  `last_exit_code` / `stdout_log_path` /
  `stderr_log_path` / `last_started_at` /
  `last_stopped_at`, при этом reader honestly
  читает schema=1 файлы с дефолтами; новые findings
  `runtime_log_paths:<svc>` /
  `runtime_log_rotated:<svc>` /
  `runtime_log_dir_failed:<svc>` /
  `runtime_restart_attempted:<svc>` /
  `runtime_restart_succeeded:<svc>` /
  `runtime_restart_failed:<svc>` поднимают
  происходящее в operator-readable форму. Никаких
  новых MCP tool'ов: registry'ы read=15 / write=25 /
  intelligence=16 не изменены. Это **не** Windows
  Service / systemd integration, **не** hot reload,
  **не** journald / log aggregation — большие куски
  явно вынесены за пределы Phase 6. **Step 7** прошёл
  как **documentation-only**: одно сквозное
  Scenario A (bootstrap → install fast path → start →
  status → dashboard → safe-add-attribute mutating
  workflow → history → inspect → executed rollback →
  post-rollback verify → readiness → smoke → stop) +
  пять honest failure paths (workflow blocked,
  rollback unsupported, broken JSON, malformed audit
  lines, smoke non-zero exit) **прошли без единой
  кодовой правки** на synthetic стенде. Кnowledge,
  которое ранее распухало по READMEам, вынесено в
  четыре standalone-документа: `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md`.
  Registry-инвариант сохранён ровно: read=15 /
  write=25 / intelligence=16. После **Step 8**
  платформа получила узкий **enterprise foundation
  slice**: добавлена одна optional product-config
  секция `enterprise` (`deployment_tier ∈
  {"dev","test","stage","prod-like"}`, `instance_id`,
  `config_owner`, `change_control_required`,
  `require_operator_identity`, `runbook_reference`)
  и один новый read-only product-layer boundary
  `inspect_enterprise_foundation(...)` /
  `inspect_enterprise_foundation_from_json_file(...)`,
  который детерминистически проверяет четыре секции
  (identity, operability, traceability, binary
  contract) и возвращает `foundation_level ∈
  {"absent","minimal","partial","strong"}` плюс
  отдельный `ready_for_enterprise_track: bool`. Это
  **foundation verdict**, не enterprise-readiness
  verdict — платформа отвечает за «есть ли опора под
  следующий enterprise шаг», не за «можно ли это
  везти в prod». Step 1–7 конфиги без секции
  продолжают грузиться; loader строго валидирует
  shape; `build_product_config_template(...)` принял
  шесть новых optional kwargs и эмитит
  enterprise-блок ровно когда хотя бы один из них
  передан. Никаких новых MCP tool'ов: registry'ы
  read=15 / write=25 / intelligence=16 не изменены.
  Это **не** SSO/RBAC, **не** multi-tenant, **не**
  secrets vault, **не** policy-as-code, **не**
  federated audit storage — всё это явно вынесено за
  Phase 6 в parallel enterprise track. **Step 9** —
  final integration pass Phase 6 — пройден: один
  связный Scenario A (16 шагов от bootstrap до stop,
  через каждый Phase 6 slice по очереди — install
  fast path, runtime layer с реальным subprocess,
  dashboard, два mutating workflow'а через
  `run_write_flow` с **подтверждённой binary-backed**
  `create_dump_snapshot` (snapshot-директория
  физически содержит скопированный
  `Catalogs/SampleCatalog.xml`, доказательство, что
  это именно binary-backed mode, а не stub),
  history → inspect → executed rollback на
  whitelisted op'е → структурный post-rollback
  verify через ElementTree + byte-equal с pre-add
  baseline'ом, real-stand smoke с реальным
  subprocess'ом, enterprise-foundation inspection
  (`foundation_level='strong',
  ready_for_enterprise_track=True`), stop runtime с
  реально умирающим PID'ом, проверка наличия
  `<work_dir>/.runtime/logs/<svc>.{out,err}.log` на
  диске). Шесть honest failure paths (workflow
  blocked, rollback unsupported для
  `add_form_attribute`, broken JSON через девять
  `_from_json_file` boundary'ев включая Step 8
  enterprise-foundation entry, smoke с реальным
  non-zero exit, enterprise foundation weak/minimal
  на prod-like без identity / binary contract,
  binary-backed dump snapshot с non-zero subprocess
  exit'ом без silent stub fallback'а). Discipline
  asserts: registries pre/post `read=15 / write=25 /
  intelligence=16` без drift'а; 0 import'ов
  `onec_policy_engine` под `apps/platform/src` и
  `apps/mcp-intelligence-server/src`; 14
  suggested-tool / suggested-write-tool lists, все
  имена реальные; ни одно boundary не raise'нуло
  наружу. Кодовых правок на Step 9 — **две
  минимальные**: добавлен один тонкий guided-wrapper
  `safe-add-form-attribute` (Step 5 shipped public
  `add_form_attribute` без guided-обёртки, без неё
  brief'овский «`run_guided_workflow` →
  `add_form_attribute`» был структурно невозможен)
  + закрыт реальный gap в
  `installer._config_to_dict`, который silently
  dropped Step 6 service-level поля и Step 8
  enterprise-блок при install fast path round-trip'е.
  Никаких новых MCP tool'ов; registries нетронуты.
  **Phase 6 закрыта.** Следующий шаг — это уже
  parallel / enterprise tracks ПОСЛЕ Phase 6 (см.
  список ниже); Phase 7 не начинается. Это **не**
  очередное расширение MCP tool surface — после
  Phase 1–5 ядро
  и product-layer контур уже есть; Phase 6 закрывает
  разрыв между «у нас сильное ядро + работающий
  product-layer контур» и «это можно установить,
  запустить, использовать, поддерживать и передать
  другому человеку как реальный индустриальный
  продукт». Шесть продуктовых блоков: real 1cv8
  binary-backed execution (точечно, для одного Phase 2
  stub-backed пути; остальные остаются follow-up'ом),
  full rollback / recovery (исполнимый хотя бы для
  одного класса), installer / packaging / setup
  short path (≤ 5 ручных шагов), metadata completion
  + первый шаг к structural editing, runtime
  hardening (логи, restart policy), operator / admin
  / developer manuals + runbooks как standalone
  docs, foundation для enterprise-трека (без полной
  enterprise-вселенной). Safety guarantees Phase 2–5
  сохраняются: `run_write_flow` остаётся единственным
  путём к mutating операциям; intelligence остаётся
  read-only; `onec_policy_engine` не импортируется;
  никакого back-door write channel в product layer.
  Закрытие Phase 6 не означает, что продукт стал
  полностью enterprise-ready — крупные хвосты
  (полная enterprise-поверхность, AST-парсер всей
  кодовой базы, web-UI, multi-instance HA, полный
  version-matrix smoke на всех 1С версиях) явно
  выносятся за пределы фазы.

Закрытые фазы:

- `docs/architecture/phase-0-summary.md` — итоги Phase 0.
- `docs/architecture/phase-1-entry.md`,
  `docs/architecture/phase-1-read-mvp-plan.md`,
  `docs/architecture/phase-1-step-map.md` — материалы Phase 1.
- `docs/architecture/phase-2-write-mvp-plan.md`,
  `docs/architecture/phase-2-step-map.md` — материалы Phase 2.
- `docs/architecture/phase-3-metadata-changes-plan.md`,
  `docs/architecture/phase-3-step-map.md` — материалы Phase 3.
- `docs/architecture/phase-4-intelligence-plan.md` — план
  Phase 4: стартовый набор intelligence-инструментов по группам
  A/B/C/D, guardrails, критерии приёмки.
- `docs/architecture/phase-4-step-map.md` — implementation map
  (7 шагов). Phase 4 закрыта на Step 7.
- `docs/architecture/phase-5-product-layer-plan.md` — план
  Phase 5: назначение, целевой результат, шесть продуктовых
  блоков (A–F), 16+ продуктовых capability'ов, guardrails,
  критерии приёмки, явный список того, что **не** входит в
  фазу.
- `docs/architecture/phase-5-step-map.md` — implementation
  map (8 шагов): product contract → installer → runner →
  doctor → workflows → rollback/recovery → real-stand →
  final integration pass. Phase 5 закрыта на Step 8.
- `docs/architecture/phase-6-industrialization-plan.md` —
  план **Phase 6 — Industrialization & Completion Track**:
  узкий honest set из шести продуктовых блоков
  (A real 1cv8 execution; B full rollback / recovery;
  C installer / packaging; D metadata completion /
  structural editing; E runtime hardening;
  F operator UX / docs / runbooks; G enterprise
  foundation). 10 проверяемых критериев приёмки. Явный
  «что НЕ входит в фазу». Phase 6 закрыта на Step 9
  (final integration pass) — see `apps/platform/README.md`
  раздел «Phase 6 закрыта» для подробного списка того,
  что закрыто честно, и того, что осталось как parallel
  / enterprise tracks после Phase 6.

Активных фаз нет. Следующие шаги — parallel / enterprise
tracks **после** Phase 6 (полный enterprise super-set,
полное замещение всех Phase 2 stub'ов одновременно,
полное rollback покрытие, AST-парсер, web-UI, full
version-matrix smoke, etc.). Phase 7 как отдельная
интеграционная фаза не запланирована — крупные новые
направления входят как параллельные track'и, а не как
ещё один линейный MVP.

## Closed parallel tracks

После закрытия Phase 6 были последовательно открыты и
закрыты пятнадцать post-phase completion track'ов:

- **Parallel Track A — Full Real 1cv8-backed Write Path** —
  закрыт на Step 7 (final integration pass and Track A
  closure).
- **Parallel Track B — Productization & Delivery Polish** —
  закрыт на Step 6 (final integration pass and Track B
  closure).
- **Parallel Track C — Packaging & Installer Delivery** —
  закрыт на Step 6 (final integration pass and Track C
  closure).
- **Parallel Track D — Operator Credentials Hardening** —
  закрыт на Step 6 (final integration pass and Track D
  closure).
- **Parallel Track E — Multi-Version 1C Smoke Matrix** —
  закрыт на Step 6 (final integration pass and Track E
  closure).
- **Parallel Track F — Rollback Whitelist Expansion** —
  закрыт на Step 6 (final integration pass and Track F
  closure).
- **Parallel Track G — Production-Grade MCP Transport and
  CLI** — закрыт на Step 6 (final integration pass and
  Track G closure).
- **Parallel Track H — Network-Grade MCP Transport and
  Authentication Boundary** — закрыт на Step 6 (final
  integration pass and Track H closure).
- **Parallel Track I — Installer Auth Round-Trip
  Integrity** — закрыт на Step 6 (final integration pass
  and Track I closure).
- **Parallel Track J — TLS and Reverse-Proxy Deployment
  Boundary** — закрыт на Step 6 (final integration pass
  and Track J closure; PATH A docs-only; Q7 = NO-BUMP,
  Track J закрыт под existing `0.5.1`).
- **Parallel Track K — Real MCP Client Integration
  Test** — закрыт на Step 6 (final integration pass
  and Track K closure; PATH B narrow harness;
  Q7 = NO-BUMP, Track K закрыт под existing `0.5.1`).
- **Parallel Track L — Service Supervision and OS
  Service Registration** — закрыт на Step 6 (final
  integration pass and Track L closure; PATH B docs +
  one declarative systemd unit template; Q7 = NO-BUMP,
  Track L закрыт под existing `0.5.1`).
- **Parallel Track M — Packaging Ecosystem and
  Distribution Boundary** — закрыт на Step 6 (final
  integration pass and Track M closure; PATH B narrow
  `pyproject.toml` wheel-build flip + one operator
  recipe; **Q7 = PATCH**, `pyproject.toml` version
  bumped `0.5.1 → 0.5.2` за declared-but-non-functional
  `[project.scripts]` surface, ставший functional
  через `python -m build` после Step 4 flip).
- **Parallel Track N — Observability and Diagnostics
  Boundary** — закрыт на Step 6 (final integration
  pass and Track N closure; PATH A docs-only +
  exactly one operator-facing recipe; **Q6 = NO-BUMP**,
  Track N закрыт под existing `0.5.2`, без further
  bump — production code не правился ни в одном из
  шести Track N шагов; recipe documents existing
  signals без их изменения; Track J/K/L NO-BUMP
  precedents применяются напрямую — Track N — purest-
  form Track J analogue).
- **Parallel Track O — Dev-Time Editable Install
  and Workspace Discovery** — закрыт на Step 6
  (final integration pass and Track O closure;
  PATH A docs-only + exactly one contributor-facing
  recipe; **Q7 = NO-BUMP**, Track O закрыт под
  existing `0.5.2`, без further bump — production
  code не правился ни в одном из шести Track O
  шагов; recipe documents existing latent hatchling
  PEP 660 editable-install capability без его
  изменения; Track J/K/L/N NO-BUMP precedents
  применяются напрямую — Track O — purest-form
  Track N analogue).

## Active parallel tracks

На текущий момент **два** post-phase parallel
track'а активны одновременно — оба находятся на
Step 1 (planning only), оба добавлены без code
changes:

1. **Parallel Track P — Test Suite Shipping and
   Verification Boundary** (шестнадцатый post-
   phase parallel track; открыт первым, commit
   `d6f1936`).
2. **Parallel Track Q — Windows Installer Path
   and setup.exe Delivery** (семнадцатый post-
   phase parallel track; открыт сейчас).

Треки независимы: Track P закрывает gap в
behavioural-unit / integration testing surface;
Track Q закрывает gap в Windows installer
experience для ordinary user без preinstalled
Python / pip / Git. Track Q **не** touch'ает
Track P deliverables; Track P **не** touch'ает
Track Q deliverables. Открытие следующих шагов
обоих треков — independent operator decisions.

### Active parallel track — Track P (Step 1 planning only)

**Parallel Track P — Test Suite Shipping and
Verification Boundary** — открыт на Step 1 (planning
only) после Track O closure (commit `720ac54`,
`0.5.2`). Track P is the sixteenth post-phase
parallel track and addresses the long-standing
aspirational `[tool.pytest.ini_options]
testpaths = ["tests"]` declaration in
`pyproject.toml:31-32`, plus the explicit "no test
suite yet" / "It does NOT run pytest" hand-off
markers in `scripts/dev/launch.ps1:28` and `:86`.

**Цель Track P.** Конвертировать current honest gap

> "проект имеет три working verification gates
> (`selfcheck.py` pre-flight, `verify-release.ps1`
> release-side 8-check, `mcp_client_smoke.py`
> transport-boundary smoke), но shipped automated
> test suite как in-repo surface отсутствует —
> `tests/` directory не существует на HEAD
> `720ac54`, хотя `pyproject.toml:31-32` declares
> `[tool.pytest.ini_options] testpaths = ["tests"]`
> aspirationally"

в disciplined six-step closure track формы Tracks
A–O (planning → audit → contract → narrow
implementation → docs alignment → final integration
pass). Track P закрывает long-standing aspirational
declaration the same way Track M closed the
`packages = []` aspirational declaration: either
docs-only formalisation (PATH A) or materialisation
via narrow `tests/` slice + dev-only `pytest` extra
declaration (PATH B). The three existing gates
remain byte-identical — Track P does NOT subsume
them; it adds the **behavioural unit / integration
test layer** that complements them.

**Step 1 — planning only (этот commit).** Ship'нуты
ровно два новых architecture doc'а:

- [`docs/architecture/track-p-test-suite-shipping-and-verification-boundary-plan.md`](docs/architecture/track-p-test-suite-shipping-and-verification-boundary-plan.md)
  — 14-section planning document (purpose / current
  post-Track-O baseline / honest gap statement
  grounded в `pyproject.toml:31-32` + `scripts/dev/
  launch.ps1:28+86` anchors / why existing gates do
  NOT equal a shipped test suite / goal / in-scope
  / out-of-scope с 23+ explicit denials including
  performance / load / stress / fuzz / browser /
  mutation / snapshot / live-1С / SaaS / multi-
  Python-matrix / containerised-CI / coverage-gate-
  absolutism / verification-philosophy redesign /
  guardrails 25 hard invariants / acceptance
  criteria 12 items / honest constraints /
  relationship-to-Tracks-K/N/O table / Q1–Q7
  directional defaults / step trajectory / honest
  summary).
- [`docs/architecture/track-p-test-suite-shipping-and-verification-boundary-step-map.md`](docs/architecture/track-p-test-suite-shipping-and-verification-boundary-step-map.md)
  — six-step boundary (Goal / What changes / What
  does NOT change / Result) + 33 track invariants
  block + hard out-of-scope carry-through + Step 6
  Q7 framing.

**Q1–Q7 directional defaults.**

- Q1 (closure-gate target) → **(B) recipe + narrow
  tests slice** as the most likely outcome
  (materialises the aspirational `testpaths`
  declaration; mirrors Track M / Step 4 closing the
  `packages = []` aspirational declaration);
  **(A) recipe-only** acceptable fallback if Step
  2 audit reveals materialising expands scope;
  **(C) non-production helper alone** rejected by
  default.
- Q2 (primary test class focus) → **(A) unit tests**
  on dataclasses / models / registry helpers /
  policy-engine decisions first; **(C) repo-local
  behavioural tests** as natural second class;
  **(B) subprocess-level integration** rejected
  by default (Track K's harness already covers
  that axis).
- Q3 (Step 4 PATH openness) → **PATH B docs +
  narrow tests slice + narrow pyproject dev-extra
  primary**, PATH A held in reserve; **Step 4
  PATH not locked at Step 1**; Step 3 contract is
  the lock point.
- Q4 (minimum closure scope) → closure document
  MUST eventually answer: what supported test-suite
  shape is (`pytest`-invoked under `tests/`); what
  tests cover and do not cover; how a contributor
  runs the tests; how tests relate to existing
  gates (complementary axes, not replacements);
  what is explicitly out-of-scope.
- Q5 (insufficient closure proof) → "aspirational
  declaration is enough" / "selfcheck covers it"
  / "verify-release covers it" / "smoke harness
  covers it" / "manual checking works" / "tests
  pass on my machine" — все insufficient.
- Q6 (production code change) → likely **NOT
  required**; tests target existing behaviour;
  Step 2 audit must verify honestly.
- Q7 (SemVer expectation) → **(A) NO-BUMP** if
  Step 4 PATH A docs-only mirroring Track J/K/L/N/O
  precedent; **(B) PATCH** as the more likely
  outcome if Step 4 PATH B materialises the
  aspirational `testpaths = ["tests"]` declaration
  (mirror of Track I / Track M PATCH precedents
  for declarative-defect-class repair); **(C)
  MINOR** explicitly rejected; MAJOR forbidden by
  track scope.

**Step 1 явно НЕ делает:** не открывает Step 2; не
пишет audit doc; не меняет production code; не
меняет `pyproject.toml`; не меняет `scripts/*`; не
меняет `SECURITY.md`; не меняет `docs/release-
handoff.md`; не меняет `CHANGELOG.md`; не меняет
`apps/platform/README.md`; не меняет manuals; не
меняет existing operator recipes (Track J/L/M/N
byte-identical); не меняет Track O dev recipe;
не меняет registries (`read=15 / write=25 /
intelligence=16` invariant carried through); не
запускает `1cv8.exe`; не делает remote push; не
фиксирует Q1–Q7 как decided answers (только
defaults / directional recommendations); не
добавляет Track P в Closed parallel tracks list
(still 15 entries A–O; что произойдёт только на
Step 6).

**Что Track P явно НЕ решает (carry-through через
все шесть шагов).** No performance benchmarking
(no `pytest-benchmark`); no load testing (no
`locust` / `wrk` / JMeter); no stress testing; no
fuzzing (no `hypothesis` / `atheris`); no browser
/ UI tests (no Selenium / Playwright / Cypress);
no web dashboard testing; no real `1cv8.exe`
execution (tests MUST NOT invoke `1cv8.exe`); no
external SaaS / live-network integration; no
multi-Python-version matrix (Python 3.11 pin
preserved); no containerised CI lab; no snapshot /
golden approval framework (no `approvaltests` /
`pytest-snapshot`); no mutation testing (no
`mutmut` / `cosmic-ray`); no coverage-gate
absolutism (coverage measurement, if introduced,
remains diagnostic-only); no rewriting verification
philosophy of selfcheck / verify-release / smoke
harness (three existing gates remain byte-
identical); no transport / auth / deployment /
service / packaging / observability / dev-time
recipe redesign; no new MCP tools; no registry
changes; no new CLI flag on existing servers; no
new `[project.scripts]` entries; no new runtime
dependencies (Step 4 MAY add `[project.optional-
dependencies] test = ["pytest"]` only if Step 3
contract authorises PATH B/C); no new entrypoint
module; no `1cv8.exe` runs; no outbound network in
any committed test; no remote push; no "testing
solved forever" / "full QA stack shipped" /
"complete confidence matrix" / "production-grade
certification" / "enterprise test infrastructure"
/ "100% coverage achieved" / "all behaviours
covered" claim.

**Selfcheck note.** `scripts/dev/selfcheck.py`
`status=ok` на post-Step-1 commit; registries
`read=15 / write=25 / intelligence=16` invariant
preserved. `scripts/release/verify-release.ps1
-AllowDirtyTree` GREEN на 8 checks.

**Канонический next step:** Parallel Track P /
Step 2 — descriptive baseline audit of current
verification state. Открытие Step 2 — отдельное
operator decision; никакой автоматизации.

### Active parallel track — Track Q (Step 1 planning only)

**Parallel Track Q — Windows Installer Path and
setup.exe Delivery** — открыт на Step 1 (planning
only) как **семнадцатый** post-phase parallel
track. Track Q адресует другой честный gap, чем
Tracks A–P: ни один из предыдущих треков **не**
закрыл setup.exe UX для обычного Windows-
пользователя.

**Честкий gap-statement Track Q.** У проекта есть:

- **wheel/pip path** (Track M:
  `1c_agent_platform-0.5.2-py3-none-any.whl`,
  `pip install <WHEEL_PATH>`),
- **install fast-path PowerShell wrapper**
  (Track B / Track I: `scripts/release/install.ps1`,
  "thin scripts-only wrapper"),
- **editable install** (Track O:
  `pip install -e .`).

Все три presuppose, что на машине **уже стоит**
Python 3.11 + pip (+ для git-based flow — Git).
**Обычный Windows-пользователь** этого не имеет.
**Setup.exe path отсутствует.** Конечный
пользовательский install experience —
"скачал → двойной клик → Next/Install/Finish →
установлено" — **не закрыт**. Никакого
`setup.exe`, никакого installer-technology
definition file (`.iss` / `.wxs` / `.nsi`),
никакого bundled Python runtime artefact в репо
нет на HEAD `d6f1936`. Anchors прямо acknowledge
deferral:

- `scripts/release/install.ps1:1-11` — "It does
  NOT introduce a new install ecosystem. No
  `.msi`, no `.deb`, no GUI wizard, no signed
  distribution."
- `docs/operators/packaging/distribution-boundary.md`
  §7 — verbatim "no GUI installer" среди explicit
  non-goals Track M recipe.
- `pyproject.toml` Track M comment block (lines
  44–50) — "no GUI installer", "no Chocolatey /
  Homebrew / apt / conda-forge / NuGet", "no
  enterprise-ready packaging".

Эти anchor'ы — honest deferrals, не permanent
closures. Track Q — dedicated narrow track, что
эту deferral закрывает.

**Цель Track Q.** Конвертировать gap выше в
disciplined six-step closure track формы Tracks
A–P (planning → audit → contract → narrow
implementation → docs alignment → final
integration pass). Single supported install
experience: download `setup.exe` → double-click
→ Next/Install/Finish → installed; uninstall
через стандартный Windows "Settings → Apps →
Installed apps" surface (Inno Setup native
behaviour, регистрация под
`HKCU\Software\Microsoft\Windows\CurrentVersion\
Uninstall\<GUID>`).

**Step 1 — planning only (этот commit).**
Ship'нуты ровно два новых architecture doc'а:

- [`docs/architecture/track-q-windows-installer-path-and-setup-exe-delivery-plan.md`](docs/architecture/track-q-windows-installer-path-and-setup-exe-delivery-plan.md)
  — 14-section planning document (purpose / current
  post-Tracks-A–O baseline relevant to Track Q
  including inventory existing install-adjacent
  surfaces and their Python prerequisite / honest
  gap statement в шести независимо проверяемых
  observations / **central honest constraint
  § 4 — bundled Python runtime структурно
  требуется**, прямо названо как §4, не как
  footnote / goal of the track / in-scope / out-
  of-scope с 30+ explicit denials (no Linux/macOS
  installer / no broad `.msi`/`.deb`/`.rpm`/`.dmg`
  ecosystem / no PyPI / no package-manager matrix /
  no code signing / no auto-update / no GUI
  dashboard / no service supervision redesign /
  no auth redesign / no transport redesign / no
  new MCP tools / no new CLI flags / no new
  `[project.scripts]` / no new dependencies / no
  remote-dev / no enterprise installer platform /
  no containerisation / no cluster-HA / "all
  Windows distributions supported" / "one-click
  everything solved forever" / "enterprise-grade
  installer" / "production-ready desktop app" /
  "GUI config wizard" / "Windows service auto-
  magic by default" claims) / guardrails 30 hard
  invariants / acceptance criteria 12 items /
  honest constraints after closure / relationship-
  to-Tracks-M/L/O/P table / Q1–Q7 directional
  defaults / step trajectory / honest summary).
- [`docs/architecture/track-q-windows-installer-path-and-setup-exe-delivery-step-map.md`](docs/architecture/track-q-windows-installer-path-and-setup-exe-delivery-step-map.md)
  — six-step boundary (Goal / What changes / What
  does NOT change / Result) + 35 track invariants
  block (включая Track P / Step 1 planning surface
  byte-identical invariant) + hard out-of-scope
  carry-through + Step 6 Q7 framing.

**Central honest constraint (план §4).** Платформа
— pure-Python codebase (Track M `py3-none-any`
wheel содержит eleven src-layout packages). При
runtime требуется CPython 3.11 interpreter.
**Acceptance criterion "no preinstalled Python /
pip / Git" структурно требует bundled Python
runtime** внутри installer'а. Структурно
существуют ровно две честные опции:

- **(α) Bundled embeddable distribution** —
  `python-3.11.<x>-embed-amd64.zip` от python.org
  (~10 MB: `python.exe`, stdlib `.zip`,
  `pythonXY.dll`, minimal `.pyd` modules); installer
  extracts его в install directory.
- **(β) Frozen executable distribution** —
  PyInstaller / Nuitka / Briefcase / py2exe
  produces standalone `.exe` files; installer
  ships frozen exes.

Нет честной третьей опции. **(α)** — default
expectation (поскольку **(β)** добавляет
PyInstaller/Nuitka toolchain'ы, которых сегодня в
репо нет). Expected installed footprint — около
**10–15 MB** (~10 MB embeddable CPython + ~1 MB
платформа + small installer overhead). Это
**структурная стоимость** закрытия gap'а;
никакого reduction не promised. Никакого bundled-
runtime бинаря в git commit'ах быть **не должно**
— python.org embeddable acquires the build helper
**at build time**, не at clone time.

**Q1–Q7 directional defaults (план §12).**

- Q1 (closure target) → **один real `setup.exe`
  installer path** для обычного Windows
  пользователя; **(B) recipe + narrow `.iss`
  installer-definition slice** как most likely
  outcome; **(A) recipe-only** acceptable
  fallback; **(C) standalone build helper без
  `.iss`** rejected by default.
- Q2 (installer technology default) → **(A) Inno
  Setup** baseline (простейшая честная Windows
  installer technology с native uninstall
  registry support; declarative `.iss`; free
  tooling; long reliability track record); **(B)
  WiX / `.msi`** considered только если Step 2
  surfaces grounded MDM / SCCM / Intune operator
  need; **(C) NSIS** considered только если Step 2
  surfaces specific need; **(D) Advanced
  Installer / (E) InstallShield / (F) MSIX**
  rejected by default. **Step 1 explicitly does
  NOT lock** technology choice; Step 3 contract —
  lock point.
- Q3 (Step 4 PATH openness) → **PATH B** (recipe
  + один `.iss` + optionally build helper)
  primary; **PATH A** docs-only в резерве; **PATH
  C** standalone helper rejected. **Step 4 PATH
  not locked at Step 1**; Step 3 contract — lock
  point.
- Q4 (install experience prerequisite stance) →
  install experience **MUST NOT** require
  preinstalled Python / pip / Git / Visual Studio
  Build Tools / MSVC / Windows SDK / C/C++ runtime
  / Chocolatey / winget / Scoop / NuGet. **Direct
  implication**: installer **MUST** bundle (или
  pull at install time) Python runtime; default
  expectation — python.org embeddable CPython 3.11
  pulled at build time.
- Q5 (uninstall path stance) → uninstall — **first-
  class part of supported boundary**; installer
  **MUST** register uninstall entry под
  `HKCU\Software\Microsoft\Windows\CurrentVersion\
  Uninstall\<GUID>` (или per-machine `HKLM`
  equivalent); ordinary Windows "Settings → Apps
  → Installed apps" surface — supported entry
  point uninstall'а; Inno Setup handles это
  natively.
- Q6 (production code change) → **likely NOT
  required**; installer packages existing wheel
  contents + bundled runtime; behaviour
  идентичный независимо от того, через какой
  Python platform запущена; Step 2 audit должен
  verify honestly; default expectation — Step 3
  contract explicitly forbids production code
  changes at Step 4.
- Q7 (SemVer expectation) — **directional
  framing only**, lock на Step 6: **(A) NO-BUMP**
  под PATH A docs-only (mirror Track J/K/L/N/O
  precedent); **(B) PATCH** defensible под PATH B
  framed as defect-class delivery-channel repair
  (mirror Track I / Track M precedents); **(C)
  MINOR** defensible под PATH B framed as new
  operator-visible delivery channel (mirror
  Track H precedent — HTTP transport как новая
  delivery capability); **(D) MAJOR** forbidden
  by track scope. Step 1 захватывает все три
  (NO-BUMP / PATCH / MINOR) как live possibilities
  и lock'ает **ни одну**.

**Step 1 явно НЕ делает:** не открывает Step 2;
не пишет audit doc; не выбирает installer
technology (Inno Setup — directional default, не
contract-binding); не commit'ит installer-
definition file; не commit'ит bundled-runtime
binary; не меняет production code; не меняет
`pyproject.toml`; не меняет `scripts/*` (включая
`scripts/release/install.ps1`, чей umbrella
comment мы цитируем как anchor — он сам
byte-identical); не troget'ит Track P / Step 1
planning surface; не troget'ит existing operator
recipes (Track J/L/M/N byte-identical) и Track O
dev recipe; не trogeт `SECURITY.md` /
`docs/release-handoff.md` / `CHANGELOG.md` /
`apps/platform/README.md` / manuals; не меняет
registries (`read=15 / write=25 / intelligence=16`
invariant carried through); не запускает
`1cv8.exe`; не делает remote push; не фиксирует
Q1–Q7 как decided answers (только defaults /
directional recommendations); не добавляет Track Q
в Closed parallel tracks list (still 15 entries
A–O); не открывает параллельно ещё один трек.

**Что Track Q явно НЕ решает (carry-through через
все шесть шагов).** No Linux installer (`.deb` /
`.rpm` / `.apk` / `.AppImage` / `.snap` /
`.flatpak`); no macOS installer (`.dmg` / `.pkg` /
`.app` / Homebrew cask / MacPorts / notarization);
no broad `.msi` ecosystem (WiX considered только
по grounded reason); no Chocolatey / winget /
Scoop / NuGet / Microsoft Store publication; no
PyPI publication; no code signing / Authenticode /
EV cert / notarization / SBOM / SLSA / supply-
chain attestation; no auto-update / OTA / delta-
update; no GUI dashboard / browser UI / web admin
panel; no service supervision redesign (Track L
preserved; installer **не** registers Windows
Service by default); no auth redesign (Tracks D /
H preserved); no transport redesign (Tracks G / H
preserved); no new MCP tools; no registry changes
(MCP registry, not Windows registry — last in
scope только для uninstall entry); no new CLI flag
on existing servers; no new `[project.scripts]`
console entries; no new entrypoint module; no new
project dependencies (ни runtime, ни optional);
no new transports; no remote-dev / IDE
integration (Track O preserved); no enterprise
installer platform / MDM / Group Policy / SCCM /
Intune; no containerisation (Dockerfile / OCI /
Podman); no cluster / HA; no "all Windows
distributions supported" claim (default support
matrix — Windows 10 + 11 amd64; Windows 7 /
Server / ARM64 / x86 — out of default); no
"one-click everything solved forever" claim; no
"enterprise-grade installer" claim; no
"production-ready desktop app" claim; no "GUI
config wizard" claim (installer drops platform
на диск; product configuration — отдельный
operator step через existing surfaces); no
"Windows service auto-magic by default" claim; no
test-suite program (Track P territory); no
observability redesign (Track N preserved); no
remote push; no новый parallel track opened
within Step 1.

**Selfcheck note.** `scripts/dev/selfcheck.py`
`status=ok` на post-Step-1 commit; registries
`read=15 / write=25 / intelligence=16` invariant
preserved. `scripts/release/verify-release.ps1
-AllowDirtyTree` GREEN на 8 checks.

**Канонический next step:** Parallel Track Q /
Step 2 — descriptive baseline audit of current
Windows install reality (inventory persona,
existing install-adjacent surfaces и их Python
prerequisite, three anchor citations, option-
space audit shape α vs β из §4, technology-
choice audit Inno Setup vs WiX vs NSIS, Q1–Q6
directional resolutions, ≥10-item Step 3 handoff
list). Открытие Step 2 — отдельное operator
decision; никакой автоматизации.

## Track O detail (закрыт)

**Цель Track O** была — закрыть следующий честный
dev-time gap: после Track M ввёл узкий supported
deploy-time wheel distribution boundary (`pip
install <WHEEL_PATH>` для оператора, см.
[`docs/operators/packaging/distribution-boundary.md`](docs/operators/packaging/distribution-boundary.md)),
у проекта всё ещё не было formal **dev-time**
boundary для contributors editing the repo. В
`scripts/dev/README.md:5-11` явно говорилось
"editable install и workspace discovery всё ещё
out of scope" — sentence committed во время Track
M / Step 4 как explicit hand-off marker для
future track. В `docs/architecture/phase-1-entry.md:79-82`
ещё ранее предсказывалось, что "потребуется
нормальный packaging / workspace setup (editable
install, entry points)". Track O — dedicated
narrow track, **orthogonal to Track M**: deploy-
time wheel distribution остался в scope Track M;
dev-time editable workflow для contributors —
новая, отдельная axis (different audience,
different lifecycle moment, different install
verb).

**Что Track O явно НЕ решает.** Production code
changes; transport / auth / deployment-boundary /
service-supervision / packaging / observability
redesign (Tracks G/H/I/J/L/M/N carry-forward);
containerised dev environment (no Dockerfile, no
`docker-compose.yml`, no `.devcontainer/`); IDE-
specific integration (no `.vscode/`, no `.idea/`,
no Cursor / Zed / Sublime / Vim project files);
remote-dev workflow (no Codespaces, no GitPod, no
Coder template); multi-Python-version matrix
(`.python-version` Python 3.11 pin preserved);
formatter / linter / test-runner policy redesign
(existing `[tool.ruff]` and
`[tool.pytest.ini_options]` operator/contributor-
side discretion); alternative build-backend
evaluation (hatchling remains); test-suite
shipping (the empty `tests/` directory remains
out-of-scope); installable-from-git-URL story
(operator-side or end-user-side install via
`pip install <git-URL>` is a different workflow
with different threat-model implications);
enterprise identity stack; clustering / HA /
orchestration; web UI / dashboard frontend; new
MCP tools; registry changes; new CLI flag on
existing servers; new `[project.scripts]`
entries; new dependencies; new entrypoint module;
1cv8 work; "developer workflow solved forever"
/ "all IDE integrations supported" / "all package
managers supported for dev install" /
"containerised dev environment shipped" /
"remote-dev shipped" / "enterprise developer
experience" / "production-ready DX" / "DX matrix
complete" claim — Track O's closure-gate covers
**только** одну integration-and-naming slice
(contributor-facing recipe documenting existing
latent capabilities); broader DX matrices remain
recommended-only.

**Step 3 PATH A docs-only (locked).** Step 3
contract pinned **PATH A**. PATH B (narrow
declarative slice — e.g., `bootstrap_paths.sh`
POSIX-shell sibling or a `pyproject.toml`
editable-install comment block) explicitly
rejected — `pip install -e .` already works on
Windows / Linux / macOS via hatchling's PEP 660
default behaviour against Track M's populated
`[tool.hatch.build.targets.wheel] packages` array;
adding a POSIX-shell sibling would create a third
source of truth for the 11 src-layout paths;
adding an editable-install comment block to
`pyproject.toml` would touch Track M's locked
artefact for prose value. PATH C (developer
bootstrap helper script) explicitly rejected —
`launch.ps1` umbrella already provides single-
entry-point discoverability; a competing helper
would muddy the boundaries. Step 4 ship'нул ровно
один файл:

- [`docs/dev/editable-install-and-workspace-discovery.md`](docs/dev/editable-install-and-workspace-discovery.md)
  — 586-line contributor-facing recipe (под soft
  cap ≤700 RECOMMENDED и hard cap ≤1000). 9 top-
  level sections: §1 Purpose / scope с **8
  explicit denials of forbidden maturity claims**
  ("Developer workflow solved forever" / "All IDE
  integrations supported" / "All package managers
  supported for dev install" / "Containerised dev
  environment shipped" / "Remote-dev shipped" /
  "Enterprise developer experience" / "Production-
  ready DX" / "DX matrix complete"); §2 Supported
  install verbs — **first-class `pip install -e .`**
  run from repo root in Python 3.11 environment
  (Windows PowerShell + POSIX bash/zsh venv
  setup examples; mechanically supported by
  hatchling's PEP 660 default against Track M's
  populated `packages` array; installs 11 src-
  layout packages + 3 `[project.scripts]` console
  entries; zero third-party runtime dependencies),
  **recommended-only Windows-only alternative**
  dot-source `scripts/dev/bootstrap_paths.ps1`
  (session-scoped, PowerShell-only, no console
  scripts), cross-OS posture table; §3 Supported
  tooling preconditions (Python 3.11 mandatory
  per `.python-version` + `requires-python`; `pip`
  mandatory; venv tool recommended; `build`
  required only for Track M wheel construction;
  formatter / linter / test-runner / IDE not
  required by recipe); §4 Workspace-discovery
  answer — the **eleven src-layout package roots**
  enumerated verbatim from `pyproject.toml:51-63`
  (the Track M lock) with dual-role explanation
  (Track M wheel-build packages array + dev-time
  PYTHONPATH bootstrap entries); acceptable-
  duplication acknowledgement between
  `pyproject.toml` and `scripts/dev/bootstrap_paths.ps1`;
  §5 Verification step — `python scripts/dev/
  selfcheck.py` (или `.\scripts\dev\launch.ps1
  selfcheck` on Windows); canonical PASS line
  `selfcheck_status = ok`; Track N FC4 inheritance
  preserved; what selfcheck does and does not
  prove explicitly enumerated; §6 Relationship to
  Track M — **orthogonal-and-complementary**
  axes table (different audience: operator vs
  contributor; different lifecycle moment: deploy-
  time vs dev-time; different install verb:
  `pip install <WHEEL_PATH>` vs `pip install -e .`;
  cross-references to Track M recipe; no content
  duplication); §7 Authoritative non-goals (7
  sub-sections covering containerised dev / IDE /
  remote-dev; multi-Python-version / build-backend;
  tooling policy; installable-from-git-URL;
  cross-track scope; 8 forbidden maturity-claim
  recap; other carry-over); §8 Cross-references —
  6 mandatory anchors с file-path links: Track M
  `distribution-boundary.md` (orthogonal axis);
  `pyproject.toml` (single source of truth for 11
  packages array); `scripts/dev/bootstrap_paths.ps1`
  (recommended-only alternative); `scripts/dev/launch.ps1`
  (Windows umbrella); `scripts/dev/selfcheck.py`
  (Track N FC4 verification gate);
  `scripts/dev/README.md` (historical hand-off
  marker pointer); §9 Honest summary.

**Q7 = NO-BUMP** (Track O закрыт под existing
`0.5.2`, без further bump). Защита решения
(grounded в repo facts):

- **PATH A docs-only.** Step 4 ship'нул ровно один
  новый файл `docs/dev/editable-install-and-
  workspace-discovery.md`; ноль production code
  change; ноль `pyproject.toml` change; ноль
  `scripts/*.ps1` / `scripts/*.py` logic change.
  Step 5 narrowly replaced two prose sentences в
  `scripts/dev/README.md` per contract §3.5
  authorisation — no script-logic change.
- **No new declared surface.** No new CLI flag on
  existing servers; no new `[project.scripts]`
  entry; no new MCP tool (registry invariant
  `read=15 / write=25 / intelligence=16` carried
  through через все шесть Track O шагов); no new
  entrypoint module; no new dependency; no new
  env-var convention.
- **No defect-class repair.** Track I PATCH
  precedent (`installer.py:_config_to_dict` +15
  LOC) required a declared-but-broken surface
  being made working; Track M PATCH precedent
  (`pyproject.toml` packages flip +7 LOC) required
  a declared-but-non-functional surface being made
  functional. Track O имеет **ноль** broken
  surfaces to repair — `pip install -e .` was
  already mechanically supported by hatchling's
  PEP 660 default against Track M's populated
  packages array; recipe **documents** that latent
  capability, does **not** make it work.
- **Track J / Track K / Track L / Track N NO-BUMP
  precedents apply directly.** Track J = PATH A
  docs-only deployment-boundary recipe → NO-BUMP.
  Track K = single new diagnostic file → NO-BUMP.
  Track L = docs + one declarative systemd unit
  template → NO-BUMP. Track N = PATH A docs-only
  observability recipe → NO-BUMP. **Track O —
  purest-form Track N analogue**: pure docs-only
  contributor-facing recipe, no template, no
  helper, no code.
- **Step 3 contract §13.5 / §11.4 explicitly
  framed NO-BUMP** as the default under PATH A,
  explicitly prohibited PATCH under PATH A (no
  code change occurs), и explicitly prohibited
  MINOR under any path (guardrails §1.4 — no new
  CLI flag, no new declared surface). MAJOR
  forbidden by track scope.
- **SemVer §6 framing.** PATCH = backward-
  compatible bug fixes. Track O Step 4 =
  backward-compatible **documentation of existing
  latent behaviour**, not a bug fix. Therefore
  NO-BUMP is the only honest outcome.

Шесть meaningful commit'ов в `main`: `4122431`
(Step 1 — planning, два planning doc'а с Q1–Q7
directional defaults) / `c8941a4` (Step 2 —
descriptive baseline audit с file:line citations
across 17 existing dev-time surfaces; key finding:
gap is integration-and-naming, not tooling
generation) / `2a24fc4` (Step 3 — normative
contract pinning **PATH A docs-only** (PATH B /
PATH C explicitly rejected); canonical recipe
path `docs/dev/editable-install-and-workspace-
discovery.md` locked; six mandatory content
elements C2–C7 locked; six mandatory cross-
references C8 locked; cross-OS posture C9 locked;
8 mandatory denial phrases locked; exhaustive
forbidden-files surface locked; V1–V12 + P1–P4
verification protocol locked; first-class install
verb `pip install -e .` locked; recommended-only
alternative `bootstrap_paths.ps1` locked; Q7
framed NO-BUMP default под PATH A mirroring Track
J/K/L/N precedent) / `24b2ee7` (Step 4 — narrow
PATH A implementation: ровно один новый файл —
`docs/dev/editable-install-and-workspace-discovery.md`
586 lines — contributor-facing recipe со всеми
contract-required elements; ноль production code
change) / `88121ad` (Step 5 — developer docs and
dev-time workflow alignment: четыре CLASS-1/2
modified files — README + PROJECT-STATUS +
scripts/dev/README.md narrow line-replacement of
hand-off-marker sentences per contract §3.5/§13.4
authorisation + docs/release-handoff.md "Where to
read deeper" bullet; ноль forbidden surface
touched) + closure commit Step 6 (final
integration pass and Track O closure; **NO-BUMP**
`pyproject.toml` `version=0.5.2` preserved byte-
identical; этот commit).

Никакого containerised dev environment (no
Dockerfile / docker-compose / .devcontainer/);
никакого IDE-specific integration (no .vscode /
.idea / Cursor / Zed / Sublime / Vim bundles);
никакого remote-dev workflow (no Codespaces /
GitPod / Coder); никакого multi-Python-version
matrix (Python 3.11 pin preserved); никакого
formatter / linter / test-runner policy redesign;
никакого alternative build-backend evaluation
(hatchling remains); никакого test-suite shipping
(empty `tests/` остаётся out of scope); никакого
installable-from-git-URL story; никаких new MCP
tools; никакого registry change (`read=15 /
write=25 / intelligence=16` invariant carried
through через все шесть Track O шагов); никаких
transport / auth / deployment-boundary / service-
supervision / packaging / observability redesigns;
никакого 1cv8 work; никакого remote push. Stdio
transport runtime byte-identical к Track G /
Step 4; HTTP transport runtime byte-identical к
Track H / Step 4 (с Track I defect-fix layered on
top); installer round-trip integrity byte-
identical к Track I / Step 4; deployment-boundary
recipe byte-identical к Track J / Step 4; real
MCP client smoke harness byte-identical к Track K
/ Step 4; service-supervision recipe + systemd
template byte-identical к Track L / Step 4;
packaging distribution-boundary recipe + wheel-
build flip byte-identical к Track M / Step 4
(11-element `[tool.hatch.build.targets.wheel]
packages` array preserved); observability recipe
byte-identical к Track N / Step 4. `apps/*/src/`
+ `packages/*/src/` byte-identical к Track N
closure state `2737a52`.

**Recommended-next-track candidates** (recommendation
only, без автоматического открытия): structured-
logging library adoption track (post-Track-N
follow-up: `structlog` / `python-json-logger`
dependency + per-record key vocabulary + JSON-
line emitter path; explicit opt-in via new CLI
flag); narrow `selfcheck --json` mode track
(post-Track-N follow-up: PATH B-style single-file
slice for operators who want machine-readable
selfcheck output); `/healthz` / `/readyz` HTTP
endpoint track (carefully gated; Track J §6 defer
reversal would be a separate decision); Windows /
macOS implementation-covered service-supervision-
extension track (post-Track-L follow-up: pywin32
service wrapper + launchd `.plist` artefact);
broader packaging ecosystem track (`.msi` /
`.deb` / `.rpm` / `.dmg` / `.pkg` / signed
distribution chain / PyPI publication / multi-
package-manager publication — Track M sticks к
одному narrow buildable-wheel slice); multi-
version 1С matrix expansion (post-Track-E
follow-up); полный rollback / AST work (post-
Track-F / post-Track-A follow-ups); web UI /
dashboard frontend track; TLS-in-process / mTLS
expansion (separate enterprise-grade identity
track); enterprise identity stack track (SSO /
OIDC / RBAC / SAML / SCIM / multi-tenant); test-
suite shipping track (would close the empty
`tests/` aspiration in `pyproject.toml`); cross-
OS dev-bootstrap parity track (post-Track-O
follow-up: would address the PowerShell-only
nature of `bootstrap_paths.ps1` via a `bash`/`zsh`
sibling — currently mitigated by `pip install -e .`
covering POSIX). Эти кандидаты — recommendation
only, не auto-opened.

## Track N detail (закрыт)

**Цель Track N** была — закрыть следующий честный
продуктовый gap: у платформы уже были рабочие MCP
entrypoints (Track G), HTTP/stdio transports
(Tracks G/H), bearer auth (Track H), installer
integrity (Track I), deployment-boundary recipe
(Track J), real MCP client smoke proof (Track K),
service-supervision recipe + systemd template
(Track L), и packaging/distribution boundary +
buildable wheel (Track M), но не было **first-class
operator-facing observability/diagnostics boundary
document**. Платформа emit'ила ad-hoc diagnostic
signals (stderr via Python `logging` at `--log-level
INFO`, three-bucket exit codes, HTTP response
envelope с auth-failure failure-equivalence per
Track H §8.4, `scripts/dev/selfcheck.py` 11-line
key=value output, `scripts/release/verify-release.ps1`
8-check gate, `scripts/dev/mcp_client_smoke.py`
structured progress, install fast-path findings,
`onec-health` + `onec-troubleshooting` library
exports), и Track L `service-supervision.md` §9.3
уже pin'ил level-to-event mapping для systemd-
supervised path. Track J / Track L / Track M каждый
denying "full observability stack" в своём scope —
никто не определял позитивно, что supported
diagnostic surface IS. Step 2 baseline audit
формализовал пять independently-verifiable
observations: (1) нет central observability
document; (2) нет log-shape contract; (3) нет
documented triage recipe; (4) нет machine-readable
health signal documented; (5) нет central non-goals
document.

**Что Track N явно НЕ решает.** Production code
changes; transport / auth / deployment-boundary /
service-supervision / packaging redesign (Tracks
G/H/I/J/L/M carry-forward); full OpenTelemetry
program (no OTel SDK dependency, no collector
configuration, no span emission, no `traceparent`
header vocabulary); Prometheus / OpenMetrics
rollout (no `/metrics` endpoint, no
`prometheus_client` dependency, no histogram /
counter / gauge surface); Grafana / Tempo / Loki /
Jaeger / Mimir / Cortex / VictoriaMetrics platform
(no dashboards bundled, no datasource config, no
panel JSON); SIEM / SOC integration (no Splunk
forwarder, no Elastic ingestion, no SOAR
scaffolding); distributed tracing (no request-id
propagation across systems, no trace assembly);
alerting / paging / on-call workflows (no
PagerDuty / Opsgenie / Slack / email alert rules);
`/healthz` / `/readyz` / `/livez` endpoint (Track J
§6 defer preserved); log-aggregation forwarder
bundled (no `vector` / `fluentd` / `fluent-bit` /
`rsyslog` / `journal-remote` config); structured-
logging library rollout (no `structlog` / `loguru`
/ `python-json-logger` dependency); log-level
redesign of existing `--log-level` flag (Track G);
new transport family; enterprise identity stack
(SSO/SAML/OIDC/SCIM/RBAC/ABAC/multi-tenant);
clustering / HA / orchestration platforms; web UI
/ dashboard frontend; new MCP tools; registry
changes; new CLI flag on existing servers; new
`[project.scripts]` entries; new dependencies; new
entrypoint module; 1cv8 work; "observability
solved forever" / "production-ready observability"
/ "full OpenTelemetry instrumentation" /
"Prometheus platform shipped" / "distributed
tracing ready" / "SIEM-ready" / "enterprise-ready
observability" / "alerting solved" / "all signals
covered" claim — Track N's closure-gate covers
**только** одну integration-and-naming slice
(operator-facing recipe documenting existing
signals); broader observability matrices remain
recommended-only.

**Step 3 PATH A docs-only (locked).** Step 3
contract pinned **PATH A**. PATH B (selfcheck
--json structured-output slice) explicitly
rejected — selfcheck output already operator-
parseable as 11 key=value lines; no operator
blocked by absence of --json mode; touching
selfcheck.py defensible only as defect-class
repair, no defect class present. PATH C (log-shape
contract slice across three MCP server
entrypoints) explicitly rejected — existing log
format string at `_stdio_transport.py:66` already
symmetric across both transports; helper would
expand touched-files surface for negligible gain.
PATH D (diagnostic-bundle helper under
`scripts/dev/`) considered and rejected — no
operator workflow currently consumes such a
bundle; existing surfaces work out-of-band; would
duplicate Track K smoke harness and Track L
journalctl recipe surface without clear additive
value. Step 4 ship'нул ровно один файл:

- [`docs/operators/observability.md`](docs/operators/observability.md)
  — 1043-line operator-facing recipe (под hard cap
  ≤1200 / soft cap ≤1000 RECOMMENDED). 13 top-
  level sections: §1 Purpose / scope с **9
  explicit denials of forbidden maturity claims**
  ("Observability solved forever" / "Production-
  ready observability" / "Full OpenTelemetry
  instrumentation" / "Prometheus platform shipped"
  / "Distributed tracing ready" / "SIEM-ready" /
  "Enterprise-ready observability" / "Alerting
  solved" / "All signals covered"); §2 Supported
  diagnostic surfaces — **7 first-class signals
  FC1–FC7** (stderr via Python `logging` at
  `--log-level INFO`; process exit codes 0/1/2;
  HTTP response envelope incl. auth-failure 401 +
  `WWW-Authenticate: Bearer realm="mcp"` + JSON-
  RPC `-32001` failure-equivalence;
  `scripts/dev/selfcheck.py` 11-key=value output;
  `scripts/release/verify-release.ps1` 8-check
  release gate; install fast-path findings;
  `journalctl -u <UNIT>.service` on Linux/systemd
  hosts deployed via Track L recipe), **4
  recommended-only signals R1–R4**
  (`mcp_client_smoke.py` transport-boundary smoke;
  `--log-level DEBUG` traces; `health_summary`
  MCP tool on `mcp-read-server`; per-request HTTP
  access lines), **10-item out-of-scope list**
  (carry-forward denials: no OTel / no Prometheus
  / no Grafana-Tempo-Loki-Jaeger / no SIEM / no
  distributed tracing / no alerting / no
  `/healthz` / no log-aggregation forwarder / no
  structured-logging library / no web UI); §3 Log
  levels and event mapping — inheriting
  `docs/operators/service/service-supervision.md`
  §9.3 verbatim с attribution (WARNING/ERROR for
  credential/auth/config; INFO for startup/
  shutdown + per-request HTTP access; DEBUG for
  transport detail); §4 Exit-code-meaning table
  (0 clean / 1 unhandled exception with
  traceback / 2 startup-time operator-readable
  failure single-line on stderr) с file:line
  citations; §5 HTTP response envelope summary
  (Track H §8.4 failure-equivalence на 401 +
  non-auth failure shapes 400/413/415 с -32600/-
  32700); §6 `/healthz` non-shipping carry-
  forward quoting `docs/operators/deployment-
  boundary.md` §6 verbatim; §7 Triage recipe с
  **тремя mandatory canonical failure modes**
  (T1 server exited code 2 immediately on startup
  с patterns table mapping last-stderr-line to
  cause to fix; T2 HTTP transport returns 401 to
  every request с bilateral server-side + client-
  side diagnosis; T3 selfcheck.py FAIL с
  traceback-driven triage and explicit "does NOT
  prove runtime works" caveat) + **двумя optional
  follow-ups** (T4 mcp_client_smoke transport
  failure; T5 systemd unit restart-loop); §8
  Relationship to existing recipes (Track J / L /
  M positioned как orthogonal-and-complementary;
  no content duplication); §9 Authoritative non-
  goals (9 sub-sections aggregating Track J §10 +
  Track L §9.5/§13 + Track M §13 + 9 forbidden
  maturity-claim recap); §10 Cross-OS posture
  (Linux/systemd/journald primary implementation-
  covered; Windows NSSM + macOS launchd + non-
  supervised execution prose-only; no fake parity
  claim); §11 Operator-side verification (7 copy-
  pasteable steps proving each first-class signal
  is readable on the operator's host); §12
  Honest summary; §13 Cross-reference index с
  file:line anchors back to production code,
  scripts, и Track J/L/M recipes.

**Q6 = NO-BUMP** (Track N закрыт под existing
`0.5.2`, без further bump). Защита решения
(grounded в repo facts):

- **PATH A docs-only.** Step 4 ship'нул ровно один
  новый файл; ноль production code change; ноль
  `pyproject.toml` change; ноль `scripts/*` change.
- **No new declared surface.** No new CLI flag on
  existing servers; no new `[project.scripts]`
  entry; no new MCP tool (registry invariant
  `read=15 / write=25 / intelligence=16` carried
  through через все шесть Track N шагов); no new
  entrypoint module; no new dependency; no new
  env-var convention.
- **No defect-class repair.** Track I PATCH
  precedent required declared-but-broken surface
  being made working; Track M PATCH precedent
  required declared-but-non-functional wheel-build
  being made functional. Track N имеет **ноль**
  broken surfaces to repair — existing diagnostic
  signals already work; recipe **documents** them,
  does **not** make them work.
- **Track J / Track K / Track L NO-BUMP
  precedents apply directly.** Track J = PATH A
  docs-only deployment-boundary recipe → NO-BUMP.
  Track K = single new diagnostic file under
  `scripts/dev/` → NO-BUMP (developer tool, not
  consumer-visible runtime capability). Track L =
  docs + one declarative systemd unit template →
  NO-BUMP (template is operator-copy artefact,
  not bundled production code). Track N — **purest-
  form Track J analogue**: pure docs-only operator-
  facing recipe, no template, no helper, no code.
- **Step 3 contract §13.5 / §11.4 explicitly
  framed NO-BUMP as the default expectation under
  PATH A**, and explicitly prohibited PATCH under
  PATH A (no code change occurs) и MINOR under
  any path (guardrails §1.4 — no new CLI flag, no
  new declared surface). MAJOR forbidden by track
  scope.
- **SemVer §6 framing.** PATCH = backward-
  compatible bug fixes. Track N Step 4 — backward-
  compatible **documentation of existing
  behaviour**, not a bug fix. Therefore NO-BUMP is
  the only honest outcome.

Шесть meaningful commit'ов в `main`: `efb4e5c`
(Step 1 — planning, два planning doc'а с Q1–Q7
directional defaults) / `d4183ca` (Step 2 —
descriptive baseline audit с file:line citations
across 17 existing diagnostic surfaces) /
`0ff3c2b` (Step 3 — normative contract pinning
**PATH A docs-only**, locking six mandatory
content elements C2–C7, seven mandatory cross-
references C8, cross-OS posture C9, nine
mandatory denial phrases, exhaustive forbidden-
files surface, V1–V12 + P1–P4 verification
protocol; Q6 framed NO-BUMP default mirroring
Track J/K/L precedent) / `76c47ba` (Step 4 —
narrow PATH A implementation: один файл
`docs/operators/observability.md` 1043 lines с
всеми contract-required elements; ноль
production code change) / `0d3627c` (Step 5 —
operator docs and observability alignment: три
CLASS-1/2 modified files — README + PROJECT-
STATUS + docs/release-handoff.md; ноль forbidden
surface touched) + closure commit Step 6 (этот
commit; final integration pass and Track N
closure; **NO-BUMP** `pyproject.toml`
`version=0.5.2` preserved byte-identical).

Никакого full observability stack rollout (no
OpenTelemetry SDK, no Prometheus / OpenMetrics
endpoint, no Grafana / Tempo / Loki / Jaeger
platform); никакого SIEM/SOC integration; никакого
distributed tracing; никакого alerting/on-call;
никакого `/healthz` endpoint (Track J §6 defer
preserved); никакого structured-logging library
dependency; никаких new MCP tools; никакого
registry change (`read=15 / write=25 /
intelligence=16` invariant carried through через
все шесть Track N шагов); никаких transport /
auth / deployment-boundary / service-supervision
/ packaging redesigns; никакого 1cv8 work;
никакого remote push. Stdio transport runtime
byte-identical к Track G / Step 4; HTTP transport
runtime byte-identical к Track H / Step 4 (с
Track I defect-fix layered on top); installer
round-trip integrity byte-identical к Track I /
Step 4; deployment-boundary recipe byte-identical
к Track J / Step 4; real MCP client smoke harness
byte-identical к Track K / Step 4; service-
supervision recipe + systemd template byte-
identical к Track L / Step 4; packaging
distribution-boundary recipe + wheel-build flip
byte-identical к Track M / Step 4 (11-element
`[tool.hatch.build.targets.wheel] packages`
array preserved). `apps/platform/src/onec_platform/`
+ `packages/*/src/` byte-identical к Track M
closure state `a3bdc48`.

**Recommended-next-track candidates** (recommendation
only, без автоматического открытия): structured-
logging library adoption track (post-Track-N
follow-up: introduce `structlog` / `python-json-
logger` dependency + per-record key vocabulary
+ separate JSON-line emitter path; explicit
opt-in via new CLI flag); narrow `selfcheck --json`
mode track (post-Track-N follow-up: PATH B-style
single-file slice for operators who want machine-
readable selfcheck output); `/healthz` /
`/readyz` HTTP endpoint track (carefully gated;
Track J §6 defer reversal would be a separate
decision); Windows / macOS implementation-covered
service-supervision-extension track (post-Track-L
follow-up: pywin32 service wrapper + launchd
`.plist` artefact); broader packaging ecosystem
track (`.msi` / `.deb` / signed distribution /
PyPI publication / multi-package-manager
publication — Track M closure-gate covered only
narrow buildable-wheel slice); multi-version 1С
matrix expansion (post-Track-E follow-up); full
rollback / AST work (post-Track-F / post-Track-A
follow-ups); web UI / dashboard frontend track;
TLS-in-process / mTLS expansion (separate
enterprise-grade identity track). Эти кандидаты —
recommendation only, не auto-opened.

## Track M detail (закрыт)

**Цель Track M** была — закрыть следующий честный
продуктовый gap: у платформы уже были рабочие MCP
entrypoints (Track G), HTTP/stdio transports
(Tracks G/H), bearer auth (Track H), installer
integrity (Track I), deployment-boundary recipe
(Track J), real MCP client smoke proof (Track K) и
service-supervision recipe + systemd template
(Track L), но не было взрослой packaging/distribution
story. В репозитории на момент открытия Track M
(commit `e21e185`) `pyproject.toml` декларировал три
`[project.scripts]` console entries
(`mcp-read-server` / `mcp-write-server` /
`mcp-intelligence-server`), но
`[tool.hatch.build.targets.wheel] packages = []` был
**намеренно пуст** per Track C / Step 3 honest
constraint (с 24-line comment block в `pyproject.toml`
явно объяснявшим: "`python -m build` produces no
usable artifact for this project"); не было buildable
wheel артефакта; не было source-archive release flow;
не было operator-bundle artefact; не было OS-native
package shipped; не было PyPI publication metadata;
не было signed-distribution chain; не было GUI
installer / wizard; не было ответа на вопрос "какой
артефакт оператор consume'ит" в
`docs/release-handoff.md` beyond cloning the repo.
Step 2 baseline audit формализовал четыре
независимо-верифицируемые observation'а: (1) wheel
build пуст по declarative artefact-surface; (2)
`scripts/release/README.md` явно говорит "no install
ecosystem"; (3) `docs/release-handoff.md` не содержал
operator-facing recipe для wheel; (4) declared
`[project.scripts]` entries функционально undeliverable
через `pip install`.

**Что Track M явно НЕ решает.** Production code
changes; transport / auth / deployment-boundary /
service-supervision redesign (Tracks G/H/I/J/L
carry-forward); broader packaging ecosystem (`.msi` /
`.deb` / `.rpm` / `.dmg` / `.pkg` / `.snap` /
`.flatpak`); multi-package-manager publication (no
PyPI, no Chocolatey, no Homebrew, no apt, no
conda-forge, no NuGet — wheel buildable но
**не** published anywhere); signed-distribution chain
(no signing keys, no `cosign` / `sigstore` /
Authenticode / Notarisation / SBOM / SLSA
attestation); GUI installer / wizard / setup.exe;
enterprise identity stack (SSO / SAML / OIDC / SCIM /
RBAC / ABAC / multi-tenant); clustering / HA /
orchestration platforms; web UI / dashboard
frontend; full observability stack; new MCP tools;
registry changes; new CLI flag на existing servers;
new `[project.scripts]` entries (три existing entries
locked); new dependencies; `/healthz` endpoint (Track
J §8 defer preserved); standalone `apps/platform`
daemon entrypoint; automatic update / OTA / self-
upgrade; rollback / AST / multi-version 1С matrix
expansion; 1cv8 work; "packaging solved forever" /
"PyPI release ready" / "signed binary distribution" /
"all package managers supported" / "production-ready
packaging" / "enterprise-ready packaging" /
"hostile-internet distribution ready" claim — Track
M's closure-gate covers **только** одну узкую
distribution-boundary slice (single buildable
pure-Python wheel + operator recipe для пяти lifecycle
verbs); broader matrices remain recommended-only.

**Step 4 PATH B (narrow declarative flip + operator
recipe).** Step 3 contract pinned **PATH B**: ровно
два файла. PATH A (docs-only) explicitly rejected
because Step 2 audit "zero buildable wheel artefact
at HEAD `79c541f`" cannot be closed honestly by prose
alone — recipe describing builds that produce nothing
operator-useful is not closure. PATH C (operator-
bundle artefact alongside / instead of wheel)
explicitly rejected because hatchling backend +
`[project.scripts]` + src-layout уже declared, и
flipping `packages = []` к populated list mechanically
narrower чем construction of a parallel `release/` /
`bundle/` directory layout. Step 4 ship'нул два
файла:

- [`docs/operators/packaging/distribution-boundary.md`](docs/operators/packaging/distribution-boundary.md)
  — 912-line operator-facing recipe (under contract
  §8.4 ≤1000 soft / ≤1200 hard caps). 14 top-level
  sections: §1 Purpose с explicit denial list, §2
  Supported distribution boundary (artefact class,
  single-wheel rationale, what Track M closes), §3
  Wheel contents (точный 11-package list — таблица +
  toml-блок), §4 Wheel non-contents (точный exclusion
  list по contract §5.3), §5 Build verb
  (`python -m build` + operator-side prerequisite
  `pip install build` + expected output filename +
  `.gitignore` policy reminder), §6 Install verb
  (`pip install <WHEEL_PATH>` + venv pattern +
  expected operator-visible result: три console
  scripts на PATH + 11 importable modules), §7
  Uninstall verb (`pip uninstall 1c-agent-platform` +
  что НЕ touch — operator-side config / .env /
  systemd unit / NSSM / launchd plist), §8 Upgrade
  verb (`pip install --upgrade <NEW_WHEEL_PATH>` +
  restart-after-upgrade recommendation для Track L
  supervisors), §9 Verify verb (`mcp-read-server
  --help` minimum + Track K smoke harness
  recommendation-only deeper verify), §10
  Relationship to current runtime surface (Tracks
  G/H/I/J/K/L invariants byte-identical, `runtime.py`
  не service manager), §11 Relationship to install
  fast path / deployment boundary / service
  supervision (orthogonal-but-complementary axes
  table), §12 Cross-OS posture (Windows / POSIX
  operator notes), §13 Honest non-goals (11 §9.2
  explicit denials + Track M scope discipline), §14
  Cross-references (Track M Step 1/2/3 docs + Track
  J/L recipes + Track K harness + install fast path).
- `pyproject.toml` — single narrow flip:
  `[tool.hatch.build.targets.wheel]` comment block
  заменён на 16-строчный pointer на recipe + mirroring
  §9.2/§9.3 denial discipline; `packages = []`
  flipped to ровно 11 src-layout package paths из
  contract §5.2 verbatim (`apps/mcp-read-server/src/
  mcp_read_server`, `apps/mcp-write-server/src/
  mcp_write_server`, `apps/mcp-intelligence-server/
  src/mcp_intelligence_server`, `apps/platform/src/
  onec_platform`, `packages/mcp-common/src/
  mcp_common`, `packages/onec-process-runner/src/
  onec_process_runner`, `packages/onec-policy-engine/
  src/onec_policy_engine`, `packages/onec-audit/src/
  onec_audit`, `packages/onec-health/src/onec_health`,
  `packages/onec-troubleshooting/src/
  onec_troubleshooting`, `packages/onec-config/src/
  onec_config`). Net +7 LOC. Никаких изменений в
  `[build-system]`, `[project]`, `[project.scripts]`
  (три entries locked), `[tool.ruff]`,
  `[tool.pytest.ini_options]`. Никаких новых
  dependencies / optional-dependencies / classifiers /
  keywords / urls / `MANIFEST.in` / `setup.py` /
  `setup.cfg`.

Optional B1 build-buildability proof: на control host
с operator-side prerequisite `pip install build`,
`python -m build` производит
`dist/1c_agent_platform-<VERSION>-py3-none-any.whl`
(`py3-none-any` platform tag) содержащий ровно 11
package-roots + `1c_agent_platform-<VERSION>.dist-info/`
metadata directory. Никаких credentials, `.env`, real
ProductConfig JSON, Track J/L recipe content, `docs/`
/ `examples/` / `scripts/` / `.git/` / CI artefacts
не входят в wheel (excluded by construction
hatchling-ом + §5.3 discipline).

**Что Track M даёт.** Operator теперь имеет:

- Один **buildable pure-Python wheel** как supported
  artefact class — `1c_agent_platform-0.5.2-py3-none-any.whl`
  (после Step 6 PATCH bump; см. ниже).
- **Five lifecycle verbs** documented end-to-end в
  одном recipe: `build` (`python -m build`) →
  `install` (`pip install <WHEEL_PATH>`) → `uninstall`
  (`pip uninstall 1c-agent-platform`) → `upgrade`
  (`pip install --upgrade <NEW_WHEEL_PATH>`) → `verify`
  (`mcp-read-server --help`).
- **Exact wheel-contents declaration** — 11 src-layout
  Python packages + три locked console-script
  entrypoints; **exact wheel-non-contents declaration**
  — no credentials, no `.env`, no real ProductConfig
  JSON, no Track L systemd template, no Track J recipe
  content, no `docs/` / `examples/` / `scripts/`
  content, no `.git/`, no CI configuration.
- **Cross-OS posture** — wheel installs identically на
  Linux / macOS / Windows; only requirement — Python
  3.11+; cross-OS specifics (`py -m build` на Windows,
  `python -m venv` на POSIX) documented как operator-
  side choices.
- **Orthogonal-but-complementary framing** to
  Track B/I install fast path (config materialiser),
  Track J deployment-boundary recipe (reverse-proxy /
  TLS termination), и Track L service-supervision
  recipe + systemd template (cross-OS supervisors).
  Все три axes сохраняют свои existing recipes и
  contracts byte-identical после Track M closure;
  Track M добавил четвёртую axis (Python code
  delivery) без redesign первых трёх.

**Q7 = PATCH** (`0.5.1 → 0.5.2`). Защита решения:

- **Defect-class declared-but-non-functional surface.**
  `[project.scripts]` console entries
  (`mcp-read-server` / `mcp-write-server` /
  `mcp-intelligence-server`) декларировались с
  Track G (`0.4.0`), но `pip install <wheel>` flow
  был non-functional, потому что
  `[tool.hatch.build.targets.wheel] packages = []`
  делал `python -m build` бесполезным per Track C /
  Step 3 honest constraint. Step 4 declarative flip
  восстанавливает functionality already-declared
  surface — внешний pip-consumer теперь получает
  installable binaries из `pip install <WHEEL_PATH>`
  именно так, как было обещано declared surface.
- **Track I PATCH precedent applies directly.** Track
  I имел `+15 LOC` production code (`installer.py:
  _config_to_dict`) + previously-broken installer
  round-trip; declared surface стал работать. Track M
  ship'нул `+7 LOC` `pyproject.toml` declarative flip +
  operator recipe; declared `[project.scripts]`
  surface стал работать через `pip install`. Defect
  class идентичен — "declared but broken" →
  "declared and working".
- **SemVer §6 framing.** PATCH = "backward-compatible
  bug fixes". Track M Step 4 — backward-compatible
  defect-class repair already-declared surface; ничего
  removed, ничего renamed, ничего semantically
  изменено в существующем code. Operators using
  `python -m <server>` invocation continue работать
  byte-identical (alternative supported).
- **MINOR rejected by step-map invariant #15.** No
  new declared surface, no new CLI flag, no new MCP
  tool, no new `[project.scripts]` entry, no new
  dependency, no new operator-facing capability
  beyond making existing declarations functional.
  Contract §10.4 explicitly excludes MINOR per same
  reasoning.
- **MAJOR forbidden by track scope.**

Pyproject.toml на Step 6 receives **только** the
`version` field bump `"0.5.1" → "0.5.2"`; everything
else (build-system, project metadata, project.scripts,
tool.ruff, tool.pytest.ini_options, tool.hatch.build.
targets.wheel packages list) byte-identical to Step 4
closure. Никакого добавления `[project.urls]`,
classifiers, keywords, dependencies, optional-
dependencies.

**Closure scope (narrowest honest).** Step 6 touched:
`README.md` (Quickstart blockquote summary flipped от
active → closed; Closed parallel tracks list extended
от двенадцать до тринадцать с Track M entry; Active
parallel track section compressed back к no-active-
track wording; new "Track M detail (закрыт)" section
added above "Track L detail (закрыт)" — этот document);
`PROJECT-STATUS.md` (header rewritten от
"Track M / Step 1 in progress" к "no active step +
Track M fully closed под `0.5.2`"; per-step closure
sections для Step 2 / Step 3 / Step 4 / Step 5 / Step
6 inserted после existing Step 1 section);
`CHANGELOG.md` (new top section `## 0.5.2 — Parallel
Track M — Packaging Ecosystem and Distribution
Boundary` за PATCH bump narrative); `pyproject.toml`
(`version = "0.5.1"` → `version = "0.5.2"` only —
никаких других изменений). **NOT touched на Step 6:**
`SECURITY.md`; `docs/release-handoff.md` (Step 5 уже
выровнял); `apps/platform/README.md`;
`docs/operators/packaging/distribution-boundary.md`
(Step 4 deliverable immutable); `docs/operators/
deployment-boundary.md` (Track J artefact);
`docs/operators/service/service-supervision.md` и
`mcp-server.service` (Track L artefacts); `scripts/
release/README.md` (Step 5 уже выровнял); `scripts/
dev/README.md` (Step 5 уже выровнял); Track M Step
1/2/3 architecture docs (frozen anchors);
`LICENSE`; manuals (`docs/operator-manual.md`,
`administrator-manual.md`, `developer-manual.md`,
`runbooks.md`); production code (`apps/*/src/`,
`packages/*/src/`); все остальные `scripts/*` files;
`examples/`.

**Verify-release.** GREEN на 8 checks pre-commit
(`-AllowDirtyTree`) и post-commit (clean tree);
selfcheck registries `read=15 / write=25 /
intelligence=16` без drift'а; никаких реальных
credentials в closure commit'е; никаких 1cv8.exe
runs; никакого remote push.

**Track M closure итог.** Тринадцать post-phase
parallel track'ов (A, B, C, D, E, F, G, H, I, J, K,
L, M) полностью закрыты. Phase 7 как линейная фаза не
запланирована. Открытие следующего параллельного
трека — отдельное operator decision. **Recommended-
next-track candidates (recommendation only, без
автоматического открытия):** TLS-in-process / mTLS
expansion (отдельный enterprise-grade identity
track); полный packaging ecosystem track (`.msi` /
`.deb` / `.rpm` / `.dmg` / `.pkg` / `.snap` /
`.flatpak` / GUI installer / wizard / signed
distribution chain / PyPI publication / multi-
package-manager publication — Track M sticks к
одному narrow buildable-wheel slice, broader
packaging ecosystem остаётся отдельной potential
track-territory); multi-version 1С matrix expansion
(post-Track-E follow-up); полный rollback / AST work
(post-Track-F / post-Track-A follow-ups); полный
observability stack track (OpenTelemetry / Prometheus
/ log aggregation); web UI / dashboard frontend
track; in-repo daemon framework / pywin32 service
wrapper / launchd plist artefacts (cross-OS
implementation slices для Track L coverage
extension); editable-install / workspace-discovery
dev-time tooling track (out of Track M scope —
Track M ship'нул deploy-time `pip install` flow,
не dev-time editable). Эти кандидаты — recommendation
only, не auto-opened.

## Track L detail (закрыт)

## Track L detail (закрыт)

**Цель Track L** была — закрыть следующий честный
эксплуатационный gap: у продукта уже были рабочие
MCP entrypoints (Track G), HTTP/stdio transports
(Tracks G/H), bearer auth (Track H), installer
integrity (Track I), deployment-boundary recipe
(Track J) и real MCP client smoke proof (Track K),
но не было взрослой service-supervision story. В
репозитории на момент открытия Track L (commit
`0e40056`) не было ни одного `systemd` unit-файла,
`launchd` plist'а, Windows Service registration
helper'а; не было PID-file handling; не было formal
stop / start / restart / status / logs operator
vocabulary для MCP-серверов как long-lived services;
не было supervisor wrapper'а; не было `Restart=` /
`RestartPolicy` shape ни в одном файле репо.
Существующие launch surfaces были недостаточны
(`scripts/dev/launch.ps1` foreground-only dev
convenience; `scripts/release/install.ps1`
материализует config но не регистрирует сервис; три
`python -m mcp_<server>` entrypoint'а блокируют
foreground invoking shell). Step 2 audit
формализовал десять конкретных absences и нашёл
ключевую adjacent-but-orthogonal находку:
`apps/platform/src/onec_platform/runtime.py`
(Phase 5 / Step 3 + Phase 6 / Step 6) — in-process
supervisor для product-layer subprocesses, **не**
для MCP-серверов; его module docstring (lines
21–31) explicitly: «not a daemon manager / service
manager (no Windows Service / systemd unit
registration on this step)», «does NOT start MCP
transports inside the three servers». Track L
закрыл supervision concern **снаружи** platform
process tree, на OS layer.

**Что Track L явно НЕ решает.** Production code
changes; `runtime.py` service manager extension
(plan §12.Q1 option C explicitly rejected; recipe
§4.3 explains why); packaging ecosystem (`.msi` /
`.deb` / signed distribution / GUI installer /
wizard / PyPI publication / wheel publication
beyond `[project.scripts]`); Windows Service
implementation in repo (no NSSM install script
shipped, no pywin32 wrapper class, no PowerShell
service-install wrapper); launchd plist artefact
shipped (macOS prose-only); hot reload; zero-
downtime restart; clustering / HA / load-balancing
/ orchestration platforms (Kubernetes / Compose-
with-replicas / Nomad / Consul / etcd / Zookeeper);
enterprise identity stack (SSO / SAML / OIDC /
SCIM / RBAC / ABAC / multi-tenant); web UI /
dashboard frontend; full observability stack
(OpenTelemetry / Jaeger / Prometheus / OpenMetrics /
log aggregation / distributed tracing); new MCP
tools; registry changes; deployment-boundary
redesign (Track J §13 / §6 / §7 / §8 carry-forward
unchanged); `/healthz` endpoint (Track J §8 defer
preserved); standalone `apps/platform` daemon
entrypoint; automatic update / OTA / self-upgrade;
rollback / AST / multi-version 1С matrix expansion;
1cv8 work; "service supervision solved forever" /
"all OS families supported" / "production-ready
service supervision" / "clustered HA" / "zero-
downtime restart" / "hostile-network-ready service
exposure" claim — recipe и template covers **только**
the narrow one-OS-family implementation slice
(systemd/Linux) plus cross-OS prose для Windows
(NSSM) и macOS (launchd); broader matrices remain
recommended-only.

**Step 4 PATH B (narrow docs + declarative
template).** Step 3 contract pinned **PATH B**: ровно
два новых файла под `docs/operators/service/`.
PATH A (docs-only) explicitly rejected because Step
2 audit "zero systemd unit files at HEAD `d58c8d9`"
cannot be closed honestly by prose alone — prose
без committed unit-file leaves operators re-inventing
unit-file structure themselves. PATH C (docs +
template + wrapper script under `scripts/release/`)
explicitly rejected because POSIX operators don't
use PowerShell wrappers, and a separate `.sh`
wrapper becomes a maintenance liability for marginal
benefit (`systemctl enable <UNIT>` is already a
single operator-visible command). Step 4 ship'нул
два файла:

- [`docs/operators/service/service-supervision.md`](docs/operators/service/service-supervision.md)
  — 972-line operator-facing recipe (under contract
  §8.5 ≤1200 soft / ≤1500 hard caps). 15 top-level
  sections: §1 Purpose с explicit denial list, §2
  Supported closure target (Linux/systemd
  implementation-covered + Windows/macOS prose-only),
  §3 Preconditions, §4 Service model (§4.2 Type=simple
  defence + §4.3 `runtime.py` non-extension
  explanation + §4.4 signal handling), §5 Start
  (one-time install + `systemctl start`), §6 Stop
  (`KillSignal=SIGINT` re-routes systemd's service-
  stop в существующий `KeyboardInterrupt` graceful
  path в `_stdio_transport.py:208` /
  `_network_transport.py:618-624` без production
  code change), §7 Restart (stop-then-start; not hot
  reload), §8 Status (`systemctl status` /
  `systemctl show` / `systemctl is-enabled`), §9
  Logs (`journalctl -u <UNIT_NAME>` follow / time-
  window / priority filter), §10 Environment / token
  configuration с full 17-placeholder vocabulary
  table + Track H `--auth-token-env` / Track D
  `${ENV:NAME}` cross-references, §11 Reverse-proxy /
  TLS boundary reminder (Track H / Track J carry-
  forward), §12 Cross-OS notes для Windows (NSSM
  prose) и macOS (launchd prose) с explicit gap-
  naming, §13 Honest non-goals в 7 subcategories +
  §13.8 eleven forbidden maturity-claim phrases,
  §14 Cross-references, §15 Honest summary.
- [`docs/operators/service/mcp-server.service`](docs/operators/service/mcp-server.service)
  — 76-line declarative systemd unit-file template
  (under contract §8.5 ≤80-line hard cap).
  `[Unit]` / `[Service]` / `[Install]` sections;
  `Type=simple`; placeholders exclusive (`<USER>`,
  `<GROUP>`, `<WORKING_DIR>`, `<ENV_FILE_PATH>`,
  `<PYTHONPATH>`, `<PYTHON_BIN>`,
  `<MCP_SERVER_MODULE>`, `<TRANSPORT>`,
  `<CONFIG_PATH>`, `<HOST>`, `<PORT>`,
  `<MCP_TOKEN_VARNAME>`); RECOMMENDED defaults inline
  (`Restart=on-failure`, `RestartSec=5s`,
  `StartLimitBurst=5`, `StartLimitIntervalSec=600s`,
  `KillSignal=SIGINT`, `KillMode=mixed`,
  `TimeoutStopSec=15s`).

**Шесть meaningful commit'ов в `main`.** Production
code не правился ни в одном из шести Track L шагов.
Runtime preserved byte-identical от Track K closure
state (`0e40056`).

- `e713f8e` Step 1 — planning (два planning-документа
  в `docs/architecture/`: plan + step-map; PATH A/B/C
  openness explicitly preserved до Step 3 contract);
- `d58c8d9` Step 2 — descriptive baseline audit
  (один новый descriptive документ
  [`docs/architecture/track-l-service-supervision-and-os-service-registration-baseline-audit.md`](docs/architecture/track-l-service-supervision-and-os-service-registration-baseline-audit.md);
  inventory of existing launch surfaces + signal-
  handling shape + Phase 6 `runtime.py` adjacent-
  but-orthogonal finding + 10 enumerated absences +
  Q1–Q6 directional resolutions + 14-item Step 3
  handoff list);
- `76342a5` Step 3 — normative contract (один новый
  normative документ
  [`docs/architecture/track-l-service-supervision-and-os-service-registration-contract.md`](docs/architecture/track-l-service-supervision-and-os-service-registration-contract.md);
  14 sections, RFC 2119 MUST/SHOULD/MAY language;
  pinned **PATH B**; pinned systemd-first; pinned
  all five lifecycle verbs mandatory; pinned no
  production code change; pinned `runtime.py` byte-
  identical NOT extended; pinned exhaustive
  forbidden file surface; pinned 22-check Step 4
  verification protocol);
- `efb4ea1` Step 4 — narrow PATH B implementation
  (два новых файла под `docs/operators/service/`:
  recipe 972 lines + systemd template 76 lines);
- `82345b4` Step 5 — operator docs and service-
  supervision alignment (3 modified files: README
  Quickstart paragraph + Active parallel track
  section refreshed to reflect Steps 1–4 closed and
  Step 5 active — Track L still framed as **active**;
  `docs/release-handoff.md` "What is in this
  handoff" list extended with the Track L recipe
  bullet, "What is NOT in this handoff" line
  rewritten, two "Known limitations" bullets
  rewritten, "Where to read deeper" extended;
  SECURITY.md / `apps/platform/README.md` /
  `scripts/dev/README.md` / manuals not touched per
  Step 3 contract default — no factual drift);
- closure commit Step 6 фиксирует обновлённые
  README / PROJECT-STATUS / CHANGELOG. Никакого
  `pyproject.toml` change.

**Recipe + template as operator-runnable artefacts.**
Together the two Step 4 files take an operator on
Linux from "I can run an MCP server in a terminal"
to "the MCP server is supervised by systemd,
survives reboots, responds to start / stop /
restart / status / logs, and logs to journald" —
without modifying any production code,
`pyproject.toml`, or any existing `scripts/*` file.
Operators on Windows and macOS apply the §12
prose to NSSM and launchd with operator-side
validation — no `.plist` and no NSSM install
script ship in repo. Closure-gate target =
systemd/Linux; cross-OS = recommended-only.

**No enterprise-ready / hostile-network-ready /
all-OS-supported claim.** Платформа после Track L —
**trusted-internal-network HTTP MCP listener with
static bearer authentication, fronted by an
operator-owned reverse proxy that terminates TLS,
plus a stdio transport for local trusted subprocess
invocation, with externally-replayable client-
integration proof (Track K) and a narrow operator-
facing service-supervision recipe + declarative
systemd unit template (Track L) covering one OS
family end-to-end with cross-OS prose for two
others**. Track L formalize'ил **only the process-
lifecycle posture** for one implementation OS
family; broader matrices (Windows Service /
launchd / clustered HA / zero-downtime restart /
hostile-internet ready supervision) — **explicitly
out of scope** и остаются recommended-only.

**Q7 = NO-BUMP.** Final SemVer decision для Track L:
no version bump. Track L закрывается под existing
`0.5.1` (Track I closure bump, preserved через
Track J и Track K NO-BUMP closures). Защита решения:
(1) production code не правился — `apps/*/src/`,
`packages/*/src/`, `_network_transport.py`,
`_stdio_transport.py`, `installer.py`, `runtime.py`,
`process_control.py`, `runtime_logs.py`, `models.py`
byte-identical от Track K closure state; (2) ноль
defect-class fixes — Step 2 audit explicitly
показал, что foreground-blocking shape MCP server
entrypoints **уже** correct для `Type=simple`
systemd unit; Track L не fix'ил bug, а добавил
operator-runnable documentation + declarative
template для уже-существующего behaviour; (3) ноль
new external capability для ordinary product
consumers — recipe и template живут под
`docs/operators/service/`, симметрично Track J
recipe; не в `[project.scripts]`; не importable
от external consumers; не часть pip-install
surface; не запускаются automatically install
fast-path'ом; (4) ноль new public API surface —
no new public types, functions, imports, `__all__`
exports, `[project.scripts]` entries,
`ProductConfig` schema fields, CLI flags на
existing servers, или HTTP endpoints; (5) SemVer
§6 не оправдывает PATCH — PATCH = "backward-
compatible bug fixes", Track L не fix'ил никакого
bug; (6) Track I PATCH precedent не переносится —
Track I имел `+15 LOC` production code И
previously-broken installer round-trip (silent
data loss в `installer.py:_config_to_dict`); Track
L не имеет ни того, ни другого, и diff'у Track L —
ноль production LOC; (7) Track J NO-BUMP precedent
applies directly — Track J тоже закрылся без
bump'а под existing `0.5.1`, с docs + один
operator-facing artefact (recipe). Track L следует
same pattern'у (docs + один operator-facing recipe
+ один declarative template); (8) Track K NO-BUMP
precedent applies directly — Track K тоже закрылся
без bump'а под existing `0.5.1`, с docs + один
operator-runnable diagnostic artefact (harness).
Track L matches that pattern as well; (9) Track
A / B / C / E precedent applies — те docs-heavy
треки тоже закрылись без separate version bumps в
CHANGELOG.md; (10) Step 1 plan §12.Q7 + Step 3
contract §10.4 + §14 explicitly authorize NO-BUMP
if Step 4 не ship'нет defect-class fix observable
by end-users и не вводит new CLI flag — оба
условия выполнены; default expectation NO-BUMP
явно pinned в Track L planning + contract.

**Registries invariant.** `read=15 / write=25 /
intelligence=16` carried through all six Track L
steps без drift'а. Selfcheck `selfcheck_status=ok`
на closure verify-release. Никаких новых MCP
tools.

**No 1cv8.exe runs.** Track L работал на process-
supervision layer, не на 1cv8 binary surface.
Никаких реальных credentials в repo / docs /
commit messages: recipe и template используют
abstract placeholders only (`<USER>`, `<GROUP>`,
`<HOST>`, `<PORT>`, `<UNIT_NAME>`,
`<SERVICE_NAME>`, `<LOG_PATH>`, `<VARNAME>`,
`<MCP_TOKEN_VARNAME>`, `<PYTHONPATH>`,
`<WORKING_DIR>`, `<ENV_FILE_PATH>`, `<PYTHON_BIN>`,
`<MCP_SERVER_MODULE>`, `<TRANSPORT>`,
`<CONFIG_PATH>`).

**Remote push — operator action, не часть трека.**
GitHub push никогда не делался автоматически в
Track L commit'ах; это остаётся отдельным
operator decision. Все шесть Track L commit'ов
локальны до явного push'а оператором.

**Track L closure summary.** Track L закрыт как
documented status. Двенадцатый post-phase parallel
track. Вместе с Tracks A/B/C/D/E/F/G/H/I/J/K —
двенадцать закрытых post-phase parallel track'ов.
Phase 7 как линейная фаза не запланирована.

Документы и artefacts трека:
[`docs/architecture/track-l-service-supervision-and-os-service-registration-plan.md`](docs/architecture/track-l-service-supervision-and-os-service-registration-plan.md),
[`docs/architecture/track-l-service-supervision-and-os-service-registration-step-map.md`](docs/architecture/track-l-service-supervision-and-os-service-registration-step-map.md),
[`docs/architecture/track-l-service-supervision-and-os-service-registration-baseline-audit.md`](docs/architecture/track-l-service-supervision-and-os-service-registration-baseline-audit.md),
[`docs/architecture/track-l-service-supervision-and-os-service-registration-contract.md`](docs/architecture/track-l-service-supervision-and-os-service-registration-contract.md),
[`docs/operators/service/service-supervision.md`](docs/operators/service/service-supervision.md),
[`docs/operators/service/mcp-server.service`](docs/operators/service/mcp-server.service).


## Track K detail (закрыт)

**Цель Track K** была — закрыть один из последних
честных gaps проекта, который был explicitly flagged
в closure narrative каждого предыдущего MCP-transport
трека (Tracks G / H / I / J): отсутствие real MCP-
client-facing end-to-end proof для already-existing
stdio/HTTP transport surfaces. Проект имеет stdlib-
level smoke (`scripts/dev/selfcheck.py` импортирует
каждый internal package и печатает registry counts)
и repo-level verify (`scripts/release/verify-release.ps1`
— восемь release-facing invariants), но ни один из
них не speaks MCP protocol externally к server
processes и не валидирует `initialize` / `tools/list`
/ `tools/call` envelope shapes против external
client. Track K formalize'ил эту gap как disciplined
six-step deliverable: planning → audit → contract →
narrow implementation → docs alignment → closure.

**Что Track K явно НЕ решает.** New transport family
(no WebSocket / SSE / TCP / Unix-socket / named-pipe
/ TLS-in-process / mTLS — Track H §13.1 / Track J
§5 carry-forward), auth-scheme redesign (no JWT /
OAuth / OIDC / SAML / SCIM / RBAC / ABAC /
per-tenant / multi-tenant identity stack), deployment-
boundary redesign (Track J §13 / §6 / §7 / §8
carry-forward unchanged), hostile-internet-ready
exposure stack, WAF / IDS / rate-limit / DDoS
protection / anomaly detection, observability stack
(OpenTelemetry / Jaeger / Prometheus / OpenMetrics /
log aggregation / distributed tracing), service
supervisor (systemd / Windows Service / launchd /
hot reload / restart watcher / auto-update), packaging
ecosystem (`.msi` / `.deb` / signed distribution /
GUI installer / wizard / PyPI publication / wheel
publication beyond `[project.scripts]`), web UI /
dashboard frontend, standalone `apps/platform`
entrypoint, новые MCP tools (registry invariant
preserved), registry changes, 1cv8 work, multi-version
1С matrix expansion (orthogonal — Track E follow-up),
rollback / AST work (orthogonal — Track F / Track A
follow-ups), `/healthz` endpoint, real-MCP-client-
against-hostile-internet proof, **"client integration
solved forever" / "all clients supported" /
"production-ready client compatibility" / "interop
fully proven" claim** — harness gate exercises
**только** the narrow minimum scenario против одного
primary closure-gate target (`mcp-read-server`) с
двумя spot-checks, не all-clients-supported matrix.

**Step 4 PATH B (narrow harness).** Step 3 contract
pinned **PATH B**: ровно один новый stand-alone
stdlib-only harness файл под `scripts/dev/`. PATH A
(docs-only) rejected because Track K's gap is
*evidence-of-runtime-behaviour* and prose cannot
supply it. PATH C (hybrid) rejected as scope creep
without corresponding closure-strength benefit.
Step 4 ship'нул single new file
[`scripts/dev/mcp_client_smoke.py`](scripts/dev/mcp_client_smoke.py)
(341 LOC, stdlib-only, под contract §10.6 ≤400
hard cap). CLI: `--server {read,write,intelligence}`
default `read`; `--transport {stdio,http,both}`
default `both`. Builds own PYTHONPATH (mirrors
`bootstrap_paths.ps1`'s 11 src paths); launches MCP
server via `subprocess.Popen([sys.executable, "-m",
<module>, ...])`; speaks JSON-RPC 2.0 over
stdin/stdout (stdio path) или `POST /mcp` с bearer
auth (HTTP path); asserts envelope shape for
`initialize` (`protocolVersion == "2024-11-05"` +
`serverInfo` + `capabilities.tools`), `tools/list`
(non-empty array + per-entry `name` / `description`
/ `inputSchema` shape), и one read-only `tools/call`
(well-shaped `result` или `error` envelope).
Ephemeral port via `socket.bind(("127.0.0.1", 0))`;
synthetic token via `secrets.token_urlsafe(32)`
exported into child env via `os.environ[<VARNAME>]`
+ `--auth-token-env`; token value **never** printed
at any verbosity level. Clean subprocess shutdown
(close-stdin → terminate → kill-on-timeout
escalation). Final summary `OK (server=... transport=...)`
on success.

**HTTP missing-Authorization probe.** Дополнительный
failure-equivalence probe для HTTP path: harness
делает `POST /mcp` без `Authorization` header и
asserts три факта одновременно — HTTP `401` + header
`WWW-Authenticate: Bearer realm="mcp"` + JSON-RPC
envelope с `error.code == -32001`. Это externally
проверяет fail-closed bearer-auth path, который
Track H Step 4 ship'нул и который раньше
exercised только в-процесс через unit-shape
assertions.

**Шесть meaningful commit'ов в `main`.** Production
code не правился ни в одном из шести Track K шагов.
Runtime preserved byte-identical от Track J closure
state (`dd86261`).

- `02783df` Step 1 — planning (два planning-документа
  в `docs/architecture/`: plan + step-map; PATH A/B/C
  openness explicitly preserved до Step 3 contract);
- `62069a5` Step 2 — descriptive baseline audit
  (один новый descriptive документ
  [`docs/architecture/track-k-real-mcp-client-integration-test-baseline-audit.md`](docs/architecture/track-k-real-mcp-client-integration-test-baseline-audit.md);
  inventory existing client-integration approximations
  + 4-class breakdown + Q1–Q6 directional resolutions
  + 14-item Step 3 handoff list);
- `ead4a0e` Step 3 — normative contract
  (один новый normative документ
  [`docs/architecture/track-k-real-mcp-client-integration-test-contract.md`](docs/architecture/track-k-real-mcp-client-integration-test-contract.md);
  15 sections, RFC 2119 MUST/SHOULD/MAY language;
  pinned **PATH B**; pinned closure-gate scenario;
  pinned synthetic-token discipline; pinned 22-check
  Step 4 verification harness);
- `979eced` Step 4 — narrow MCP client smoke harness
  ([`scripts/dev/mcp_client_smoke.py`](scripts/dev/mcp_client_smoke.py),
  341 LOC stdlib-only); verified runnable —
  `python scripts/dev/mcp_client_smoke.py --server
  read --transport both` → exit 0 + raw `OK` line +
  no orphan processes + token value never printed;
  spot-checks `--server write --transport stdio`
  и `--server intelligence --transport http` also
  passed;
- `ef9c6c7` Step 5 — operator docs and client-
  integration alignment (3 files: `README.md`
  Quickstart paragraph + Active parallel track
  section refreshed to reflect Steps 1–4 closed;
  `docs/release-handoff.md` "What is in this handoff"
  + "Where to read deeper" lists referenced new
  harness; `scripts/dev/README.md` "Содержимое"
  section listed harness alongside existing dev
  scripts);
- closure commit Step 6 фиксирует обновлённые
  README / PROJECT-STATUS / CHANGELOG. Никакого
  `pyproject.toml` change.

**Harness как operator-runnable diagnostic tooling.**
`scripts/dev/mcp_client_smoke.py` живёт в той же
категории, что и `scripts/dev/selfcheck.py`: stdlib-
only Python file, который operator может запустить
вручную для replayable proof существующего behaviour.
Это **не** часть production runtime, **не** в
`[project.scripts]`, **не** importable от внешних
consumers, **не** часть install fast path. Pip-
installing проект (если он когда-нибудь wheel-build
получит) не expose'ит harness. Closure-gate target —
`mcp-read-server` over both transports; harness
работает против всех трёх servers, но Track K
acceptance bound только к read-server primary
target плюс two spot-checks.

**No enterprise-ready / hostile-network-ready /
all-clients-supported claim.** Платформа после
Track K — **trusted-internal-network HTTP MCP
listener with static bearer authentication, fronted
by an operator-owned reverse proxy that terminates
TLS, plus a stdio transport for local trusted
subprocess invocation, with externally-replayable
proof that both transports honour the MCP
2024-11-05 envelope shapes for initialize /
tools/list / one read-only tools/call against the
read-server primary target**. Track K formalize'ил
**only the replayability of that single closure-
gate scenario**; broader matrices (third-party real
MCP clients like Claude Desktop, all servers /
write-server mutating tools / HTTP+stdio matrix
under all permutations, multi-version 1С matrix,
hostile-internet posture) — **explicitly out of
scope** и остаются recommended-only.

**Q7 = NO-BUMP.** Final SemVer decision для Track K:
no version bump. Track K закрывается под existing
`0.5.1` (Track I closure bump, preserved через
Track J NO-BUMP closure). Защита решения:
(1) production code не правился — `apps/*/src/`,
`packages/*/src/`, `_network_transport.py`,
`_stdio_transport.py`, `installer.py` byte-identical
от Track J closure state; (2) ноль defect-class
fixes — Step 2 audit explicitly показал, что
runtime internally consistent с plausible MCP
interpretation; Track K не fix'ил bug, а добавил
replayable external proof уже-существующего
behaviour; (3) ноль new external capability для
ordinary product consumers — harness живёт под
`scripts/dev/`, симметрично `selfcheck.py`, не в
`[project.scripts]`, не importable, не часть pip-
install surface; (4) ноль new public API surface
(no new public types, functions, imports, `__all__`
exports, `[project.scripts]` entries, `ProductConfig`
schema fields, или CLI flags на existing servers);
(5) SemVer §6 не оправдывает PATCH — PATCH =
"backward-compatible bug fixes", Track K не fix'ил
никакого bug; (6) Track I PATCH precedent не
переносится — Track I имел `+15 LOC` production
code И previously-broken installer round-trip
(silent data loss в `installer.py:_config_to_dict`);
Track K не имеет ни того, ни другого, и diff'у
Track K — 0 production LOC; (7) Track J NO-BUMP
precedent applies directly — Track J тоже закрылся
без bump'а под existing 0.5.1, с docs + один
operator-facing artefact; Track K следует тому же
паттерну (docs + один operator-runnable diagnostic
artefact); (8) Track A / B / C / E precedent
applies — те docs-heavy треки тоже закрылись без
separate version bumps в CHANGELOG.md; (9) Step 1
plan §12 Q7 + Step 3 contract §3.Q7 / §11.5
explicitly authorize NO-BUMP if Step 4 не ship'нет
defect-class fix observable by end-users — оба
условия выполнены; default expectation NO-BUMP
явно pinned в Track K planning.

**Registries invariant.** `read=15 / write=25 /
intelligence=16` carried through all six Track K
steps без drift'а. Selfcheck `selfcheck_status=ok`
на closure verify-release. Никаких новых MCP tools.

**No 1cv8.exe runs.** Track K работал на MCP client
/ transport layer, не на 1cv8 binary surface.
Никаких реальных credentials в repo / docs / commit
messages: harness генерирует synthetic bearer token
через `secrets.token_urlsafe(32)` at run time,
экспортит через `os.environ[<VARNAME>]` для server
subprocess только, и never печатает value.

**Remote push — operator action, не часть трека.**
GitHub push никогда не делался автоматически в
Track K commit'ах; это остаётся отдельным operator
decision. Все шесть Track K commit'ов локальны до
явного push'а оператором.

**Track K closure summary.** Track K закрыт как
documented status. Одиннадцатый post-phase parallel
track. Вместе с Tracks A/B/C/D/E/F/G/H/I/J —
одиннадцать закрытых post-phase parallel track'ов.
Phase 7 как линейная фаза не запланирована.

Документы и harness трека:
[`docs/architecture/track-k-real-mcp-client-integration-test-plan.md`](docs/architecture/track-k-real-mcp-client-integration-test-plan.md),
[`docs/architecture/track-k-real-mcp-client-integration-test-step-map.md`](docs/architecture/track-k-real-mcp-client-integration-test-step-map.md),
[`docs/architecture/track-k-real-mcp-client-integration-test-baseline-audit.md`](docs/architecture/track-k-real-mcp-client-integration-test-baseline-audit.md),
[`docs/architecture/track-k-real-mcp-client-integration-test-contract.md`](docs/architecture/track-k-real-mcp-client-integration-test-contract.md),
[`scripts/dev/mcp_client_smoke.py`](scripts/dev/mcp_client_smoke.py).

## Track J detail (закрыт)

**Цель Track J** была — формализовать "trusted-network
behind operator-owned reverse proxy" general-policy
statement из Track H Step 3 contract §13 в
operator-facing single-source-of-truth deployment-
boundary recipe. Step 2 audit подтвердил, что runtime
**уже** enforce'ит ключевые deployment-boundary
invariants (`_parse_bind` HOST:PORT shape + range +
`socket.gethostbyname` validation; no default
`--bind`; `_MCPHandler` single-`/mcp`-POST + 1 MiB
cap + bearer auth + failure-equivalence + redaction
discipline; `_serve_http` plain HTTP/1.1 без `ssl`
imports beyond stdlib's indirect pulls; whole-repo
grep showed zero consumption of `X-Forwarded-*` /
`Forwarded` / `X-Real-IP` / `client_ip` / `peer_ip`
для access-control purposes), поэтому dominant gap
был **operator-facing документация**, не runtime
behaviour. Step 3 contract pinned **PATH A docs-only**
for Step 4 (PATH B / PATH C explicitly rejected).
Step 4 ship'нул single ten-section operator-facing
recipe at [`docs/operators/deployment-boundary.md`](docs/operators/deployment-boundary.md):
per-scenario MUST/SHOULD/MAY matrix для трёх
scenarios (loopback / trusted private subnet /
public-facing-through-reverse-proxy), per-scenario
walkthroughs, explicit Forwarded-header
MUST-NOT-consume policy для `X-Forwarded-*` /
`Forwarded` / `X-Real-IP` / `True-Client-IP` /
`CF-Connecting-IP`, `/healthz` non-shipping
rationale + workarounds для strict-2xx-only probers,
два abstract reverse-proxy snippet'а (nginx +
Caddy), восемь operator decision-point Q&A, honest
non-goals.

**Что Track J явно НЕ решает.** In-process TLS /
HTTPS termination (carry-forward Track H §13.1
forbid; никогда не shipped), mTLS / client
certificate authentication (carry-forward §13.3),
hostile-internet-ready exposure stack, full
enterprise identity stack (SSO / SAML / OIDC /
SCIM / RBAC / ABAC / per-tool ACL / per-tenant
isolation / multi-tenant), zero-trust posture,
WAF / IDS / rate-limit / DDoS protection / anomaly
detection, observability stack (OpenTelemetry /
Jaeger / Prometheus / OpenMetrics / log
aggregation / distributed tracing), service
supervisor / systemd unit / Windows Service /
launchd / hot reload / restart watcher /
auto-update, packaging ecosystem (`.msi` / `.deb` /
signed distribution / GUI installer / wizard /
PyPI publication / wheel publication beyond
`[project.scripts]`), web UI / dashboard frontend,
standalone `apps/platform` entrypoint (carry-over
из Tracks G / H / I), `/healthz` / `/readyz` /
`/livez` HTTP endpoint (Step 3 contract §8 deferred
explicitly), `0.0.0.0` runtime warning (deferred —
risk documented в recipe §3 / §4 prose, без code
addition), новые MCP tools (registry invariant
preserved), 1cv8 work, multi-version 1С matrix
expansion, rollback / AST. Эти направления — out
of Track J scope; некоторые могут быть addressed
будущими треками, некоторые остаются на постоянной
основе в "What is NOT in this handoff" surface.

**Step 4 PATH A docs-only.** Production code не
правился ни в одном из шести Track J шагов. Runtime
preserved byte-identical от Track I closure state
(`d408dd2`). Шесть meaningful commit'ов в `main`:

- `e203e43` Step 1 — planning (планирующие документы
  + step-map; PATH A/B/C openness explicitly
  preserved для Step 4);
- `344129c` Step 2 — descriptive baseline audit
  (980-line read-only audit с Q1–Q6 directional
  resolutions + 14-item Step 3 handoff list);
- `4e04771` Step 3 — normative contract (15 sections,
  RFC 2119 MUST/SHOULD/MAY language; pinned PATH A;
  pinned per-scenario matrix; pinned forwarded-header
  MUST-NOT-consume policy; pinned `/healthz` defer;
  pinned 18-check Step 4 verification harness);
- `5c793c1` Step 4 — operator-facing deployment-
  boundary recipe (single new file at
  `docs/operators/deployment-boundary.md`,
  691 lines, ten sections);
- `19e8923` Step 5 — operator docs and deployment-
  boundary alignment (3 files: README.md
  Quickstart + Active parallel track section,
  SECURITY.md "Threat model for HTTP" bullet
  cross-link, `docs/release-handoff.md` "What is in
  this handoff" + "Where to read deeper" lists);
- closure commit Step 6 фиксирует обновлённые
  README / PROJECT-STATUS / CHANGELOG. Никакого
  `pyproject.toml` change.

**Operator-facing deployment recipe existence.** За
шесть шагов Track J ship'нул пять документов под
`docs/`: четыре architecture-документа в
`docs/architecture/track-j-*.md` (planning / step-
map / baseline audit / normative contract) и один
operator-facing recipe в
[`docs/operators/deployment-boundary.md`](docs/operators/deployment-boundary.md).
Recipe — single source of truth для оператора,
который раздаёт `--transport http`. Контракт
([`docs/architecture/track-j-deployment-boundary-contract.md`](docs/architecture/track-j-deployment-boundary-contract.md))
— normative source-of-truth для policy.

**No enterprise-ready / hostile-network-ready
claim.** Платформа после Track J — **trusted-
internal-network HTTP MCP listener with static
bearer authentication, fronted by an operator-owned
reverse proxy that terminates TLS**. Это **не**
hostile-internet ready, **не** enterprise-identity
ready, **не** multi-tenant, **не** load-balanced,
**не** observed, **не** supervised. Track J
formalize'ил **first half** этой фразы; **second
half** Track J не менял.

**Q7 = NO-BUMP.** Final SemVer decision для Track J:
no version bump. Track J закрывается под existing
`0.5.1` (Track I closure bump). Защита решения:
(1) production code не правился — `apps/*/src/`,
`packages/*/src/`, `_network_transport.py`,
`_stdio_transport.py`, `installer.py` byte-identical
от Track I closure state; (2) ноль defect-class
fixes — Step 2 audit explicitly показал, что runtime
уже enforce'ил deployment-boundary invariants;
(3) ноль new external capability — no new endpoint,
no new CLI flag, no new MCP tool, no new auth
scheme, no new transport; Step 3 contract pinned
PATH A specifically чтобы избежать net-new
capability; (4) ноль new public API surface (no new
public types, functions, imports, `__all__` exports,
or `[project.scripts]` entries); (5) SemVer §6 не
оправдывает PATCH — PATCH = "backward-compatible
bug fixes", Track J не fix'ил никакого bug;
(6) Track I PATCH precedent не переносится — Track
I имел `+15 LOC` production code И previously-broken
round-trip; Track J не имеет ни того, ни другого;
(7) Track A / B / C / E precedent — те docs-heavy
треки тоже закрылись без separate version bumps
(они отсутствуют как `## VERSION — Track X`
headings в `CHANGELOG.md`); (8) Step 1 plan §14 и
Step 3 contract §3.7 / §11.5 explicitly authorize
NO-BUMP if Step 6 = closure-doc alignment с no
version-relevant change.

**Registries invariant.** `read=15 / write=25 /
intelligence=16` carried through all six Track J
steps без drift'а. Selfcheck `selfcheck_status=ok`
на closure verify-release. Никаких новых MCP tools.

**Remote push — operator action, не часть трека.**
GitHub push никогда не делался автоматически в
Track J commit'ах; это остаётся отдельным operator
decision. Все шесть Track J commit'ов локальны до
явного push'а оператором.

**Track J closure summary.** Track J закрыт как
documented status. Десятый post-phase parallel
track. Вместе с Tracks A/B/C/D/E/F/G/H/I — десять
закрытых post-phase parallel track'ов. Phase 7 как
линейная фаза не запланирована.

## Track I detail (закрыт)

**Цель Track I** была — закрыть один honest gap, явно
зафиксированный в Track H closure narrative:
`apps/platform/src/onec_platform/installer.py:_config_to_dict`
не emit'ил новый `auth` section, поэтому config round-tripped
через `scripts/release/install.ps1 ... -Confirm` silently
терял declarations `auth.tokens`. Operator получал clean
fail-closed startup ("`--transport http requires
--auth-token-env or auth.tokens in product config`"), что
было не silent insecure success (Track H §10.6 fail-closed
gate работал корректно), но silent configuration data loss,
ломающий declarative round-trip guarantee, на которую
полагаются другие installer paths (existing `enterprise`
block + `runtime.services[*]` Phase 6/Step 6 service-level
fields — оба honored emit-only-when-divergent pattern'ом).
Track I восстановил preservation symmetric к существующему
Phase 6 / Step 8 enterprise-block pattern. Это **не**
redesign `ProductAuthSettings` schema, **не** changes к
`_parse_auth` validation, **не** changes к
`_network_transport.py` auth resolution, **не** introduction
secret storage / vault / KMS / OS keychain, **не** packaging
ecosystem (`.msi` / `.deb` / signed distribution / PyPI
publication / wheel publication beyond existing
`[project.scripts]` declarations), **не** service supervision
(systemd / Windows Service / hot reload / supervisor daemon),
**не** network hardening (TLS-in-process / mTLS / new
transport family), **не** enterprise identity stack
(SSO / OIDC / RBAC / multi-tenant), **не** standalone
`apps/platform` entrypoint, **не** новые MCP tools (registry
invariant `read=15 / write=25 / intelligence=16` carried
through unchanged). Платформа архитектурно осталась при том
же подходе: existing Track G + Track H artefacts (3
`__main__.py` entrypoints, `_stdio_transport.py` helper,
`_network_transport.py` helper, `[project.scripts]` block,
`ProductAuthSettings` dataclass, `_parse_auth` loader,
`_AUTH_ENV_TOKEN_RE` regex, `Authorization` header parsing
+ case-insensitive scheme + `hmac.compare_digest` validation
+ failure-equivalence rule + complete redaction discipline)
preserved byte-identical; Track I ship'ил **только narrow
installer.py extension** (+15 / -0 LOC, single emit branch).
Шесть шагов; production-код Track I правил **только Step 4
commit** и **только** в `installer.py:_config_to_dict`.

- **Step 1 (planning, docs-only, commit `cb79597`)** — два
  planning-документа
  ([`docs/architecture/track-i-installer-auth-round-trip-integrity-plan.md`](docs/architecture/track-i-installer-auth-round-trip-integrity-plan.md),
  [`track-i-...-step-map.md`](docs/architecture/track-i-installer-auth-round-trip-integrity-step-map.md)):
  назначение трека, целевой результат, что закрывает /
  не закрывает Track I, отличия от Tracks A–H, guardrails,
  acceptance criteria, открытые вопросы Q1–Q7. Никакого
  code change.
- **Step 2 (installer round-trip baseline audit, docs-only,
  commit `e7d9973`)** — новый descriptive audit-документ
  [`track-i-installer-auth-round-trip-baseline-audit.md`](docs/architecture/track-i-installer-auth-round-trip-baseline-audit.md)
  (889 lines, 12 sections); per-section `_config_to_dict`
  inventory (9 logical sections); 4-class breakdown
  идентифицировал `auth` как единственный CLASS-3 gap;
  resolved Q1 (`installer.py` only — verified by Phase
  6/Step 6 service-level + Phase 6/Step 8 enterprise
  single-file precedents), Q2 (5 preservation rules с
  file/line anchors), Q3 (11 forbidden sub-rules с Track H
  contract + observed-evidence anchors).
- **Step 3 (auth round-trip preservation contract,
  docs-only, commit `525c611`)** — новый prescriptive
  normative document
  [`track-i-installer-auth-round-trip-contract.md`](docs/architecture/track-i-installer-auth-round-trip-contract.md)
  (843 lines, 118 RFC 2119 keyword usages: 78 MUST, 32
  MUST NOT, 4 SHOULD, 3 MAY, 1 SHALL); 11 sections
  pinning round-trip integrity definition, exact emit-
  branch placement (after `enterprise_block` attach at
  l.314, before `return out`), exact accumulator-and-
  conditional-attach shape, list-copying discipline,
  raw `${ENV:NAME}` byte-identical preservation, no env-
  resolution-at-install-time rule, exact Step 4 allowed/
  forbidden file surfaces, verification protocol (6
  positive checks + 6 negative checks + 4 insufficient-
  verification exclusions + no-real-MCP-client-gate
  carry-over), 15 honest non-goals each followed by "No
  ..." denial clauses, 8-precondition + 11-prohibition
  Step 4 handoff note.
- **Step 4 (narrow installer auth round-trip
  implementation, единственный шаг с production code
  change, commit `d047a6d`)** — 1 file modified, +15/-0
  LOC. Additive emit branch в `installer.py:_config_to_dict`
  между existing `enterprise_block` attach (l.314) и
  `return out`:

  ```python
  auth_block: dict[str, Any] = {}
  if config.auth.tokens:
      auth_block["tokens"] = list(config.auth.tokens)
  if auth_block:
      out["auth"] = auth_block
  ```

  Comment block описывает Track I provenance + raw
  `${ENV:NAME}` preservation rule + resolution boundary
  в `_network_transport.py`. **No new imports** (`Any`
  already imported at l.33 per Step 3 §7.3 default-zero);
  **no edits в existing 8 emit branches** (per §7.1
  byte-identical preservation); **no helper extraction**
  / no refactor / no cleanup churn. Verification: 14/14
  PASS через одноразовый `.tmp_track_i_smoke.py` smoke
  harness (deleted pre-commit) — multi-token round-trip
  preserved с order; single-token round-trip; empty/
  default no-injection across 3 cases; pre-Track-H
  reload defaults to empty; token order positionally
  preserved; raw `${ENV:NAME}` byte-for-byte preserved
  WITHOUT populating os.environ; no env resolution at
  install time (probe value `should-never-appear-in-
  projection` set в os.environ → never appears в
  projected JSON); literal cleartext rejected fail-
  closed by `loader._parse_auth` upstream; end-to-end
  install fast-path executed-mode real-IO round-trip
  preserves `auth.tokens` element-wise.
- **Step 5 (operator docs and installer auth alignment,
  docs-only, commit `2e9e0b8`)** — narrow alignment
  под фактический Step 4 fix state; 3 files +185/-84:
  `SECURITY.md` (single bullet "Known limitation in
  install fast path round-trip" → "Install fast path
  auth round-trip preserved (Track I / Step 4)");
  `docs/release-handoff.md` (2 locations: "What is NOT
  in this handoff" bullet + "Known limitations"
  pointer); `README.md` (Quickstart paragraph + "Active
  parallel track" section enumerating Steps 1-4 closure
  summary). Drift inventory classified 8 candidates: 3
  CLASS-1 (touched), 3 CLASS-2 (apps/platform/README.md
  + scripts/dev/launch.ps1 + scripts/dev/README.md —
  qualitatively still accurate, no gap mention), 2
  CLASS-3 (PROJECT-STATUS.md + CHANGELOG.md — closure
  narrative territory).
- **Step 6 (final integration pass and Track I closure,
  этот closure)** — `pyproject.toml` version bumped
  `0.5.0` → `0.5.1` (Q6 = PATCH; см. ниже); README +
  PROJECT-STATUS + CHANGELOG обновлены под Track I
  closed.

**Q6 resolution = PATCH (NOT MINOR).** Track I — defect-
class round-trip integrity fix, не feature delta:

- Step 4 commit (`d047a6d`) изменил `+15 / -0` LOC в
  одной функции (`installer.py:_config_to_dict`),
  symmetric к существующему Phase 6 / Step 8
  `enterprise_block` pattern, который в `_config_to_dict`
  с момента Phase 6.
- **No new public API surface.** `ProductAuthSettings` и
  `ProductConfig.auth` уже существовали (Track H Step 4 в
  version 0.5.0). Track I добавил zero new public types,
  zero new functions, zero new module imports, zero new
  CLI flags, zero new MCP tools, zero changes to
  `mcp_common/__init__.py` `__all__`, zero changes to
  `[project.scripts]`.
- **No new runtime capability.** Operators using
  `--transport http` уже имели два рабочих пути pre-Track-I:
  declare `auth.tokens` в source config (worked unless
  они round-trip'ят через install fast-path), либо use
  `--auth-token-env` CLI override. Track I closed silent
  data-loss bug в install fast-path materialization,
  который operators обходили. Net-new capability нет;
  есть previously-broken round-trip, который теперь
  работает.
- **SemVer prior precedent comparison.** Track D
  `0.1.0 → 0.2.0` (env-substitution + verify-release Check
  8 — added 50+ LOC of new credential-resolution logic +
  new release-side check). Track F `0.2.0 → 0.3.0`
  (whitelist 2→6 entries — meaningful runtime-reachable
  rollback capability for 4 new tool families). Track G
  `0.3.0 → 0.4.0` (3 new `__main__.py` + 245-LOC
  `_stdio_transport.py` + new `[project.scripts]` block —
  net-new runnable surface). Track H `0.4.0 → 0.5.0`
  (549-LOC `_network_transport.py` + new HTTP/`/mcp`
  endpoint + bearer auth + new CLI flags — net-new
  transport family). Each of D/F/G/H added a recognizable
  new external capability. **Track I does not.** It
  restores integrity of a flow that should have always
  preserved this section.
- **Per Keep-a-Changelog conventions and SemVer §6**, "Bug
  fixes" → PATCH. Track I plan §10 Q6 explicitly framed
  PATCH `0.5.1` как «alternative path только if Step 4
  diff truly tiny and framing honest as defect-fix»; Step
  4 diff был 15 LOC (well within "truly tiny"); fix —
  genuinely defect-class round-trip integrity repair.

После Track I closure фактически работает:

```powershell
# Operator declares config с auth section
.\scripts\release\install.ps1 `
    -ConfigPath input.config.json `
    -OutputConfigPath out.config.json `
    -Confirm
# Materialised out.config.json теперь содержит
# "auth": {"tokens": ["${ENV:MCP_TOKEN}"]}
# byte-identical к source (raw env-substitution form
# preserved as configuration data; no env resolution
# at install time)
```

Что Track I **реально закрыл** (на основе Steps 1–5
deliverables):

- installer auth round-trip integrity — `_config_to_dict`
  теперь preserves `config.auth.tokens` через install
  fast-path materialization round-trip byte-identical к
  source list (operator's declared `${ENV:NAME}` strings
  round-trip как configuration data, не resolved env
  values);
- backward compatibility — pre-Track-H configs (без
  `auth` section) round-trip byte-identical (no implicit
  `"auth": {}` injection); existing 8 emit branches в
  `_config_to_dict` byte-identical; Track H auth/runtime
  surfaces (`ProductAuthSettings`, `ProductConfig.auth`,
  `_parse_auth`, `_AUTH_ENV_TOKEN_RE`,
  `_network_transport.py`, `_stdio_transport.py`, three
  `__main__.py`, `mcp_common/__init__.py` `__all__`)
  byte-identical;
- two new architecture docs (descriptive baseline audit
  + RFC 2119 normative contract) + plan + step-map = 4
  Track I architecture docs;
- aligned operator-facing docs (`SECURITY.md`,
  `docs/release-handoff.md`, `README.md`) — все говорят
  one truth: post-Step-4 fix preserved auth round-trip;
  broader installer / packaging / deployment ecosystem
  limitations carry forward;
- registries invariant `read=15 / write=25 /
  intelligence=16` carried through unchanged;
  `mcp_common` public API export'ы preserved
  byte-identical.

Что Track I **не делает** «installer ecosystem solved»
после closure (honest constraints, никаких скрытых
гэпов):

- никакого full installer ecosystem (`.msi` / `.deb` /
  signed binary distribution / GUI installer / wizard /
  PyPI publication / wheel publication beyond existing
  `[project.scripts]` declarations); Track C wheel-build
  empty constraint preserved;
- никакого secret storage / vault / KMS / HashiCorp Vault
  / AWS Secrets Manager / OS keychain integration;
- никакого env-var resolution at install time (это design
  invariant, не gap — resolution остаётся
  `_network_transport._resolve_env_token` runtime
  boundary);
- никакого Track H auth model changes (bearer / case-
  insensitive scheme / constant-time compare / failure-
  equivalence rule preserved byte-identical);
- никакого new transport / network / TLS / mTLS / OAuth
  / JWT / OIDC / SAML / SCIM / RBAC / multi-tenant /
  sessions / rate limiting / token rotation /
  refresh tokens;
- никакого supervisor daemon / systemd unit / Windows
  Service registration / `launchd` plist / hot reload /
  restart watcher / auto-update / orchestration
  templates / HA / clustering / load balancing;
- никакого web UI / dashboard frontend;
- никакого distributed tracing / observability stack
  (OpenTelemetry / Jaeger / Prometheus / OpenMetrics);
- никакого standalone `apps/platform` entrypoint
  (carry-over out-of-scope from Tracks G/H);
- никаких новых MCP tools (registry invariant
  preserved);
- никаких 1cv8.exe runs ни на одном шаге Track I —
  трек работает на install/materialization layer уровне,
  не на 1cv8 binary surface;
- никакого deployment perimeter беyond Track H trusted-
  network behind operator-owned reverse proxy;
- никакого enterprise-ready / hostile-network-ready
  posture claim;
- никакого real MCP client integration test (Claude
  Desktop, MCP CLI launching server) **не** часть Track
  I closure gate — recommended но не blocker (carry-over
  Track G/H pattern).

Registry-инвариант сохранён точно на всём треке: `read=15
/ write=25 / intelligence=16`, `selfcheck_status=ok`.
Никаких реальных credentials ни в одном из шести Track I
commit'ов (Step 4 smoke harness использовал abstract
`${ENV:MCP_TOKEN_*}` test placeholders + ephemeral non-
secret canary string `"should-never-appear-in-projection"`
inside the deleted harness; nothing committed). Никаких
1cv8.exe runs ни на одном шаге Track I. **GitHub remote
push** не часть Track I — repo готов к выкладке, но
пушить — operator action.

Документы трека:
[`track-i-installer-auth-round-trip-integrity-plan.md`](docs/architecture/track-i-installer-auth-round-trip-integrity-plan.md),
[`track-i-installer-auth-round-trip-integrity-step-map.md`](docs/architecture/track-i-installer-auth-round-trip-integrity-step-map.md),
[`track-i-installer-auth-round-trip-baseline-audit.md`](docs/architecture/track-i-installer-auth-round-trip-baseline-audit.md),
[`track-i-installer-auth-round-trip-contract.md`](docs/architecture/track-i-installer-auth-round-trip-contract.md).

## Track H detail (закрыт)

**Цель Track H** была — ship'ить **второй слой зрелости**
поверх Track G: добавить один network-facing MCP transport
family и один minimum authentication baseline, additive
над existing local stdio surface (Track G `python -m
<server> --transport stdio` остаётся supported byte-
identically). Это **не** universal enterprise deployment
platform, **не** full identity stack (SSO / SAML / OIDC
federation / SCIM / organizational RBAC / multi-tenant
policy), **не** zero-trust mesh (mTLS-everywhere / service
mesh / KMS / vault как mandatory baseline), **не** web UI
/ dashboard frontend, **не** packaging ecosystem (`.msi`
/ `.deb` / signed distribution / PyPI publication / wheel
publication beyond existing `[project.scripts]`
declarations), **не** service management ecosystem
(systemd unit / Windows Service registration / `launchd`
plist / auto-update / HA / clustering / load balancing /
hot reload / supervisor daemon с restart watcher), **не**
standalone `apps/platform` entrypoint (carry-over
out-of-scope from Track G Q6), **не** новые MCP tools
(registry invariant `read=15 / write=25 / intelligence=16`
carried through unchanged). Платформа архитектурно
осталась при том же подходе: existing
`server.py:REGISTERED_TOOLS` registries для всех 3 MCP
servers preserved byte-identical (`list_tools()` /
`get_tool(name)` API без изменений); Track H ship'ил
**дополнительный transport / auth layer поверх** этих
registries, не задевая их; existing Track G artefacts
(3 `__main__.py` entrypoints, `_stdio_transport.py`
helper, `[project.scripts]` block) preserved. Шесть шагов
+ один Step 2 follow-up; production-код Track H правил
**только Step 4 commit** и **только** на explicit allowed
surfaces (1 new private helper + 3 modified
`__main__.py` + 2 modified `apps/platform` files).

- **Step 1 (planning, docs-only, commit `563b27b`)** —
  два planning-документа
  ([`docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md),
  [`track-h-...-step-map.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md)):
  назначение трека, целевой результат, что закрывает /
  не закрывает Track H, отличия от Tracks A–G,
  guardrails, acceptance criteria, открытые вопросы Q1–Q7.
  Никакого code change.
- **Step 2 (transport / auth baseline audit, docs-only,
  commit `3c74564`)** — новый descriptive audit-документ
  [`track-h-transport-and-auth-baseline-audit.md`](docs/architecture/track-h-transport-and-auth-baseline-audit.md)
  (1085 lines, 11 sections): per-server / per-package /
  per-pyproject inventory current state + 4-class
  breakdown (11 reusable / 8 adjacent / 11 missing / 12
  out-of-scope) + read-only evidence (zero hits across 8
  grep categories — HTTP server libs, SSE, WebSocket,
  TCP, TLS, auth, sessions, rate-limit). Resolved Q1
  (HTTP-based MCP transport), Q2 (exactly one transport
  family), Q3 (static bearer token via Authorization
  header, constant-time compare, fail-closed), Q4
  (`ProductConfig.auth.tokens` + Track D `${ENV:NAME}`
  pattern + `--auth-token-env` CLI override).
- **Step 2 follow-up (commit `0628f4c`)** — narrow
  one-file fix removing literal credential-leak-guard
  pattern strings from the audit doc that were
  triggering `verify-release.ps1` Check 7 self-match
  after the doc became tracked. The same self-reference
  hazard is already handled for the script and its
  README via the script's `$excludes` list; the audit
  doc fell into the same trap on tracked-state. Fix
  paraphrased the strings without weakening the audit's
  meaning; touched only `scripts/release/verify-release.ps1`
  was deliberately avoided (that would be Track H docs
  follow-up scope creep).
- **Step 3 (network transport / auth contract, docs-only,
  commit `2e76061`)** — новый prescriptive normative
  document
  [`track-h-network-transport-and-auth-contract.md`](docs/architecture/track-h-network-transport-and-auth-contract.md)
  (1650 lines, 293 RFC 2119 keyword usages: 199 MUST,
  74 MUST NOT, 17 MAY, 2 SHOULD, 1 SHALL). 18 sections:
  purpose / inheritance / network transport contract
  (HTTP/1.1 ThreadingHTTPServer, single `/mcp` endpoint,
  POST only, `application/json`, 1 MiB body cap, SSE
  forbidden in Step 4 baseline) / MCP method coverage
  (same six methods as `_stdio_transport`) / JSON-RPC ↔
  HTTP boundary (per-failure-mode HTTP status + envelope
  pinned) / concurrency / auth (`Authorization: <case-
  insensitive-Bearer> <token>`, `hmac.compare_digest`,
  failure-equivalence rule, complete redaction
  discipline, exhaustive forbidden auth-shape list) /
  config schema / CLI surface / integration boundary /
  backward compatibility / TLS posture (in-process TLS
  forbidden; operator's reverse proxy responsibility) /
  pyproject posture / Step 4 implementation surface
  (allowed/forbidden file lists) / verification protocol
  / honest non-goals / Step 4 handoff note.
- **Step 4 (narrow HTTP transport and bearer auth boundary,
  единственный шаг Track H с production code change,
  commit `5814041`)** — PATH A. Ship'нуто 5 файлов
  (+877/-35; 1 new + 4 modified):
  - `packages/mcp-common/src/mcp_common/_network_transport.py`
    (новый, 549 LOC, underscore-prefixed private,
    **NOT** в `mcp_common/__init__.py` `__all__`,
    pure stdlib `http.server.ThreadingHTTPServer` +
    `hmac.compare_digest`); содержит handler для `/mcp`
    POST endpoint (GET → 405+`Allow: POST`; non-`/mcp`
    → 404; wrong Content-Type → 415+`-32600`; body >
    1 MiB → 413+`-32600`; multiple Authorization
    headers → 400+`-32600`; case-insensitive Bearer
    scheme; constant-time token compare; failure-
    equivalence 401+`WWW-Authenticate: Bearer
    realm="mcp"`+JSON-RPC `-32001` для missing / empty
    / malformed / invalid token; notifications → 204;
    complete redaction discipline); unified
    `run_main_http(...)` с одним argparser'ом для обоих
    transport'ов (stdio path делегирует в existing
    `_stdio_transport._serve_stdio` byte-identically).
  - 3 `__main__.py` (modified) — switched import
    `_stdio_transport.run_main` →
    `_network_transport.run_main_http`; `SERVER_VERSION`
    bumped 0.3.0→0.4.0; module docstrings updated;
    `main() -> int` signature preserved.
  - `apps/platform/src/onec_platform/models.py`
    (modified) — добавлен `ProductAuthSettings`
    dataclass с `tokens: list[str]` + `auth` field на
    `ProductConfig` с `default_factory`.
  - `apps/platform/src/onec_platform/loader.py`
    (modified) — `_AUTH_ENV_TOKEN_RE` regex byte-
    identical к Track D pattern; `_parse_auth(auth_raw)`
    с unknown-keys reject, list-of-strings validation,
    env-substitution regex enforce per entry, literal
    cleartext fail-closed at config-load time.

  Verification: 51/51 PASS через одноразовый smoke
  harness — per-server `--help` exits, HTTP startup
  negative tests (missing `--bind`, missing token
  source, unresolved env), per-server HTTP positive
  smoke (tools/list valid Bearer → 200 с правильным
  tool count 15/25/16), **byte-identical 401 fail-
  closed** (no-Authorization vs wrong-token дают
  identical status + headers + JSON envelope с
  `-32001`), case-insensitive scheme {`Bearer`, `bearer`,
  `BEARER`, `BeArEr`} × 3 servers, GET 405+`Allow: POST`,
  non-`/mcp` 404, malformed JSON 400+`-32700`, wrong
  Content-Type 415+`-32600`, unknown method 200+`-32601`,
  multiple Authorization 400+`-32600`, notification 204,
  `tools/call ping` 200, cross-transport parity
  (sorted stdio names == sorted http names).
- **Step 5 (operator docs and security alignment,
  docs-only, commit `407a2f2`)** — narrow alignment
  под фактический Step 4 surface; 6 files +410/-173:
  README.md (Quickstart + «Что Quickstart не обещает»
  + полный rewrite Active parallel track секции с
  Steps 1-4 closure summary), SECURITY.md (single-
  per-transport-block rewrite + exhaustive still-NOT
  list + installer auth-round-trip gap), docs/release-
  handoff.md (4 locations: «What is in this handoff» /
  «What is NOT» / launch parenthetical / Known
  limitations), apps/platform/README.md (4 locations:
  Phase 5/Step 3 callout + «Чего сейчас намеренно
  ещё нет» + 2 lower-section parallel lists), 
  scripts/dev/launch.ps1 (header comment + Show-Usage
  help text — both transports described; in-process
  TLS not provided framing), scripts/dev/README.md
  (per-transport launch.ps1 parenthetical).
  PROJECT-STATUS.md и CHANGELOG.md deliberately
  не тронуты (Step 6 closure territory).
- **Step 6 (final integration pass and Track H closure,
  этот closure)** — `pyproject.toml` version bumped
  `0.4.0` → `0.5.0` (Q7 = ДА; Step 4 ship'нул real
  production code change с **observable runtime
  capability delta** — `python -m <server>
  --transport http --bind ... --auth-token-env ...`
  теперь реально стартует HTTP/1.1 listener с bearer
  auth, что до Track H было невозможно; backward-
  compatible new functionality classifying as MINOR
  bump per SemVer; precedent — Track D `0.1.0 → 0.2.0`,
  Track F `0.2.0 → 0.3.0`, Track G `0.3.0 → 0.4.0`);
  README + PROJECT-STATUS + CHANGELOG обновлены под
  Track H closed.

После Track H closure фактически работают:

```powershell
python -m mcp_read_server --transport stdio --help
python -m mcp_read_server --transport http --bind 127.0.0.1:8765 --auth-token-env MCP_TOKEN --help
```

(и аналогично для двух остальных серверов). Каждый сервер
поддерживает оба transport'а через единый
`list_tools()` / `get_tool(name)` boundary; `run_write_flow`
discipline для write-tools и read-only-by-construction
discipline intelligence-сервера preserved unchanged на
обоих transport'ах. CLI surface: `--help`, `--config-path`,
`--transport {stdio,http}`, `--log-level
{DEBUG,INFO,WARNING,ERROR}`, `--bind <HOST>:<PORT>`,
`--auth-token-env <VARNAME>`. Token sources: либо
`ProductConfig.auth.tokens` (each entry MUST be
`${ENV:NAME}` env-substitution; literal cleartext rejected
at config-load), либо `--auth-token-env <VARNAME>` CLI
flag (CLI wins, replace not merge). Threat model =
trusted-local-stdio для `--transport stdio`; trusted-
network behind operator-owned reverse proxy для
`--transport http`. In-process TLS не предоставляется.

Что Track H **реально закрыл** (на основе Steps 1–5
deliverables):

- second transport family поверх existing `list_tools()`
  / `get_tool(name)` boundary — single HTTP/1.1 `/mcp`
  endpoint, POST only, `application/json`, 1 MiB body
  cap, single JSON-RPC message per body, ThreadingHTTPServer
  one-thread-per-request, daemon-thread Ctrl-C, stderr-
  only logging;
- minimum authentication boundary — static bearer token
  via `Authorization: <case-insensitive-Bearer> <token>`,
  byte-exact constant-time comparison via
  `hmac.compare_digest`, failure-equivalence rule
  (missing / empty / malformed / invalid → identical
  401), complete token redaction discipline (token value
  / length / prefix / suffix / hash / fingerprint MUST
  NOT appear anywhere);
- new `ProductConfig.auth.tokens` optional schema +
  `_parse_auth` loader validation (env-substitution
  regex enforcement; literal cleartext fail-closed at
  config-load);
- two new CLI flags (`--bind`, `--auth-token-env`) +
  extended `--transport` choice set (`{stdio,http}`);
- four track-H architecture docs (plan + step-map +
  baseline audit + RFC 2119 normative contract);
- aligned operator-facing docs (README, SECURITY,
  docs/release-handoff.md, apps/platform/README.md,
  scripts/dev/launch.ps1, scripts/dev/README.md);
- registries invariant `read=15 / write=25 /
  intelligence=16` carried through unchanged;
  `mcp_common` public API export'ы preserved
  byte-identical; `_stdio_transport.py` byte-identical;
  audit `details` shape preserved.

Что Track H **не делает** «hostile-network-ready
enterprise deployment» после closure (honest constraints,
никаких скрытых гэпов):

- никакого in-process TLS / HTTPS termination — operator
  обязан terminate TLS at a reverse proxy and bind the
  Track H listener to a loopback or private interface;
- никакого mTLS / client certificate authentication;
- никакого JWT / OAuth 2.0 / OIDC / SAML / SCIM —
  introspection, refresh tokens, rotation endpoints
  тоже out-of-scope;
- никакого RBAC / ABAC / per-token permissioning /
  per-tool ACL / per-tenant isolation / multi-tenant
  policy engine — single-tier auth (valid token →
  access full registry);
- никаких session cookies / rate limiting / quotas;
- никаких WebSocket / Server-Sent Events / TCP /
  Unix-socket / named-pipe transports;
- никакого supervisor daemon / systemd unit / Windows
  Service registration / `launchd` plist / Docker /
  Kubernetes deployment manifests / `supervisor` /
  `runit` / `s6` recipes / auto-update / orchestration
  templates / HA / clustering / load balancing / hot
  reload / background watchers;
- никакого distributed tracing / observability stack
  (OpenTelemetry / Jaeger / Prometheus / OpenMetrics);
- никакого web UI / dashboard frontend;
- никакого packaging ecosystem beyond
  `[project.scripts]` declarations (`.msi` / `.deb` /
  signed distribution / GUI installer / wizard / PyPI
  publication / wheel publication; wheel build по-
  прежнему пуст по Track C honest constraint);
- никакого standalone `apps/platform` entrypoint
  (carry-over out-of-scope from Track G Q6);
- никаких новых MCP tools (registry invariant
  preserved);
- никаких 1cv8.exe runs ни на одном шаге Track H —
  трек работает на process / transport / auth layer
  уровне, не на 1cv8 binary surface;
- known install fast path round-trip limitation:
  `apps/platform/src/onec_platform/installer.py:_config_to_dict`
  не emit'ит новый `auth` section, поэтому config
  round-tripped через `scripts/release/install.ps1 ...
  -Confirm` silently теряет declarations
  `auth.tokens` — operator получает clean fail-closed
  startup и либо re-add the section by hand либо use
  `--auth-token-env <VARNAME>` to bypass the config;
  future post-Track-H fix аналогичен Phase 6 / Step 9
  service-level + enterprise round-trip fix;
- real MCP client integration test (Claude Desktop,
  MCP CLI launching server) **не** часть Track H
  closure gate — recommended но не blocker (carry-over
  Track G pattern).

Registry-инвариант сохранён точно на всём треке: `read=15
/ write=25 / intelligence=16`, `selfcheck_status=ok`.
Никаких реальных credentials ни в одном из шести Track H
commit'ов плюс одного Step 2 follow-up. Никаких 1cv8.exe
runs ни на одном шаге Track H. **GitHub remote push** не
часть Track H — repo готов к выкладке, но пушить —
operator action.

Документы трека:
[`track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md),
[`track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md),
[`track-h-transport-and-auth-baseline-audit.md`](docs/architecture/track-h-transport-and-auth-baseline-audit.md),
[`track-h-network-transport-and-auth-contract.md`](docs/architecture/track-h-network-transport-and-auth-contract.md).

Track H сейчас на **Step 5 (operator/security docs
alignment, docs-only)**. Закрытые шаги:

- **Step 1 (planning, docs-only, commit `563b27b`)** —
  ship'нуты два planning-документа
  ([`docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md),
  [`track-h-...-step-map.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md)).
- **Step 2 (transport / auth baseline audit, docs-only,
  commit `3c74564`; follow-up commit `0628f4c` removed
  literal credential-leak-guard pattern strings to keep
  the audit doc outside `verify-release.ps1` Check 7's
  match set)** — ship'нут
  [`track-h-transport-and-auth-baseline-audit.md`](docs/architecture/track-h-transport-and-auth-baseline-audit.md);
  resolved Q1 (HTTP-based), Q2 (exactly one), Q3 (static
  bearer + constant-time compare), Q4
  (`ProductConfig.auth.tokens` + `${ENV:NAME}` +
  `--auth-token-env` CLI override).
- **Step 3 (network transport / auth contract, docs-only,
  commit `2e76061`)** — ship'нут
  [`track-h-network-transport-and-auth-contract.md`](docs/architecture/track-h-network-transport-and-auth-contract.md)
  (1650 lines, 293 RFC 2119 keyword usages: 199 MUST,
  74 MUST NOT, 17 MAY, 2 SHOULD, 1 SHALL); 18 sections
  pinning every transport / auth / config / CLI /
  integration / verification rule for Step 4.
- **Step 4 (narrow HTTP transport and bearer auth
  boundary, единственный шаг с production code change,
  commit `5814041`)** — PATH A (per Step 3 contract
  §11). Ship'нуто 5 файлов (+877/-35):
  - `packages/mcp-common/src/mcp_common/_network_transport.py`
    (новый, 549 LOC, underscore-prefixed private,
    **NOT** в `mcp_common/__init__.py`'s `__all__`,
    pure stdlib `http.server.ThreadingHTTPServer` +
    `hmac.compare_digest`); содержит handler для
    `/mcp` POST endpoint (GET → 405+`Allow:POST`;
    non-`/mcp` → 404; wrong Content-Type → 415+`-32600`;
    body > 1 MiB → 413+`-32600`; multiple Authorization
    headers → 400+`-32600`; case-insensitive Bearer
    scheme; constant-time token compare; failure-
    equivalence 401+`WWW-Authenticate`+JSON-RPC `-32001`
    для missing/empty/malformed/invalid token;
    notifications → 204; complete redaction discipline);
    unified `run_main_http(...)` с одним argparser'ом
    для обоих transport'ов (stdio path делегирует в
    existing `_stdio_transport._serve_stdio` byte-
    identically).
  - 3 `__main__.py` (modified) — switched import
    `_stdio_transport.run_main` → `_network_transport.run_main_http`;
    `SERVER_VERSION` 0.3.0→0.4.0; module docstrings
    updated; `main() -> int` signature preserved.
  - `apps/platform/src/onec_platform/models.py`
    (modified) — добавлен новый `ProductAuthSettings`
    dataclass с `tokens: list[str]` + `auth` field на
    `ProductConfig` с `default_factory`.
  - `apps/platform/src/onec_platform/loader.py`
    (modified) — новый `_AUTH_ENV_TOKEN_RE` regex
    byte-identical к Track D pattern; новый
    `_parse_auth(auth_raw)` с unknown-keys reject,
    list-of-strings validation, env-substitution regex
    enforce per entry, literal cleartext fail-closed
    at config-load time.

После Step 4 фактически работают:

```powershell
python -m mcp_read_server --transport stdio --help
python -m mcp_read_server --transport http --bind 127.0.0.1:8765 --auth-token-env MCP_TOKEN --help
```

(и аналогично для двух остальных серверов). Каждый сервер
поддерживает оба transport'а через единый
`list_tools()` / `get_tool(name)` boundary; `run_write_flow`
discipline для write-tools и read-only-by-construction
discipline intelligence-сервера preserved unchanged на
обоих transport'ах. Step 4 verification — 51 / 51 PASS
(per-server `--help` exit 0; HTTP startup negative tests:
missing `--bind`, missing token source, unresolved env;
HTTP positive smoke на всех 3 servers; **byte-identical
401 fail-closed** для no-Authorization vs wrong-token;
case-insensitive scheme через {`Bearer`, `bearer`,
`BEARER`, `BeArEr`}; GET 405; non-`/mcp` 404; malformed
JSON 400+`-32700`; wrong Content-Type 415+`-32600`;
unknown method 200+`-32601`; multiple Authorization
400+`-32600`; notification 204; `tools/call ping` 200;
cross-transport parity stdio = HTTP tool-name set).

Registries `read=15 / write=25 / intelligence=16` без
drift'а; никаких новых MCP tools; никаких новых runtime
dependencies (implementation pure stdlib); никаких
1cv8.exe runs ни на одном шаге трека; никаких реальных
credentials в repo / docs / commit messages.

Что **не** входит в Track H (повтор для ясности после
Step 4): in-process TLS / HTTPS termination, mTLS /
client certificate authentication, JWT / OAuth 2.0 /
OIDC / SAML / SCIM, RBAC / ABAC / per-tool ACL /
per-tenant isolation / multi-tenant policy engine,
token rotation endpoint / refresh tokens / session
cookies, rate limiting, WebSocket / SSE / TCP /
Unix-socket / named-pipe transports, supervisor daemon
/ systemd unit / Windows Service registration /
`launchd` plist / auto-update / orchestration templates
/ HA / clustering / load balancing / hot reload /
background watchers, web UI / dashboard frontend,
packaging ecosystem (`.msi` / `.deb` / signed
distribution / GUI installer / PyPI publication / wheel
publication beyond `[project.scripts]` declarations),
new MCP tools (registries without drift), 1cv8 work,
rollback / AST / multi-version 1С matrix expansion,
standalone `apps/platform` entrypoint, distributed
tracing / observability stack, real MCP client
integration test as closure gate, remote push.

Известный gap из Step 4 (operator-facing item handled
in this Step 5 alignment, not a Step 4 code-fix):
`apps/platform/src/onec_platform/installer.py:_config_to_dict`
не emit'ит новый `auth` section, поэтому config
round-tripped через `scripts/release/install.ps1 ...
-Confirm` silently теряет declarations `auth.tokens`.
Operators using `--transport http` against a round-
tripped config get a clean fail-closed startup и либо
re-add the section by hand либо use `--auth-token-env
<VARNAME>` CLI flag to bypass the config. Future
post-Track-H fix к `_config_to_dict` analogous Phase 6
/ Step 9 service-level + enterprise round-trip fix.

Следующий шаг по Track H — **Step 6 (final integration
pass and Track H closure)**: closure narrative pass
через `README.md` + `PROJECT-STATUS.md` + `CHANGELOG.md`
(Q7 default ДА — version bump 0.4.0→0.5.0 на closure
если Step 4 functional delta проходит SemVer MINOR-
bump bar; финальное решение — Step 6); **GitHub remote
push — operator action, не часть трека**.

Документы трека:
[`track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md),
[`track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md`](docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md),
[`track-h-transport-and-auth-baseline-audit.md`](docs/architecture/track-h-transport-and-auth-baseline-audit.md),
[`track-h-network-transport-and-auth-contract.md`](docs/architecture/track-h-network-transport-and-auth-contract.md).

Подробности по последнему закрытому треку — в секции
«Track G detail (закрыт)» ниже.

## Track G detail (закрыт)

**Цель Track G** была — ship'ить **первый production-grade
operational слой** для трёх MCP servers, закрывая factual
gap «MCP servers cannot start at all»: canonical
`__main__.py` для всех трёх MCP servers, minimum-viable
stdio JSON-RPC 2.0 transport, minimal CLI surface
(`--help`, `--config-path`, `--transport`, `--log-level`),
`[project.scripts]` console entry points в `pyproject.toml`.
Это **не** universal production transport, **не**
network-grade HTTP/WebSocket layer, **не** authentication /
authorization, **не** supervisor daemon, **не** HA /
clustering, **не** web UI, **не** packaging ecosystem
(`.msi` / `.deb` / signed distribution), **не** enterprise
super-set (SSO/RBAC/multi-tenant), **не** standalone
`apps/platform` entrypoint. Платформа архитектурно остаётся
при том же подходе: existing `server.py:REGISTERED_TOOLS`
registries (`list_tools()` / `get_tool(name)`) preserved
byte-identical; Track G ship'ил **transport layer поверх**
этих registries, не задевая их. Шесть шагов;
production-код Track G правил **только Step 4 commit** и
**только** на explicit allowed surfaces (3 new `__main__.py`
files + 1 new private `mcp_common._stdio_transport` helper +
`pyproject.toml` `[project.scripts]` block).

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-g-production-grade-mcp-transport-and-cli-plan.md`](docs/architecture/track-g-production-grade-mcp-transport-and-cli-plan.md),
  [`docs/architecture/track-g-production-grade-mcp-transport-and-cli-step-map.md`](docs/architecture/track-g-production-grade-mcp-transport-and-cli-step-map.md)):
  назначение трека, целевой результат, что закрывает /
  не закрывает Track G, отличия от Tracks A–F, guardrails,
  acceptance criteria, открытые вопросы Q1–Q7. Никакого
  code change. Commit `7a39454`.
- **Step 2 (transport baseline audit)** — новый
  documentation-only audit-документ
  ([`docs/architecture/track-g-transport-baseline-audit.md`](docs/architecture/track-g-transport-baseline-audit.md),
  587 строк) с per-server inventory current state +
  4-class breakdown (already useful baseline / adjacent
  insufficient / clearly missing / out-of-scope) +
  read-only evidence. Critical findings: pyproject.toml
  имеет zero declared runtime deps (no `[project.dependencies]`
  block at all), zero MCP SDK imports anywhere в repo,
  все 3 MCP server packages идентичная structure без
  `__main__.py`. **Q1 resolved** (stdio only), **Q2
  resolved** (custom stdlib без новых deps), **Q6
  resolved** (`apps/platform` standalone entrypoint
  out-of-scope). Никакого code change. Commit `6f3ad73`.
- **Step 3 (runtime CLI / entrypoint contract)** — новый
  prescriptive normative document
  ([`docs/architecture/track-g-runtime-cli-entrypoint-contract.md`](docs/architecture/track-g-runtime-cli-entrypoint-contract.md),
  879 строк) с RFC 2119-style MUST / MUST NOT / SHALL /
  SHOULD / MAY wording (85 normative keyword usages).
  15 sections: exact `__main__.py` shape, exact CLI
  surface, exact transport scope (stdio JSON-RPC 2.0 only,
  forbidden libraries, stdout/stderr discipline,
  minimum-viable MCP method set), server binding /
  dispatch contract (через existing `list_tools()` /
  `get_tool(name)` indirection — никаких parallel
  registration paths), no-auth posture, no-supervisor
  posture, exact `[project.scripts]` block, backward
  compatibility (15/25/16 registries + `mcp_common` API +
  audit shape preserved), exact Step 4 implementation
  surface (allowed files + forbidden surfaces + scope
  creep markers), verification protocol. Никакого code
  change. Commit `8bb3883`.
- **Step 4 (narrow stdio transport and CLI entrypoints)** —
  единственный шаг Track G с production code change.
  Implementation path **PATH B** (3 entrypoints + pyproject
  scripts + 1 private `mcp_common` helper). PATH A pure
  inline был отвергнут потому что каждый `__main__.py`
  carried бы ~140 LOC идентичных argparse / JSON-RPC
  framing / dispatch logic — ~280 LOC pure copy-paste
  через 3 server'а — что qualifies as «duplication
  otherwise unreasonable» под Step 3 contract §12.1.4.
  Ship'нуто 5 файлов (+361 lines):
  - `packages/mcp-common/src/mcp_common/_stdio_transport.py`
    (новый, 245 LOC) — underscore-prefixed internal helper,
    **NOT** экспортирован из `mcp_common/__init__.py`;
    pure stdlib (`argparse`, `json`, `logging`, `inspect`,
    `sys`); реализует line-delimited JSON-RPC 2.0 loop,
    четыре required CLI флага, handlers для `initialize` /
    `ping` / `tools/list` / `tools/call` /
    `notifications/initialized` / `notifications/cancelled`,
    serialization `ToolResult` → MCP envelope (`content`
    + `structuredContent` + `isError`), top-of-`run_main`
    exception boundary; stdout reserved для JSON-RPC
    envelopes, диагностика — в stderr через `logging`;
  - `apps/mcp-read-server/src/mcp_read_server/__main__.py`
    (новый, ~30 LOC);
  - `apps/mcp-write-server/src/mcp_write_server/__main__.py`
    (новый, ~30 LOC);
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
    (новый, ~30 LOC) — каждый определяет `main() → int`
    которая зовёт `run_main` с per-package's existing
    `list_tools` / `get_tool` boundary и per-server name +
    version. No `__init__.py` edits, no `server.py` edits,
    no `tools.py` / `models.py` / `runtime/` / `apps/platform/`
    touches;
  - `pyproject.toml` (edit) — добавлен `[project.scripts]`
    block с ровно тремя console entries
    (`mcp-read-server`, `mcp-write-server`,
    `mcp-intelligence-server`); никаких новых deps;
    `[tool.hatch.build.targets.wheel] packages = []`
    preserved unchanged (Track C / Step 3 honest
    constraint kept).

  Commit `370c5a8`.
- **Step 5 (operator docs and transport alignment)** —
  docs-only narrow alignment под фактический Step 4
  surface; 6 files +229/-81 lines: `README.md` (Quickstart
  paragraph + «Что Quickstart не обещает» + полный rewrite
  Active parallel track секции), `SECURITY.md` (один bullet
  «No production-grade MCP transport yet» → «Local stdio
  MCP transport only» с explicit threat model и still-NOT
  list), `docs/release-handoff.md` (новый bullet под
  «What is in this handoff» + «What is NOT in this
  handoff» reworded + «Local check / launch» parenthetical
  fix + Known limitations alignment),
  `apps/platform/README.md` (4 locations: Phase 5/Step 3
  callout + «Чего сейчас намеренно ещё нет» + parallel
  list + Phase 6 honest-constraints item),
  `scripts/dev/launch.ps1` (header comment + Show-Usage
  help text — operators pointed at `python -m <server>
  --help`), `scripts/dev/README.md` (две parenthetical
  wording fixes + CI workflow note distinguishes live
  MCP runtime от selfcheck). NOT touched: PROJECT-STATUS
  + CHANGELOG (closure territory); production code;
  pyproject.toml (Q7 = Step 6); registries `15/25/16`
  invariant. Commit `5890ba5`.
- **Step 6 (final integration pass and Track G closure)** —
  этот closure: `pyproject.toml` version bumped
  `0.3.0` → `0.4.0` (Q7 = ДА; Track G / Step 4 ship'нул
  real production code change с **observable runtime
  capability delta** — `python -m mcp_{read,write,intelligence}_server`
  теперь реально стартуют stdio JSON-RPC server, что
  до Track G было невозможно; backward-compatible new
  functionality classifying as MINOR bump per SemVer;
  precedent — Track D `0.1.0 → 0.2.0` и Track F
  `0.2.0 → 0.3.0` shipped comparable scale functional
  delta);
  README + PROJECT-STATUS + CHANGELOG обновлены под
  Track G closed.

После Track G closure фактически работают:

```powershell
python -m mcp_read_server --help
python -m mcp_write_server --help
python -m mcp_intelligence_server --help
```

Каждый сервер поднимает line-delimited stdio JSON-RPC 2.0
loop с handler'ами для `initialize` / `ping` / `tools/list`
/ `tools/call` / `notifications/initialized` /
`notifications/cancelled`. Stdout зарезервирован под
JSON-RPC envelopes; диагностика идёт в stderr через
`logging`. Tool dispatch идёт через existing `server.py`
boundary (`list_tools()` / `get_tool(name)`);
`run_write_flow` discipline для write-tool'ов сохранена;
read-only-by-construction discipline intelligence-сервера
сохранена; `mcp_common` public API surface (export'ы из
`mcp_common/__init__.py`) preserved byte-identical.

Что Track G **реально закрыл** (на основе Steps 1–5
deliverables):

- три canonical entrypoint'а
  (`apps/mcp-{read,write,intelligence}-server/src/.../`__main__.py``)
  + одну private internal stdio JSON-RPC 2.0 transport
  библиотеку (`packages/mcp-common/src/mcp_common/_stdio_transport.py`,
  underscore-prefixed, **NOT** в public `mcp_common`
  surface) — `python -m <server>` теперь runtime-достижим;
- minimal CLI surface на каждом сервере: `--help`,
  `--config-path`, `--transport stdio`, `--log-level
  {DEBUG,INFO,WARNING,ERROR}`; `--help` exit 0 + non-empty
  usage verified для всех трёх servers;
- `[project.scripts]` block в `pyproject.toml` с тремя
  console entries (готовы к activation, как только future
  packaging track ship'ит real wheel — wheel build по-
  прежнему пуст по Track C honest constraint);
- formal normative entrypoint / CLI / transport contract
  (RFC 2119-style, 879 строк) — единая reference для
  любого future transport extension;
- aligned operator-facing docs (README, SECURITY,
  docs/release-handoff.md, apps/platform/README.md,
  scripts/dev/launch.ps1, scripts/dev/README.md) — все
  говорят one truth: local stdio transport baseline
  exists, network/auth/supervisor still out-of-scope;
- registries invariant `read=15 / write=25 /
  intelligence=16` carried through unchanged;
  `mcp_common` public API export'ы preserved
  byte-identical; audit `details` shape preserved.

Что Track G **не делает** «production-deployment-ready
MCP сервером для adversarial network» после closure
(honest constraints, никаких скрытых гэпов):

- никакого network transport (HTTP / WebSocket / SSE /
  TCP / Unix domain socket / named pipe / Windows IPC) —
  это subsequent post-Track-G track;
- никакой authentication / authorization (token / Bearer
  / JWT / API key / mTLS / OAuth 2.0 / OpenID Connect /
  SAML / RBAC / ABAC / multi-tenant isolation) —
  trusted-stdio-only threat model;
- никакого supervisor daemon (systemd unit / Windows
  Service / `launchd` plist / Docker / Kubernetes /
  `supervisor` / `runit` / `s6` integration recipes /
  automatic restart watcher / log aggregation);
- никакого hot reload или background config watcher;
- никакого web UI / dashboard frontend;
- никакого packaging ecosystem beyond
  `[project.scripts]` declarations (`.msi` / `.deb` /
  GUI installer / signed distribution / PyPI publication
  / wheel publication — Track C wheel-build empty
  constraint preserved);
- никакого standalone `apps/platform` entrypoint
  (deliberately out-of-scope per Q6);
- никакого 1cv8.exe execution work на любом шаге трека;
- никаких новых MCP tools (registries без drift'а);
- никакого distributed tracing / observability stack
  (OpenTelemetry / Jaeger / Prometheus);
- никаких rate limiting / multi-instance load balancing;
- real MCP client integration test (Claude Desktop, MCP
  CLI launching server) **не** часть Track G closure
  gate — это operator infra territory.

Registry-инвариант сохранён точно на всём треке: `read=15 /
write=25 / intelligence=16`, `selfcheck_status=ok`. Никаких
реальных credentials ни в одном из шести Track G commit'ов.
Никаких 1cv8.exe runs ни на одном шаге Track G (Track G
работает на process / transport layer уровне, не на 1cv8
binary surface). **GitHub remote push** не часть Track G —
repo готов к выкладке, но пушить — operator action.

Документы трека:
[`docs/architecture/track-g-production-grade-mcp-transport-and-cli-plan.md`](docs/architecture/track-g-production-grade-mcp-transport-and-cli-plan.md),
[`docs/architecture/track-g-production-grade-mcp-transport-and-cli-step-map.md`](docs/architecture/track-g-production-grade-mcp-transport-and-cli-step-map.md),
[`docs/architecture/track-g-transport-baseline-audit.md`](docs/architecture/track-g-transport-baseline-audit.md),
[`docs/architecture/track-g-runtime-cli-entrypoint-contract.md`](docs/architecture/track-g-runtime-cli-entrypoint-contract.md).

## Track F detail (закрыт)

**Цель Track F** была — узко и контролируемо расширить
`_AUTOMATIC_RECOVERY_SUPPORTED` whitelist
(`apps/platform/src/onec_platform/recovery.py:126-133`) за
пределы Phase-6 / Step-4 baseline'а в 2 tools для нескольких
file-based mutating tools, чьи inverse semantics уже честно
покрываются existing `restore_dump_file_from_snapshot`
mechanism'ом. Это **не** universal rollback, **не** «rollback
теперь есть везде», **не** public `delete_*` write-tools,
**не** multi-file / DB schema rollback, **не** AST-based
semantic reverse engine, **не** новый MCP surface, **не**
execution-core rewrite. Платформа архитектурно осталась при
том же подходе: rollback идёт через public write-tool по
`run_write_flow` дисциплине; Track F расширил **whitelist
configuration**, не mechanism. Шесть шагов; production-код
Track F правил **только два** boundary'а в одном Step 4
commit'е.

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-f-rollback-whitelist-expansion-plan.md`](docs/architecture/track-f-rollback-whitelist-expansion-plan.md),
  [`docs/architecture/track-f-rollback-whitelist-expansion-step-map.md`](docs/architecture/track-f-rollback-whitelist-expansion-step-map.md)):
  назначение трека, целевой результат, gap statement, 10
  acceptance criteria, открытые вопросы Q1–Q7. Никакого code
  change. Commit `351278b`.
- **Step 2 (rollback baseline audit and candidate selection)** —
  новый documentation-only audit-документ
  ([`docs/architecture/track-f-rollback-baseline-audit.md`](docs/architecture/track-f-rollback-baseline-audit.md),
  637 строк): per-tool evaluation 12 mutating tools (Group
  C/D/E из 25 registry) против criteria a/b/c с manual code
  review evidence (file/line + payload key для каждого);
  **Tier 4** (already, 2 tools), **Tier 1** (strong
  candidates, 4 tools), **Tier 2** (deferred — `update_module_code`
  payload key gap), **Tier 3** (categorically excluded — 5
  tools: 3 `create_*` family + `apply_config_from_files` +
  `update_database_configuration`); resolve **Q2** —
  exact Step 4 target set. Никакого code change. Commit
  `e9725b2`.
- **Step 3 (rollback eligibility contract)** — новый
  prescriptive normative document
  ([`docs/architecture/track-f-rollback-eligibility-contract.md`](docs/architecture/track-f-rollback-eligibility-contract.md),
  633 строки) с RFC 2119-style MUST / MUST NOT / SHALL / MAY
  wording (64 normative keyword usages): formal eligibility
  criteria 4.A–4.F (payload shape via `_RELATIVE_PATH_KEYS`,
  restore semantics, verification, sync discipline,
  non-expansion, implementation surface), 9 categorical
  exclusions, exact Step 4 implementation boundary с per-tool
  sanity check anchors, escape clause без silent target-set
  drift, backward compatibility statement. Никакого code
  change. Commit `45ad2b2`.
- **Step 4 (narrow rollback whitelist expansion)** —
  единственный шаг Track F с production code change. Narrow
  two-file expansion 2 → 6 entries: расширены
  `apps/platform/src/onec_platform/recovery.py:_AUTOMATIC_RECOVERY_SUPPORTED`
  и
  `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py:_ROLLBACK_SUPPORTED_OPERATIONS`
  identical content'ом — добавлены `add_form_attribute`,
  `add_form_element`, `append_module_method`,
  `replace_module_method_body` (alphabetically). Plus minor
  sync-comment wording update в `flow.py:97-103` (allowed per
  Step 3 contract Section 6.3.1). Per-tool sanity check
  anchors зафиксированы в commit message с
  `tools.py` line numbers (3512-3520 / 2680-2687 / 2833-2838 /
  2994-2999). Никаких изменений в `tools.py`,
  `_RELATIVE_PATH_KEYS`, `_extract_relative_path`, audit
  shape, registries. Commit `cd95627`.
- **Step 5 (operator docs and rollback coverage alignment)** —
  8 точечных wording-edits в трёх operator-facing docs:
  `apps/platform/README.md` (5 правок: RECOVERY_MODES
  executed-mode wording; section heading «Почему пуст» →
  «исторически был пуст и как он расширялся»; «Что rollback
  UX не делает» bullet; Phase 6 / Step 4 historical section
  + новая «Track F / Step 4 — расширение whitelist до 6
  tools» subsection), `README.md` (2 правки: Quickstart
  Track F open + Track A detail honest constraints bullet),
  `docs/release-handoff.md` (1 правка: «Limited rollback
  coverage» Known limitations bullet). Никакого code change.
  Commit `60f1761`.
- **Step 6 (final integration pass and Track F closure)** —
  этот closure: `pyproject.toml` version bumped
  `0.2.0` → `0.3.0` (Q5 = ДА; Track F / Step 4 ship'нул real
  code change с functional delta — backward-compatible new
  functionality classifying as MINOR bump per SemVer);
  README + PROJECT-STATUS + CHANGELOG обновлены под Track F
  closed.

Что Track F **реально закрыл** (на основе Steps 1–5
deliverables):

- расширение `_AUTOMATIC_RECOVERY_SUPPORTED` whitelist'а
  с 2 до 6 entries identical в обеих mirror frozenset'ах
  (recovery.py + flow.py); `automatic_recovery_supported=True`
  теперь runtime-достижим для 4 дополнительных tool families
  (XML form-edit ops + BSL module-edit ops);
- formal normative eligibility contract (RFC 2119-style)
  определяющий что считается eligible (payload shape +
  restore semantics + verification + sync discipline +
  non-expansion + implementation surface) — единая reference
  для будущих whitelist expansion attempts;
- per-tool descriptive audit с manual code review evidence
  (file/line + payload key) для всех 12 mutating tools
  registry surface;
- aligned operator-facing docs (`apps/platform/README.md`,
  `README.md`, `docs/release-handoff.md`) под фактический
  whitelist size 6 — все говорят one truth: coverage broader
  but still narrow, no blanket reversibility claim, Tier 3
  categorical exclusions remain.

Что Track F **не делает** «полным rollback'ом всего» после
closure (honest constraints, никаких скрытых гэпов):

- никакого universal / arbitrary rollback для любого
  write-tool — whitelist остаётся ограничен exact 6 entries;
- никакого AST-based semantic reverse engine для BSL / XML;
- никакого public `delete_*` write-tools (semantics удаления
  в 1С остаётся undecided);
- никакого multi-file / full filesystem snapshot-restore —
  single-file `restore_dump_file_from_snapshot` остаётся
  exclusive mutating mechanism;
- никакого rollback для `apply_config_from_files`
  (multi-file impact violates criterion (a));
- никакого rollback для `update_database_configuration`
  (DB schema migration violates criteria (a)/(b)/(c));
- никакого rollback для `create_*` family (`create_catalog`,
  `create_common_module`, `create_managed_form` — Tier 3
  categorical exclusion: inverse = delete; snapshot
  pre-create не содержит file для restore);
- coverage breadth: 6 of 25 mutating registry tools = 24%
  mutating surface; 19 mutating tools остаются manual
  snapshot-restore territory by design.

Registry-инвариант сохранён точно на всём треке: `read=15 /
write=25 / intelligence=16`, `selfcheck_status=ok`. Никаких
реальных credentials ни в одном из шести Track F commit'ов.
Никаких 1cv8.exe runs ни на одном шаге Track F (Track F
работает на whitelist configuration уровне, не на 1cv8
binary surface). **GitHub remote push** не часть Track F —
repo готов к выкладке, но пушить — operator action.

Документы трека: `docs/architecture/track-f-rollback-whitelist-expansion-plan.md`,
`docs/architecture/track-f-rollback-whitelist-expansion-step-map.md`,
`docs/architecture/track-f-rollback-baseline-audit.md`,
`docs/architecture/track-f-rollback-eligibility-contract.md`.

## Track E detail (закрыт)

**Цель Track E** была — расширить доказательную базу проекта с
**одного** reference stand'а / **одной** 1С версии
(`8.3.27.1859`, evidence Track A / Step 6) на узкую
documented smoke matrix из нескольких 1С версий по одному
и тому же узкому сценарию. Платформа архитектурно
остаётся multi-version-friendly: оператор сам выбирает
binary path в config'е; Track E добавляет
evidence-уровень и docs, **не** архитектуру. Это **не**
«поддержка всех версий», **не** full QA program, **не**
performance / stress / fuzzing track, **не** enterprise
certification, **не** новый MCP surface. Шесть шагов;
production-код Track E **вообще не правил**.

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-e-multi-version-smoke-matrix-plan.md`](docs/architecture/track-e-multi-version-smoke-matrix-plan.md),
  [`docs/architecture/track-e-multi-version-smoke-matrix-step-map.md`](docs/architecture/track-e-multi-version-smoke-matrix-step-map.md)):
  назначение трека, целевой результат, gap statement
  (argv-grammar drift между версиями + install layout
  dependency), guardrails, 10 acceptance criteria, открытые
  вопросы Q1–Q7. Никакого code change. Commit `1b233ce`.
- **Step 2 (current evidence audit + smoke scenario freeze)** —
  два новых short documentation-only документа:
  [`docs/architecture/track-e-current-evidence-audit.md`](docs/architecture/track-e-current-evidence-audit.md)
  (descriptive — что уже доказано на reference version,
  physical artifacts, чего пока нет, why single-version
  insufficient) и
  [`docs/architecture/track-e-smoke-scenario.md`](docs/architecture/track-e-smoke-scenario.md)
  (prescriptive **frozen** — name `frozen-smoke-v1`,
  cut-down `create_dump_snapshot` через `/DumpConfigToFiles`
  only, principle-based version selection criteria,
  12-column matrix shape, PASS / FAIL / NOT RUN semantics,
  required evidence fields). Никакого code change. Commit
  `630f837`.
- **Step 3 (matrix scaffolding and operator runbook)** — два
  новых operator-facing документа:
  [`docs/runbooks/track-e-multi-version-smoke-matrix.md`](docs/runbooks/track-e-multi-version-smoke-matrix.md)
  (operator runbook для прогона `frozen-smoke-v1` на
  operator-supplied 1С версии — preconditions, execution
  procedure, evidence capture, common stop conditions,
  honest constraints) и
  [`docs/version-support-matrix.md`](docs/version-support-matrix.md)
  (top-level evidence table с frozen 12-column shape; одна
  reference row заполнена copy-only из existing Track A /
  Step 6 evidence, scenario field явно
  `stronger-than-frozen-smoke-v1`; никаких имитированных
  additional rows). Никакого 1cv8.exe run. Commit `7c08cae`.
- **Step 4 (operator-driven smoke execution and matrix
  update)** — закрыт через **PATH B (honest
  operator-supplied gap)**. Никаких 1cv8.exe runs не было
  выполнено в этом шаге; никаких additional evidence rows
  не было добавлено. Operator-side inventory показал только
  `8.3.27` minor family (builds `1859/x64` reference и
  `1936/x86` дисквалифицирован per Step 2 §2.2 — same minor
  family); никаких `8.3.<other minor>` family у operator'а
  нет; ENV-substitution credentials не выставлены в session.
  Per Track E plan Q4 + step-map Step 4 это **honest
  closure**, не failure. Matrix doc дополнен Step 4 closure
  note с inventory-таблицей и explicit list того, что Step 4
  сознательно не делал. Commit `f962d78`.
- **Step 5 (support statement and docs alignment)** — три
  operator-facing документа выровнены под фактический Step 4
  PATH B результат:
  [`SECURITY.md`](SECURITY.md) («Single-version 1С evidence
  (with multi-version scaffolding)» bullet с pointer на
  matrix doc + «no blanket multi-version support claim»),
  [`docs/release-handoff.md`](docs/release-handoff.md)
  («Multi-version 1С smoke matrix — scaffolding only»
  Known limitations + Single-version coverage bullet pointer
  расширение), и Quickstart paragraph + «Куда идти дальше»
  navigation в этом README. Никакого code change. Commit
  `78d5956`.
- **Step 6 (final integration pass and Track E closure)** —
  этот closure: README + PROJECT-STATUS + CHANGELOG
  обновлены под Track E closed; никакого version bump
  (Q5 = НЕТ — Track E без functional delta).

Что Track E **реально закрыл** (на основе Steps 1–5
deliverables):

- frozen narrow smoke scenario `frozen-smoke-v1` —
  cut-down `create_dump_snapshot` через
  `/DumpConfigToFiles` only, читаемый contract на
  PASS / FAIL / NOT RUN verdict;
- documented matrix scaffolding (12-column frozen
  contract в `docs/version-support-matrix.md`,
  reference row copy-only из existing Track A
  evidence);
- operator runbook для прогона smoke на любой
  operator-supplied 1С версии без feature changes
  в платформе;
- aligned operator-facing docs (SECURITY,
  release-handoff, README) — все говорят одно и то
  же про current evidence level: reference есть,
  matrix scaffolding есть, additional rows нет,
  PATH B honest gap;
- single source of truth для actual evidence level —
  `docs/version-support-matrix.md`;
- post-closure additional rows возможны через
  operator-driven runs по runbook'у без re-open
  трека (per plan Q7).

Что Track E **не делает** «полной совместимостью
со всеми 1С версиями» после closure (honest
constraints, никаких скрытых гэпов):

- никаких additional version evidence rows beyond
  reference — Step 4 закрыт через PATH B; на
  operator machine отсутствуют 1С minor families
  помимо `8.3.27`;
- никакого blanket multi-version support claim;
- никакой полной QA-программы, performance /
  stress / fuzzing testing, enterprise
  certification;
- никакого version-sniffing в платформе;
- никаких новых MCP tools (registries `read=15 /
  write=25 / intelligence=16` без drift'а);
- никаких 1cv8 binary changes, transport rewrite,
  packaging rewrite;
- никакой CI matrix runner-инфраструктуры для
  multi-version 1cv8 (это physical operator
  territory);
- никакого long-tail backwards compatibility
  guarantee для будущих 1С версий, ещё не
  вышедших на момент closure.

Registry-инвариант сохранён точно на всём треке:
`read=15 / write=25 / intelligence=16`,
`selfcheck_status=ok`. Никаких реальных credentials
ни в одном из шести Track E commit'ов. Никаких
запусков 1cv8.exe ни на одном шаге Track E (Step 4
PATH B closure означал явное отсутствие runs).
**GitHub remote push** не часть Track E — repo
готов к выкладке, но пушить — operator action.

Документы трека: `docs/architecture/track-e-multi-version-smoke-matrix-plan.md`,
`docs/architecture/track-e-multi-version-smoke-matrix-step-map.md`,
`docs/architecture/track-e-current-evidence-audit.md`,
`docs/architecture/track-e-smoke-scenario.md`,
`docs/runbooks/track-e-multi-version-smoke-matrix.md`,
`docs/version-support-matrix.md`.

## Track D detail (закрыт)

**Цель Track D** была — сделать operator credentials flow
менее хрупким: ввести документированный env-substitution путь
для DESIGNER credentials в `onec_*_command_template`-массивах,
добавить redaction discipline в `command_preview` и trimmed
payload-excerpt'ы, перенести cleartext-password literal из
«нормального baseline'а» в legacy fallback, и расширить
`verify-release.ps1` узкой credential-template-hygiene
heuristic'ой. Это **не** enterprise security platform, **не**
vault / KMS / SSO / RBAC track, **не** OS keychain integration
as baseline и **не** production-grade MCP transport. Шесть
шагов; production-код Track D правил **только два**
boundary'а — один внутри `mcp-write-server` runtime layer и
один release-side скрипт.

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-d-operator-credentials-hardening-plan.md`](docs/architecture/track-d-operator-credentials-hardening-plan.md),
  [`docs/architecture/track-d-operator-credentials-hardening-step-map.md`](docs/architecture/track-d-operator-credentials-hardening-step-map.md)):
  назначение трека, целевой результат, guardrails,
  10 acceptance criteria, открытые вопросы Q1–Q7. Никакого
  code change; commit `61cf225`.
- **Step 2 (credentials-flow audit and contract)** — два
  новых documentation-only документа:
  [`docs/architecture/track-d-credentials-flow-audit.md`](docs/architecture/track-d-credentials-flow-audit.md)
  (где `/P "<password>"` физически появляется сегодня, какие
  payload-поля видят rendered argv, что значит «out-of-band»
  до Track D), и
  [`docs/architecture/track-d-credentials-contract.md`](docs/architecture/track-d-credentials-contract.md)
  (формальный contract на env-substitution syntax,
  render-time resolution order, fail-closed semantics,
  redaction discipline, backward-compat с literal
  cleartext). Никаких изменений production-кода; commit
  `0d708d1`.
- **Step 3 (env substitution and preview redaction)** —
  implementation в
  `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`:
  helper `_resolve_env_token(...)` резолвит full-element
  токен `${ENV:NAME}` из process environment в render-time
  (после structural-placeholder substitution); fail-closed
  на missing / empty / partial / mixed формах
  (`ok=False`, `command_preview=None`, subprocess **не**
  стартует); helper `_redact_password_args(...)` подменяет
  argv-элемент после `/P` или `/Pwd` (case-insensitive) на
  sentinel `<redacted>` в `command_preview` и trimmed
  excerpt'ах. Actual subprocess argv остаётся unredacted —
  иначе binary не аутентифицируется. Literal cleartext
  templates по-прежнему supported как legacy fallback.
  Registry-инвариант `read=15 / write=25 / intelligence=16`
  без drift'а; commit `af4436f`.
- **Step 4 (operator docs and migration alignment)** —
  operator-facing документация переведена на
  `${ENV:NAME}` форму как **рекомендованный default**, с
  literal cleartext clearly marked legacy fallback. Три
  документа выровнены:
  [`docs/runbooks/track-a-reference-stand-round-trip.md`](docs/runbooks/track-a-reference-stand-round-trip.md)
  (product-config example, env-substitution callout,
  failure mode F2 расширен под env-token failures,
  credentials-in-logs нота обновлена),
  [`SECURITY.md`](SECURITY.md) (Honest constraints block
  переписан под env-substitution),
  [`docs/release-handoff.md`](docs/release-handoff.md)
  (Known limitations DESIGNER credentials bullet
  переписан). Никаких изменений production-кода; commit
  `393e869`.
- **Step 5 (release verify credential hygiene heuristic)** —
  8-й check **Credential template hygiene** добавлен в
  [`scripts/release/verify-release.ps1`](scripts/release/verify-release.ps1).
  Сканирует tracked `*.config.json` (через `git ls-files`)
  на argv-элементы непосредственно после `"/P"` / `"/Pwd"`
  (case-insensitive) внутри command-template массивов.
  Документированные safe-формы (`"${ENV:NAME}"`,
  `"<password>"`) → PASS; literal cleartext → **WARN**
  (не FAIL), с file:line; пустые value не флагуются. WARN
  не меняет exit-code semantics, поэтому legacy templates
  не блокируют receive-side flow.
  [`scripts/release/README.md`](scripts/release/README.md) и
  [`docs/release-handoff.md`](docs/release-handoff.md)
  синхронизированы под 8 checks и описывают узкий
  heuristic-not-DLP scope; commit `1fd2d35`.
- **Step 6 (final integration pass and Track D closure)** —
  этот closure: `pyproject.toml` version bumped
  `0.1.0` → `0.2.0`; README + PROJECT-STATUS + CHANGELOG
  обновлены под Track D closed.

Что Track D **реально закрыл** (на основе Steps 1–5
deliverables):

- documented `${ENV:NAME}` substitution path для DESIGNER
  credentials в `onec_*_command_template`-массивах;
  render-time resolution; fail-closed на missing / empty /
  mixed формах;
- redaction discipline: argv-элемент после `/P` / `/Pwd`
  редактируется на `<redacted>` в `command_preview` и
  trimmed excerpt'ах; actual subprocess argv остаётся
  unredacted (binary должен аутентифицироваться);
- migration: env-substitution стал рекомендованным
  default'ом, literal cleartext остался supported как
  legacy fallback — backward-compat сохраняется;
- release-verify scope расширен 8-м credential-template-
  hygiene check'ом, который ловит наиболее очевидный
  паттерн утечки (literal `/P "<value>"` без
  env-substitution или `<password>` placeholder'а) как
  WARN, не блокируя release flow.

Что Track D **не делает** «enterprise security platform»
после closure (honest constraints, никаких скрытых гэпов):
никакого secrets manager / vault / KMS / cloud secrets
service / OS keychain integration / encrypted-at-rest
secrets format; никакого SSO / RBAC / multi-tenant
identity; никакого federated audit storage /
policy-as-code DSL; никакого production-grade MCP
transport / auth; никакого GUI installer wizard / signed
distribution / package-manager publication / web-UI /
dashboard; никакой multi-version 1С matrix / AST-парсер /
hot reload / новых MCP tools / 1cv8 binary changes. Эти
направления остаются за пределами Track A + Track B +
Track C + Track D.

Registry-инвариант сохранён точно на всём треке: `read=15 /
write=25 / intelligence=16`, `selfcheck_status=ok`.
Никаких реальных credentials ни в одном из шести Track D
commit'ов. **GitHub remote push** не часть Track D — repo
готов к выкладке, но пушить — operator action.

## Track C detail (закрыт)

**Цель Track C** была — довести существующий продукт до
состояния, в котором его удобно передать другому человеку
как **packaged unit / process**: release-facing layout
polish, reproducible install sequence checklist, pre-
handoff sanity check, release handoff документация,
единый release entrypoint map. Это **не** новый execution-
core sprint, **не** enterprise track, **не** GUI installer
wizard, **не** signed binary distribution, **не** package-
manager publication. Шесть шагов; production-код Track C
вообще **не правил**.

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-c-packaging-installer-delivery-plan.md`](docs/architecture/track-c-packaging-installer-delivery-plan.md),
  [`docs/architecture/track-c-packaging-installer-delivery-step-map.md`](docs/architecture/track-c-packaging-installer-delivery-step-map.md)):
  назначение трека, целевой результат, guardrails,
  10 acceptance criteria, явный список «что НЕ входит»;
  commit `af2d7f4`.
- **Step 2 (release-facing verify path and layout polish)** —
  [`scripts/release/verify-release.ps1`](scripts/release/verify-release.ps1)
  как pre-handoff sanity check (read-only: проверяет
  наличие entry points, dev-check workflow, planning docs,
  printing concise human-readable report); расширение
  [`scripts/release/README.md`](scripts/release/README.md)
  под трёх-entrypoint surface (install / verify / dev
  launch). Production-код не правил; commit `ef087c8`.
- **Step 3 (packaging-facing install flow honest review)** —
  честный review `pyproject.toml`: добавлен явный
  block-комментарий о том, что
  `[tool.hatch.build.targets.wheel] packages = []` —
  намеренный no-op (Phase 6 продукт не предназначен для
  publication как single Python wheel из-за multi-app
  monorepo shape); расширение release/README с
  packaging story. Никакого фиктивного wheel build не
  ввели; commit `a4f42f9`.
- **Step 4 (release handoff documentation)** — новый
  документ [`docs/release-handoff.md`](docs/release-handoff.md)
  для receive-side оператора: что вы получили, system
  prerequisites, reproducible install sequence, verify
  sequence, known limitations honest table; commit
  `7ca9b3f`.
- **Step 5 (integration and handoff polish)** —
  минимальный pointer на `docs/release-handoff.md` в
  Quickstart-навигации root README; никакой broad docs
  rewrite; commit `8ccecf6`.
- **Step 6 (final integration pass and Track C closure)** —
  этот closure: README + PROJECT-STATUS + CHANGELOG
  обновлены под Track C closed.

Что Track C **не** делает «глубоким индустриальным
продуктом» после closure (honest constraints, никаких
скрытых гэпов): GUI installer wizard, `.msi` / `.deb` /
signed binary distribution, publication к package
managers (PyPI / Chocolatey / winget / apt), systemd /
Windows Service registration, hot reload, web-UI /
dashboard frontend, полный enterprise super-set (SSO/RBAC,
multi-tenant, secrets vault как сервис, federated audit
storage, policy-as-code DSL, multi-instance HA),
production-grade MCP transport, multi-version 1С matrix,
полный AST-парсер XML/BSL, полная rollback/delete-
вселенная, новые MCP tools, production code rewrite. Эти
направления остаются за пределами Track A + Track B +
Track C — открытие отдельных тематических parallel
track'ов под них — operator decision.

Registry-инвариант сохранён точно на всём треке: `read=15 /
write=25 / intelligence=16`, `selfcheck_status=ok`. **GitHub
remote push** не часть Track C — repo готов к выкладке, но
пушить — operator action.

## Track B detail (закрыт)

**Цель Track B** была — довести существующий продукт до
удобного **install / run / repo / release** состояния, не
открывая нового execution-core sprint'а и не входя в
enterprise-super-set. Шесть шагов; production-код Track B
вообще **не правил**.

- **Step 1 (planning)** — два planning-документа
  ([`docs/architecture/track-b-productization-polish-plan.md`](docs/architecture/track-b-productization-polish-plan.md),
  [`docs/architecture/track-b-productization-polish-step-map.md`](docs/architecture/track-b-productization-polish-step-map.md)):
  назначение трека, целевой результат, guardrails,
  10 acceptance criteria, явный список «что НЕ входит».
- **Step 2 (repo hygiene + legal layer)** — `git init` на
  `main`, расширенный `.gitignore` под snapshot trees /
  audit dirs / live dump trees / runtime state / 1С DB-
  файлы / writable configs / scratch dirs;
  [`LICENSE`](LICENSE) (Apache-2.0, полный стандартный
  текст); [`CHANGELOG.md`](CHANGELOG.md);
  [`SECURITY.md`](SECURITY.md) (reporting flow + honest
  constraints + safety guarantees); первый meaningful
  commit `85a4a7e`.
- **Step 3 (operator-discoverable install fast path)** —
  тонкий PowerShell wrapper [`scripts/release/install.ps1`](scripts/release/install.ps1)
  поверх существующего `run_install_fast_path` из
  Phase 6 / Step 3, плюс `_install_runner.py` и
  [`scripts/release/README.md`](scripts/release/README.md).
  Production-код не правил.
- **Step 4 (operator/dev local launch umbrella)** —
  [`scripts/dev/launch.ps1`](scripts/dev/launch.ps1) с
  четырьмя subcommands (`selfcheck` / `repl` / `run` /
  `help`); добавлена секция в
  [`scripts/dev/README.md`](scripts/dev/README.md).
  Production-код не правил.
- **Step 5 (root README quickstart and docs polish)** —
  верхний `## Quickstart` блок в этом README с install /
  check / launch командами и map'ом deeper docs.
- **Step 6 (final integration pass and Track B closure)** —
  этот closure: README + PROJECT-STATUS + CHANGELOG
  обновлены под Track B closed.

Что Track B **не** делает «глубоким индустриальным продуктом»
после closure (honest constraints, никаких скрытых гэпов):
production-grade MCP transport (нет authentication /
authorisation / network hardening), full installer ecosystem
(`.msi` / `.deb` / GUI wizard / signed distribution),
web-UI / dashboard frontend, полный enterprise super-set
(SSO/RBAC, multi-tenant, secrets vault как сервис, federated
audit, policy-as-code DSL, multi-instance HA), hot reload /
OS-level service supervision, multi-version matrix smoke,
полный AST-парсер XML/BSL, полная rollback/delete-вселенная,
новые MCP tools, production code rewrite. Эти направления
остаются за пределами Track B — открытие отдельных тематических
parallel track'ов под них — operator decision.

Registry-инвариант сохранён точно на всём треке: `read=15 /
write=25 / intelligence=16`, `selfcheck_status=ok`. **GitHub
remote push** не часть Track B — repo готов к выкладке, но
пушить — operator action.

## Track A detail (закрыт)

- **Parallel Track A — Full Real 1cv8-backed Write Path
  (закрыт на Step 7).**
  Цель — **доведение существующего write-core до finished
  real-write behavior**, а не новый MCP-surface sprint.
  Конкретно:
  - `apply_config_from_files` и
    `update_database_configuration` сегодня остаются
    Phase 2 stub-backed. Track A переводит их на honest
    dual-mode contract с real binary-backed dispatch'ем
    при наличии operator-declared argv-template'ов;
    config-time fallback на stub при отсутствии binary
    contract'а сохраняется без изменений; runtime-failure
    при non-zero exit subprocess'а — honest failure без
    silent stub fallback'а;
  - `create_dump_snapshot` (binary-backed branch которого
    был ship'нут на Phase 6 / Step 2) нормализуется
    под общий shared payload-контракт со всеми тремя
    binary-backed write-tool'ами;
  - Один **реальный multi-step round-trip** на reference
    stand'е с настоящим 1cv8 binary'ом (real DumpCfg →
    real apply (LoadCfg) → real UpdateDBCfg) выполняется
    end-to-end и фиксируется как воспроизводимый
    runbook;
  - Существующие product-layer boundary'и
    (`run_guided_workflow`, `run_rollback_assistant`,
    `run_real_stand_smoke_test`,
    `inspect_enterprise_foundation`) используются
    поверх real write path **без правок собственной
    логики** — весь real binary-backed dispatch живёт
    в write-server'е, не в product layer'е.

Это **post-phase completion track**, **не** новая Phase 7.
Безопасность Phase 1–6 не размывается:
`run_write_flow` остаётся единственным mutating-путём,
intelligence-server остаётся read-only,
`onec_policy_engine` не импортируется в
product/intelligence, нет back-door write channel'а из
product layer'а, нет `shell=True`, audit append-only,
fail-closed по умолчанию. Default trek'а — registries
остаются `read=15 / write=25 / intelligence=16` без
изменений; любое отклонение honestly мотивируется в
шаговом документе.

План трека и step-map: [`docs/architecture/track-a-real-write-path-plan.md`](docs/architecture/track-a-real-write-path-plan.md),
[`docs/architecture/track-a-real-write-path-step-map.md`](docs/architecture/track-a-real-write-path-step-map.md).
Step 1 (planning), **Step 2 (real binary-backed
`apply_config_from_files` contract)**, **Step 3 (real
binary-backed `update_database_configuration` contract)**,
**Step 4 (internal unification of binary-backed write
contract)** и **Step 5 (product-layer integration over
real write path)** — пройдены. Step 2 расширил
`EnvironmentConfig` полем `onec_applycfg_command_template`;
Step 3 — симметричным полем `onec_updatedb_command_template`
(loader fail-closed на bad shape; placeholder whitelist
tighter — без `{output_path}` / `{source_dump_path}`,
поскольку UpdateDBCfg операционно работает на живой
инфобазе). `apply_config_from_files(...)` и
`update_database_configuration(...)` оба переведены на
dual-mode dispatcher с одной и той же дисциплиной:
config-time fallback на stub при отсутствии binary
contract'а; binary-backed branch при наличии (реальный
subprocess через `onec_process_runner.run_process`,
captured stdout/stderr, timeout 300 s); runtime failure
в binary-backed ветке = honest failure без silent
fallback'а на stub. **Step 4 — internal-only refactor:**
все три binary-backed write-tool'а
(`create_dump_snapshot`, `apply_config_from_files`,
`update_database_configuration`) теперь сидят на одном
shared internal helper layer (новый internal модуль
`apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`
— excerpt cap, default timeout, render-time placeholder
substitution engine, stub/render-fail/start-fail/
binary-backed payload field assembly, shape verify
helper); три duplicated константы
(`_*_OUTPUT_EXCERPT_LIMIT`) и три duplicated константы
(`_*_DEFAULT_TIMEOUT_SECONDS`) удалены, единые источники
правды теперь в `binary_dispatch`. Tool-specific
placeholder whitelists остаются **per-tool** (намеренно
не объединены в superset). Дополнительно Step 4 закрыл
payload-discipline gap у `create_dump_snapshot`: до
refactor'а несколько ветвей (stub success, render-fail,
PlatformError-fail, dump-meta-fail, mkdir-fail) не несли
всех шести honest-mode полей; теперь **каждая** ветка
**каждого** из трёх tool'ов несёт все шесть
(`mode`, `binary_invoked`, `exit_code`,
`command_preview`, `stdout_excerpt`, `stderr_excerpt`)
честно (`None` / `False` где не применимо). **Step 5 —
product-layer surface-only update:** boundaries в
`apps/platform` теперь честно отражают, что real write
path есть для всех трёх binary-backed write-tool'ов.
Q7 закрыт: `run_real_stand_smoke_test(...)` plan summary
(и module docstring) больше не утверждают "Phase 2
stubs are NOT rewritten"; вместо этого summary честно
называет три tool'а с their honest dual-mode contract'ом
после Track A / Steps 2–4, явно отмечает что smoke сам
по себе остаётся bounded probe и что multi-step
round-trip — это Track A / Step 6, а не этот surface.
Q8 закрыт: `inspect_enterprise_foundation(...)` теперь
оценивает binary section по полному real-write
contract'у — `onec_binary_path` плюс **три** command
template'а (dumpcfg, applycfg, updatedb), score range
0..4. На prod-like config'ах отсутствие любого из трёх
template'ов — error finding с recommended_actions; на
non-prod — presumed warning. `foundation_level='strong'`
требует full-contract + чистые остальные секции.
Step 1–4 product-config'и без apply/updatedb template'ов
продолжают загружаться без изменений. Никаких новых MCP
tool'ов, никаких изменений в registries (read=15 /
write=25 / intelligence=16), никаких импортов
`onec_policy_engine` из product layer'а, никаких
изменений `onec-config` schema (full contract уже
существовал после Steps 2–3 — Step 5 только начал
**использовать** его в product surface'е). Operator-facing
ToolResult shape / argv grammar — без изменений.
**Step 6 (reference stand multi-step round-trip) —
закрыт.** Operator-driven exercise по runbook'у
`docs/runbooks/track-a-reference-stand-round-trip.md`
прошёл honestly на real 1cv8 binary'е
(`C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe`)
и реальной file-based инфобазе InfoBase6
(`C:/Users/user/Documents/InfoBase6`). Все три
binary-backed write-tool'а отработали зелёным:
A.2 — `create_dump_snapshot` через
`/DumpConfigToFiles` (`mode='binary-backed'`,
`binary_invoked=True`, `exit_code=0`); A.4 —
`apply_config_from_files` через `/LoadConfigFromFiles`
(`stage='completed'`, mutating audit row написан);
A.5 — `update_database_configuration` через
`/UpdateDBCfg` (`stage='completed'`, mutating audit
row написан). На диске реальный
`Configuration.xml` + поддиректории, два backup
snapshot'а перед mutating операциями, два pre-mutating
dump-snapshot'а (созданы `run_write_flow`'ом
автоматически), и **две** append-only audit row'и
для двух mutating операций. Standalone
`create_dump_snapshot` audit row не пишет by design —
он не идёт через `run_write_flow`; pre-apply /
pre-updatedb dump подтверждается через
`details.dump_snapshot_path` mutating row'и. Runbook +
local closure logic выровнены под фактическое
поведение (две mutating audit row + dump_snapshot_path
в details). Никаких production-правок Step 6 не
делал — dual-mode contract уже введён Track A /
Steps 2–4, unified `binary_dispatch` уже на месте,
product-layer surface уже обновлён Step 5. **Step 7
(final integration pass and Track A closure) —
закрыт без production-правок:** existing evidence
Step 6 round-trip'а покрывает acceptance criteria
1–5 (full real binary-backed contract, multi-step
real round-trip, product-layer integration, no
silent fallback, honest payload discipline);
discipline asserts criteria 6–10 удовлетворены
(registries `read=15 / write=25 / intelligence=16`
без drift'а; ноль импортов `onec_policy_engine` под
`apps/platform/src` и
`apps/mcp-intelligence-server/src`; нет back-door
write channel'а; operator-facing messages честные;
Track A closed как documented status). Закрытие
выполнено только обновлением closure-status в
`README.md` и `PROJECT-STATUS.md` — никаких новых
запусков 1cv8.exe для Step 7 не понадобилось.

Что **не** входит в Track A (и **остаётся** будущей
работой после закрытия трека): enterprise super-set
(SSO/RBAC, multi-tenant, secrets vault, federated
audit, policy-as-code, multi-instance HA), web-UI,
полный AST-парсер, полная metadata-вселенная, полная
rollback/delete-вселенная, production-grade MCP
transport, packaging ecosystem, multi-version matrix
в полном объёме. Эти направления остаются **другими**
parallel track'ами после Phase 6 / Track A — Track A
их не открывал и не закрывал. После закрытия Track A
ни один из них автоматически не открывается;
открытие следующего трека — отдельное решение
оператора проекта.

Что Track A **реально закрыл** (на основе Steps 2–7
и Step 6 evidence на InfoBase6):

- real binary-backed dispatch для **всех трёх** ранее
  stub-backed-путей (`create_dump_snapshot`,
  `apply_config_from_files`,
  `update_database_configuration`);
- final contract correctness: один shared
  `binary_dispatch` helper, per-tool placeholder
  whitelists, fail-closed на unknown placeholder,
  fixed timeout cap;
- no silent fallback: при non-zero exit
  binary-backed branch'а tool возвращает honest
  `ok=False` с populated `mode='binary-backed'` /
  `exit_code != 0`, без тихого downgrade'а на
  stub;
- honest payload discipline: каждая ветка каждого
  из трёх tool'ов несёт все шесть unified
  honest-mode полей (`mode`, `binary_invoked`,
  `exit_code`, `command_preview`, `stdout_excerpt`,
  `stderr_excerpt`);
- reference-stand execution layer proven: real
  multi-step round-trip отработал на InfoBase6, audit
  honest, snapshot trees физически на диске.

Что Track A **не делает** «готовым индустриальным
продуктом** даже после closure: операторские
credentials всё равно out-of-band (не в config),
multi-version matrix на всех 1С версиях не пройдена
(закрыт single-version smoke на 8.3.27.1859),
production runbook ecosystem не построен
(один reference-stand runbook), packaging /
installer / signed distribution не сделан,
enterprise super-set не открыт, web-UI / dashboard
frontend не сделан, полная rollback-вселенная не
покрыта (whitelist расширен до 6 tools после
Track F / Step 4 — `add_catalog_attribute`,
`add_document_attribute`, `add_form_attribute`,
`add_form_element`, `append_module_method`,
`replace_module_method_body` — но это всё ещё
narrow set, 6 of 25 mutating tools; multi-file /
DB-schema / `create_*` / public `delete_*`
остаются categorically out-of-scope),
полный AST-парсер XML/BSL не написан. Это
явные honest constraints, **не** скрытые гэпы.

Документы parallel-track'ов:

- `docs/architecture/track-a-real-write-path-plan.md` —
  план **Parallel Track A — Full Real 1cv8-backed Write
  Path**: post-phase completion track для доведения
  оставшихся Phase 2 stub-backed-путей
  (`apply_config_from_files`,
  `update_database_configuration`) до honest dual-mode
  contract'а с real binary-backed dispatch'ем; нормализация
  `create_dump_snapshot` real path'а под общий
  payload-контракт; один реальный multi-step round-trip на
  reference stand'е. Не Phase 7. Без расширения MCP
  surface'а.
- `docs/architecture/track-a-real-write-path-step-map.md`
  — семь шагов: planning (documentation entry) → real
  apply → real update-db → unify dump-snapshot + payload
  discipline → product-layer integration → reference stand
  round-trip → final integration pass + closure.

Архивные планы:

- `docs/architecture/phase-6-industrialization-plan.md` —
  план **Phase 6 — Industrialization & Completion Track**
  (исходник — пройден).
  Это **не** очередное расширение MCP tool surface и **не**
  ещё один технический MVP — это специально выделенная
  фаза доведения продукта до **finished / deployable**
  состояния поверх уже готового ядра Phase 1–5: реальный
  1cv8-backed dispatch (хотя бы для одного Phase 2
  stub-backed пути), исполнимый rollback хотя бы для
  одного класса write-tool'ов, короткий install/setup
  сценарий, real-stand end-to-end smoke на reference
  stand'е, runtime hardening (логи, restart policy),
  operator/admin/developer manuals + runbooks как
  standalone docs, foundation для enterprise-трека (без
  полного enterprise-супер-сета). Шесть продуктовых
  блоков (A — real 1cv8 execution; B — full rollback /
  recovery; C — installer / packaging; D — metadata
  completion / structural editing; E — runtime
  hardening; F — operator UX / docs / runbooks; G —
  enterprise foundation). 10 проверяемых критериев
  приёмки. Явный «что НЕ входит в фазу» (полная
  enterprise-вселенная, AST-парсер всей кодовой базы,
  web-UI, multi-instance HA — out of Phase 6 scope).
- `docs/architecture/phase-6-step-map.md` — стартовый
  implementation map (8 шагов): planning → real 1cv8
  contract → installer → rollback execution → metadata
  completion → runtime hardening → real-stand validation
  + docs → final integration pass.

## По какому документу ведётся работа

Разработка ведётся строго по внутреннему **ТЗ v1.1**. Все решения по структуре,
именам пакетов и границам ответственности согласованы с этим документом.

## Структура репозитория

```
1c-agent-platform/
├── apps/         # Исполняемые MCP-серверы (read / write / intelligence)
├── packages/     # Переиспользуемые библиотеки платформы
├── docs/         # Архитектура, спецификации, безопасность, runbooks, API
├── examples/     # Демонстрационные инфобазы, дампы, примеры патчей
└── scripts/      # Скрипты для разработки, тестов и релизов
```
