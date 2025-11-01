import json
# import ai
from urllib.parse import urlparse
from parsers.ebay import get_item_data as ebay_parse
from parsers.vestiairecollective import parse as ves_parse
from parsers.postmark import parse as post_parse
import re
import work_db

DATA = json.load(open('data/data.json', encoding='utf-8'))
data1 = json.load(open('data/filter.json', encoding='utf-8'))

allowed_domains = [
    "poshmark.com",
    "ebay.com", "ebay.co.uk",
    "vestiairecollective.com",
]
parsers_func = {
    "poshmark": post_parse,
    "vestiairecollective": ves_parse,
    "ebay": ebay_parse,
}


def normalize_price(data):
    """
    Очищает список объектов:
    - оставляет только числа с валютой ($ или €)
    - преобразует price в float и добавляет currency
    """
    cleaned = []

    for item in data:
        price = item.get("price")

        if price is None:
            continue

        # Если price — словарь (как в eBay), достанем значение
        if isinstance(price, dict):
            price_value = price.get("price")
        else:
            price_value = price

        price_str = str(price_value).replace(",", "").strip()

        # Поиск числа с валютой
        match = re.search(r"\$?(\d+(\.\d+)?)|(\d+(\.\d+)?\s*€)", price_str)
        if match:
            # Определяем валюту
            if "$" in match.group(0):
                currency = "USD"
                price_num = match.group(1)
            else:
                currency = "EUR"
                price_num = re.search(r"\d+(\.\d+)?", match.group(0)).group(0)

            item["price"] = float(price_num)
            item["currency"] = currency
            cleaned.append(item)

    return cleaned


def get_domain(url):
    parsed = urlparse(url)
    return parsed.netloc.lower()


def extract_domain_name(domain: str) -> str:
    # Если передана полная ссылка — достаём хост
    parsed = urlparse(domain)
    host = parsed.netloc or domain

    # Убираем www и поддомены
    parts = host.split('.')
    if len(parts) >= 2:
        # Берём предпоследнюю часть (основное имя)
        return parts[-2]
    return host


def filter_results(results):
    filtered = []
    for item in results:
        domain = get_domain(item["link"])
        for allowed in allowed_domains:
            if allowed in domain:
                filtered.append({
                    "title": item["title"],
                    "link": item["link"],
                    "thumbnail": item["thumbnail"],
                    "source": domain,
                    "price": item.get("price"),
                })
                break
    return filtered


def start_parser(item):
    domain = extract_domain_name(item["link"])
    price = parsers_func.get(domain)(item['link'])
    if price is None:
        return None
    item["price"] = price

    return item


def work(data):
    filtered_results = filter_results(data["visual_matches"])
    print(f"Итого найдено: {len(filtered_results)} подходящих сайтов")
    correct_response = []
    for i, item in enumerate(filtered_results, 1):
        price_data = item.get("price")
        if isinstance(price_data, dict):
            price_value = price_data.get("value")
        elif isinstance(price_data, str):
            price_value = price_data
        else:
            price_value = None

        if price_value is not None:
            item["price"] = price_value
            correct_response.append(item)
        else:
            res = start_parser(item)
            if res is None:
                continue
            correct_response.append(res)
    print(f"всего изъято {len(correct_response)}")
    correct_response = normalize_price(correct_response)
    for a, i in enumerate(correct_response):
        print(f'{a}-{i}')
    work_db.add_values(correct_response)

work(DATA)