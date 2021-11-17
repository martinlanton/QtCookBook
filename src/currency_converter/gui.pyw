import sys
import urllib
from PySide6 import QtWidgets
from PySide6 import QtCore


class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.rates = {}
        date = self.getdata()
        rates = sorted(self.rates.keys())
        dateLabel = QtWidgets.QLabel(date)
        self.fromComboBox = QtWidgets.QComboBox()
        self.fromComboBox.addItems(rates)
        self.fromSpinBox = QtWidgets.QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 10000000.00)
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QtWidgets.QComboBox()
        self.toComboBox.addItems(rates)
        self.toLabel = QtWidgets.QLabel("1.00")

        grid = QtWidgets.QGridLayout()
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)

        self.connect(self.fromComboBox,
                     QtCore.SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.connect(self.toComboBox,
                     QtCore.SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.connect(self.fromSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"), self.updateUi)
        self.setWindowTitle("Currency")

    def updateUi(self):
        to = str(self.toComboBox.currentText())

        from_ = str(self.fromComboBox.currentText())
        amount = (self.rates[from_] / self.rates[to]) * self.fromSpinBox.value()
        self.toLabel.setText("%0.2f" % amount)

    def getdata(self):  # Idea taken from the Python Cookbook
        try:
            date = "Unknown"
            fh = urllib.urlopen("http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv")  # doc is here : https://docs.python.org/3/howto/urllib2.html
            for line in fh:
                if not line or line.startswith(("#", "Closing ")):
                    continue
                fields = line.split(",")
                if line.startswith("Date "):
                    date = fields[-1]
                else:
                    try:
                        value = float(fields[-1])
                        self.rates[str(fields[0])] = value
                    except ValueError:
                        pass
            return "Exchange Rates Date: " + date
        except Exception as e:
            return "Failed to download:\n%s" % e


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
