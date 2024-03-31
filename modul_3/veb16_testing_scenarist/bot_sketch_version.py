import logging
import os.path
import sqlite3
from datetime import datetime

import telebot
from telebot import types

from gpt import ask_gpt, create_prompt, count_tokens_in_dialogue
from info import HELP_COMMANDS, DEV_COMMANDS, END_STORY
from story import genres, characters, settings
from validators import is_sessions_limit, is_tokens_limit
from database import (
    prepare_db,
    get_dialogue_for_user,
    add_record_to_table,
    get_value_from_table,
    is_value_in_table,
    count_all_tokens_from_db,
    execute_selection_query,
    get_users_amount
)

LOGS_PATH = 'logs.txt'

DB_DIR = 'db'
DB_NAME = 'gpt_helper.db'
DB_TABLE_PROMPTS_NAME = 'prompts'

ADMIN_ID = ''
TOKEN = ''
MAX_USERS = 3
# Модель, которую используем
GPT_MODEL = 'yandexgpt'
# Ограничение на выход модели в токенах
MAX_MODEL_TOKENS = 1000
# Креативность GPT (от 0 до 1)
MODEL_TEMPERATURE = 0.6

# Каждому пользователю даем 3 сеанса общения, каждый сеанс это новый help_with
MAX_SESSIONS = 3
# Каждому пользователю выдаем 1500 токенов на 1 сеанс общения
MAX_TOKENS_IN_SESSION = 2500

SYSTEM_PROMPT = (
    "Ты пишешь историю вместе с человеком. "
    "Историю вы пишете по очереди. Начинает человек, а ты продолжаешь. "
    "Если это уместно, ты можешь добавлять в историю диалог между персонажами. "
    "Диалоги пиши с новой строки и отделяй тире. "
    "Не пиши никакого пояснительного текста в начале, а просто логично продолжай историю"
)


# Создаёт клавиатуру с указанными кнопками
def menu_keyboard(options: list) -> types.ReplyKeyboardMarkup:
    buttons = (types.KeyboardButton(text=option) for option in options)
    keyboard = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    keyboard.add(*buttons)
    return keyboard


logging.basicConfig(
    filename=LOGS_PATH,
    level=logging.DEBUG,
    format="%(asctime)s %(message)s", filemode="w"
)

# Создаём бота
bot = telebot.TeleBot(TOKEN)

user_data = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id

    bot.send_message(message.chat.id, f"Привет, {user_name}! Я бот, который создаёт истории с помощью нейросети.\n"
                                      f"Мы будем писать историю поочерёдно. Я начну, а ты продолжить.\n"
                                      "Напиши /new_story, чтобы начать новую историю.\n"
                                      f"А когда ты закончишь, напиши /end.",
                     reply_markup=menu_keyboard(["/new_story"]))


# Обработчик команды /begin
@bot.message_handler(commands=['begin'])
def begin_story(message):
    user_id = message.from_user.id
    # Проверяем, что пользователь прошёл регистрацию
    # Запрашиваем ответ нейросети
    get_story(message)


# Обработчик команды /new_story
@bot.message_handler(commands=['new_story'])
def registration(message):
    """Меняет статус пользователя на "в истории",
     записывает в бд и отправляет первый вопрос о жанре"""

    bot.send_message(message.chat.id, "Для начала выбери жанр своей истории:\n",
                     reply_markup=menu_keyboard(genres))
    bot.register_next_step_handler(message, handle_genre)


def handle_genre(message):
    """Записывает ответ на вопрос о жанре в бд и отправляет следующий вопрос о персонаже"""
    user_id = message.from_user.id
    # считывает ответ на предыдущий вопрос
    genre = message.text

    # отправляет следующий вопрос
    bot.send_message(message.chat.id, "Выбери главного героя:",
                     reply_markup=menu_keyboard(characters))
    bot.register_next_step_handler(message, handle_character)


