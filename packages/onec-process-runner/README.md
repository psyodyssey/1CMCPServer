# onec-process-runner

Библиотека запуска внешних процессов для платформы 1C Agent Platform.
Используется read- и write-серверами как единая точка для вызова `1cv8`,
распаковщиков конфигурации и других внешних утилит.

## Что внутри

- `ProcessRunRequest` — описание запуска: `command`, `cwd`,
  `timeout_seconds`, `capture_output`, `text`, `env`, `input_text`.
- `ProcessRunResult` — результат: `exit_code`, `completed`, `stdout`,
  `stderr`.
- `run_process(request)` — реальный runner поверх `subprocess.run`.

Пакет больше не stub: `run_process` действительно выполняет внешний
процесс.

## Поведение

- Под капотом `subprocess.run`. **Никогда** не используются `shell=True`,
  `os.system` или ручной `Popen`.
- Поддерживаются `cwd`, `timeout_seconds`, подмена окружения через `env`
  и подача на stdin через `input_text`.
- **Нормальное завершение** — возвращается `ProcessRunResult` с
  `completed=True`, реальным `exit_code`, заполненными `stdout`/`stderr`.
- **Таймаут** (`subprocess.TimeoutExpired`) не выбрасывается наружу.
  Возвращается `ProcessRunResult(completed=False, exit_code=-1, ...)`
  с частично собранным `stdout`/`stderr`, к `stderr` добавляется
  короткая пометка о таймауте.
- **`FileNotFoundError`** (исполняемый файл отсутствует) преобразуется
  в `ProcessExecutionError` из `mcp_common` с понятным сообщением.
- Другие ошибки старта процесса (`OSError`, `PermissionError` и т.п.)
  также поднимаются как `ProcessExecutionError`.
- Ошибки не проглатываются: runner не логирует, не пишет файлы и не
  скрывает причины сбоев — решение о реакции принимает вызывающий код.

## Что не делает

- Не интерпретирует stdout/stderr под какой-либо формат 1С.
- Не знает про публикации, dump'ы и конкретные команды — это ответственность
  вышележащих слоёв.
- Не ведёт аудит вызовов (это делает `onec-audit`).
