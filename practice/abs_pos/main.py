from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        lbl1 = QLabel("Doogie", self)
        lbl1.move(15, 10)

        lbl2 = QLabel("tutorials", self)
        lbl2.move(35, 40)

        lbl3 = QLabel("for programmers", self)
        lbl3.move(55, 70)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("Absolute")
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
