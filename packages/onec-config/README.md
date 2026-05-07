# onec-config

Библиотека конфигурации платформы 1C Agent Platform. Держит рабочую
модель окружения тестовой базы, которой пользуются все серверы и пакеты
(`mcp-read-server`, `onec-health`, адаптеры live/dump и т.д.).

## Что внутри

- `EnvironmentConfig` — параметры одного окружения (инфобазы):
  - `name` — человекочитаемое имя окружения;
  - `base_id` — идентификатор базы в рамках проекта;
  - `base_path` — путь к файловой/серверной инфобазе;
  - `publication_name` — имя публикации на Apache/IIS;
  - `http_base_url` — базовый URL публикации;
  - `dump_path` — каталог распакованной выгрузки конфигурации;
  - `timeout_seconds` — общий таймаут операций с окружением
    (`int | float`);
  - `allow_write` — разрешение write-операций для этого окружения
    (по умолчанию `False`).
  - `onec_binary_path` (Phase 5 / Step 7, опц.) — абсолютный путь
    к исполняемому файлу 1cv8. По умолчанию `None`. Используется
    исключительно product-layer real-stand readiness / smoke
    boundary'ями; ни один read/write/intelligence MCP-tool на это
    поле не завязан.
  - `onec_binary_probe_args` (Phase 5 / Step 7, опц.) —
    operator-declared argv-tail для контролируемого binary
    probe. По умолчанию `None`. Если задан — должен быть
    `list[str]`. Платформа не подсказывает значения этих
    аргументов и не «угадывает» 1cv8 CLI: оператор знает свой
    стенд и сам выбирает безопасный probe.
  - `onec_dumpcfg_command_template` (Phase 6 / Step 2, опц.) —
    operator-declared **полный argv-template** для запуска
    1cv8 в режиме создания dump snapshot. По умолчанию
    `None`. Если задан — должен быть **non-empty** `list[str]`.
    Каждый item — строка; placeholders из небольшого
    whitelist'а (`{binary_path}` / `{output_path}` /
    `{base_path}` / `{base_id}` / `{publication_name}` /
    `{http_base_url}`) подставляются write-tool'ом
    `create_dump_snapshot` через безопасный
    `str.format(...)`-style рендер. Shell-строки не
    поддерживаются. Платформа **не угадывает** 1cv8 CLI
    grammar: оператор пишет точную argv, которую он хочет
    видеть исполненной. Когда это поле задано вместе с
    `onec_binary_path`, `create_dump_snapshot` переключается
    в binary-backed режим; иначе остаётся текущий
    Phase 2 / Step 5 stub без изменений.
  - `onec_applycfg_command_template` (Parallel Track A /
    Step 2, опц.) — operator-declared **полный
    argv-template** для запуска 1cv8 в режиме apply
    config from files (`LoadConfigFromFiles` semantics).
    По умолчанию `None`. Если задан — должен быть
    **non-empty** `list[str]`. Каждый item — строка;
    placeholders из небольшого whitelist'а
    (`{binary_path}` / `{source_dump_path}` /
    `{base_path}` / `{base_id}` / `{publication_name}` /
    `{http_base_url}`) подставляются write-tool'ом
    `apply_config_from_files` через безопасный
    `str.format(...)`-style рендер. Shell-строки не
    поддерживаются. Когда это поле задано вместе с
    `onec_binary_path`, `apply_config_from_files`
    переключается в binary-backed режим; иначе остаётся
    текущий Phase 2 / Step 7 stub-process apply без
    изменений. Whitelist отличается от dumpcfg только
    одним токеном — `{output_path}` заменён на
    `{source_dump_path}` (apply читает дамп, dumpcfg
    его пишет).
  - `onec_updatedb_command_template` (Parallel Track A /
    Step 3, опц.) — operator-declared **полный
    argv-template** для запуска 1cv8 в режиме update
    database configuration (`UpdateDBCfg` semantics).
    По умолчанию `None`. Если задан — должен быть
    **non-empty** `list[str]`. Каждый item — строка;
    placeholders из **более узкого** whitelist'а
    (`{binary_path}` / `{base_path}` / `{base_id}` /
    `{publication_name}` / `{http_base_url}`)
    подставляются write-tool'ом
    `update_database_configuration` через безопасный
    `str.format(...)`-style рендер. Shell-строки не
    поддерживаются. UpdateDBCfg операционно работает на
    живой инфобазе с уже-применённым config'ом, поэтому
    в whitelist'е **нет** ни `{output_path}` (нечего
    дампить), ни `{source_dump_path}` (нечего читать
    из source-tree); это сознательно более узкий
    surface, чтобы случайный typo (`{source_dump_path}`
    вместо чего-то ещё) был отвергнут на render-time.
    Когда это поле задано вместе с `onec_binary_path`,
    `update_database_configuration` переключается в
    binary-backed режим; иначе остаётся текущий
    Phase 2 / Step 9 stub-process update без изменений.

