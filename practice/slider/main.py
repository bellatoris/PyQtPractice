import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import pdb

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        sld = QSlider(QtCore.Qt.Horizontal, self)
        sld.setFocusPolicy(QtCore.Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        sld.valueChanged[int].connect(self.changeValue)

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("mute.png"))
        self.label.setGeometry(160, 40, 80, 30)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle("QSlider")
        self.show()

    def changeValue(self, value):
        if value == 0:
            self.label.setPixmap(QPixmap("mute.png"))
        elif value > 0 and value <= 30:
            self.label.setPixmap(QPixmap("min.png"))
        elif value > 30 and value < 80:
            self.label.setPixmap(QPixmap("med.png"))
        else:
            self.label.setPixmap(QPixmap("max.png"))


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

