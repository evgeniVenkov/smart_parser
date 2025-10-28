from fastapi import FastAPI, Query
from serpapi_client import search_by_image

app = FastAPI(title="Image Price Finder")

@app.get("/search")
async def search(image_url: str = Query(..., description="URL изображения")):
    """
    Простой эндпоинт: принимает URL изображения и возвращает найденные результаты.
    """
    try:
        results = await search_by_image(image_url)
        return {"count": len(results), "results": results}
    except Exception as e:
        return {"error": str(e)}
