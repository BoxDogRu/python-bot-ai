import json

# Создание словаря с информацией о пользователе
user_data = {
    "12376": {
        "name": "Дмитрий",
        "age": 17,
        "city": "Санкт-Петербург"
    },
    "5454": {
        "name": "Станислав",
        "age": 20,
        "city": "Москва"
    },
}

# Преобразование словаря в JSON-строку
json_data = json.dumps(user_data)

# Вывод JSON-строки
print(json_data)

# Преобразование JSON-строки в словарь
user_data = json.loads(json_data)

# Получение имен из JSON
print(user_data)
print(user_data['12376']['name'])
print(user_data['5454']['name'])

for id in user_data.keys():
    print(user_data[id]["name"])

# Генерация пары вопросов на основе информации о пользователе
questions = []
for user_id in user_data:
    questions.append(f'Как тебя зовут, {user_data[user_id]["name"]}?')
    questions.append(f'Сколько тебе лет, {user_data[user_id]["name"]}?')

# Вывод вопросов
for question in questions:
    print(question)

