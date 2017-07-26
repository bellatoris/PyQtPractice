from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import sys


def main():
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
