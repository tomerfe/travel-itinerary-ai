import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_image(query):
    """Fetch a relevant image URL from Pexels for the given query with attribution."""
    fallback_url = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop"
    pexels_api_key = os.getenv("PEXELS_API_KEY")
    print("Pexels key:", pexels_api_key)
    print("Query:", query)
    
    if not pexels_api_key:
        print("Warning: PEXELS_API_KEY not found in .env file")
        return fallback_url
    
    if not query or not isinstance(query, str) or query.strip() == "":
        return fallback_url
    
    try:
        # Search for images on Pexels
        url = "https://api.pexels.com/v1/search"
        headers = {
            "Authorization": pexels_api_key
        }
        params = {
            "query": query,
            "per_page": 1,
            "orientation": "landscape"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print("Pexels response:", data)
        
        if data["photos"]:
            photo = data["photos"][0]
            image_url = photo["src"]["large"]
            
            # Return image URL with attribution data
            attribution = {
                "photographer": photo["photographer"],
                "profile": photo["photographer_url"],
                "image_url": image_url
            }
            return attribution
        else:
            return fallback_url
            
    except Exception as e:
        print(f"Error fetching image for '{query}': {str(e)}")
        return fallback_url