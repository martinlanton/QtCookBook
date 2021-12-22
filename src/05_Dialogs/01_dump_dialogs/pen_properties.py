import sys
from PySide6 import QtWidgets, QtCore


class PenActions(QtWidgets.QDialog):
    def __init__(self):
        super(PenActions, self).__init__()
        self.width = 1
        self.beveled = False
        self.style = "Solid"
        layout = QtWidgets.QHBoxLayout(self)
        self.open = QtWidgets.QPushButton("Open Options")
        self.open.clicked.connect(self.setPenProperties)
        layout.addWidget(self.open)

    def updateData(self):
        print("Pen width is {}".format(self.width))
        print("Pen beveled is {}".format(self.beveled))
        print("Pen style is {}".format(self.style))

    def setPenProperties(self):
        dialog = PenPropertiesDlg(self)
        dialog.widthSpinBox.setValue(self.width)
        dialog.beveledCheckBox.setChecked(self.beveled)
        dialog.styleComboBox.setCurrentIndex(dialog.styleComboBox.findText(self.style))
        if dialog.exec():
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
        self.styleComboBox.addItems(
            ["Solid", "Dashed", "Dotted", "DashDotted", "DashDotDotted"]
        )
        okButton = QtWidgets.QPushButton("&OK")
        cancelButton = QtWidgets.QPushButton("Cancel")

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(widthLabel, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(self.beveledCheckBox, 0, 2)
        layout.addWidget(styleLabel, 1, 0)
        layout.addWidget(self.styleComboBox, 1, 1, 1, 2)
        layout.addLayout(buttonLayout, 2, 0, 1, 3)
        self.setLayout(layout)


app = QtWidgets.QApplication(sys.argv)
form = PenActions()
form.show()
app.exec()
