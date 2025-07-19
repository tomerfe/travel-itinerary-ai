import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("UNSPLASH_API_KEY")
print("Using API Key:", api_key[:6] + "..." if api_key else "None")

query = "mountains"
url = "https://api.unsplash.com/search/photos"
params = {
    "query": query,
    "client_id": api_key,
    "per_page": 1
}

response = requests.get(url, params=params)
print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    image_url = data["results"][0]["urls"]["regular"] if data["results"] else "No image found"
    print("Image URL:", image_url)
else:
    print("Error:", response.json())
