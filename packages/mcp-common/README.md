# mcp-common

Общая библиотека для MCP-серверов платформы 1C Agent Platform.

Здесь живёт то, что не должно дублироваться между read / write / intelligence
серверами: базовая обвязка MCP, общие типы, утилиты, общая иерархия исключений
и общий контракт ответа инструментов.

## Что сейчас внутри

- **shared exception hierarchy** — `PlatformError`, `PolicyDeniedError`,
  `ProcessExecutionError`, `HealthCheckError`;
- **`OperationContext`** — описание контекста одного вызова MCP-инструмента
  (`operation_id`, `environment`, `base_id`, `tool_name`, `allow_write`);
- **shared `ToolResult`** — единый response envelope для всех трёх серверов
  (`ok`, `tool_name`, `message`, `payload`);
- **shared registry helpers** — `ToolCallable`, `build_tool_registry`,
  `list_registered_tools`, `get_registered_tool`: единый формат регистрации
  инструментов и их поиска по имени.

Это skeleton-уровень: контракты зафиксированы, но никакой реальной логики
MCP-обвязки тут ещё нет.
