from prepare_database_rez import prepare_db, execute_selection_query, TABLE_NAME


# ------------- Вариант 1 -------------
# Функция, возвращающая размер указанной сессии в токенах
def get_session_size(user_id, session_id):
    sql_query = f'''SELECT tokens FROM {TABLE_NAME} WHERE user_id = ? AND session_id = ? ORDER BY date DESC LIMIT 1'''
    session_size = execute_selection_query(sql_query, (user_id, session_id, ))[0][0]
    return session_size

"""
Альтернативная версия 
token_sum = execute_selection_query('''SELECT SUM(tokens) AS total_sum FROM database WHERE user_id = ? AND session_id = ?''', (user_id, session_id))[0][0]
"""

# ------------- Вариант 2 -------------
# Функция для получения идентификатора последней сессии пользователя (чтобы мы знали, какое значение задать новому)
def get_last_session_id(user_id):
    sql_query = f'''SELECT session_id FROM {TABLE_NAME} WHERE user_id = ? ORDER BY date DESC LIMIT 1'''
    last_session_id = execute_selection_query(sql_query, (user_id, ))[0][0]
    return last_session_id



# ------------- Вариант 3 -------------
# Функция для проверки лимита пользователей.
# Выводит False, если количество уникальных пользователей
# в таблице меньше USERS_LIMIT
# Здесь поможет DISTINCT
def is_users_limit(USERS_LIMIT = 3):
    unique_users = execute_selection_query(f'''SELECT COUNT(DISTINCT user_id) FROM {TABLE_NAME}''')[0][0]
    return unique_users >= USERS_LIMIT

"""
Альтернативная версия - тоже рабочая
def is_users_limit(USERS_LIMIT = 3):
    unique_users = execute_selection_query(f'''SELECT DISTINCT user_id FROM {TABLE_NAME}''')
    return len(unique_users) >= USERS_LIMIT
"""


# ------------- Вариант 4 -------------
# Функция, которая суммирует размеры
# всех сессий всех пользователей
def get_all_tokens():
    # Получить список уникальных пар из айди пользователей
    # и сессий.
    # По ним можно получить каждую уникальную сессию
    sql_query = f'SELECT DISTINCT user_id, session_id from {TABLE_NAME};'
    all_user_and_session_ids = execute_selection_query(sql_query)
    #print(all_user_and_session_ids)

    all_tokens = 0
    # Для каждой пары найти размер сессии по последней строчке
    # и просуммировать
    for user_id, session_id in all_user_and_session_ids:
        session_size = get_session_size(user_id, session_id)
        #print(session_size)
        all_tokens += session_size
    return all_tokens


if __name__ == '__main__':
    # prepare_db() # Эту функцию достаточно вызвать один раз - после этого у вас появится нужная таблица

    # Здесь можно протестировать наши функции
    print('get_session_size', get_session_size(10001, 3))
    print('get_last_session_id', get_last_session_id(10002))
    print('is_users_limit', is_users_limit(USERS_LIMIT=3))
    # 84
    print('get_all_tokens', get_all_tokens())
