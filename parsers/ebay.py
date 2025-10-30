import requests
from dotenv import load_dotenv
import os
load_dotenv()
SEARCH_URL = "https://serpapi.com/search.json"
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


item_id = "395716071598"

params = {
    "engine": "ebay",
    "_nkw": item_id,
    "api_key": SERPAPI_KEY
}

response = requests.get(SEARCH_URL, params=params)
data = response.json()
print(data)
items = data.get("items", [])
if items:
    item = items[0]
    item_data = {
        "title": item.get("title"),
        "price": item.get("price", {}).get("value"),
        "currency": item.get("price", {}).get("currency"),
        "link": item.get("link"),
        "thumbnail": item.get("thumbnail")
    }
    print(item_data)
else:
    print("Товар не найден")

