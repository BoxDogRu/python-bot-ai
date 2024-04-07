import json

import dateutil.parser
from datetime import datetime, timezone
import time

import jwt
import requests


def load_authorization():
    """Загрузка авторизационных данных."""

    try:
        with open('auth_gpt/authorized_key.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("auth_gpt/authorized_key.json file not found")
        return None
    except json.JSONDecodeError:
        print("Error decoding json")
        return None


def save_token_to_file(token_response):
    """Сохраняем iamToken"""

    try:
        data = token_response.text
        data_dict = json.loads(data)
        with open('auth_gpt/iam_token.json', 'w') as file:
            json.dump(data_dict, file)
        print("Token saved successfully to iam_token.json")
    except Exception as e:
        print(f"An error occurred while saving the token: {e}")


def get_token(encoded_token):
    """Получаем iamToken"""

    try:
        response = requests.post(
            'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            headers={'Content-Type': 'application/json'},
            json={'jwt': encoded_token})
        response.raise_for_status()
        save_token_to_file(response)
        return response.json()['iamToken']
    except requests.exceptions.RequestException as e:
        print(f"Error getting token: {e}")
        return None


def create_new_token():
    """
    Функция создания нового IAM-токена
    - Создаем JWT
    - Меняем JWT на IAM-токен
    - Сохраняем токен
    - Возвращаем токен
    """
    print('Создаем новый токен')
    auth_data = load_authorization()

    if auth_data:
        service_account_id = auth_data.get('service_account_id')
        key_id = auth_data.get('id')
        private_key = auth_data.get('private_key')

        now = int(time.time())
        payload = {
                'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
                'iss': service_account_id,
                'iat': now,
                'exp': now + 360}

        # Формирование JWT.
        encoded_token = jwt.encode(
            payload,
            private_key,
            algorithm='PS256',
            headers={'kid': key_id})
        # print('encoded_token', encoded_token)

        return get_token(encoded_token)
    else:
        print("Error: Unable to load authorization data.")
        return None


def is_token_valid(token_data):
    """Функция проверки валидности токена"""
    if token_data is None or not isinstance(token_data, dict):
        return False

    expires_at = token_data.get('expiresAt')
    if not expires_at:
        return False

    expires_at_datetime = dateutil.parser.parse(expires_at)
    # print('expires_at_datetime', expires_at_datetime)
    # print('now', datetime.now(timezone.utc))

    return expires_at_datetime > datetime.now(timezone.utc)


def get_valid_token():
    """Функция получения валидного токена.
    Возвращаем валидный токен."""
    try:
        with open('auth_gpt/iam_token.json', 'r') as file:
            token_data = json.load(file)
            if not is_token_valid(token_data):
                print('Невалидный токен, создаем новый')
                iam_token = create_new_token()
                if iam_token is None:
                    raise ValueError("Token creation failed")
                return iam_token
            print('Токен валидный')
            return token_data["iamToken"]
    except FileNotFoundError:
        raise ValueError("Token creation failed - FileNotFoundError")
