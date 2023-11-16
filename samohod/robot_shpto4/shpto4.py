"""
Описание технологического процесса

- перед ШПТО-4 по конвейеру едут поддоны разного размера с добытой горной породой
- в породе может быть редкий, ценный элемент, но могут встречаться радиоактивные вкрапления, всё остальное — пустая порода
- извлекать ценный элемент трудоёмко, если его доля в породе мала, это экономически невыгодно
- работать с радиацией опасно, но на комбинате есть «грязный цех» — там можно извлечь ценный элемент без риска облучения, но это будет ещё дороже из-за всех мер предосторожности

- задача робота — принять решение по отправке содержимого каждого поддона. Он может отправить его:
-- в отвал — если ценного элемента и опасных вкраплений нет или мало (меньше 10% и 15% соответственно),
-- в «грязный цех» — если опасной составляющей немало (больше 15%), но ценной достаточно, чтобы окупить извлечение в грязном цехе (больше 25%),
-- в могильник для опасных отходов, если радиоактивных вкраплений много (больше 15%), а ценности недостаточно для покрытия стоимости извлечения в грязном цехе (меньше 25%),
-- в «чистый цех», если радиации нет (меньше 15%), а ценность есть (больше 10%).

- ШПТО-4 своим чёрно-белым зрением смотрит в ящики, и вот как это выглядит для него:
-- ценный элемент самый тёмный,
-- пустая порода — основная серая масса,
-- радиоактивные вкрапления светятся, их яркость выше всего.

- на роботе есть «крутилки», которые настраивают пороговые значения в процентах:
-- доля ценного элемента в чистом образце, выше которой извлекать его выгодно,
-- доля ценного элемента в грязном образце, выше которой извлекать его всё еще выгодно, уже в грязном цехе,
-- доля радиоактивных примесей, делающая образец опасным.

- соотнеся увиденное и свои настройки, ШПТО-4 отправляет на пульт один из четырёх сигналов, соответствующих принятому решению:
-- И ради такого меня посылали? Спасибо, не надо. Отправлю это в отвал
-- В этом что-то есть. Дам ему шанс в грязном цехе
-- В этом что-то есть. Но мне здоровье дороже. Отвезу-ка в могильник!
-- А вы спрашиваете, ради чего я корячусь тут… Ради такого! Отвезу в чистый цех!
"""

# импортируем класс Image из PIL
from PIL import Image

# определяем пороговые значения яркости для "ценных" и "опасных" пикселей
valuable_threshold = 42
dangerous_threshold = 210

# определяем доли ценных и опасных пикселей
effective_safe_ratio = 0.1
effective_unsafe_ratio = 0.25
unsafe_ratio = 0.15

# будем проверять картинки одну за одной, выход из цикла сделаем внутри
while True:

    # запрашиваем у пользователя имя файла или команду "завершить"
    filename = input('Введите имя файла (с расширением) или "завершить": ')

    # отличаем команду от имени, если команда, выходим из цикла, завершая программу
    if filename.lower() == "завершить":
        break

    # иначе все основные действия
    else:
        # создаём объект типа Image, передав в метод open имя файла
        sample = Image.open(filename)

        # преобразуем изображение в градации серого
        sample = sample.convert('L')

        # контрольный показ текущего состояния картинки
        sample.show()

        # вычисляем и сохраняем количество пикселей в изображении
        num_pixels = sample.height * sample.width

        # вычисляем конкретные пороговые значения числа ценных и опасных пикселей
        effective_safe_threshold = num_pixels * effective_safe_ratio
        effective_unsafe_threshold = num_pixels * effective_unsafe_ratio
        unsafe_threshold = num_pixels * unsafe_ratio

        # заводим счётчики для ценных и опасных пикселей в изображении
        num_valuable = 0
        num_dangerous = 0

        # вложенным циклом обходим все пиксели изображения
        for x in range(sample.width):
            for y in range(sample.height):
                test_pixel = sample.getpixel((x,y))

                # проверяем, попадает ли яркость текущего пикселя в зону ценных или опасных
                # если попадает, увеличиваем соответствующий счетчик
                if test_pixel <= valuable_threshold:
                    num_valuable += 1
                elif test_pixel >= dangerous_threshold:
                    num_dangerous += 1

        # заводим переменную с сообщением о решении, помещаем туда сообщение по умолчанию
        # которое останется в ней, если далее не подставится другое
        resolution = "Почему-то решение не было принято, проверь код"

        # проверяем количества ценных и опасных пикселей по набору условий и обновляем сообщение о решении
        if num_valuable < effective_safe_threshold and num_dangerous < unsafe_threshold:
            resolution = "И ради такого меня посылали? Спасибо, не надо. Отправлю это в отвал"
        elif num_valuable > effective_unsafe_threshold and num_dangerous > unsafe_threshold:
            resolution = "В этом что-то есть. Дам ему шанс в грязном цехе"
        elif num_valuable < effective_unsafe_threshold and num_dangerous > unsafe_threshold:
            resolution = "В этом что-то есть. Но мне здоровье дороже. Отвезу-ка в могильник!"
        elif num_valuable > effective_safe_threshold and num_dangerous < unsafe_threshold:
            resolution = "А вы спрашиваете, ради чего я корячусь тут… Ради такого! Отвезу в чистый цех!"

        # отладочный вывод закомментирован
        print(f"Пикселей: {num_pixels}, плохих {num_dangerous} хороших {num_valuable}")

        # печатаем решение
        print(resolution)
