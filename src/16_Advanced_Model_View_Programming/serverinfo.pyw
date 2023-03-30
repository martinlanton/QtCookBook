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
import treeoftable


class ServerModel(treeoftable.TreeOfTableModel):
    def __init__(self, parent=None):
        super(ServerModel, self).__init__(parent)

    def data(self, index, role):
        if role == QtCore.Qt.DecorationRole:
            node = self.nodeFromIndex(index)
            if node is None:
                return None
            if isinstance(node, treeoftable.BranchNode):
                if index.column() != 0:
                    return None
                filename = node.toString().replace(" ", "_")
                parent = node.parent.toString()
                if parent and parent != "USA":
                    return None
                if parent == "USA":
                    filename = "USA_" + filename
                filename = os.path.join(
                    os.path.dirname(__file__), "flags", filename + ".png"
                )
                pixmap = QtGui.QPixmap(filename)
                if pixmap.isNull():
                    return None
                return pixmap
        return treeoftable.TreeOfTableModel.data(self, index, role)


class TreeOfTableWidget(QtWidgets.QTreeView):
    def __init__(self, filename, nesting, separator, parent=None):
        super(TreeOfTableWidget, self).__init__(parent)
        self.setSelectionBehavior(QtWidgets.QTreeView.SelectItems)
        self.setUniformRowHeights(True)
        model = ServerModel(self)
        self.setModel(model)
        try:
            model.load(filename, nesting, separator)
        except IOError as e:
            QtWidgets.QMessageBox.warning(self, "Server Info - Error", e)
        self.connect(self, QtCore.SIGNAL("activated(QtCore.QModelIndex)"), self.activated)
        self.connect(self, QtCore.SIGNAL("expanded(QtCore.QModelIndex)"), self.expanded)
        self.expanded()

    def currentFields(self):
        return self.model().asRecord(self.currentIndex())

    def activated(self, index):
        self.emit(QtCore.SIGNAL("activated"), self.model().asRecord(index))

    def expanded(self):
        for column in range(self.model().columnCount(QtCore.QModelIndex())):
            self.resizeColumnToContents(column)


class MainForm(QtWidgets.QMainWindow):
    def __init__(self, filename, nesting, separator, parent=None):
        super(MainForm, self).__init__(parent)
        headers = ["Country/State (US)/City/Provider", "Server", "IP"]
        if nesting != 3:
            if nesting == 1:
                headers = ["Country/State (US)", "City", "Provider", "Server"]
            elif nesting == 2:
                headers = ["Country/State (US)/City", "Provider", "Server"]
            elif nesting == 4:
                headers = ["Country/State (US)/City/Provider/Server"]
            headers.append("IP")

        self.treeWidget = TreeOfTableWidget(filename, nesting, separator)
        self.treeWidget.model().headers = headers
        self.setCentralWidget(self.treeWidget)

        QtGui.QShortcut(QtGui.QKeySequence("Escape"), self, self.close)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)

        self.treeWidget.activated.connect(self.activated)

        self.setWindowTitle("Server Info")
        self.statusBar().showMessage("Ready...", 5000)

    def picked(self):
        return self.treeWidget.currentFields()

    def activated(self, fields):
        self.statusBar().showMessage("*".join(fields), 60000)


app = QtWidgets.QApplication(sys.argv)
nesting = 3
if len(sys.argv) > 1:
    try:
        nesting = int(sys.argv[1])
    except:
        pass
    if nesting not in (1, 2, 3, 4):
        nesting = 3

form = MainForm(os.path.join(os.path.dirname(__file__), "servers.txt"), nesting, "*")
form.resize(750, 550)
form.show()
app.exec()
print("*".join(form.picked()))
