#!/usr/bin/env python3
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import sys
from PySide6 import QtWidgets, QtCore

LEFT, ABOVE = range(2)


class LabelledLineEdit(QtWidgets.QWidget):
    def __init__(self, labelText="", position=LEFT, parent=None):
        super(LabelledLineEdit, self).__init__(parent)
        self.label = QtWidgets.QLabel(labelText)
        self.lineEdit = QtWidgets.QLineEdit()
        self.label.setBuddy(self.lineEdit)
        layout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.LeftToRight
            if position == LEFT
            else QtWidgets.QBoxLayout.TopToBottom
        )
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)


class LabelledTextEdit(QtWidgets.QWidget):
    def __init__(self, labelText="", position=LEFT, parent=None):
        super(LabelledTextEdit, self).__init__(parent)
        self.label = QtWidgets.QLabel(labelText)
        self.textEdit = QtWidgets.QTextEdit()
        self.label.setBuddy(self.textEdit)
        layout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.LeftToRight
            if position == LEFT
            else QtWidgets.QBoxLayout.TopToBottom
        )
        layout.addWidget(self.label)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)


class Dialog(QtWidgets.QDialog):
    def __init__(self, address=None, parent=None):
        super(Dialog, self).__init__(parent)

        self.street = LabelledLineEdit("&Street:")
        self.city = LabelledLineEdit("&City:")
        self.state = LabelledLineEdit("St&ate:")
        self.zipcode = LabelledLineEdit("&Zipcode:")
        self.notes = LabelledTextEdit("&Notes:", ABOVE)
        if address is not None:
            self.street.lineEdit.setText(address.get("street", ""))
            self.city.lineEdit.setText(address.get("city", ""))
            self.state.lineEdit.setText(address.get("state", ""))
            self.zipcode.lineEdit.setText(address.get("zipcode", ""))
            self.notes.textEdit.setPlainText(address.get("notes", ""))
        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.street, 0, 0)
        grid.addWidget(self.city, 0, 1)
        grid.addWidget(self.state, 1, 0)
        grid.addWidget(self.zipcode, 1, 1)
        grid.addWidget(self.notes, 2, 0, 1, 2)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.reject)

        self.setWindowTitle("Labelled Widgets")


if __name__ == "__main__":
    fakeAddress = dict(
        street="3200 Mount Vernon Memorial Highway",
        city="Mount Vernon",
        state="Virginia",
        zipcode="22121",
    )
    app = QtWidgets.QApplication(sys.argv)
    form = Dialog(fakeAddress)
    form.show()
    app.exec()
    print("Street:", form.street.lineEdit.text())
    print("City:", form.city.lineEdit.text())
    print("State:", form.state.lineEdit.text())
    print("Notes:")
    print(form.notes.textEdit.toPlainText())
