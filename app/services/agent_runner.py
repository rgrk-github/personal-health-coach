from typing import Dict, List, TypedDict, Optional
from langgraph.graph import StateGraph
from app.services.nutrition_api import get_nutrition_summary
import asyncio

# Define our agent's state structure
class AgentState(TypedDict, total=False):
    meal_name: str
    foods: List[Dict]
    goal: str
    parsed_foods: List[Dict]
    nutrition_summary: Dict
    spike_risk: str
    goal_feedback: str

# Step 1: Parse the meal input (for now, use input directly)
def parse_meal_input(state: AgentState) -> AgentState:
    state["parsed_foods"] = state.get("foods", [])
    return state

# Step 2: Lookup dummy nutrition data
async def lookup_nutrition(state: AgentState) -> AgentState:
    parsed_foods = state.get("parsed_foods", [])
    # Fix: Use 'item' field instead of 'name' field based on schema
    query = ", ".join([item.get("item", "") for item in parsed_foods if item.get("item")])

    print("🔍 Query to Nutritionix:", repr(query))
    print("🔍 Parsed foods:", parsed_foods)

    # Check if we have a valid query
    if not query or query.strip() == "":
        print("❌ Empty query - no food items found")
        print("🔍 Raw foods data:", state.get("foods", []))
        raise ValueError("No valid food items found in the request")

    response = await get_nutrition_summary(query)
    foods = response.get("foods", [])

    total = {
        "calories": sum(f.get("nf_calories", 0) for f in foods),
        "protein": sum(f.get("nf_protein", 0) for f in foods),
        "fat": sum(f.get("nf_total_fat", 0) for f in foods),
        "carbs": sum(f.get("nf_total_carbohydrate", 0) for f in foods),
        "fiber": sum(f.get("nf_dietary_fiber", 0) for f in foods),
    }
    total["net_carbs"] = total["carbs"] - total["fiber"]

    state["nutrition_summary"] = total
    print("✅ Real Nutrition Summary:", total)
    return state


# Step 3: Estimate spike risk
def estimate_spike_risk(state: AgentState) -> AgentState:
    print("🔍 Debug - State keys in estimate_spike_risk:", list(state.keys()))
    
    # Check if nutrition_summary exists
    if "nutrition_summary" not in state:
        print("❌ Error: nutrition_summary not found in state")
        raise KeyError("nutrition_summary not found in state. Available keys: " + str(list(state.keys())))
    
    carbs = state["nutrition_summary"]["carbs"]
    if carbs < 10:
        risk = "Low"
    elif carbs < 25:
        risk = "Medium"
    else:
        risk = "High"
    state["spike_risk"] = risk
    print("✅ Spike risk calculated:", risk)
    return state

# Step 4: Goal-based feedback (dummy logic)
def goal_based_summary(state: AgentState) -> AgentState:
    goal = state.get("goal", "").lower()
    carbs = state["nutrition_summary"]["net_carbs"]

    if goal == "keto" and carbs <= 20:
        feedback = "Meal fits your ketogenic goal well."
    elif goal == "glucose_control" and state["spike_risk"] == "Low":
        feedback = "Meal is good for glucose control."
    elif goal == "cholesterol":
        feedback = "Consider using more plant-based fats for cholesterol control."
    else:
        feedback = "Goal feedback not available."

    state["goal_feedback"] = feedback
    return state

# Build the LangGraph
def build_health_agent():
    builder = StateGraph(AgentState)

    builder.add_node("parse_meal_input", parse_meal_input)
    builder.add_node("lookup_nutrition", lookup_nutrition)
    builder.add_node("estimate_spike_risk", estimate_spike_risk)
    builder.add_node("goal_based_summary", goal_based_summary)

    builder.set_entry_point("parse_meal_input")
    builder.add_edge("parse_meal_input", "lookup_nutrition")
    builder.add_edge("lookup_nutrition", "estimate_spike_risk")
    builder.add_edge("estimate_spike_risk", "goal_based_summary")
    builder.set_finish_point("goal_based_summary")

    return builder.compile()
