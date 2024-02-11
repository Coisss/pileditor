from PIL import Image, ImageFilter
import os

PATH = os.path.dirname(__file__) + os.sep

class ImageProcessor():

    def __init__(self, filename, foldername):
        self.filename = filename
        self.foldername = foldername
        self.image = None

    def load(self):
        self.image = Image.open(self.filename)
        self.image.show()

Image = ImageProcessor(PATH + "mongoose.png", "modified")
Image.load() 