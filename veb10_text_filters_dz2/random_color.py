import random


def random_color(text):
    """Окрашивает каждый символ текста в рандомный цвет."""
    for letter in text:
        num_fore = random.randint(30, 37)
        num_back = random.randint(40, 47)
        print("\033[", end='')
        if letter != ' ':
            print(f"{num_fore}m{letter}", end='')
        else:
            print(f"{num_back}m{letter}", end='')
        print("\033[0m", end='')
    print('\n')


# документ-строка
# help(random_color)
# print(random_color.__doc__)


def random_color2(text):
    result = ''
    for letter in text:
        num_fore = random.randint(30, 37)
        num_back = random.randint(40, 47)
        result += "\033["
        if letter != ' ':
            result += f"{num_fore}m{letter}"
        else:
            result += f"{num_back}m{letter}"
        result += "\033[0m"
    return result