import requests
from transformers import AutoTokenizer


class GPT:
    def __init__(self, system_content=""):
        self.system_content = system_content
        self.URL = 'http://localhost:1234/v1/chat/completions'
        self.HEADERS = {"Content-Type": "application/json"}
        self.MAX_TOKENS = 256
        self.assistant_content = "Решим задачу по шагам: "

    # Подсчитываем количество токенов в промпте
    @staticmethod
    def count_tokens(prompt):
        tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")  # название модели
        return len(tokenizer.encode(prompt))

    # Проверка ответа на возможные ошибки и его обработка
    def process_resp(self, response) -> [bool, str]:
        # Проверка статус кода
        if response.status_code < 200 or response.status_code >= 300:
            self.clear_history()
            return False, f"Ошибка: {response.status_code}."

        # Проверка на json
        try:
            full_response = response.json()
        except:
            self.clear_history()
            return False, "Ошибка получения JSON"

        # Проверка ответа на ошибку
        if "error" in full_response or 'choices' not in full_response:
            self.clear_history()
            return False, f"Ошибка: {full_response}"

        # Результат
        result = full_response['choices'][0]['message']['content']

        # TODO
        # Пустой результат == объяснение закончено

        # Сохраняем ответ в истории
        self.save_history(result)
        return True, self.assistant_content

    # Формирование промпта
    def make_prompt(self, user_request):
        json = {
            "messages": [
                # TODO Добавить запрос ...
                {"role": "user", "content": user_request},
                # TODO Добавить ответ ...
            ],
            "temperature": 1.2,
            "max_tokens": self.MAX_TOKENS,
        }
        return json

    # Отправка запроса
    def send_request(self, json):
        resp = requests.post(url=self.URL, headers=self.HEADERS, json=json)
        return resp

    # Сохраняем историю ответов
    def save_history(self, content_response):
        # TODO, замени pass
        pass

    # Очистка истории ответов
    def clear_history(self):
        # TODO, замени pass
        pass
