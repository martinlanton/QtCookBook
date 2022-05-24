# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import functools
import random
import sys
from PySide6 import QtWidgets, QtCore, QtGui, QtPrintSupport

MAC = "qt_mac_set_native_menubar" in dir()

# PageSize = (595, 842) # A4 in points
PageSize = (612, 792)  # US Letter in points
PointSize = 10

MagicNumber = 0x70616765
FileVersion = 1

Dirty = False


class TextItemDlg(QtWidgets.QDialog):
    def __init__(self, item=None, position=None, scene=None, parent=None):
        super(TextItemDlg, self).__init__(parent)

        self.item = item
        self.position = position
        self.scene = scene

        self.editor = QtWidgets.QTextEdit()
        self.editor.setAcceptRichText(False)
        self.editor.setTabChangesFocus(True)
        editorLabel = QtWidgets.QLabel("&Text:")
        editorLabel.setBuddy(self.editor)
        self.fontComboBox = QtWidgets.QFontComboBox()
        self.fontComboBox.setCurrentFont(QtGui.QFont("Times", PointSize))
        fontLabel = QtWidgets.QLabel("&Font:")
        fontLabel.setBuddy(self.fontComboBox)
        self.fontSpinBox = QtWidgets.QSpinBox()
        self.fontSpinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.fontSpinBox.setRange(6, 280)
        self.fontSpinBox.setValue(PointSize)
        fontSizeLabel = QtWidgets.QLabel("&Size:")
        fontSizeLabel.setBuddy(self.fontSpinBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        if self.item is not None:
            self.editor.setPlainText(self.item.toPlainText())
            self.fontComboBox.setCurrentFont(self.item.font())
            self.fontSpinBox.setValue(self.item.font().pointSize())

        layout = QtWidgets.QGridLayout()
        layout.addWidget(editorLabel, 0, 0)
        layout.addWidget(self.editor, 1, 0, 1, 6)
        layout.addWidget(fontLabel, 2, 0)
        layout.addWidget(self.fontComboBox, 2, 1, 1, 2)
        layout.addWidget(fontSizeLabel, 2, 3)
        layout.addWidget(self.fontSpinBox, 2, 4, 1, 2)
        layout.addWidget(self.buttonBox, 3, 0, 1, 6)
        self.setLayout(layout)

        self.connect(
            self.fontComboBox,
            QtCore.SIGNAL("currentFontChanged(QFont)"),
            self.updateUi,
        )
        self.connect(
            self.fontSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.updateUi
        )
        self.connect(self.editor, QtCore.SIGNAL("textChanged()"), self.updateUi)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)

        self.setWindowTitle(
            "Page Designer - {} Text Item".format(
                "Add" if self.item is None else "Edit"
            )
        )
        self.updateUi()

    def updateUi(self):
        font = self.fontComboBox.currentFont()
        font.setPointSize(self.fontSpinBox.value())
        self.editor.document().setDefaultFont(font)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(
            bool(self.editor.toPlainText())
        )

    def accept(self):
        if self.item is None:
            self.item = TextItem("", self.position, self.scene)
        font = self.fontComboBox.currentFont()
        font.setPointSize(self.fontSpinBox.value())
        self.item.setFont(font)
        self.item.setPlainText(self.editor.toPlainText())
        self.item.update()
        global Dirty
        Dirty = True
        QtWidgets.QDialog.accept(self)


class TextItem(QtWidgets.QGraphicsTextItem):
    def __init__(
        self,
        text,
        position,
        scene,
        font=QtGui.QFont("Times", PointSize),
        transform=QtGui.QTransform(),
    ):
        super(TextItem, self).__init__(text)
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsSelectable
            | QtWidgets.QGraphicsItem.ItemIsMovable
        )
        self.setFont(font)
        self.setPos(position)
        self.setTransform(transform)
        scene.clearSelection()
        scene.addItem(self)
        self.setSelected(True)
        global Dirty
        Dirty = True

    def parentWidget(self):
        return self.scene().views()[0]

    def itemChange(self, change, variant):
        if change != QtWidgets.QGraphicsItem.ItemSelectedChange:
            global Dirty
            Dirty = True
        return QtWidgets.QGraphicsTextItem.itemChange(self, change, variant)

    def mouseDoubleClickEvent(self, event):
        dialog = TextItemDlg(self, self.parentWidget())
        dialog.exec()


