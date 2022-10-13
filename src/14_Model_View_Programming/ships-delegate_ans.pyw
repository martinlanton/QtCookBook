# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import re
import sys
from PySide6 import QtWidgets, QtCore

import ships_ans as ships

MAC = "qt_mac_set_native_menubar" in dir()


class MainForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = ships.ShipTableModel("ships.dat")
        tableLabel1 = QtWidgets.QLabel("Table &1")
        self.tableView1 = QtWidgets.QTableView()
        tableLabel1.setBuddy(self.tableView1)
        self.tableView1.setModel(self.model)
        self.tableView1.setItemDelegate(ships.ShipDelegate(self))
        tableLabel2 = QtWidgets.QLabel("Table &2")
        self.tableView2 = QtWidgets.QTableView()
        tableLabel2.setBuddy(self.tableView2)
        self.tableView2.setModel(self.model)
        self.tableView2.setItemDelegate(ships.ShipDelegate(self))

        addShipButton = QtWidgets.QPushButton("&Add Ship")
        removeShipButton = QtWidgets.QPushButton("&Remove Ship")
        exportButton = QtWidgets.QPushButton("E&xport...")
        quitButton = QtWidgets.QPushButton("&Quit")
        if not MAC:
            addShipButton.setFocusPolicy(QtCore.Qt.NoFocus)
            removeShipButton.setFocusPolicy(QtCore.Qt.NoFocus)
            exportButton.setFocusPolicy(QtCore.Qt.NoFocus)
            quitButton.setFocusPolicy(QtCore.Qt.NoFocus)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(addShipButton)
        buttonLayout.addWidget(removeShipButton)
        buttonLayout.addWidget(exportButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(tableLabel1)
        vbox.addWidget(self.tableView1)
        widget = QtWidgets.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(tableLabel2)
        vbox.addWidget(self.tableView2)
        widget = QtWidgets.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        for tableView in (self.tableView1, self.tableView2):
            header = tableView.horizontalHeader()
            self.connect(header, QtCore.SIGNAL("sectionClicked(int)"), self.sortTable)
        self.connect(addShipButton, QtCore.SIGNAL("clicked()"), self.addShip)
        self.connect(removeShipButton, QtCore.SIGNAL("clicked()"), self.removeShip)
        self.connect(exportButton, QtCore.SIGNAL("clicked()"), self.export)
        self.connect(quitButton, QtCore.SIGNAL("clicked()"), self.accept)

        self.setWindowTitle("Ships (delegate)")
        QtCore.QTimer.singleShot(0, self.initialLoad)

    def initialLoad(self):
        if not QtCore.QFile.exists(self.model.filename):
            self.model.beginResetModel()
            for ship in ships.generateFakeShips():
                self.model.ships.append(ship)
                self.model.owners.add(ship.owner)
                self.model.countries.add(ship.country)
            self.model.endResetModel()
            self.model.dirty = False
        else:
            try:
                self.model.load()
            except IOError as e:
                QtWidgets.QMessageBox.warning(
                    self, "Ships - Error", "Failed to load: {}".format(e)
                )
        self.model.sortByName()
        self.resizeColumns()

    def resizeColumns(self):
        self.tableView1.resizeColumnsToContents()
        self.tableView2.resizeColumnsToContents()

    def reject(self):
        self.accept()

    def accept(self):
        if (
            self.model.dirty
            and QtWidgets.QMessageBox.question(
                self,
                "Ships - Save?",
                "Save unsaved changes?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.Yes
        ):
            try:
                self.model.save()
            except IOError as e:
                QtWidgets.QMessageBox.warning(
                    self, "Ships - Error", "Failed to save: {}".format(e)
                )
        QtWidgets.QDialog.accept(self)

    def sortTable(self, section):
        if section in (ships.OWNER, ships.COUNTRY):
            self.model.sortByCountryOwner()
        elif section == ships.TEU:
            self.model.sortByTEU()
        else:
            self.model.sortByName()
        self.resizeColumns()

    def addShip(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, 0)
        tableView = self.tableView1
        if self.tableView2.hasFocus():
            tableView = self.tableView2
        tableView.setFocus()
        tableView.setCurrentIndex(index)
        tableView.edit(index)

    def removeShip(self):
        tableView = self.tableView1
        if self.tableView2.hasFocus():
            tableView = self.tableView2
        index = tableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        name = self.model.data(self.model.index(row, ships.NAME))
        owner = self.model.data(self.model.index(row, ships.OWNER))
        country = self.model.data(self.model.index(row, ships.COUNTRY))
        if (
            QtWidgets.QMessageBox.question(
                self,
                "Ships - Remove",
                "Remove {} of {}/{}?".format(name, owner, country),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.No
        ):
            return
        self.model.removeRow(row)
        self.resizeColumns()

    def export(self):
        filename, filtering = QtWidgets.QFileDialog.getSaveFileName(
            self, "Ships - Choose Export File", ".", "Export files (*.txt)"
        )
        if not filename:
            return
        htmlTags = re.compile(r"<[^>]+?>")
        nonDigits = re.compile("[., ]")
        self.model.sortByCountryOwner()
        fh = None
        try:
            fh = QtCore.QFile(filename)
            if not fh.open(QtCore.QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setCodec("UTF-8")
            for row in range(self.model.rowCount()):
                name = self.model.data(self.model.index(row, ships.NAME))
                owner = self.model.data(self.model.index(row, ships.OWNER))
                country = self.model.data(self.model.index(row, ships.COUNTRY))
                teu = self.model.data(self.model.index(row, ships.TEU))
                teu = int(nonDigits.sub("", teu))
                description = self.model.data(self.model.index(row, ships.DESCRIPTION))
                description = htmlTags.sub("", description)
                (
                    stream
                    << name
                    << "|"
                    << owner
                    << "|"
                    << country
                    << "|"
                    << teu
                    << "|"
                    << description
                    << "\n"
                )
        except EnvironmentError as e:
            QtWidgets.QMessageBox.warning(self, "Ships - Error", "Failed to export: {}".format(e))
        finally:
            if fh:
                fh.close()
        QtWidgets.QMessageBox.warning(
            self, "Ships - Export", "Successfully exported ship to {}".format(filename)
        )

app = QtWidgets.QApplication(sys.argv)
form = MainForm()
form.show()
app.exec()