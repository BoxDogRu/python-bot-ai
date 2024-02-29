import json
import logging
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from config import TOKEN, MAX_TOKENS
from gpt import GPT

gpt = GPT()

bot = TeleBot(TOKEN)
MAX_LETTERS = MAX_TOKENS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)

def save_to_json():
    with open('users_history.json', 'w', encoding='utf-8') as f:
        json.dump(users_history, f, indent=2, ensure_ascii=False)

def load_from_json():
    try:
        with open('users_history.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {}
    return data

users_history = load_from_json()

def create_keyboard(buttons_list):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    logging.info("Отправка приветственного сообщения(/start)")
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     text=f"Привет, {user_name}! Я бот-помощник для решения вопросов в подборе одежды!\n"
                          f"Ты можешь расказать мне о погодных условиях и о своём предпочтении в одежде, так же не забудь указать пол.\n"
                          "Иногда ответы получаются слишком длинными - в этом случае ты можешь попросить продолжить.",
                     reply_markup=create_keyboard(["/solve_task", '/help']))

# Команда /help
@bot.message_handler(commands=['help'])
def support(message):
    logging.info("Отправка вспомогательного сообщения(/help)")
    bot.send_message(message.from_user.id,
                     text="Чтобы приступить к общению с ботом нажми на /solve_task, ну или просто напиши в чат.\n"
                          "Затем можешь написать свой запрос.\n\n"
                          "Пример запроса: Я парень 19 лет, сейчас на улице весна, я люблю ветровки.",
                     reply_markup=create_keyboard(["/solve_task"]))

@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)

@bot.message_handler(commands=['solve_task'])
def solve_task(message):
    logging.debug("Вызвана команда solve_task, ждём запрос пользователя.")
    bot.send_message(message.chat.id, "Какая одежда тебе нужна?")
    bot.register_next_step_handler(message, get_promt)

def continue_filter(message):
    logging.info("Пользователь продолжил решение.")
    button_text = 'Продолжить решение'
    return message.text == button_text

@bot.message_handler(func=continue_filter)
def get_promt(message):
    user_id = str(message.from_user.id)  # ВАЖНО!

    if not message.text:
        logging.warning("Получено пустое текстовое сообщение")
        bot.send_message(user_id, "Необходимо отправить именно текстовое сообщение")
        bot.register_next_step_handler(message, get_promt)
        return

    user_request = message.text
    logging.debug(f"Полученный текст от пользователя: {message.text}")

    if gpt.count_tokens(user_request) >= gpt.MAX_TOKENS:
        logging.warning("Превышенно количество токенов")
        bot.send_message(user_id, "Запрос превышает количество символов\nИсправь запрос")
        bot.register_next_step_handler(message, get_promt)
        return

    if user_id not in users_history or users_history[user_id] == {}:
        if user_request == "Продолжить решение":
            logging.warning("Поользователь активировал команду 'Продолжить решение', но ещё не задал запрос.")
            bot.send_message(message.chat.id, "Кажется, вы еще не задали вопрос.")
            bot.register_next_step_handler(message, get_promt)
            return

        users_history[user_id] = {
            'system_content': ("Ты бот, который подбираешь одежду по погодным условиям и предпочтениям во вкусе пользователей."
                               "Опирайся на пол который указал пользователь, если он не был указан придумай универсальный образ."),
            'user_content': user_request,
            'assistant_content': "Пишем название одежды на русском: "
        }
        save_to_json()

    bot.send_message(message.chat.id, "Запрос в обработке.")
    logging.info("Запрос в обработке.")
    prompt = gpt.make_promt(users_history[user_id])
    resp = gpt.send_request(prompt)
    answer = resp.json()['choices'][0]['message']['content']
    users_history[user_id]["assistant_content"] += answer
    save_to_json()
    keyboard = create_keyboard(["Продолжить решение", "Завершить решение"])
    logging.info("Ответ пользователю успешно отправлен")
    bot.send_message(message.chat.id, answer, reply_markup=keyboard)

@bot.message_handler(content_types=['text'], func=lambda message: message.text.lower() == "завершить решение")
def end_task(message):
    user_id = message.from_user.id
    logging.debug("Текущий диалог закончен, ждём новый запрос пользователя.")
    bot.send_message(user_id, "Текущий диалог звершён")
    users_history[user_id] = {}
    solve_task(message)

logging.info("Бот запущен")
bot.polling()