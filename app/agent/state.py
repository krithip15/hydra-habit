from typing import TypedDict


class AgentState(TypedDict, total=False):
    user_id: int

    user_profile: dict
    health_summary: dict

    insight: str
    action: str
    recommendation: str
    confidence: str

    recommendation_id: int

    error: str
