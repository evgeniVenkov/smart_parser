import httpx
import os
from dotenv import load_dotenv

load_dotenv()
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

async def upload_to_imgbb(image_bytes: bytes):
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": IMGBB_API_KEY,
    }
    files = {
        "image": ("image.jpg", image_bytes, "image/jpeg")
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data=payload, files=files)
        resp.raise_for_status()
        return resp.json()["data"]["url"]
