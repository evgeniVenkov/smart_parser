from playwright.sync_api import sync_playwright


def parse(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=100)
            page = browser.new_page()
            page.goto(url)

            # Ждём, пока появится любой span с ценой
            page.wait_for_timeout(5000)  # даём JS подгрузить страницу

            # Пытаемся найти актуальную цену
            price_selectors = [
                'span[data-cy="product_price"]',       # обычная цена
                'span[data-cy="product_price_drop"]',  # старая цена

            ]

            price = None
            for selector in price_selectors:
                el = page.query_selector(selector)
                if el:
                    price = el.inner_text().strip()
                    break

            # Ссылка на картинку
            img_element = page.query_selector('img[class*="vc-images_image__"]')
            img_url = img_element.get_attribute("src") if img_element else None

            data = {
                "url": url,
                "price": price,
                "image_url": img_url
            }

            browser.close()
            return data['price']
    except Exception as e:
        print(f"ошибка в парсере vest {e}")
