from PIL import Image

img = Image.open("images/image_1.png").convert("L")     # конвертируем в черно-белый формат

# img.show()

# Обрезаем изображение
# im.crop((left, upper, right, lower))
# left, upper - координаты верхнего левого угла
# right, lower - координаты нижнего правого угла

# обрежем изображение по координатам углов (40, 30) и (60, 50)
# img.crop((40, 30, 60, 50)).show()

# # Рисуем на изображении
from PIL import ImageDraw

draw = ImageDraw.Draw(img)

# Рисуем линию
# ImageDraw.Draw.line(xy, fill=None, width=0, joint=None)
# xy – координаты начала и конца линии
# fill – цвет линии
# width – толщина линии
# joint – тип соединения линий. Возможные значения: “curve”, “none”, “miter”, “round”, “bevel”.

# w, h = img.size
# draw.line((0, 0, w, h), fill=0)
# draw.line((0, h, w, 0), fill=255, width=5)
# img.show()


# Рисуем прямоугольник, но можно и многоугольник, добавляя по 2 координаты для новой точки
# ImageDraw.Draw.rectangle(xy, fill=None, outline=None, width=0)
# xy – координаты верхнего левого и нижнего правого угла прямоугольника
# fill – цвет заливки
# outline – цвет границы
# width – толщина границы

img = Image.open("images/Spectrogram_of_violin.png").convert("L")
draw = ImageDraw.Draw(img)
# draw.rectangle((20, 0, 80, 40), fill=0)
# img.show()
# draw.rectangle((40, 20, 80, 70), outline=128, width=3)
# img.show()

# рисуем круг
# draw.ellipse((20, 20, 80, 80), fill=0)
# img.show()


# Рисуем текст

# ImageDraw.Draw.text(xy, text, fill=None, font=None, anchor=None, spacing=0, align="left",
#                     language=None, stroke_width=0, stroke_fill=None)
# xy – координаты верхнего левого угла текста
# text – текст
# fill – цвет текста
# font – шрифт
# anchor – определяет как координаты xy будут интерпретироваться. Если anchor = None, то координаты xy будут интерпретироваться как координаты левого верхнего угла текста. Если anchor = “mm”, то координаты xy будут интерпретироваться как координаты центра текста.
# spacing – межстрочный интервал
# align – выравнивание текста. Возможные значения: “left”, “center”, “right”
# language – язык текста (например, “ru”)
# stroke_width – толщина обводки текста
# stroke_fill – цвет обводки текста

# можно загрузить шрифт из файла с помощью ImageFont.truetype и указать его в параметре font
from PIL import ImageFont
font = ImageFont.truetype("fonts/ofont.ru_Raydis.ttf", size=30)

# draw.text((20, 10), 'Helolo привет!', fill=0, font=font, stroke_fill=255, stroke_width=2)
draw.multiline_text((20, 10), 'Trololo,\nпривет чувак!', fill=0, font=font, stroke_fill=255, stroke_width=2)
# img.resize((400, 400)).show()


# можно нарисовать текст с обводкой с помощью stroke_width и stroke_fill


# можно написать текст в несколько строк c draw.multiline_text
# draw.multiline_text((20, 10), 'Trololo,\nпривет чувак!', fill=0, font=font, stroke_fill=255, stroke_width=2)
# img.show()


# # Задание 2
# # Подпиши мем и сохрани его
# meme = Image.open("hlebushek.png")
# meme.show()
#
#
# _________________________________________________________________
# Попиксельное изменение изображения
# _________________________________________________________________

# получение цвета пикселя по координатам
# Image.getpixel((x, y))
# x, y – координаты пикселя

img = Image.open("images/Spectrogram_of_violin.png").convert("L")
# print(img.getpixel((0, 0)))

# изменение цвета пикселя по координатам
# Image.putpixel((x, y), color)
# x, y – координаты пикселя

# img.putpixel((0, 0), 255)
# img.show()


# Поменяем цвета на изображении

w, h = img.size

# Делаем выстоту внешним циклом - чтобы отпринтовать яркость пикселей в соответствии с располжением картинки (снизу вверх).
for j in range(h): # проходимся по высоте картинки - по каждой строке.
    for i in range(w): # проходимся по ширине - по каждому пикселю в строке.
        # получаем цвет
        pixel = img.getpixel((i, j))
        print(pixel, end=' ')

        # как-либо меняем цвет, например инвертируем цвет чб картинки
        # new_pixel = 255 - pixel
        # img.putpixel((i, j), new_pixel)

        # можно обрабатывать по условиям (условия могут быть сложные)
        if i % 20 == 0:
            new_pixel = 0

            # сохраняем пиксель обратно
            img.putpixel((i, j), new_pixel)
    print()

img.show()
