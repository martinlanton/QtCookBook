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
from PySide6 import QtWidgets, QtGui, QtCore, QtSql

# Since pyrcc is no longer provided with PyQt or PySide, we
# need to change resources location using the information from this thread :
# https://stackoverflow.com/questions/66099225/how-can-resources-be-provided-in-pyqt6-which-has-no-pyrcc
# That said PySide6 does still provide an alternative : https://doc.qt.io/qtforpython-6/tutorials/basictutorial/qrcfiles.html
# import qrc_resources  # this means this needs to go, and we need to adjust all the resources calls
QtCore.QDir.addSearchPath("resources", "images/")


MAC = True
try:
    from PyQt4.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

ID = 0
NAME = ASSETID = 1
CATEGORYID = DATE = DESCRIPTION = 2
ROOM = ACTIONID = 3

ACQUIRED = 1


def createFakeData():
    import random

    print("Dropping tables...")
    query = QtSql.QSqlQuery()
    query.exec("DROP TABLE assets")
    query.exec("DROP TABLE logs")
    query.exec("DROP TABLE actions")
    query.exec("DROP TABLE categories")
    QtWidgets.QApplication.processEvents()

    print("Creating tables...")
    query.exec(
        """CREATE TABLE actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(20) NOT NULL,
                description VARCHAR(40) NOT NULL)"""
    )
    query.exec(
        """CREATE TABLE categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(20) NOT NULL,
                description VARCHAR(40) NOT NULL)"""
    )
    query.exec(
        """CREATE TABLE assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(40) NOT NULL,
                categoryid INTEGER NOT NULL,
                room VARCHAR(4) NOT NULL,
                FOREIGN KEY (categoryid) REFERENCES categories)"""
    )
    query.exec(
        """CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                assetid INTEGER NOT NULL,
                date DATE NOT NULL,
                actionid INTEGER NOT NULL,
                FOREIGN KEY (assetid) REFERENCES assets,
                FOREIGN KEY (actionid) REFERENCES actions)"""
    )
    QtWidgets.QApplication.processEvents()

    print("Populating tables...")
    query.exec(
        "INSERT INTO actions (name, description) "
        "VALUES ('Acquired', 'When installed')"
    )
    query.exec(
        "INSERT INTO actions (name, description) "
        "VALUES ('Broken', 'When failed and unusable')"
    )
    query.exec(
        "INSERT INTO actions (name, description) "
        "VALUES ('Repaired', 'When back in service')"
    )
    query.exec(
        "INSERT INTO actions (name, description) "
        "VALUES ('Routine maintenance', "
        "'When tested, refilled, etc.')"
    )
    query.exec(
        "INSERT INTO categories (name, description) VALUES "
        "('Computer Equipment', "
        "'Monitors, System Units, Peripherals, etc.')"
    )
    query.exec(
        "INSERT INTO categories (name, description) VALUES "
        "('Furniture', 'Chairs, Tables, Desks, etc.')"
    )
    query.exec(
        "INSERT INTO categories (name, description) VALUES "
        "('Electrical Equipment', 'Non-computer electricals')"
    )
    today = QtCore.QDate.currentDate()
    floors = list(range(1, 12)) + list(range(14, 28))
    monitors = (
        ('17" LCD Monitor', 1),
        ('20" LCD Monitor', 1),
        ('21" LCD Monitor', 1),
        ('21" CRT Monitor', 1),
        ('24" CRT Monitor', 1),
    )
    computers = (
        ("Computer (32-bit/80GB/0.5GB)", 1),
        ("Computer (32-bit/100GB/1GB)", 1),
        ("Computer (32-bit/120GB/1GB)", 1),
        ("Computer (64-bit/240GB/2GB)", 1),
        ("Computer (64-bit/320GB/4GB)", 1),
    )
    printers = (
        ("Laser Printer (4 ppm)", 1),
        ("Laser Printer (6 ppm)", 1),
        ("Laser Printer (8 ppm)", 1),
        ("Laser Printer (16 ppm)", 1),
    )
    chairs = (
        ("Secretary Chair", 2),
        ("Executive Chair (Basic)", 2),
        ("Executive Chair (Ergonimic)", 2),
        ("Executive Chair (Hi-Tech)", 2),
    )
    desks = (
        ("Desk (Basic, 3 drawer)", 2),
        ("Desk (Standard, 3 drawer)", 2),
        ("Desk (Executive, 3 drawer)", 2),
        ("Desk (Executive, 4 drawer)", 2),
        ("Desk (Large, 4 drawer)", 2),
    )
    furniture = (
        ("Filing Cabinet (3 drawer)", 2),
        ("Filing Cabinet (4 drawer)", 2),
        ("Filing Cabinet (5 drawer)", 2),
        ("Bookcase (4 shelves)", 2),
        ("Bookcase (6 shelves)", 2),
        ("Table (4 seater)", 2),
        ("Table (8 seater)", 2),
        ("Table (12 seater)", 2),
    )
    electrical = (
        ("Fan (3 speed)", 3),
        ("Fan (5 speed)", 3),
        ("Photocopier (4 ppm)", 3),
        ("Photocopier (6 ppm)", 3),
        ("Photocopier (8 ppm)", 3),
        ("Shredder", 3),
    )
    query.prepare(
        "INSERT INTO assets (name, categoryid, room) "
        "VALUES (:name, :categoryid, :room)"
    )
    logQuery = QtSql.QSqlQuery()
    logQuery.prepare(
        "INSERT INTO logs (assetid, date, actionid) "
        "VALUES (:assetid, :date, :actionid)"
    )
    assetid = 1
    for i in range(20):
        room = "{0:02d}{1:02d}".format(random.choice(floors), random.randint(1, 62))
        for name, category in (
            random.choice(monitors),
            random.choice(computers),
            random.choice(chairs),
            random.choice(desks),
            random.choice(furniture),
        ):
            query.bindValue(":name", name)
            query.bindValue(":categoryid", category)
            query.bindValue(":room", room)
            query.exec()
            logQuery.bindValue(":assetid", assetid)
            when = today.addDays(-random.randint(7, 1500))
            logQuery.bindValue(":date", when)
            logQuery.bindValue(":actionid", ACQUIRED)
            logQuery.exec()
            if random.random() > 0.7:
                logQuery.bindValue(":assetid", assetid)
                when = when.addDays(random.randint(1, 1500))
                if when <= today:
                    logQuery.bindValue(":date", when)
                    logQuery.bindValue(":actionid", random.choice((2, 4)))
                    logQuery.exec()
            assetid += 1
        if random.random() > 0.8:
            name, category = random.choice(printers)
            query.bindValue(":name", name)
            query.bindValue(":categoryid", category)
            query.bindValue(":room", room)
            query.exec()
            logQuery.bindValue(":assetid", assetid)
            when = today.addDays(-random.randint(7, 1500))
            logQuery.bindValue(":date", when)
            logQuery.bindValue(":actionid", ACQUIRED)
            logQuery.exec()
            if random.random() > 0.6:
                logQuery.bindValue(":assetid", assetid)
                when = when.addDays(random.randint(1, 1500))
                if when <= today:
                    logQuery.bindValue(":date", when)
                    logQuery.bindValue(":actionid", random.choice((2, 4)))
                    logQuery.exec()
            assetid += 1
        if random.random() > 0.6:
            name, category = random.choice(electrical)
            query.bindValue(":name", name)
            query.bindValue(":categoryid", category)
            query.bindValue(":room", room)
            query.exec()
            logQuery.bindValue(":assetid", assetid)
            when = today.addDays(-random.randint(7, 1500))
            logQuery.bindValue(":date", when)
            logQuery.bindValue(":actionid", ACQUIRED)
            logQuery.exec()
            if random.random() > 0.5:
                logQuery.bindValue(":assetid", assetid)
                when = when.addDays(random.randint(1, 1500))
                if when <= today:
                    logQuery.bindValue(":date", when)
                    logQuery.bindValue(":actionid", random.choice((2, 4)))
                    logQuery.exec()
            assetid += 1
        QtWidgets.QApplication.processEvents()

    print("Assets:")
    query.exec("SELECT id, name, categoryid, room FROM assets " "ORDER by id")
    categoryQuery = QtSql.QSqlQuery()
    while query.next():
        id = int(query.value(0))
        name = query.value(1)
        categoryid = int(query.value(2))
        room = query.value(3)
        categoryQuery.exec(
            "SELECT name FROM categories " "WHERE id = {}".format(categoryid)
        )
        category = "{}".format(categoryid)
        if categoryQuery.next():
            category = categoryQuery.value(0)
        print("{0}: {1} [{2}] {3}".format(id, name, category, room))
    QtWidgets.QApplication.processEvents()


