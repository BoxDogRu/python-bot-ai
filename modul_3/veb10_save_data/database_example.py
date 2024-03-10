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

# def execute_selection_query(sql_query, data=None, db_path=f'{DB_NAME}'):
def get_all_rows(table_name):
    # TODO: Требуется написать код для вывода всей таблицы
    query = f'SELECT * FROM {table_name}'
    rows = execute_selection_query(query)
    print(rows)



# Функиця для удаления всех записей из таблицы
# Создаёт запрос DELETE FROM имя_таблицы
def clean_table(table_name):
    # TODO: Требуется написать код для удаления всех записей таблицы
    pass


# Функция для вставки новой строки в таблицу
# Принимает список значений для каждой колонки и названия колонок
# Создаёт запрос INSERT INTO имя_таблицы (колонка1, колонка2) VALUES (?, ?)[значение1, значение2]
def insert_row(values):
    # TODO: Требуется написать код для вставки новой строки в таблицу
    pass


# Функция для проверки, есть ли элемент в указанном столбце таблицы
# Создаёт запрос SELECT колонка FROM имя_таблицы WHERE колонка == значение LIMIT 1
def is_value_in_table(table_name, column_name, value):
    # TODO: Требуется написать код для проверки есть ли запись в таблице
    pass


# Удалить пользователя по id
def delete_user(user_id):
    # TODO: Требуется написать код для удаления пользователя по id
    pass


# Обновить значение в указанной строке и колонки
def update_row_value(user_id, column_name, new_value):
    # TODO: Здесь вам нужно добавить код для выполнения запроса и записи в логи
    pass


# Функция для получения данных для указанного пользователя
def get_data_for_user(user_id):
    # TODO: Здесь вам нужно добавить код для выполнения запроса и записи в логи
    pass


# Функция для подготовки базы данных
# Создаёт/подключается к бд, добавляет все таблицы, заполняет таблицу с промтами
def prepare_db(clean_if_exists=False):
    create_db()
    create_table(DB_TABLE_USERS_NAME)


if __name__ == '__main__':
    prepare_db(True)
    get_all_rows(DB_TABLE_USERS_NAME)

    insert_row([1, 'math', 'beginner', '2+2=', '4'])
    insert_row([2, 'history', 'advanced', '????', ''])

    update_row_value(1, 'task', '2*442')
    update_row_value(1, 'answer', '=884')
    get_all_rows(DB_TABLE_USERS_NAME)

    res = get_data_for_user(2)
    print(res)