### Философия binary-related полей

Все пять полей (`onec_binary_path`,
`onec_binary_probe_args`, `onec_dumpcfg_command_template`,
`onec_applycfg_command_template`,
`onec_updatedb_command_template`) выражают
**operator-owned execution contract**: оператор
описывает, что и как платформа должна вызывать. Платформа
не имеет встроенных предположений о версиях 1cv8, режимах
запуска или о синтаксисе ключей — это знание остаётся в
конфиге окружения. Любая ошибка в этих полях даёт
fail-closed на этапе loader'а или на этапе вызова tool'а
(в зависимости от того, где она проявляется), без
silent fallback.

Отдельно про argv-templates
(`onec_dumpcfg_command_template`,
`onec_applycfg_command_template`,
`onec_updatedb_command_template`): **platform does not
guess 1cv8 CLI grammar**. Никаких захардкоженных
`/DumpCfg`, `/LoadCfg`, `/UpdateDBCfg`,
`/DisableStartupDialogs`, `/AllowedThicknesses` и т.п. в
коде платформы нет. Любой такой флаг пишется оператором
прямо в argv-template'е соответствующей операции.
Платформа просто запускает subprocess с этой argv (через
`onec-process-runner`, **без** shell — никакого
`shell=True`, никакой shell-string'ы поверх argv list'а).
Unknown placeholder внутри template'а — fail-closed на
render-time, до запуска subprocess'а.

Track A / Step 3 переводит на binary-backed dispatch
**только** `update_database_configuration`. Финальная
унификация payload-discipline между всеми тремя
binary-backed write-tool'ами (`create_dump_snapshot`,
`apply_config_from_files`, `update_database_configuration`)
— задача Track A / Step 4. До Step 4 каждый tool имеет
свой набор констант / render-функции / operation+verify
callable'ов; они симметричны по форме, но
независимы по реализации. Это сознательное анти-
расползание: общий helper-framework появляется только
тогда, когда у нас уже есть три рабочих по факту
независимых binary-backed branch'а.
- `ProjectConfig` — верхнеуровневая конфигурация:
  `environments: dict[str, EnvironmentConfig]`.
- `load_project_config(data)` — преобразование dict → `ProjectConfig`
  с валидацией структуры.

## Обязательные поля окружения

`name`, `base_id`, `base_path`, `publication_name`, `http_base_url`,
`dump_path`, `timeout_seconds`. Поля `allow_write`,
`onec_binary_path`, `onec_binary_probe_args`,
`onec_dumpcfg_command_template`,
`onec_applycfg_command_template`,
`onec_updatedb_command_template` опциональны (по умолчанию
`False` / `None` / `None` / `None` / `None` / `None`
соответственно).

## Поведение loader

- Если в входном dict'е нет ключа `environments` — `ValueError`.
- Если `environments` пустой — `ValueError`.
- Если в каком-то окружении отсутствует обязательное поле — `ValueError`
  с указанием имени окружения и имени отсутствующего поля.
- При валидном входе возвращается `ProjectConfig` с
  `EnvironmentConfig` по всем окружениям.

## Что пока ещё не реализовано

- Чтение конфигурации из файлов (YAML/JSON/TOML).
- Чтение из переменных окружения / `os.environ`.
- Слияние профилей (base + overlay).
- Секреты и их безопасная подстановка.

Всё это подключим позже; на текущем шаге `onec-config` — чистая,
синхронная валидация структуры dict без внешнего I/O.
