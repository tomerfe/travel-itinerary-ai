import os
import json
import re
import requests
from io import BytesIO
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

def generate_trip_summary_image(user_input):
    """Generate a trip summary image using multiple approaches."""
    
    # Approach 1: Try Hugging Face Space (more reliable)
    try:
        return generate_image_via_hf_space(user_input)
    except Exception as e:
        print(f"HF Space approach failed: {e}")
    
    # Approach 2: Try direct API with different models
    try:
        return generate_image_via_hf_api(user_input)
    except Exception as e:
        print(f"HF API approach failed: {e}")
    
    # Approach 3: Use a simple AI image generation service
    try:
        return generate_image_via_pollinations(user_input)
    except Exception as e:
        print(f"Pollinations approach failed: {e}")
    
    # If all approaches fail, return placeholder
    print("All image generation approaches failed, using placeholder")
    return "https://via.placeholder.com/1024x768?text=AI+Image+Generation+Unavailable"

def generate_image_via_pollinations(user_input):
    """Generate image using Pollinations AI (free, no API key needed)."""
    prompt = (
        f"A vibrant, photorealistic image of {user_input['people']} "
        f"enjoying {user_input['interests']} in {user_input['destination']} "
        f"during {user_input['season_or_dates']}, highly detailed, realistic"
    )
    
    # Pollinations AI - free image generation
    encoded_prompt = requests.utils.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&seed=42"
    
    print(f"Trying Pollinations AI with prompt: {prompt[:100]}...")
    
    try:
        resp = requests.get(image_url, timeout=30)
        if resp.status_code == 200 and resp.headers.get('content-type', '').startswith('image/'):
            print("Successfully generated image with Pollinations AI")
            return BytesIO(resp.content)
        else:
            raise Exception(f"Failed to get image: {resp.status_code}")
    except Exception as e:
        print(f"Pollinations AI error: {e}")
        raise

def generate_image_via_hf_space(user_input):
    """Try using Hugging Face Spaces API (often more reliable)."""
    HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
    
    if not HF_TOKEN or HF_TOKEN == "your_huggingface_api_key_here":
        raise Exception("Hugging Face API key not configured")
    
    # Try a popular Stable Diffusion space
    space_url = "https://hf.co/spaces/stabilityai/stable-diffusion"
    api_url = f"https://stabilityai-stable-diffusion.hf.space/api/predict"
    
    prompt = (
        f"A vibrant, photorealistic image of {user_input['people']} "
        f"enjoying {user_input['interests']} in {user_input['destination']} "
        f"during {user_input['season_or_dates']}, highly detailed, realistic, 8k"
    )
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"data": [prompt, "", 7.5, 20, 512, 512]}
    
    print(f"Trying Hugging Face Space: {space_url}")
    
    resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
    if resp.status_code == 200:
        result = resp.json()
        if 'data' in result and result['data']:
            image_url = result['data'][0]
            img_resp = requests.get(image_url, timeout=30)
            if img_resp.status_code == 200:
                print("Successfully generated image via HF Space")
                return BytesIO(img_resp.content)
    
    raise Exception(f"HF Space failed: {resp.status_code}")

def generate_image_via_hf_api(user_input):
    """Try the original HF API approach with updated models."""
    HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
    
    if not HF_TOKEN or HF_TOKEN == "your_huggingface_api_key_here":
        raise Exception("Hugging Face API key not configured")
    
    # Try newer/different models that might be working
    models_to_try = [
        "black-forest-labs/FLUX.1-schnell",  # Newer, faster model
        "stabilityai/sdxl-turbo",            # SDXL Turbo
        "segmind/SSD-1B",                    # Smaller, faster model
        "CompVis/stable-diffusion-v1-4",    # Classic fallback
    ]
    
    prompt = (
        f"A vibrant, photorealistic image of {user_input['people']} "
        f"enjoying {user_input['interests']} in {user_input['destination']} "
        f"during {user_input['season_or_dates']}, highly detailed, realistic, 8k"
    )
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    for model in models_to_try:
        try:
            API_URL = f"https://api-inference.huggingface.co/models/{model}"
            print(f"Trying HF API model: {model}")
            
            payload = {"inputs": prompt}
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            if resp.status_code == 200:
                if resp.headers.get('content-type', '').startswith('image/'):
                    print(f"Successfully generated image with HF API model: {model}")
                    return BytesIO(resp.content)
                else:
                    print(f"Model {model} response was not an image:", resp.text[:200])
                    continue
            else:
                print(f"Model {model} failed with status {resp.status_code}: {resp.text[:200]}")
                continue
                
        except Exception as e:
            print(f"Model {model} error: {e}")
            continue
    
    raise Exception("All HF API models failed")

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