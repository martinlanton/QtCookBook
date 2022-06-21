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
import ships

MAC = "qt_mac_set_native_menubar" in dir()


class MainForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        listLabel = QtWidgets.QLabel("&List")
        self.listWidget = QtWidgets.QListWidget()
        listLabel.setBuddy(self.listWidget)

        tableLabel = QtWidgets.QLabel("&Table")
        self.tableWidget = QtWidgets.QTableWidget()
        tableLabel.setBuddy(self.tableWidget)

        treeLabel = QtWidgets.QLabel("Tre&e")
        self.treeWidget = QtWidgets.QTreeWidget()
        treeLabel.setBuddy(self.treeWidget)

        addShipButton = QtWidgets.QPushButton("&Add Ship")
        removeShipButton = QtWidgets.QPushButton("&Remove Ship")
        quitButton = QtWidgets.QPushButton("&Quit")
        if not MAC:
            addShipButton.setFocusPolicy(QtCore.Qt.NoFocus)
            removeShipButton.setFocusPolicy(QtCore.Qt.NoFocus)
            quitButton.setFocusPolicy(QtCore.Qt.NoFocus)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(listLabel)
        vbox.addWidget(self.listWidget)
        widget = QtWidgets.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(tableLabel)
        vbox.addWidget(self.tableWidget)
        widget = QtWidgets.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(treeLabel)
        vbox.addWidget(self.treeWidget)
        widget = QtWidgets.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(addShipButton)
        buttonLayout.addWidget(removeShipButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(
            self.tableWidget,
            QtCore.SIGNAL("itemChanged(QtWidgets.QTableWidgetItem*)"),
            self.tableItemChanged,
        )
        self.connect(addShipButton, QtCore.SIGNAL("clicked()"), self.addShip)
        self.connect(removeShipButton, QtCore.SIGNAL("clicked()"), self.removeShip)
        self.connect(quitButton, QtCore.SIGNAL("clicked()"), self.accept)

        self.ships = ships.ShipContainer("ships.dat")
        self.setWindowTitle("Ships (dict)")
        QtCore.QTimer.singleShot(0, self.initialLoad)

    def initialLoad(self):
        if not QtCore.QFile.exists(self.ships.filename):
            for ship in ships.generateFakeShips():
                self.ships.addShip(ship)
            self.ships.dirty = False
        else:
            try:
                self.ships.load()
            except IOError as e:
                QtWidgets.QMessageBox.warning(
                    self, "Ships - Error", "Failed to load: {}".format(e)
                )
        self.populateList()
        self.populateTable()
        self.tableWidget.sortItems(0)
        self.populateTree()

    def reject(self):
        self.accept()

    def accept(self):
        if (
            self.ships.dirty
            and QtWidgets.QMessageBox.question(
                self,
                "Ships - Save?",
                "Save unsaved changes?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.Yes
        ):
            try:
                self.ships.save()
            except IOError as e:
                QtWidgets.QMessageBox.warning(
                    self, "Ships - Error", "Failed to save: {}".format(e)
                )
        QtWidgets.QDialog.accept(self)

    def populateList(self, selectedShip=None):
        selected = None
        self.listWidget.clear()
        for ship in self.ships.inOrder():
            item = QtWidgets.QListWidgetItem(
                "{} of {}/{} ({:,})".format(
                    ship.name, ship.owner, ship.country, ship.teu
                )
            )
            self.listWidget.addItem(item)
            if selectedShip is not None and selectedShip == id(ship):
                selected = item
        if selected is not None:
            selected.setSelected(True)
            self.listWidget.setCurrentItem(selected)

    def populateTable(self, selectedShip=None):
        selected = None
        self.tableWidget.clear()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setRowCount(len(self.ships))
        headers = ["Name", "Owner", "Country", "Description", "TEU"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        for row, ship in enumerate(self.ships):
            item = QtWidgets.QTableWidgetItem(ship.name)
            item.setData(QtCore.Qt.UserRole, int(id(ship)))
            if selectedShip is not None and selectedShip == id(ship):
                selected = item
            self.tableWidget.setItem(row, ships.NAME, item)
            self.tableWidget.setItem(
                row, ships.OWNER, QtWidgets.QTableWidgetItem(ship.owner)
            )
            self.tableWidget.setItem(
                row, ships.COUNTRY, QtWidgets.QTableWidgetItem(ship.country)
            )
            self.tableWidget.setItem(
                row, ships.DESCRIPTION, QtWidgets.QTableWidgetItem(ship.description)
            )
            item = QtWidgets.QTableWidgetItem("{:10}".format(ship.teu))
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(row, ships.TEU, item)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.resizeColumnsToContents()
        if selected is not None:
            selected.setSelected(True)
            self.tableWidget.setCurrentItem(selected)

    def populateTree(self, selectedShip=None):
        selected = None
        self.treeWidget.clear()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(["Country/Owner/Name", "TEU"])
        self.treeWidget.setItemsExpandable(True)
        parentFromCountry = {}
        parentFromCountryOwner = {}
        for ship in self.ships.inCountryOwnerOrder():
            ancestor = parentFromCountry.get(ship.country)
            if ancestor is None:
                ancestor = QtWidgets.QTreeWidgetItem(self.treeWidget, [ship.country])
                parentFromCountry[ship.country] = ancestor
            countryowner = ship.country + "/" + ship.owner
            parent = parentFromCountryOwner.get(countryowner)
            if parent is None:
                parent = QtWidgets.QTreeWidgetItem(ancestor, [ship.owner])
                parentFromCountryOwner[countryowner] = parent
            item = QtWidgets.QTreeWidgetItem(
                parent, [ship.name, "{:,}".format(ship.teu)]
            )
            item.setTextAlignment(1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            if selectedShip is not None and selectedShip == id(ship):
                selected = item
            self.treeWidget.expandItem(parent)
            self.treeWidget.expandItem(ancestor)
        self.treeWidget.resizeColumnToContents(0)
        self.treeWidget.resizeColumnToContents(1)
        if selected is not None:
            selected.setSelected(True)
            self.treeWidget.setCurrentItem(selected)

    def addShip(self):
        ship = ships.Ship(" Unknown", " Unknown", " Unknown")
        self.ships.addShip(ship)
        self.populateList()
        self.populateTree()
        self.populateTable(id(ship))
        self.tableWidget.setFocus()
        self.tableWidget.editItem(self.tableWidget.currentItem())

    def tableItemChanged(self, item):
        ship = self.currentTableShip()
        if ship is None:
            return
        column = self.tableWidget.currentColumn()
        if column == ships.NAME:
            ship.name = item.text().strip()
        elif column == ships.OWNER:
            ship.owner = item.text().strip()
        elif column == ships.COUNTRY:
            ship.country = item.text().strip()
        elif column == ships.DESCRIPTION:
            ship.description = item.text().strip()
        elif column == ships.TEU:
            ship.teu = int(item.text())
        self.ships.dirty = True
        self.populateList()
        self.populateTree()

    def currentTableShip(self):
        item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if item is None:
            return None
        return self.ships.ship(int(item.data(QtCore.Qt.UserRole)))

    def removeShip(self):
        ship = self.currentTableShip()
        if ship is None:
            return
        if (
            QtWidgets.QMessageBox.question(
                self,
                "Ships - Remove",
                "Remove {} of {}/{}?".format(ship.name, ship.owner, ship.country),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.No
        ):
            return
        self.ships.removeShip(ship)
        self.populateList()
        self.populateTree()
        self.populateTable()


app = QtWidgets.QApplication(sys.argv)
form = MainForm()
form.show()
app.exec_()
