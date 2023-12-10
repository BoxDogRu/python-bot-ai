from PIL import Image
from math import exp, e
# from typing import Tuple

# код изменен под цветные фильтры, чб - не будут работать

class Filter:
    """
    Базовый класс для создания фильтров.
    """

    def apply_to_pixel(self, r: int, g: int, b: int) -> tuple[int, int, int]:
        """
        Применяет фильтр к одному пикселю.
        :param pixel: цвет пикселя
        :return: новый цвет пикселя
        """
        raise NotImplementedError()

    def apply_to_image(self, img: Image.Image) -> Image.Image:
        """
        Применяет фильтр к изображению.
        :param img: исходное изображение
        :return: новое изображение
        """
        for i in range(img.width):
            for j in range(img.height):
                # получаем цвет
                # pixel = img.getpixel((i, j))
                r, b, g = img.getpixel((i, j))

                # как-либо меняем цвет
                new_pixel = self.apply_to_pixel((r, b, g))

                # сохраняем пиксель обратно
                img.putpixel((i, j), new_pixel)
        return img


class BlackAndWhiteFilter(Filter):
    """
    Фильтр, который преобразует цветную картинку в черно-белую.
    """
    def apply_to_pixel(self, r: int, g: int, b: int):
        avg = (r + g + b) // 3
        return avg, avg, avg


class RedFilter(Filter):
    """
    Фильтр, который плавно усиляет красный.
    """
    def apply_to_pixel(self, r: int, g: int, b: int):
        r = int(exp(r / 255) / e * 255)
        return r, g, b


class BrightFilter(Filter):
    """
    Фильтр, который делает изображение ярче.
    """
    def apply_to_pixel(self, pixel: int) -> int:
        new_pixel = min(pixel + 100, 255)
        return new_pixel


class DarkFilter(Filter):
    """
    Фильтр, который делает изображение темнее.
    """
    def apply_to_pixel(self, pixel: int) -> int:
        new_pixel = max(pixel - 100, 0)
        return new_pixel


class InverseFilter(Filter):
    """
    Фильтр, который инвертирует изображение.
    """
    def apply_to_pixel(self, pixel: int) -> int:
        new_pixel = 255 - pixel
        return new_pixel
