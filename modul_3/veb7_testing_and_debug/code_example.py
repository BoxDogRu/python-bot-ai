import telebot
import requests

BOT_TOKEN = '6448841386:AAGUqIwA65FK0iG4I5qQcH79Abd6uupa8m9'
bot = telebot.TeleBot(BOT_TOKEN)

# История чата для каждого пользователя
chat_history = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
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

    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'messages': chat_history[user_id],
        'temperature': 2.1,
    }
    response = requests.post('https://localhost:1234/v1', headers=headers, json=data)
    answer = response.json()['choices'][0]['message']['content']

    return answer


bot.infinity_polling()