from state.graph_state import BaseGraphState
from tools.scan import run_snyk_code, run_snyk_test


def scan_agent(state: BaseGraphState):

    repo = state["repo_path"]
    dependency_report = run_snyk_test(repo)
    code_report = run_snyk_code(repo)

    return {"dependency_report": dependency_report, "code_report": code_report}
