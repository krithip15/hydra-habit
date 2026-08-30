from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.agent.graph import build_graph
from app.database.database import get_db

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post("/analyze/{user_id}")
def analyze_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    graph = build_graph(db)

    result = graph.invoke(
        {
            "user_id": user_id,
        }
    )

    if result.get("error"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"],
        )

    return {
        "user_id": user_id,
        "insight": result.get("insight"),
        "action": result.get("action"),
        "recommendation": result.get("recommendation"),
        "confidence": result.get("confidence"),
        "recommendation_id": result.get("recommendation_id"),
    }
