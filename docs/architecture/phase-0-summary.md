# Phase 0 Summary

## Назначение фазы

Собрать инфраструктурную базу 1C Agent Platform: структуру монорепозитория,
общие контракты, skeleton трёх MCP-серверов и воспроизводимый локальный
quality gate. Без реального MCP-рантайма и без интеграции с 1С.

## Что собрано

- **Монорепозиторий** — `apps/`, `packages/`, `docs/`, `examples/`,
  `scripts/`, корневые `README.md`, `PROJECT-STATUS.md`, `.gitignore`,
  `.editorconfig`, `.python-version`.
- **Root bootstrap** — минимальный `pyproject.toml` (hatchling, базовые
  настройки `ruff` и `pytest`), per-package `src/__init__.py` и README.
- **Общие пакеты** — `mcp-common` (контексты, иерархия исключений,
  shared `ToolResult`, registry helpers), `onec-process-runner`,
  `onec-policy-engine`, `onec-audit`, `onec-health`, `onec-troubleshooting`,
  `onec-config`. Везде skeleton уровня контрактов.
- **Skeleton трёх серверов** — `mcp-read-server`, `mcp-write-server`,
  `mcp-intelligence-server`: общий response envelope, registry через
  shared helpers из `mcp-common`, `ping` у каждого, `health_summary`
  у read-server поверх `onec-health` + `onec-troubleshooting`.
- **Dev bootstrap и selfcheck** — `scripts/dev/bootstrap_paths.ps1`
  (per-session `PYTHONPATH`, 10 `src/` путей, ничего не трогает в
  системе) и `scripts/dev/selfcheck.py` (импорт всех skeleton-модулей,
  безопасные вызовы базовых функций, печать компактного отчёта, без
  `try/except`).
- **CI skeleton** — `.github/workflows/dev-check.yml`: один job
  `dev-check` на `windows-latest`, Python 3.11, bootstrap + selfcheck.
  Без установки пакетов, pytest, ruff и matrix.
- **Единая команда локальной проверки** — `scripts/dev/run_dev_check.ps1`:
  dot-source bootstrap + запуск selfcheck, при успехе печатает
  `Dev check completed successfully.`
- **Runbook локальной проверки** — `docs/runbooks/local-dev-check.md`:
  цель, prerequisites, команда запуска, критерии успеха, типовые падения.

## Что подтверждено на практике

- `bootstrap_paths.ps1` корректно выставляет `PYTHONPATH` в текущую сессию;
  все 10 `src/` путей монорепо видны Python'у.
- `selfcheck.py` проходит с `selfcheck_status = ok` на реальном
  Python 3.11+.
- Все три MCP-сервера импортируются и отдают свои registry-составы
  (`read = ['health_summary', 'ping']`, `write = ['ping']`,
  `intelligence = ['ping']`).
- Skeleton wiring `mcp-read-server → onec-health → onec-troubleshooting`
  работает: `health_summary` с заведомо плохими входами возвращает
  `ok = false` и корректный `problem_code = gateway_down`.
- Shared `ToolResult` и registry helpers из `mcp-common` используются
  всеми тремя серверами через compatibility wrappers в их `models.py`
  и через `build_tool_registry` / `list_registered_tools` /
  `get_registered_tool` в их `server.py`.

## Что пока ещё не реализовано

- Реальный MCP runtime (транспорт, регистрация инструментов во внешнем
  MCP-хосте).
- Реальные вызовы 1С (HTTP-адаптер, подключение к инфобазе, работа с
  публикацией).
- Реализация `onec-process-runner` (сейчас `run_process` — stub,
  поднимает `NotImplementedError`).
- Реальные health checks (сейчас все три проверки — stub, работают на
  булевых входах).
- Read-tools Phase 1 (`get_configuration_info`, `get_metadata_tree`,
  `search_code`, `execute_read_query` и т.д.).
- Write-логика (policy enforcement, backup/dump/apply/verify, аудит).
- Intelligence-логика (анализ зависимостей, impact analysis,
  troubleshooting поверх реальных журналов).

## Вывод по фазе

Phase 0 считается завершённой. Инфраструктурная база 1C Agent Platform
готова для входа в Phase 1: каркас монорепо, shared контракты, skeleton
трёх серверов, воспроизводимый dev-check локально и в CI. Дальнейшие
шаги — реальная функциональность Read MVP.
