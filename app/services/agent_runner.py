from typing import Dict, List, TypedDict, Optional
from langgraph.graph import StateGraph

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
def lookup_nutrition(state: AgentState) -> AgentState:
    print("🔍 Debug - State keys in lookup_nutrition:", list(state.keys()))
    print("🔍 Debug - Foods received:", state.get("parsed_foods", []))
    
    # Dummy values for now (will be replaced by Nutritionix API later)
    total_nutrition = {
        "calories": 250,
        "protein": 15,
        "fat": 20,
        "carbs": 5,
        "fiber": 2,
        "net_carbs": 3
    }

    # ✅ THIS LINE IS CRITICAL
    state["nutrition_summary"] = total_nutrition
    print("✅ Nutrition summary added to state:", total_nutrition)
    print("🔍 Debug - State keys after adding nutrition_summary:", list(state.keys()))
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
