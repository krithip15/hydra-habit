from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.models.recommendation import Recommendation
from app.schemas.recommendation import RecommendationResponse

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get(
    "/{user_id}",
    response_model=list[RecommendationResponse],
)
def get_recommendations(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    recommendations = db.scalars(
        select(Recommendation)
        .where(Recommendation.user_id == user_id)
        .order_by(Recommendation.created_at.desc())
    ).all()

    return recommendations
