from PySide6 import QtWidgets, QtCore, QtGui


class NumberFormatDlg(QtWidgets.QDialog):

    changed = QtCore.Signal()

    def __init__(self, format, parent=None):
        super(NumberFormatDlg, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
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
        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Close
        )

        self.format = format

        grid = QtWidgets.QGridLayout()
        grid.addWidget(thousandsLabel, 0, 0)
        grid.addWidget(self.thousandsEdit, 0, 1)
        grid.addWidget(decimalMarkerLabel, 1, 0)
        grid.addWidget(self.decimalMarkerEdit, 1, 1)
        grid.addWidget(decimalPlacesLabel, 2, 0)
        grid.addWidget(self.decimalPlacesSpinBox, 2, 1)
        grid.addWidget(self.redNegativesCheckBox, 3, 0, 1, 2)
        grid.addWidget(buttonBox, 4, 0, 1, 2)
        self.setLayout(grid)

        buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(
            self.apply,
        )
        buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Set Number Format (Modeless)")

    def apply(self):
        thousands = str(self.thousandsEdit.text())
        decimal = str(self.decimalMarkerEdit.text())

        if thousands == decimal:
            QtWidgets.QMessageBox.warning(
                self,
                "Format Error",
                "The thousands separator and the decimal marker " "must be different.",
            )
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return

        if len(decimal) == 0:
            QtWidgets.QMessageBox.warning(
                self, "Format Error", "The decimal marker may not be empty."
            )
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
            return

        self.format["thousandsseparator"] = thousands
        self.format["decimalmarker"] = decimal
        self.format["decimalplaces"] = self.decimalPlacesSpinBox.value()
        self.format["rednegatives"] = self.redNegativesCheckBox.isChecked()
        self.changed.emit()
