from pydantic import BaseModel
from typing import List

class FoodItem(BaseModel):
    item: str
    quantity: float
    unit: str

class MealLogRequest(BaseModel):
    meal_name: str
    foods: List[FoodItem]
    goal: str  # e.g., "keto", "glucose_control", "cholesterol"

class NutritionSummary(BaseModel):
    calories: float
    protein: float
    fat: float
    carbs: float
    fiber: float
    net_carbs: float

class MealLogResponse(BaseModel):
    nutrition_summary: NutritionSummary
    spike_risk: str
    goal_feedback: str
