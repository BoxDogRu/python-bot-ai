from PIL import Image


class Filter:
    def apply_to_pixel(self, pixel: int) -> int:
        raise NotImplementedError()

    def apply_to_image(self, img: Image.Image) -> Image.Image:
        for j in range(img.height):
            for i in range(img.width):
                pixel = img.getpixel((i, j))
                new_pixel = self.apply_to_pixel(pixel)
                img.putpixel((i, j), new_pixel)
        return img


class BrightFilter(Filter):
    def apply_to_pixel(self, pixel: int) -> int:
        new_pixel = min(pixel + 100, 255)
        return new_pixel


class DarkFilter(Filter):
    def apply_to_pixel(self, pixel: int) -> int:
        pass


class InverseFilter(Filter):
    def apply_to_pixel(self, pixel: int) -> int:
        pass

