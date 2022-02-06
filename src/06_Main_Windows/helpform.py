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


class HelpForm(QtWidgets.QDialog):
    def __init__(self, page, parent=None):
        super(HelpForm, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowModality(QtCore.Qt.WindowModal)

        backAction = QtGui.QAction(QtGui.QIcon("resources:back.png"), "&Back", self)
        backAction.setShortcut(QtGui.QKeySequence.Back)
        homeAction = QtGui.QAction(QtGui.QIcon("resources:home.png"), "&Home", self)
        homeAction.setShortcut("Home")
        self.pageLabel = QtWidgets.QLabel()

        toolBar = QtWidgets.QToolBar()
        toolBar.addAction(backAction)
        toolBar.addAction(homeAction)
        toolBar.addWidget(self.pageLabel)
        self.textBrowser = QtWidgets.QTextBrowser()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolBar)
        layout.addWidget(self.textBrowser, 1)
        self.setLayout(layout)

        self.connect(
            backAction,
            QtCore.SIGNAL("triggered()"),
            self.textBrowser,
            QtCore.SLOT("backward()"),
        )
        self.connect(
            homeAction,
            QtCore.SIGNAL("triggered()"),
            self.textBrowser,
            QtCore.SLOT("home()"),
        )
        self.connect(
            self.textBrowser, QtCore.SIGNAL("sourceChanged(QUrl)"), self.updatePageTitle
        )

        self.textBrowser.setSearchPaths([":/help"])
        self.textBrowser.setSource(QtCore.QUrl(page))
        self.resize(400, 600)
        self.setWindowTitle("{} Help".format(QtWidgets.QApplication.applicationName()))

    def updatePageTitle(self):
        self.pageLabel.setText(self.textBrowser.documentTitle())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    form = HelpForm("index.html")
    form.show()
    app.exec()
