# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.


from PySide6 import QtWidgets, QtCore, QtGui


class YPipeWidget(QtWidgets.QWidget):
    valueChanged = QtCore.Signal((int, int))

    def __init__(self, leftFlow=0, rightFlow=0, maxFlow=100, parent=None):
        super(YPipeWidget, self).__init__(parent)

        self.leftSpinBox = QtWidgets.QSpinBox(self)
        self.leftSpinBox.setRange(0, maxFlow)
        self.leftSpinBox.setValue(leftFlow)
        self.leftSpinBox.setSuffix(" l/s")
        self.leftSpinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.connect(
            self.leftSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.updateValue
        )

        self.rightSpinBox = QtWidgets.QSpinBox(self)
        self.rightSpinBox.setRange(0, maxFlow)
        self.rightSpinBox.setValue(rightFlow)
        self.rightSpinBox.setSuffix(" l/s")
        self.rightSpinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.connect(
            self.rightSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.updateValue
        )

        self.label = QtWidgets.QLabel(self)
        self.label.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        fm = QtGui.QFontMetricsF(self.font())
        self.label.setMinimumWidth(fm.horizontalAdvance(" 999 l/s "))

        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding,
            )
        )
        self.setMinimumSize(self.minimumSizeHint())
        self.updateValue()

    def updateValue(self):
        a = self.leftSpinBox.value()
        b = self.rightSpinBox.value()
        self.label.setText("{} l/s".format(a + b))
        self.valueChanged.emit(a, b)
        self.update()

    def values(self):
        return self.leftSpinBox.value(), self.rightSpinBox.value()

    def minimumSizeHint(self):
        return QtCore.QSize(self.leftSpinBox.width() * 3, self.leftSpinBox.height() * 5)

    def resizeEvent(self, event=None):
        fm = QtGui.QFontMetricsF(self.font())
        x = (self.width() - self.label.width()) / 2
        y = self.height() - (fm.height() * 1.5)
        self.label.move(x, y)
        y = self.height() / 60.0
        x = (self.width() / 4.0) - self.leftSpinBox.width()
        self.leftSpinBox.move(x, y)
        x = self.width() - (self.width() / 4.0)
        self.rightSpinBox.move(x, y)

    def paintEvent(self, event=None):
        LogicalSize = 100.0

        def logicalFromPhysical(length, side):
            return (length / side) * LogicalSize

        fm = QtGui.QFontMetricsF(self.font())
        ymargin = (LogicalSize / 30.0) + logicalFromPhysical(
            self.leftSpinBox.height(), self.height()
        )
        ymax = int(LogicalSize - logicalFromPhysical(fm.height() * 2, self.height()))
        width = int(LogicalSize / 4.0)
        cx, cy = int(LogicalSize / 2.0), int(LogicalSize / 3.0)
        ax, ay = cx - int(2 * width), ymargin
        bx, by = cx - width, ay
        dx, dy = cx + width, ay
        ex, ey = cx + int(2 * width), ymargin
        fx, fy = cx + int(width / 2), cx + int(LogicalSize / 24.0)
        gx, gy = fx, ymax
        hx, hy = cx - int(width / 2), ymax
        ix, iy = hx, fy

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        side = min(self.width(), self.height())
        painter.setViewport(
            (self.width() - side) / 2, (self.height() - side) / 2, side, side
        )
        painter.setWindow(0, 0, LogicalSize, LogicalSize)

        painter.setPen(QtCore.Qt.NoPen)

        gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(0, 100))
        gradient.setColorAt(0, QtCore.Qt.white)
        a = self.leftSpinBox.value()
        gradient.setColorAt(1, (QtCore.Qt.red if a != 0 else QtCore.Qt.white))
        painter.setBrush(QtGui.QBrush(gradient))
        painter.drawPolygon(QtGui.QPolygon([QtCore.QPoint(ax, ay), QtCore.QPoint(bx, by), QtCore.QPoint(cx, cy), QtCore.QPoint(ix, iy)]))

        gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(0, 100))
        gradient.setColorAt(0, QtCore.Qt.white)
        b = self.rightSpinBox.value()
        gradient.setColorAt(1, (QtCore.Qt.blue if b != 0 else QtCore.Qt.white))
        painter.setBrush(QtGui.QBrush(gradient))
        painter.drawPolygon(QtGui.QPolygon([QtCore.QPoint(cx, cy), QtCore.QPoint(dx, dy), QtCore.QPoint(ex, ey), QtCore.QPoint(fx, fy)]))

        if (a + b) == 0:
            color = QtGui.QColor(QtCore.Qt.white)
        else:
            ashare = int((a / (a + b)) * 255.0)
            bshare = int(255.0 - ashare)
            color = QtGui.QColor(ashare, 0, bshare)
        gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(0, 100))
        gradient.setColorAt(0, QtCore.Qt.white)
        gradient.setColorAt(1, color)
        painter.setBrush(QtGui.QBrush(gradient))
        painter.drawPolygon(QtGui.QPolygon([QtCore.QPoint(cx, cy), QtCore.QPoint(fx, fy), QtCore.QPoint(gx, gy), QtCore.QPoint(hx, hy), QtCore.QPoint(ix, iy)]))

        painter.setPen(QtCore.Qt.black)
        painter.drawPolyline(QtGui.QPolygon([QtCore.QPoint(ax, ay), QtCore.QPoint(ix, iy), QtCore.QPoint(hx, hy)]))
        painter.drawPolyline(QtGui.QPolygon([QtCore.QPoint(gx, gy), QtCore.QPoint(fx, fy), QtCore.QPoint(ex, ey)]))
        painter.drawPolyline(QtGui.QPolygon([QtCore.QPoint(bx, by), QtCore.QPoint(cx, cy), QtCore.QPoint(dx, dy)]))


if __name__ == "__main__":
    import sys

    def valueChanged(a, b):
        print(a, b)

    app = QtWidgets.QApplication(sys.argv)
    form = YPipeWidget()
    form.valueChanged.connect(valueChanged)
    form.setWindowTitle("YPipe")
    form.move(0, 0)
    form.show()
    form.resize(400, 400)
    app.exec()
