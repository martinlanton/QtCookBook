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

from PySide6 import QtWidgets, QtCore


class ResizeDlg(QtWidgets.QDialog):
    def __init__(self, width, height, parent=None):
        super(ResizeDlg, self).__init__(parent)

        widthLabel = QtWidgets.QLabel("&Width:")
        self.widthSpinBox = QtWidgets.QSpinBox()
        widthLabel.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.widthSpinBox.setRange(4, width * 4)
        self.widthSpinBox.setValue(width)
        heightLabel = QtWidgets.QLabel("&Height:")
        self.heightSpinBox = QtWidgets.QSpinBox()
        heightLabel.setBuddy(self.heightSpinBox)
        self.heightSpinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.heightSpinBox.setRange(4, height * 4)
        self.heightSpinBox.setValue(height)

        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        layout = QtWidgets.QGridLayout()
        layout.addWidget(widthLabel, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(heightLabel, 1, 0)
        layout.addWidget(self.heightSpinBox, 1, 1)
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.reject)

        self.setWindowTitle("Image Changer - Resize")

    def result(self):
        return self.widthSpinBox.value(), self.heightSpinBox.value()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    form = ResizeDlg(64, 128)
    form.show()
    app.exec()
