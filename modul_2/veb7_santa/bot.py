import telebot
from data import load_user_data, save_user_data
from secret_santa import welcome_message, shuffle_users

from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

# todo: вставить свой токен
# TOKEN = "YOUR TOKEN HERE"
# bot = telebot.TeleBot(TOKEN)

# todo: указать количество участников
users_total = 2
users_sent_gift = 0

data_path = "users.json"
user_data = load_user_data(data_path)

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    global user_data
    # Считываем данные из файла, если
    # Инициализируем данные пользователя
    user_data[message.chat.id] = {"name": message.from_user.first_name,
                                  "send_to": None, "gift_path": "", "gift_type": ""}
    # Сохраняем данные пользователя
    save_user_data(user_data, data_path)

    # Отправляем приветственное сообщение
    bot.send_message(message.chat.id, welcome_message)
    # Если все участники зарегистрированы, то отправляем сообщение с информацией о том, кому кто дарит подарок
    if len(user_data) == users_total:
        # Перемешиваем пользователей
        user_data = shuffle_users(user_data)
        # Сохраняем данные пользователя
        save_user_data(user_data, data_path)
        # Отправляем сообщение с информацией о том, кому кто дарит подарок
        send_info(user_data)
    else:
        bot.send_message(message.chat.id, "Пока не все участники зарегистрированы, придётся немного подождать")


def send_info(user_data):
    # todo: текст сообщения можно поменять
    for user_id, user in user_data.items():
        bot.send_message(user_id, f"Итак, {user['name']}, "
                                  f"У меня для тебя хорошие новости!")
        bot.send_message(user_id, f"Все участники зарегистрированы, начинаем розыгрыш!")
        bot.send_message(user_id, f"Твой счастливчик - {user_data[user['send_to']]['name']}"
                                  f"Отпрваь открытку для своего подопечного ответным сообщением")


# Команда для отправки медиа-файлов
@bot.message_handler(content_types=['photo', 'video', 'audio'])
def handle_media_files(message):
    global user_data, users_sent_gift
    chat_id = message.chat.id
    if chat_id in user_data:
        file_id = message.document.file_id if message.document else message.photo[-1].file_id
        user_data[chat_id]['gift_path'] = file_id
        user_data[chat_id]['gift_type'] = message.content_type
        save_user_data(user_data, data_path)
        bot.send_message(chat_id, "Медиа-файл принят!")
        users_sent_gift += 1
        if users_sent_gift == users_total:
            send_media_files(user_data)


def send_media_files(user_data):
    for user_id, user in user_data.items():
        recipient_id = user['send_to']
        file_id = user['gift_path']
        file_type = user['gift_type']
        # todo: текст сообщения можно поменять
        bot.send_message(recipient_id, f"Привет, {user_data[recipient_id]['name']}!\n"
                                       f"Тебе тут открытка от твоего секретного санты!")
        if file_type == 'photo':
            bot.send_photo(recipient_id, file_id)
        elif file_type == 'video':
            bot.send_video(recipient_id, file_id)
        elif file_type == 'audio':
            bot.send_audio(recipient_id, file_id)



# Запуск бота
bot.infinity_polling()
