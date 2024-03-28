import sqlite3

DB_NAME = 'prompts_database.db'
TABLE_NAME = 'prompts'


# Функция для подключения к базе данных или создания новой, если её ещё нет
def create_db(database_name=DB_NAME):
    connection = sqlite3.connect(database_name)
    connection.close()


# Функция для выполнения любого sql-запроса для изменения данных
# Получает sql-запрос и выполняет его
def execute_query(sql_query, data=None, db_path=DB_NAME):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        if data:
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)
        connection.commit()


# Функция для выполнения любого sql-запроса для получения данных (возвращает значение)
def execute_selection_query(sql_query, data=None, db_path=DB_NAME):
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

    # TODO: дописать запрос для создания таблицы
    sql_query = f'CREATE TABLE IF NOT EXISTS {table_name} <список колонок>'
    execute_query(sql_query)


# Функция для вставки новой строки в таблицу
# Принимает список значений для каждой колонки и названия колонок
# Создаёт запрос INSERT INTO имя_таблицы (колонка1, колонка2)VALUES (?, ?)[значение1, значение2]
def insert_row(table_name, values, columns=''):
    if columns != '':
        columns = '(' + ', '.join(columns) + ')'
    sql_query = f"INSERT INTO {table_name} {columns}VALUES ({', '.join(['?'] * len(values))})"
    execute_query(sql_query, values)


# Функция для заполнения таблицы тестовыми данными
def insert_test_data_in_table(table_name):
    insert_row(TABLE_NAME, [1, 10001, 'system_prompt', 'Ты - помощник для написания сценариев. Напиши историю про Ферзя', '2024-02-17 15:45:00', 8, 1])
    insert_row(TABLE_NAME, [2, 10001, 'user_prompt', 'Далеко на севере есть край под названием Эдилада,', '2024-02-17 15:46:00', 14, 1])
    insert_row(TABLE_NAME, [3, 10001, 'assistant_prompt', 'Что означает "Полная Луна"', '2024-02-17 15:46:15', 15, 1])

    insert_row(TABLE_NAME, [4, 10002, 'system_prompt', 'Ты - помощник для написания сценариев. Напиши историю про Валета', '2024-03-01 22:00:00', 9, 1])
    insert_row(TABLE_NAME, [5, 10002, 'user_prompt', 'Валериан Валет - личный защитник Короля,', '2024-03-01 22:00:30', 17, 1])
    insert_row(TABLE_NAME, [6, 10002, 'assistant_prompt', 'по долгу службы вынужденный сопровождать его во всех похождениях', '2024-03-01 22:00:35', 23, 1])
    insert_row(TABLE_NAME, [7, 10002, 'assistant_prompt', 'и не давать попадать в неприятности,', '2024-03-01 22:00:40', 31, 1])
    insert_row(TABLE_NAME, [8, 10002, 'assistant_prompt', 'хотя его собственная жажда приключений ничуть не меньше.', '2024-03-01 22:00:45', 36, 1])

    insert_row(TABLE_NAME, [9, 10001, 'system_prompt', 'Ты - помощник для написания сценариев. Напиши историю про Короля', '2024-03-05 12:23:00', 8, 2])
    insert_row(TABLE_NAME, [10, 10001, 'user_prompt', 'Однажды Король выглянул в окно и увидел в роще блуждающий огонёк.', '2024-03-05 12:23:20', 14, 2])
    insert_row(TABLE_NAME, [11, 10001, 'assistant_prompt', 'Он был непохож на обычные местерские огни.', '2024-03-05 12:24:00', 16, 2])

    insert_row(TABLE_NAME, [12, 10001, 'system_prompt', 'Ты - помощник для написания сценариев. Напиши историю про Жара', '2024-03-10 11:14:00', 8, 3])
    insert_row(TABLE_NAME, [13, 10001, 'user_prompt', 'В далёкой-далёкой стране жил-был маленький принц по имени Жар Мрамор.', '2024-03-10 11:40:00', 15, 3])
    insert_row(TABLE_NAME, [14, 10001, 'assistant_prompt', 'Он был рождён богиней весны и умел превращаться в золотую птицу.', '2024-03-10 11:41:00', 17, 3])


# Функция для подготовки базы данных
# Создает-подключается к бд, создаёт и заполняет таблицу
def prepare_db():
    create_db()
    create_table(TABLE_NAME)
    insert_test_data_in_table(TABLE_NAME)
