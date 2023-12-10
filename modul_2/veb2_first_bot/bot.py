import telebot
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('TOKEN')

bot = telebot.TeleBot(token)


def filter_hello(message):
    # проверка на одно слово
    # keyword = 'привет'
    # return keyword in message.text.lower()

    # посмотреть дополнительную информацию по объекту
    # print(type(message.from_user))
    # print(dir(message.from_user))

    keywords = ['привет', 'hello', 'здарово']
    text_msg = message.text.lower()
    for i in keywords:
        if i in text_msg:
            return True


@bot.message_handler(content_types=['text'], func=filter_hello)
def echo_message(message):
    bot.send_message(message.chat.id, 'И тебе привет')


@bot.message_handler(content_types=['text'])
def say_hello(message):
    bot.send_message(message.chat.id, message.text)

"""
# ответы на любые сообщения
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)
"""

bot.polling()
