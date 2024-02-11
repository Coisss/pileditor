from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
import os
import uuid

workdir = None

PATH = os.path.dirname(__file__) + os.sep

image_extensions = ['jpg', 'jpeg', 'png', 'bmp', 'webp', 'heic']

class ImageProcessor():

    def __init__(self, filename, foldername):
        self.filename = filename
        self.foldername = foldername
        self.image = None

    def load(self):
        self.image = Image.open(self.filename)
        self.image.show()

    def showImage(self, item_name):
       lb_image.hide()
       pixmapimage = QPixmap(workdir + os.sep + item_name.text())
       w, h = lb_image.width(), lb_image.height()
       pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
       lb_image.setPixmap(pixmapimage)
       lb_image.show()
       self.image = Image.open(workdir + os.sep + item_name.text())
    
    def LeftImage(self):
        pic_left = self.image.transpose(Image.ROTATE_90)
        unique_filename = str(uuid.uuid4()) + '.png'
        NewPATH = os.path.join(PATH, self.foldername, unique_filename)
        pic_left.save(NewPATH)
        self.showRedactedImage(NewPATH)

    def RightImage(self):
        pic_right = self.image.transpose(Image.ROTATE_180)
        unique_filename = str(uuid.uuid4()) + '.png'
        NewPATH = os.path.join(PATH, self.foldername, unique_filename)
        pic_right.save(NewPATH)
        self.showRedactedImage(NewPATH)

    def MirrorImage(self):
        pic_mirror = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        unique_filename = str(uuid.uuid4()) + '.png'
        NewPATH = os.path.join(PATH, self.foldername, unique_filename)
        pic_mirror.save(NewPATH)
        self.showRedactedImage(NewPATH)

    def SharpImage(self):
        pic_sharp = self.image.filter(ImageFilter.BLUR)
        unique_filename = str(uuid.uuid4()) + '.png'
        NewPATH = os.path.join(PATH, self.foldername, unique_filename)
        pic_sharp.save(NewPATH)
        self.showRedactedImage(NewPATH)

    def ImageGray(self):
        pic_gray = self.image.convert("L")
        unique_filename = str(uuid.uuid4()) + '.png'
        NewPATH = os.path.join(PATH, self.foldername, unique_filename)
        pic_gray.save(NewPATH)
        self.showRedactedImage(NewPATH)

    def SaveImage(self, image):
        self


    def showRedactedImage(self, image_name):
       lb_image.hide()
       pixmapimage = QPixmap(image_name)
       w, h = lb_image.width(), lb_image.height()
       pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
       lb_image.setPixmap(pixmapimage)
       lb_image.show()

    

def filterImage(files, extensions):
    result = list()
    for file in files:
        r = file.split(".")
        if len(r) >= 2 and r[1] in extensions:
            result.append(file)
    return result


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    list_files = os.listdir(workdir)
    list_image_files = filterImage(list_files, image_extensions)
    for file in list_image_files:
        list_images.addItem(file)
    print(workdir)



app = QApplication([])

window = QWidget()

mongoose = ImageProcessor(PATH + "mongoose.png", "modified") 

window.resize(800, 600)

folder_btn = QPushButton('Папка')
list_images = QListWidget() # list widget images

lb_image = QLabel('Картинка')

left_btn = QPushButton("Влево")
right_btn = QPushButton("Вправо")
mirror_btn = QPushButton("Зеркало")
sharp_btn = QPushButton("Резкость")
L_btn = QPushButton("Ч/Б")

workdir = None

folder_btn.clicked.connect(chooseWorkdir)
left_btn.clicked.connect(mongoose.LeftImage)
right_btn.clicked.connect(mongoose.RightImage)
mirror_btn.clicked.connect(mongoose.MirrorImage)
sharp_btn.clicked.connect(mongoose.SharpImage)
L_btn.clicked.connect(mongoose.ImageGray)

list_images.itemClicked.connect(mongoose.showImage)

main_layout = QHBoxLayout()

image_list_layout = QVBoxLayout()

control_panel_layout = QVBoxLayout()
btn_layout = QHBoxLayout()

image_list_layout.addWidget(folder_btn)
image_list_layout.addWidget(list_images)

control_panel_layout.addWidget(lb_image)

btn_layout.addWidget(left_btn)
btn_layout.addWidget(right_btn)
btn_layout.addWidget(mirror_btn)
btn_layout.addWidget(sharp_btn)
btn_layout.addWidget(L_btn)

control_panel_layout.addLayout(btn_layout)

main_layout.addLayout(image_list_layout, 20)
main_layout.addLayout(control_panel_layout, 80)

window.setLayout(main_layout)

window.show()

app.exec()