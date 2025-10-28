from playwright.sync_api import sync_playwright


def parse(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        # Ждём немного, чтобы JS подгрузил цену
        page.wait_for_timeout(3000)

        # Выбираем все span.a-offscreen
        price_elements = page.query_selector_all("span.a-price > span.a-offscreen")

        price = None
        for el in price_elements:
            text = el.inner_text().strip()
            if text:  # берем первый непустой
                price = text
                break

        print("Price:", price)

        browser.close()
