# scripts/dev

Скрипты для локальной разработки 1C Agent Platform.

На текущем этапе это временный bootstrap для монорепы:
editable install и workspace discovery всё ещё out of scope. Track M /
Step 4 ввёл узкий supported distribution boundary — один buildable
`py3-none-any` wheel (см.
[`docs/operators/packaging/distribution-boundary.md`](../../docs/operators/packaging/distribution-boundary.md)),
но он покрывает `pip install` deployment flow, не dev-time editable
install.

Если ты только пришёл в проект — начни с `launch.ps1` (умbrella-вход
в типовые локальные действия). Остальные скрипты ниже — это нижний
слой, на который `launch.ps1` ссылается.

## Содержимое

### `launch.ps1`

Operator/dev umbrella для типовых локальных действий. Track B /
Step 4. Тонкий PowerShell-диспетчер поверх `bootstrap_paths.ps1`
и `run_dev_check.ps1`; никакой новой бизнес-логики не вводит.

Subcommands:

```powershell
.\scripts\dev\launch.ps1 selfcheck         # эквивалент run_dev_check.ps1
.\scripts\dev\launch.ps1 repl              # interactive Python REPL с PYTHONPATH
.\scripts\dev\launch.ps1 run <script> [args...]   # ad-hoc Python script
.\scripts\dev\launch.ps1 help              # usage
```

Без аргументов или с `help` печатает usage. Exit codes: `0` —
success / help; делегированный `$LASTEXITCODE` для `selfcheck` /
`run`; `64` — unknown command или missing args.

