import os
from dotenv import load_dotenv

import telebot
import logging

from yandex_gpt import ask_gpt
from yandex_speechkit import text_to_speech, speech_to_text
from models import User
from keyboards import keyboard_menu, keyboard_menu_admin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H",
    filename="log_file.txt",
    filemode="w",
    force=True
)

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_ADMIN = int(os.getenv('TG_ADMIN'))

bot = telebot.TeleBot(token=TG_TOKEN)


def extract_unique_code(text):
    """Фиксируем промо ссылки"""
    # Extracts the unique_code from the sent /start command.
    # https://t.me/my_experimental_bot?start=promo
    return text.split()[1] if len(text.split()) > 1 else None


@bot.message_handler(commands=["start"])
def start_bot(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Persistent data from message
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    language_code = message.from_user.language_code
    unique_code = extract_unique_code(message.text)
    deep_link = unique_code if unique_code else ''
    is_admin = True if user_id == TG_ADMIN else False

    user = User.get_or_none(telegram_id=user_id)

    if user is None:
        user = User(telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=first_name,
                    last_name=last_name,
                    language_code=language_code,
                    deep_link=deep_link,
                    is_admin=is_admin)
        user.save()
    bot.set_my_commands(keyboard_menu_admin) if user.is_admin else bot.set_my_commands(keyboard_menu)
    bot.send_message(chat_id, "Welcome, " + message.from_user.first_name)


@bot.message_handler(commands=['stt'])
def stt_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь голосовое сообщение, чтобы я его распознал!')
    bot.register_next_step_handler(message, stt)


def stt(message):
    user_id = message.from_user.id

    # Проверка, что сообщение действительно голосовое
    if not message.voice:
        return

    file_id = message.voice.file_id  # получаем id голосового сообщения
    file_info = bot.get_file(file_id)  # получаем информацию о голосовом сообщении
    file = bot.download_file(file_info.file_path)  # скачиваем голосовое сообщение

    # with open('output.ogg', "rb") as audio_file:
    #    audio_data = audio_file.read()
    success, result = speech_to_text(file)    # audio_data
    if success:
        print("Распознанный текст: ", result)
        bot.send_message(message.chat.id,
                         result,
                         parse_mode="html")
    else:
        print("Ошибка при распознавании речи: ", result)


@bot.message_handler(content_types=["text"])
def make_genre(message):
    """Test GPT"""
    gpt_answer = ask_gpt(message)
    logging.info(f"Ответ GPT: {gpt_answer}")
    bot.send_message(message.chat.id,
                     gpt_answer,
                     parse_mode="html")

    """
    # тест функции
    success, response = text_to_speech(gpt_answer)
    if success:
        # Если все хорошо, сохраняем аудио в файл
        with open("output.ogg", "wb") as audio_file:
            audio_file.write(response)
        print("Аудиофайл успешно сохранен как output.ogg")
        bot.send_voice(message.chat.id, open('output.ogg', 'rb'))
    else:
        # Если возникла ошибка, выводим сообщение об ошибке
        print("Ошибка:", response)
    """


if __name__ == "__main__":
    logging.info("Бот запущен")
    bot.infinity_polling()
