"""Minimal import/self-check for 1C Agent Platform skeleton modules.

Run this after loading PYTHONPATH via scripts/dev/bootstrap_paths.ps1.
No try/except: if anything is wired incorrectly, we want a loud, honest failure.
"""

from mcp_read_server import (
    health_summary,
    list_tools as read_list_tools,
    ping as read_ping,
)
from mcp_write_server import (
    list_tools as write_list_tools,
    ping as write_ping,
)
from mcp_intelligence_server import (
    list_tools as intelligence_list_tools,
    ping as intelligence_ping,
)
from onec_audit import AuditRecord, format_audit_record
from onec_config import load_project_config
from onec_health import (
    check_dump_path_exists,
    check_http_gateway_available,
    check_search_index_available,
    summarize_health,
)
from onec_policy_engine import check_write_allowed
from onec_troubleshooting import diagnose_from_health


def main() -> None:
    read_ping()
    write_ping()
    intelligence_ping()

    read_tools = read_list_tools()
    write_tools = write_list_tools()
    intelligence_tools = intelligence_list_tools()

    prod_decision = check_write_allowed("production", True)
    local_decision = check_write_allowed("local-dev", False)

    dump_result = check_dump_path_exists("Z:\\nonexistent-dump-path")
    gateway_result = check_http_gateway_available(False)
    index_result = check_search_index_available(True)
    summarize_health([dump_result, gateway_result, index_result])

    health_summary_result = health_summary(
        dump_path="Z:\\nonexistent-dump-path",
        gateway_available=False,
        search_index_available=True,
    )
    if health_summary_result.ok:
        health_summary_ok = "true"
        health_summary_problem = "none"
    else:
        health_summary_ok = "false"
        troubleshooting = health_summary_result.payload.get("troubleshooting")
        if troubleshooting:
            health_summary_problem = troubleshooting["problem_code"]
        else:
            health_summary_problem = "none"

    report = diagnose_from_health(["gateway_down"])

    project_config = load_project_config(
        {
            "environments": {
                "local-dev": {
                    "name": "Local Dev",
                    "base_id": "local-dev",
                    "base_path": "C:\\tmp\\infobase",
                    "publication_name": "local-dev",
                    "http_base_url": "http://localhost:8080/local-dev",
                    "dump_path": "C:\\tmp\\dump\\local-dev",
                    "timeout_seconds": 30,
                    "allow_write": False,
                }
            }
        }
    )

    format_audit_record(
        AuditRecord(
            operation_id="op-001",
            tool_name="ping",
            environment="local-dev",
            base_id="local-dev",
            status="ok",
            message="selfcheck",
        )
    )

    print("imports_ok = true")
    print(f"read_server_tools = {read_tools}")
    print(f"write_server_tools = {write_tools}")
    print(f"intelligence_server_tools = {intelligence_tools}")
    print(f"production_write_allowed = {str(prod_decision.allowed).lower()}")
    print(f"local_dev_write_allowed = {str(local_decision.allowed).lower()}")
    print(f"diagnosis_example = {report.problem_code}")
    print(f"config_envs = {sorted(project_config.environments)}")
    print(f"health_summary_ok = {health_summary_ok}")
    print(f"health_summary_problem = {health_summary_problem}")
    print("selfcheck_status = ok")


if __name__ == "__main__":
    main()
