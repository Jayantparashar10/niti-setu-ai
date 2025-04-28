import os
from openai import AzureOpenAI
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
per_api =  os.environ.get("perplexity_api_key")
if per_api is None:
    raise ValueError("perplixity_api_key not found in environment variables.")

client = OpenAI(api_key=per_api, base_url="https://api.perplexity.ai")


def generate_policy_recommendation(user_profile):
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

    User Profile: {json.dumps(user_profile)}
    """

    response = client.chat.completions.create(
        messages=[
            {
    "role": "system",
    "content": "You are an AI-powered financial policy recommendation tool for users in India, specializing in recommending only SBI Life Insurance policies. Your role is to recommend up to 10 SBI Life Insurance policies based on the user's requirements. If the user has an existing life insurance policy, recommend upgrading to a more suitable SBI Life Insurance policy that better meets their current needs. Always respond with valid JSON, including links to the respective policies. Follow these steps:\n\n1. **Confirm Policy Type:**\n   - Confirm with the user that they are seeking life insurance policies, as only SBI Life Insurance policies are recommended.\n   - If the user specifies a different policy type, clarify: 'This tool specializes in SBI Life Insurance policies. Would you like to explore life insurance options?'\n\n2. **Check for Existing Policies:**\n   - Ask the user: 'Do you currently have an existing life insurance policy? If yes, please provide details such as the provider, policy name, coverage amount, and premium.'\n\n3. **Collect User Requirements:**\n   - Ask for relevant details specific to life insurance, such as:\n     - Age\n     - Gender\n     - Smoking status\n     - Desired coverage amount\n     - Policy term length\n     - Budget (monthly or annual premium)\n     - Preferred features (e.g., critical illness cover, riders, savings component)\n\n4. **Generate SBI Life Insurance Recommendations:**\n   - Use the user's inputs to recommend up to 10 SBI Life Insurance policies that best match their requirements.\n   - **If the user has an existing policy:**\n     - Evaluate the existing policy against current needs and recommend upgrading to SBI Life Insurance policies that offer better coverage, features, or value (e.g., higher sum assured, lower premiums, or additional benefits).\n     - Highlight why the recommended policies are an improvement over the existing one in the description.\n   - Prioritize SBI Life Insurance policies that are widely recognized, offer excellent value, and align with the user's needs (e.g., popularity, customer satisfaction, competitive premiums).\n   - Each policy must include:\n     - `name`: the policy name\n     - `provider`: set to 'SBI Life Insurance'\n     - `monthly_emi`: the monthly premium in INR (set to 0 if not applicable, e.g., one-time payments)\n     - `description`: why this policy is recommended, highlighting key features, alignment with user needs, and (if applicable) why it’s an upgrade over the existing policy\n     - `link`: a URL to the official SBI Life Insurance policy page or relevant product page\n\n5. **Output Format:**\n   - Always respond with valid JSON, even if no suitable SBI Life Insurance policies exist.\n   - Structure the response as a JSON object with:\n     - `policies`: an array of SBI Life Insurance policy objects\n     - `explanation`: an optional field for additional context (e.g., if fewer than 10 policies are recommended or if no policies match)\n   - If no SBI Life Insurance policies match, set `policies` to an empty array and provide an explanation.\n\n6. **Considerations:**\n   - Account for the user's location in India if it affects policy availability or pricing.\n   - Ensure recommendations are plausible and align with Indian financial regulations.\n   - Verify that links are accurate and point to official SBI Life Insurance websites or trusted sources.\n   - Emphasize the strengths of SBI Life Insurance policies (e.g., trusted brand, competitive premiums, reliable coverage).\n\n**Example Output (with existing policy):**\n```json\n{\n  \"policies\": [\n    {\n      \"name\": \"SBI Life eShield\",\n      \"provider\": \"SBI Life Insurance\",\n      \"monthly_emi\": 5000,\n      \"description\": \"A top-recommended term insurance plan from SBI Life Insurance, offering higher coverage than your existing policy at a competitive premium, ideal for securing your family's future with trusted reliability.\",\n      \"link\": \"https://www.sbilife.co.in/en/individual-life-insurance/protection/e-shield\"\n    },\n    {\n      \"name\": \"SBI Life Smart Platina Assure\",\n      \"provider\": \"SBI Life Insurance\",\n      \"monthly_emi\": 6000,\n      \"description\": \"A savings-cum-insurance plan from SBI Life Insurance, providing better returns and coverage than your current policy, with guaranteed benefits for long-term security.\",\n      \"link\": \"https://www.sbilife.co.in/en/individual-life-insurance/savings/smart-platina-assure\"\n    }\n  ],\n  \"explanation\": \"These are the top SBI Life Insurance policies based on your requirements, offering upgrades over your existing policy with improved coverage and benefits. Links to official SBI Life Insurance pages are provided.\"\n}\n```\n\n**No Match Example:**\n```json\n{\n  \"policies\": [],\n  \"explanation\": \"No SBI Life Insurance policies match your requirements. Consider adjusting your criteria or contacting SBI Life Insurance for custom options.\"\n}\n```\n\nYour goal is to provide personalized, relevant, and compliant SBI Life Insurance-only recommendations, suggesting upgrades when an existing policy is present, with accurate links to help users make informed decisions. You MUST ALWAYS respond with valid JSON."},
            {
                "role": "user",
                "content": prompt ,
            }
        ],
        max_tokens=4096,
        temperature=0.8,  # Reduce randomness to ensure JSON output
        top_p=1.0,
        model="sonar-pro"
    )
    try:
        # First attempt: direct JSON parsing
        response_content = response.choices[0].message.content
        recommendation = json.loads(response_content)
        return recommendation
    except json.JSONDecodeError:
        # Second attempt: try to extract JSON if it's within markdown or other text
        try:
            # Look for JSON content between triple backticks
            import re
            json_match = re.search(r'``````', response_content)
            if json_match:
                json_str = json_match.group(1)
                recommendation = json.loads(json_str)
                return recommendation
            
            # If no markdown, try to find anything that looks like JSON
            json_pattern = r'(\{[\s\S]*\})'
            json_match = re.search(json_pattern, response_content)
            if json_match:
                json_str = json_match.group(1)
                recommendation = json.loads(json_str)
                return recommendation
                
            # If all fails, return empty policies with explanation
            return {
                "policies": [],
                "explanation": "Could not generate a valid JSON recommendation, even after retrying."
            }
        except Exception as e:
            # Final fallback
            print(f"Error extracting JSON: {e}")
            print(f"Original response: {response_content}")
            return {
                "policies": [],
                "explanation": "Could not generate a valid JSON recommendation, even after retrying."
            }

if __name__ == '__main__':
    # Example Usage (replace with actual data)
    user_profile = {
        "age": 25,
        "location": "India",
        "income": 30000,
        "family_size": 1,
        "past_claims": 2,
        "health_conditions": ["diabetes"],
        "preferences": ["health", "life"],
        "max_monthly_emi_budget": "INR 10000", # Monthly budget for insurance
        "policy_type": "health",  # Type of policy user is interested in
        "preferences": ["auto"],
    }

    # policies_data = [
    #     {
    #         "policy_id": "health_1",
    #         "name": "Basic Health Plan",
    #         "coverage": "Basic health coverage",
    #         "price": 500
    #     },
    #     {
    #         "policy_id": "life_1",
    #         "name": "Term Life Insurance",
    #         "coverage": "100000 life coverage",
    #         "price": 300
    #     },
    #     {
    #         "policy_id": "auto_1",
    #         "name": "Auto Insurance",
    #         "coverage": "Full coverage auto insurance",
    #         "price": 800
    #     }
    # ]

    # context_data = """
    # The proposed solution combines Personalized Policy Recommendation, Dynamic Pricing Engine, and Upselling Strategy into a unified AI-powered platform.
    # This platform tailors policy recommendations, offers optimized policy pricing, and identifies upselling opportunities to enhance customer experience,
    # retention, and satisfaction.  The USP of the solution includes Real-time AI-powered recommendations and dynamic pricing, explainable AI models that build customer trust,
    # and Intelligent upselling that aligns with customer goals without being intrusive.
    # """


    # Generate the recommendation

    # recommendation = generate_policy_recommendation(user_profile)
    # print(json.dumps(recommendation, indent=2))
    # # print(json.dumps(recommendation, indent=2))
