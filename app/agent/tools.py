from sqlalchemy.orm import Session

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