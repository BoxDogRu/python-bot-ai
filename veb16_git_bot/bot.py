import os
from typing import Type
from random import randint

import telebot      # Документация https://pypi.org/project/pyTelegramBotAPI/
from filters import Filter  # BlueFilter, GreenFilter, InverseFilter, RedFilter
from filters import DolgovBlurFilter, SopolevRandomFilter, BekrenevReversFilter, KirpichevRedFilter, OrlovGreenFilter, BuninEdgesFilter
from PIL import Image
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, Message

# TOKEN = "6280348456:ABGXJ4SjOcaHjKMA3fIBLydbkbKnph_XKoM"
from dotenv import load_dotenv  # загружаем переменные среды
load_dotenv()
TOKEN = os.getenv('TOKEN')

print(f'TOKEN {TOKEN[0:3]}...{TOKEN[-4:-1]}')
bot = telebot.TeleBot(TOKEN)

filters: dict[str, Type[Filter]] = {
    "Рандом от Александра": SopolevRandomFilter(),
    "Блюр от Данилы": DolgovBlurFilter(),
    "ЧБ-реверс от Егора": BekrenevReversFilter(),
    "Красная маска от Захара": KirpichevRedFilter(),
    "Зеленая маска от Кирилла": OrlovGreenFilter(),
    "Рельеф от Николая": BuninEdgesFilter(),
}

# Словарь для хранения последней пользовательской картинки
user_images = {}

images_folder = "./images"

if not os.path.exists(images_folder):
    os.makedirs(images_folder)


@bot.message_handler(commands=["start"])
def handle_start(message: Message):
    bot.send_message(
        message.chat.id,
        "Я бот, который накладывает фильтры на картинки. Пожалуйста, загрузите изображение.",
    )


@bot.message_handler(content_types=["photo"])
def handle_photo(message: Message):
    process_image(message)


@bot.message_handler(content_types=["text"])
def handle_text(message: Message):
    apply_filter(message)


def process_image(message: Message):
    """Обработка изображений"""
    #try:
    # Получаем информацию о картинке
    file_info = bot.get_file(message.photo[-1].file_id)

    # Скачиваем картинку по ссылке
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохраняем картинку во временный файл
    # file_path = f"{images_folder}/{message.chat.id}.jpg"

    # Альтернативное решение - сохраняем все загруженные картинки от пользователей, обновляем их при применении фильтра
    if not os.path.isdir(f"{images_folder}/{message.chat.id}"):
        os.mkdir(f"{images_folder}/{message.chat.id}")
    file_path = f"{images_folder}/{message.chat.id}/{str(randint(0, 1000001))}.jpg"

    with open(file_path, "wb") as image_file:
        image_file.write(downloaded_file)

    # Привязываем файл к пользователю
    user_images[message.chat.id] = file_path

    # Отправляем сообщение о выборе фильтра
    keyboard = make_filter_options_keyboard(message)
    bot.send_message(message.chat.id, "Выберите фильтр:", reply_markup=keyboard)

    #except Exception:
    #    bot.reply_to(message, "Что-то пошло не так. Пожалуйста, отправьте изображение.")


def make_filter_options_keyboard(message: Message):
    """Собирает меню с кнопками-названиями фильтров"""
    markup = ReplyKeyboardMarkup(row_width=1)
    filter_buttons = [KeyboardButton(filt_name) for filt_name in filters.keys()]
    markup.add(*filter_buttons)
    return markup


def apply_filter(message: Message):
    """Применение выбранного фильтра и отправка результата.
    Обработка текстовых сообщений"""

    # Считываем картинку из временного файла
    file_path = user_images.get(message.chat.id)
    if not file_path:
        bot.reply_to(
            message, "Изображение не найдено. Пожалуйста, загрузите изображение."
        )
        return

    try:
        img = Image.open(file_path)
    except IOError:
        # Ошибка считывания файла
        bot.reply_to(
            message,
            "Формат изображения не поддерживается. Пожалуйста, загрузите другое изображение.",
        )
        return

    # Получаем название фильтра из сообщения пользователя
    selected_filter_name = message.text
    if selected_filter_name not in filters:
        bot.reply_to(
            message,
            "Выбранный фильтр не найден. Пожалуйста, выберите фильтр из предложенного списка.",
        )
        return

    try:
        # Выбираем фильтр и применяем его
        selected_filter = filters[selected_filter_name]
        img = selected_filter.apply_to_image(img)

        # Сохраняем результат без создания временного файла
        img.save(file_path, "JPEG")

        with open(file_path, "rb") as image_file:
            bot.send_photo(message.chat.id, photo=image_file)
            bot.send_message(
                message.chat.id, "Ваше изображение с примененным фильтром."
            )

        # Даём пользователю выбрать другой фильтр
        # keyboard = make_filter_options_keyboard(message)
        # bot.send_message(message.chat.id, "Выберите фильтр:", reply_markup=keyboard)
    except Exception as e:
        print(e)
        bot.reply_to(message, "Что-то пошло не так. Пожалуйста, попробуйте еще раз.")

bot.polling()
