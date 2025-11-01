import requests
from filter import work
# URL твоего локального API
url = "http://127.0.0.1:8000/search/upload"

# путь к картинке
image_path = "data/images/test.jpg"


# открываем файл в бинарном режиме
with open(image_path, "rb") as img:
    files = {"file": ("test.jpg", img, "image/jpeg")}
    response = requests.post(url, files=files)

# вывод результата
print(response.status_code)
work(response.json())

