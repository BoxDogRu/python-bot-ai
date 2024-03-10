import sqlite3
import logging

from config_db import DB_DIR, DB_NAME, DB_TABLE_USERS_NAME, LOGS_PATH

logging.basicConfig(filename=LOGS_PATH)


# Функция для подключения к базе данных или создания новой, если её ещё нет
def create_db(database_name=DB_NAME):
    db_path = f'{database_name}'
    connection = sqlite3.connect(db_path)
    connection.close()

    logging.info('Database created')


# Функция для выполнения любого sql-запроса для изменения данных
def execute_query(sql_query, data=None, db_path=f'{DB_NAME}'):

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    if data:
        cursor.execute(sql_query, data)
    else:
        cursor.execute(sql_query)

    connection.commit()
    connection.close()


# Функция для выполнения любого sql-запроса для получения данных (возвращает значение)
def execute_selection_query(sql_query, data=None, db_path=f'{DB_NAME}'):

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    if data:
        cursor.execute(sql_query, data)
    else:
        cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.close()
    return rows


# Функция для создания новой таблицы (если такой ещё нет)
# Получает название и список колонок в формате ИМЯ: ТИП
# Создаёт запрос CREATE TABLE IF NOT EXISTS имя_таблицы (колонка1 ТИП, колонка2 ТИП)
def create_table(table_name):
    # TODO: Здесь необходимо прописать тип полей, вместо ##

    sql_query = f'CREATE TABLE IF NOT EXISTS {table_name} ' \
                f'(id INTEGER PRIMARY KEY, ' \
                f'user_id INTEGER, ' \
                f'subject TEXT, ' \
                f'level TEXT, ' \
                f'task TEXT, ' \
                f'answer TEXT)'
    execute_query(sql_query)


# Функция для вывода всей таблицы (для проверки)
# Создаёт запрос SELECT * FROM имя_таблицы

# def execute_selection_query(sql_query, data, db_path=f'{DB_NAME}'):
def get_all_rows(table_name):
    # Владимир
    query = f'SELECT * FROM {table_name}'
    rows = execute_selection_query(query, None)
    print(rows)



# Функция для удаления всех записей из таблицы
# Создаёт запрос DELETE FROM имя_таблицы
def clean_table(table_name):
    # TODO: Требуется написать код для удаления всех записей таблицы
    pass


# Функция для вставки новой строки в таблицу
# Принимает список значений для каждой колонки и названия колонок
# Создаёт запрос INSERT INTO имя_таблицы (колонка1, колонка2) VALUES (?, ?)[значение1, значение2]
"""
def insert_row(table_name, values):
    # Федор
    columns = ', '.join('?' * len(values))
    query = f"INSERT INTO {table_name} VALUES ({columns});"

    execute_query(query, values)
    """


def insert_row(values):
    columns = '(user_id, subject, level, task, answer)'
    query = f"INSERT INTO {DB_TABLE_USERS_NAME} {columns} VALUES (?, ?, ?, ?, ?)"
    execute_query(query, values)


# Функция для проверки, есть ли элемент в указанном столбце таблицы
# Создаёт запрос SELECT колонка FROM имя_таблицы WHERE колонка == значение LIMIT 1
def is_value_in_table(table_name, column_name, value):
    # TODO: Требуется написать код для проверки есть ли запись в таблице
    pass


# Удалить пользователя по id
def delete_user(table_name, user_id):
    # Даша
    user_delete = f'DELETE FROM {table_name} WHERE id = {user_id};'
    execute_query(user_delete)


# Обновить значение в указанной строке и колонки
def update_row_value(table_name, user_id, column_name, new_value):
    # Николай тестирует
    try:
        data = (new_value, user_id)
        query = f"UPDATE {table_name} SET {column_name} = ? WHERE user_id = ?"
        execute_query(query, data=data)
    except sqlite3.OperationalError:
        print("Неверные данные")


# Функция для получения данных для указанного пользователя
def get_data_for_user(table_name, user_id):
    # Леонид
    try:
        query = f"SELECT * FROM {table_name} WHERE user_id = {user_id}"
        execute_query(query)
    except sqlite3.OperationalError:
        print("Ошибка в get_data_for_user")


# Функция для подготовки базы данных
# Создаёт/подключается к бд, добавляет все таблицы, заполняет таблицу с промтами
def prepare_db(clean_if_exists=False):
    create_db()
    create_table(DB_TABLE_USERS_NAME)


if __name__ == '__main__':
    prepare_db(True)
    get_all_rows(DB_TABLE_USERS_NAME)

    # вариант 1
    # insert_row(DB_TABLE_USERS_NAME, [1, 'math', 'beginner', '2+2=', '4'])
    # вариант 2
    # insert_row([2, 'history', 'advanced', '????', ''])

    update_row_value(DB_TABLE_USERS_NAME, 2, 'task', '2*442')
    # update_row_value(DB_TABLE_USERS_NAME, 1, 'answer', '=884')
    get_all_rows(DB_TABLE_USERS_NAME)

    res = get_data_for_user(2)
    print(res)

    # delete_user()

