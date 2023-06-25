from PySide6 import QtWidgets


class Layout(QtWidgets.QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.line_edit_1 = QtWidgets.QLineEdit()
        self.addWidget(self.line_edit_1)
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.addWidget(self.line_edit_2)
