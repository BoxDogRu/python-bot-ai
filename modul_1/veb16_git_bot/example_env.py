"""
python-dotenv - это библиотека Python, которая позволяет загружать переменные окружения из файла .env в ваш проект Python.
Это удобный способ хранения конфиденциальных данных, таких как пароли, API-ключи и другие конфигурационные параметры, вне кода,
что делает их более безопасными и удобными для управления.

Установка: pip install python-dotenv

Пример установки всех необходимых пакетов из файла: pip install -r requirements.txt
"""

from dotenv import load_dotenv
import os

# Загрузить переменные окружения из файла .env
load_dotenv()

# Использовать переменные окружения
db_password = os.getenv("DB_PASSWORD")
api_key = os.getenv("API_KEY")
