from telebot.types import BotCommand

keyboard_menu = [
    BotCommand('start', 'Перезапустить бота'),
    BotCommand('talk', 'Начать диалог'),
    BotCommand('stats', 'Статистика использования'),
    BotCommand('about', 'Бот-сценарист')
]

keyboard_menu_admin = [  # Установка списка команд с областью видимости и описанием
    BotCommand('start', 'Перезапустить бота'),
    BotCommand('talk', 'Начать диалог'),
    BotCommand('about', 'Бот-сценарист'),
    BotCommand('debug', 'Debug-режим'),
    BotCommand('settings', 'Изменить конфигурацию GPT'),
    BotCommand('stats_admin', 'Статистика использования')
]