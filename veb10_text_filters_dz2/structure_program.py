from random_color import random_color2


def filter_scream(text):
    text = text.upper() + '!!!'
    return text


filters = {
    '1': {
        'name': 'The Scream',
        'description': 'Преобразует текст в КРИК!!!',
        "function": filter_scream
    },
    '2': {
        'name': 'Random color',
        'description': 'Давайте раскрасим этом мир!',
        "function": random_color2
    },
    '0': {
        'name': 'Выход из программы',
        'description': 'Спасибо за участие.'
    },
}

while True:
    print('Программа текстового преобразования к вашим услугам!')

    # основное меню
    for number, filter in filters.items():
        if int(number):
            print(f"{number} - фильтр {filter['name']}")
        else:
            print(f"{number} - {filter['name']}")

    choose = input('Введите номер команды - выберите нужный фильтр. Или 0 для выхода.\n')

    # 1. обработка неправильного ввода
    if choose not in filters:
       print("Команд не распознана. Повторите ввод.")

    # 2. выход из программы
    elif not int(choose):
       exit(filters[choose]['description'])

    # 3. меню текущего фильтра
    else:
       filter = filters[choose]
       print(f"Фильтр {filter['name']} к вашим услугам.")
       print(f"{filter['description']}")

       text = input('Введите текст для фильтрации, или 0 для возврата в меню фильтров:\n')

       while text != '0':
           print('Ваш текст: ', text)
           print('Результат: ', filter['function'](text))

           text = input('Введите новый текст, или 0 для возврата в меню фильтров:\n')
