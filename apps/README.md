# apps/

Исполняемые приложения платформы 1C Agent Platform.

В этом разделе живут самостоятельные приложения, у каждого из которых
своя зона ответственности и свой контракт:

- `mcp-read-server` — read-only MCP-сервер: чтение конфигурации,
  метаданных, кода, журналов, диагностика окружения.
- `mcp-write-server` — write MCP-сервер: контролируемые правки
  через единый `run_write_flow` (preflight → snapshots →
  operation → verify → audit), включая metadata-level операции
  Phase 3.
- `mcp-intelligence-server` — read-only intelligence MCP-сервер:
  dependency / impact / diagnostics / recommendations поверх
  read- и write-runtime'ов.
- `platform` — продуктовый слой Phase 5: product-config schema,
  prereqs doctor, bootstrap entrypoint. Это **не** MCP-сервер;
  он не регистрирует MCP tool'ов. Назначение — собрать платформу
  в продуктовую поверхность поверх трёх MCP-серверов выше.
