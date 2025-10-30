from PIL import Image
import requests
from io import BytesIO
import torch
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity

# Загружаем модель
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

from PIL import Image
from io import BytesIO
import requests, time


def fetch_image(url, retries=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/138.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    for i in range(retries):
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
            return resp.content
        except requests.RequestException:
            time.sleep(2)
    return None


def image_embedding_from_url(url):
    content = fetch_image(url)
    if content is None:
        return None
    image = Image.open(BytesIO(content)).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embeddings = model.get_image_features(**inputs)
    embeddings = embeddings / embeddings.norm(p=2, dim=-1, keepdim=True)
    return embeddings.numpy()


def similarity(emb1, url2):
    emb2 = image_embedding_from_url(url2)
    if emb1 is None or emb2 is None:
        print(f"Ошибка: один из эмбеддингов пустой. emb1={emb1}, emb2={emb2}")
        return None
    similarit = cosine_similarity(emb1, emb2)[0][0]
    print("Сходство:", similarit)

    if similarit > 0.9:
        print("Похоже на один и тот же товар ✅")
        return True
    else:
        print("Это разные товары ❌")
        return False
