import telebot
import requests
import logging
from config import BOT_TOKEN

URL_GPT = 'http://localhost:1234/v1/chat/completions'
HEADERS = {'Content-Type': 'application/json'}
MAX_TOKENS = 50
TEMPERATURE = 0.5

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(BOT_TOKEN)

# История чата для каждого пользователя
chat_history = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    logging.info(f"User {message.from_user.id} started the bot")
    bot.reply_to(message,
                 "Привет! Я бот, который использует GPT для ответов на ваши вопросы. Просто напиши мне что-нибудь.")


@bot.message_handler(commands=['history'])
def send_history(message):
    user_id = message.from_user.id
    history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history[user_id]])
    bot.reply_to(message, f"Ваша история сообщений:\n{history}")


@bot.message_handler()
def handle_message(message):
    user_id = message.from_user.id
    chat_history[user_id] = []

    # Добавляем сообщение пользователя в историю чата
    chat_history[user_id].append({"role": "user", "content": message.text})

    response = ask_gpt(user_id)

    # Добавляем ответ бота в историю чата
    chat_history[user_id].append({"role": "assistant", "сontent": response})

    bot.reply_to(message, response)


def ask_gpt(user_id):
    if user_id not in chat_history:
        return "Привет! Чем могу помочь?"

    data = {
        'messages': chat_history[user_id],
        'temperature': TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }

    # упрощенный вариант
    try:
        response = requests.post(URL_GPT, headers=HEADERS, json=data)
        # logging.info(f"Смотрим словарь-ответ: {response.json()}")
        answer = response.json()['choices'][0]['message']['content']
    except:
        return 'Ошибка!'

    # вариант с детализацией
    if 'choices' in response.json():
        answer = response.json()['choices'][0]['message']['content']
    else:
        return 'Ошибка получения ответа'

    return answer


bot.infinity_polling()