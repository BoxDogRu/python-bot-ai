class BrightFilter:
    def apply_to_image(self, img):
        print('apply BrightFilter')
        return img


class DarkFilter:
    pass


class InverseFilter:
    pass


"""
img = Image.open('meme.jpg').convert('L')
img = img.resize((int(img.width * 0.5), int(img.height * 0.5)))
img.show()

for j in range(img.height):
    for i in range(img.width):
        pixel = img.getpixel((i, j))
        new_pixel = max(100, pixel)
        img.putpixel((i, j), new_pixel)

img.show()
"""
