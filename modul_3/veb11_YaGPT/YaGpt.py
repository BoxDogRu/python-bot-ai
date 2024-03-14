import requests
import logging
from config_credentials import TOKEN, FOLDER_ID
from config_model import GPT_MODEL, MAX_MODEL_TOKENS, MODEL_TEMPERATURE
from config_model import system_role_default

# Дока по АПИ: https://cloud.yandex.ru/ru/docs/yandexgpt/operations/create-prompt#service-account_1
# ssh -i ~/Местохранениятокена/Название_файла_вида_034823ef9be48155549e student@айпиадер_вида_158.160.159.92
# Получение IAM-токена: curl -sf -H Metadata-Flavor:Google 169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(message)s")


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

    # упражение

    return result


if __name__ == '__main__':
    result = ask_gpt('Придумай сценарий эльфийской истории')
    print(result)
