from langgraph.graph import END, START, StateGraph

from agents.analysis_agent import analysis_agent, initialize_queue, load_next_vulnerability
from agents.code_agent.context_builder import context_builder
from agents.code_agent.patch_apply import patch_apply
from agents.code_agent.patch_generator import patch_generator
from agents.code_agent.repository_discovery import repository_discovery
from agents.code_agent.validator import code_validator
from agents.dependecy_agent.dependency import dependency_agent
from agents.dependecy_agent.updater import dependency_updater
from agents.dependecy_agent.validator import dependency_validator
from agents.planning_agent import code_planner, dependency_planner, retry_router, vulnerability_router
from agents.scan_agent import scan_agent
from state.graph_state import BaseGraphState


def add_nodes(builder: StateGraph) -> StateGraph:

    builder.add_node("scan", scan_agent)
    builder.add_node("analysis", analysis_agent)

    builder.add_node("initialize_queue", initialize_queue)
    builder.add_node("load_next", load_next_vulnerability)

    builder.add_node("dependency_planner", dependency_planner)
    builder.add_node("code_planner", code_planner)

    builder.add_node("dependency_agent", dependency_agent)
    builder.add_node("dependency_updater", dependency_updater)
    builder.add_node("dependency_validator", dependency_validator)

    builder.add_node("patch_apply", patch_apply)
    builder.add_node("repository_context", repository_discovery)
    builder.add_node("patch_generator", patch_generator)
    builder.add_node("code_validator", code_validator)
    builder.add_node("context_builder", context_builder)

    return builder


def add_edges(builder: StateGraph) -> StateGraph:

    builder.add_edge(START, "scan")
    builder.add_edge("scan", "analysis")
    builder.add_edge("analysis", "initialize_queue")
    builder.add_edge("initialize_queue", "load_next")

    builder.add_conditional_edges(
        "load_next",
        vulnerability_router,
        {
            "dependency": "dependency_planner",
            "code": "code_planner",
            "finish": END,
        },
    )

    builder.add_edge("dependency_planner", "dependency_agent")
    builder.add_edge("dependency_agent", "dependency_updater")
    builder.add_edge("dependency_updater", "dependency_validator")
    builder.add_edge(
        "code_planner",
        "repository_context",
    )

    builder.add_edge(
        "repository_context",
        "context_builder",
    )

    builder.add_edge(
        "context_builder",
        "patch_generator",
    )

    builder.add_edge(
        "patch_generator",
        "patch_apply",
    )

    builder.add_edge(
        "patch_apply",
        "code_validator",
    )

    builder.add_conditional_edges(
        "dependency_validator",
        retry_router,
        {
            "retry": "dependency_planner",
            "next": "load_next",
            "finish": END,
        },
    )

    builder.add_conditional_edges(
        "code_validator",
        retry_router,
        {
            "retry": "code_planner",
            "next": "load_next",
            "finish": END,
        },
    )

    builder.add_edge("analysis", END)
    return builder


def save_graph(graph, output_path="graph.png"):
    png_bytes = graph.get_graph().draw_mermaid_png()

    with open(output_path, "wb") as f:
        f.write(png_bytes)

    print(f"Graph saved to {output_path}")
    return output_path


builder = StateGraph(BaseGraphState)
builder = add_nodes(builder)
builder = add_edges(builder)
graph = builder.compile()

if __name__ == "__main__":

    save_graph(graph=graph, output_path="image/workflow.png")
