"""Skeleton server bootstrap for mcp-write-server.

Holds only a tool registry and lookup helpers. Real MCP transport,
policy enforcement, backup/dump/apply/verify flows will be added later.
"""

from mcp_common import (
    ToolCallable,
    build_tool_registry,
    get_registered_tool,
    list_registered_tools,
)

from .tools import (
    add_catalog_attribute,
    add_document_attribute,
    add_form_attribute,
    add_form_element,
    append_module_method,
    apply_config_from_files,
    check_write_preconditions,
    create_backup_snapshot,
    create_catalog,
    create_common_module,
    create_dump_snapshot,
    create_managed_form,
    describe_last_write_operation,
    diff_dump_fragment,
    ping,
    prepare_rollback_hint,
    replace_module_method_body,
    restore_dump_file_from_snapshot,
    update_database_configuration,
    update_module_code,
    verify_attribute_exists,
    verify_metadata_change,
    verify_module_contains,
    verify_object_exists,
    write_audit_record,
)

REGISTERED_TOOLS: dict[str, ToolCallable] = build_tool_registry(
    {
        "ping": ping,
        "check_write_preconditions": check_write_preconditions,
        "create_backup_snapshot": create_backup_snapshot,
        "create_dump_snapshot": create_dump_snapshot,
        "apply_config_from_files": apply_config_from_files,
        "update_module_code": update_module_code,
        "create_common_module": create_common_module,
        "verify_module_contains": verify_module_contains,
        "verify_object_exists": verify_object_exists,
        "verify_metadata_change": verify_metadata_change,
        "update_database_configuration": update_database_configuration,
        "add_catalog_attribute": add_catalog_attribute,
        "write_audit_record": write_audit_record,
        "describe_last_write_operation": describe_last_write_operation,
        "prepare_rollback_hint": prepare_rollback_hint,
        "create_catalog": create_catalog,
        "add_document_attribute": add_document_attribute,
        "verify_attribute_exists": verify_attribute_exists,
        "diff_dump_fragment": diff_dump_fragment,
        "create_managed_form": create_managed_form,
        "add_form_element": add_form_element,
        "append_module_method": append_module_method,
        "replace_module_method_body": replace_module_method_body,
        "restore_dump_file_from_snapshot": restore_dump_file_from_snapshot,
        "add_form_attribute": add_form_attribute,
    }
)


def list_tools() -> list[str]:
    """Return names of registered tools, sorted alphabetically."""
    return list_registered_tools(REGISTERED_TOOLS)


def get_tool(name: str) -> ToolCallable | None:
    """Return the registered tool callable by name, or ``None``."""
    return get_registered_tool(REGISTERED_TOOLS, name)
