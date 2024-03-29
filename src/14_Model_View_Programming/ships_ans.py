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

import re
from PySide6 import QtWidgets, QtGui, QtCore
import richtextlineedit

NAME, OWNER, COUNTRY, DESCRIPTION, TEU = range(5)

MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1


class Ship(object):
    def __init__(self, name, owner, country, teu=0, description=""):
        self.name = name
        self.owner = owner
        self.country = country
        self.teu = teu
        self.description = description

    def __hash__(self):
        return super(Ship, self).__hash__()

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()


class ShipTableModel(QtCore.QAbstractTableModel):
    def __init__(self, filename=""):
        super(ShipTableModel, self).__init__()
        self.filename = filename
        self.dirty = False
        self.ships = []
        self.owners = set()
        self.countries = set()

    def sortByName(self):
        self.beginResetModel()
        self.ships = sorted(self.ships)
        self.endResetModel()

    def sortByTEU(self):
        ships = [(ship.teu, ship) for ship in self.ships]
        ships.sort()
        self.ships = [ship for teu, ship in ships]
        self.reset()

    def sortByCountryOwner(self):
        self.beginResetModel()
        self.ships = sorted(self.ships, key=lambda s: (s.country, s.owner))
        self.endResetModel()

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemFlags(
            QtCore.QAbstractTableModel.flags(self, index) | QtCore.Qt.ItemIsEditable
        )

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.ships)):
            return None
        ship = self.ships[index.row()]
        column = index.column()
        if role == QtCore.Qt.DisplayRole:
            if column == NAME:
                return ship.name
            elif column == OWNER:
                return ship.owner
            elif column == COUNTRY:
                return ship.country
            elif column == DESCRIPTION:
                return ship.description
            elif column == TEU:
                return "{:,}".format(ship.teu)
        elif role == QtCore.Qt.TextAlignmentRole:
            if column == TEU:
                return int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            return int(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # QtCore.Qt.TextColorRole no longer exist, replace with QtCore.Qt.ForegroundRole
        elif role == QtCore.Qt.ForegroundRole and column == TEU:
            if ship.teu < 80000:
                return QtGui.QColor(QtCore.Qt.black)
            elif ship.teu < 100000:
                return QtGui.QColor(QtCore.Qt.darkBlue)
            elif ship.teu < 120000:
                return QtGui.QColor(QtCore.Qt.blue)
            else:
                return QtGui.QColor(QtCore.Qt.red)
        elif role == QtCore.Qt.BackgroundRole:
            if ship.country in (
                "Bahamas",
                "Cyprus",
                "Denmark",
                "France",
                "Germany",
                "Greece",
            ):
                return QtGui.QColor(250, 230, 250)
            elif ship.country in ("Hong Kong", "Japan", "Taiwan"):
                return QtGui.QColor(250, 250, 230)
            elif ship.country in ("Marshall Islands",):
                return QtGui.QColor(230, 250, 250)
            else:
                return QtGui.QColor(210, 230, 230)
        elif role == Qt.ToolTipRole:
            msg = "<br>(minimum of 3 characters)"
            if column == NAME:
                return ship.name + msg
            elif column == OWNER:
                return ship.owner + msg
            elif column == COUNTRY:
                return ship.country + msg
            elif column == DESCRIPTION:
                return ship.description
            elif column == TEU:
                return "{:,} twenty foot equivalents".format(ship.teu)
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return int(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            return int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            if section == NAME:
                return "Name"
            elif section == OWNER:
                return "Owner"
            elif section == COUNTRY:
                return "Country"
            elif section == DESCRIPTION:
                return "Description"
            elif section == TEU:
                return "TEU"
        return int(section + 1)

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.ships)

    def columnCount(self, index=QtCore.QModelIndex()):
        return 5

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.ships):
            ship = self.ships[index.row()]
            column = index.column()
            if column == NAME:
                ship.name = value
            elif column == OWNER:
                ship.owner = value
            elif column == COUNTRY:
                ship.country = value
            elif column == DESCRIPTION:
                ship.description = value
            elif column == TEU:
                ship.teu = int(value)
            self.dirty = True
            self.emit(
                QtCore.SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                index,
                index,
            )
            return True
        return False

    def insertRows(self, position, rows=1, index=QtCore.QModelIndex()):
        self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.ships.insert(position + row, Ship(" Unknown", " Unknown", " Unknown"))
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self, position, rows=1, index=QtCore.QModelIndex()):
        self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)
        self.ships = self.ships[:position] + self.ships[position + rows :]
        self.endRemoveRows()
        self.dirty = True
        return True

    def load(self):
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for loading")
            fh = QtCore.QFile(self.filename)
            if not fh.open(QtCore.QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QDataStream(fh)
            magic = stream.readInt32()
            if magic != MAGIC_NUMBER:
                raise IOError("unrecognized file type")
            fileVersion = stream.readInt16()
            if fileVersion != FILE_VERSION:
                raise IOError("unrecognized file type version")
            stream.setVersion(QtCore.QDataStream.Qt_4_5)
            self.ships = []
            while not stream.atEnd():
                name = stream.readQString()
                owner = stream.readQString()
                country = stream.readQString()
                description = stream.readQString()
                teu = stream.readInt32()
                self.ships.append(Ship(name, owner, country, teu, description))
                self.owners.add(owner)
                self.countries.add(country)
            self.dirty = False
        except IOError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception

    def save(self):
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for saving")
            fh = QtCore.QFile(self.filename)
            if not fh.open(QtCore.QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QDataStream(fh)
            stream.writeInt32(MAGIC_NUMBER)
            stream.writeInt16(FILE_VERSION)
            stream.setVersion(QtCore.QDataStream.Qt_4_5)
            for ship in self.ships:
                stream.writeQString(ship.name)
                stream.writeQString(ship.owner)
                stream.writeQString(ship.country)
                stream.writeQString(ship.description)
                stream.writeInt32(ship.teu)
            self.dirty = False
        except IOError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


class ShipDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ShipDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if index.column() == DESCRIPTION:
            text = index.model().data(index)
            palette = QtWidgets.QApplication.palette()
            document = QtGui.QTextDocument()
            document.setDefaultFont(option.font)
            if option.state & QtWidgets.QStyle.State_Selected:
                document.setHtml(
                    "<font color={}>{}</font>".format(
                        palette.highlightedText().color().name(), text
                    )
                )
            else:
                document.setHtml(text)
            color = (
                palette.highlight().color()
                if option.state & QtWidgets.QStyle.State_Selected
                else QtGui.QColor(
                    index.model().data(index, QtCore.Qt.BackgroundColorRole)
                )
            )
            painter.save()
            painter.fillRect(option.rect, color)
            painter.translate(option.rect.x(), option.rect.y())
            document.drawContents(painter)
            painter.restore()
        else:
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):
        fm = option.fontMetrics
        if index.column() == TEU:
            return QtCore.QSize(fm.horizontalAdvance("9,999,999"), fm.height())
        if index.column() == DESCRIPTION:
            text = index.model().data(index)
            document = QtGui.QTextDocument()
            document.setDefaultFont(option.font)
            document.setHtml(text)
            return QtCore.QSize(document.idealWidth() + 5, fm.height())
        return QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)

    def createEditor(self, parent, option, index):
        if index.column() == TEU:
            spinbox = QtWidgets.QSpinBox(parent)
            spinbox.setRange(0, 200000)
            spinbox.setSingleStep(1000)
            spinbox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            return spinbox
        elif index.column() == OWNER:
            combobox = QtWidgets.QComboBox(parent)
            combobox.addItems(sorted(index.model().owners))
            combobox.setEditable(True)
            return combobox
        elif index.column() == COUNTRY:
            combobox = QtWidgets.QComboBox(parent)
            combobox.addItems(sorted(index.model().countries))
            combobox.setEditable(True)
            return combobox
        elif index.column() == NAME:
            editor = QtWidgets.QLineEdit(parent)
            self.connect(
                editor, QtCore.SIGNAL("returnPressed()"), self.commitAndCloseEditor
            )
            return editor
        elif index.column() == DESCRIPTION:
            editor = richtextlineedit.RichTextLineEdit(parent)
            self.connect(
                editor, QtCore.SIGNAL("returnPressed()"), self.commitAndCloseEditor
            )
            return editor
        else:
            return QtWidgets.QStyledItemDelegate.createEditor(
                self, parent, option, index
            )

    def commitAndCloseEditor(self):
        editor = self.sender()
        if isinstance(editor, (QtWidgets.QTextEdit, QtWidgets.QLineEdit)):
            self.emit(QtCore.SIGNAL("commitData(QWidget*)"), editor)
            self.emit(QtCore.SIGNAL("closeEditor(QWidget*)"), editor)

    def setEditorData(self, editor, index):
        text = index.model().data(index, QtCore.Qt.DisplayRole)
        if index.column() == TEU:
            if text is None:
                value = 0
            elif isinstance(text, int):
                value = text
            else:
                value = int(re.sub(r"[., ]", "", text))
            editor.setValue(value)
        elif index.column() in (OWNER, COUNTRY):
            i = editor.findText(text)
            if i == -1:
                i = 0
            editor.setCurrentIndex(i)
        elif index.column() == NAME:
            editor.setText(text)
        elif index.column() == DESCRIPTION:
            editor.setHtml(text)
        else:
            QtWidgets.QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        if index.column() == TEU:
            model.setData(index, editor.value())
        elif index.column() in (OWNER, COUNTRY):
            text = editor.currentText()
            if len(text) >= 3:
                model.setData(index, text)
        elif index.column() == NAME:
            text = editor.text()
            if len(text) >= 3:
                model.setData(index, text)
        elif index.column() == DESCRIPTION:
            model.setData(index, editor.toSimpleHtml())
        else:
            QtWidgets.QStyledItemDelegate.setModelData(self, editor, model, index)


