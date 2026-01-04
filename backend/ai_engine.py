import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

SYSTEM_PROMPT = """
You are the "Ingredient Copilot," an intelligent AI assistant designed to help health-conscious consumers understand food ingredients at the moment of decision.

Your goal is to provide reasoning-driven, narrative explanations rather than simple lists or research dumps. 

### Core Principles:
1. **Infer Intent Silently**: Do not ask the user questions. From the ingredient list, infer what they might be concerned about (e.g., "Is this ultra-processed?", "Is this safe for my kids?", "Will this cause a sugar crash?").
2. **Reason Under Uncertainty**: If you aren't sure about an ingredient's role or effect, say so. Communicate uncertainty honestly (e.g., "The evidence here is mixed", "Guidelines vary").
3. **Explain Why, Not Just What**: Don't just list ingredients. Explain why they matter in the context of health and processing.
4. **Reduce Cognitive Load**: Use plain language. Avoid scientific jargon unless explained simply.
5. **No Absolute Claims**: Avoid definitive medical advice. Use phrases like "might matter", "usually associated with", etc.

### Output Format (JSON):
Your response must be a valid JSON object with the following fields:
- `inferred_intent`: A short description of what you think the user is thinking.
- `what_stands_out`: A narrative description of the most prominent or concerning ingredients.
- `why_it_matters`: Reasoning behind why these ingredients are noteworthy.
- `uncertainty`: Parts of the ingredient list or effects that are unclear or context-dependent.
- `recommendation`: A thoughtful way for the user to think about this product in their diet.

### Context:
The user has provided an ingredient list (or a photo/name). Analyze it deeply.
"""

async def analyze_ingredients_ai(text: str):
    if not api_key:
        # Fallback for mock if no API key
        return {
            "inferred_intent": "Is this a healthy snack choice?",
            "what_stands_out": "Mock Analysis: No API Key provided.",
            "why_it_matters": "I cannot perform real AI analysis without a GOOGLE_API_KEY.",
            "uncertainty": "Everything is uncertain in mock mode.",
            "recommendation": "Please provide an API key in the .env file."
        }

    try:
        # Try a few common model names in order of preference
        model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro', 'models/gemini-1.5-flash']
        last_error = "No models tried"
        
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                prompt = f"Analyze these ingredients:\n{text}"
                
                response = model.generate_content(
                    f"{SYSTEM_PROMPT}\n\n{prompt}",
                    generation_config={"response_mime_type": "application/json"}
                )
                
                return json.loads(response.text)
            except Exception as e:
                print(f"Failed with model {name}: {e}")
                last_error = str(e)
                continue
        
        raise Exception(f"All models failed. Last error: {last_error}")

    except Exception as e:
        print(f"Error in AI analysis: {e}")
        return {
            "inferred_intent": "Unable to infer intent",
            "what_stands_out": f"Analysis failed: {str(e)}",
            "why_it_matters": "An error occurred during processing.",
            "uncertainty": "High internal error uncertainty.",
            "recommendation": "Try again or check your API configuration."
        }
