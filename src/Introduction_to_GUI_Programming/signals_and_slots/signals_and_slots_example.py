import sys
from PySide6 import QtWidgets, QtCore


class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        dial = QtWidgets.QDial()
        dial.setNotchesVisible(True)
        spinbox = ZeroSpinBox()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(spinbox)
        self.setLayout(layout)
        self.connect(dial, QtCore.SIGNAL("valueChanged(int)"), spinbox.setValue)
        self.connect(spinbox, QtCore.SIGNAL("valueChanged(int)"), dial.setValue)
        self.connect(spinbox, QtCore.SIGNAL("atzero"), self.announce)
        self.setWindowTitle("Signals and Slots")

    def announce(self, zeros):
        print("ZeroSpinBox has been at zero {} times".format(zeros))


class ZeroSpinBox(QtWidgets.QSpinBox):
    zeros = 0

    def __init__(self, parent=None):
        """We connect to the spinbox’s own valueChanged() signal and have it call our
        checkzero() slot."""
        super(ZeroSpinBox, self).__init__(parent)
        self.connect(self, QtCore.SIGNAL("valueChanged(int)"), self.checkzero)

    def checkzero(self):
        """If the value happens to be 0, the checkzero() slot emits the
        atzero signal, along with a count of how many times it has been zero; passing
        additional data like this is optional. The lack of parentheses for the signal is
        important: It tells PyQt that this is a “short-circuit” signal (as opposed to
        "valueChanged(int)" which contains parentheses in the signal type).

        A signal with no arguments (and therefore no parentheses) is a short-circuit
        Python signal. When such a signal is emitted, any data can be passed as
        additional arguments to the emit() method, and they are passed as Python
        objects. This avoids the overhead of converting the arguments to and fromC++
        data types, and also means that arbitrary Python objects can be passed, even
        ones which cannot be converted to and from C++ data types. A signal with at
        least one argument is either a Qt signal or a non-short-circuit Python signal.
        In these cases, PyQt will check to see whether the signal is a Qt signal, and if
        it is not will assume that it is a Python signal. In either case, the arguments
        are converted to C++ data types."""
        if self.value() == 0:
            self.zeros += 1
            self.emit(QtCore.SIGNAL("atzero"), self.zeros)


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec()
