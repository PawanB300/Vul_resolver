# agents/code/context_builder.py

from pathlib import Path

from state.graph_state import BaseGraphState

CONTEXT_LINES = 30


def _read_context(path: Path, start_line: int, end_line: int):

    lines = path.read_text(encoding="utf-8").splitlines()

    start = max(0, start_line - CONTEXT_LINES - 1)
    end = min(len(lines), end_line + CONTEXT_LINES)

    snippet = "\n".join(lines[start:end])

    return {
        "snippet": snippet,
        "snippet_start": start + 1,
        "snippet_end": end,
    }


def context_builder(state: BaseGraphState):

    repo = Path(state["repo_path"])
    vuln = state["current_vulnerability"]

    file_path = repo / vuln["file_path"]

    context = _read_context(
        file_path,
        vuln["start_line"],
        vuln["end_line"],
    )

    return {
        "code_context": {
            "file": str(file_path),
            "rule": vuln["rule_id"],
            "title": vuln["title"],
            "severity": vuln["severity"],
            "message": vuln["message"],
            "description": vuln["description"],
            **context,
        }
    }
