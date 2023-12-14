import telebot
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')

bot = telebot.TeleBot(token)

def filter_hello(message):
    msg_box = ['привет', 'хай', 'дарова', 'привки', 'здарова', 'прив']
    for i in msg_box:
        if i in message.text.lower():
            return True

def filter_bye(message):
    msg_box = ['пока', 'бай бай', 'бб', 'поки', 'гуд бай', 'гуд бай', 'бай']
    for i in msg_box:
        if i in message.text.lower():
            return True


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет,Я MegaBot cделал в качестве проекта курса \"Python в ИИ от Яндекс\".\nПропиши /help, чтобы поссмотреть список команд.")
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "/info - Информации обо мне\n"
                                      "/functions - Все функции бота\n")


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, "Меня завут Данила и мне 14 лет живу я в россии. Мои увлечения: Программирование , Работа по дереву и всё. . . . .\nУчусь в 8 классе троешник (По русскому 1 тройка😢😭)\nП.С если хотите увидеть моё лицо напишите \"Лицо\"")

@bot.message_handler(commands=['functions'])
def info(message):
    bot.send_message(message.chat.id,"Бот может отвечать на слова \"Привет\" и \"Пока\". ")


@bot.message_handler(content_types=['text'], func=filter_hello)
def hello(message):
    bot.send_message(message.chat.id,f"Привет, {message.from_user.first_name}💓")

@bot.message_handler(content_types=['text'], func=filter_bye)
def good_bye(message):
    bot.send_message(message.chat.id,"Пока 😢")

@bot.message_handler(func=lambda message: message.text.lower() == 'лицо')
def send_photo(message):
    bot.send_photo(message.chat.id, 'https://i.pinimg.com/originals/2f/0c/92/2f0c92732be94b73fb41ef81f4dda9da.png')

@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.send_photo(message.chat.id, "https://avatars.mds.yandex.net/i?id=bf4cf71aeaa662f02a4afb421f7a9f2c_l-5495450-images-thumbs&n=13")

@bot.message_handler(content_types=['audio',"voice","photo"])
def good_photo(message):
    bot.send_photo(message.chat.id,"https://avatars.mds.yandex.net/i?id=bf4cf71aeaa662f02a4afb421f7a9f2c_l-5495450-images-thumbs&n=13")

bot.polling()
