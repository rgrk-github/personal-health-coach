import httpx
import os
from dotenv import load_dotenv

load_dotenv()

NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_APP_KEY = os.getenv("NUTRITIONIX_APP_KEY")
NUTRITIONIX_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"

headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_APP_KEY,
    "Content-Type": "application/json"
}

async def get_nutrition_summary(query: str) -> dict:
    print(f"🔍 API Request - Query: '{query}'")
    print(f"🔍 API Request - App ID: {NUTRITIONIX_APP_ID}")
    print(f"🔍 API Request - App Key: {'*' * len(NUTRITIONIX_APP_KEY) if NUTRITIONIX_APP_KEY else 'None'}")
    
    if not NUTRITIONIX_APP_ID or not NUTRITIONIX_APP_KEY:
        raise ValueError("Nutritionix API credentials not found in environment variables")
    
    if not query or query.strip() == "":
        raise ValueError("Query cannot be empty")
    
    payload = {"query": query}
    print(f"🔍 API Request - Payload: {payload}")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            NUTRITIONIX_URL,
            headers=headers,
            json=payload
        )
        
        print(f"🔍 API Response - Status: {response.status_code}")
        print(f"🔍 API Response - Headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"❌ API Response - Error Body: {response.text}")
        
        response.raise_for_status()
        return response.json()
