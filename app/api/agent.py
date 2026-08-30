from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.graph import build_graph
from app.database.database import get_db
from app.models.agent_execution_log import AgentExecutionLog

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


@router.get("/logs/{user_id}")
def get_agent_logs(
    user_id: int,
    db: Session = Depends(get_db),
):
    logs = db.scalars(
        select(AgentExecutionLog)
        .where(AgentExecutionLog.user_id == user_id)
        .order_by(AgentExecutionLog.created_at.desc())
    ).all()

    return [
        {
            "id": log.id,
            "tool_name": log.tool_name,
            "tool_input": log.tool_input,
            "tool_output": log.tool_output,
            "decision_summary": log.decision_summary,
            "final_action": log.final_action,
            "created_at": log.created_at,
        }
        for log in logs
    ]
