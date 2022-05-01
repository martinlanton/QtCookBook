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

        listWidget = QtWidgets.QListWidget()
        listWidget.setAcceptDrops(True)
        listWidget.setDragEnabled(True)
        path = os.path.dirname(__file__)
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png"):
                item = QtWidgets.QListWidgetItem(image.split(".")[0].capitalize())
                item.setIcon(QtGui.QIcon(os.path.join(path, "images/{}".format(image))))
                listWidget.addItem(item)
        iconListWidget = QtWidgets.QListWidget()
        iconListWidget.setAcceptDrops(True)
        iconListWidget.setDragEnabled(True)
        iconListWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        tableWidget = QtWidgets.QTableWidget()
        tableWidget.setRowCount(5)
        tableWidget.setColumnCount(2)
        tableWidget.setHorizontalHeaderLabels(["Column #1", "Column #2"])
        tableWidget.setAcceptDrops(True)
        tableWidget.setDragEnabled(True)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(listWidget)
        splitter.addWidget(iconListWidget)
        splitter.addWidget(tableWidget)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.setWindowTitle("Drag and Drop")


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec()
