import sys
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
        self.connect(self.lineedit, QtCore.SIGNAL("returnPressed()"),
                     self.updateUi)
        self.setWindowTitle("Calculate")

    def updateUi(self):
        text = str(self.lineedit.text())
        try:
            self.browser.append("{} = <b>{}</b>".format(text, eval(text)))
        except Exception:
            self.browser.append("<font color=red>{} is invalid!</font>".format(text))


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec()
