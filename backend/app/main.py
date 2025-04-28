
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
    marital_status: str = Field(..., description="Marital status (single/married)")
    dependents: int = Field(..., description="Number of dependents")
    occupation: str = Field(..., description="Occupation of the user")
    education: str = Field(..., description="Education level of the user")
    other_coverage: str = Field(..., description="Health coverage type (individual/family)")
    other_policy: str = Field(..., description="Other policy types (SBI Health, SBI Life, etc.)")
    smoking_status: str = Field(..., description="Smoking status (smoker/non-smoker)")
    drinking_status: str = Field(..., description="Drinking status (drinker/non-drinker)")
    family_size: int = Field(..., description="Number of family members")
    gender: str = Field(..., description="Male")
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
        print(recommendation)
        # Return the recommendation
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, 
                           detail=f"Error generating recommendation: {str(e)}")

# Form submission endpoint
@app.post("/recommend-form/")
async def recommend_policy_form(request: Request,
    age: int = Form(...),
    location: str = Form(...),
    income: float = Form(...),
    marital_status: str = Form(...),
    dependents: int = Form(...),
    occupation: str = Form(...),
    education: str = Form(...),
    other_coverage: str = Form(...),
    other_policy: str = Form(default="None"),
    smoking_status: str = Form(...),
    drinking_status: str = Form(...),  # Added this required field
    family_size: int = Form(...),
    gender: str = Form(...),
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
            "marital_status": marital_status,
            "dependents": dependents,
            "occupation": occupation,
            "education": education,
            "other_coverage": other_coverage,
            "other_policy": other_policy,
            "smoking_status": smoking_status,
            "family_size": family_size,
            "past_claims": past_claims,
            "drinking_status": drinking_status,
            "health_conditions": health_list,
            "gender": gender,
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
class ChatRequest(BaseModel):
    policy_name: str
    provider: str
    question: str

@app.post("/chat-about-policy")
async def chat_about_policy(request: ChatRequest):
    """Handle chatbot interactions for policy questions"""
    try:
        # Get the policy details and user question
        policy_name = request.policy_name
        provider = request.provider
        user_question = request.question
        
        # Create a prompt for the AI
        prompt = f"""
        I want you to act as an insurance policy advisor for the policy: {policy_name} from {provider}.
        
        Answer the following customer question about this policy:
        "{user_question}"
        
        Provide a helpful, accurate, and concise response. If you don't know specific details about
        this policy, provide general information about similar policies but make it clear that
        these are general guidelines.
        Don't add any related annotations like [][].
        If a user allready have a policy encurouge it to upgrade it. 
        Your response should be friendly, informative, and encourage further questions if needed.
        You response should be in normal text format, not in JSON or any other format.
        """
        
        # Use your existing OpenAI client
        from policy_recommendation_model import client
        
        # Call the AI model for a response
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful insurance advisor chatbot."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.8,
            model="sonar-pro"  # Use the same model as your recommendation engine
        )
        
        # Extract and return the response
        bot_response = response.choices[0].message.content
        
        return {"response": bot_response}
    
    except Exception as e:
        print(f"Error in chatbot: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


# Run the application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
