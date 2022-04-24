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

MAC = True
try:
    from PyQt4.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False


class FindAndReplaceDlg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(FindAndReplaceDlg, self).__init__(parent)

        findLabel = QtWidgets.QLabel("Find &what:")
        self.findLineEdit = QtWidgets.QLineEdit()
        findLabel.setBuddy(self.findLineEdit)
        replaceLabel = QtWidgets.QLabel("Replace w&ith:")
        self.replaceLineEdit = QtWidgets.QLineEdit()
        replaceLabel.setBuddy(self.replaceLineEdit)
        self.caseCheckBox = QtWidgets.QCheckBox("&Case sensitive")
        self.wholeCheckBox = QtWidgets.QCheckBox("Wh&ole words")
        self.wholeCheckBox.setChecked(True)
        moreFrame = QtWidgets.QFrame()
        moreFrame.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)
        self.backwardsCheckBox = QtWidgets.QCheckBox("Search &Backwards")
        self.regexCheckBox = QtWidgets.QCheckBox("Regular E&xpression")
        self.ignoreNotesCheckBox = QtWidgets.QCheckBox(
            "Ignore foot&notes " "and endnotes"
        )
        line = QtWidgets.QFrame()
        line.setFrameStyle(QtWidgets.QFrame.VLine | QtWidgets.QFrame.Sunken)
        self.findButton = QtWidgets.QPushButton("&Find")
        self.replaceButton = QtWidgets.QPushButton("&Replace")
        closeButton = QtWidgets.QPushButton("Close")
        moreButton = QtWidgets.QPushButton("&More")
        moreButton.setCheckable(True)
        if not MAC:
            self.findButton.setFocusPolicy(QtCore.Qt.NoFocus)
            self.replaceButton.setFocusPolicy(QtCore.Qt.NoFocus)
            closeButton.setFocusPolicy(QtCore.Qt.NoFocus)
            moreButton.setFocusPolicy(QtCore.Qt.NoFocus)

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(findLabel, 0, 0)
        gridLayout.addWidget(self.findLineEdit, 0, 1)
        gridLayout.addWidget(replaceLabel, 1, 0)
        gridLayout.addWidget(self.replaceLineEdit, 1, 1)
        frameLayout = QtWidgets.QVBoxLayout()
        frameLayout.addWidget(self.backwardsCheckBox)
        frameLayout.addWidget(self.regexCheckBox)
        frameLayout.addWidget(self.ignoreNotesCheckBox)
        moreFrame.setLayout(frameLayout)
        leftLayout = QtWidgets.QVBoxLayout()
        leftLayout.addLayout(gridLayout)
        leftLayout.addWidget(self.caseCheckBox)
        leftLayout.addWidget(self.wholeCheckBox)
        leftLayout.addWidget(moreFrame)
        buttonLayout = QtWidgets.QVBoxLayout()
        buttonLayout.addWidget(self.findButton)
        buttonLayout.addWidget(self.replaceButton)
        buttonLayout.addWidget(closeButton)
        buttonLayout.addWidget(moreButton)
        buttonLayout.addStretch()
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addWidget(line)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        moreFrame.hide()
        mainLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.connect(
            moreButton,
            QtCore.SIGNAL("toggled(bool)"),
            moreFrame,
            QtCore.SLOT("setVisible(bool)"),
        )
        self.connect(
            self.findLineEdit, QtCore.SIGNAL("textEdited(QString)"), self.updateUi
        )
        self.connect(self.findButton, QtCore.SIGNAL("clicked()"), self.findClicked)
        self.connect(
            self.replaceButton, QtCore.SIGNAL("clicked()"), self.replaceClicked
        )

        self.updateUi()
        self.setWindowTitle("Find and Replace")

    def findClicked(self):
        self.emit(
            QtCore.SIGNAL("find"),
            self.findLineEdit.text(),
            self.caseCheckBox.isChecked(),
            self.wholeCheckBox.isChecked(),
            self.backwardsCheckBox.isChecked(),
            self.regexCheckBox.isChecked(),
            self.ignoreNotesCheckBox.isChecked(),
        )

    def replaceClicked(self):
        self.emit(
            QtCore.SIGNAL("replace"),
            self.findLineEdit.text(),
            self.replaceLineEdit.text(),
            self.caseCheckBox.isChecked(),
            self.wholeCheckBox.isChecked(),
            self.backwardsCheckBox.isChecked(),
            self.regexCheckBox.isChecked(),
            self.ignoreNotesCheckBox.isChecked(),
        )

    def updateUi(self):
        enable = bool(self.findLineEdit.text())
        self.findButton.setEnabled(enable)
        self.replaceButton.setEnabled(enable)


if __name__ == "__main__":

    def find(what, *args):
        print("Find {} {}".format(what, [x for x in args]))

    def replace(old, new, *args):
        print("Replace {} with {} {}".format(old, new, [x for x in args]))

    app = QtWidgets.QApplication(sys.argv)
    form = FindAndReplaceDlg()
    form.connect(form, QtCore.SIGNAL("find"), find)
    form.connect(form, QtCore.SIGNAL("replace"), replace)
    form.show()
    app.exec()
