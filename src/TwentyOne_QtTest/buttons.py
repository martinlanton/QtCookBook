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

        self.button_1.clicked.connect(self.print_1)
        self.button_2.clicked.connect(self.print_2)

    def print_1(self):
        log.info("Hello")

    def print_2(self):
        log.info("World")
