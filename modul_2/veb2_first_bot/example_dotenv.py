# pip install python-dotenv
# необходимо создать файл .env, в котором и будем хранить конфиденциальные данные, например, токен бот
# необходимо проверить, что .env не пушится в git

from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('TOKEN')
