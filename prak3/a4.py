import math
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

        loadUi('UI/prak_3.ui', self)
        self.image = None
        # button
        self.loadButton.clicked.connect(self.loadClicked)
        self.saveButton.clicked.connect(self.saveClicked)
        # file menu bar
        self.actionLoad_Image.triggered.connect(self.loadClicked)
        self.actionSave_Image.triggered.connect(self.saveClicked)
        self.actiontranslasi.triggered.connect(self.imageTranslation)
        self.action_46.triggered.connect(self.Rotasimin45Clicked)
        self.action45.triggered.connect(self.RotasiPlus45Clicked)
        self.action90.triggered.connect(self.Rotasiplus90Clicked)
        self.action_90.triggered.connect(self.RotasiMin90Clicked)
        self.action180.triggered.connect(self.Rotasiplus180Clicked)
        self.actiontranspose.triggered.connect(self.TransposeClicked)
        self.action2x.triggered.connect(self.zoom2x)
        self.action3x.triggered.connect(self.zoom3x)
        self.actionskewed.triggered.connect(self.skewed_SizeClicked)
        self.action1_2.triggered.connect(self.zoomset)
        self.action1_4.triggered.connect(self.zoomper4)
        self.action3_4.triggered.connect(self.zoomtigper4)
        self.actioncrop.triggered.connect(self.cropwithvalue)


    @pyqtSlot()
    def loadClicked(self):
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
        h, w = self.image.shape[:2]
        quarter_h, quarter_w = h / 4, w / 4
        T = np.float32([[1, 0, quarter_w], [0, 1, quarter_h]])
        img = cv2.warpAffine(self.image, T, (w, h))
        self.image = img
        self.displayImage(2)
        print (img)


    @pyqtSlot()
    def rotasi(self, degree):
        h, w = self.image.shape[:2]
        rotationMatrix = cv2.getRotationMatrix2D((w / 2, h / 2), degree, .7)
        cos = np.abs(rotationMatrix[0, 0])
        sin = np.abs(rotationMatrix[0, 1])
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        rotationMatrix[0, 2] += (nW / 2) - w / 2
        rotationMatrix[1, 2] += (nH / 2) - h / 2
        rot_image = cv2.warpAffine(self.image, rotationMatrix, (h, w))
        self.image = rot_image

    @pyqtSlot()
    def Rotasimin45Clicked(self):
        self.rotasi(-45)
        self.displayImage(2)
    @pyqtSlot()
    def RotasiPlus45Clicked(self):
        self.rotasi(45)
        self.displayImage(2)

    @pyqtSlot()
    def RotasiMin90Clicked(self):
        self.rotasi(-90)
        self.displayImage(2)

    @pyqtSlot()
    def Rotasiplus90Clicked(self):
        self.rotasi(90)
        self.displayImage(2)

    @pyqtSlot()
    def Rotasiplus180Clicked(self):
        self.rotasi(180)
        self.displayImage(2)

    @pyqtSlot()
    def TransposeClicked(self):
        trans_img = cv2.transpose(self.image)
        self.image = trans_img
        self.displayImage(2)

    @pyqtSlot()
    def resizeImage(self):
        resize_img = cv2.resize(self.image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        self.image = resize_img
        self.displayImage(3)

    @pyqtSlot()
    def zoom2x(self):
        cv2.imshow('Original', self.image)
        resize_img = cv2.resize(self.image, None, fx=2, fy=2)
        self.image = resize_img
        cv2.imshow('', self.image)
        #self.displayImage(3)

    def zoom3x(self):
        cv2.imshow('Original', self.image)
        resize_img = cv2.resize(self.image, None, fx=3, fy=3)
        self.image = resize_img
        cv2.imshow('', self.image)
        #self.displayImage(3)

    @pyqtSlot()
    def zoomset(self):
        cv2.imshow('Original', self.image)
        resize_img = cv2.resize(self.image, None, fx=0.5, fy=0.5, interpolation=
        cv2.INTER_CUBIC)
        self.image = resize_img
        cv2.imshow('', self.image)
        self.displayImage(3)

    @pyqtSlot()
    def zoomper4(self):
        cv2.imshow('Original', self.image)
        resize_img = cv2.resize(self.image, None, fx=0.25, fy=0.25, interpolation=
        cv2.INTER_CUBIC)
        self.image = resize_img
        cv2.imshow('', self.image)
        self.displayImage(3)

    @pyqtSlot()
    def zoomtigper4(self):
        cv2.imshow('Original', self.image)
        resize_img = cv2.resize(self.image, None, fx=0.75, fy=0.75, interpolation=
        cv2.INTER_CUBIC)
        self.image = resize_img
        cv2.imshow('', self.image)
        self.displayImage(3)

    @pyqtSlot()
    def skewed_SizeClicked(self):
        cv2.imshow('Original', self.image)
        resize_img = cv2.resize(self.image, (900, 400), interpolation=cv2.INTER_AREA)
        self.image = resize_img
        cv2.imshow('', self.image)

    @pyqtSlot()
    def CropingClicked(self):
        h, w = self.image.shape[:2]
        start_row, start_col = int(h * .1), int(w * .1)
        end_row, end_col = int(h * .5), int(w * .5)
        crop = self.image[start_row:end_row, start_col:end_col]
        cv2.imshow('Original', self.image)
        cv2.imshow('CropImage',crop)

    @pyqtSlot()
    def cropwithvalue(self):
        h, w = self.image.shape[:2]
        crop = self.image[0:50, 0:100]
        cv2.imshow('Original', self.image)
        cv2.imshow('CropImage', crop)



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
        if windows == 3:
            self.hasilLabel.setPixmap(QPixmap.fromImage(img))
            self.hasilLabel.setAlignment(QtCore.Qt.AlignHCenter
                                         | QtCore.Qt.AlignVCenter)