def handle_character(message):
    """Записывает ответ на вопрос о персонаже в бд и отправляет следующий вопрос о сеттинге"""
    user_id = message.from_user.id
    # считывает ответ на предыдущий вопрос
    character = message.text
    # Если пользователь отвечает что-то не то, то отправляет ему вопрос ещё раз
    settings_string = "\n".join([f"{name}: {description}" for name, description in settings.items()])
    # отправляет следующий вопрос
    bot.send_message(message.chat.id, "Выбери сеттинг:\n" + settings_string,
                     reply_markup=menu_keyboard(settings.keys()))
    bot.register_next_step_handler(message, handle_setting)


def handle_setting(message):
    """Записывает ответ на вопрос о сеттинге в бд и отправляет следующий вопрос о доп. информации"""
    user_id = message.from_user.id
    # Считывает ответ на предыдущий вопрос
    user_setting = message.text
    # Отправляет следующий вопрос
    bot.send_message(message.chat.id, "Если ты хочешь, чтобы мы учли ещё какую-то информацию, "
                                      "напиши её сейчас. Или ты можешь сразу переходить "
                                      "к истории написав /begin.",
                     reply_markup=menu_keyboard(["/begin"]))

    bot.register_next_step_handler(message, handle_add_info)


def handle_add_info(message):
    """Записывает ответ на вопрос о доп. информации в бд"""
    user_id = message.from_user.id
    # Считывает ответ на предыдущий вопрос
    additional_info = message.text

    if additional_info == "/begin":
        begin_story(message)
    else:
        # Обновляет данные пользователя в бд
        user_data[user_id]['additional_info'] = additional_info
        # Отправляет следующий вопрос
        bot.send_message(message.chat.id, "Спасибо! Всё учтём :)\n"
                                          "Напиши /begin, чтобы начать писать историю.",
                         reply_markup=menu_keyboard(["/begin"]))


# Обработчик для генерирования вопроса
@bot.message_handler(content_types=['text'])
def get_story(message: types.Message):
    user_id: int = message.from_user.id

    session_id = 1
    if is_value_in_table(DB_TABLE_PROMPTS_NAME, 'user_id', user_id):
        row: sqlite3.Row = get_value_from_table('session_id', user_id)
        session_id = row['session_id'] + 1

    user_story = create_prompt(user_data, message.from_user.id)

    collection: list = get_dialogue_for_user(user_id, session_id)
    collection.append({'role': 'system', 'content': user_story})
    tokens: int = count_tokens_in_dialogue(collection)

    bot.send_message(message.chat.id, "Генерирую...")

    add_record_to_table(
        user_id,
        'system',
        user_story,
        datetime.now(),
        tokens,
        session_id
    )

    collection: list = get_dialogue_for_user(user_id, session_id)
    gpt_text, result_for_test = ask_gpt(collection)
    collection.append({'role': 'assistant', 'content': gpt_text})


    add_record_to_table(
        user_id,
        'assistant',
        gpt_text,
        datetime.now(),
        tokens,
        session_id
    )

    if gpt_text is None:
        bot.send_message(
            message.chat.id,
            "Не могу получить ответ от GPT :(",
            reply_markup=menu_keyboard(HELP_COMMANDS)
        )

    elif gpt_text == "":
        bot.send_message(
            message.chat.id,
            "Не могу сформулировать решение :(",
            reply_markup=menu_keyboard(HELP_COMMANDS)
        )
        logging.info(f"TELEGRAM BOT: Input: {message.text}\nOutput: Error: нейросеть вернула пустую строку")

    else:
        if not user_data[user_id]['test_mode']:
            msg = bot.send_message(message.chat.id, gpt_text)
        else:
            msg = bot.send_message(message.chat.id, result_for_test)
        # bot.register_next_step_handler(msg, story_handler)


# Создаём базы данных или подключаемся к существующей
prepare_db(True)
bot.infinity_polling()
