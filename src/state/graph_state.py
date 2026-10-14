from typing import Any, Dict, List, Optional, TypedDict


class BaseGraphState(TypedDict):

    repo_path: str
    dependency_report: Dict[str, Any]
    code_report: Dict[str, Any]

    dependency_findings: List[Dict[str, Any]]
    code_findings: List[Dict[str, Any]]

    normalized_vulnerabilities: List[Dict[str, Any]]

    vulnerability_queue: List[Dict]
    current_vulnerability: Optional[Dict]
    current_plan: Dict[str, Any]
    current_result: dict

    remediation_results: List[Dict[str, Any]]

    validation_result: Dict[str, Any]
