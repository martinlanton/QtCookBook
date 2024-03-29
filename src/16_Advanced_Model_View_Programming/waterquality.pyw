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

import gzip
import os
import platform
import sys
from PySide6 import QtWidgets, QtCore, QtGui


(
    TIMESTAMP,
    TEMPERATURE,
    INLETFLOW,
    TURBIDITY,
    CONDUCTIVITY,
    COAGULATION,
    RAWPH,
    FLOCCULATEDPH,
) = range(8)

TIMESTAMPFORMAT = "yyyy-MM-dd hh:mm"


class WaterQualityModel(QtCore.QAbstractTableModel):
    def __init__(self, filename):
        super(WaterQualityModel, self).__init__()
        self.filename = filename
        self.results = []

    def load(self):
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for loading")
            self.beginResetModel()
            self.results = []
            line_data = gzip.open(self.filename).read()
            for line in line_data.decode("utf-8").splitlines():
                parts = line.rstrip().split(",")
                date = QtCore.QDateTime.fromString(parts[0] + ":00", QtCore.Qt.ISODate)
                result = [date]
                for part in parts[1:]:
                    result.append(float(part))
                self.results.append(result)
        except (IOError, ValueError) as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            self.endResetModel()
            if exception is not None:
                raise exception

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.results)):
            return None
        column = index.column()
        result = self.results[index.row()]
        if role == QtCore.Qt.DisplayRole:
            item = result[column]
            if column == TIMESTAMP:
                item = item
            else:
                item = "{:.2f}".format(item)
            return item
        elif role == QtCore.Qt.TextAlignmentRole:
            if column != TIMESTAMP:
                return int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            return int(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # QtCore.Qt.TextColorRole no longer exist, replace with QtCore.Qt.ForegroundRole
        elif role == QtCore.Qt.ForegroundRole and column == INLETFLOW:
            if result[column] < 0:
                return QtGui.QColor(QtCore.Qt.red)
        # QtCore.Qt.TextColorRole no longer exist, replace with QtCore.Qt.ForegroundRole
        elif role == QtCore.Qt.ForegroundRole and column in (RAWPH, FLOCCULATEDPH):
            ph = result[column]
            if ph < 7:
                return QtGui.QColor(QtCore.Qt.red)
            elif ph >= 8:
                return QtGui.QColor(QtCore.Qt.blue)
            else:
                return QtGui.QColor(QtCore.Qt.darkGreen)
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return int(QtCore.Qt.AlignCenter)
            return int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            if section == TIMESTAMP:
                return "Timestamp"
            elif section == TEMPERATURE:
                return "\u00B0" + "C"
            elif section == INLETFLOW:
                return "Inflow"
            elif section == TURBIDITY:
                return "NTU"
            elif section == CONDUCTIVITY:
                return "\u03BCS/cm"
            elif section == COAGULATION:
                return "mg/L"
            elif section == RAWPH:
                return "Raw Ph"
            elif section == FLOCCULATEDPH:
                return "Floc Ph"
        return int(section + 1)

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.results)

    def columnCount(self, index=QtCore.QModelIndex()):
        return 8