class ReferenceDataDlg(QtWidgets.QDialog):
    def __init__(self, table, title, parent=None):
        super(ReferenceDataDlg, self).__init__(parent)

        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable(table)
        self.model.setSort(NAME, QtCore.Qt.AscendingOrder)
        self.model.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(NAME, QtCore.Qt.Horizontal, "Name")
        self.model.setHeaderData(DESCRIPTION, QtCore.Qt.Horizontal, "Description")
        self.model.select()

        self.view = QtWidgets.QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.view.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.view.setColumnHidden(ID, True)
        self.view.resizeColumnsToContents()

        addButton = QtWidgets.QPushButton("&Add")
        deleteButton = QtWidgets.QPushButton("&Delete")
        okButton = QtWidgets.QPushButton("&OK")
        if not MAC:
            addButton.setFocusPolicy(QtCore.Qt.NoFocus)
            deleteButton.setFocusPolicy(QtCore.Qt.NoFocus)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(deleteButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(addButton, QtCore.SIGNAL("clicked()"), self.addRecord)
        self.connect(deleteButton, QtCore.SIGNAL("clicked()"), self.deleteRecord)
        self.connect(okButton, QtCore.SIGNAL("clicked()"), self.accept)

        self.setWindowTitle("Asset Manager - Edit {} Reference Data".format(title))

    def addRecord(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, NAME)
        self.view.setCurrentIndex(index)
        self.view.edit(index)

    def deleteRecord(self):
        index = self.view.currentIndex()
        if not index.isValid():
            return
        # QtSql.QSqlDatabase.database().transaction()
        record = self.model.record(index.row())
        id = int(record.value(ID))
        table = self.model.tableName()
        query = QtSql.QSqlQuery()
        if table == "actions":
            query.exec("SELECT COUNT(*) FROM logs " "WHERE actionid = {}".format(id))
        elif table == "categories":
            query.exec(
                "SELECT COUNT(*) FROM assets " "WHERE categoryid = {}".format(id)
            )
        count = 0
        if query.next():
            count = int(query.value(0))
        if count:
            QtWidgets.QMessageBox.information(
                self,
                "Delete {}".format(table),
                "Cannot delete {}<br>"
                "from the {} table because it is used by "
                "{} records".format(record.value(NAME), table, count),
            )
            # QtSql.QSqlDatabase.database().rollback()
            return
        self.model.removeRow(index.row())
        self.model.submitAll()
        # QtSql.QSqlDatabase.database().commit()


class AssetDelegate(QtSql.QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(AssetDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        myoption = QtWidgets.QStyleOptionViewItem(option)
        if index.column() == ROOM:
            myoption.displayAlignment |= QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        QtSql.QSqlRelationalDelegate.paint(self, painter, myoption, index)

    def createEditor(self, parent, option, index):
        if index.column() == ROOM:
            editor = QtWidgets.QLineEdit(parent)
            regex = QtCore.QRegularExpression(
                r"(?:0[1-9]|1[0124-9]|2[0-7])" r"(?:0[1-9]|[1-5][0-9]|6[012])"
            )
            validator = QtGui.QRegularExpressionValidator(regex, parent)
            editor.setValidator(validator)
            editor.setInputMask("9999")
            editor.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            return editor
        else:
            return QtSql.QSqlRelationalDelegate.createEditor(
                self, parent, option, index
            )

    def setEditorData(self, editor, index):
        if index.column() == ROOM:
            text = index.model().data(index, QtCore.Qt.DisplayRole)
            editor.setText(text)
        else:
            QtSql.QSqlRelationalDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        if index.column() == ROOM:
            model.setData(index, editor.text())
        else:
            QtSql.QSqlRelationalDelegate.setModelData(self, editor, model, index)


class LogDelegate(QtSql.QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(LogDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        myoption = QtWidgets.QStyleOptionViewItem(option)
        if index.column() == DATE:
            myoption.displayAlignment |= QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        QtSql.QSqlRelationalDelegate.paint(self, painter, myoption, index)

    def createEditor(self, parent, option, index):
        if index.column() == ACTIONID:
            text = index.model().data(index, QtCore.Qt.DisplayRole)
            if text.isdigit() and int(text) == ACQUIRED:
                return  # Acquired is read-only
        if index.column() == DATE:
            editor = QtWidgets.QDateEdit(parent)
            editor.setMaximumDate(QtCore.QDate.currentDate())
            editor.setDisplayFormat("yyyy-MM-dd")
            editor.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            return editor
        else:
            return QtSql.QSqlRelationalDelegate.createEditor(
                self, parent, option, index
            )

    def setEditorData(self, editor, index):
        if index.column() == DATE:
            date = index.model().data(index, QtCore.Qt.DisplayRole)
            editor.setDate(date)
        else:
            QtSql.QSqlRelationalDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        if index.column() == DATE:
            model.setData(index, editor.date())
        else:
            QtSql.QSqlRelationalDelegate.setModelData(self, editor, model, index)


class MainForm(QtWidgets.QDialog):
    def __init__(self):
        super(MainForm, self).__init__()

        self.assetModel = QtSql.QSqlRelationalTableModel(self)
        self.assetModel.setTable("assets")
        self.assetModel.setRelation(
            CATEGORYID, QtSql.QSqlRelation("categories", "id", "name")
        )
        self.assetModel.setSort(ROOM, QtCore.Qt.AscendingOrder)
        self.assetModel.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        self.assetModel.setHeaderData(NAME, QtCore.Qt.Horizontal, "Name")
        self.assetModel.setHeaderData(CATEGORYID, QtCore.Qt.Horizontal, "Category")
        self.assetModel.setHeaderData(ROOM, QtCore.Qt.Horizontal, "Room")
        self.assetModel.select()

        self.assetView = QtWidgets.QTableView()
        self.assetView.setModel(self.assetModel)
        self.assetView.setItemDelegate(AssetDelegate(self))
        self.assetView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.assetView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.assetView.setColumnHidden(ID, True)
        self.assetView.resizeColumnsToContents()
        assetLabel = QtWidgets.QLabel("A&ssets")
        assetLabel.setBuddy(self.assetView)

        self.logModel = QtSql.QSqlRelationalTableModel(self)
        self.logModel.setTable("logs")
        self.logModel.setRelation(ACTIONID, QtSql.QSqlRelation("actions", "id", "name"))
        self.logModel.setSort(DATE, QtCore.Qt.AscendingOrder)
        self.logModel.setHeaderData(DATE, QtCore.Qt.Horizontal, "Date")
        self.logModel.setHeaderData(ACTIONID, QtCore.Qt.Horizontal, "Action")
        self.logModel.select()

        self.logView = QtWidgets.QTableView()
        self.logView.setModel(self.logModel)
        self.logView.setItemDelegate(LogDelegate(self))
        self.logView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.logView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.logView.setColumnHidden(ID, True)
        self.logView.setColumnHidden(ASSETID, True)
        self.logView.resizeColumnsToContents()
        self.logView.horizontalHeader().setStretchLastSection(True)
        logLabel = QtWidgets.QLabel("&Logs")
        logLabel.setBuddy(self.logView)

        addAssetButton = QtWidgets.QPushButton("&Add Asset")
        deleteAssetButton = QtWidgets.QPushButton("&Delete Asset")
        addActionButton = QtWidgets.QPushButton("Add A&ction")
        deleteActionButton = QtWidgets.QPushButton("Delete Ac&tion")
        editActionsButton = QtWidgets.QPushButton("&Edit Actions...")
        editCategoriesButton = QtWidgets.QPushButton("Ed&it Categories...")
        quitButton = QtWidgets.QPushButton("&Quit")
        for button in (
            addAssetButton,
            deleteAssetButton,
            addActionButton,
            deleteActionButton,
            editActionsButton,
            editCategoriesButton,
            quitButton,
        ):
            if MAC:
                button.setDefault(False)
                button.setAutoDefault(False)
            else:
                button.setFocusPolicy(QtCore.Qt.NoFocus)

        dataLayout = QtWidgets.QVBoxLayout()
        dataLayout.addWidget(assetLabel)
        dataLayout.addWidget(self.assetView, 1)
        dataLayout.addWidget(logLabel)
        dataLayout.addWidget(self.logView)
        buttonLayout = QtWidgets.QVBoxLayout()
        buttonLayout.addWidget(addAssetButton)
        buttonLayout.addWidget(deleteAssetButton)
        buttonLayout.addWidget(addActionButton)
        buttonLayout.addWidget(deleteActionButton)
        buttonLayout.addWidget(editActionsButton)
        buttonLayout.addWidget(editCategoriesButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(dataLayout, 1)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(
            self.assetView.selectionModel(),
            QtCore.SIGNAL(("currentRowChanged(QModelIndex,QModelIndex)")),
            self.assetChanged,
        )
        self.connect(addAssetButton, QtCore.SIGNAL("clicked()"), self.addAsset)
        self.connect(deleteAssetButton, QtCore.SIGNAL("clicked()"), self.deleteAsset)
        self.connect(addActionButton, QtCore.SIGNAL("clicked()"), self.addAction)
        self.connect(deleteActionButton, QtCore.SIGNAL("clicked()"), self.deleteAction)
        self.connect(editActionsButton, QtCore.SIGNAL("clicked()"), self.editActions)
        self.connect(
            editCategoriesButton, QtCore.SIGNAL("clicked()"), self.editCategories
        )
        self.connect(quitButton, QtCore.SIGNAL("clicked()"), self.done)

        self.assetChanged(self.assetView.currentIndex())
        self.setMinimumWidth(650)
        self.setWindowTitle("Asset Manager")

    def done(self, result=1):
        query = QtSql.QSqlQuery()
        query.exec(
            "DELETE FROM logs WHERE logs.assetid NOT IN" "(SELECT id FROM assets)"
        )
        QtWidgets.QDialog.done(self, 1)

    def assetChanged(self, index):
        if index.isValid():
            record = self.assetModel.record(index.row())
            id = int(record.value("id"))
            self.logModel.setFilter("assetid = {}".format(id))
        else:
            self.logModel.setFilter("assetid = -1")
        self.logModel.select()
        self.logView.horizontalHeader().setVisible(self.logModel.rowCount() > 0)

    def addAsset(self):
        row = (
            self.assetView.currentIndex().row()
            if self.assetView.currentIndex().isValid()
            else 0
        )

        QtSql.QSqlDatabase.database().transaction()
        self.assetModel.insertRow(row)
        index = self.assetModel.index(row, NAME)
        self.assetView.setCurrentIndex(index)

        assetid = 1
        query = QtSql.QSqlQuery()
        query.exec("SELECT MAX(id) FROM assets")
        if query.next():
            assetid = int(query.value(0))
        query.prepare(
            "INSERT INTO logs (assetid, date, actionid) "
            "VALUES (:assetid, :date, :actionid)"
        )
        query.bindValue(":assetid", assetid + 1)
        query.bindValue(":date", QtCore.QDate.currentDate())
        query.bindValue(":actionid", ACQUIRED)
        query.exec()
        QtSql.QSqlDatabase.database().commit()
        self.assetView.edit(index)

    def deleteAsset(self):
        index = self.assetView.currentIndex()
        if not index.isValid():
            return
        QtSql.QSqlDatabase.database().transaction()
        record = self.assetModel.record(index.row())
        assetid = int(record.value(ID))
        logrecords = 1
        query = QtSql.QSqlQuery(
            "SELECT COUNT(*) FROM logs WHERE assetid = {}".format(assetid)
        )
        if query.next():
            logrecords = int(query.value(0))
        msg = "<font color=red>Delete</font><br><b>{}</b>" "<br>from room {}".format(
            record.value(NAME), record.value(ROOM)
        )
        if logrecords > 1:
            msg += ", along with {} log records".format(logrecords)
        msg += "?"
        if (
            QtWidgets.QMessageBox.question(
                self,
                "Delete Asset",
                msg,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.No
        ):
            QtSql.QSqlDatabase.database().rollback()
            return
        query.exec("DELETE FROM logs WHERE assetid = {}".format(assetid))
        self.assetModel.removeRow(index.row())
        self.assetModel.submitAll()
        QtSql.QSqlDatabase.database().commit()
        self.assetChanged(self.assetView.currentIndex())

    def addAction(self):
        index = self.assetView.currentIndex()
        if not index.isValid():
            return
        QtSql.QSqlDatabase.database().transaction()
        record = self.assetModel.record(index.row())
        assetid = int(record.value(ID))

        row = self.logModel.rowCount()
        self.logModel.insertRow(row)
        self.logModel.setData(self.logModel.index(row, ASSETID), assetid)
        self.logModel.setData(
            self.logModel.index(row, DATE), QtCore.QDate.currentDate()
        )
        QtSql.QSqlDatabase.database().commit()
        index = self.logModel.index(row, ACTIONID)
        self.logView.setCurrentIndex(index)
        self.logView.edit(index)

    def deleteAction(self):
        index = self.logView.currentIndex()
        if not index.isValid():
            return
        record = self.logModel.record(index.row())
        action = record.value(ACTIONID)
        if action == "Acquired":
            QtWidgets.QMessageBox.information(
                self,
                "Delete Log",
                "The 'Acquired' log record cannot be deleted.<br>"
                "You could delete the entire asset instead.",
            )
            return
        when = record.value(DATE)
        if (
            QtWidgets.QMessageBox.question(
                self,
                "Delete Log",
                "Delete log<br>{} {}?".format(when, action),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.No
        ):
            return
        self.logModel.removeRow(index.row())
        self.logModel.submitAll()

    def editActions(self):
        form = ReferenceDataDlg("actions", "Action", self)
        form.exec()

    def editCategories(self):
        form = ReferenceDataDlg("categories", "Category", self)
        form.exec()


def main():
    app = QtWidgets.QApplication(sys.argv)

    filename = os.path.join(os.path.dirname(__file__), "assets.db")
    create = not QtCore.QFile.exists(filename)
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QtWidgets.QMessageBox.warning(
            None, "Asset Manager", "Database Error: {}".format(db.lastError().text())
        )
        sys.exit(1)

    splash = None
    if create:
        app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        splash = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("resources:assetmanagersplash.png")
        splash.setPixmap(pixmap)
        splash.setMask(pixmap.createHeuristicMask())
        splash.setWindowFlags(QtCore.Qt.SplashScreen)
        rect = QtGui.QScreen().availableGeometry()
        splash.move(
            (rect.width() - pixmap.width()) / 2, (rect.height() - pixmap.height()) / 2
        )
        splash.show()
        app.processEvents()
        createFakeData()

    form = MainForm()
    form.show()
    if create:
        splash.close()
        app.processEvents()
        app.restoreOverrideCursor()
    app.exec()
    del form
    del db


main()
