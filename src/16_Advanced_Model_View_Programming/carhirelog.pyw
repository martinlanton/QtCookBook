# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import bisect
import os
import sys
from PySide6 import QtWidgets, QtCore, QtGui
import genericdelegates


(
    LICENSE,
    CUSTOMER,
    HIRED,
    MILEAGEOUT,
    RETURNED,
    MILEAGEBACK,
    NOTES,
    MILEAGE,
    DAYS,
) = range(9)


class CarHireLog(object):
    def __init__(
        self,
        license,
        customer,
        hired,
        mileageout,
        returned=QtCore.QDate(),
        mileageback=0,
        notes="",
    ):
        self.license = license  # plain text
        self.customer = customer  # plain text
        self.hired = hired  # QtCore.QDate
        self.mileageout = mileageout  # int
        self.returned = returned  # QtCore.QDate
        self.mileageback = mileageback  # int
        self.notes = notes  # HTML

    def field(self, column):
        if column == LICENSE:
            return self.license
        elif column == CUSTOMER:
            return self.customer
        elif column == HIRED:
            return self.hired
        elif column == MILEAGEOUT:
            return self.mileageout
        elif column == RETURNED:
            return self.returned
        elif column == MILEAGEBACK:
            return self.mileageback
        elif column == NOTES:
            return self.notes
        elif column == MILEAGE:
            return self.mileage()
        elif column == DAYS:
            return self.days()
        assert False

    def mileage(self):
        return 0 if self.mileageback == 0 else self.mileageback - self.mileageout

    def days(self):
        return 0 if not self.returned.isValid() else self.hired.daysTo(self.returned)

    def __hash__(self):
        return super(CarHireLog, self).__hash__()

    def __eq__(self, other):
        if self.hired != other.hired:
            return False
        if self.customer != other.customer:
            return False
        if self.license != other.license:
            return False
        return id(self) == id(other)

    def __lt__(self, other):
        if self.hired < other.hired:
            return True
        if self.customer < other.customer:
            return True
        if self.license < other.license:
            return True
        return id(self) < id(other)


class CarHireModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super(CarHireModel, self).__init__(parent)
        self.logs = []

        # Generate fake data
        import gzip
        import random
        import string

        surname_data = gzip.open(
            os.path.join(os.path.dirname(__file__), "surnames.txt.gz")
        ).read()
        surnames = surname_data.decode("utf-8").splitlines()
        years = ("06 ", "56 ", "07 ", "57 ", "08 ", "58 ")
        titles = ("Ms ", "Mr ", "Ms ", "Mr ", "Ms ", "Mr ", "Dr ")
        notetexts = (
            "Returned <font color=red><b>damaged</b></font>",
            "Returned with <i>empty fuel tank</i>",
            "Customer <b>complained</b> about the <u>engine</u>",
            "Customer <b>complained</b> about the <u>gears</u>",
            "Customer <b>complained</b> about the <u>clutch</u>",
            "Returned <font color=darkred><b>dirty</b></font>",
        )
        today = QtCore.QDate.currentDate()
        for i in range(250):
            license = []
            for c in range(5):
                license.append(random.choice(string.ascii_uppercase))
            license = "".join(license[:2]) + random.choice(years) + "".join(license[2:])
            customer = random.choice(titles) + random.choice(surnames)
            hired = today.addDays(-random.randint(0, 365))
            mileageout = random.randint(10000, 30000)
            notes = ""
            if random.random() >= 0.2:
                days = random.randint(1, 21)
                returned = hired.addDays(days)
                mileageback = mileageout + (days * random.randint(30, 300))
                if random.random() > 0.75:
                    notes = random.choice(notetexts)
            else:
                returned = QtCore.QDate()
                mileageback = 0
            log = CarHireLog(
                license, customer, hired, mileageout, returned, mileageback, notes
            )
            bisect.insort(self.logs, log)

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.logs)

    def columnCount(self, index=QtCore.QModelIndex()):
        return 9

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            log = self.logs[index.row()]
            value = log.field(index.column())
            if index.column() in (MILEAGEBACK, MILEAGE, DAYS) and value == 0:
                return None
            return value
        if role == QtCore.Qt.TextAlignmentRole and index.column() not in (
            LICENSE,
            CUSTOMER,
            NOTES,
        ):
            return int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        if role == QtCore.Qt.ForegroundRole:
            palette = QtWidgets.QApplication.palette()
            if index.column() in (LICENSE, MILEAGE, DAYS):
                return palette.placeholderText()
            else:
                return palette.text()
        if role == QtCore.Qt.BackgroundRole:
            palette = QtWidgets.QApplication.palette()
            return palette.light()
        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if (
            index.isValid()
            and role == QtCore.Qt.EditRole
            and index.column() not in (LICENSE, MILEAGE, DAYS)
        ):
            log = self.logs[index.row()]
            column = index.column()
            if column == CUSTOMER:
                log.customer = value
            elif column == HIRED:
                log.hired = value
            elif column == MILEAGEOUT:
                log.mileageout = int(value)
            elif column == RETURNED:
                log.returned = value
            elif column == MILEAGEBACK:
                log.mileageback = int(value)
            elif column == NOTES:
                log.notes = value
            self.emit(
                QtCore.SIGNAL("dataChanged(QtCore.QModelIndex,QtCore.QModelIndex)"),
                index,
                index,
            )
            return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return int(QtCore.Qt.AlignCenter)
            return int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            if section == LICENSE:
                return "License"
            elif section == CUSTOMER:
                return "Customer"
            elif section == HIRED:
                return "Hired"
            elif section == MILEAGEOUT:
                return "Mileage #1"
            elif section == RETURNED:
                return "Returned"
            elif section == MILEAGEBACK:
                return "Mileage #2"
            elif section == DAYS:
                return "Days"
            elif section == MILEAGE:
                return "Miles"
            elif section == NOTES:
                return "Notes"
        return section + 1

    def flags(self, index):
        flag = QtCore.QAbstractTableModel.flags(self, index)
        if index.column() not in (LICENSE, MILEAGE, DAYS):
            flag |= QtCore.Qt.ItemIsEditable
        return flag


