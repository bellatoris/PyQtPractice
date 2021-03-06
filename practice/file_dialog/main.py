import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon("open.png"), "Open", self)
        openFile.setShortcut("Ctrl+o")
        openFile.setStatusTip("Open new File")
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("File dialog")
        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, "Open file",
                "/home")

        f = open(fname, 'r')

        with f:
            data = f.read()
            self.textEdit.setText(data)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

