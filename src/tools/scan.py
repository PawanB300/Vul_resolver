import json
import subprocess


def _run_snyk_command(command, repo_path):
    result = subprocess.run(
        command,
        cwd=repo_path,
        capture_output=True,
        text=True,
    )

    if result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "error": "invalid_json",
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

    return {"error": "no_output", "stderr": result.stderr}


def run_snyk_test(repo_path):

    dependency_report = _run_snyk_command(["snyk", "test", "--json"], repo_path)

    return dependency_report


def run_snyk_code(repo_path):
    code_report = _run_snyk_command(["snyk", "code", "test", "--json"], repo_path)
    return code_report
