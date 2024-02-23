from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from config import TOKEN, MAX_TOKENS

bot = TeleBot(TOKEN)
MAX_LETTERS = MAX_TOKENS


'''
Добро пожаловать в "TeamWork" 
Выполняй небольшие задачи ниже и получай баллы!
Максимальное количество баллов: 18

P.S. Некоторые задачи связаны, и их можно выполнить только при выполнении предыдущей
'''


# Словарик для хранения задач пользователей и ответов GPT
users_history = {}


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
    ...


# Фильтр для обработки кнопочки "Продолжить решение"
def continue_filter(message):
    button_text = 'Продолжить решение'
    return message.text == button_text


# Получение задачи от пользователя или продолжение решения
@bot.message_handler(func=continue_filter)
def get_promt(message):
    user_id = message.from_user.id

    '''
    Напиши проверку на тип сообщения (текст, картинка, видео и тд). Если это НЕ текст - сообщи об ошибке пользователю,
    и сделай так, чтобы следующее сообщение пользователя попало в эту же функцию - get_promt()
    
    За выполнение: 2 балла 
    '''
    if ...:
        bot.send_message(user_id, "Необходимо отправить именно текстовое сообщение")
        ...
        return

    # Получаем текст сообщения от пользователя
    user_request = message.text

    '''
    Напиши проверку задачи пользователя на количество токенов. Сейчас, вместо токенов, проверяй на количество символов.
    Например: максимально 150 символов. Если количество символов больше - сообщи об ошибке пользователю, 
    и сделай так, чтобы следующее сообщение пользователя попало в эту же функцию - get_promt()
    
    За выполнение: 2 балла
    '''
    if ...:
        bot.send_message(user_id, "Запрос превышает количество символов\nИсправь запрос")
        ...
        return

    '''
    Сделай проверку: если у пользователя нет начатой задачи, тогда ее нужно начать
    
    За выполнение: 3 балла
    '''
    if ...:
        # Сохраняем промт пользователя и начало ответа GPT в словарик users_history
        users_history[user_id] = {
            'system_content': "Ты - дружелюбный помощник для решения задач по математике. Давай подробный ответ с решением на русском языке",
            'user_content': user_request,
            'assistant_content': "Решим задачу по шагам: "
        }

    # Пока что ответом от GPT будет любой текст, просто придумай его)
    answer = "Позже здесь будет реальное решение, а пока что так :)"

    '''
    Напиши код, который будет дописывать этот ответ от GPT к предыдущему ответу GPT
    (ответ от GPT - сообщение, которое ты придумал_а выше)
    
    За выполнение: 2 балла
    '''
    # users_history...

    '''
    Отправь полный ответ пользователю
    И добавь кнопочки "продолжить решение" и "завершить решение".
        Продолжить решение - пользователь просит GPT дописать ответ к текущей задаче
        Завершить решение - решение задачи прекращается, все предыдущие сообщения удаляются из истории пользователя
    
    За выполнение: 2 балла
    '''
    # bot.send_message()


'''
Напиши фильтр для обработки кнопочки "Завершить решение"

За выполнение: 1 балл
'''
# РЕШЕНИЕ
def end_filter(message):
    ...


@bot.message_handler(content_types=['text'], func=end_filter)
def end_task(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Текущие решение завершено")
    users_history[user_id] = {}
    solve_task(message)


'''
Добавь в функции get_promt и end_task проверку состояния пользователя.
Например, если пользователь не начал диалог, но хочет продолжить ответ - бот отправит сообщение об ошибке и предложит сначала начать задачу

За выполнение: 3 балла
'''

bot.polling()
