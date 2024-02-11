from PIL import Image, ImageFilter
import os

class ImageEditor:

    def __init__(self, filename):
        self.filename = filename
        self.original = Image.open(filename)
        self.changed = []

    def do_bw(self):
        gray = self.original.convert("L")
        self.changed.append(gray)
        gray.save(f"{os.path.splitext(self.filename)[0]}_L.png")

    def do_blur(self, radius=5):
        blurred = self.original.filter(ImageFilter.GaussianBlur(radius=radius))
        self.changed.append(blurred)
        blurred.save(f"{os.path.splitext(self.filename)[0]}_blurred.png")

    def do_rotate(self):
        rotated = self.original.transpose(Image.ROTATE_90)
        self.changed.append(rotated)
        rotated.save(f"{os.path.splitext(self.filename)[0]}_rotated.png")


PATH = os.path.dirname(__file__) + os.sep
image = 'mongoose.png'

image_editor = ImageEditor(PATH + image)
image_editor.do_bw()
image_editor.do_blur()
image_editor.do_rotate()

# for image in image_editor.changed:
#     image.show()
