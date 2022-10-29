import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class ShowImage(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi('prak4.ui', self)
        self.image = None
        # button
        self.loadButton.clicked.connect(self.loadClicked)
        self.loadButton_2.clicked.connect(self.loadClicked_2)
        # file menu bar
        self.actionLoad_Image.triggered.connect(self.loadClicked)
        self.actionaritmatik.triggered.connect(self.aritmatika_CitraClicked)
        self.actionboolean.triggered.connect(self.booleanClicked)



    @pyqtSlot()
    def loadClicked(self):
        global flname1
        flname1 = 'gambar/earth.jpg'
        self.loadImage(flname1)
        pixel = self.image
        print(pixel)


    @pyqtSlot()
    def loadClicked_2(self):
        global flname2
        flname2 = 'gambar/beach.jpg'
        self.loadImage2(flname2)
        pixel = self.image
        print(pixel)

    @pyqtSlot()
    def loadImage(self, flname1):
        self.image = cv2.imread(flname1, cv2.IMREAD_COLOR)
        self.displayImage(1)


    def loadImage2(self, flname2):
        self.image = cv2.imread(flname2, cv2.IMREAD_COLOR)
        self.displayImage(2)


    @pyqtSlot()
    def aritmatika_CitraClicked(self):
        img1 = cv2.imread('gambar/earth.jpg', 1)
        img2 = cv2.imread('gambar/beach.jpg', 1)
        add_img = img1 + img2
        subtract = img1 - img2
        mul = img1 * img2
        div = img1 / img2
        cv2.imshow('Add', add_img)
        cv2.imshow('Subtraction', subtract)
        cv2.imshow('Multiply', mul)
        cv2.imshow('Divide', div)

    @pyqtSlot()
    def booleanClicked(self):
        img1 = cv2.imread('gambar/earth.jpg', 0)
        img2 = cv2.imread('gambar/beach.jpg', 0)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        op_and = cv2.bitwise_and(img1, img2)
        op_or = cv2.bitwise_or(img2, img2)
        op_xor = cv2.bitwise_xor(img1, img2)
        cv2.imshow('And', op_and)
        cv2.imshow('OR', op_or)
        cv2.imshow('XOR', op_xor)
        print(op_xor)

    def displayImage(self, windows=1):
        qformat = QImage.Format_Indexed8

        if len(self.image.shape) == 3:
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(self.image,
                     self.image.shape[1],
                     self.image.shape[0],
                     self.image.strides[0],
                     qformat)
        img = img.rgbSwapped()

        if windows == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(img))
            self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter
                                       | QtCore.Qt.AlignVCenter)
            self.imgLabel.setScaledContents(True)

        if windows == 2:
            self.imagelabel.setPixmap(QPixmap.fromImage(img))
            self.imagelabel.setAlignment(QtCore.Qt.AlignHCenter
                                         | QtCore.Qt.AlignVCenter)
            self.imagelabel.setScaledContents(True)
