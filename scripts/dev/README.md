# scripts/dev

Скрипты для локальной разработки 1C Agent Platform.

На текущем этапе это временный bootstrap для монорепы: настоящий
packaging / workspace setup (editable install, workspace discovery)
появится позже. Пока используем три скрипта.

## Содержимое

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
import/wiring skeleton-модулей, без реального MCP-рантайма,
интеграции с 1С, pytest, ruff или установки пакетов.

## Статус

Это временный bootstrap-этап до появления нормального packaging/workspace
setup (editable install, workspace discovery, CLI-скрипты и т.п.).
