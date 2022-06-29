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
from PySide6 import QtWidgets, QtGui, QtCore, QtSql

#  Since pyrcc is no longer provided with PyQt or PySide, we
#  need to change resources location using the information from this thread :
#  https://stackoverflow.com/questions/66099225/how-can-resources-be-provided-in-pyqt6-which-has-no-pyrcc
# import qrc_resources  # this means this needs to go, and we need to adjust all the resources calls
QtCore.QDir.addSearchPath("resources", "images/")

MAC = "qt_mac_set_native_menubar" in dir()

ID, CALLER, STARTTIME, ENDTIME, TOPIC = range(5)
DATETIME_FORMAT = "yyyy-MM-dd hh:mm"


def createFakeData():
    import random

    print("Dropping table...")
    query = QtSql.QSqlQuery()
    query.exec("DROP TABLE calls")
    QtWidgets.QApplication.processEvents()

    print("Creating table...")
    query.exec(
        """CREATE TABLE calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                caller VARCHAR(40) NOT NULL,
                starttime DATETIME NOT NULL,
                endtime DATETIME NOT NULL,
                topic VARCHAR(80) NOT NULL)"""
    )
    topics = (
        "Complaint",
        "Information request",
        "Off topic",
        "Information supplied",
        "Complaint",
        "Complaint",
    )
    now = QtCore.QDateTime.currentDateTime()
    print("Populating table...")
    query.prepare(
        "INSERT INTO calls (caller, starttime, endtime, " "topic) VALUES (?, ?, ?, ?)"
    )
    for name in (
        "Joshan Cockerall",
        "Ammanie Ingham",
        "Diarmuid Bettington",
        "Juliana Bannister",
        "Oakley-Jay Buxton",
        "Reilley Collinge",
        "Ellis-James Mcgehee",
        "Jazmin Lawton",
        "Lily-Grace Smythe",
        "Coskun Lant",
        "Lauran Lanham",
        "Millar Poindexter",
        "Naqeeb Neild",
        "Maxlee Stoddart",
        "Rebia Luscombe",
        "Briana Christine",
        "Charli Pease",
        "Deena Mais",
        "Havia Huffman",
        "Ethan Davie",
        "Thomas-Jack Silver",
        "Harpret Bray",
        "Leigh-Ann Goodliff",
        "Seoras Bayes",
        "Jenna Underhill",
        "Veena Helps",
        "Mahad Mcintosh",
        "Allie Hazlehurst",
        "Aoife Warrington",
        "Cameron Burton",
        "Yildirim Ahlberg",
        "Alissa Clayton",
        "Josephine Weber",
        "Fiore Govan",
        "Howard Ragsdale",
        "Tiernan Larkins",
        "Seren Sweeny",
        "Arisha Keys",
        "Kiki Wearing",
        "Kyran Ponsonby",
        "Diannon Pepper",
        "Mari Foston",
        "Sunil Manson",
        "Donald Wykes",
        "Rosie Higham",
        "Karmin Raines",
        "Tayyibah Leathem",
        "Kara-jay Knoll",
        "Shail Dalgleish",
        "Jaimie Sells",
    ):
        start = now.addDays(-random.randint(1, 30))
        start = now.addSecs(-random.randint(60 * 5, 60 * 60 * 2))
        end = start.addSecs(random.randint(20, 60 * 13))
        topic = random.choice(topics)
        query.addBindValue(name)
        query.addBindValue(start)
        query.addBindValue(end)
        query.addBindValue(topic)
        query.exec()
    QtWidgets.QApplication.processEvents()

    print("Calls:")
    query.exec(
        "SELECT id, caller, starttime, endtime, topic FROM calls " "ORDER by starttime"
    )
    while query.next():
        id = int(query.value(0))
        caller = query.value(1)
        starttime = query.value(2)
        endtime = query.value(3)
        topic = query.value(4)
        print(
            "{0:02d}: {1} {2} - {3} {4}".format(id, caller, starttime, endtime, topic)
        )
    QtWidgets.QApplication.processEvents()


