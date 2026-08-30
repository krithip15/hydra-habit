from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.agent import router as agent_router
from app.api.health_data import router as health_data_router
from app.api.health_summary import router as health_summary_router
from app.api.recommendations import router as recommendations_router
from app.api.users import router as users_router

app = FastAPI(title="HydraHabit API")


app.include_router(users_router)
app.include_router(health_data_router)
app.include_router(health_summary_router)
app.include_router(agent_router)
app.include_router(recommendations_router)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/style.css", include_in_schema=False)
def serve_css():
    return FileResponse(
        FRONTEND_DIR / "style.css",
        media_type="text/css",
    )


@app.get("/app.js", include_in_schema=False)
def serve_javascript():
    return FileResponse(
        FRONTEND_DIR / "app.js",
        media_type="application/javascript",
    )
