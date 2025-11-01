import requests
from dotenv import load_dotenv
import os
import re
load_dotenv()
SEARCH_URL = "https://serpapi.com/search.json"
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def get_item_data(url: str):
    print("запуск парсера ebay")
    item_id = extract_item_id(url)
    if item_id is None:
        print("Item not found")
        return None
    params = {
        "engine": "ebay",
        "_nkw": item_id,
        "api_key": SERPAPI_KEY
    }
    response = requests.get(SEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()

    organic_results = data.get("organic_results", [])
    if not organic_results:
        print("не смог вытащить данные из ссылки")
        return None

    # Берём первый результат
    item = organic_results[0]
    item_data = {
        "title": item.get("title"),
        "price": item.get("price", {}).get("extracted"),
        "currency": item.get("price", {}).get("raw", "").replace(str(item.get("price", {}).get("extracted", "")), "").strip(),
        "link": item.get("link"),
        "thumbnail": item.get("thumbnail")
    }

    return item_data['price']


def extract_item_id(url: str) -> str:
    """
    Извлекает item_id из ссылки на eBay и проверяет её формат.

    Пример:
        https://www.ebay.com/itm/395716071598 -> '395716071598'
    """
    pattern = r"^https://www\.ebay\.com/itm/(\d+)(?:[/?].*)?$"
    match = re.match(pattern, url.strip())

    if not match:
        print("Некорректная ссылка. Ожидается формат: https://www.ebay.com/itm/<item_id>\n"
              f"{url}")
        return None

    return match.group(1)




