# https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf
# 1. Получение картинок по ключевому слову "moon"

import requests

url = "https://images-api.nasa.gov/search"

params = {
    "q": "moon",
    "page": "1",
    "media_type": "image",
    "year_start": "1920",
    "year_end": "2020"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    images = response.json()["collection"]["items"]
    for image in images:
        image_url = image["links"][0]["href"]
        print(image_url)
else:
    print("Ошибка:", response.json())


# 2. Получение фотографии по nasa_id, просмотр дополнительной информации

import json


def save_json(data, data_path):
    """Функция, которая сохраняет данные ответа в файл.
    :param data: словарь с данными пользователей
    :param data_path: путь к файлу с данными
    """
    with open(data_path, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


"""

nasa_id = "PIA12890"    # из предыдущего запроса
url = f"https://images-api.nasa.gov/asset/{nasa_id}"
response = requests.get(url)

if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))                    # смотрим что получили
    save_json(response.json(), 'api_nasa_response.json')   # можно сохранить
    print(response.json()["collection"]["items"][0]['href'])        # ссылка на фотку
else:
    print("Ошибка:", response.json())

url = response.json()["collection"]["items"][3]['href']
response = requests.get(url)
save_json(response.json(), 'api_nasa_meta.json')            # сохраним и посмотрим метаданные

"""