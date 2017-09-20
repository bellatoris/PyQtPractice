from PyQt5.QtWidgets import QApplication

from finddialog import FindDialog

def main(*arg):
    app = QApplication([])
    find_dialog = FindDialog()
    find_dialog.show()

    return app.exec()


if __name__ == '__main__':
    main()
