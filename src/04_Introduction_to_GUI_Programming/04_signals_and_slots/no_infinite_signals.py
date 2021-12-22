from PySide6 import QtCore


class TaxRate(QtCore.QObject):
    def __init__(self):
        super(TaxRate, self).__init__()
        self.__rate = 17.5

    def rate(self):
        return self.__rate

    def setRate(self, rate):
        if rate != self.__rate:
            self.__rate = rate
            self.emit(QtCore.SIGNAL("rateChanged"), self.__rate)


def rateChanged(value):
    print("TaxRate changed to %.2f%%" % value)


vat = TaxRate()
vat.connect(vat, QtCore.SIGNAL("rateChanged"), rateChanged)
vat.setRate(17.5)  # No change will occur (new rate is the same)
vat.setRate(8.5)  # A change will occur (new rate is different)
