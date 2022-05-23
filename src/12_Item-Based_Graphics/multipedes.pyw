# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import math
import random
import sys
from PySide6 import QtWidgets, QtCore, QtGui


SCENESIZE = 500
INTERVAL = 200

Running = False


class Head(QtWidgets.QGraphicsItem):

    Rect = QtCore.QRectF(-30, -20, 60, 40)

    def __init__(self, color, angle, position):
        super(Head, self).__init__()
        self.color = color
        self.angle = angle
        self.setPos(position)
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.timeout)
        self.timer.start(INTERVAL)

    def boundingRect(self):
        return Head.Rect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(Head.Rect)
        return path

    def paint(self, painter, option, widget=None):
        transform = self.transform()
        level_of_detail = option.levelOfDetailFromTransform(transform)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawEllipse(Head.Rect)
        if level_of_detail > 0.5:  # Outer eyes
            painter.setBrush(QtGui.QBrush(QtCore.Qt.yellow))
            painter.drawEllipse(-12, -19, 8, 8)
            painter.drawEllipse(-12, 11, 8, 8)
            if level_of_detail > 0.9:  # Inner eyes
                painter.setBrush(QtGui.QBrush(QtCore.Qt.darkBlue))
                painter.drawEllipse(-12, -19, 4, 4)
                painter.drawEllipse(-12, 11, 4, 4)
                if level_of_detail > 1.3:  # Nostrils
                    painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
                    painter.drawEllipse(-27, -5, 2, 2)
                    painter.drawEllipse(-27, 3, 2, 2)

    def timeout(self):
        if not Running:
            return
        angle = self.angle
        while True:
            angle += random.randint(-9, 9)
            offset = random.randint(3, 15)
            x = self.x() + (offset * math.sin(math.radians(angle)))
            y = self.y() + (offset * math.cos(math.radians(angle)))
            if 0 <= x <= SCENESIZE and 0 <= y <= SCENESIZE:
                break
        self.angle = angle
        self.setRotation(random.randint(-5, 5))
        self.setPos(QtCore.QPointF(x, y))
        for item in self.scene().collidingItems(self):
            if isinstance(item, Head):
                self.color.setRed(min(255, self.color.red() + 1))
            else:
                item.color.setBlue(min(255, item.color.blue() + 1))


class Segment(QtWidgets.QGraphicsItem):
    def __init__(self, color, offset, parent):
        super(Segment, self).__init__(parent)
        self.color = color
        self.rect = QtCore.QRectF(offset, -20, 30, 40)
        self.path = QtGui.QPainterPath()
        self.path.addEllipse(self.rect)
        x = offset + 15
        y = -20
        self.path.addPolygon(
            QtGui.QPolygonF(
                [
                    QtCore.QPointF(x, y),
                    QtCore.QPointF(x - 5, y - 12),
                    QtCore.QPointF(x - 5, y),
                ]
            )
        )
        self.path.closeSubpath()
        y = 20
        self.path.addPolygon(
            QtGui.QPolygonF(
                [
                    QtCore.QPointF(x, y),
                    QtCore.QPointF(x - 5, y + 12),
                    QtCore.QPointF(x - 5, y),
                ]
            )
        )
        self.path.closeSubpath()
        self.change = 1
        self.angle = 0
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.timeout)
        self.timer.start(INTERVAL)

    def boundingRect(self):
        return self.path.boundingRect()

    def shape(self):
        return self.path

    def paint(self, painter, option, widget=None):
        transform = self.transform()
        level_of_detail = option.levelOfDetailFromTransform(transform)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(self.color))
        if level_of_detail < 0.9:
            painter.drawEllipse(self.rect)
        else:
            painter.drawPath(self.path)

    def timeout(self):
        if not Running:
            return
        transform = self.transform()
        transform.reset()
        self.setTransform(transform)
        self.angle += self.change
        if self.angle > 5:
            self.change = -1
            self.angle -= 1
        elif self.angle < -5:
            self.change = 1
            self.angle += 1
        self.setRotation(self.angle)


class MainForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, SCENESIZE, SCENESIZE)
        self.scene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        self.view = QtWidgets.QGraphicsView()
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setScene(self.scene)
        self.view.setFocusPolicy(QtCore.Qt.NoFocus)
        zoomSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        zoomSlider.setRange(5, 200)
        zoomSlider.setValue(100)
        self.pauseButton = QtWidgets.QPushButton("Pa&use")
        quitButton = QtWidgets.QPushButton("&Quit")
        quitButton.setFocusPolicy(QtCore.Qt.NoFocus)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        bottomLayout = QtWidgets.QHBoxLayout()
        bottomLayout.addWidget(self.pauseButton)
        bottomLayout.addWidget(zoomSlider)
        bottomLayout.addWidget(quitButton)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

        self.connect(zoomSlider, QtCore.SIGNAL("valueChanged(int)"), self.zoom)
        self.connect(self.pauseButton, QtCore.SIGNAL("clicked()"), self.pauseOrResume)
        self.connect(quitButton, QtCore.SIGNAL("clicked()"), self.accept)

        self.populate()
        self.startTimer(INTERVAL)
        self.setWindowTitle("Multipedes")

    def zoom(self, value):
        factor = value / 100.0
        transform = self.view.transform()
        transform.reset()
        transform.scale(factor, factor)
        self.view.setTransform(transform)

    def pauseOrResume(self):
        global Running
        Running = not Running
        self.pauseButton.setText("Pa&use" if Running else "Res&ume")

    def populate(self):
        red, green, blue = 0, 150, 0
        for i in range(random.randint(6, 10)):
            angle = random.randint(0, 360)
            offset = random.randint(0, SCENESIZE // 2)
            half = SCENESIZE / 2
            x = half + (offset * math.sin(math.radians(angle)))
            y = half + (offset * math.cos(math.radians(angle)))
            color = QtGui.QColor(red, green, blue)
            head = Head(color, angle, QtCore.QPointF(x, y))
            color = QtGui.QColor(red, green + random.randint(10, 60), blue)
            offset = 25
            segment = Segment(color, offset, head)
            for j in range(random.randint(3, 7)):
                offset += 25
                segment = Segment(color, offset, segment)
            head.setRotation(random.randint(0, 360))
            self.scene.addItem(head)
        global Running
        Running = True

    def timerEvent(self, event):
        if not Running:
            return
        dead = set()
        items = self.scene.items()
        if len(items) == 0:
            self.populate()
            return
        heads = set()
        for item in items:
            if isinstance(item, Head):
                heads.add(item)
                if item.color.red() == 255:
                    dead.add(item)
        if len(heads) == 1:
            dead = heads
        del heads
        while dead:
            item = dead.pop()
            self.scene.removeItem(item)
            del item


app = QtWidgets.QApplication(sys.argv)
form = MainForm()
rect = QtGui.QScreen().availableGeometry()
form.resize(int(rect.width() * 0.75), int(rect.height() * 0.9))
form.show()
app.exec()
