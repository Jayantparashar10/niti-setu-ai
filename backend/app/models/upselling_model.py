import os
from openai import AzureOpenAI
import json
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("OPENAI_ENDPOINT")
deployment = "gpt-4o-mini"  # or your specified deployment name
subscription_key = os.getenv("OPENAI_KEY")
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

def generate_upselling_recommendation(user_profile, current_policies, available_add_ons, context_data):
    """
    Generates an upselling or cross-selling recommendation based on user profile,
    current policies, available add-ons, and project context.

    Args:
        user_profile (dict): User's demographic data, policy history, etc.
        current_policies (list): List of the user's current insurance policies.
        available_add_ons (list): List of available add-ons or upgraded policies.
        context_data (str): Project context from the PPT.

    Returns:
        dict: A dictionary containing the upselling recommendation and explanation.
    """

    prompt = f"""
    You are an expert insurance advisor specializing in upselling and cross-selling.
    Based on the user profile, their current insurance policies, available add-ons or upgraded policies,
    and the provided project context, recommend an appropriate upselling or cross-selling opportunity
    that would benefit the user without being intrusive.

    Explain why you recommend this particular add-on or upgrade, emphasizing how it aligns with the
    user's needs, goals, and existing coverage. Suggest a realistic price increase if applicable.

    **IMPORTANT: You *MUST* respond with a valid JSON object.
    Do NOT include any introductory or conversational text. The JSON object
    *MUST* conform to the following schema:**

    ```
    {{
        "upsell_id": "Add-on or upgraded policy ID (e.g., roadside_assistance, premium_coverage).  If NO suitable upsell opportunity exists, upsell_id MUST be null",
        "explanation": "Detailed explanation of the recommendation, including benefits and price (if applicable).  This MUST be a complete and well-formed sentence"
    }}
    ```

    User Profile: {json.dumps(user_profile)}

    Current Policies: {json.dumps(current_policies)}

    Available Add-ons/Upgrades: {json.dumps(available_add_ons)}

    Project Context (from Leximinds-HACK-AI-THON-2024.pptx): {context_data}
    """

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a JSON-outputting expert in insurance upselling. You MUST ALWAYS respond with valid JSON.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=4096,
        temperature=0.0,  # Reduce randomness to ensure JSON output
        top_p=1.0,
        model=deployment
    )

    try:
        upsell_data = json.loads(response.choices[0].message.content)
        return upsell_data
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")  # Print the error for debugging
        print(f"Response content: {response.choices[0].message.content}")  # Print the problematic content
        return {"upsell_id": None, "explanation": "Could not generate a valid JSON upselling recommendation."}


if __name__ == '__main__':
    # Example Usage (replace with actual data)
    user_profile = {
        "age": 40,
        "location": "Mumbai",
        "family_size": 3,
        "income": 1200000,
        "risk_tolerance": "Medium"
    }

    current_policies = [
        {
            "policy_id": "health_1",
            "name": "Basic Health Plan",
            "coverage": "Basic health coverage",
            "price": 10000
        }
    ]

    available_add_ons = [
        {
            "upsell_id": "critical_illness",
            "name": "Critical Illness Rider",
            "description": "Provides coverage for critical illnesses",
            "price_increase": 5000
        },
        {
            "upsell_id": "room_upgrade",
            "name": "Room Upgrade",
            "description": "Allows for room upgrades in hospitals",
            "price_increase": 2000
        }
    ]

    context_data = """
    The proposed solution combines Personalized Policy Recommendation, Dynamic Pricing Engine, and Upselling Strategy into a unified AI-powered platform. The upselling strategy must be intelligent and align with customer goals without being intrusive. Suggestions for extending policy durations or upgrading coverage levels should be relevant.  Upselling must be in Indian Rupees (INR).
    """

    upselling_result = generate_upselling_recommendation(user_profile, current_policies, available_add_ons, context_data)
    print(upselling_result)
