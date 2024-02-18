import requests
from transformers import AutoTokenizer
from pprint import pprint


URL = 'http://localhost:1234/v1/chat/completions'
HEADERS = {"Content-Type": "application/json"}

MAX_TOKENS = 35


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
        "max_tokens": 15,
    }
    return json


def send_request():
    """Отправка и обработка запроса к GPT"""

    # Получение запроса от пользователя
    user_request = input("Введите запрос к GPT: ")

    # TODO Задание 1. Формирование промта и отправка запроса
    resp = requests.post(url=URL, headers=HEADERS, json=make_promt(user_request))

    # TODO Задание 2. Печать результата
    result = resp.json()['choices'][0]['message']['content']
    print(result)


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
