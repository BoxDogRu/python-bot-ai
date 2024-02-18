import requests
from transformers import AutoTokenizer
from pprint import pprint


URL = 'http://localhost:1234/v1/chat/completions'
HEADERS = {"Content-Type": "application/json"}

MAX_TOKENS = 35


def count_tokens(text):
    """Подсчитываем количество токенов в промте"""
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")  # название модели
    return len(tokenizer.encode(text))


def make_promt(user_request):
    """Формирование промта"""
    json = {
        "messages": [
            {
                "role": "user",
                "content": user_request
            },
        ],
        "temperature": 1.2,
        "max_tokens": 50,
    }
    return json


def send_request():
    """Отправка и обработка запроса к GPT"""

    # Получение запроса от пользователя
    user_request = input("Введите запрос к GPT: ")
    request_tokens = count_tokens(user_request)
    while request_tokens > MAX_TOKENS or request_tokens < 1:
        user_request = input("Запрос несоответствует кол-ву токенов\nИсправьте запрос: ")
        request_tokens = count_tokens(user_request)

    # TODO Задание 1. Формирование промта и отправка запроса
    resp = requests.post(url=URL, headers=HEADERS, json=make_promt(user_request))
    full_response = process_resp(resp)

    if not full_response:
        print("Не удалось выполнить запрос...")
        return False

    # TODO Задание 2.2. Печать результата
    print_result = full_response['choices'][0]['message']['content']
    print(print_result)


def process_resp(response):
    """Проверка ответа на возможные ошибки и его обработка"""

    # TODO Задание 2.1. Обработка ответа

    if response.status_code != 200:
        print(f'Ошибка {response.status_code}')
        return False

    # Проверка json
    try:
        full_response = response.json()
    except:
        print("Ошибка получения JSON")
        return False

    # Проверка сообщения об ошибке
    if "error" in full_response:
        print(f"Ошибка: {full_response['error']}")
        return False

    return full_response


def end():
    """Выход =)"""
    print("До новых встреч!")
    exit(0)


def start():
    menu = {
        "1": {
            "text": "Запрос к GPT",
            "func": send_request
        },
        "2": {
            "text": "Выход",
            "func": end
        }
    }

    print("Добро пожаловать в Чат-с-GPT")
    # Бесконечный цикл
    while True:
        # Вывод меню
        print("Меню:")
        for num, item in menu.items():
            print(f"{num}. {item['text']}")

        # Получение корректного выбора пользователя
        choice = input("Выберите: ")
        while choice not in menu:
            choice = input("Выберите корректный пункт: ")

        # Вызов функции из меню
        menu[choice]['func']()


if __name__ == "__main__":
    start()