import logging
from PySide6 import QtWidgets, QtGui


log = logging.getLogger(__name__)


class Layout(QtWidgets.QVBoxLayout):
    def __init__(self, parent=None):
        super(Layout, self).__init__(parent)
        self.button_1 = ButtonOne("one")
        self.addWidget(self.button_1)
        self.button_2 = QtWidgets.QPushButton("two")
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


class ButtonOne(QtWidgets.QPushButton):
    def mouseMoveEvent(self, event) -> None:
        log.info("Moving from button 1")
        return


class ButtonTwo(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(ButtonTwo, self).__init__(parent)

    def mouseMoveEvent(self, arg__1: QtGui.QMouseEvent) -> None:
        log.info("Moving to button 2")
        return

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        log.info("Releasing on button 2")
        return
