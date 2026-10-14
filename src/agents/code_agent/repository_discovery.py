from pathlib import Path

from state.code.code import RepositoryContext
from state.graph_state import BaseGraphState

WINDOW = 30


def repository_discovery(state: BaseGraphState):

    plan = state["current_plan"]

    absolute_path = f"{state['repo_path']}/{plan.target_file}"

    lines = Path(absolute_path).read_text().splitlines()

    start = max(0, plan.start_line - WINDOW)
    end = min(len(lines), plan.end_line + WINDOW)

    snippet = "\n".join(lines[start:end])

    imports = [line for line in lines if line.startswith("import ") or line.startswith("from ")]

    return {
        "repository_context": RepositoryContext(
            file=plan.target_file,
            absolute_path=absolute_path,
            start_line=start + 1,
            end_line=end,
            imports=imports,
            snippet=snippet,
        )
    }
