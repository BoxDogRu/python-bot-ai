# Считаем токены
import requests
import logging

from config_credentials import TOKEN, FOLDER_ID

# config model
GPT_MODEL = 'yandexgpt-lite'
MAX_TOKENS_IN_SESSION = 80
MAX_SESSIONS = 2

MAX_MODEL_TOKENS = 800
MODEL_TEMPERATURE = 0.6


# Подсчитывает количество токенов в сессии
# Документация https://cloud.yandex.ru/ru/docs/yandexgpt/text-generation/api-ref/Tokenizer/tokenizeCompletion
def count_tokens_in_dialogue(messages: list) -> int:
    """Считаем токены в Yandex GPT"""

    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion'
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
       "modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
       "maxTokens": MAX_MODEL_TOKENS,
       "messages": []
    }

    for row in messages:
        data["messages"].append(
            {
                "role": row["role"],
                "text": row["text"]
            }
        )

    return len(
        requests.post(
            url,
            json=data,
            headers=headers
        ).json()["tokens"]
    )


# Документация https://cloud.yandex.ru/ru/docs/yandexgpt/operations/create-chat
def ask_gpt(collection):
    """Запрос к Yandex GPT"""
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
        "modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
        "completionOptions": {
            "stream": False,
            "temperature": MODEL_TEMPERATURE,
            "maxTokens": MAX_TOKENS_IN_SESSION
        },
        "messages": []
    }

    for row in collection:
        data["messages"].append(
            {
                "role": row["role"],
                "text": row["text"]
            }
        )

    try:
        response = requests.post(
            url,
            json=data,
            headers=headers
        )
        if response.status_code != 200:
            logging.debug(f"Response {response.json()} Status code:{response.status_code} Message {response.text}")
            result = f'Произошла ошибка. Статус код {response.status_code}. Подробности в журнале'
            return result
        result = response.json()["result"]["alternatives"][0]["message"]["text"]
    except Exception as e:
        logging.error(f'Ошибка {e}')
        result = 'Произошла непридвиденная ошибка'

    return result


if __name__ == '__main__':
    session = 0
    dialogue = [{'role': 'system', 'text': 'Ты помощник для решения задач по математике'}]

    while session < MAX_SESSIONS:
        user_text = input('Введи запрос к нейросети')
        dialogue.append({'role': 'system', 'text': user_text})

        tokens = count_tokens_in_dialogue(dialogue)

        if tokens > MAX_TOKENS_IN_SESSION:
            print('Превышен лимит токенов в сессии')
            break
        else:
            print('Все ок')

        result = ask_gpt(dialogue)
        print(result)

        dialogue.append({'role': 'assistant', 'text': result})
        session += 1

    print('Вы превысили лимит сессий')
