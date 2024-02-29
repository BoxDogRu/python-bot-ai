import telebot
import requests
import logging
from transformers import AutoTokenizer
from config import URL, TOKEN_BOT

# pyTelegramBotAPI==4.16.1
# requests==2.31.0
# transformers==4.37.2

bot = telebot.TeleBot(TOKEN_BOT)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)

HEADERS = {"Content-Type": "application/json"}
max_tokens = 30

chat_history = {}


def make_prompt(user_request, previous_response=""):
    json = {
        "messages": [
            {
                "role": "user",
                "content": user_request
            },
            {
                "role": "assistant",
                "content": previous_response
            },
        ],
        "temperature": 1.2,
        "max_tokens": max_tokens,
    }
    return json


# Прошлый промт

# json = {
#        "messages": [
#            {
#                "role": "user",
#                "content": user_request
#            },
#            {
#                "role": "system",
#                "content": "Давай ответы на русском языке."
#            },
#        ],
#        "temperature": 0.5,
#        "max_tokens": 50,
#    }


def count_tokens(text):
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    return len(tokenizer.encode(text))


@bot.message_handler(commands=['debug'])
def send_logs(message):
    logging.info("Отправка Логов")
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    logging.info("Отправка приветственного сообщения")
    bot.reply_to(
        message,
        "Hi! I am a bot assistant who came from the UK, so I can only speak English. I apologize immediately for the inconvenience.")

@bot.message_handler(commands=["help"])
def send_welcome(message):
    logging.info("Отправка краткой информации")
    bot.reply_to(
        message,
        "Brief information on how to use the bot:\n1. To ask a question, just write it in the chat.\n2. The bot is not very strong, so do not download it too much.\n3. Since he came from the UK, he speaks only English well.")


@bot.message_handler(content_types=["text"])
def send_request(message):
    user_request = message.text
    previous_response = ""

    if user_request == "/continue":
        chat_id = message.chat.id
        if chat_id in chat_history:
            user_request = chat_history[chat_id]['user']
            previous_response = chat_history[chat_id]['assistant']
        else:
            bot.send_message(chat_id, "There is no history of correspondence that could be continued.")
            return

    if count_tokens(user_request) > max_tokens:
        logging.error('Задача слишком длинная: %s', user_request)
        bot.send_message(message.chat.id, "The task is too long.")
        return

    resp = requests.post(url=URL, headers=HEADERS, json=make_prompt(user_request, previous_response))

    if resp.status_code == 200 and 'choices' in resp.json():
        result = resp.json()['choices'][0]['message']['content']
        logging.info('Отправлено сообщение пользователю: %s', result)
        bot.send_message(message.chat.id, result)
        chat_id = message.chat.id
        chat_history[chat_id] = {'user': user_request, 'assistant': result}
    else:
        logging.error("Не удалось получить ответ от нейросети. Текст ошибки: %s", resp.json())
        bot.send_message(message.chat.id, "Couldn't get a response from GPT")
        bot.send_message(message.chat.id, 'Error text:', resp.json())


bot.polling()