def generateFakeShips():
    for name, owner, country, teu, description in (
        (
            "Emma M\u00E6rsk",
            "M\u00E6rsk Line",
            "Denmark",
            151687,
            "<b>W\u00E4rtsil\u00E4-Sulzer RTA96-C</b> main engine,"
            "<font color=green>109,000 hp</font>",
        ),
        ("MSC Pamela", "MSC", "Liberia", 90449, "Draft <font color=green>15m</font>"),
        (
            "Colombo Express",
            "Hapag-Lloyd",
            "Germany",
            93750,
            "Main engine, <font color=green>93,500 hp</font>",
        ),
        (
            "Houston Express",
            "Norddeutsche Reederei",
            "Germany",
            95000,
            "Features a <u>twisted leading edge full spade rudder</u>. "
            "Sister of <i>Savannah Express</i>",
        ),
        (
            "Savannah Express",
            "Norddeutsche Reederei",
            "Germany",
            95000,
            "Sister of <i>Houston Express</i>",
        ),
        ("MSC Susanna", "MSC", "Liberia", 90449, ""),
        (
            "Eleonora M\u00E6rsk",
            "M\u00E6rsk Line",
            "Denmark",
            151687,
            "Captain <i>Hallam</i>",
        ),
        (
            "Estelle M\u00E6rsk",
            "M\u00E6rsk Line",
            "Denmark",
            151687,
            "Captain <i>Wells</i>",
        ),
        (
            "Evelyn M\u00E6rsk",
            "M\u00E6rsk Line",
            "Denmark",
            151687,
            "Captain <i>Byrne</i>",
        ),
        ("Georg M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
        ("Gerd M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
        ("Gjertrud M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
        ("Grete M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
        ("Gudrun M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
        ("Gunvor M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
        ("CSCL Le Havre", "Danaos Shipping", "Cyprus", 107200, ""),
        ("CSCL Pusan", "Danaos Shipping", "Cyprus", 107200, "Captain <i>Watts</i>"),
        (
            "Xin Los Angeles",
            "China Shipping Container Lines (CSCL)",
            "Hong Kong",
            107200,
            "",
        ),
        (
            "Xin Shanghai",
            "China Shipping Container Lines (CSCL)",
            "Hong Kong",
            107200,
            "",
        ),
        ("Cosco Beijing", "Costamare Shipping", "Greece", 99833, ""),
        ("Cosco Hellas", "Costamare Shipping", "Greece", 99833, ""),
        ("Cosco Guangzho", "Costamare Shipping", "Greece", 99833, ""),
        ("Cosco Ningbo", "Costamare Shipping", "Greece", 99833, ""),
        ("Cosco Yantian", "Costamare Shipping", "Greece", 99833, ""),
        ("CMA CGM Fidelio", "CMA CGM", "France", 99500, ""),
        ("CMA CGM Medea", "CMA CGM", "France", 95000, ""),
        ("CMA CGM Norma", "CMA CGM", "Bahamas", 95000, ""),
        ("CMA CGM Rigoletto", "CMA CGM", "France", 99500, ""),
        (
            "Arnold M\u00E6rsk",
            "M\u00E6rsk Line",
            "Denmark",
            93496,
            "Captain <i>Morrell</i>",
        ),
        (
            "Anna M\u00E6rsk",
            "M\u00E6rsk Line",
            "Denmark",
            93496,
            "Captain <i>Lockhart</i>",
        ),
        (
            "Albert M\u00E6rsk",
            "M\u00E6rsk Line",
            "Denmark",
            93496,
            "Captain <i>Tallow</i>",
        ),
        (
            "Adrian M\u00E6rsk",
            "M\u00E6rsk Line",
            "Denmark",
            93496,
            "Captain <i>G. E. Ericson</i>",
        ),
        ("Arthur M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 93496, ""),
        ("Axel M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 93496, ""),
        ("NYK Vega", "Nippon Yusen Kaisha", "Panama", 97825, ""),
        ("MSC Esthi", "MSC", "Liberia", 99500, ""),
        ("MSC Chicago", "Offen Claus-Peter", "Liberia", 90449, ""),
        ("MSC Bruxelles", "Offen Claus-Peter", "Liberia", 90449, ""),
        ("MSC Roma", "Offen Claus-Peter", "Liberia", 99500, ""),
        ("MSC Madeleine", "MSC", "Liberia", 107551, ""),
        ("MSC Ines", "MSC", "Liberia", 107551, ""),
        ("Hannover Bridge", "Kawasaki Kisen Kaisha", "Japan", 99500, ""),
        ("Charlotte M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Clementine M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Columbine M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Cornelia M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Chicago Express", "Hapag-Lloyd", "Germany", 93750, ""),
        ("Kyoto Express", "Hapag-Lloyd", "Germany", 93750, ""),
        ("Clifford M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Sally M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Sine M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Skagen M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Sofie M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Sor\u00F8 M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Sovereing M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Susan M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Svend M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Svendborg M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        (
            "A.P. M\u00F8ller",
            "M\u00E6rsk Line",
            "Denmark",
            91690,
            "Captain <i>Ferraby</i>",
        ),
        ("Caroline M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Carsten M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Chastine M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("Cornelius M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
        ("CMA CGM Otello", "CMA CGM", "France", 91400, ""),
        ("CMA CGM Tosca", "CMA CGM", "France", 91400, ""),
        ("CMA CGM Nabucco", "CMA CGM", "France", 91400, ""),
        ("CMA CGM La Traviata", "CMA CGM", "France", 91400, ""),
        ("CSCL Europe", "Danaos Shipping", "Cyprus", 90645, ""),
        ("CSCL Africa", "Seaspan Container Line", "Cyprus", 90645, ""),
        ("CSCL America", "Danaos Shipping ", "Cyprus", 90645, ""),
        ("CSCL Asia", "Seaspan Container Line", "Hong Kong", 90645, ""),
        (
            "CSCL Oceania",
            "Seaspan Container Line",
            "Hong Kong",
            90645,
            "Captain <i>Baker</i>",
        ),
        ("M\u00E6rsk Seville", "Blue Star GmbH", "Liberia", 94724, ""),
        ("M\u00E6rsk Santana", "Blue Star GmbH", "Liberia", 94724, ""),
        ("M\u00E6rsk Sheerness", "Blue Star GmbH", "Liberia", 94724, ""),
        ("M\u00E6rsk Sarnia", "Blue Star GmbH", "Liberia", 94724, ""),
        ("M\u00E6rsk Sydney", "Blue Star GmbH", "Liberia", 94724, ""),
        ("MSC Heidi", "MSC", "Panama", 95000, ""),
        ("MSC Rania", "MSC", "Panama", 95000, ""),
        ("MSC Silvana", "MSC", "Panama", 95000, ""),
        ("M\u00E6rsk Stralsund", "Blue Star GmbH", "Liberia", 95000, ""),
        ("M\u00E6rsk Saigon", "Blue Star GmbH", "Liberia", 95000, ""),
        ("M\u00E6rsk Seoul", "Blue Star Ship Managment GmbH", "Germany", 95000, ""),
        ("M\u00E6rsk Surabaya", "Offen Claus-Peter", "Germany", 98400, ""),
        ("CMA CGM Hugo", "NSB Niederelbe", "Germany", 90745, ""),
        ("CMA CGM Vivaldi", "CMA CGM", "Bahamas", 90745, ""),
        ("MSC Rachele", "NSB Niederelbe", "Germany", 90745, ""),
        ("Pacific Link", "NSB Niederelbe", "Germany", 90745, ""),
        ("CMA CGM Carmen", "E R Schiffahrt", "Liberia", 89800, ""),
        ("CMA CGM Don Carlos", "E R Schiffahrt", "Liberia", 89800, ""),
        ("CMA CGM Don Giovanni", "E R Schiffahrt", "Liberia", 89800, ""),
        ("CMA CGM Parsifal", "E R Schiffahrt", "Liberia", 89800, ""),
        ("Cosco China", "E R Schiffahrt", "Liberia", 91649, ""),
        ("Cosco Germany", "E R Schiffahrt", "Liberia", 89800, ""),
        ("Cosco Napoli", "E R Schiffahrt", "Liberia", 89800, ""),
        ("YM Unison", "Yang Ming Line", "Taiwan", 88600, ""),
        ("YM Utmost", "Yang Ming Line", "Taiwan", 88600, ""),
        ("MSC Lucy", "MSC", "Panama", 89954, ""),
        ("MSC Maeva", "MSC", "Panama", 89954, ""),
        ("MSC Rita", "MSC", "Panama", 89954, ""),
        ("MSC Busan", "Offen Claus-Peter", "Panama", 89954, ""),
        ("MSC Beijing", "Offen Claus-Peter", "Panama", 89954, ""),
        ("MSC Toronto", "Offen Claus-Peter", "Panama", 89954, ""),
        ("MSC Charleston", "Offen Claus-Peter", "Panama", 89954, ""),
        ("MSC Vittoria", "MSC", "Panama", 89954, ""),
        (
            "Ever Champion",
            "NSB Niederelbe",
            "Marshall Islands",
            90449,
            "Captain <i>Phillips</i>",
        ),
        (
            "Ever Charming",
            "NSB Niederelbe",
            "Marshall Islands",
            90449,
            "Captain <i>Tonbridge</i>",
        ),
        ("Ever Chivalry", "NSB Niederelbe", "Marshall Islands", 90449, ""),
        ("Ever Conquest", "NSB Niederelbe", "Marshall Islands", 90449, ""),
        ("Ital Contessa", "NSB Niederelbe", "Marshall Islands", 90449, ""),
        ("Lt Cortesia", "NSB Niederelbe", "Marshall Islands", 90449, ""),
        ("OOCL Asia", "OOCL", "Hong Kong", 89097, ""),
        ("OOCL Atlanta", "OOCL", "Hong Kong", 89000, ""),
        ("OOCL Europe", "OOCL", "Hong Kong", 89097, ""),
        ("OOCL Hamburg", "OOCL", "Marshall Islands", 89097, ""),
        ("OOCL Long Beach", "OOCL", "Marshall Islands", 89097, ""),
        ("OOCL Ningbo", "OOCL", "Marshall Islands", 89097, ""),
        ("OOCL Shenzhen", "OOCL", "Hong Kong", 89097, ""),
        ("OOCL Tianjin", "OOCL", "Marshall Islands", 89097, ""),
        ("OOCL Tokyo", "OOCL", "Hong Kong", 89097, ""),
    ):
        yield Ship(name, owner, country, teu, description)
