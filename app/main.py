from fastapi import FastAPI

from app.api.users import router as users_router

app = FastAPI(title="HydraHabit API")

app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "HydraHabit API is running"}