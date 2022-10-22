import numpy as np
import sys
import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore    import pyqtSlot
from PyQt5.QtGui     import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic       import loadUi

class ShowImage (QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi('tugas.ui',self)
        self.image = None
        self.loadButton.clicked.connect(self.loadClicked)
        self.loadtranslasi.clicked.connect(self.loadimagetranslasi)

    @pyqtSlot()
    def loadClicked(self):
        self.loadImage('anjing.jpg', cv2.IMREAD_GRAYSCALE)

    def loadImage(self, flname, cv ):
        self.image = cv2.imread(flname)
        self.displayImage(2)

    def imagetranlasi(self,):
        h, w = self.image.shape[:2]
        quarter_h, quarter_w = h/4, w/4
        T = np.float32([[1, 0, quarter_w], [0, 1, quarter_h]])
        img = cv2.warpAffine(self.image, T, (w, h))
        self()

    def displayImage(self):
        qformat = QImage.Format_Indexed8

        if len(self.image.shape) == 3:
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

                img = QImage(self.image,
                             self.image.shape[1],
                             self.image.shape[0],
                             self.image.strides[0],
                             qformat)
                img = img.rgbSwapped()

                self.imgLabel.setPixmap(QPixmap.fromImage(img))
                self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.imgLabel.setScaledContents(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ShowImage()
    window.setWindowTitle('Penampil Gambar')
    window.show()
    sys.exit(app.exec_())