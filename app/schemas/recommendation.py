from datetime import date, datetime

from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    id: int
    user_id: int
    date: date
    insight: str
    recommendation_text: str
    action_type: str
    confidence: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }