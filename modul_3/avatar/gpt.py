import os
from dotenv import load_dotenv
import logging
import requests
from auth_gpt.authorization import get_valid_token

from models import User, GPTModel, GPTMethod, GPTModelSET, GPTRequest

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H",
    filename="log_file.txt",
    filemode="w",
    force=True
)

load_dotenv()

#################
# DEFAULT_CONFIG

DEFAULT_MODEL = 'yandexgpt-lite'
DEFAULT_METHOD = 'text_generating'

#################


def get_modelUri(model_id):
    GPT_FOLDER_ID = os.getenv('GPT_FOLDER_ID')
    if model_id != 'edu_test':
        return f'gpt://{GPT_FOLDER_ID}/{model_id}/latest'
    else:
        return f'ds://{model_id}'



def get_headers():
    iam_token = get_valid_token()
    return {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }


def ask_gpt(message):
    user_id = message.from_user.id
    user = User.get_or_none(telegram_id=user_id)
    if user is None:
        return 'Ошибка. Нажмите /start для сброса настроек бота.'

    gpt_model = GPTModel.get(model_id=DEFAULT_MODEL)
    gpt_method = GPTMethod.get(method=DEFAULT_METHOD)
    modelUri = get_modelUri(DEFAULT_MODEL)

    data = {
          "modelUri": modelUri,
          "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": 2000
          },
          "messages": [
            {
              "role": "system",
              "text": "Отвечай пользователю кратко."
            }
          ]
    }

    data["messages"].append({
        "role": "user",
        "text": message.text
    })

    # токенизация произвольного текста
    post_template_tokenize = {
        "modelUri": modelUri,
        "text": "text_input"
    }

    try:
        print('url', modelUri)
        print('data', data)

        response = requests.post(gpt_method.url,
                           headers=get_headers(),
                           json=data)

        # print('response.status_code', response.status_code)
        if 200 <= response.status_code < 400:
            result = response.json()['result']['alternatives'][0]['message']['text']
            # tokens_in_assistant_content = count_tokens([{"role": "assistant", "text": result}])
            # tokens_in_assistant_content += tokens_in_user_content

            # add_prompt_to_database(user_id, "assistant", assistant_content + result,
            #                       tokens_in_assistant_content, session_id)
            print('result', result)
            return result

        logging.error(f"Код ошибки: {response.status_code}, Ошибка {response.json()['error']}")
        return f"Ошибка ответа. Код ошибки: {response.status_code}, ошибка {response.json()['error']}"

    except Exception as e:
        logging.error(f"Произошла непредвиденная ошибка: {e}")
        return "Ошибка ответа. Произошла непредвиденная ошибка. Приходите позже."
