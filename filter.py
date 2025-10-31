import json
# import ai
from urllib.parse import urlparse
from parsers.ebay import get_item_data as ebay_parse
from parsers.vestiairecollective import parse as ves_parse
from parsers.postmark import parse as post_parse

DATA = json.load(open('data/test.json', encoding='utf-8'))

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
                    "price": item["price"],
                })
                break
    return filtered


def start_parser(item):
    domain = extract_domain_name(item["link"])
    price = parsers_func.get(domain)(item['link'])
    item["price"] = price

    return item


def work(data):
    base_url = data['image_url']
    filtered_results = filter_results(data["results"])
    print(f"Итого найдено: {len(filtered_results)} подходящих сайтов")
    correct_response = []
    # emb1 = ai.image_embedding_from_url(base_url)
    # выводим красиво
    for i, item in enumerate(filtered_results, 1):
        price_data = item.get("price")

        if isinstance(price_data, dict):
            price_value = price_data.get("value")
        elif isinstance(price_data, str):
            price_value = price_data
        else:
            price_value = False

        if price_value != "Цена не найдена":
            print(f"   Цена:{price_value}\n")
            item["price"] = price_value
            correct_response.append(item)
        else:
            res = start_parser(item)
            if res is None:
                continue
            correct_response.append(res)
        item = correct_response[-1]
        print(f"{item}")
    print(f"всего изъято {len(correct_response)}")
    print("------------------------------------------------------")
    for item in correct_response:
        print(f"{item}")

work(DATA)
