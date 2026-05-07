# Runbook: локальная dev-проверка skeleton-проекта

## Цель

Убедиться, что текущий skeleton 1C Agent Platform корректно собран локально:
все внутренние модули импортируются, registry трёх MCP-серверов читается,
health/troubleshooting wiring работает.

Это минимальный quality gate Phase 0. Он не проверяет реальный MCP-рантайм,
интеграцию с 1С, Apache или внешние сервисы.

## Prerequisites

- Python 3.11+ установлен и доступен в PATH как `python`.
- Windows PowerShell доступен.
- Репозиторий склонирован в `C:\Tools\1c-agent-platform`
  (или в другой каталог — команда работает от расположения самого скрипта).

## Команда запуска

В PowerShell-сессии:

```powershell
. "C:\Tools\1c-agent-platform\scripts\dev\run_dev_check.ps1"
```

Скрипт dot-source'ит `bootstrap_paths.ps1` и запускает
`scripts/dev/selfcheck.py` в текущей сессии.

## Что считается успешным результатом

В выводе должны присутствовать обе строки:

- `selfcheck_status = ok` — от `selfcheck.py`;
- `Dev check completed successfully.` — от `run_dev_check.ps1`.

## Типовые падения

- **`python` не установлен / указывает на Microsoft Store alias stub.**
  В PATH лежит заглушка, которая не запускает код. Установить настоящий
  Python 3.11+ и убедиться, что `python --version` возвращает реальную
  версию.
- **`PYTHONPATH` не выставился.**
  Обычно значит, что `bootstrap_paths.ps1` не был dot-source'нут
  (запущен как `./bootstrap_paths.ps1` вместо `. ./bootstrap_paths.ps1`).
  Переменная окружения ставится только на текущую сессию PowerShell.
  Использовать `run_dev_check.ps1` — он делает dot-source сам.
- **`ModuleNotFoundError` на одном из skeleton-модулей.**
  Значит, сломался wiring в `apps/` или `packages/`. Проверить, что все
  пакеты на месте и их `src/` пути действительно попадают в `PYTHONPATH`
  (вывод `bootstrap_paths.ps1` печатает полный список путей).
