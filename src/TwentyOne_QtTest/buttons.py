import logging
from PySide6 import QtWidgets


log = logging.getLogger(__name__)


class Layout(QtWidgets.QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.button_1 = QtWidgets.QPushButton()
        self.addWidget(self.button_1)
        self.button_2 = QtWidgets.QPushButton()
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
