from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Optional, Literal
from pydantic import BaseModel
import httpx
import os
from datetime import datetime
import uuid
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()
TYPEFORM_API_KEY = os.getenv("TYPEFORM_API_KEY")
TYPEFORM_FORM_ID = os.getenv("TYPEFORM_FORM_ID")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_current_user(authorization: str = Header(None)):
    """Validate JWT and return user data"""
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization token")
    
    try:
        token = authorization.split(" ")[1]
        response = await supabase.auth.get_user(token)
        user = response.user
        return {"id": user.id, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

async def fetch_form_fields() -> Dict[str, str]:
    """Fetch Typeform fields and return id->question mapping"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.typeform.com/forms/{TYPEFORM_FORM_ID}",
            headers={"Authorization": f"Bearer {TYPEFORM_API_KEY}"}
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error fetching form fields")
            
        form = response.json()
        return {
            field["id"]: field["title"] 
            for field in form["fields"]
        }

async def fetch_latest_response(user_email: str) -> dict:
    """Fetch latest Typeform response for user"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://api.typeform.com/forms/{TYPEFORM_FORM_ID}/responses",
                params={
                    "query": user_email,
                    "sort": "-submitted_at",
                    "page_size": 1
                },
                headers={
                    "Authorization": f"Bearer {TYPEFORM_API_KEY}",
                    "Accept": "application/json"
                }
            )
            
            # Print debug information
            print(f"Typeform API Response Status: {response.status_code}")
            print(f"Response Body: {response.text}")
            
            if response.status_code == 404:
                raise HTTPException(
                    status_code=404, 
                    detail="Form not found. Please check TYPEFORM_FORM_ID."
                )
                
            if response.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail=f"Typeform API error: {response.text}"
                )
                
            data = response.json()
            
            if not data.get("items"):
                raise HTTPException(
                    status_code=404,
                    detail=f"No form submission found for email: {user_email}"
                )
                
            return data["items"][0]
            
        except httpx.RequestError as e:
            print(f"Request Error: {str(e)}")
            raise HTTPException(
                status_code=502,
                detail=f"Error connecting to Typeform: {str(e)}"
            )


def build_qa_dict(submission: dict, field_map: Dict[str, str]) -> Dict[str, str]:
    """Convert Typeform submission into Q&A dictionary"""
    qa_dict = {}
    for answer in submission.get("answers", []):
        question = field_map.get(answer["field"]["id"])
        if question:
            qa_dict[question] = answer.get("text", answer.get("choice", {}).get("label", ""))
    return qa_dict


@app.post("/api/agents/{feature}")
async def run_agent(
    feature: Literal["recommendation", "pricing", "upsell"],
    user = Depends(get_current_user)
) -> Dict:
    """Run AI agent for specific feature"""
    try:
        # Fetch form data
        field_map = await fetch_form_fields()
        submission = await fetch_latest_response(user["email"])
        user_profile = build_qa_dict(submission, field_map)
        
        # Run appropriate agent (using existing client in agent files)
        if feature == "recommendation":
            from models.policy_recommendation_model import generate_policy_recommendation
            result = await generate_policy_recommendation(user_profile)
        elif feature == "pricing":
            from models.pricing_model import generate_dynamic_price
            result = await generate_dynamic_price(user_profile)
        else:  # upsell
            from models.upselling_model import generate_upselling_recommendation
            result = await generate_upselling_recommendation(user_profile)
            
        # Store in Supabase
        await supabase.table("agent_results").insert({
            "id": str(uuid.uuid4()),
            "user_id": user["id"],
            "feature": feature,
            "profile": user_profile,
            "result": result,
            "created_at": datetime.utcnow().isoformat()
        })
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))