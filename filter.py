import json
import ai
from urllib.parse import urlparse

DATA = json.load(open('data/test.json', encoding='utf-8'))

allowed_domains = [
    "poshmark.com",
    "ebay.com", "ebay.co.uk",
    "vestiairecollective.com",
]
parsers = {
    "www.poshmark.com": None,
    "www.vestiairecollective.com": None,
    "www.ebay.com": None,
    "www.ebay.co.uk": None,
}


def get_domain(url):
    parsed = urlparse(url)
    return parsed.netloc.lower()


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
    domain = get_domain(item["link"])
    parsers[domain](item["link"])


def work(data):
    base_url = data['image_url']
    filtered_results = filter_results(data["results"])
    print(f"Итого найдено: {len(filtered_results)} подходящих сайтов")
    correct_response = []
    emb1 = ai.image_embedding_from_url(base_url)
    # выводим красиво
    for i, item in enumerate(filtered_results, 1):
        print(f"{i}. {item['title']} ({item['source']})")
        print(f"   {item['link']}")
        print(f"   {item['thumbnail']}\n")
        price_data = item.get("price")

        if isinstance(price_data, dict):
            price_value = price_data.get("value")
        elif isinstance(price_data, str):
            price_value = price_data
        else:
            price_value = None

        if price_value:
            print(f"   Цена: {price_value}\n")
        else:
            print("   Цена не найдена\n")

        res = ai.similarity(emb1, item['thumbnail'])
        if res:
            correct_response.append(item)

    if len(correct_response) >= 1:
        print("Старт парсеров!\n"
              f"всего подходящих товаров {len(correct_response)}")

        # for el in correct_response:
        #     start_parser(el)
    else:
        print("не нашлось похожих товаров")


work(DATA)
