import sys
import math
from PySide6 import QtWidgets
from PySide6 import QtCore


class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.browser = QtWidgets.QTextBrowser()
        self.lineedit = QtWidgets.QLineEdit("Type an expression and press Enter")
        self.lineedit.selectAll()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()
        self.connect(self.lineedit, QtWidgets.SIGNAL("returnPressed()"),
                     self.updateUi)
        self.setWindowTitle("Calculate")
