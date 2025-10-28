from parsers.amazon import parse as AmazonParser
from filter import get_domain

url = 'https://www.amazon.ca/-/fr/OEIPSMK-Sweet-Korea-bandoulière-femme/dp/B0D796YGGL'
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
domain = get_domain(url)

parser = parsers[domain](url)
