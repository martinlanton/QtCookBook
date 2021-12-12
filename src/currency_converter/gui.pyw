import sys
import csv
from pprint import pprint
import urllib.request
import datetime
from PySide6 import QtWidgets
from PySide6 import QtCore


class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.rates = Rates()
        dateLabel = QtWidgets.QLabel(self.rates.date)
        self.fromComboBox = QtWidgets.QComboBox()
        self.fromComboBox.addItems(self.rates.currencies)
        self.fromSpinBox = QtWidgets.QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 10000000.00)
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QtWidgets.QComboBox()
        self.toComboBox.addItems(self.rates.currencies)
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
        origin_currency_rate = self.rates.rates[from_]
        destination_currency_rate = self.rates.rates[to]

        if any([origin_currency_rate == "N/A", destination_currency_rate == "N/A"]):
            message = "Currency conversion not available for these currencies."
        else:
            amount = (origin_currency_rate / destination_currency_rate) * self.fromSpinBox.value()
            message = "%0.2f" % amount
        self.toLabel.setText(message)


class Rates(object):
    def __init__(self):
        self.url = "https://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/csv?start_date={}"
        self.date = "Unknown"
        self.rates = {"CAD": 1}
        self.data = self.download_file()
        self.currencies = list()
        self.sort_data()
        self.currencies.append("CAD")

    def download_file(self):
        today = datetime.date.today()
        time_delta = datetime.timedelta(days=today.weekday(), weeks=1)
        target_day = today - time_delta
        target_date = target_day.strftime("%Y-%m-%d")
        # Trying to get the date from there : https://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/
        with urllib.request.urlopen(self.url.format(target_date)) as response:  # doc is here : https://docs.python.org/3/howto/urllib2.html
            response = response.read().decode('utf-8')
            data = response.split("\n")
        return data

    def sort_data(self):
        rates = list()
        got_date = False
        for line in self.data:
            line_data = line.replace('"', '')
            if got_date and not line_data:
                break

            if not line_data:
                continue

            if line_data.startswith("FX"):
                currencies = line_data.split(",")[1]
                self.currencies.append(currencies.split("/")[0])
            elif line_data.startswith("date"):
                got_date = True
            elif got_date:
                print(type(line_data), line_data)
                splitted_line = line_data.split(",")
                self.date = splitted_line.pop(0)
                rates = [float(rate) if rate else "N/A" for rate in splitted_line]

        for i, rate in enumerate(rates):
            self.rates[self.currencies[i]] = rate


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec()
