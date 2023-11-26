from PIL import Image
from filters import BrightFilter, DarkFilter, InverseFilter
import os


def main():
    filters = {
        '1': {
            'name': 'Bright Filter',
            'description': 'Увеличивать яркость',
            "class": BrightFilter()
        },
        '2': {
            'name': 'Dark Filter',
            'description': 'Уменьшить яркость',
            "class": DarkFilter()
        },
        '3': {
            'name': 'Inverse Filter',
            'description': 'Инверсия',
            "class": InverseFilter()
        },
        '0': {
            'name': 'Выход из программы',
            'description': 'Спасибо за участие.'
        },
    }

    while True:
        print('Добро пожаловать в консольный фоторедактор!')

        path = input('Введите путь к файлу: ')

        while not os.path.exists(path):
            path = input('Файл не найден. Повторите еще раз: ')

        img = Image.open(path).convert('L')
        print(type(img))

        # основное меню
        for number, filter in filters.items():
            if int(number):
                print(f"{number} - фильтр {filter['name']}")
            else:
                print(f"{number} - {filter['name']}")

        choose = input('Введите номер команды - выберите нужный фильтр. Или 0 для выхода.\n')

        # обработка неправильного ввода
        if choose not in filters:
            print("Команд не распознана. Повторите ввод.")

        # выход из программы
        elif not int(choose):
            exit(filters[choose]['description'])

        # меню текущего фильтра
        else:
            filter = filters[choose]
            print(f"Фильтр {filter['name']} к вашим услугам.")
            print(f"{filter['description']}")
            img = filter["class"].apply_to_image(img)

            save_path = input('Куда сохранить: ')

            img.save(save_path)

            # код ниже требует дополнительного тестирования, не может считаться финальным вариантом
            repeat = input('Еще раз? (да/нет).').lower()

            while repeat in ['да', 'нет']:
                if repeat == 'да':
                    break
                else:
                    exit(filters[choose]['description'])
            else:
                repeat = input('Еще раз? (да/нет).').lower()


if __name__ == '__main__':
    main()
