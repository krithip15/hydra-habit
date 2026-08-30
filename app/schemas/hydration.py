from datetime import date

from pydantic import BaseModel, Field


class HydrationRecordCreate(BaseModel):
    user_id: int = Field(gt=0)
    date: date
    water_intake_ml: int = Field(ge=0)


class HydrationRecordResponse(BaseModel):
    id: int
    user_id: int
    date: date
    water_intake_ml: int

    model_config = {"from_attributes": True}
