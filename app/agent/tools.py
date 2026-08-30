import json
from datetime import date

from sqlalchemy.orm import Session

from app.models.agent_execution_log import AgentExecutionLog
from app.models.recommendation import Recommendation
from app.models.user import User
from app.services.health_summary_service import get_health_summary

def get_user_profile(
    db: Session,
    user_id: int,
):
    user = db.get(User, user_id)

    if user is None:
        return None

    return {
        "user_id": user.id,
        "name": user.name,
        "age": user.age,
        "gender": user.gender,
        "health_goal": user.health_goal,
        "daily_water_target_ml": user.daily_water_target_ml,
        "preferred_reminder_time": user.preferred_reminder_time,
        "health_limitation": user.health_limitation,
    }


def get_hydration_summary(
    db: Session,
    user_id: int,
):
    summary = get_health_summary(db, user_id)

    if summary is None:
        return None

    return summary.model_dump()


def save_recommendation(
    db: Session,
    user_id: int,
    insight: str,
    recommendation: str,
    action: str,
    confidence: str,
):
    recommendation_record = Recommendation(
        user_id=user_id,
        date=date.today(),
        insight=insight,
        recommendation_text=recommendation,
        action_type=action,
        confidence=confidence,
    )

    db.add(recommendation_record)
    db.commit()
    db.refresh(recommendation_record)

    return {
        "recommendation_id": recommendation_record.id,
        "status": "saved",
    }

def log_agent_execution(
    db: Session,
    user_id: int,
    tool_name: str,
    tool_input: dict,
    tool_output: dict,
    decision_summary: str | None = None,
    final_action: str | None = None,
):
    log = AgentExecutionLog(
        user_id=user_id,
        tool_name=tool_name,
        tool_input=json.dumps(tool_input),
        tool_output=json.dumps(tool_output),
        decision_summary=decision_summary,
        final_action=final_action,
    )

    db.add(log)
    db.commit()
