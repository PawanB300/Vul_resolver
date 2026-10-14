from src.agents.scan import run_snyk

target_folder = r"/home/pawanbisht/PepsiCo/LLM/Vulnerability_resolver"

results = run_snyk(target_folder)


def extract_findings(results):
    findings = []

    for issue in results.get("runs", [])[0].get("results", []):
        findings.append(
            {
                "rule_id": issue.get("ruleId"),
                "message": issue.get("message", {}).get("text"),
                "locations": issue.get("locations", []),
            }
        )

    return findings


# result = extract_findings(results)

# if not result:
#     print("No findings returned from run_snyk() or scan produced no results.")
# else:
#     for idx, finding in enumerate(result, start=1):
#         print(f"Finding #{idx}")
#         for k, v in finding.items():
#             print(f"  {k}: {v}")
#         print()

print(results)
