from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.hydration_record import HydrationRecord
from app.models.user import User
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
    return create_hydration_record(
        db,
        record_data,
    )


@router.get(
    "/{user_id}",
    response_model=list[HydrationRecordResponse],
)
def get_hydration_records(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    records = db.scalars(
        select(HydrationRecord)
        .where(HydrationRecord.user_id == user_id)
        .order_by(HydrationRecord.date.desc())
    ).all()

    return records