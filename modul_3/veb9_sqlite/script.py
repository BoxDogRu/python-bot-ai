import sqlite3
import random

def prepare_database():
    try:
        # Установка соединения с базой данных
        connection = sqlite3.connect('sqlite3.db')
        cur = connection.cursor()

        # Создание таблицы students, если она не существует
        cur.execute('''CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY,
                            student_name TEXT,
                            group_number INTEGER,
                            course TEXT,
                            age INTEGER
                       )''')

        # Заполнение таблицы данными
        student_names = ['Иван', 'Мария', 'Петр', 'Анна', 'Алексей', 'Елена', 'Сергей', 'Ольга', 'Владимир', 'Татьяна']
        courses = ['python-ai', 'web', 'game-dev']

        for i in range(1, 31):  # Заполним таблицу 30 случайными записями
            student_name = random.choice(student_names)
            group_number = random.randint(1, 20)
            course = random.choice(courses)
            age = random.randint(14, 18)
            cur.execute('''INSERT INTO students (student_name, group_number, course, age) 
                           VALUES (?, ?, ?, ?)''', (student_name, group_number, course, age))

        # Фиксация изменений и закрытие соединения
        connection.commit()
    except sqlite3.Error as e:
        print("Ошибка при работе с SQLite:", e)
    finally:
        connection.close()

prepare_database()
