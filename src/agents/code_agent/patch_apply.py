from agents.code_agent.patch import PatchTool
from state.graph_state import BaseGraphState

tool = PatchTool()


def patch_apply(state: BaseGraphState):

    patch = state["generated_patch"]

    repo = state["repository_context"]

    tool.apply_patch(
        repo.absolute_path,
        patch.original_snippet,
        patch.fixed_snippet,
    )

    return {
        "current_result": {
            "file": repo.file,
            "status": "patched",
        }
    }
