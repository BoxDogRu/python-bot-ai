# Нужно знать: telebot, классы, наследование, лямбда-функции, json
# Сложность: 6 из 10
# Добавлено: бот, наследованный класс

import telebot
from telebot import types
from game import *
# import json

# все пароли и токены не должны быть в коде и должны храниться в отдельном файле
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('TOKEN')

# вариант хранения токена в json
# config_file = open("config.json", "r")
# configs = json.load(config_file)
# token = configs["telegram"]['TOKEN']

# создаём бота
bot = telebot.TeleBot(token, parse_mode=None)

# добавляем к нему меню
menu = {"/start": "Зарегистрироваться в игре", "/help": "Помощь", "/play": "Начать игру!"}
menu_keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
menu_keyboard.add(*menu.keys())
bot.set_my_commands(commands=[types.BotCommand(command, description) for command, description in menu.items()])

# создаём словарь для хранения игроков и игр вида {user_id: player}, {user_id: game}
players = {}
games = {}


def answers_with_choice(options, one_time_keyboard=True):
    """Делает клавиатуру с вариантами ответа."""
    options = map(types.KeyboardButton, options)
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=one_time_keyboard)
    markup.add(*options)
    return markup


# делаем новый класс, наследющий класс Game и переопределяющий некоторые методы
class BotGame(Game):
    """Класс игры, которая работает с ботом."""

    def __init__(self, player, json_file):
        super().__init__(player, json_file)
        # переопределяем метод вывода, чтобы он отправлял сообщение в чат
        self.output = lambda x: bot.send_message(player.id, self.process_output(x))

    def __str__(self):
        return f'BotGame(player={self.player})'

    # переопределяем метод вывода доступных действий, чтобы он выводил кнопки
    def output_actions(self):
        """Выводит варианты действий."""
        location = self.player.location
        markup = answers_with_choice(location.actions.keys())
        bot.send_message(self.player.id, f"{self.process_output(location.description)}", reply_markup=markup)


# создаём функции, которые будут вызываться при вводе команд

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, f'''
/start - Зарегистрироваться в игре
/help - Помощь
/play - Начать игру!''', reply_markup=menu_keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    id, name = message.from_user.id, message.from_user.first_name
    players[id] = Player(id=id, name=name)
    markup = answers_with_choice(['Мужской', 'Женский'])
    bot.send_message(id, f'Привет, {name}! Добро пожаловать в игру!\n'
                         f'Чтобы продолжить, введи, пожалуйста, свой пол', reply_markup=markup)
    bot.register_next_step_handler(message, gender)


def gender(message):
    id = message.from_user.id
    players[id].set_sex(message.text)
    bot.send_message(id, f'Отлично!\nЧтобы начать игру, введи /play. '
                         f'Если тебе нужна помощь, введи /help',
                     reply_markup=menu_keyboard)


@bot.message_handler(commands=['play'])
def play(message):
    id = message.from_user.id
    if id not in players.keys():
        bot.send_message(message.from_user.id, f'Прежде, чем начать игру, '
                                               f'необходимо зарегистрироваться.\n'
                                               f'Введи /start!',
                         reply_markup=menu_keyboard)
        return
    games[id] = BotGame(players[id], 'locations.json')
    games[id].player.location = games[id].locations['start']
    games[id].output_actions()


@bot.message_handler(func=lambda m: True)
def handler(message):
    choice = message.text
    id = message.from_user.id
    if choice not in games[id].player.location.actions.keys():
        bot.send_message(id, f'''Можно выбрать только из вариантов, предложенных в игре. Попробуй ещё раз!''')
    games[id].take_an_action(choice)
    if games[id].player.location.name != "exit":
        games[id].output_actions()
    else:
        bot.send_message(id, f'''Игра окончена!''',
                         reply_markup=menu_keyboard)
        players[id].time_late = 0


bot.infinity_polling()
