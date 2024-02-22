from gpt import GPT

# Объект GPT
gpt = GPT()


# Диалог с GPT
def gpt_dialog():
    print('Можешь ввести любую задачу, и я постараюсь её решить, и я постараюсь её решить')
    print('- Если напишешь "продолжи", я продолжу объяснять задачу')
    print('- Для завершения диалога напиши "конец"')
    while True:
        # Получение запроса от пользователя
        user_request = input("Ввод: ")

        # Завершение работы с GPT
        if user_request.lower() == 'конец':
            break

        # Проверка запроса на количество токенов
        request_tokens = gpt.count_tokens(user_request)
        while request_tokens > gpt.MAX_TOKENS:
            user_request = input("Запрос слишком длинный\nПожалуйста введите запрос заново\nВвод: ")
            request_tokens = gpt.count_tokens(user_request)

        # НЕ продолжаем обработку ответа и начинаем общаться заново
        if user_request.lower() != 'продолжи':
            gpt.clear_history()
        # Формирование промта
        json = gpt.make_prompt(user_request)

        # Отправка запроса
        resp = gpt.send_request(json)

        # Проверка ответа на наличие ошибок и парсинг его
        response = gpt.process_resp(resp)
        print(response)
        if not response[0]:
            print("Не удалось выполнить запрос...")
        # Вывод ответа или сообщения об ошибке
        print(response[1])


# Выход
def end():
    print("До новых встреч!")
    exit(0)


# Запуск программы
def start():
    menu = {
        "1": {
            "text": "Общение с GPT",
            "func": gpt_dialog
        },
        "2": {
            "text": "Выход",
            "func": end
        }
    }

    print("Добро пожаловать в Чат-с-GPT\nЯ твой помощник для решения задач по математике")
    # Бесконечный цикл
    while True:
        # Вывод меню
        print("Меню:")
        for num, item in menu.items():
            print(f"{num}. {item['text']}")

        # Получение выбора пользователя
        choice = input("Выберите: ")
        while choice not in menu:
            choice = input("Выберите корректный пункт: ")

        # Запуск соответствующей функции из меню
        menu[choice]['func']()


# Точка входа в программу
if __name__ == "__main__":
    start()
