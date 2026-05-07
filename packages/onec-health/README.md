# onec-health

Библиотека проверок состояния инфобаз и окружения 1С. Используется
серверами платформы для предполётной диагностики и как источник
`problem_code` для `onec-troubleshooting`.

Пакет больше не чистый stub: HTTP- и dump-проверки теперь реальные,
а bool-совместимость сохранена для текущего skeleton selfcheck.

## Что внутри

- `HealthCheckResult` — результат одной проверки (`status`, `check_name`,
  `message`). Контракт не меняется.
- `check_dump_path_exists(path)` — проверка существования каталога
  выгрузки через `pathlib.Path`. Без сети.
- `check_http_gateway_available(target, timeout_seconds=None)` —
  реальный HTTP probe через `urllib.request`:
  - `target` как `bool` — legacy stub mode для selfcheck;
  - `target` как `str` — URL endpoint. `status="ok"` при HTTP 2xx/3xx,
    иначе `status="error"`. Таймаут пробрасывается в `urlopen`.
  - Сетевые исключения, таймауты и HTTP-ошибки не выходят наружу —
    всегда возвращается `HealthCheckResult`.
- `check_search_index_available(target)` — индикатор пригодности dump
  для code-search:
  - `target` как `bool` — legacy stub mode;
  - `target` как `str` — путь к каталогу выгрузки. `status="ok"`, если
    каталог существует и рекурсивно найден хотя бы один файл `.bsl`.
  - Имя `search_index` условное; `summarize_health` по этому check_name
    выдаёт `index_lock` при ошибке.
- `check_environment_health(environment)` — helper, запускающий три
  базовые проверки по `EnvironmentConfig` из `onec-config`:
  `check_dump_path_exists(environment.dump_path)`,
  `check_http_gateway_available(environment.http_base_url,
  environment.timeout_seconds)`,
  `check_search_index_available(environment.dump_path)`. Возвращает
  список из трёх `HealthCheckResult` в стабильном порядке.
- `summarize_health(results)` — агрегатор problem codes, остаётся
  как был: `dump_missing`, `gateway_down`, `index_lock` или `["ok"]`.

## Что не делает

- Не поднимает реальный HTTP-сервер — только GET к уже существующему
  endpoint'у.
- Не запускает процессы 1С (это ответственность `onec-process-runner`).
- Не решает, что делать с ошибкой — решение принимает вызывающий код
  (в перспективе — `onec-troubleshooting` и read-server adapter).
- Не ведёт аудит вызовов.
