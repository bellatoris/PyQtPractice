from PyQt5 import QtGui
from PyQt5.QtWidgets import (
        QDialog, QLabel, QLineEdit, QPushButton,
        QHBoxLayout, QVBoxLayout, QCheckBox
        )
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot

class FindDialog(QDialog):
    find_next = pyqtSignal(str, Qt.CaseSensitivity)
    find_previous = pyqtSignal(str, Qt.CaseSensitivity)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel(self.tr('Find &what:'))
        self.line_edit = QLineEdit()
        self.label.setBuddy(self.line_edit)

        self.case_check_box = QCheckBox(self.tr('Match &case'))
        self.backward_check_box = QCheckBox(self.tr('Search &backward'))

        self.find_button = QPushButton(self.tr('&Find'))
        self.find_button.setDefault(True)
        self.find_button.setEnabled(False)

        self.close_button = QPushButton(self.tr('Close'))

        self.line_edit.textChanged.connect(self.enable_find_button)
        self.find_button.clicked.connect(self.find_clicked)
        self.close_button.clicked.connect(self.close)

        self.top_left_layout = QHBoxLayout()
        self.top_left_layout.addWidget(self.label)
        self.top_left_layout.addWidget(self.line_edit)

        self.left_layout = QVBoxLayout()
        self.left_layout.addLayout(self.top_left_layout)
        self.left_layout.addWidget(self.case_check_box)
        self.left_layout.addWidget(self.backward_check_box)

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.find_button)
        self.right_layout.addWidget(self.close_button)
        self.right_layout.addStretch()

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.setLayout(self.main_layout)

        self.setWindowTitle(self.tr('Find'))
        self.setFixedHeight(self.sizeHint().height())

    @pyqtSlot()
    def find_clicked(self):
        text = self.line_edit.text()
        case_sensitivity = Qt.CaseSensitive if self.case_check_box.isChecked()\
                           else Qt.CaseInsensitive

        if self.backward_check_box.isChecked():
            self.find_previous.emit(text, case_sensitivity)
        else:
            self.find_next.emit(text, case_sensitivity)

    @pyqtSlot(str)
    def enable_find_button(self, text: str) -> None:
        self.find_button.setEnabled(bool(text))
