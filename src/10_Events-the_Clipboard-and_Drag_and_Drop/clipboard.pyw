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

import os
import sys
from PySide6 import QtWidgets, QtCore, QtGui


class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        textCopyButton = QtWidgets.QPushButton("&Copy Text")
        textPasteButton = QtWidgets.QPushButton("Paste &Text")
        htmlCopyButton = QtWidgets.QPushButton("C&opy HTML")
        htmlPasteButton = QtWidgets.QPushButton("Paste &HTML")
        imageCopyButton = QtWidgets.QPushButton("Co&py Image")
        imagePasteButton = QtWidgets.QPushButton("Paste &Image")
        self.textLabel = QtWidgets.QLabel("Original text")
        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setPixmap(
            QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "images/clock.png"))
        )

        layout = QtWidgets.QGridLayout()
        layout.addWidget(textCopyButton, 0, 0)
        layout.addWidget(imageCopyButton, 0, 1)
        layout.addWidget(htmlCopyButton, 0, 2)
        layout.addWidget(textPasteButton, 1, 0)
        layout.addWidget(imagePasteButton, 1, 1)
        layout.addWidget(htmlPasteButton, 1, 2)
        layout.addWidget(self.textLabel, 2, 0, 1, 2)
        layout.addWidget(self.imageLabel, 2, 2)
        self.setLayout(layout)

        self.connect(textCopyButton, QtCore.SIGNAL("clicked()"), self.copyText)
        self.connect(textPasteButton, QtCore.SIGNAL("clicked()"), self.pasteText)
        self.connect(htmlCopyButton, QtCore.SIGNAL("clicked()"), self.copyHtml)
        self.connect(htmlPasteButton, QtCore.SIGNAL("clicked()"), self.pasteHtml)
        self.connect(imageCopyButton, QtCore.SIGNAL("clicked()"), self.copyImage)
        self.connect(imagePasteButton, QtCore.SIGNAL("clicked()"), self.pasteImage)

        self.setWindowTitle("Clipboard")

    def copyText(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText("I've been clipped!")

    def pasteText(self):
        clipboard = QtWidgets.QApplication.clipboard()
        self.textLabel.setText(clipboard.text())

    def copyImage(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setPixmap(
            QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "images/gvim.png"))
        )

    def pasteImage(self):
        clipboard = QtWidgets.QApplication.clipboard()
        self.imageLabel.setPixmap(clipboard.pixmap())

    def copyHtml(self):
        mimeData = QtCore.QMimeData()
        mimeData.setHtml("<b>Bold and <font color=red>Red</font></b>")
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setMimeData(mimeData)

    def pasteHtml(self):
        clipboard = QtWidgets.QApplication.clipboard()
        mimeData = clipboard.mimeData()
        if mimeData.hasHtml():
            self.textLabel.setText(mimeData.html())


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec()
