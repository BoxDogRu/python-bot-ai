import math
from PIL import Image, ImageFilter, ImageOps
from random import randrange

class Filter:
    """
    Базовый класс для создания фильтров.
    """

    def apply_to_pixel(self, r: int, g: int, b: int) -> tuple[int, int, int]:
        # Этот метод нужно будет реализовать в новых классах.
        raise NotImplementedError

    def apply_to_image(self, img: Image.Image) -> Image.Image:
        # цикл по всем пикселям
        # img.width - ширина картинки
        # img.height - высота картинки
        for i in range(img.width):
            for j in range(img.height):
                # получаем цвет
                r, g, b = img.getpixel((i, j))

                # как-либо меняем цвет
                new_colors = self.apply_to_pixel(r, g, b)

                # сохраняем пиксель обратно
                img.putpixel((i, j), new_colors)
        return img

# Фильтры по умолчанию
class RedFilter(Filter):
    def apply_to_pixel(self, r: int, g: int, b: int) -> tuple[int, int, int]:
        # плавно усиляет красный
        r = int(math.exp(r / 255) / math.e * 255)
        return r, g, b


class GreenFilter(Filter):
    def apply_to_pixel(self, r: int, g: int, b: int) -> tuple[int, int, int]:
        # плавно усиляет зелёный
        g = int(math.exp(g / 255) / math.e * 255)
        return r, g, b


class BlueFilter(Filter):
    def apply_to_pixel(self, r: int, g: int, b: int) -> tuple[int, int, int]:
        # плавно усиляет синий
        b = int(math.exp(b / 255) / math.e * 255)
        return r, g, b


class InverseFilter(Filter):
    def apply_to_pixel(self, r: int, g: int, b: int) -> tuple[int, int, int]:
        # инвертирует цвета
        result = []
        for color in (r, g, b):
            result.append(int((1 - math.exp(color / 255) / math.e) * 255))
        return tuple(result)


# Фильтры от участников команды

class SopolevRandomFilter(Filter):

    def apply_to_image(self, img):
        img = img.convert("RGB")
        x, y = img.size
        for i in range(x):
            for e in range(y):
                r, g, b = img.getpixel((i, e))
                r, g, b = (max(0, r-randrange(0, 255)),
                           max(0, g-randrange(0, 255)),
                           max(0, b-randrange(0, 255)))
                img.putpixel((i, e), (r, g, b))
        return img


class DolgovBlurFilter(Filter):
    def apply_to_image(self, image):
        blurred_image = image.filter(ImageFilter.BLUR)
        return blurred_image


class BekrenevReversFilter(Filter):
    def apply_to_image(self, img):
        img = img.convert("L")
        pixel_values = list(img.getdata())
        transformed_pixel_values = [255 - value for value in pixel_values]
        img.putdata(transformed_pixel_values)
        return img


class KirpichevRedFilter(Filter):
    def apply_to_image(self, image):
        pixels = list(image.getdata())
        new_pixels = [(pixel[0], 0, 0) for pixel in pixels]
        filtered_image = Image.new(image.mode, image.size)
        filtered_image.putdata(new_pixels)
        return filtered_image


class OrlovGreenFilter(Filter):
    def apply_to_image(self, image):
        return ImageOps.colorize(image.convert("L"), "#00ff00", "#000000")


class OrlovGreenFilter(Filter):
    def apply_to_image(self, image):
        return ImageOps.colorize(image.convert("L"), "#00ff00", "#000000")


class BuninEdgesFilter(Filter):
    def apply_to_image(self, image):
        img_gray = image.convert("L")
        img_gray_smooth = img_gray.filter(ImageFilter.SMOOTH)
        emboss = img_gray_smooth.filter(ImageFilter.EMBOSS)
        return emboss
