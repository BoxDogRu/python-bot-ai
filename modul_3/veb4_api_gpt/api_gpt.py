import requests
from transformers import AutoTokenizer
from pprint import pprint


URL = 'http://localhost:1234/v1/chat/completions'
HEADERS = {"Content-Type": "application/json"}

MAX_TOKENS = 35


# Формирование промта
def make_promt(user_request):
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


# Проверка ответа на возможные ошибки и его обработка
def process_resp(response):
    ...
    full_response = response
    ...
    return full_response


# Отправка и обработка запроса к GPT
def send_request():
    # Получение запроса от пользователя
    user_request = input("Введите запрос к GPT: ")
    ...


# Выход =)
def end():
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