from fastapi import APIRouter
from app.models.schemas import MealLogRequest, MealLogResponse, NutritionSummary
from app.services.agent_runner import build_health_agent

router = APIRouter()

@router.post("/", response_model=MealLogResponse)
async def log_meal(meal: MealLogRequest):
    agent = build_health_agent()

    # Prepare the initial agent state
    state = {
        "meal_name": meal.meal_name,
        "foods": [item.dict() for item in meal.foods],
        "goal": meal.goal,
    }    # Invoke LangGraph agent asynchronously
    result = await agent.ainvoke(state)

    # Return response in expected schema format
    return {
        "nutrition_summary": result["nutrition_summary"],
        "spike_risk": result["spike_risk"],
        "goal_feedback": result["goal_feedback"]
    }
