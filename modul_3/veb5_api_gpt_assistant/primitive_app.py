import requests
from transformers import AutoTokenizer


def count_tokens(text):
    # tokenizer = AutoTokenizer.from_pretrained("TheBloke/Mistral-7B-Instruct-v0.1-GGUF")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
    return len(tokenizer.encode(text))


print('Привет!')
print('Я твой помощник для решения задач по математике. Можешь ввести любую задачу, и я постараюсь её решить.')
print('Если введёшь слово "Продолжить", я продолжу объяснять задачу.')
print('Для завершения диалога введи слово "Конец".')

system_content = "Ты - дружелюбный помощник для решения задач по математике. Давай подробный ответ с решением на русском языке"
assistant_content = "Решим задачу по шагам: "

task = ""
answer = ""
max_tokens_in_task = 512

while True:
    user_content = input()

    if count_tokens(user_content) > max_tokens_in_task:
        print("Текст задачи слишком длинный!")
        continue

    if user_content.lower() == 'конец':
        break

    if user_content.lower() != "продолжить":
        task = user_content
        answer = ""

    resp = requests.post(
        'http://localhost:1234/v1/chat/completions',
        headers={"Content-Type": "application/json"},

        json={
            "messages": [
                # TODO
                # Добавить запрос ...
                {"role": "user", "content": user_content},
                # TODO
                # Добавить ответ ...
            ],
            "temperature": 1.1,
            "max_tokens": 512
        }
    )

    if resp.status_code == 200 and 'choices' in resp.json():
        result = resp.json()['choices'][0]['message']['content']
        # TODO
        # Простой результат == объяснение задачи
    else:
        print('Не удалось получить ответ от нейросети')
        print('Текст ошибки:', resp.json())
