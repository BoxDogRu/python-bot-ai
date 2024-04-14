import os
from dotenv import load_dotenv
import logging
import requests
from auth_gpt.authorization import get_valid_token

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H",
    filename="log_file.txt",
    filemode="w",
    force=True
)

load_dotenv()


def get_voice_headers():
    iam_token = get_valid_token()
    return {
        'Authorization': f'Bearer {iam_token}',
    }



def speech_to_text(audio_data):
    GPT_FOLDER_ID = os.getenv('GPT_FOLDER_ID')
    params = "&".join([
        "topic=general",  # используем основную версию модели
        f"folderId={GPT_FOLDER_ID}",
        "lang=ru-RU"  # распознаём голосовое сообщение на русском языке
    ])
    response = requests.post(
        f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}",
        headers=get_voice_headers(),
        data=audio_data
    )

    # Читаем json в словарь
    decoded_data = response.json()
    # Проверяем, не произошла ли ошибка при запросе
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")  # Возвращаем статус и текст из аудио
    else:
        return False, "При запросе в SpeechKit возникла ошибка"


def text_to_speech(text: str):
    GPT_FOLDER_ID = os.getenv('GPT_FOLDER_ID')
    data = {
        'text': text,  # текст, который нужно преобразовать в голосовое сообщение
        'lang': 'ru-RU',  # язык текста - русский
        'voice': 'filipp',  # голос Филиппа
        'folderId': GPT_FOLDER_ID,
    }
    # Выполняем запрос
    response = requests.post(
        'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize',
        headers=get_voice_headers(),
        data=data)

    if response.status_code == 200:
        return True, response.content  # Возвращаем голосовое сообщение
    else:
        return False, f"При запросе в SpeechKit возникла ошибка. Код ошибки: {response.status_code}"
