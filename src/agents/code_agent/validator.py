from state.graph_state import BaseGraphState
from tools.scan import run_snyk_code


def code_validator(state: BaseGraphState):

    report = run_snyk_code(state["repo_path"])

    vuln = state["current_vulnerability"]

    still_exists = False

    for run in report.get("runs", []):

        for result in run.get("results", []):

            if result["ruleId"] == vuln["rule_id"]:

                if result["locations"][0]["physicalLocation"]["artifactLocation"]["uri"] == vuln["file_path"]:
                    still_exists = True

    return {
        "validation_result": {
            "success": not still_exists,
            "scanner": "code",
        }
    }
