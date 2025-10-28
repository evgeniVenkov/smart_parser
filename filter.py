import json
import ai
from urllib.parse import urlparse
from parsers.amazon import parse as AmazonParser

# DATA = json.load(open('data/test.json', encoding='utf-8'))
# BASE_URL = 'https://avatars.mds.yandex.net/i?id=8d7fe7f2055e71df511f15bda056fca5_l-5259114-images-thumbs&n=13'

allowed_domains = [
    "amazon.com", "amazon.ca", "amazon.co.uk",
    "ebay.com", "ebay.co.uk",
    "walmart.com",
    "fashionphile.com",
    "rebag.com",
    "therealreal.com",
    "nordstrom.com"
]
parsers = {
    "www.amazon.com": AmazonParser,
    "www.amazon.ca": AmazonParser,
    "www.amazon.co.uk": AmazonParser,
    "www.ebay.com": None,
    "www.ebay.co.uk": None,
    "www.walmart.com": None,
    "www.fashionphile.com": None,
    "www.rebag.com": None,
    "www.therealreal.com": None,
    "www.nordstrom.com": None,
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
                    "source": domain
                })
                break
    return filtered


def start_parser(item):
    domain = get_domain(item["link"])
    parsers[domain](item["link"])


def work(data,base_url):
    filtered_results = filter_results(data["results"])
    print(f"Итого найдено: {len(filtered_results)} англоязычных товаров")
    correct_response = []
    # выводим красиво
    for i, item in enumerate(filtered_results, 1):
        print(f"{i}. {item['title']} ({item['source']})")
        print(f"   {item['link']}")
        print(f"   {item['thumbnail']}\n")
        res = ai.similarity(base_url, item['thumbnail'])
        if res:
            correct_response.append(item)


    if len(correct_response) >= 1:
        print("Старт парсеров")
        for el in correct_response:
            start_parser(el)
    else:
        print("не нашлось похожих товаров")


