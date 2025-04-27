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

def generate_dynamic_price(user_profile, policy_features, market_trends, context_data):
    """
    Generates a dynamic price for an insurance policy based on user profile,
    policy features, market trends, and project context. Price is in INR.

    Args:
        user_profile (dict): User's demographic data, risk profile, etc.
        policy_features (dict): Features of the insurance policy (coverage, limits, etc.).
        market_trends (dict): Current market conditions affecting pricing.
        context_data (str): Project context extracted from the PPT.

    Returns:
        dict: A dictionary containing the dynamic price in INR and explanation.
    """

    prompt = f"""
    You are an expert actuary and pricing specialist. Based on the user profile,
    insurance policy features, current market trends, and the provided project
    context, calculate a *dynamic and optimized* price in **Indian Rupees (INR)** for the insurance policy.

    Explain the factors that influenced the price, including adjustments based on
    user risk, policy features, and market conditions. The price must be a realistic figure in INR.

    **IMPORTANT: You *MUST* respond with a valid JSON object.
    Do NOT include any introductory or conversational text. The JSON object
    *MUST* conform to the following schema:**

    ```
    {{
        "price_inr": "Price in INR (e.g., 45075.50). MUST be a valid number",
        "explanation": "Detailed explanation of the pricing calculation and factors considered.  This MUST be a complete and well-formed sentence"
    }}
    ```

    User Profile: {json.dumps(user_profile)}

    Policy Features: {json.dumps(policy_features)}

    Market Trends: {json.dumps(market_trends)}

    Project Context (from Leximinds-HACK-AI-THON-2024.pptx): {context_data}

    """

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a JSON-outputting expert actuary specializing in dynamic insurance pricing in INR.  You MUST ALWAYS respond with valid JSON.",
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
        pricing_data = json.loads(response.choices[0].message.content)
        return pricing_data
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")  # Print the error for debugging
        print(f"Response content: {response.choices[0].message.content}")  # Print the problematic content
        return {"price_inr": None, "explanation": "Could not generate a valid JSON price in INR."}


if __name__ == '__main__':
    # Example Usage (replace with actual data)
    user_profile = {
        "age": 30,
        "location": "Delhi",  # Changed location
        "driving_experience": 5,
        "vehicle_type": "Sedan",
        "past_accidents": 0
    }

    policy_features = {
        "coverage_level": "Comprehensive",
        "deductible": 5000,  # Changed deductible to INR equivalent
        "liability_limit": 1000000  # Changed liability limit to INR equivalent
    }

    market_trends = {
        "inflation_rate": 0.06,  # Changed inflation rate
        "competition_index": 0.8,
        "claim_frequency": 0.07
    }

    context_data = """
    The proposed solution uses a Dynamic Pricing Engine that tailors policy pricing based on individual customer profiles,
    market trends, and policy features to enhance customer experience and satisfaction. The USP of the solution includes:
    Real-time AI-powered recommendations and dynamic pricing, explainable AI models that build customer trust. Pricing must always be in Indian Rupees (INR).
    """

    pricing_result = generate_dynamic_price(user_profile, policy_features, market_trends, context_data)
    print(pricing_result)
