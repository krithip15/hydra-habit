from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.hydration import (
    HydrationRecordCreate,
    HydrationRecordResponse,
)
from app.services.hydration_service import create_hydration_record

router = APIRouter(
    prefix="/health-data",
    tags=["Health Data"],
)


@router.post(
    "",
    response_model=HydrationRecordResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_hydration_record(
    record_data: HydrationRecordCreate,
    db: Session = Depends(get_db),
):
    return create_hydration_record(db, record_data)
