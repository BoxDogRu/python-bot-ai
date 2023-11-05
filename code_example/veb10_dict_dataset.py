filters = {
    'Выход': 'Выход',
    'Caps фильтр': 'Фильтр, который "преобразует" все буквы в верхний регистр.',
    'Шифр Цезаря': 'Фильтр, который преобразует все буквы текста в нижний регистр.'
}


filters = {
    1: {
        'name': 'Caps фильтр',
        'description': 'Фильтр, который преобразует все буквы в верхний регистр.'
    },
    2: {
        'name': 'Lower фильтр',
        'description': 'Фильтр, который преобразует все буквы текста в нижний регистр.'
    }
}


def caps_filter(text):
    return text.upper()


def lower_filter(text):
    return text.lower()


filters = {
    1: {
        'name': 'Caps фильтр',
        'description': 'Фильтр, который преобразует все буквы в верхний регистр.',
        "function": caps_filter
    },
    2: {
        'name': 'Lower фильтр',
        'description': 'Фильтр, который преобразует все буквы текста в нижний регистр.',
        "function": lower_filter
    }
}