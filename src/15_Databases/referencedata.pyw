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
from PySide6 import QtWidgets, QtCore, QtSql

MAC = True
try:
    from PySide6.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

ID, CATEGORY, SHORTDESC, LONGDESC = range(4)


class ReferenceDataDlg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ReferenceDataDlg, self).__init__(parent)

        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable("reference")
        self.model.setSort(ID, QtCore.Qt.AscendingOrder)
        self.model.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(CATEGORY, QtCore.Qt.Horizontal, "Category")
        self.model.setHeaderData(SHORTDESC, QtCore.Qt.Horizontal, "Short Desc.")
        self.model.setHeaderData(LONGDESC, QtCore.Qt.Horizontal, "Long Desc.")
        self.model.select()

        self.view = QtWidgets.QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.view.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.view.setColumnHidden(ID, True)
        self.view.resizeColumnsToContents()

        buttonBox = QtWidgets.QDialogButtonBox()
        addButton = buttonBox.addButton("&Add", QtWidgets.QDialogButtonBox.ActionRole)
        deleteButton = buttonBox.addButton("&Delete", QtWidgets.QDialogButtonBox.ActionRole)
        sortButton = buttonBox.addButton("&Sort", QtWidgets.QDialogButtonBox.ActionRole)
        if not MAC:
            addButton.setFocusPolicy(QtCore.Qt.NoFocus)
            deleteButton.setFocusPolicy(QtCore.Qt.NoFocus)
            sortButton.setFocusPolicy(QtCore.Qt.NoFocus)

        menu = QtWidgets.QMenu(self)
        sortByCategoryAction = menu.addAction("Sort by &Category")
        sortByDescriptionAction = menu.addAction("Sort by &Description")
        sortByIDAction = menu.addAction("Sort by &ID")
        sortButton.setMenu(menu)
        closeButton = buttonBox.addButton(QtWidgets.QDialogButtonBox.Close)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(addButton, QtCore.SIGNAL("clicked()"), self.addRecord)
        self.connect(deleteButton, QtCore.SIGNAL("clicked()"), self.deleteRecord)
        self.connect(
            sortByCategoryAction, QtCore.SIGNAL("triggered()"), lambda: self.sort(CATEGORY)
        )
        self.connect(
            sortByDescriptionAction, QtCore.SIGNAL("triggered()"), lambda: self.sort(SHORTDESC)
        )
        self.connect(sortByIDAction, QtCore.SIGNAL("triggered()"), lambda: self.sort(ID))
        self.connect(closeButton, QtCore.SIGNAL("clicked()"), self.accept)

        self.setWindowTitle("Reference Data")

    def addRecord(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, CATEGORY)
        self.view.setCurrentIndex(index)
        self.view.edit(index)

    def deleteRecord(self):
        index = self.view.currentIndex()
        if not index.isValid():
            return
        record = self.model.record(index.row())
        category = record.value(CATEGORY)
        desc = record.value(SHORTDESC)
        if (
            QtWidgets.QMessageBox.question(
                self,
                "Reference Data",
                "Delete {} from category {}?".format(desc, category),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.No
        ):
            return
        self.model.removeRow(index.row())
        self.model.submitAll()

    def sort(self, column):
        self.model.setSort(column, QtCore.Qt.AscendingOrder)
        self.model.select()


def main():
    app = QtWidgets.QApplication(sys.argv)

    filename = os.path.join(os.path.dirname(__file__), "reference.db")
    create = not QtCore.QFile.exists(filename)

    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QtWidgets.QMessageBox.warning(
            None, "Reference Data", "Database Error: {}".format(db.lastError().text())
        )
        sys.exit(1)

    if create:
        query = QtSql.QSqlQuery()
        query.exec_(
            """CREATE TABLE reference (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                category VARCHAR(30) NOT NULL,
                shortdesc VARCHAR(20) NOT NULL,
                longdesc VARCHAR(80))"""
        )

    form = ReferenceDataDlg()
    form.show()
    sys.exit(app.exec())


main()
