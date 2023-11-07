from veb10_random_color import random_color


print('Вариант 1. "Диспетчер" и простые функции')
def filter(filter_id, text):
    """Фильтры
    Caps - все буквы в верхний регистр.
    Lower - все буквы в нижний регистр.
    Title (Крик) - первые буквы в словах в верхний регистр.
    """

    if filter_id == 1:
        return text.upper()
    elif filter_id == 2:
        return text.lower()
    elif filter_id == 3:
        return text.title()
    elif filter_id == 4:
        return random_color(text)
    else:
        return text

print(filter(1, 'Кодеры любят сталкеров: гит, гитхаб.'))
print(filter(2, '"Есть ли у тебя WiFi?"'))
print(filter(3, 'Кофе, код, бесконечный цикл.'))
print(filter(4, 'Почему программист разорился? Потому что он исчерпал всё своё кэширование.'))


print('\nВариант 2. Простое комбинирование функций')

def camel_filter(text):
    """Преобразует текст в формат CamelCase.
    Нет пробелов и первая буква каждого слова заглавная.
    """
    return text.title().replace(" ", "")


def snake_filter(text):
    """Преобразует текст в формат snake_case.
    Нижний регистр, все пробелы заменяются на нижнее подчёркивание.
    """
    return text.lower().replace(" ", "-")

print(camel_filter('Software developers, the real keyboard warriors.'))
print(snake_filter('Отладка - поиск иголки в стоге стоге стоге.'))
print('Можно еще отладить по знакам препинания')

# Дополнительная информация
# ctrl + / - раскомментировать строки в pyCharm

# import string
# from string import punctuation
#
# print('Требуется доработка обработка символов, в нашем распоряжении')
# print('3. Библиотечка string')
# print(string.ascii_letters)
# print(string.ascii_uppercase)
# print(string.ascii_lowercase)
# print(string.digits)
# print(string.hexdigits)
# print(string.octdigits)
# print(string.punctuation)
# print(punctuation)
# print(string.printable)

# Кириллица
# cyrillic_lower_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
# cyrillic_letters = cyrillic_lower_letters + cyrillic_lower_letters.upper()
# print(cyrillic_letters)


# Дополнительный пример для изучения.
# Пример создания cyrillic_letters с Unicode.
# cyrillic_letters = ''.join(map(chr, range(ord('А'), ord('я')+1))) + 'Ёё'
# print(cyrillic_letters)

# # функции из примера
# print('_'.join(['mama', 'mila', 'ramu'])) # join() - список в строку
# print(list(map(str, input().split())))    # list() + map() + range
# print(ord('Ё'), ord('ё'))                 # ord()
# print(chr(1040), chr(1103))               # chr()
