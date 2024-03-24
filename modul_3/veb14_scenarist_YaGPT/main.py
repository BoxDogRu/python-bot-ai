import requests
from config_template import GPT_MODEL, CONTINUE_STORY, END_STORY, SYSTEM_PROMPT
import os
from dotenv import load_dotenv
import json
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

load_dotenv()

GPT_IAM_TOKEN = os.getenv('GPT_IAM_TOKEN')
FOLDER_ID = os.getenv('FOLDER_ID')

# Словарь для хранения настроек пользователя, формируем в main()
user_data = {}
'''
Примерная структура словаря:

user_data = {
    user_id: {
        'genre': 'genre',
        'character': 'character',
        'setting': 'setting',
        
    }
}
'''

# Словарь для хранения истории диалога пользователя и GPT
user_collection = {}
'''
Примерная структура словаря:

user_collection = {
    user_id: [
        {'role': 'system', 'content': 'system_promt'},
        
    ]
}
'''


def ask_gpt(collection, mode='continue'):
    url = f"https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Authorization': f'Bearer {GPT_IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 100
        },
        "messages": []
    }

    for row in collection:
        content = row['text']

        # TODO. Добавь дополнительный текст к сообщению пользователя в зависимости от режима
        if mode == 'continue' and row['role'] == 'user':
            # CONTINUE_STORY
            content += '\n' + CONTINUE_STORY
        elif mode == 'end' and row['role'] == 'user':
            # END_STORY
            content += '\n' + END_STORY

        data["messages"].append(
                {
                    "role": row["role"],
                    "text": content
                }
            )

    try:
        with open('user_collection.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            result = f"Status code {response.status_code}"
            return result
        result = response.json()['result']['alternatives'][0]['message']['text']
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        result = "Произошла непредвиденная ошибка. Подробности см. в журнале."
    return result


def create_system_prompt(data, user_id):
    prompt = SYSTEM_PROMPT
    # TODO. Допиши к SYSTEM_PROMPT информацию о:
    prompt += f"Придумай сценарий рассказа, который должен быть в жанре {user_data[user_id]['genre']}.Главный герой должен быть {user_data[user_id]['character']}. Действия рассказа происходят в {user_data[user_id]['setting']}. Начало должно быть коротким, 1-3 предложения."

    """
    # Альтернативная версия из тренажера
    prompt += (f"\nНапиши начало истории в стиле {user_data[user_id]['genre']} "
               f"с главным героем {user_data[user_id]['character']}. "
               f"Вот начальный сеттинг: \n{user_data[user_id]['setting']}. \n"
               "Начало должно быть коротким, 1-3 предложения.\n")
    """

    return prompt


def main(user_id=1):
    print("Привет! Я помогу тебе составить классный сценарий!")
    genre = input("Для начала напиши жанр, в котором хочешь составить сценарий: ")
    character = input("Теперь опиши персонажа, который будет главным героем: ")
    setting = input("И последнее. Напиши сеттинг, в котором будет жить главный герой: ")

    # TODO Запиши полученную информацию в user_data
    user_data[user_id] = {
        'genre': genre,
        'character': character,
        'setting': setting,
    }

    """
    # Альтернативная версия 1
    user_data = {
        user_id: {
            'genre': genre,
            'character': character,
            'setting': setting,

        }
    }    
    
    # Альтернативная версия 2
    try:
        user_data[user_id]
    except KeyError:
        user_data[user_id] = {}
    user_data[user_id]["genre"] = genre
    user_data[user_id]["character"] = character
    user_data[user_id]["setting"] = setting

    user_data[user_id] = {
        'genre': genre,
        'character': character,
        'setting': setting,
    }
    """

    # TODO Запиши системный промт, созданный на основе полученной информации от пользователя, в user_collection
    system_prompt = create_system_prompt(user_data, user_id)

    try:
        user_collection[user_id]
    except KeyError:
        user_collection[user_id] = []
    user_collection[user_id].append({"role": "system", "text": system_prompt})

    """
    # Альтернативная версия 1
    
    prompt = create_system_prompt(user_data, user_id)
    user_collection[user_id] = {'role': 'system', 'content': prompt}    # обратить внимание на структуру

    # Альтернативная версия 2
    user_collection = {
        user_id: [
            {'role': 'system', 'content': create_system_prompt(user_data, user_id)},

        ]
    }
    """

    user_content = input('Напиши начало истории: \n')
    while user_content.lower() != 'end':

        # TODO. Запиши user_content в user_collection
        user_collection[user_id].append({"role": "user", "text": user_content})
        """
        user_collection = {
            user_id: [
                {'role': 'system', 'content': create_system_prompt(user_data, user_id)},
                {'role': 'user', 'content': user_content}

            ]
        }
        """

        assistant_content = ask_gpt(user_collection[user_id])

        # TODO. Запиши assistant_content в user_collection
        user_collection[user_id].append({"role": "assistant", "text": assistant_content})

        print('YandexGPT: ', assistant_content)
        user_content = input('Напиши продолжение истории. Чтобы закончить введи end: \n')

    assistant_content = ask_gpt(user_collection[user_id], 'end')
    # Запиши assistant_content в user_collection
    user_collection[user_id].append({"role": "assistant", "text": assistant_content})


    with open('user_collection_fin.json', 'w', encoding='utf-8') as f:
        json.dump(user_collection, f, ensure_ascii=False, indent=2)
    print('\nВот, что у нас получилось:\n')

    # TODO. Напиши красивый вывод получившейся истории
    for mes in user_collection[user_id]:
        print(mes['text'])

    input('\nКонец... ')


if __name__ == "__main__":
    main()
