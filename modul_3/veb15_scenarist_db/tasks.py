from prepare_database import prepare_db, execute_selection_query, TABLE_NAME


# ------------- Вариант 1 -------------
# Функция, возвращающая размер указанной сессии в токенах
def get_session_size(user_id, session_id):
    # Получить последнюю строчку для указанной сессии и пользователя
    # Взять из неё значение столбца tokens
    session_size = ''
    return session_size


# ------------- Вариант 2 -------------
# Функция для получения идентификатора последней сессии пользователя (чтобы мы знали, какое значение задать новому)
def get_last_session_id(user_id):
    last_session_id = ''
    return last_session_id


# ------------- Вариант 3 -------------
# Функция для проверки лимита пользователей. Выводит False, если количество уникальных пользователей в таблице меньше USERS_LIMIT
# Здесь поможет DISTINCT
def is_users_limit(USERS_LIMIT = 3):
    unique_users = ''
    return unique_users >= USERS_LIMIT


# ------------- Вариант 4 -------------
# Функция, которая суммирует размеры всех сессий всех пользователей
def get_all_tokens():
    # Получить список уникальных пар из айди пользователей и сессий. По ним можно получить каждую уникальную сессию
    sql_query = f'SELECT DISTINCT user_id, session_id from {TABLE_NAME};'

    all_user_and_session_ids = ''
    # Для каждой пары найти размер сессии по последней строчке и просуммировать
    for user_id, session_id in all_user_and_session_ids:
        sql_query = ''
        all_tokens = ''
    return all_tokens


if __name__ == '__main__':
    prepare_db() # Эту функцию достаточно вызвать один раз - после этого у вас появится нужная таблица

    # Здесь можно протестировать наши функции
