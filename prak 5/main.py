import sys
from PyQt5 import QtWidgets
from praktikum5 import ShowImage


sys.path.append(".")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ShowImage()
    window.setWindowTitle('Praktikum Modul 5')
    window.show()
    sys.exit(app.exec_())