`launch.ps1` сознательно **не** делает: не стартует MCP-серверы
(каждый сервер запускается оператором отдельно через
`python -m <pkg>`; Track G / Step 4 ship'нул local stdio baseline,
Track H / Step 4 добавил narrow HTTP/1.1 `/mcp` endpoint c static
bearer authentication — `--transport stdio` для local subprocess
deployment без auth или `--transport http --bind HOST:PORT
--auth-token-env VARNAME` для trusted-network deployment behind
operator's reverse proxy; in-process TLS не предоставляется), не
запускает pytest (нет test suite'а), не делает install fast path
(см. `scripts/release/install.ps1`, Track B / Step 3), не трогает
1С-инфобазу.

### `bootstrap_paths.ps1`

PowerShell-скрипт, который выставляет `PYTHONPATH` для текущей сессии так,
чтобы Python видел все `src/` каталоги монорепо: три приложения из `apps/`
и семь пакетов из `packages/`. Ничего не трогает в системе — ни PATH,
ни реестр. Живёт только в текущем процессе PowerShell.

Запуск (dot-source, чтобы `$env:PYTHONPATH` остался в текущей сессии):

```powershell
. .\scripts\dev\bootstrap_paths.ps1
```

### `selfcheck.py`

Минимальный self-check, который:

- импортирует все skeleton-модули платформы
  (`mcp_read_server`, `mcp_write_server`, `mcp_intelligence_server`,
  `onec_policy_engine`, `onec_audit`, `onec_config`, `onec_health`,
  `onec_troubleshooting`);
- вызывает их базовые функции (`ping`, `list_tools`, `check_write_allowed`,
  `summarize_health`, `diagnose_from_health`, `load_project_config`,
  `format_audit_record`) на безопасных данных;
- печатает компактный отчёт с ключевыми полями и `selfcheck_status = ok`.

Скрипт сознательно не оборачивает вызовы в `try/except`: если wiring
неверный, мы хотим честную, громкую ошибку.

Запуск (после `bootstrap_paths.ps1` в той же сессии):

```powershell
python .\scripts\dev\selfcheck.py
```

### `mcp_client_smoke.py`

Track K / Step 4 closure-gate harness: stdlib-only
minimum-viable MCP client smoke. Exercises the platform's
existing MCP server surface (`mcp-read-server` /
`mcp-write-server` / `mcp-intelligence-server`)
end-to-end via JSON-RPC 2.0 over both `--transport stdio`
и `--transport http`. Не модифицирует ни один файл
production-кода и ни одну MCP tool registration.

Что делает:

- запускает выбранный MCP server как subprocess через
  `python -m <module>`;
- speaks JSON-RPC 2.0 over stdin/stdout (stdio path)
  или `POST /mcp` через stdlib `urllib.request` (HTTP
  path);
- выполняет `initialize` → `tools/list` → один
  read-only `tools/call` с synthetic empty arguments;
- asserts envelope shape (`protocolVersion =
  "2024-11-05"`; non-empty `serverInfo.name` /
  `version`; non-empty `tools` list; well-shaped
  `result` или well-shaped `error` envelope —
  contract §7.1.4 принимает оба как valid evidence);
- для HTTP path дополнительно выполняет missing-
  `Authorization` probe asserting `401` +
  `WWW-Authenticate: Bearer realm="mcp"` + JSON-RPC
  `error.code == -32001` (failure-equivalence per
  Track H §6 / §8);
- генерирует synthetic bearer token через
  `secrets.token_urlsafe(32)` at run time; token value
  **никогда** не печатается;
- ephemeral port discovery через
  `socket.bind(("127.0.0.1", 0))`;
- clean subprocess shutdown (close-stdin →
  `terminate` → kill-on-timeout escalation; no orphan
  processes);
- финальная строка `OK (server=... transport=...)`
  на success; exit code 0 на success, non-zero на
  assertion failure.

CLI:

```powershell
python .\scripts\dev\mcp_client_smoke.py --server read --transport both
python .\scripts\dev\mcp_client_smoke.py --server write --transport stdio
python .\scripts\dev\mcp_client_smoke.py --server intelligence --transport http
```

- `--server {read,write,intelligence}` — какой MCP
  server exercise'ить. По умолчанию `read` (mandatory
  closure-gate target per contract §3.4); другие
  значения = recommended-only spot coverage.
- `--transport {stdio,http,both}` — какой transport(s)
  exercise'ить. По умолчанию `both`.

PYTHONPATH не обязателен заранее: harness строит свой
собственный PYTHONPATH для subprocess (mirrors
`bootstrap_paths.ps1`'s 11 src paths) если он не
выставлен parent сессией.

Что harness сознательно **не** делает:

- не модифицирует production-код, `pyproject.toml`,
  registries, или существующие `scripts/*` файлы;
- не добавляет new dependencies (stdlib-only —
  `argparse`, `json`, `os`, `secrets`, `socket`,
  `subprocess`, `urllib.request`/`urllib.error`,
  `time`, `contextlib`, `pathlib`);
- не импортирует `mcp_common._stdio_transport` или
  `mcp_common._network_transport` (server-side
  internals); работает через wire (subprocess pipes /
  HTTP);
- не запускает `1cv8.exe` и не трогает 1С-инфобазу;
- не делает remote push.

Это **не** "client integration solved" / "production-
ready client compatibility" / "interop fully proven" /
"all clients supported" — harness exercises только
narrow minimum scenario (`initialize` + `tools/list` +
один read-only `tools/call` + HTTP 401 probe) и его
job — produce byte-replayable closure-gate evidence,
не establish broader QA framework. Per Track K Step 3
contract §9 (PATH B pinned) / §10.1 (this file
location pinned) / §13 (honest non-goals).

### `run_dev_check.ps1`

Единая команда локальной проверки skeleton-проекта. Dot-source'ит
`bootstrap_paths.ps1` в текущей сессии и запускает `selfcheck.py`.
При успехе печатает `Dev check completed successfully.`, при ошибке
завершается с тем же exit code, что и Python.

Запуск:

```powershell
. .\scripts\dev\run_dev_check.ps1
```

Тот же сценарий (bootstrap + selfcheck) повторяется в минимальном
CI workflow `.github/workflows/dev-check.yml`. На текущем этапе это
единственный quality gate проекта — он проверяет только
import/wiring skeleton-модулей и registry counts, без запуска
живого MCP-рантайма (Track G / Step 4 stdio entrypoints
запускаются оператором отдельно — см. выше про `launch.ps1`),
без интеграции с 1С, без pytest / ruff / установки пакетов.

## Статус

Это временный bootstrap-этап. Track M / Step 4 закрыл deploy-time
packaging boundary (один buildable wheel, см.
[`docs/operators/packaging/distribution-boundary.md`](../../docs/operators/packaging/distribution-boundary.md));
dev-time editable install, workspace discovery и CLI-скрипты под
local-dev workflow по-прежнему out of scope.
