from PyQt5.QtWidget import QApplication

from mainwindow import MainWindow

def main():
    app = QApplication([])
    main_win = MainWindow()
    main_win.show()
    return app.exec()


if __name__ == '__main__':
    main()
