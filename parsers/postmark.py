from playwright.sync_api import sync_playwright


def parse(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        page.goto(url)

        # Ждём блок с ценами
        page.wait_for_selector('div.listing__ipad-centered', timeout=15000)

        # Берём все span внутри p.h1
        spans = page.query_selector_all('div.listing__ipad-centered p.h1 span')

        price = spans[0].inner_text().strip() if len(spans) > 0 else None
        old_price = spans[1].inner_text().strip() if len(spans) > 1 else None

        data = {
            "url": url,
            "price": price,
            "old_price": old_price
        }

        browser.close()
        return data['price']



