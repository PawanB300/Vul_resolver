from model.model import model
from prompts.code import PATCH_PROMPT
from state.code.code import CodePatch
from state.graph_state import BaseGraphState

patch_model = model.with_structured_output(CodePatch)


def patch_generator(state: BaseGraphState):

    prompt = PATCH_PROMPT.format(
        vuln=state["current_vulnerability"],
        plan=state["current_plan"],
        snippet=state["repository_context"].get("snippet", []),
    )

    patch = patch_model.invoke(prompt)

    return {"generated_patch": patch}
