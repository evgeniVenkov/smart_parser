import requests
import filter

api_url = "http://127.0.0.1:8000/search"
url = input("Enter the URL: ")

params = {"image_url": url}  # ключ совпадает с аргументом эндпоинта

try:
    response = requests.get(api_url, params=params, timeout=15)
    response.raise_for_status()
    result = response.json()
    print("Ответ API:", result)
    filter.work(result, url)
except requests.exceptions.RequestException as e:
    print("Ошибка при запросе к API:", e)
