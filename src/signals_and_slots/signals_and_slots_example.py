import sys
from PySide6 import QtWidgets, QtCore


class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        dial = QtWidgets.QDial()
        dial.setNotchesVisible(True)
        spinbox = QtWidgets.QSpinBox()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(spinbox)
        self.setLayout(layout)
        self.connect(dial, QtCore.SIGNAL("valueChanged(int)"), spinbox.setValue)
        self.connect(spinbox, QtCore.SIGNAL("valueChanged(int)"), dial.setValue)
        self.setWindowTitle("Signals and Slots")


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec()
