import sys
from PySide6 import QtWidgets
from functools import partial


class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        button1 = QtWidgets.QPushButton("One")
        button2 = QtWidgets.QPushButton("Two")
        button3 = QtWidgets.QPushButton("Three")
        button4 = QtWidgets.QPushButton("Four")
        button5 = QtWidgets.QPushButton("Five")

        self.connect(button1, QtWidgets.SIGNAL("clicked()"), self.one)
        self.connect(button2, QtWidgets.SIGNAL("clicked()"), partial(self.any_button, "Two"))
        button3_callback = lambda value="Three": self.any_button(value)
        self.connect(button3, QtWidgets.SIGNAL("clicked()"), button3_callback)
        self.connect(button4, QtWidgets.SIGNAL("clicked()"), lambda value="Four": self.any_button(value))
        self.connect(button5, QtWidgets.SIGNAL("clicked()"), self.clicked)

    def one(self):
        self.label.setText("You clicked button 'One'")

    def any_button(self, value):
        self.label.setText("You clicked button '{}'".format(value))

    def clicked(self):
        button = self.sender()
        if button is None or not isinstance(button, QtWidgets.QPushButton):
            return
        self.label.setText("You clicked button '%s'".format(button.text()))


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec()