class BoxItem(QtWidgets.QGraphicsItem):
    def __init__(
        self,
        position,
        scene,
        style=QtCore.Qt.SolidLine,
        rect=None,
        transform=QtGui.QTransform(),
    ):
        super(BoxItem, self).__init__()
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsSelectable
            | QtWidgets.QGraphicsItem.ItemIsMovable
            | QtWidgets.QGraphicsItem.ItemIsFocusable
        )
        if rect is None:
            rect = QtCore.QRectF(
                -10 * PointSize, -PointSize, 20 * PointSize, 2 * PointSize
            )
        self.rect = rect
        self.style = style
        self.setPos(position)
        self.setTransform(transform)
        scene.clearSelection()
        scene.addItem(self)
        self.setSelected(True)
        self.setFocus()
        global Dirty
        Dirty = True

    def parentWidget(self):
        return self.scene().views()[0]

    def boundingRect(self):
        return self.rect.adjusted(-2, -2, 2, 2)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen(self.style)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(1)
        if option.state & QtWidgets.QStyle.State_Selected:
            pen.setColor(QtCore.Qt.blue)
        painter.setPen(pen)
        painter.drawRect(self.rect)

    def itemChange(self, change, variant):
        if change != QtWidgets.QGraphicsItem.ItemSelectedChange:
            global Dirty
            Dirty = True
        return QtWidgets.QGraphicsItem.itemChange(self, change, variant)

    def contextMenuEvent(self, event):
        wrapped = []
        menu = QtWidgets.QMenu(self.parentWidget())
        for text, param in (
            ("&Solid", QtCore.Qt.SolidLine),
            ("&Dashed", QtCore.Qt.DashLine),
            ("D&otted", QtCore.Qt.DotLine),
            ("D&ashDotted", QtCore.Qt.DashDotLine),
            ("DashDo&tDotted", QtCore.Qt.DashDotDotLine),
        ):
            wrapper = functools.partial(self.setStyle, param)
            wrapped.append(wrapper)
            menu.addAction(text, wrapper)
        menu.exec(event.screenPos())

    def setStyle(self, style):
        self.style = style
        self.update()
        global Dirty
        Dirty = True

    def keyPressEvent(self, event):
        factor = PointSize / 4
        changed = False
        if event.modifiers() & QtCore.Qt.ShiftModifier:
            if event.key() == QtCore.Qt.Key_Left:
                self.rect.setRight(self.rect.right() - factor)
                changed = True
            elif event.key() == QtCore.Qt.Key_Right:
                self.rect.setRight(self.rect.right() + factor)
                changed = True
            elif event.key() == QtCore.Qt.Key_Up:
                self.rect.setBottom(self.rect.bottom() - factor)
                changed = True
            elif event.key() == QtCore.Qt.Key_Down:
                self.rect.setBottom(self.rect.bottom() + factor)
                changed = True
        if changed:
            self.update()
            global Dirty
            Dirty = True
        else:
            QtWidgets.QGraphicsItem.keyPressEvent(self, event)


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        factor = 1.41 ** (delta / 240.0)
        self.scale(factor, factor)


class MainForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.filename = ""
        self.copiedItem = QtCore.QByteArray()
        self.pasteOffset = 5
        self.prevPoint = QtCore.QPoint()
        self.addOffset = 5
        self.borders = []

        self.printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        self.printer.setPageSize(QtGui.QPageSize.Letter)

        self.view = GraphicsView()
        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, PageSize[0], PageSize[1])
        self.addBorders()
        self.view.setScene(self.scene)

        buttonLayout = QtWidgets.QVBoxLayout()
        for text, slot in (
            ("Add &Text", self.addText),
            ("Add &Box", self.addBox),
            ("Add Pi&xmap", self.addPixmap),
            ("&Copy", self.copy),
            ("C&ut", self.cut),
            ("&Paste", self.paste),
            ("&Delete...", self.delete),
            ("&Rotate", self.rotate),
            ("Pri&nt...", self.print_),
            ("&Open...", self.open),
            ("&Save", self.save),
            ("&Quit", self.accept),
        ):
            button = QtWidgets.QPushButton(text)
            if not MAC:
                button.setFocusPolicy(QtCore.Qt.NoFocus)
            self.connect(button, QtCore.SIGNAL("clicked()"), slot)
            if text == "Pri&nt...":
                buttonLayout.addStretch(5)
            if text == "&Quit":
                buttonLayout.addStretch(1)
            buttonLayout.addWidget(button)
        buttonLayout.addStretch()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.view, 1)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        fm = QtGui.QFontMetrics(self.font())
        self.resize(
            int(self.scene.width() + fm.horizontalAdvance(" Delete... ") + 50),
            int(self.scene.height() + 50),
        )
        self.setWindowTitle("Page Designer")

    def addBorders(self):
        self.borders = []
        rect = QtCore.QRectF(0, 0, PageSize[0], PageSize[1])
        brush = QtGui.QBrush()
        pen = QtGui.QPen(QtCore.Qt.yellow)
        self.borders.append(self.scene.addRect(rect, pen, brush))
        margin = 5.25 * PointSize
        self.borders.append(
            self.scene.addRect(
                rect.adjusted(margin, margin, -margin, -margin), pen, brush
            )
        )

    def removeBorders(self):
        while self.borders:
            item = self.borders.pop()
            self.scene.removeItem(item)
            del item

    def reject(self):
        self.accept()

    def accept(self):
        self.offerSave()
        QtWidgets.QDialog.accept(self)

    def offerSave(self):
        if (
            Dirty
            and QtWidgets.QMessageBox.question(
                self,
                "Page Designer - Unsaved Changes",
                "Save unsaved changes?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.Yes
        ):
            self.save()

    def position(self):
        point = self.mapFromGlobal(QtGui.QCursor.pos())
        if not self.view.geometry().contains(point):
            coord = random.randint(36, 144)
            point = QtCore.QPoint(coord, coord)
        else:
            if point == self.prevPoint:
                point += QtCore.QPoint(self.addOffset, self.addOffset)
                self.addOffset += 5
            else:
                self.addOffset = 5
                self.prevPoint = point
        return self.view.mapToScene(point)

    def addText(self):
        dialog = TextItemDlg(position=self.position(), scene=self.scene, parent=self)
        dialog.exec()

    def addBox(self):
        BoxItem(self.position(), self.scene)

    def addPixmap(self):
        path = QtCore.QFileInfo(self.filename).path() if self.filename else "."
        fname, filter = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Page Designer - Add Pixmap",
            path,
            "Pixmap Files (*.bmp *.jpg *.png *.xpm)",
        )
        if not fname:
            return
        self.createPixmapItem(QtGui.QPixmap(fname), self.position())

    def createPixmapItem(self, pixmap, position, transform=QtGui.QTransform()):
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        item.setFlags(
            QtWidgets.QGraphicsItem.ItemIsSelectable
            | QtWidgets.QGraphicsItem.ItemIsMovable
        )
        item.setPos(position)
        item.setTransform(transform)
        self.scene.clearSelection()
        self.scene.addItem(item)
        item.setSelected(True)
        global Dirty
        Dirty = True

    def selectedItem(self):
        items = self.scene.selectedItems()
        if len(items) == 1:
            return items[0]
        return None

    def copy(self):
        item = self.selectedItem()
        if item is None:
            return
        self.copiedItem.clear()
        self.pasteOffset = 5
        stream = QtCore.QDataStream(self.copiedItem, QtCore.QIODevice.WriteOnly)
        self.writeItemToStream(stream, item)

    def cut(self):
        item = self.selectedItem()
        if item is None:
            return
        self.copy()
        self.scene.removeItem(item)
        del item

    def paste(self):
        if self.copiedItem.isEmpty():
            return
        stream = QtCore.QDataStream(self.copiedItem, QtCore.QIODevice.ReadOnly)
        self.readItemFromStream(stream, self.pasteOffset)
        self.pasteOffset += 5

    def rotate(self):
        for item in self.scene.selectedItems():
            rotation = item.rotation()
            item.setRotation(rotation + 30)

    def delete(self):
        items = self.scene.selectedItems()
        if (
            len(items)
            and QtWidgets.QMessageBox.question(
                self,
                "Page Designer - Delete",
                "Delete {} item{}?".format(len(items), "s" if len(items) != 1 else ""),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.Yes
        ):
            while items:
                item = items.pop()
                self.scene.removeItem(item)
                del item
            global Dirty
            Dirty = True

    def print_(self):
        dialog = QtPrintSupport.QPrintDialog(self.printer)
        if dialog.exec():
            painter = QtGui.QPainter(self.printer)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
            self.scene.clearSelection()
            self.removeBorders()
            self.scene.render(painter)
            self.addBorders()

    def open(self):
        self.offerSave()
        path = QtCore.QFileInfo(self.filename).path() if self.filename else "."
        fname, filter = QtWidgets.QFileDialog.getOpenFileName(
            self, "Page Designer - Open", path, "Page Designer Files (*.pgd)"
        )
        if not fname:
            return
        self.filename = fname
        fh = None
        try:
            fh = QtCore.QFile(self.filename)
            if not fh.open(QtCore.QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            items = self.scene.items()
            while items:
                item = items.pop()
                self.scene.removeItem(item)
                del item
            self.addBorders()
            stream = QtCore.QDataStream(fh)
            stream.setVersion(QtCore.QDataStream.Qt_4_2)
            magic = stream.readInt32()
            if magic != MagicNumber:
                raise IOError("not a valid .pgd file")
            fileVersion = stream.readInt16()
            if fileVersion != FileVersion:
                raise IOError("unrecognised .pgd file version")
            while not fh.atEnd():
                self.readItemFromStream(stream)
        except IOError as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Page Designer -- Open Error",
                "Failed to open {}: {}".format(self.filename, e),
            )
        finally:
            if fh is not None:
                fh.close()
        global Dirty
        Dirty = False

    def save(self):
        if not self.filename:
            path = "."
            fname, filter = QtWidgets.QFileDialog.getSaveFileName(
                self, "Page Designer - Save As", path, "Page Designer Files (*.pgd)"
            )
            if not fname:
                return
            if not fname.lower().endswith(".pgd"):
                fname += ".pgd"
            self.filename = fname
        fh = None
        try:
            fh = QtCore.QFile(self.filename)
            if not fh.open(QtCore.QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            self.scene.clearSelection()
            stream = QtCore.QDataStream(fh)
            stream.setVersion(QtCore.QDataStream.Qt_4_2)
            stream.writeInt32(MagicNumber)
            stream.writeInt16(FileVersion)
            for item in self.scene.items():
                self.writeItemToStream(stream, item)
        except IOError as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Page Designer -- Save Error",
                "Failed to save {}: {}".format(self.filename, e),
            )
        finally:
            if fh is not None:
                fh.close()
        global Dirty
        Dirty = False

    def readItemFromStream(self, stream, offset=0):
        type = ""
        position = QtCore.QPointF()
        matrix = QtGui.QTransform()
        type = stream.readQString()
        stream >> position >> matrix
        if offset:
            position += QtCore.QPointF(offset, offset)
        if type == "Text":
            text = stream.readQString()
            font = QtGui.QFont()
            stream >> font
            TextItem(text, position, self.scene, font, matrix)
        elif type == "Box":
            rect = QtCore.QRectF()
            stream >> rect
            style = QtCore.Qt.PenStyle(stream.readInt16())
            BoxItem(position, self.scene, style, rect, matrix)
        elif type == "Pixmap":
            pixmap = QtGui.QPixmap()
            stream >> pixmap
            self.createPixmapItem(pixmap, position, matrix)

    def writeItemToStream(self, stream, item):
        if isinstance(item, QtWidgets.QGraphicsTextItem):
            stream.writeQString("Text")
            stream << item.pos() << item.transform()
            stream.writeQString(item.toPlainText())
            stream << item.font()
        elif isinstance(item, QtWidgets.QGraphicsPixmapItem):
            stream.writeQString("Pixmap")
            stream << item.pos() << item.transform() << item.pixmap()
        elif isinstance(item, BoxItem):
            stream.writeQString("Box")
            stream << item.pos() << item.transform() << item.rect
            stream.writeInt16(item.style)


app = QtWidgets.QApplication(sys.argv)
form = MainForm()
rect = QtGui.QScreen().availableGeometry()
form.resize(int(rect.width() * 0.6), int(rect.height() * 0.9))
form.show()
app.exec()
