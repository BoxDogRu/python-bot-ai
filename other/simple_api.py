# В Terminale (не в питоне) вводится команда:
# pip install requests


import requests     # Импортируем установленную библиотеку в программу. И мы уже можем делать запросы в интернет.
# from random import randint    # Генератор случайных чисел из диапазона тоже можно раскомментировать и попробовать.

number = 21
# number = randint(0, 100)

url = f'http://numbersapi.com/{number}'     # формируем ссылку, т.е. то что "парсим".

response = requests.get(url)        # делаем запрос через метод get библиотеки, сохраняем ответ

# Кто-то на вебинаре спрашивал про объект ориентированное программирование (ООП).
# Интереса ради, мы можем посмотреть что мы сохранили.

print(type(response))   # Это специальный тип данных.

# Всё в питоне - объект, и объекты бывают разные. Объект 'response' в библиотеке 'requests' - специальный класс.
# Но нам сейчас достаточно знать лишь одно, что из нашего объекта мы можем получить текстовое содержимое ответа - str.
# Строку - тип данных, который мы уже знаем.
# Кста, на текущей неделе уже работаем с новым типом данных - словарями. Это один из самых крутых типов данных в питоне.
# Открывает бооольшие возможности.

fact = response.text    # получаем строку, в данном случае без круглых скобок, т.к. это т.н. атрибут класса

print(f"Fact about the number {number}: {fact}")
