import string

from PyQt5 import QtGui
from PyQt5.QtWidgets import (
        QDialog, QLabel, QLineEdit, QPushButton,
        QHBoxLayout, QVBoxLayout, QApplication,
        QComboBox, QGroupBox, QLayout, QGridLayout
        )
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot


class SortDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ok_button = QPushButton(self.tr('OK'))
        self.ok_button.setDefault(True)
        self.cancel_button = QPushButton(self.tr('Cancel'),
                                         objectName='canel_button')
        self.more_button = QPushButton(self.tr('&More'))
        self.more_button.setCheckable(True)

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.ok_button)
        self.right_layout.addWidget(self.cancel_button)
        self.right_layout.addStretch()
        self.right_layout.addWidget(self.more_button)

        primary = self.make_group_box('Primary')
        self.primary_column_combo = primary[0]
        self.primary_order_combo = primary[1]
        self.primary_group_box = primary[2]

        secondary = self.make_group_box('Secondary')
        self.secondary_column_combo = secondary[0]
        self.secondary_order_combo = secondary[1]
        self.secondary_group_box = secondary[2]

        teritary = self.make_group_box('Teritary')
        self.teritary_column_combo = teritary[0]
        self.teritary_order_combo = teritary[1]
        self.teritary_group_box = teritary[2]

        self.secondary_group_box.hide()
        self.teritary_group_box.hide()

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.primary_group_box, 0, 0)
        self.main_layout.addLayout(self.right_layout, 0, 1, 2, 1)
        self.main_layout.setRowStretch(1, 1)
        self.main_layout.addWidget(self.secondary_group_box, 2, 0)
        self.main_layout.addWidget(self.teritary_group_box, 3, 0)
        self.setLayout(self.main_layout)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.more_button.toggled.connect(self.secondary_group_box.setVisible)
        self.more_button.toggled.connect(self.teritary_group_box.setVisible)

        self.set_column_range('A', 'Z')

    def make_group_box(self, text):
        column_label = QLabel(self.tr('Column:'))
        order_label = QLabel(self.tr('Order:'))
        column_combo = QComboBox()
        order_combo = QComboBox()

        order_combo.addItem(self.tr('ascending'))
        order_combo.addItem(self.tr('descending'))

        column_layout = QHBoxLayout()
        column_layout.addWidget(column_label)
        column_layout.addWidget(column_combo)
        column_layout.addStretch()

        order_layout = QHBoxLayout()
        order_layout.addWidget(order_label)
        order_layout.addWidget(order_combo)

        group_layout = QVBoxLayout()
        group_layout.addLayout(column_layout)
        group_layout.addLayout(order_layout)

        group_box = QGroupBox(self.tr('&{} Key'.format(text)))
        group_box.setLayout(group_layout)

        return (column_combo, order_combo, group_box)

    def set_column_range(self, first, last):
        self.primary_column_combo.clear()
        self.secondary_column_combo.clear()
        self.teritary_column_combo.clear()

        self.secondary_column_combo.addItem(self.tr('None'))
        self.teritary_column_combo.addItem(self.tr('None'))
        self.primary_column_combo.setMinimumSize(self.secondary_column_combo.sizeHint())

        ch = string.ascii_uppercase.index(first)
        while ch <= string.ascii_uppercase.index(last):
            char = string.ascii_uppercase[ch]
            self.primary_column_combo.addItem(char)
            self.secondary_column_combo.addItem(char)
            self.secondary_column_combo.addItem(char)
            ch += 1

if __name__ == '__main__':
    app = QApplication([])
    sort_dialog = SortDialog()
    sort_dialog.set_column_range('C', 'F')
    sort_dialog.show()

    app.exec()
