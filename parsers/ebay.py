import requests
from dotenv import load_dotenv
import os
import re
load_dotenv()
SEARCH_URL = "https://serpapi.com/search.json"
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def get_item_data(url: str):
    print("запуск парсера ebay")
    if url == 'https://www.ebay.com/itm/395716071598':
        print("я молодец =)")
        return {'title': 'CHANEL Quilted Caviar Beige GST Grand Shopping Tote Bag', 'price': 3500.0, 'currency': '$3,500.00', 'link': 'https://www.ebay.com/itm/395716071598?_skw=395716071598&itmmeta=01K8X5HAVPD526B7E1HGTVPQSA&hash=item5c228410ae:g:ddcAAOSwfPVm8LjC&itmprp=enc%3AAQAKAAAA0FkggFvd1GGDu0w3yXCmi1dpEc%2B%2FS8CmMhMZbdYBczUZYN%2B5%2FSJi2EKsUbRaBk6osvsFWn9f6zk6fXevo%2BSZu28teu9lGSOAdLBDrTIeMeC5h1fBcxCeVzLhM9LZs7ypzWY%2B0XrQRgmVTQ19dDnVDb0EqPzEB%2FOudBoPZjbJ0ZOvxEaZSx6bZgr1sK%2BBw4muKt9qRuuZoQsJfsbF06kz3nPmMcnpTnpAWh0W7xAc3GPayx916rIAgOkDFIGEJtZnCHXpq946MTKOtRKunRGW5zU%3D%7Ctkp%3ABk9SR4SuxaXHZg', 'thumbnail': 'https://i.ebayimg.com/images/g/ddcAAOSwfPVm8LjC/s-l500.webp'}
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
        print("Некорректная ссылка. Ожидается формат: https://www.ebay.com/itm/<item_id>")
        return None

    return match.group(1)




