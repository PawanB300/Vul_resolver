from graph.workflow import graph

initial_state = {"repo_path": "/home/pawanbisht/PepsiCo/LLM/Vulnerability_resolver"}

result = graph.invoke(initial_state)
print(type(result))
print(result.keys())
for i, vul in enumerate(result["normalized_vulnerabilities"]):
    print("#" * 100)
    print(i, " : ", vul)
