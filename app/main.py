from fastapi import FastAPI
from app.routes import meal

app = FastAPI(title="Personal Health Coach API")

app.include_router(meal.router, prefix="/log", tags=["Meal Logger"])
