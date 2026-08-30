from fastapi import FastAPI

from app.api.health_data import router as health_data_router
from app.api.health_summary import router as health_summary_router
from app.api.users import router as users_router
from app.api.agent import router as agent_router

app = FastAPI(title="HydraHabit API")


app.include_router(users_router)
app.include_router(health_data_router)
app.include_router(health_summary_router)
app.include_router(agent_router)


@app.get("/")
def root():
    return {"message": "HydraHabit API is running"}
