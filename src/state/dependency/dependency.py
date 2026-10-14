from typing import List, Literal

from pydantic import BaseModel, Field

from state.graph_state import BaseGraphState


class DependencyRemediationPlan(BaseModel):
    scanner: Literal["dependency"]

    vulnerability_id: str
    title: str
    severity: str

    package_name: str
    package_manager: str

    current_version: str
    target_version: str

    is_upgradable: bool
    is_patchable: bool

    fix_strategy: Literal[
        "upgrade_dependency",
        "apply_patch",
        "manual_review",
    ]

    requires_code_changes: bool

    target_files: List[str] = Field(default_factory=list)

    actions: List[str] = Field(default_factory=list)

    reason: str


class DependencyState(BaseGraphState):

    current_plan: DependencyRemediationPlan

    dependency_file: str

    dependency_changes: list

    update_result: dict


class DependencyUpdateResult(BaseModel):

    success: bool

    package_name: str

    old_version: str | None

    new_version: str | None

    manifest_file: str

    message: str
