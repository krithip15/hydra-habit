from fastapi import FastAPI

app = FastAPI(title="HydraHabit API")


@app.get("/")
def root():
    return {"message": "HydraHabit API is running"}
