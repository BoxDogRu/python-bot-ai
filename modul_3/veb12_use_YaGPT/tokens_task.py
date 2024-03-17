# Считаем токены

import requests

from config_credentials import TOKEN, FOLDER_ID

# config model
GPT_MODEL = 'yandexgpt-lite'
MAX_TOKENS_IN_SESSION = 80
MAX_SESSIONS = 2
MAX_MODEL_TOKENS = 800


# Подсчитывает количество токенов в сессии
# Документация https://cloud.yandex.ru/ru/docs/yandexgpt/text-generation/api-ref/Tokenizer/tokenizeCompletion
def count_tokens_in_dialogue(messages: list) -> int:

    # TODO
    url = ''
    headers = {
        'Authorization': '',
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
                "text": row["content"]
            }
        )

    return len(
        requests.post(
            url,
            json='',
            headers=''
        ).json()["tokens"]
    )


# Документация https://cloud.yandex.ru/ru/docs/yandexgpt/operations/create-chat
def ask_gpt(collection):
    """Запрос к Yandex GPT"""
    pass


session = 0
dialogue = [{'role': 'system', 'text': 'Ты помощник для решения задач по математике'}]

while session < MAX_SESSIONS:
    user_text = input('Введи запрос к нейросети')
    dialogue.append()

    tokens = count_tokens_in_dialogue(dialogue)

    if tokens > MAX_TOKENS_IN_SESSION:
        print('')
        break
    else:
        print('')

    result = ask_gpt(dialogue)

    dialogue.append()
    session += 1

print('Вы превысили лимит сессий')



