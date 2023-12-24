# https://praktikum.notion.site/7172d54a87b74cdaac02fa37049d76b6

game_data = {
    "start": {
        "description": "Вы стоите на перекрестке. Куда вы хотите пойти?\n1) В лес\n2) В горы\n3) К деревне",
        "options": {"1": "forest", "2": "mountains", "3": "village"},
    },
    "forest": {
        "description": "Вы находитесь в темном лесу. Что вы хотите сделать?\n1) Идти глубже в лес\n2) Вернуться "
                       "на перекресток",
        "options": {"1": "deep_forest", "2": "start"},
    },
    "deep_forest": {
        "description": "Вы заблудились в лесу. Что делать?\n1) Попытаться найти дорогу\n2) Вернуться откуда пришли",
        "options": {"1": "find_path", "2": "forest"},
    },
    "find_path": {
        "description": "Поздравляю, вы нашли дорогу и выбрались из леса!",
        "options": {},
    },
    "mountains": {
        "description": "Вы поднимаетесь в горы. Что вы видите?\n1) Водопад\n2) Пещера\n3) Вернуться на перекресток",
        "options": {"1": "waterfall", "2": "cave", "3": "start"},
    },
    "waterfall": {
        "description": "Вы находитесь у водопада. Ваши действия?\n1) Подойти ближе\n2) Вернуться в горы",
        "options": {"1": "approach_waterfall", "2": "mountains"},
    },
    "approach_waterfall": {
        "description": "Ого, это волшебный водопад! Вы получили волшебные силы и покинули горы.",
        "options": {},
    },
    "cave": {
        "description": "Вы вошли в пещеру. Что делать дальше?\n1) Исследовать глубже\n2) Выйти из пещеры",
        "options": {"1": "explore_cave", "2": "mountains"},
    },
    "explore_cave": {
        "description": "Увы, вас здесь поджидал медведь. Вы проиграли!",
        "options": {},
    },
    "village": {
        "description": "Вы пришли в деревню. Жители рады вас видеть. Что вы хотите сделать?\n1) Поговорить с "
                       "жителями\n2) Покинуть деревню",
        "options": {"1": "talk_to_villagers", "2": "start"},
    },
    "talk_to_villagers": {
        "description": "Жители рассказали вам много интересных историй. Вы провели отличное время в деревне!",
        "options": {},
    },
}


def start_game(player, game_data):
    print("Приветствую вас в мире приключений!")
    while True:
        current_location = player["location"]
        print(game_data[current_location]["description"])
        options = game_data[current_location]["options"]
        if not options:
            print("Игра завершена.")
            break
        choice = input("Выберите вариант: ")
        if choice in options:
            player["location"] = options[choice]
        else:
            print("Неверный выбор. Попробуйте снова.")


def register_player():
    """Функция регистрации игрока.
    Возвращает словарь player = {"username": ..., "location": ...}
    с именем игрока и начальной локацией."""
    # Ваш код здесь

    return player

player = register_player()
start_game(player, game_data)
