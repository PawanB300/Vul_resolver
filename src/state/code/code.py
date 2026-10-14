from typing import List, Literal, Optional

from pydantic import BaseModel

from state.graph_state import BaseGraphState


class RepositoryContext(BaseModel):

    file: str

    absolute_path: str

    start_line: int

    end_line: int

    function_name: Optional[str] = None

    class_name: Optional[str] = None

    imports: List[str] = []

    snippet: str


class CodePatch(BaseModel):

    file: str
    original_snippet: str
    fixed_snippet: str
    explanation: str


class CodeRemediationPlan(BaseModel):

    vulnerability_id: str
    target_file: str
    start_line: int
    end_line: int
    title: str
    reason: str
    remediation_strategy: Literal[
        "replace_function",
        "rewrite_block",
        "change_api",
        "sanitize_input",
        "remove_eval",
        "manual_review",
    ]


class CodeState(BaseGraphState):

    current_plan: CodeRemediationPlan
    repository_context: RepositoryContext
    generated_patch: CodePatch
