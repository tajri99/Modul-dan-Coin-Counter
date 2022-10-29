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

        loadUi('UI/a4.ui', self)
        self.image = None
        # button
        self.loadButton.clicked.connect(self.loadClicked)
        self.saveButton.clicked.connect(self.saveClicked)
        # file menu bar
        self.actionLoad_Image.triggered.connect(self.loadClicked)
        self.actionSave_Image.triggered.connect(self.saveClicked)
        # operasi titik menu bar
        self.actionGrayscale.triggered.connect(self.grayClicked)
        self.actionBrightness.triggered.connect(self.brightnessClicked)
        self.actionContrast.triggered.connect(self.contrastClicked)
        self.actionContrast_Stretching.triggered.connect(self.stretchingContrastClicked)
        self.actionNegative.triggered.connect(self.negativeClicked)
        self.actionBiner.triggered.connect(self.binerClicked)
        self.actionGray_Histogram.triggered.connect(self.GrayHistogramClicked)
        self.actionRGB_Histogram.triggered.connect(self.RGBHistogramClicked)
        self.actionEqual_Histogram.triggered.connect(self.EqualHistogramClicked)
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

    @pyqtSlot()  # grayscale
    def grayClicked(self):
        h, w = self.image.shape[:2]
        gray = np.zeros((h, w), np.uint8)
        for i in range(h):
            for j in range(w):
                gray[i, j] = np.clip(
                    0.07 * self.image[i, j, 0] +
                    0.72 * self.image[i, j, 1] +
                    0.21 * self.image[i, j, 2], 0, 255)
        print(gray)
        self.image = gray
        self.displayImage(2)
        self.loadImage(flname)

    @pyqtSlot()
    def brightnessClicked(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        brightness = 50
        h, w = img.shape[:2]

        for i in np.arange(h):
            for j in np.arange(w):
                a = img.item(i, j)
                b = a + brightness

                if b > 255:
                    b = 255
                elif b < 0:
                    b = 0
                else:
                    b = b
                img.itemset((i, j), b)

        self.image = img
        self.displayImage(2)
        self.loadImage(flname)

    @pyqtSlot()  # Contrast
    def contrastClicked(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        height = gray.shape[0]
        width = gray.shape[1]
        contrast = 2
        for i in np.arange(height):
            for j in np.arange(width):
                a = gray.item(i, j)
                b = math.ceil(a * contrast)
                if b > 255:
                    b = 255
                gray.itemset((i, j), b)
            self.image = gray
            self.displayImage(2)
        self.loadImage(flname)
        print(gray)

    @pyqtSlot()  # Stretching Contrast
    def stretchingContrastClicked(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        h, w = img.shape[:2]

        min = 255
        max = 0

        for i in np.arange(h):
            for j in np.arange(w):
                a = img.item(i, j)
                if a > max:
                    max = a
                if a < min:
                    min = a

        for i in np.arange(h):
            for j in np.arange(w):
                a = img.item(i, j)
                b = float(a - min) / (max - min) * 255
                img.itemset((i, j), b)

        self.image = img
        self.displayImage(2)
        self.loadImage(flname)
        print(img)

    @pyqtSlot()  # Negative
    def negativeClicked(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        h, w = img.shape[:2]
        max_intensity = 255

        for i in range(h):
            for j in range(w):
                a = img.item(i, j)
                b = max_intensity - a
                img.itemset((i, j), b)

        self.image = img
        self.displayImage(2)
        self.loadImage(flname)
        print(img)

    @pyqtSlot()  # biner
    def binerClicked(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        thres = 20
        h, w = img.shape[:2]

        for i in np.arange(h):
            for j in np.arange(w):
                a = img.item(i, j)
                if a > thres:
                    a = 255
                elif a < thres:
                    a = 0
                else:
                    a = a
                img.itemset((i, j), a)

        self.image = img
        self.displayImage(2)
        self.loadImage(flname)
        print(img)

    @pyqtSlot()
    def GrayHistogramClicked(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = img
        self.displayImage(2)
        plt.hist(img.ravel(), 255, [0, 255])
        plt.show()
        self.loadImage(flname)

    @pyqtSlot()
    def RGBHistogramClicked(self):
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histo = cv2.calcHist([self.image], [i], None, [256], [0, 256])
            plt.plot(histo, color=col)
            plt.xlim([0, 256])
        plt.show()
        self.loadImage(flname)

    @pyqtSlot()
    def EqualHistogramClicked(self):
        hist, bins = np.histogram(self.image.flatten(), 256, [0, 256])

        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max() / cdf.max()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        self.image = cdf[self.image]
        self.displayImage(2)
        plt.plot(cdf_normalized, color='b')
        plt.hist(self.image.flatten(), 256, [0, 256], color='r')
        plt.xlim([0, 256])
        plt.legend(('cdf', 'histogram'), loc='upper left')
        plt.show()
        self.loadImage(flname)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ShowImage()
    window.setWindowTitle('Image Processsing')
    window.show()
    sys.exit(app.exec_())
