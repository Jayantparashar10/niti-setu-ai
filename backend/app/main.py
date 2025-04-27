
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
import os
from policy_recommendation_model import generate_policy_recommendation

# Initialize FastAPI app
app = FastAPI(title="Policy Recommendation API", 
              description="API for generating personalized policy recommendations")

# Mount static files and templates for the web interface
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Define input model (Pydantic model for request validation)
class UserProfile(BaseModel):
    age: int = Field(..., description="User's age in years")
    location: str = Field(..., description="User's location in India")
    income: float = Field(..., description="Monthly income in INR")
    family_size: int = Field(..., description="Number of family members")
    past_claims: int = Field(..., description="Number of past insurance claims")
    health_conditions: List[str] = Field([], description="List of health conditions")
    preferences: List[str] = Field([], description="List of policy preferences")
    max_monthly_emi_budget: str = Field(..., description="Maximum monthly budget for insurance (e.g., 'INR 10000')")
    policy_type: str = Field(..., description="Type of policy (health, life, auto, etc.)")

# Define output models
class Policy(BaseModel):
    name: str
    provider: str
    monthly_emi: float
    description: str
    link: str

class PolicyRecommendation(BaseModel):
    policies: List[Policy]
    explanation: Optional[str] = None

# Home page endpoint - serves the HTML form
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Home page with a form to submit user profile data"""
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoint for JSON requests
@app.post("/recommend/", response_model=PolicyRecommendation)
async def recommend_policy(user_profile: UserProfile):
    """Generate personalized policy recommendations based on user profile"""
    try:
        # Convert Pydantic model to dictionary
        user_data = user_profile.dict()
        
        # Call the recommendation function
        recommendation = generate_policy_recommendation(user_data)
        
        # Return the recommendation
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, 
                           detail=f"Error generating recommendation: {str(e)}")

# Form submission endpoint
@app.post("/recommend-form/")
async def recommend_policy_form(
    request: Request,
    age: int = Form(...),
    location: str = Form(...),
    income: float = Form(...),
    family_size: int = Form(...),
    past_claims: int = Form(...),
    health_conditions: str = Form(""),
    preferences: str = Form(""),
    max_monthly_emi_budget: str = Form(...),
    policy_type: str = Form(...)
):
    """Handle form submission for policy recommendation"""
    try:
        # Parse health conditions and preferences as comma-separated lists
        health_list = [h.strip() for h in health_conditions.split(",") if h.strip()]
        preferences_list = [p.strip() for p in preferences.split(",") if p.strip()]
        
        # Create user profile dictionary
        user_data = {
            "age": age,
            "location": location,
            "income": income,
            "family_size": family_size,
            "past_claims": past_claims,
            "health_conditions": health_list,
            "preferences": preferences_list,
            "max_monthly_emi_budget": max_monthly_emi_budget,
            "policy_type": policy_type
        }
        
        # Get recommendations
        recommendation = generate_policy_recommendation(user_data)
        
        # Ensure we have the expected structure
        if "policies" not in recommendation:
            recommendation = {
                "policies": [],
                "explanation": recommendation.get("explanation", "Invalid response format")
            }
        
        # Return the results page
        return templates.TemplateResponse(
            "results.html", 
            {
                "request": request,
                "recommendation": recommendation,
                "user_data": user_data
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": str(e)
            }
        )

# Run the application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("main:app", host="0.0.1.1", port=5000, reload=True)
