from pydantic import BaseModel


class HealthSummaryResponse(BaseModel):
    user_id: int
    target_ml: int

    average_intake_ml: float | None
    target_achievement_percent: float | None
    gap_ml: float | None

    target_status: str

    valid_days: int
    missing_days: int
    suspicious_days: int

    trend: str
    data_quality: str
