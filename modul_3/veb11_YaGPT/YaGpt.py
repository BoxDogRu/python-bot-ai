import requests
import logging
from config_credentials import TOKEN, FOLDER_ID
from config_model import GPT_MODEL, MAX_MODEL_TOKENS, MODEL_TEMPERATURE
from config_model import system_role_default
# from transformers import AutoTokenizer

# Дока по АПИ: https://cloud.yandex.ru/ru/docs/yandexgpt/operations/create-prompt#service-account_1
    # Про токены https://cloud.yandex.ru/ru/docs/yandexgpt/text-generation/api-ref/Tokenizer/tokenize

# Получение IAM-токена
# Шаг 1. Заходим на сервер используя команду (указать свой IP и место расположения ключа)
# ssh -i ~/Папкахранениятокена/Еще_Папка/Название_файла_вида_034823ef9be48155549e student@айпиадер_вида_158.160.159.92
# Шаг 2. Получение IAM-токена
# curl -sf -H Metadata-Flavor:Google 169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(message)s")

"""
def count_tokens(prompt):
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")  # название модели
    return len(tokenizer.encode(prompt))
"""


def count_tokens(promt) -> int:
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    result = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",
        headers = headers,
        json = {
            "modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
            "text": promt
        }
    ).json()['tokens']
    return len(result)


def ask_gpt(user_text):
    """Запрос к Yandex GPT"""

    url = f"https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
        "modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
        "completionOptions": {
            "stream": False,
            "temperature": MODEL_TEMPERATURE,
            "maxTokens": MAX_MODEL_TOKENS
        },
        "messages": [
            {"role": "system", "text": system_role_default},
            {"role": "user", "text": user_text},
            # Можно продолжить диалог
            # {"role": "assistant", "text": ""}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            logging.debug(f"Response {response.json()} Status code:{response.status_code} Message {response.text}")
            result = f"Status code {response.status_code}. Подробности см. в журнале."
            return result
        result = response.json()['result']['alternatives'][0]['message']['text']
        logging.info(f"Request: {response.request.url}\n"
                     f"Response: {response.status_code}\n"
                     f"Response Body: {response.text}\n"
                     f"Processed Result: {result}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        result = "Произошла непредвиденная ошибка. Подробности см. в журнале."

    return result


if __name__ == '__main__':
    result = ask_gpt('Придумай сценарий эльфийской истории')
    print(result)

    text_for_tokens = 'Это пробный текст. Хочу, чтобы мне вернулось количество токенов из которых он состоит'
    print(f'Количество токенов в тексте - {count_tokens(text_for_tokens)}')