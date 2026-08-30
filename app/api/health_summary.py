from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.health_summary import HealthSummaryResponse
from app.services.health_summary_service import get_health_summary

router = APIRouter(
    prefix="/health-summary",
    tags=["Health Summary"],
)


@router.get(
    "/{user_id}",
    response_model=HealthSummaryResponse,
)
def health_summary(
    user_id: int,
    db: Session = Depends(get_db),
):
    summary = get_health_summary(db, user_id)

    if summary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return summary
