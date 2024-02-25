import json

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from config import TOKEN, MAX_TOKENS
from gpt import GPT

gpt = GPT()

bot = TeleBot(TOKEN)
MAX_LETTERS = MAX_TOKENS

'''
Добро пожаловать в "TeamWork" 
Выполняй небольшие задачи ниже и получай баллы!
Максимальное количество баллов: 18

P.S. Некоторые задачи связаны, и их можно выполнить только при выполнении предыдущей
'''


def save_to_json():
    with open('users_history.json', 'w', encoding='utf-8') as f:
        json.dump(users_history, f, indent=2, ensure_ascii=False)


def load_from_json():
    # noinspection PyBroadException
    try:
        with open('users_history.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {}

    return data


users_history = load_from_json()
# Словарик для хранения задач пользователей и ответов GPT


# Функция для создания клавиатуры с нужными кнопочками
def create_keyboard(buttons_list):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard


# Приветственное сообщение /start
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     text=f"Привет, {user_name}! Я бот-помощник для решения разных задач!\n"
                          f"Ты можешь прислать условие задачи, а я постараюсь её решить.\n"
                          "Иногда ответы получаются слишком длинными - в этом случае ты можешь попросить продолжить.",
                     reply_markup=create_keyboard(["/solve_task", '/help']))


# Команда /help
@bot.message_handler(commands=['help'])
def support(message):
    bot.send_message(message.from_user.id,
                     text="Чтобы приступить к решению задачи: нажми /solve_task, а затем напиши условие задачи",
                     reply_markup=create_keyboard(["/solve_task"]))


# Команда /solve_task и регистрация функции get_promt() для обработки любого следующего сообщения от пользователя
'''
Допиши функцию, для обработки команды /solve_task и для принятия ЛЮБОГО следующего сообщения пользователя, как условие задачи
Другими словами, после команды /solve_task, следующее сообщение от пользователя должно обрабатываться функцией get_promt()

За выполнение: 3 балла
'''


@bot.message_handler(commands=['solve_task'])
def solve_task(message):
    bot.send_message(message.chat.id, "Напиши условие новой задачи:")
    bot.register_next_step_handler(message, get_promt)


# Фильтр для обработки кнопочки "Продолжить решение"
def continue_filter(message):
    button_text = 'Продолжить решение'
    return message.text == button_text


# Получение задачи от пользователя или продолжение решения
@bot.message_handler(func=continue_filter)
def get_promt(message):
    user_id = str(message.from_user.id)  # ВАЖНО!

    '''
    Напиши проверку на тип сообщения (текст, картинка, видео и тд). Если это НЕ текст - сообщи об ошибке пользователю,
    и сделай так, чтобы следующее сообщение пользователя попало в эту же функцию - get_promt()

    За выполнение: 2 балла 
    '''
    if not message.text:
        bot.send_message(user_id, "Необходимо отправить именно текстовое сообщение")
        bot.register_next_step_handler(message, get_promt)
        return

    # Получаем текст сообщения от пользователя
    user_request = message.text

    '''
    Напиши проверку задачи пользователя на количество токенов. Сейчас, вместо токенов, проверяй на количество символов.
    Например: максимально 150 символов. Если количество символов больше - сообщи об ошибке пользователю, 
    и сделай так, чтобы следующее сообщение пользователя попало в эту же функцию - get_promt()

    За выполнение: 2 балла
    '''
    # if len(user_request) >= MAX_TOKENS:
    #     bot.send_message(user_id, "Запрос превышает количество символов\nИсправь запрос")
    #     bot.register_next_step_handler(message, get_promt)
    #     return

    if gpt.count_tokens(user_request) >= gpt.MAX_TOKENS:
        bot.send_message(user_id, "Запрос превышает количество символов\nИсправь запрос")
        bot.register_next_step_handler(message, get_promt)
        return

    '''
    Сделай проверку: если у пользователя нет начатой задачи, тогда ее нужно начать

    За выполнение: 3 балла
    '''
    if user_id not in users_history or users_history[user_id] == {}:
        if user_request == "Продолжить решение":
            bot.send_message(message.chat.id, "Кажется, вы еще не задали вопрос.")
            bot.register_next_step_handler(message, get_promt)
            return
        # Сохраняем промт пользователя и начало ответа GPT в словарик users_history
        users_history[user_id] = {
            'system_content': ("Ты бот, разрабатывающий персонажей игр и возвращающий ответ в виде класса python."
                               "У тебя обязательно должна быть функция def __init__."
                               "Придумай 2 метода использования уникальных качеств персонажа."),
            'user_content': user_request,
            'assistant_content': "Пишем класс на python: "
        }
        save_to_json()

    # Пока что ответом от GPT будет любой текст, просто придумай его)
    # answer = "Позже здесь будет реальное решение, а пока что так :)"
    prompt = gpt.make_promt(users_history[user_id])
    resp = gpt.send_request(prompt)
    answer = resp.json()['choices'][0]['message']['content']
    '''
    Напиши код, который будет дописывать этот ответ от GPT к предыдущему ответу GPT
    (ответ от GPT - сообщение, которое ты придумал_а выше)

    За выполнение: 2 балла
    '''
    # users_history...
    users_history[user_id]["assistant_content"] += answer
    save_to_json()
    '''
    Отправь полный ответ пользователю
    И добавь кнопочки "продолжить решение" и "завершить решение".
        Продолжить решение - пользователь просит GPT дописать ответ к текущей задаче
        Завершить решение - решение задачи прекращается, все предыдущие сообщения удаляются из истории пользователя

    За выполнение: 2 балла
    '''
    keyboard = create_keyboard(["Продолжить решение", "Завершить решение"])
    bot.send_message(message.chat.id, answer, reply_markup=keyboard)


'''
Напиши фильтр для обработки кнопочки "Завершить решение"

За выполнение: 1 балл
'''


# РЕШЕНИЕ

@bot.message_handler(commands=['end'])
@bot.message_handler(content_types=['text'], func=lambda message: message.text.lower() == "завершить решение")
def end_task(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Текущие решение завершено")
    users_history[user_id] = {}
    solve_task(message)


'''
Добавь в функции get_promt и end_task проверку состояния пользователя.
Например, если пользователь не начал диалог, но хочет продолжить ответ - 
бот отправит сообщение об ошибке и предложит сначала начать задачу

За выполнение: 3 балла
'''

bot.polling()
