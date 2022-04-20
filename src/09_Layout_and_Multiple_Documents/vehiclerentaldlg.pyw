#!/usr/bin/env python3
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import sys
from PySide6 import QtWidgets, QtCore


class VehicleRentalDlg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(VehicleRentalDlg, self).__init__(parent)

        vehicleLabel = QtWidgets.QLabel("&Vehicle Type:")
        self.vehicleComboBox = QtWidgets.QComboBox()
        vehicleLabel.setBuddy(self.vehicleComboBox)
        self.vehicleComboBox.addItems(["Car", "Van"])
        colorLabel = QtWidgets.QLabel("Co&lor:")
        self.colorComboBox = QtWidgets.QComboBox()
        colorLabel.setBuddy(self.colorComboBox)
        self.colorComboBox.addItems(
            ["Black", "Blue", "Green", "Red", "Silver", "White", "Yellow"]
        )
        seatsLabel = QtWidgets.QLabel("&Seats:")
        self.seatsSpinBox = QtWidgets.QSpinBox()
        seatsLabel.setBuddy(self.seatsSpinBox)
        self.seatsSpinBox.setRange(2, 12)
        self.seatsSpinBox.setValue(4)
        self.seatsSpinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        weightLabel = QtWidgets.QLabel("&Weight:")
        self.weightSpinBox = QtWidgets.QSpinBox()
        weightLabel.setBuddy(self.weightSpinBox)
        self.weightSpinBox.setRange(1, 8)
        self.weightSpinBox.setValue(1)
        self.weightSpinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.weightSpinBox.setSuffix(" tons")
        volumeLabel = QtWidgets.QLabel("Volu&me")
        self.volumeSpinBox = QtWidgets.QSpinBox()
        volumeLabel.setBuddy(self.volumeSpinBox)
        self.volumeSpinBox.setRange(4, 22)
        self.volumeSpinBox.setValue(10)
        self.volumeSpinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.volumeSpinBox.setSuffix(" cu m")
        mileageLabel = QtWidgets.QLabel("Max. Mileage")
        self.mileageLabel = QtWidgets.QLabel("1000 miles")
        self.mileageLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.mileageLabel.setFrameStyle(
            QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken
        )
        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        self.stackedWidget = QtWidgets.QStackedWidget()

        carWidget = QtWidgets.QWidget()
        carLayout = QtWidgets.QGridLayout()
        carLayout.addWidget(colorLabel, 0, 0)
        carLayout.addWidget(self.colorComboBox, 0, 1)
        carLayout.addWidget(seatsLabel, 1, 0)
        carLayout.addWidget(self.seatsSpinBox, 1, 1)
        carWidget.setLayout(carLayout)
        self.stackedWidget.addWidget(carWidget)

        vanWidget = QtWidgets.QWidget()
        vanLayout = QtWidgets.QGridLayout()
        vanLayout.addWidget(weightLabel, 0, 0)
        vanLayout.addWidget(self.weightSpinBox, 0, 1)
        vanLayout.addWidget(volumeLabel, 1, 0)
        vanLayout.addWidget(self.volumeSpinBox, 1, 1)
        vanWidget.setLayout(vanLayout)
        self.stackedWidget.addWidget(vanWidget)

        topLayout = QtWidgets.QHBoxLayout()
        topLayout.addWidget(vehicleLabel)
        topLayout.addWidget(self.vehicleComboBox)
        bottomLayout = QtWidgets.QHBoxLayout()
        bottomLayout.addWidget(mileageLabel)
        bottomLayout.addWidget(self.mileageLabel)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addWidget(self.stackedWidget)
        layout.addLayout(bottomLayout)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.vehicleComboBox.currentIndexChanged.connect(self.setWidgetStack)

        self.weightSpinBox.valueChanged.connect(self.weightChanged)

        self.setWindowTitle("Vehicle Rental")

    def setWidgetStack(self, index):
        if index == 0:
            print("It's a car, switching to Van.")
            self.stackedWidget.setCurrentIndex(index)
            self.mileageLabel.setText("1000 miles")
        else:
            print("It's a van, switching to car.")
            self.stackedWidget.setCurrentIndex(index)
            self.weightChanged(self.weightSpinBox.value())

    def weightChanged(self, amount):
        self.mileageLabel.setText("{} miles".format(8000 / amount))


app = QtWidgets.QApplication(sys.argv)
form = VehicleRentalDlg()
form.show()
app.exec()
