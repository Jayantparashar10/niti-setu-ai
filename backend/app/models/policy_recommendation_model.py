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

def generate_policy_recommendation(user_profile, policies_data, context_data):
    """
    Generates personalized policy recommendations based on user profile,
    available policies, and context.  Improves prompt to *force* JSON output.

    Args:
        user_profile (dict): User's demographic data, preferences, and past behavior.
        policies_data (list): A list of dictionaries, each representing an insurance policy.
        context_data (str): Content from the PPT, providing project context.

    Returns:
        dict: A dictionary containing the policy recommendation and explanation.  Returns
              a default if a valid JSON cannot be generated.
    """

    prompt = f"""
    You are an expert insurance advisor providing personalized policy recommendations.
    Based on the user profile, available policies, and the following project context,
    recommend the *single best* insurance policy for the user. Explain why you recommend
    this particular policy, emphasizing how it aligns with the user's needs and preferences.

    **IMPORTANT: You *MUST* respond with a valid JSON object.  Do NOT include any
    introductory or conversational text. The JSON object *MUST* conform to the following schema:**
gi
    ```
    {{
        "policy_id": "policy id here (e.g., health_1, life_2).  If NO suitable policy exists, policy_id MUST be null",
        "explanation": "Detailed explanation of the recommendation (or why NO policy is suitable). This MUST be a complete and well-formed sentence"
    }}
    ```

    User Profile: {json.dumps(user_profile)}

    Available Policies: {json.dumps(policies_data)}

    Project Context (from Leximinds-HACK-AI-THON-2024.pptx): {context_data}
    """

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a JSON-outputting expert insurance advisor.  You MUST ALWAYS respond with valid JSON, even if no suitable policy exists. policy_id MUST be set to null in this situation.  ex: {\"policy_id\": null, \"explanation\": \"...\"}",
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
        recommendation = json.loads(response.choices[0].message.content)
        return recommendation
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}") # Print the error for debugging
        print(f"Response content: {response.choices[0].message.content}") # Print the problematic content

        return {"policy_id": None, "explanation": "Could not generate a valid JSON recommendation, even after retrying."}


if __name__ == '__main__':
    # Example Usage (replace with actual data)
    user_profile = {
        "age": 25,
        "location": "New York",
        "income": 30000,
        "family_size": 1,
        "past_claims": 2,
        "preferences": ["auto"],
    }

    policies_data = [
        {
            "policy_id": "health_1",
            "name": "Basic Health Plan",
            "coverage": "Basic health coverage",
            "price": 500
        },
        {
            "policy_id": "life_1",
            "name": "Term Life Insurance",
            "coverage": "100000 life coverage",
            "price": 300
        },
        {
            "policy_id": "auto_1",
            "name": "Auto Insurance",
            "coverage": "Full coverage auto insurance",
            "price": 800
        }
    ]

    context_data = """
    The proposed solution combines Personalized Policy Recommendation, Dynamic Pricing Engine, and Upselling Strategy into a unified AI-powered platform.
    This platform tailors policy recommendations, offers optimized policy pricing, and identifies upselling opportunities to enhance customer experience,
    retention, and satisfaction.  The USP of the solution includes Real-time AI-powered recommendations and dynamic pricing, explainable AI models that build customer trust,
    and Intelligent upselling that aligns with customer goals without being intrusive.
    """

    recommendation = generate_policy_recommendation(user_profile, policies_data, context_data)
    print(recommendation)
