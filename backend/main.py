# FastAPI backend for Ingredient Copilot

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Ingredient Copilot API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import ai_engine

class AnalysisRequest(BaseModel):
    ingredients_text: Optional[str] = None
    image_data: Optional[str] = None # Base64 encoded image
    product_name: Optional[str] = None

class AnalysisResponse(BaseModel):
    what_stands_out: str
    why_it_matters: str
    uncertainty: str
    recommendation: str
    inferred_intent: str

@app.get("/")
async def root():
    return {"message": "Ingredient Copilot API is running"}

@app.get("/sample-data")
async def get_sample_data():
    return [
        {
            "id": "1",
            "name": "Energy Drink",
            "ingredients": "Carbonated Water, High Fructose Corn Syrup, Citric Acid, Natural Flavors, Caffeine, Sodium Benzoate, Red 40"
        },
        {
            "id": "2",
            "name": "Organic Almond Milk",
            "ingredients": "Almond Base (Filtered Water, Almonds), Sea Salt, Locust Bean Gum, Sunflower Lecithin, Gellan Gum, Vitamin A Palmitate, Ergocalciferol (Vitamin D2)"
        },
        {
            "id": "3",
            "name": "Potato Chips",
            "ingredients": "Potatoes, Vegetable Oil (Sunflower, Corn, and/or Canola Oil), Salt"
        }
    ]

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_ingredients(request: AnalysisRequest):
    input_text = request.ingredients_text or request.product_name
    if not input_text:
        raise HTTPException(status_code=400, detail="No ingredients or product name provided")
    
    result = await ai_engine.analyze_ingredients_ai(input_text)
    return AnalysisResponse(**result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
