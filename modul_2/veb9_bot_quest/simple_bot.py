from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton # импорт нужных классов

bot = TeleBot('токен')

# Вставить пути к своим файлам
content = {
    'Текст': "Привет",
    "Картинка": "",
    "Аудио": "",
    "Файл": ""
}

def makeKeyboard(items):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in items:
        markup.add(KeyboardButton(item))
    return markup


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = makeKeyboard(list(content.keys()))
    bot.send_message(message.chat.id, 'Выберите, что вам прислать:', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_start(message):
    markup = makeKeyboard(list(content.keys()))

    if message.text == "Текст":
        bot.send_message(message.chat.id, content['Текст'], reply_markup=markup)

    elif message.text == "Картинка":
        with open(content["Картинка"], 'rb') as f:
            bot.send_photo(message.chat.id, f, reply_markup=markup)

    elif message.text == "Аудио":
        with open(content["Аудио"], 'rb') as f:
            bot.send_audio(message.chat.id, f, reply_markup=markup)

    elif message.text == "Файл":
        with open(content["Файл"], 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=markup)

    else:
        bot.send_message(message.chat.id, "Выберите один из предложенных вариантов", reply_markup=markup)


bot.polling()
