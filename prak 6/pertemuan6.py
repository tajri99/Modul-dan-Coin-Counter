import sys
import cv2

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray
from convolusi import convolve


class ShowImage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image = None
        loadUi('praktikum6.ui', self)
        self.loadButton.clicked.connect(self.loadClicked)
        self.actionSobel.triggered.connect(self.SobelClicked)
        self.actionPrewitt.triggered.connect(self.prewitt)
        self.actioncannyedge.triggered.connect(self.canny)
        #self.actionsharpening_laplace.triggered.connect(self.sharpening)
        #self.actionMedian_Filter.triggered.connect(self.MedianClicked)
        #self.actionMax.triggered.connect(self.MaxClicked)
        #self.actionMin.triggered.connect(self.MinClicked)

    @pyqtSlot()
    def loadClicked(self):
        global flname
        flname = 'gambar/eye.jpg'
        self.loadImage(flname)

    @pyqtSlot()
    def loadImage(self, flname):
        self.image = cv2.imread(flname)
        self.displayImage(1)
        pixel = self.image
        print(pixel)

    @pyqtSlot()
    def SobelClicked(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        Sx = np.array([[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]])
        Sy = np.array([[-1, -2, -1],
                       [0, 0, 0],
                       [1, 2, 1]])
        img_x = convolve(img, Sx)
        img_y = convolve(img, Sy)
        img_out = np.sqrt(img_x * img_x + img_y * img_y)
        img_out = (img_out / np.max(img_out)) * 255
        pixel = img_out
        print(pixel)
        f = plt.figure()
        f.add_subplot(1, 2, 1)
        plt.imshow(img, cmap='gray', interpolation='bicubic')
        plt.title('citra asli')
        f.add_subplot(1, 2, 2)
        plt.imshow(img_out, cmap='gray', interpolation='bicubic')
        plt.title('citra sobel')
        plt.show(block=True)

    @pyqtSlot()
    def prewitt(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        Px = np.array([[-1, 0, 1],
                       [-1, 0, 1],
                       [-1, 0, 1]])
        Py = np.array([[-1, -1, -1],
                       [0, 0, 0],
                       [1, 1, 1]])
        img_x = convolve(image, Px)
        img_y = convolve(image, Py)
        img_out = np.sqrt((img_x * img_x) + (img_y * img_y))
        img_out = (img_out / np.max(img_out)) * 255
        pixel = img_out
        print(pixel)
        f = plt.figure()
        f.add_subplot(1, 2, 1)
        plt.imshow(image, cmap='gray', interpolation='bicubic')
        plt.title('citra asli')
        f.add_subplot(1, 2, 2)
        plt.imshow(img_out, cmap='gray', interpolation='bicubic')
        plt.title('citra prewitt')
        plt.show(block=True)

    @pyqtSlot()
    def canny(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gauss = (1.0 / 57) * np.array(
            [[0, 1, 2, 1, 0],
             [1, 3, 5, 3, 1],
             [2, 5, 9, 5, 2],
             [1, 3, 5, 3, 1],
             [0, 1, 2, 1, 0]])
        img_out = convolve(img, gauss)

        Sx = np.array([[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]])
        Sy = np.array([[-1, -2, -1],
                       [0, 0, 0],
                       [1, 2, 1]])
        img_x = convolve(img_out, Sx)
        img_y = convolve(img_out, Sy)
        theta = np.arctan2(img_y, img_x)
        angle = theta * 180. / np.pi
        angle[angle < 0] += 180
        H, W = img.shape
        Z = np.zeros((H, W), dtype=np.int32)
        for i in range(1, H - 1):
            for j in range(1, W - 1):
                try:
                    q = 255
                    r = 255
                    # angle 0
                    if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                        q = img_out[i, j + 1]
                        r = img_out[i, j - 1]
                    # angle 45
                    elif (22.5 <= angle[i, j] < 67.5):
                        q = img_out[i + 1, j - 1]
                        r = img_out[i - 1, j + 1]
                    # angle 90
                    elif (67.5 <= angle[i, j] < 112.5):
                        q = img_out[i + 1, j]
                        r = img_out[i - 1, j]
                    # angle 135
                    elif (112.5 <= angle[i, j] < 157.5):
                        q = img_out[i - 1, j - 1]
                        r = img_out[i + 1, j + 1]
                    if (img_out[i, j] >= q) and (img_out[i, j] >= r):
                        Z[i, j] = img_out[i, j]
                    else:
                        Z[i, j] = 0

                except IndexError as e:
                    pass
        img_N = Z.astype("uint8")
        weak = 100
        strong = 200
        for i in np.arange(H):
            for j in np.arange(W):
                a = img_N.item(i, j)
                if (a > weak):
                    b = weak
                    if (a > strong):
                        b = 255
                else:
                    b = 0
                img_N.itemset((i, j), b)
        img_H1 = img_N.astype("uint8")
        cv2.imshow('histeris 1', img_H1)
        strong = 255
        for i in range(1, H - 1):
            for j in range(1, W - 1):
                if (img_H1[i, j] == weak):
                    try:
                        if ((img_H1[i + 1, j - 1] == strong) or (img_H1[i + 1, j] == strong) or
                                (img_H1[i + 1, j + 1] == strong) or (img_H1[i, j - 1] == strong) or
                                (img_H1[i, j + 1] == strong) or (img_H1[i - 1, j - 1] == strong) or
                                (img_H1[i - 1, j] == strong) or (img_H1[i - 1, j + 1] == strong)):
                            img_H1[i, j] = strong
                        else:
                            img_H1[i, j] = 0
                    except IndexError as e:
                        pass
        img_H2 = img_H1.astype("uint8")
        cv2.imshow('histeris 2', img_H2)
        #f = plt.figure()
        #f.add_subplot(1, 3, 1)
        #plt.imshow(img, cmap='gray')
        #plt.title('citra asli')
        #f.add_subplot(1, 3, 2)
        #plt.imshow(img_H1, cmap='gray')
       # plt.title('Hyterisis 1')
        #f.add_subplot(1, 3, 3)
        #plt.imshow(img_H2, cmap='gray')
        #plt.title('canny edge lengkap')
        #plt.show(block=True)

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
