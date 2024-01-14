# Нужно знать: условные операторы, циклы, функции, классы, словари, чтение json файла, форматирование строк, lambda-функции
# Сложность: 8 из 10
# Добавлено: класс для игрока и локаций, чтение json файла
import json


class Player():
    """Класс игрока. Имеет имя и пол."""

    def __init__(self, id=None, name='', location=None, sex='ж'):
        self.id = id  # id игрока, понадобится для бота
        self.name = name  # Имя игрока
        self.location = location  # Текущая локация игрока
        self.time_late = 0  # Время, на которое игрок опоздал на урок
        self.num_locations = 0  # Количество локаций, посещённых игроком
        self.sex = sex  # Пол игрока
        if 'м' in self.sex.lower():
            self.ending = ''  # Окончание глаголов для мужского пола
        elif 'ж' in self.sex.lower():
            self.ending = 'а'  # Окончание глаголов для женского пола

    def set_sex(self, sex):
        self.sex = sex  # Пол игрока
        if 'м' in self.sex.lower():
            self.ending = ''  # Окончание глаголов для мужского пола
        elif 'ж' in self.sex.lower():
            self.ending = 'а'  # Окончание глаголов для женского пола

    def __str__(self):
        return f'Имя: {self.name}, id: {self.id}, sex: {self.sex}'

class Location():
    """Класс локации. Имеет название, описание и варианты действий."""

    def __init__(self, name, description, actions):
        self.name = name  # Название локации, уникальный идентификатор
        self.description = description  # Описание локации, выводится при входе в неё
        self.actions = actions  # Словарь вида {текст_действия: следующая_локация} со всеми действиями в локации


class Game():
    """Класс игры. Задаётся игрок и json-файл с локациями."""

    def __init__(self, player, json_file):
        self.player = player  # Объект класса Player
        self.process_input = lambda x: str(x). \
            replace('{ending}', self.player.ending). \
            replace('{name}', self.player.name)
        self.process_output = lambda x: str(x).replace('{time}', str(self.player.time_late))
        self.locations = parse_json(json_file, self.process_input) # Словарь вида {название_локации: объект_класса_Location}
        self.player.location = self.locations['start']  # Начальная локация игрока
        self.output = lambda x: print(self.process_output(x))  # Функция вывода текста

    def get_actions(self):
        """Возвращает список действий в текущей локации."""
        actions = self.player.location.actions.keys()
        return list(actions)

    def output_actions(self):
        """Выводит варианты действий."""
        self.output("Варианты действий:")
        for choice, action in enumerate(self.get_actions(), 1):
            self.output(f'{choice}) {action}')

    def take_an_action(self, action):
        """Делает выбранное действие и обновляет аттрибуты игрока."""

        self.player.num_locations += 1
        self.player.time_late += 3

        if action.isdigit():
            action = self.get_actions()[int(choice) - 1]
        self.player.location = self.locations[self.player.location.actions[action]]

        if self.player.location.name == 'start':
            self.player.num_locations = 0
            self.player.time_late = 0
        elif self.player.location.name == 'kabinet223' and self.player.num_locations > 4:
            self.player.location = self.locations['lose-late']


def parse_json(filename, process_str=lambda x: x):
    """Читает json файл с описаниям локаций и возвращает словарь объектов класса Location"""
    file = open(filename, encoding='utf-8').read()
    file = process_str(file)
    file = json.loads(file)
    all_locations = {}
    for location_name in file['locations']:
        location = file['locations'][location_name]
        all_locations[location_name] = Location(location_name, location['description'], location['actions'])

    return all_locations


if __name__ == '__main__':
    player = Player(name='Иван', sex='м')
    game = Game(player, 'locations.json')
    while game.player.location.name != "exit":
        game.output(game.player.location.description)
        game.output_actions()
        choice = input()
        game.take_an_action(choice)
