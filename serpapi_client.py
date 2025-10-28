import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
SEARCH_URL = "https://serpapi.com/search.json"


async def search_by_image(image_url: str):
    """
    Отправляет запрос в SerpApi для поиска похожих изображений.
    Возвращает список результатов (title, link, thumbnail).
    """
    if not SERPAPI_KEY:
        raise ValueError("SERPAPI_KEY не найден в .env")

    params = {
        "engine": "google_lens",
        "url": image_url,
        "api_key": SERPAPI_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()

    # Забираем первые результаты
    results = []
    for item in data.get("visual_matches", []):
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "thumbnail": item.get("thumbnail"),
        })

    return results
