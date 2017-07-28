import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()


    def initUI(self):
        exitAction = QAction(QIcon("exit.png"), "&Exit", self)
        exitAction.setShortcut("Ctrl+q")
        exitAction.setStatusTip("Exit application")
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Menubar")
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
