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

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(SEARCH_URL, params=params)
            response.raise_for_status()
            data = response.json()
            data['image_url'] = image_url
    except httpx.ReadTimeout:
        return {"error": "Сервер поиска не ответил вовремя"}

    return data


@app.post("/search/upload")
async def search_by_image(
        file: UploadFile = File(...),
        query_text: Optional[str] = Query(None, description="Дополнительный текст для уточнения поиска"),
):
    # читаем байты
    image_bytes = await file.read()
    # загружаем на imgbb
    image_url = await upload_to_imgbb(image_bytes)
    data = await search(image_url, query_text)
    return data
