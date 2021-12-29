from PySide6 import QtWidgets, QtCore, QtGui


class NumberFormatDlg(QtWidgets.QDialog):
    def __init__(self, format, refreshTable, parent=None):
        super(NumberFormatDlg, self).__init__(parent)

        self.callback = refreshTable

        punctuationRe = QtCore.QRegularExpression(r"[ ,;:.]")
        thousandsLabel = QtWidgets.QLabel("&Thousands separator")
        self.thousandsEdit = QtWidgets.QLineEdit(format["thousandsseparator"])
        thousandsLabel.setBuddy(self.thousandsEdit)
        self.thousandsEdit.setMaxLength(1)
        self.thousandsEdit.setValidator(QtGui.QRegularExpressionValidator(punctuationRe, self))

        decimalMarkerLabel = QtWidgets.QLabel("Decimal &marker")
        self.decimalMarkerEdit = QtWidgets.QLineEdit(format["decimalmarker"])
        decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)
        self.decimalMarkerEdit.setMaxLength(1)
        self.decimalMarkerEdit.setValidator(QtGui.QRegularExpressionValidator(punctuationRe, self))
        self.decimalMarkerEdit.setInputMask("X")

        decimalPlacesLabel = QtWidgets.QLabel("&Decimal places")
        self.decimalPlacesSpinBox = QtWidgets.QSpinBox()
        decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format["decimalplaces"])

        self.redNegativesCheckBox = QtWidgets.QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format["rednegatives"])

        self.format = format

        grid = QtWidgets.QGridLayout()
        grid.addWidget(thousandsLabel, 0, 0)
        grid.addWidget(self.thousandsEdit, 0, 1)
        grid.addWidget(decimalMarkerLabel, 1, 0)
        grid.addWidget(self.decimalMarkerEdit, 1, 1)
        grid.addWidget(decimalPlacesLabel, 2, 0)
        grid.addWidget(self.decimalPlacesSpinBox, 2, 1)
        grid.addWidget(self.redNegativesCheckBox, 3, 0, 1, 2)
        self.setLayout(grid)

        self.thousandsEdit.textEdited.connect(self.checkAndFix)
        self.decimalMarkerEdit.textEdited.connect(self.checkAndFix)
        self.decimalPlacesSpinBox.valueChanged.connect(self.apply)
        self.redNegativesCheckBox.toggled.connect(self.apply)

        self.setWindowTitle("Set Number Format (`Live')")

    def apply(self):
        self.format["thousandsseparator"] = str(self.thousandsEdit.text())
        self.format["decimalmarker"] = str(self.decimalMarkerEdit.text())
        self.format["decimalplaces"] = self.decimalPlacesSpinBox.value()
        self.format["rednegatives"] = self.redNegativesCheckBox.isChecked()
        self.callback()

    def checkAndFix(self):
        thousands = str(self.thousandsEdit.text())
        decimal = str(self.decimalMarkerEdit.text())
        if thousands == decimal:
            self.thousandsEdit.clear()
            self.thousandsEdit.setFocus()
        if len(decimal) == 0:
            self.decimalMarkerEdit.setText(".")
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
        self.apply()
