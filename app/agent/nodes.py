import json

from langchain_ollama import ChatOllama
from sqlalchemy.orm import Session

from app.agent.prompts import ALLOWED_ACTIONS, SYSTEM_PROMPT
from app.agent.state import AgentState
from app.agent.tools import (
    get_hydration_summary,
    get_user_profile,
    log_agent_execution,
    save_recommendation,
)


llm = ChatOllama(
    model="qwen3:1.7b",
    temperature=0,
)


def get_profile_node(
    state: AgentState,
    db: Session,
) -> AgentState:

    profile = get_user_profile(
        db,
        state["user_id"],
    )

    if profile is None:
        return {
            **state,
            "error": "User not found",
        }

    log_agent_execution(
        db=db,
        user_id=state["user_id"],
        tool_name="get_user_profile",
        tool_input={
            "user_id": state["user_id"],
        },
        tool_output=profile,
    )

    return {
        **state,
        "user_profile": profile,
    }


def get_summary_node(
    state: AgentState,
    db: Session,
) -> AgentState:

    if state.get("error"):
        return state

    summary = get_hydration_summary(
        db,
        state["user_id"],
    )

    if summary is None:
        return {
            **state,
            "error": "Unable to generate health summary",
        }

    log_agent_execution(
        db=db,
        user_id=state["user_id"],
        tool_name="get_hydration_summary",
        tool_input={
            "user_id": state["user_id"],
        },
        tool_output=summary,
    )

    return {
        **state,
        "health_summary": summary,
    }


def check_data_quality_node(
    state: AgentState,
    db: Session,
) -> AgentState:

    if state.get("error"):
        return state

    summary = state["health_summary"]

    log_agent_execution(
        db=db,
        user_id=state["user_id"],
        tool_name="check_data_quality",
        tool_input={},
        tool_output={
            "data_quality": summary["data_quality"],
            "valid_days": summary["valid_days"],
            "missing_days": summary["missing_days"],
            "suspicious_days": summary["suspicious_days"],
        },
        decision_summary="Data quality evaluated",
    )

    if summary["data_quality"] == "INSUFFICIENT":
        return {
            **state,
            "action": "NO_ACTION",
            "insight": "There is not enough reliable hydration data.",
            "recommendation": (
                "Collect more hydration data before making "
                "a meaningful recommendation."
            ),
            "confidence": "HIGH",
        }

    return state


def route_after_quality_check(
    state: AgentState,
) -> str:

    if state.get("error"):
        return "end"

    if state.get("action") == "NO_ACTION":
        return "save"

    return "analyze"


def analyze_node(
    state: AgentState,
    db: Session,
) -> AgentState:

    if state.get("error"):
        return state

    user_profile = state["user_profile"]
    health_summary = state["health_summary"]

    prompt = f"""
User profile:
{json.dumps(user_profile, indent=2)}

Health summary:
{json.dumps(health_summary, indent=2)}

Analyze this information and choose the most appropriate action.
"""

    response = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("human", prompt),
        ]
    )

    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        return {
            **state,
            "error": "LLM returned invalid JSON",
        }

    action = result.get("action")

    if action not in ALLOWED_ACTIONS:
        return {
            **state,
            "error": f"Invalid agent action: {action}",
        }

    log_agent_execution(
        db=db,
        user_id=state["user_id"],
        tool_name="llm_analyze",
        tool_input={
            "user_profile": user_profile,
            "health_summary": health_summary,
        },
        tool_output=result,
        decision_summary=result.get("insight"),
        final_action=action,
    )

    return {
        **state,
        "insight": result.get("insight", ""),
        "action": action,
        "recommendation": result.get(
            "recommendation",
            "",
        ),
        "confidence": result.get(
            "confidence",
            "LOW",
        ),
    }


def save_recommendation_node(
    state: AgentState,
    db: Session,
) -> AgentState:

    if state.get("error"):
        return state

    result = save_recommendation(
        db=db,
        user_id=state["user_id"],
        insight=state.get("insight", ""),
        recommendation=state.get("recommendation", ""),
        action=state.get("action", "NO_ACTION"),
        confidence=state.get("confidence", "LOW"),
    )

    log_agent_execution(
        db=db,
        user_id=state["user_id"],
        tool_name="save_recommendation",
        tool_input={
            "user_id": state["user_id"],
            "action": state.get("action"),
        },
        tool_output=result,
        decision_summary=state.get("insight"),
        final_action=state.get("action"),
    )

    return {
        **state,
        "recommendation_id": result["recommendation_id"],
    }
