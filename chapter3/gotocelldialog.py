from PyQt5 import QtGui
from PyQt5.QtWidgets import (
        QDialog, QLabel, QLineEdit, QPushButton,
        QHBoxLayout, QVBoxLayout, QApplication
        )
from PyQt5.QtCore import (
        pyqtSignal, Qt, pyqtSlot, QRegExp,
        )
from PyQt5.QtGui import QRegExpValidator

class GoToCellDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel(self.tr('&Cell Location:'))
        self.line_edit = QLineEdit()
        self.label.setBuddy(self.line_edit)

        self.ok_button = QPushButton(self.tr('OK'))
        self.ok_button.setDefault(True)
        self.ok_button.setEnabled(False)

        self.cancel_button = QPushButton(self.tr('Cancel'))

        self.line_edit.textChanged.connect(self.enable_ok_button)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.label)
        self.top_layout.addWidget(self.line_edit)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.ok_button)
        self.bottom_layout.addWidget(self.cancel_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)
        self.setLayout(self.main_layout)

        self.setWindowTitle(self.tr('Go to cell'))
        self.setFixedHeight(self.sizeHint().height())

        self.reg_exp = QRegExp('[A-za-z][1-9][0-9]{0,2}')
        self.line_edit.setValidator(QRegExpValidator(self.reg_exp, self))

    @pyqtSlot(str)
    def enable_ok_button(self, text):
        self.ok_button.setEnabled(self.line_edit.hasAcceptableInput())

if __name__ == '__main__':
    app = QApplication([])
    goto_dialog = GoToCellDialog()
    goto_dialog.show()

    app.exec()
