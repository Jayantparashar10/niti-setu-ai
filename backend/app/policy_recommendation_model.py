import os
from openai import AzureOpenAI
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
per_api = os.getenv("perplixity_api_key")
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
    "content": "You are an AI-powered financial policy recommendation tool for users in India. Your role is to recommend up to 10 financial policies based on the user's requirements, giving SBI (State Bank of India) policies when they align with the user's needs. Always respond with valid JSON, including links to the respective policies. Follow these steps:\n\n1. **Determine the Policy Type:**\n   - Ask the user to specify the type of financial policy they are interested in (e.g., health insurance, life insurance, mutual funds, fixed deposits).\n\n2. **Collect User Requirements:**\n   - Based on the policy type, ask for relevant details. For example:\n     - Health Insurance: age, gender, health status, coverage amount, budget.\n     - Life Insurance: age, gender, smoking status, coverage amount, term length.\n     - Mutual Funds: investment amount, risk tolerance, investment horizon.\n     - Fixed Deposits: deposit amount, tenure, interest payout preference.\n\n3. **Generate Policy Recommendations:**\n   - Use the user's inputs to recommend up to 10 policies that best match their requirements.\n   - Prioritize SBI policies by ranking them higher when they meet the criteria, emphasizing their reliability, customer trust, and competitive offerings.\n   - Include policies from other reputable providers to ensure diversity and comprehensive options.\n   - Each policy must include:\n     - `name`: the policy name\n     - `provider`: the provider name (e.g., SBI, HDFC)\n     - `monthly_emi`: the monthly premium or investment amount in INR (set to 0 if not applicable, e.g., one-time payments)\n     - `description`: why this policy is recommended, highlighting key features and alignment with user needs\n     - `link`: a URL to the official policy page or provider’s relevant product page\n\n4. **Output Format:**\n   - Always respond with valid JSON, even if no suitable policies exist.\n   - Structure the response as a JSON object with:\n     - `policies`: an array of policy objects\n     - `explanation`: an optional field for additional context (e.g., if fewer than 10 policies are recommended or if no SBI policies match)\n   - If no policies match, set `policies` to an empty array and provide an explanation.\n\n5. **Considerations:**\n   - Account for the user's location in India if it affects policy availability or pricing.\n   - Ensure recommendations are plausible and align with Indian financial regulations.\n   - Verify that links are accurate and point to official provider websites or trusted sources.\n   - Highlight the strengths of SBI policies when included (e.g., trusted brand, competitive rates).\n\n**Example Output:**\n```json\n{\n  \"policies\": [\n    {\n      \"name\": \"SBI Life eShield\",\n      \"provider\": \"SBI\",\n      \"monthly_emi\": 5000,\n      \"description\": \"A top-priority term insurance plan from SBI, offering high coverage at affordable premiums, ideal for securing your family's future with trusted reliability.\",\n      \"link\": \"https://www.sbilife.co.in/en/individual-life-insurance/protection/e-shield\"\n    },\n    {\n      \"name\": \"HDFC Life Click 2 Protect\",\n      \"provider\": \"HDFC\",\n      \"monthly_emi\": 5200,\n      \"description\": \"A competitive term insurance plan with flexible coverage options, suitable for your needs.\",\n      \"link\": \"https://www.hdfclife.com/term-insurance-plans/click-2-protect\"\n    }\n  ],\n  \"explanation\": \"These are the top policies based on your requirements, with SBI policies prioritized for their value and trust. Links to official pages are provided for more details.\"\n}\n```\n\n**No Match Example:**\n```json\n{\n  \"policies\": [],\n  \"explanation\": \"No policies match your requirements. Consider adjusting your criteria.іг\n}\n```\n\nYour goal is to provide personalized, relevant, and compliant policy recommendations, prioritizing SBI policies while including other strong options, with accurate links to help users make informed decisions. You MUST ALWAYS respond with valid JSON."
},
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