class PhoneLogDlg(QtWidgets.QDialog):

    FIRST, PREV, NEXT, LAST = range(4)

    def __init__(self, parent=None):
        super(PhoneLogDlg, self).__init__(parent)

        callerLabel = QtWidgets.QLabel("&Caller:")
        self.callerEdit = QtWidgets.QLineEdit()
        callerLabel.setBuddy(self.callerEdit)
        today = QtCore.QDate.currentDate()
        startLabel = QtWidgets.QLabel("&Start:")
        self.startDateTime = QtWidgets.QDateTimeEdit()
        startLabel.setBuddy(self.startDateTime)
        self.startDateTime.setDateRange(today, today)
        self.startDateTime.setDisplayFormat(DATETIME_FORMAT)
        endLabel = QtWidgets.QLabel("&End:")
        self.endDateTime = QtWidgets.QDateTimeEdit()
        endLabel.setBuddy(self.endDateTime)
        self.endDateTime.setDateRange(today, today)
        self.endDateTime.setDisplayFormat(DATETIME_FORMAT)
        topicLabel = QtWidgets.QLabel("&Topic:")
        topicEdit = QtWidgets.QLineEdit()
        topicLabel.setBuddy(topicEdit)
        firstButton = QtWidgets.QPushButton()
        firstButton.setIcon(QtGui.QIcon("resources:first.png"))
        prevButton = QtWidgets.QPushButton()
        prevButton.setIcon(QtGui.QIcon("resources:prev.png"))
        nextButton = QtWidgets.QPushButton()
        nextButton.setIcon(QtGui.QIcon("resources:next.png"))
        lastButton = QtWidgets.QPushButton()
        lastButton.setIcon(QtGui.QIcon("resources:last.png"))
        addButton = QtWidgets.QPushButton("&Add")
        addButton.setIcon(QtGui.QIcon("resources:add.png"))
        deleteButton = QtWidgets.QPushButton("&Delete")
        deleteButton.setIcon(QtGui.QIcon("resources:delete.png"))
        quitButton = QtWidgets.QPushButton("&Quit")
        quitButton.setIcon(QtGui.QIcon("resources:quit.png"))
        if not MAC:
            addButton.setFocusPolicy(QtCore.Qt.NoFocus)
            deleteButton.setFocusPolicy(QtCore.Qt.NoFocus)

        fieldLayout = QtWidgets.QGridLayout()
        fieldLayout.addWidget(callerLabel, 0, 0)
        fieldLayout.addWidget(self.callerEdit, 0, 1, 1, 3)
        fieldLayout.addWidget(startLabel, 1, 0)
        fieldLayout.addWidget(self.startDateTime, 1, 1)
        fieldLayout.addWidget(endLabel, 1, 2)
        fieldLayout.addWidget(self.endDateTime, 1, 3)
        fieldLayout.addWidget(topicLabel, 2, 0)
        fieldLayout.addWidget(topicEdit, 2, 1, 1, 3)
        navigationLayout = QtWidgets.QHBoxLayout()
        navigationLayout.addWidget(firstButton)
        navigationLayout.addWidget(prevButton)
        navigationLayout.addWidget(nextButton)
        navigationLayout.addWidget(lastButton)
        fieldLayout.addLayout(navigationLayout, 3, 0, 1, 2)
        buttonLayout = QtWidgets.QVBoxLayout()
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(deleteButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(fieldLayout)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable("calls")
        self.model.setSort(STARTTIME, QtCore.Qt.AscendingOrder)
        self.model.select()

        self.mapper = QtWidgets.QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.callerEdit, CALLER)
        self.mapper.addMapping(self.startDateTime, STARTTIME)
        self.mapper.addMapping(self.endDateTime, ENDTIME)
        self.mapper.addMapping(topicEdit, TOPIC)
        self.mapper.toFirst()

        self.connect(
            firstButton,
            QtCore.SIGNAL("clicked()"),
            lambda: self.saveRecord(PhoneLogDlg.FIRST),
        )
        self.connect(
            prevButton,
            QtCore.SIGNAL("clicked()"),
            lambda: self.saveRecord(PhoneLogDlg.PREV),
        )
        self.connect(
            nextButton,
            QtCore.SIGNAL("clicked()"),
            lambda: self.saveRecord(PhoneLogDlg.NEXT),
        )
        self.connect(
            lastButton,
            QtCore.SIGNAL("clicked()"),
            lambda: self.saveRecord(PhoneLogDlg.LAST),
        )
        self.connect(addButton, QtCore.SIGNAL("clicked()"), self.addRecord)
        self.connect(deleteButton, QtCore.SIGNAL("clicked()"), self.deleteRecord)
        self.connect(quitButton, QtCore.SIGNAL("clicked()"), self.accept)

        self.setWindowTitle("Phone Log")

    def reject(self):
        self.accept()

    def accept(self):
        self.mapper.submit()
        QtWidgets.QDialog.accept(self)

    def addRecord(self):
        row = self.model.rowCount()
        self.mapper.submit()
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        now = QtCore.QDateTime.currentDateTime()
        self.startDateTime.setDateTime(now)
        self.endDateTime.setDateTime(now)
        self.callerEdit.setFocus()

    def deleteRecord(self):
        caller = self.callerEdit.text()
        starttime = self.startDateTime.dateTime().toString()
        if (
            QtWidgets.QMessageBox.question(
                self,
                "Delete",
                "Delete call made by<br>{} on {}?".format(caller, starttime),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.No
        ):
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)

    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == PhoneLogDlg.FIRST:
            row = 0
        elif where == PhoneLogDlg.PREV:
            row = 0 if row <= 1 else row - 1
        elif where == PhoneLogDlg.NEXT:
            row += 1
            if row >= self.model.rowCount():
                row = self.model.rowCount() - 1
        elif where == PhoneLogDlg.LAST:
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)


def main():
    app = QtWidgets.QApplication(sys.argv)

    filename = os.path.join(os.path.dirname(__file__), "phonelog.db")
    create = not QtCore.QFile.exists(filename)

    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QtWidgets.QMessageBox.warning(
            None, "Phone Log", "Database Error: {}".format(db.lastError().text())
        )
        sys.exit(1)

    splash = None
    if create:
        app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        splash = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("resources:phonelogsplash.png")
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

    form = PhoneLogDlg()
    form.show()
    if create:
        splash.close()
        app.processEvents()
        app.restoreOverrideCursor()
    sys.exit(app.exec())


main()
