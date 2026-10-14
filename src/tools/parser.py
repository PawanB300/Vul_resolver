from typing import Any, Dict


def normalize_dependency_vulnerability(vuln: Dict) -> Dict:
    return {
        "type": "dependency",
        # Identity
        "id": vuln.get("id"),
        "title": vuln.get("title"),
        # Package
        "package": vuln.get("packageName"),
        "package_manager": vuln.get("packageManager"),
        "language": vuln.get("language"),
        # Versions
        "current_version": vuln.get("version"),
        "target_version": (vuln.get("fixedIn")[0] if vuln.get("fixedIn") else None),
        # Severity
        "severity": vuln.get("severity"),
        # Description
        "description": vuln.get("description"),
        # Metadata
        "cve": vuln.get("identifiers", {}).get("CVE", []),
        "cwe": vuln.get("identifiers", {}).get("CWE", []),
        # Fixability
        "is_upgradable": vuln.get("isUpgradable", False),
        "is_patchable": vuln.get("isPatchable", False),
        # Dependency path
        "dependency_path": vuln.get("from", []),
    }


def parse_code_report(report: dict):

    normalized = []

    for run in report.get("runs", []):

        rules = {rule["id"]: rule for rule in run["tool"]["driver"].get("rules", [])}

        for result in run.get("results", []):

            normalized.append(
                normalize_code_vulnerability(
                    result,
                    rules,
                )
            )

    return normalized


def normalize_code_vulnerability(result: Dict, rules: dict) -> Dict:
    rule = rules.get(result["ruleId"], {})

    location = result.get("locations", [{}])[0].get("physicalLocation", {})

    artifact = location.get("artifactLocation", {})
    region = location.get("region", {})

    return {
        "type": "code",
        # Identity
        "rule_id": result.get("ruleId"),
        "title": rule.get("name"),
        # Severity
        "severity": rule.get("defaultConfiguration", {}).get("level"),
        # File information
        "file_path": artifact.get("uri"),
        "start_line": region.get("startLine"),
        "end_line": region.get("endLine"),
        # Scanner message
        "message": result.get("message", {}).get("text"),
        # Description
        "description": (rule.get("help", {}).get("markdown")),
        # CWE
        "cwe": (rule.get("properties", {}).get("cwe", [])),
        # Categories
        "tags": (rule.get("properties", {}).get("tags", [])),
        # Examples from Snyk
        "example_fixes": (rule.get("properties", {}).get("exampleCommitFixes", [])),
    }
