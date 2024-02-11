from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QImage
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
        self.saved_image_path = None

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
        self.image = self.image.transpose(Image.ROTATE_90)
        self.showRedactedImage()

    def RightImage(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.showRedactedImage()

    def MirrorImage(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.showRedactedImage()

    def SharpImage(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.showRedactedImage()

    def ImageGray(self):
        self.image = self.image.convert("L")
        self.showRedactedImage()

    def SaveImage(self):
        if self.saved_image_path:
            QMessageBox.warning(window, 'Предупреждение', 'Изображение уже было сохранено')
            return
        unique_filename = str(uuid.uuid4()) + '.png'
        self.saved_image_path = os.path.join(PATH, self.foldername, unique_filename)
        self.image.save(self.saved_image_path)
        QMessageBox.information(window, 'Информация', 'Изображение сохранено')

    def showRedactedImage(self):
        lb_image.hide()
        image_data = self.image.convert("RGBA").tobytes("raw", "RGBA")
        qimage = QImage(image_data, self.image.size[0], self.image.size[1], QImage.Format_RGBA8888)
        pixmapimage = QPixmap.fromImage(qimage)
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
    
    list_images.clear()
    
    for file in list_image_files:
        list_images.addItem(file)
    print(workdir)

app = QApplication([])

window = QWidget()

mongoose = ImageProcessor(PATH + "mongoose.png", "modified") 

window.resize(800, 600)

folder_btn = QPushButton('Выбрать папку')
folder_btn.setIcon(QIcon(PATH + 'folder_icon.png')) 
list_images = QListWidget() 

lb_image = QLabel('Изображение')

left_btn = QPushButton("Повернуть влево")
left_btn.setIcon(QIcon(PATH + 'rotate_left_icon.png')) # Add rotate left icon
right_btn = QPushButton("Повернуть вправо")
right_btn.setIcon(QIcon(PATH + 'rotate_right_icon.png')) # Add rotate right icon
mirror_btn = QPushButton("Отзеркалить")
mirror_btn.setIcon(QIcon(PATH + 'mirror_icon.png')) # Add mirror icon
sharp_btn = QPushButton("Острота")
sharp_btn.setIcon(QIcon(PATH + 'sharpen_icon.png')) # Add sharpen icon
L_btn = QPushButton("Ч/Б")
L_btn.setIcon(QIcon(PATH + 'grayscale_icon.png')) # Add grayscale icon

save_btn = QPushButton("Сохранить")
save_btn.setIcon(QIcon(PATH + 'save_icon.png')) # Add save icon

workdir = None

folder_btn.clicked.connect(chooseWorkdir)
left_btn.clicked.connect(mongoose.LeftImage)
right_btn.clicked.connect(mongoose.RightImage)
mirror_btn.clicked.connect(mongoose.MirrorImage)
sharp_btn.clicked.connect(mongoose.SharpImage)
L_btn.clicked.connect(mongoose.ImageGray)
save_btn.clicked.connect(mongoose.SaveImage)

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
control_panel_layout.addWidget(save_btn)

main_layout.addLayout(image_list_layout, 20)
main_layout.addLayout(control_panel_layout, 80)

window.setLayout(main_layout)

# Adding styles
window.setStyleSheet("""
    QWidget {
        border: 2px solid #354152;
        border-radius: 10px;
        background-color: #f0f0f0;
    }
    
    QPushButton {
        border: none;
        border-radius: 5px;
        background-color: #5e6c84;
        color: white;
        padding: 8px 16px;
    }

    QPushButton:hover {
        background-color: #7289da;
    }

    QListWidget {
        border: 2px solid #354152;
        border-radius: 5px;
    }

    QLabel {
        border: 2px solid #354152;
        border-radius: 5px;
        background-color: white;
    }
""")

window.show()

app.exec()
