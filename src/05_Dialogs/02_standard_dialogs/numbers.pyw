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

import math
import random
import string
import sys
from PySide6 import QtWidgets, QtCore
import numberformatdlg1
import numberformatdlg2
import numberformatdlg3


class Form(QtWidgets.QDialog):

    X_MAX = 26
    Y_MAX = 60

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        pass

        self.numberFormatDlg = None
        self.format = dict(
            thousandsseparator=",",
            decimalmarker=".",
            decimalplaces=2,
            rednegatives=False,
        )
        self.numbers = {}
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                self.numbers[(x, y)] = (10000 * random.random()) - 5000

        self.table = QtWidgets.QTableWidget()
        formatButton1 = QtWidgets.QPushButton("Set Number Format... (&Modal)")
        formatButton2 = QtWidgets.QPushButton("Set Number Format... (Modele&ss)")
        formatButton3 = QtWidgets.QPushButton("Set Number Format... (`&Live')")

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(formatButton1)
        buttonLayout.addWidget(formatButton2)
        buttonLayout.addWidget(formatButton3)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(formatButton1, QtCore.SIGNAL("clicked()"), self.setNumberFormat1)
        self.connect(formatButton2, QtCore.SIGNAL("clicked()"), self.setNumberFormat2)
        self.connect(formatButton3, QtCore.SIGNAL("clicked()"), self.setNumberFormat3)
        self.setWindowTitle("Numbers")
        self.refreshTable()

    def refreshTable(self):
        self.table.clear()
        self.table.setColumnCount(self.X_MAX)
        self.table.setRowCount(self.Y_MAX)
        self.table.setHorizontalHeaderLabels(list(string.ascii_uppercase))
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                fraction, whole = math.modf(self.numbers[(x, y)])
                sign = "-" if whole < 0 else ""
                whole = "{}".format(int(math.floor(abs(whole))))
                digits = []
                for i, digit in enumerate(reversed(whole)):
                    if i and i % 3 == 0:
                        digits.insert(0, self.format["thousandsseparator"])
                    digits.insert(0, digit)
                if self.format["decimalplaces"]:
                    fraction = "{0:.7f}".format(abs(fraction))
                    fraction = (
                        self.format["decimalmarker"]
                        + fraction[2 : self.format["decimalplaces"] + 2]
                    )
                else:
                    fraction = ""
                text = "{}{}{}".format(sign, "".join(digits), fraction)
                item = QtWidgets.QTableWidgetItem(text)
                item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                if sign and self.format["rednegatives"]:
                    item.setBackground(QtCore.Qt.red)
                self.table.setItem(y, x, item)

    def setNumberFormat1(self):
        dialog = numberformatdlg1.NumberFormatDlg(self.format, self)
        if dialog.exec():
            self.format = dialog.numberFormat()
            self.refreshTable()

    def setNumberFormat2(self):
        dialog = numberformatdlg2.NumberFormatDlg(self.format, self)
        dialog.changed.connect(self.refreshTable)
        dialog.show()

    def setNumberFormat3(self):
        if self.numberFormatDlg is None:
            self.numberFormatDlg = numberformatdlg3.NumberFormatDlg(
                self.format, self.refreshTable, self
            )
        self.numberFormatDlg.show()
        self.numberFormatDlg.raise_()
        self.numberFormatDlg.activateWindow()


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec()
