import telebot
import os
from dotenv import load_dotenv
import random

load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def starting(message):
    bot.send_message(message.chat.id, 'Привет, дружище, мы команда юных зоологов, покажем вам фауну львов и тигров.\n'
                                      'Для начала напиши команду /help')
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/lion - покажу льва\n'
                                      '/tiger - покажу тигра')

@bot.message_handler(commands=['lion'])
def lion(message):
    bot.send_photo(message.chat.id, photo=open(f'cats/L({random.randint(1, 4)}).jpg', 'rb'))

@bot.message_handler(commands=['tiger'])
def tiger(message):
    bot.send_photo(message.chat.id, photo=open(f'cats/T({random.randint(1, 7)}).jpg', 'rb'))

def hello(message):
    msg_box = ['привет', 'хай', 'дарова', 'привки', 'здарова', 'прив']
    for i in msg_box:
        if i in message.text.lower():
            return True

def bb(message):
    msg_box = ['пока', 'бай бай', 'бб', 'поки', 'гуд бай', 'гуд бай', 'бай']
    for i in msg_box:
        if i in message.text.lower():
            return True

@bot.message_handler(content_types=['text'], func=hello)
def hi(message):
    bot.reply_to(message, f'И тебе привет, {message.from_user.first_name}')

@bot.message_handler(content_types=['text'], func=bb)
def bb(message):
    bot.reply_to(message, f'Поки, {message.from_user.first_name}')

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

bot.polling()
