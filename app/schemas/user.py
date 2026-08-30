from pydantic import BaseModel, Field

from app.schemas.enums import HealthGoal


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(gt=0, le=120)
    gender: str = Field(min_length=1, max_length=50)

    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)

    health_goal: HealthGoal

    daily_water_target_ml: int = Field(gt=0)

    preferred_reminder_time: str | None = None

    health_limitation: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    health_goal: HealthGoal
    daily_water_target_ml: int
    preferred_reminder_time: str | None
    health_limitation: str | None

    model_config = {"from_attributes": True}
