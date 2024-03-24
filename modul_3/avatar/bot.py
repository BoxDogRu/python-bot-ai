import os
from dotenv import load_dotenv

import telebot
import logging

from models import User
from keyboards import keyboard_menu, keyboard_menu_admin

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


if __name__ == "__main__":
    logging.info("Бот запущен")
    bot.infinity_polling()