class HireDateColumnDelegate(genericdelegates.DateColumnDelegate):
    def createEditor(self, parent, option, index):
        i = index.sibling(index.row(), RETURNED)
        self.maximum = i.model().data(i, QtCore.Qt.DisplayRole).addDays(-1)
        return genericdelegates.DateColumnDelegate.createEditor(
            self, parent, option, index
        )


class ReturnDateColumnDelegate(genericdelegates.DateColumnDelegate):
    def createEditor(self, parent, option, index):
        i = index.sibling(index.row(), HIRED)
        self.minimum = i.model().data(i, QtCore.Qt.DisplayRole).addDays(1)
        return genericdelegates.DateColumnDelegate.createEditor(
            self, parent, option, index
        )


class MileageOutColumnDelegate(genericdelegates.IntegerColumnDelegate):
    def createEditor(self, parent, option, index):
        i = index.sibling(index.row(), MILEAGEBACK)
        maximum = int(i.model().data(i, QtCore.Qt.DisplayRole))
        self.maximum = 1000000 if maximum == 0 else maximum - 1
        return genericdelegates.IntegerColumnDelegate.createEditor(
            self, parent, option, index
        )


class MileageBackColumnDelegate(genericdelegates.IntegerColumnDelegate):
    def createEditor(self, parent, option, index):
        i = index.sibling(index.row(), MILEAGEOUT)
        self.minimum = int(i.model().data(i, QtCore.Qt.DisplayRole)) + 1
        return genericdelegates.IntegerColumnDelegate.createEditor(
            self, parent, option, index
        )


class MainForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        model = CarHireModel(self)

        self.view = QtWidgets.QTableView()
        self.view.setModel(model)
        self.view.resizeColumnsToContents()

        delegate = genericdelegates.GenericDelegate(self)
        delegate.insertColumnDelegate(
            CUSTOMER, genericdelegates.PlainTextColumnDelegate()
        )
        earliest = QtCore.QDate.currentDate().addYears(-3)
        delegate.insertColumnDelegate(HIRED, HireDateColumnDelegate(earliest))
        delegate.insertColumnDelegate(MILEAGEOUT, MileageOutColumnDelegate(0, 1000000))
        delegate.insertColumnDelegate(RETURNED, ReturnDateColumnDelegate(earliest))
        delegate.insertColumnDelegate(
            MILEAGEBACK, MileageBackColumnDelegate(0, 1000000)
        )
        delegate.insertColumnDelegate(NOTES, genericdelegates.RichTextColumnDelegate())

        self.view.setItemDelegate(delegate)
        self.setCentralWidget(self.view)

        QtGui.QShortcut(QtGui.QKeySequence("Escape"), self, self.close)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)

        self.setWindowTitle("Car Hire Logs")


app = QtWidgets.QApplication(sys.argv)
form = MainForm()
rect = QtGui.QScreen().availableGeometry()
form.resize(int(rect.width() * 0.7), int(rect.height() * 0.8))
form.move(0, 0)
form.show()
app.exec()
