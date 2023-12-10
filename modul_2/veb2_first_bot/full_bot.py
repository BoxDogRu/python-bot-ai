import telebot

token = 'наш_токен'
bot = telebot.TeleBot(token)


def filter_hello(message):
    password = "привет"
    return password in message.text.lower()


def filter_bye(message):
    password = "пока"
    return password in message.text.lower()


@bot.message_handler(content_types=['text'], func=filter_hello)
def say_hello(message):
    bot.send_message(message.chat.id, f"И тебе привет, {message.from_user.first_name}!")


@bot.message_handler(content_types=['text'], func=filter_bye)
def say_hello(message):
    bot.send_message(message.chat.id, f"Пока-пока, {message.from_user.first_name}!")


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, "Я, маленький вежливый бот, готов к работе!")


@bot.message_handler(commands=['help'])
def say_start(message):
    bot.send_message(message.chat.id, 'Вот список того, что я умею:\n'
                                      '- По команде /start сообщаю о готовности к общению\n'
                                      '- По команде /help показываю эту справку о себе\n'
                                      '- Отвечаю приветствием на сообщение со словом "привет"\n'
                                      '- Прощаюсь, если пришло сообщение со словом "пока"\n'
                                      '- Все другие сообщения просто повторяю')


@bot.message_handler(content_types=['text'])
def repeat_message(message):
    bot.send_message(message.chat.id, f'Вы прислали сообщение "{message.text}"')


bot.polling()
