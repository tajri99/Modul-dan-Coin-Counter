import math
import sys

import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
import numpy as np
from matplotlib import pyplot as plt


class ShowImage(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi('prak_3.ui', self)
        self.image = None
        # button
        self.loadButton.clicked.connect(self.loadClicked)
        self.saveButton.clicked.connect(self.saveClicked)
        # file menu bar
        self.actionLoad_Image.triggered.connect(self.loadClicked)
        self.actionSave_Image.triggered.connect(self.saveClicked)
        self.actiontranslasi.triggered.connect(self.imageTranslation)

    @pyqtSlot()
    def loadClicked(self):
        # flname, filter = QFileDialog.getOpenFileName(self, 'OpenFile', 'D:\\', "Image Files (*.jpg)")
        # if flname:
        #     self.loadImage(flname)
        # else:
        #     print('invalid image')

        # static image
        global flname
        flname = 'gambar/anjing.jpg'
        self.loadImage(flname)

    @pyqtSlot()
    def loadImage(self, flname):
        self.image = cv2.imread(flname, cv2.IMREAD_COLOR)
        self.displayImage(1)

    @pyqtSlot()
    def saveClicked(self):
        flname, filter = QFileDialog.getSaveFileName(self, 'Save File', 'D:\\', "Image Files (*.jpg)")
        if flname:
            cv2.imwrite(flname, self.image)
        else:
            print('Error')

    @pyqtSlot()
    def imageTranslation(self):
        h, w = self.image.shape[: 2]
        quarter_h, quarter_w = h/4, w/4
        T = np.float32([[1, 0, quarter_w], [0, 1, quarter_h]] )
        img = cv2.warpAffine(self.image, T, (w, h))
        self.image(img)
        self.displayImage(2)

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
            self.hasilLabel.setPixmap(QPixmap.fromImage(img))
            self.hasilLabel.setAlignment(QtCore.Qt.AlignHCenter
                                         | QtCore.Qt.AlignVCenter)
            self.hasilLabel.setScaledContents(True)