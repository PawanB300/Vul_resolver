from typing import Dict

from state.graph_state import BaseGraphState
from tools.dependency_tools.file import UpdateFile


def dependency_agent(state: BaseGraphState) -> Dict:

    plan = state["current_plan"]
    vuln = state["current_vulnerability"]

    updater = UpdateFile()

    # Later this can come from the planner itself
    path = f"{state['repo_path']}/{plan.target_files[0]}"

    if not updater.file_exists(path):
        raise FileNotFoundError(path)

    updater.backup(path)

    content = updater.read_file(path)

    updated = updater.update_requirement(
        content=content,
        package=vuln["package"],
        target_version=vuln["target_version"],
    )

    updater.write_file(path, updated)

    result = {
        "status": "success",
        "scanner": "dependency",
        "package": vuln["package"],
        "old_version": vuln["current_version"],
        "new_version": vuln["target_version"],
        "file": path,
        "actions": plan.actions,
    }

    return {
        "current_result": result,
        "remediation_results": state.get("remediation_results", []) + [result],
    }
