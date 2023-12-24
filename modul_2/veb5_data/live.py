import json


def load_user_data():
    try:
        with open('user_data.json', 'r+', encoding='utf8') as file:
            data = json.load(file)
    except:
        data = {}
    return data


def save_user_data(user_data):
    with open('user_data.json', 'w+', encoding='utf8') as file:
        json.dump(user_data, file, ensure_ascii=False, indent=2, sort_keys=True)


data = load_user_data()


def register(user_id):
    if user_id in data:
        print('Пользователь с таким именем уже существует. Перенаправляем на логин.')
        login(user_id)
    else:
        password = input('Введите пароль: ')
        data[user_id] = password
        save_user_data(data)
        print('Вы успешно зарегистрировались.')


def login(user_id):
    if user_id not in data:
        print('Пользователь с таким именем не существует. Перенаправляем на регистрацию.')
        register(user_id)
    else:
        password = input('Введите пароль: ')
        if password == data[user_id]:
            print('Вы успешно авторизованы.')
        else:
            print('Неверный пароль. Попробуйте снова.')
            login(user_id)


print('Выберите действие:')
print('1. Зарегистироваться')
print('2. Войти')

choice = int(input())

if choice not in [1, 2]:
    print('Некорректный ввод. Перезапустите программу: ')

user_id = input('Введите имя пользователя: ')
if choice == 1:
    register(user_id)
elif choice == 2:
    login(user_id)
