import sys
from PySide6 import QtWidgets, QtCore
from functools import partial


class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        button1 = QtWidgets.QPushButton("One")
        layout.addWidget(button1)
        button2 = QtWidgets.QPushButton("Two")
        layout.addWidget(button2)
        button3 = QtWidgets.QPushButton("Three")
        layout.addWidget(button3)
        button4 = QtWidgets.QPushButton("Four")
        layout.addWidget(button4)
        button5 = QtWidgets.QPushButton("Five")
        layout.addWidget(button5)
        self.label = QtWidgets.QLabel("Nothing to say here.")
        layout.addWidget(self.label)

        self.connect(button1, QtCore.SIGNAL("clicked()"), self.one)
        self.connect(
            button2, QtCore.SIGNAL("clicked()"), partial(self.any_button, "Two")
        )
        button3_callback = lambda value="Three": self.any_button(value)
        self.connect(button3, QtCore.SIGNAL("clicked()"), button3_callback)
        self.connect(
            button4,
            QtCore.SIGNAL("clicked()"),
            lambda value="Four": self.any_button(value),
        )
        self.connect(button5, QtCore.SIGNAL("clicked()"), self.clicked)

    def one(self):
        self.label.setText("You clicked button 'One'")

    def any_button(self, value):
        self.label.setText("You clicked button '{}'".format(value))

    def clicked(self):
        button = self.sender()
        if button is None or not isinstance(button, QtWidgets.QPushButton):
            return
        self.label.setText("You clicked button '{}'".format(button.text()))


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec()
