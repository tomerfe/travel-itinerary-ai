import os
import json
import re
from typing import List, Dict, Any, Union
from dotenv import load_dotenv  # type: ignore
import cohere

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("COHERE_API_KEY is not set. Check your .env file.")

co = cohere.Client(api_key)

def extract_json(text: str) -> str:
    """Extract the first JSON object from a string."""
    match = re.search(r'(\{.*\})', text, re.DOTALL)
    if match:
        return match.group(1)
    return text  # fallback to original text

def truncate_to_last_complete_json_object(json_str: str) -> str:
    """Truncate a JSON object string to the last complete closing bracket."""
    last_bracket = json_str.rfind('}')
    if last_bracket != -1:
        return json_str[:last_bracket+1]
    return json_str

def generate_itineraries(user_input: dict) -> Union[Dict, Dict[str, str]]:
    """
    Generate 1 trip itinerary using Cohere's Command R+ model based on user input.
    Returns an itinerary dict or an error message dict.
    """
    # Build the prompt dynamically
    prompt = (
        "You are a helpful travel planner that creates a multi-day itinerary based on user preferences. "
        "Respond in JSON format as a single itinerary. The itinerary should have a 'title' and a 'days' list. "
        "Each day should include: day number, activity name(s), and a short description. "
        "Keep descriptions concise and ensure the entire response fits within the token limit. "
        "Do not include any text outside the JSON.\n"
        "Please create one unique, concise travel itinerary based on these preferences:\n"
    )
    for key, label in [
        ("destination", "Destination"),
        ("num_days", "Number of days"),
        ("season_or_dates", "Season or dates"),
        ("people", "Group info"),
        ("interests", "Interests")
    ]:
        value = user_input.get(key)
        if value:
            prompt += f"{label}: {value}\n"

    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            temperature=0.7,
            max_tokens=1500
        )
        content = response.generations[0].text.strip()
        json_str = extract_json(content)
        try:
            # Try parsing as-is
            itinerary = json.loads(json_str)
            return itinerary
        except Exception:
            # Try truncating to last complete object and parse again
            truncated = truncate_to_last_complete_json_object(json_str)
            try:
                itinerary = json.loads(truncated)
                return itinerary
            except Exception as e:
                return {"error": f"Failed to parse JSON: {str(e)}", "raw_output": truncated}
    except Exception as e:
        return {"error": f"Cohere API error: {str(e)}"} 