from state.graph_state import BaseGraphState
from tools.parser import normalize_dependency_vulnerability, parse_code_report


def analysis_agent(state: BaseGraphState):

    normalized = []

    # Dependency findings
    for vuln in state["dependency_report"].get("vulnerabilities", []):
        normalized.append(normalize_dependency_vulnerability(vuln))

    # Code findings
    normalized.extend(parse_code_report(state["code_report"]))

    return {"normalized_vulnerabilities": normalized}


def initialize_queue(state: BaseGraphState):

    return {
        "vulnerability_queue": state["normalized_vulnerabilities"].copy(),
        "remediation_plans": [],
    }


def load_next_vulnerability(state: BaseGraphState):

    queue = state["vulnerability_queue"]

    if not queue:
        return {"current_vulnerability": None}

    current = queue.pop(0)

    return {
        "current_vulnerability": current,
        "vulnerability_queue": queue,
    }
