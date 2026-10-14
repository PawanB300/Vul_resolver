from state.dependency.dependency import DependencyUpdateResult
from state.graph_state import BaseGraphState
from tools.dependency_tools.file import UpdateFile


def dependency_updater(state: BaseGraphState):

    plan = state["current_plan"]

    updater = UpdateFile()

    path = f"{state['repo_path']}/{plan.manifest_file}"

    content = updater.read_file(path)

    updated = updater.update_requirement(
        content,
        plan.package_name,
        plan.target_version,
    )

    updater.write_file(path, updated)

    return {
        "current_result": DependencyUpdateResult(
            success=True,
            package_name=plan.package_name,
            old_version=plan.current_version,
            new_version=plan.target_version,
            manifest_file=plan.manifest_file,
            message="Dependency upgraded",
        )
    }
