import logging
import os
import sqlite3
from datetime import datetime

from config import DB_DIR, DB_NAME, DB_TABLE_PROMPTS_NAME, LOGS_PATH


logging.basicConfig(filename=LOGS_PATH, level=logging.DEBUG,
                    format="%(asctime)s %(message)s", filemode="w")


# Функция для подключения к базе данных или создания новой, если её ещё нет
def create_db(directory=DB_DIR, database_name=DB_NAME):
    if not os.path.exists(directory):
        os.makedirs(directory)

    db_path = f'{directory}/{database_name}'
    with sqlite3.connect(db_path) as connection:
        connection.cursor()

    logging.info(f"DATABASE: Output: База данных успешно создана")


# Функция для выполнения любого sql-запроса для изменения данных
def execute_query(sql_query, data=None, db_path=f'{DB_DIR}/{DB_NAME}'):
    try:
        logging.info(f"DATABASE: Execute query: {sql_query}")

        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            if data:
                cursor.execute(sql_query, data)
            else:
                cursor.execute(sql_query)

            connection.commit()

    except Exception as e:
        logging.error(f"DATABASE: Error executing query: {e}")


# Функция для выполнения любого sql-запроса для получения данных (возвращает значение)
def execute_selection_query(sql_query, data=None, db_path=f'{DB_DIR}/{DB_NAME}'):
    try:
        logging.info(f"DATABASE: Execute query: {sql_query}")

        with sqlite3.connect(db_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            if data:
                cursor.execute(sql_query, data)
            else:
                cursor.execute(sql_query)
            rows = cursor.fetchall()

        return rows
    except Exception as e:
        logging.error(f"DATABASE ERROR: {e}")


# Функция для создания новой таблицы (если такой ещё нет)
# Получает название и список колонок в формате ИМЯ: ТИП
# Создаёт запрос CREATE TABLE IF NOT EXISTS имя_таблицы (колонка1 ТИП, колонка2 ТИП)
def create_table(table_name, table_columns):
    sql_query = f'CREATE TABLE IF NOT EXISTS {table_name} '
    sql_query += '('

    cols = []
    for name, type in table_columns.items():
        cols.append(f'{name} {type}')
    sql_query += ', '.join(cols) + ')'

    execute_query(sql_query)


# Функция для вывода всей таблицы (для проверки)
# Создаёт запрос SELECT * FROM имя_таблицы
def get_all_rows(table_name):
    rows = execute_selection_query(f'SELECT * FROM {table_name} ORDER BY date desc ')
    for row in rows:
        print(row)


# Функция для вывода количества пользователей (для проверки)
def get_users_amount(table_name):
    row = execute_selection_query(f'SELECT COUNT(DISTINCT user_id) AS unique_users FROM {table_name};')
    return row[0]['unique_users']


# Функция для добавления пользователя в таблицу
def add_user(self, id, story=''):
    """Добавление нового пользователя с историей"""
    if not self.id_in_table(id):
        self._insert_row(self.table_name, [id, story])
    else:
        print(f"Ошибка при добавлении: пользователь с id = {id} уже есть в таблице")


# Функиця для удаления всех записей из таблицы
# Создаёт запрос DELETE FROM имя_таблицы
def clean_table(table_name):
    execute_query(f'DELETE FROM {table_name}')


# Функция для вставки новой строки в таблицу
# Принимает список значений для каждой колонки и названия колонок
# Создаёт запрос INSERT INTO имя_таблицы (колонка1, колонка2)VALUES (?, ?)[значение1, значение2]
def insert_row(table_name, values, columns=''):
    if columns != '':
        columns = '(' + ', '.join(columns) + ')'
    sql_query = f"INSERT INTO {table_name} {columns}VALUES ({', '.join(['?'] * len(values))})"
    execute_query(sql_query, values)


# Функция для проверки, есть ли элемент в указанном столбце таблицы
# Создаёт запрос SELECT колонка FROM имя_таблицы WHERE колонка == значение LIMIT 1
def is_value_in_table(table_name, column_name, value):
    sql_query = f'SELECT {column_name} FROM {table_name} WHERE {column_name} = ? order by date desc'
    rows = execute_selection_query(sql_query, [value])
    return rows


# Функция, записывающая историю запросов в таблицу
def add_record_to_table(user_id, role, content, date, tokens, session_id):
    insert_row(DB_TABLE_PROMPTS_NAME,
               [user_id, role, content, date, tokens, session_id],
               columns=['user_id', 'role', 'content', 'date', 'tokens', 'session_id'])


# Функция для подготовки базы данных
# Создаёт/подключается к бд
def prepare_db(clean_if_exists=False):
    create_db()
    create_table(DB_TABLE_PROMPTS_NAME,
                 table_columns={
                     'id': 'INTEGER PRIMARY KEY',
                     'user_id': 'INTEGER',
                     'role': 'TEXT',
                     'content': 'TEXT',
                     'date': 'DATETIME',
                     'tokens': 'INTEGER',
                     'session_id': 'INTEGER'

                 })
    # Для дебага
    # if clean_if_exists:
    #     clean_table(DB_TABLE_PROMPTS_NAME)


# Функция для получения последнего значения из таблицы для пользователя
def get_value_from_table(value, user_id):
    sql_query = f'SELECT {value} FROM {DB_TABLE_PROMPTS_NAME} where user_id = ? order by date desc'
    rows = execute_selection_query(sql_query, [user_id])
    return rows[0]


# Функция для получения диалога для указанного пользователя
def get_dialogue_for_user(user_id, session_id):
    sql_query = (
        f'SELECT * FROM {DB_TABLE_PROMPTS_NAME} '
        f'where user_id = ? AND tokens IS NOT NULL AND session_id = ?'
        f'order by date asc'
    )
    rows = execute_selection_query(sql_query, [user_id, session_id])
    return rows


# Функция для увелечения сессии пользователя
def increment_session_id(user_id: int):
    row: sqlite3.Row = get_value_from_table("session_id", user_id)
    session_id: int = row["session_id"] + 1
    insert_row(
        DB_TABLE_PROMPTS_NAME,
        [user_id, datetime.now(), session_id],
        ['user_id', 'date', 'session_id']
    )


# Функция, чтобы получить кол-во использованных токенов за все время
def count_all_tokens_from_db():
    sql_query = (
        f"""
        SELECT SUM(subquery.tokens) AS total_tokens
        FROM (
            SELECT tokens
            FROM {DB_TABLE_PROMPTS_NAME}
            WHERE (session_id, date) IN (
                SELECT session_id, MAX(date)
                FROM {DB_TABLE_PROMPTS_NAME}
                GROUP BY session_id
            )
        ) AS subquery;
        """
    )
    rows = execute_selection_query(sql_query)
    return rows[0]['total_tokens']



if __name__ == '__main__':
    prepare_db(True)
    get_all_rows(DB_TABLE_PROMPTS_NAME)
