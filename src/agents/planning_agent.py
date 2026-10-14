import json

from model.model import model
from prompts.planner import CODE_PLANNER_PROMPT, DEPENDENCY_PLANNER_PROMPT
from state.code.code import CodeRemediationPlan
from state.dependency.dependency import DependencyRemediationPlan
from state.graph_state import BaseGraphState

model_dependency_planner = model.with_structured_output(DependencyRemediationPlan)
mode_code_planner = model.with_structured_output(CodeRemediationPlan)


def retry_router(state: BaseGraphState):

    validation = state["validation_result"]

    if not validation["success"]:
        return "retry"

    if state["vulnerability_queue"]:
        return "next"

    return "finish"


def vulnerability_router(state: BaseGraphState):

    vuln = state["current_vulnerability"]

    if vuln is None:
        return "finish"

    if vuln["type"] == "dependency":
        return "dependency"

    return "code"


def dependency_planner(state: BaseGraphState):

    vuln = state["current_vulnerability"]

    prompt = DEPENDENCY_PLANNER_PROMPT.format(
        package=vuln["package"],
        current_version=vuln["current_version"],
        target_version=vuln["target_version"],
        severity=vuln["severity"],
        description=vuln["description"],
        is_upgradable=vuln["is_upgradable"],
        is_patchable=vuln["is_patchable"],
    )

    plan = model_dependency_planner.invoke(prompt)

    return {
        "current_plan": plan,
        "remediation_plans": state["remediation_plans"] + [plan],
    }


def code_planner(state: BaseGraphState):

    vuln = state["current_vulnerability"]

    prompt = CODE_PLANNER_PROMPT.format(
        rule_id=vuln["rule_id"],
        title=vuln["title"],
        severity=vuln["severity"],
        file_path=vuln["file_path"],
        start_line=vuln["start_line"],
        end_line=vuln["end_line"],
        description=vuln["description"],
        message=vuln["message"],
        cwe=vuln["cwe"],
    )

    plan = mode_code_planner.invoke(prompt)

    return {
        "current_plan": plan,
        "remediation_plans": state["remediation_plans"] + [plan],
    }
