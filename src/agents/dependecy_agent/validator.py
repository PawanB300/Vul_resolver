from state.graph_state import BaseGraphState
from state.validator import ValidationResult
from tools.scan import run_snyk_test


def dependency_validator(state: BaseGraphState):

    report = run_snyk_test(state["repo_path"])

    vuln_id = state["current_vulnerability"]["id"]

    remaining = [v for v in report.get("vulnerabilities", []) if v.get("id") == vuln_id]

    return {
        "validation_result": ValidationResult(
            success=len(remaining) == 0,
            vulnerability_id=vuln_id,
            remaining_findings=len(remaining),
            message=("Resolved" if len(remaining) == 0 else "Still present"),
        )
    }
