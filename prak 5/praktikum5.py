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
        loadUi('praktikum5.ui', self)
        self.loadButton.clicked.connect(self.loadClicked)
        self.actionfiltering.triggered.connect(self.filteringClicked)
        self.actionmean.triggered.connect(self.MeanClicked)
        self.actiongauss_smoothing.triggered.connect(self.smoothing_gauss)
        self.actionsharpening_laplace.triggered.connect(self.sharpening)
        self.actionMedian_Filter.triggered.connect(self.MedianClicked)
        self.actionMax.triggered.connect(self.MaxClicked)
        self.actionMin.triggered.connect(self.MinClicked)

    @pyqtSlot()
    def loadClicked(self):
        global flname
        flname = 'gambar/elang.jpg'
        self.loadImage(flname)

    @pyqtSlot()
    def loadImage(self, flname):
        self.image = cv2.imread(flname)
        self.displayImage(1)
        #pixel = self.image
        #print(pixel)

    @pyqtSlot()
    def filteringClicked(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        kernel = np.array([[6, 0, -6],
                           [6, 1, -6],
                           [6, 0, -6]])
        img_out = convolve(image, kernel)
        pixel = img_out
        print(pixel)
        f = plt.figure()
        f.add_subplot(1, 2, 1)
        plt.imshow(image, cmap='gray', interpolation='bicubic')
        plt.title('citra asli')
        f.add_subplot(1, 2, 2)
        plt.imshow(img_out, cmap='gray', interpolation='bicubic')
        plt.title('citra hasil')
        plt.show(block=True)

    @pyqtSlot()
    def MeanClicked(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        mean = (1.0 / 9) * np.array(
            [[1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]])
        img_out = convolve(image, mean)
        pixel = img_out
        print(pixel)
        f = plt.figure()
        f.add_subplot(1, 2, 1)
        plt.imshow(image, cmap='gray', interpolation='bicubic')
        plt.title('citra asli')
        f.add_subplot(1, 2, 2)
        plt.imshow(img_out, cmap='gray', interpolation='bicubic')
        plt.title('citra hasil')
        plt.show(block=True)

    @pyqtSlot()
    def smoothing_gauss(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        print(image)
        gauss = (1.0 / 345) * np.array(
            [[1, 5, 7, 5, 1],
             [5, 20, 33, 20, 5],
             [7, 33, 55, 33, 7],
             [5, 20, 33, 20, 5],
             [1, 5, 7, 5, 1]])
        img_out = convolve(image, gauss)
        pixel = img_out
        print(pixel)
        f = plt.figure()
        f.add_subplot(1, 2, 1)
        plt.imshow(image, cmap='gray', interpolation='bicubic')
        plt.title('citra asli')
        f.add_subplot(1, 2, 2)
        plt.imshow(img_out, cmap='gray', interpolation='bicubic')
        plt.title('citra hasil')
        plt.show(block=True)

    @pyqtSlot()
    def sharpening(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        print(image)
        #laplace = np.array(
            #[[-1, -1, -1],
            #[-1, 8, -1],
            #[-1, -1, -1]])
        laplace = (1.0 / 16) * np.array(
                        [[0, 0, -1, 0, 0],
                        [0, -1, -2, -1, 0],
                        [-1, -2, 16, -2, -1],
                        [0, -1, -2, -1, 0],
                        [0, 0, -1, 0, 0]])
        img_out = convolve(image, laplace)
        pixel = img_out
        print(pixel)
        f = plt.figure()
        f.add_subplot(1, 2, 1)
        plt.imshow(image, cmap='gray', interpolation='bicubic')
        plt.title('citra asli')
        f.add_subplot(1, 2, 2)
        plt.imshow(img_out, cmap='gray', interpolation='bicubic')
        plt.title('citra hasil')
        plt.show(block=True)

    @pyqtSlot()
    def MedianClicked(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        print(img)
        img_out = img.copy()
        h, w = img.shape[:2]
        for i in np.arange(3, h - 3):
            for j in np.arange(3, w - 3):
                neighbors = []
                for k in np.arange(-3, 4):
                    for l in np.arange(-3, 4):
                        a = img.item(i + k, j + l)
                        neighbors.append(a)
                neighbors.sort()
                median = neighbors[24]
                b = median
                img_out.itemset((i, j), b)
        pixel = img_out
        print(pixel)
        f = plt.figure()
        f.add_subplot(1, 2, 1)
        plt.imshow(img, cmap='gray', interpolation='bicubic')
        plt.title('citra asli')
        f.add_subplot(1, 2, 2)
        plt.imshow(img_out, cmap='gray', interpolation='bicubic')
        plt.title('citra hasil')
        plt.show(block=True)

    @pyqtSlot()
    def MaxClicked(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        print(img)
        img_out = img.copy()
        h, w = img.shape[:2]
        for i in np.arange(1, h - 1):
            for j in np.arange(1, w - 1):
                max = 0
                for k in np.arange(-1, 2):
                    for l in np.arange(-1, 2):
                        a = img.item(i + k, j + l)
                        if a > max:
                            max = a
                            b = max
                img_out.itemset((i, j), b)
                pixel = img_out
                print(pixel)
        f = plt.figure()
        f.add_subplot(1, 2, 1)
        plt.imshow(img, cmap='gray', interpolation='bicubic')
        plt.title('citra asli')
        f.add_subplot(1, 2, 2)
        plt.imshow(img_out, cmap='gray', interpolation='bicubic')
        plt.title('citra hasil')
        plt.show(block=True)

    @pyqtSlot()
    def MinClicked(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        print(img)
        img_out = img.copy()
        h, w = img.shape[:2]
        for i in np.arange(1, h - 1):
            for j in np.arange(1, w - 1):
                min = 255
                for k in np.arange(-1, 2):
                    for l in np.arange(-1, 2):
                        a = img.item(i + k, j + l)
                        if a < min:
                            min = a
                            b = min
                img_out.itemset((i, j), b)

        pixel = img_out
        print(pixel)
        f = plt.figure()
        f.add_subplot(1, 2, 1)
        plt.imshow(img, cmap='gray', interpolation='bicubic')
        plt.title('citra asli')
        f.add_subplot(1, 2, 2)
        plt.imshow(img_out, cmap='gray', interpolation='bicubic')
        plt.title('citra hasil')
        plt.show(block=True)

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
