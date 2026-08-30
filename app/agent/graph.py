from langgraph.graph import END, START, StateGraph

from app.agent.nodes import (
    analyze_node,
    check_data_quality_node,
    get_profile_node,
    get_summary_node,
    route_after_quality_check,
    save_recommendation_node,
)
from app.agent.state import AgentState


def build_graph(db):

    graph = StateGraph(AgentState)

    graph.add_node(
        "get_profile",
        lambda state: get_profile_node(state, db),
    )

    graph.add_node(
        "get_summary",
        lambda state: get_summary_node(state, db),
    )

    graph.add_node(
        "check_quality",
        lambda state: check_data_quality_node(state, db),
    )

    graph.add_node(
        "analyze",
        lambda state: analyze_node(state, db),
    )

    graph.add_node(
        "save",
        lambda state: save_recommendation_node(state, db),
    )

    graph.add_edge(
        START,
        "get_profile",
    )

    graph.add_edge(
        "get_profile",
        "get_summary",
    )

    graph.add_edge(
        "get_summary",
        "check_quality",
    )

    graph.add_conditional_edges(
        "check_quality",
        route_after_quality_check,
        {
            "analyze": "analyze",
            "save": "save",
            "end": END,
        },
    )

    graph.add_edge(
        "analyze",
        "save",
    )

    graph.add_edge(
        "save",
        END,
    )

    return graph.compile()