import httpx
from fastapi import FastAPI, Query, File, UploadFile
from typing import Optional
from dotenv import load_dotenv
import os
import re
from imgbb import upload_to_imgbb

app = FastAPI(title="Image Price Finder")
load_dotenv()
SEARCH_URL = "https://serpapi.com/search.json"
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
app = FastAPI()


def search_price(data):
    results = []
    for item in data.get("visual_matches", []):
        title = item.get("title")
        link = item.get("link")
        thumbnail = item.get("thumbnail")
        snippet = item.get("snippet", "")

        # 1️⃣ Проверяем явное поле "price"
        price = item.get("price")

        # 2️⃣ Если нет — ищем в rich_snippet (там часто массив с валютой)
        if not price:
            rich_snippet = item.get("rich_snippet", {})
            if rich_snippet:
                extensions = rich_snippet.get("top", {}).get("extensions", [])
                # Пример: ["$450.00", "Free shipping"]
                for ext in extensions:
                    if "$" in ext or "€" in ext:
                        price = ext
                        break

        # 3️⃣ Если и там нет — ищем шаблон цены прямо в тексте
        if not price:
            text_to_search = " ".join([title or "", snippet or ""])
            match = re.search(r"[\$€£]\s?\d+(?:[\.,]\d{2})?", text_to_search)
            if match:
                price = match.group(0)

        results.append({
            "title": title,
            "link": link,
            "thumbnail": thumbnail,
            "price": price or "Цена не найдена"
        })

    return {"count": len(results), "results": results}


@app.get("/search")
async def search(
    image_url: str = Query(..., description="URL изображения"),
    query_text: Optional[str] = Query(None, description="Дополнительный текст для уточнения поиска"),
):
    """
    Эндпоинт: принимает URL изображения и опционально текстовое уточнение.
    Если текст передан — отправляет оба параметра в SerpApi Google Lens.
    """
    params = {
        "engine": "google_lens",
        "url": image_url,
        "api_key": SERPAPI_KEY,
    }

    if query_text:
        params["q"] = query_text  # добавляем уточняющий текст

    async with httpx.AsyncClient() as client:
        response = await client.get(SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
    return search_price(data)


@app.post("/search/upload")
async def search_by_image(
        file: UploadFile = File(...),
        query_text: Optional[str] = Query(None, description="Дополнительный текст для уточнения поиска"),
):
    # читаем байты
    image_bytes = await file.read()
    # загружаем на imgbb
    image_url = await upload_to_imgbb(image_bytes)

    return search(image_url, query_text)

