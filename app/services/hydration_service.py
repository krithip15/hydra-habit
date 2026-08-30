from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.hydration_record import HydrationRecord
from app.models.user import User
from app.schemas.hydration import HydrationRecordCreate


def create_hydration_record(
    db: Session,
    record_data: HydrationRecordCreate,
) -> HydrationRecord:

    user = db.get(User, record_data.user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    existing_record = db.scalar(
        select(HydrationRecord).where(
            HydrationRecord.user_id == record_data.user_id,
            HydrationRecord.date == record_data.date,
        )
    )

    if existing_record is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Hydration record already exists for this user and date",
        )

    record = HydrationRecord(
        user_id=record_data.user_id,
        date=record_data.date,
        water_intake_ml=record_data.water_intake_ml,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record