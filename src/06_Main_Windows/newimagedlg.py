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

from PySide6 import QtWidgets, QtCore, QtGui

# TODO : create this properly from newimagedlg.ui
import ui_newimagedlg


class NewImageDlg(QtWidgets.QDialog, ui_newimagedlg.Ui_NewImageDlg):
    def __init__(self, parent=None):
        super(NewImageDlg, self).__init__(parent)
        self.setupUi(self)

        self.color = QtCore.Qt.red
        for value, text in (
            (QtCore.Qt.SolidPattern, "Solid"),
            (QtCore.Qt.Dense1Pattern, "Dense #1"),
            (QtCore.Qt.Dense2Pattern, "Dense #2"),
            (QtCore.Qt.Dense3Pattern, "Dense #3"),
            (QtCore.Qt.Dense4Pattern, "Dense #4"),
            (QtCore.Qt.Dense5Pattern, "Dense #5"),
            (QtCore.Qt.Dense6Pattern, "Dense #6"),
            (QtCore.Qt.Dense7Pattern, "Dense #7"),
            (QtCore.Qt.HorPattern, "Horizontal"),
            (QtCore.Qt.VerPattern, "Vertical"),
            (QtCore.Qt.CrossPattern, "Cross"),
            (QtCore.Qt.BDiagPattern, "Backward Diagonal"),
            (QtCore.Qt.FDiagPattern, "Forward Diagonal"),
            (QtCore.Qt.DiagCrossPattern, "Diagonal Cross"),
        ):
            self.brushComboBox.addItem(text, value)

        self.connect(self.colorButton, QtCore.SIGNAL("clicked()"), self.getColor)
        self.connect(self.brushComboBox, QtCore.SIGNAL("activated(int)"), self.setColor)
        self.setColor()
        self.widthSpinBox.setFocus()

    def getColor(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.black, self)
        if color.isValid():
            self.color = color
            self.setColor()

    def setColor(self):
        pixmap = self._makePixmap(60, 30)
        self.colorLabel.setPixmap(pixmap)

    def image(self):
        pixmap = self._makePixmap(self.widthSpinBox.value(), self.heightSpinBox.value())
        return QtGui.QPixmap.toImage(pixmap)

    def _makePixmap(self, width, height):
        pixmap = QtGui.QPixmap(width, height)
        style = int(self.brushComboBox.itemData(self.brushComboBox.currentIndex()))
        brush = QtGui.QBrush(self.color, QtCore.Qt.BrushStyle(style))
        painter = QtGui.QPainter(pixmap)
        painter.fillRect(pixmap.rect(), QtCore.Qt.white)
        painter.fillRect(pixmap.rect(), brush)
        return pixmap


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    form = NewImageDlg()
    form.show()
    app.exec()
