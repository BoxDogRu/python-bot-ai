from filters import BlueFilter, GreenFilter, InverseFilter, RedFilter
from PIL import Image


def main():
    filter_names = [
        "Красный фильтр",
        "Зелёный фильтр",
        "Синий фильтр",
        "Инверсия",
    ]
    filters = [
        RedFilter(),
        GreenFilter(),
        BlueFilter(),
        InverseFilter(),
    ]

    print("Добро пожаловать в консольный фоторедактор.")
    is_finished = False
    while not is_finished:
        # путь к файлу
        path = input("Введите путь к файлу: ")

        # открываем изображение и на всякий случай преобразуем его в RGB - чтобы работало с png и gif
        img = Image.open(path).convert("RGB")

        print("Какой фильтр вы хотите применить?")
        for i in range(len(filter_names)):
            print(f"{i} - {filter_names[i]}")

        # запрашиваем номер фильтра
        choice = input("Выберите фильтр (введите номер): ")

        # если нажали 1 - применяем градации серого
        filt = filters[int(choice)]
        img = filt.apply_to_image(img)

        # спрашиваем куда сохранить результат
        save_path = input("Куда сохранить: ")

        # сохраняем
        img.save(save_path)

        is_finished = input("Ещё раз? (да/нет): ").lower() == "нет"


if __name__ == "__main__":
    main()
