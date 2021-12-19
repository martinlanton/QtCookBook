from PySide6 import QtWidgets, QtCore


def setPenProperties(self):
    dialog = PenPropertiesDlg(self)
    dialog.widthSpinBox.setValue(self.width)
    dialog.beveledCheckBox.setChecked(self.beveled)
    dialog.styleComboBox.setCurrentIndex(
    dialog.styleComboBox.findText(self.style))
    if dialog.exec_():
        self.width = dialog.widthSpinBox.value()
        self.beveled = dialog.beveledCheckBox.isChecked()
        self.style = str(dialog.styleComboBox.currentText())
        self.updateData()


class PenPropertiesDlg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PenPropertiesDlg, self).__init__(parent)
        widthLabel = QtWidgets.QLabel("&Width:")
        self.widthSpinBox = QtWidgets.QSpinBox()
        widthLabel.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.widthSpinBox.setRange(0, 24)
        self.beveledCheckBox = QtWidgets.QCheckBox("&Beveled edges")
        styleLabel = QtWidgets.QLabel("&Style:")
        self.styleComboBox = QtWidgets.QComboBox()
        styleLabel.setBuddy(self.styleComboBox)
        self.styleComboBox.addItems(["Solid", "Dashed", "Dotted",
                                     "DashDotted", "DashDotDotted"])
        okButton =QtWidgets. QPushButton("&OK")
        cancelButton = QtWidgets.QPushButton("Cancel")