class WaterQualityView(QtWidgets.QWidget):

    FLOWCHARS = (chr(0x21DC), chr(0x21DD), chr(0x21C9))

    def __init__(self, parent=None):
        super(WaterQualityView, self).__init__(parent)
        self.scrollarea = None
        self.model = None
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.selectedRow = -1
        self.flowfont = self.font()
        size = self.font().pointSize()
        if platform.system() == "Windows":
            # The constructor for QtGui.QFontDatabase is deprecated, the methods should
            # be called as classmethods instead, as follows
            for face in [face.lower() for face in QtGui.QFontDatabase.families()]:
                if face.find("unicode") >= 0:
                    self.flowfont = QtGui.QFont(face, size)
                    break
            else:
                self.flowfont = QtGui.QFont("symbol", size)
                WaterQualityView.FLOWCHARS = (chr(0xAC), chr(0xAE), chr(0xDE))

    def setModel(self, model):
        self.model = model
        self.connect(
            self.model,
            QtCore.SIGNAL("dataChanged(QtCore.QModelIndex,QtCore.QModelIndex)"),
            self.setNewSize,
        )
        self.connect(self.model, QtCore.SIGNAL("modelReset()"), self.setNewSize)
        self.setNewSize()

    def setNewSize(self):
        self.resize(self.sizeHint())
        self.update()
        self.updateGeometry()

    def minimumSizeHint(self):
        size = self.sizeHint()
        fm = QtGui.QFontMetrics(self.font())
        size.setHeight(fm.height() * 3)
        return size

    def sizeHint(self):
        fm = QtGui.QFontMetrics(self.font())
        size = fm.height()
        return QtCore.QSize(
            fm.horizontalAdvance("9999-99-99 99:99 ") + (size * 4),
            (size / 4) + (size * self.model.rowCount()),
        )

    def paintEvent(self, event):
        if self.model is None:
            return
        fm = QtGui.QFontMetrics(self.font())
        timestampWidth = fm.horizontalAdvance("9999-99-99 99:99 ")
        size = fm.height()
        indicatorSize = int(size * 0.8)
        offset = int(1.5 * (size - indicatorSize))
        minY = event.rect().y()
        maxY = minY + event.rect().height() + size
        minY -= size
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        y = 0
        for row in range(self.model.rowCount()):
            x = 0
            if minY <= y <= maxY:
                painter.save()
                painter.setPen(self.palette().color(QtGui.QPalette.Text))
                if row == self.selectedRow:
                    painter.fillRect(
                        x,
                        int(y + (offset * 0.8)),
                        self.width(),
                        size,
                        self.palette().highlight(),
                    )
                    painter.setPen(self.palette().color(QtGui.QPalette.HighlightedText))
                timestamp = self.model.data(self.model.index(row, TIMESTAMP))
                painter.drawText(x, y + size, timestamp.toString("yyyy-MM-dd hh:mm"))
                x += timestampWidth
                temperature = float(self.model.data(self.model.index(row, TEMPERATURE)))
                if temperature < 20:
                    color = QtGui.QColor(0, 0, int(255 * (20 - temperature) / 20))
                elif temperature > 25:
                    color = QtGui.QColor(int(255 * temperature / 100), 0, 0)
                else:
                    color = QtGui.QColor(0, int(255 * temperature / 100), 0)
                painter.setPen(QtCore.Qt.NoPen)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize, indicatorSize)
                x += size
                rawPh = float(self.model.data(self.model.index(row, RAWPH)))
                if rawPh < 7:
                    color = QtGui.QColor(int(255 * rawPh / 10), 0, 0)
                elif rawPh >= 8:
                    color = QtGui.QColor(0, 0, int(255 * rawPh / 10))
                else:
                    color = QtGui.QColor(0, int(255 * rawPh / 10), 0)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize, indicatorSize)
                x += size
                flocPh = float(self.model.data(self.model.index(row, FLOCCULATEDPH)))
                if flocPh < 7:
                    color = QtGui.QColor(int(255 * flocPh / 10), 0, 0)
                elif flocPh >= 8:
                    color = QtGui.QColor(0, 0, int(255 * flocPh / 10))
                else:
                    color = QtGui.QColor(0, int(255 * flocPh / 10), 0)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize, indicatorSize)
                painter.restore()
                painter.save()
                x += size
                flow = float(self.model.data(self.model.index(row, INLETFLOW)))
                char = None
                if flow <= 0:
                    char = WaterQualityView.FLOWCHARS[0]
                elif flow < 3:
                    char = WaterQualityView.FLOWCHARS[1]
                elif flow > 5.5:
                    char = WaterQualityView.FLOWCHARS[2]
                if char is not None:
                    painter.setFont(self.flowfont)
                    painter.drawText(x, y + size, char)
                painter.restore()
            y += size
            if y > maxY:
                break

    def mousePressEvent(self, event):
        fm = QtGui.QFontMetrics(self.font())
        self.selectedRow = event.position().y() // fm.height()
        self.update()
        self.emit(
            QtCore.SIGNAL("clicked(QtCore.QModelIndex)"),
            self.model.index(self.selectedRow, 0),
        )

    def keyPressEvent(self, event):
        if self.model is None:
            return
        row = -1
        if event.key() == QtCore.Qt.Key_Up:
            row = max(0, self.selectedRow - 1)
        elif event.key() == QtCore.Qt.Key_Down:
            row = min(self.selectedRow + 1, self.model.rowCount() - 1)
        if row != -1 and row != self.selectedRow:
            self.selectedRow = row
            if self.scrollarea is not None:
                fm = QtGui.QFontMetrics(self.font())
                y = fm.height() * self.selectedRow
                self.scrollarea.ensureVisible(0, y)
            self.update()
            self.emit(
                QtCore.SIGNAL("clicked(QtCore.QModelIndex)"),
                self.model.index(self.selectedRow, 0),
            )
        else:
            QtWidgets.QWidget.keyPressEvent(self, event)


class MainForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = WaterQualityModel(
            os.path.join(os.path.dirname(__file__), "waterdata.csv.gz")
        )
        self.tableView = QtWidgets.QTableView()
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setModel(self.model)
        self.waterView = WaterQualityView()
        self.waterView.setModel(self.model)
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setBackgroundRole(QtGui.QPalette.Light)
        scrollArea.setWidget(self.waterView)
        self.waterView.scrollarea = scrollArea

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.tableView)
        splitter.addWidget(scrollArea)
        splitter.setSizes([600, 250])
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.setWindowTitle("Water Quality Data")
        QtCore.QTimer.singleShot(0, self.initialLoad)

    def initialLoad(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        splash = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(
            os.path.join(os.path.dirname(__file__), "iss013-e-14802.jpg")
        )
        splash.setPixmap(pixmap)
        splash.setWindowFlags(QtCore.Qt.SplashScreen)
        splash.move(
            int(self.x() + ((self.width() - pixmap.width()) / 2)),
            int(self.y() + ((self.height() - pixmap.height()) / 2)),
        )
        splash.show()
        QtWidgets.QApplication.processEvents()
        try:
            self.model.load()
        except IOError as e:
            QtWidgets.QMessageBox.warning(self, "Water Quality - Error", e)
        else:
            self.tableView.resizeColumnsToContents()
        splash.close()
        QtWidgets.QApplication.processEvents()
        QtWidgets.QApplication.restoreOverrideCursor()


app = QtWidgets.QApplication(sys.argv)
form = MainForm()
form.resize(850, 620)
form.show()
app.exec()
