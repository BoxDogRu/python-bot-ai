from filters import BrightFilter, DarkFilter, InverseFilter
from filters import BlackAndWhiteFilter, RedFilter
from PIL import Image
import os


def main():
    filter_names = [
        "Увеличить яркость",
        "Уменьшить яркость",
        "Инверсия",
    ]
    filters = [
        BrightFilter(), # BlackAndWhiteFilter(), RedFilter(),
        DarkFilter(),
        InverseFilter(),
    ]

    print("Добро пожаловать в консольный фоторедактор.")
    is_finished = False
    while not is_finished:
        # спрашиваем путь к файлу
        path = input("Введите путь к файлу: ")

        # проверяем ввод
        while not os.path.exists(path):
            path = input("Файл не найден. Попробуйте ещё раз: ")

        # открываем изображение и на всякий случай преобразуем его в L, чтобы сделать чёрно-белым
        img = Image.open(path).convert("L")     # обращаем внимание, в какой формат конвертируем

        print("Какой фильтр вы хотите применить?")
        for i in range(len(filter_names)):
            print(f"{i} - {filter_names[i]}")

        # запрашиваем номер фильтра
        choice = input("Выберите фильтр (введите номер): ")

        # проверяем ввод
        while not choice.isdigit() or int(choice) >= len(filters):
            choice = input("Некорректный ввод. Попробуйте ещё раз: ")

        # применяем фильтр
        filt = filters[int(choice)]
        img = filt.apply_to_image(img)

        # спрашиваем куда сохранить результат
        save_path = input("Куда сохранить: ")

        # сохраняем
        img.save(save_path)

        # спрашиваем, хотим ли повторить
        answer = input("Ещё раз? (да/нет): ").lower()

        # проверяем ввод
        while answer != "да" and answer != "нет":
            answer = input("Некорректный ввод. Попробуйте ещё раз: ").lower()
        is_finished = answer == "нет"


if __name__ == "__main__":
    main()
