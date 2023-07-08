import logging
from PySide6 import QtWidgets, QtGui, QtCore


log = logging.getLogger(__name__)


class Layout(QtWidgets.QVBoxLayout):
    def __init__(self, parent=None):
        super(Layout, self).__init__(parent)
        self.button_1 = Button("one")
        self.addWidget(self.button_1)
        self.button_2 = Button("two")
        self.addWidget(self.button_2)

        self.button_1.clicked.connect(self.print_click_1)
        self.button_2.clicked.connect(self.print_click_2)

        self.button_1.pressed.connect(self.print_pressed_1)
        self.button_2.pressed.connect(self.print_pressed_2)

        self.button_1.released.connect(self.print_released_1)
        self.button_2.released.connect(self.print_released_2)

    def print_click_1(self):
        log.info("Hello")

    def print_click_2(self):
        log.info("World")

    def print_pressed_1(self):
        log.info("Tralala")

    def print_pressed_2(self):
        log.info("Pouetpouet")

    def print_released_1(self):
        log.info("Foo")

    def print_released_2(self):
        log.info("Bar")


class Button(QtWidgets.QPushButton):
    def __init__(self, name, parent=None):
        super(Button, self).__init__(name, parent)
        self.name = name
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        log.info("Moving to button %s", self.name)
        event.accept()

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        log.info("Moving on button %s", self.name)
        event.accept()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        log.info("Releasing on button %s", self.name)
        event.accept()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        log.debug("Moving from button %s", self.name)

        if event.buttons() == QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            mime = QtCore.QMimeData()
            drag.setMimeData(mime)
            drag.exec_(QtCore.Qt.MoveAction)
        return

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        log.info("Releasing on button %s", self.name)
        event.accept()
        return
