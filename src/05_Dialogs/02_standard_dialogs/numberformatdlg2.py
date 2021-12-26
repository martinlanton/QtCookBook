from PySide6 import QtWidgets, QtCore, QtGui


class NumberFormatDlg(QtWidgets.QDialog):
    def __init__(self, format, parent=None):
        super(NumberFormatDlg, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        punctuationRe = QtWidgets.QRegExp(r"[ ,;:.]")
        thousandsLabel = QtWidgets.QLabel("&Thousands separator")
        self.thousandsEdit = QtWidgets.QLineEdit(format["thousandsseparator"])
        thousandsLabel.setBuddy(self.thousandsEdit)
        self.thousandsEdit.setMaxLength(1)
        self.thousandsEdit.setValidator(QtGui.QRegExpValidator(punctuationRe, self))

        decimalMarkerLabel = QtWidgets.QLabel("Decimal &marker")
        self.decimalMarkerEdit = QtWidgets.QLineEdit(format["decimalmarker"])
        decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)
        self.decimalMarkerEdit.setMaxLength(1)
        self.decimalMarkerEdit.setValidator(QtGui.QRegExpValidator(punctuationRe, self))
        self.decimalMarkerEdit.setInputMask("X")

        decimalPlacesLabel = QtWidgets.QLabel("&Decimal places")
        self.decimalPlacesSpinBox = QtWidgets.QSpinBox()
        decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format["decimalplaces"])

        self.redNegativesCheckBox = QtWidgets.QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format["rednegatives"])
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Apply |
                                               QtWidgets.QDialogButtonBox.Close)
