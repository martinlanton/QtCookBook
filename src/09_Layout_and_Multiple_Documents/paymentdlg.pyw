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


class PaymentDlg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PaymentDlg, self).__init__(parent)

        forenameLabel = QtWidgets.QLabel("&Forename:")
        self.forenameLineEdit = QtWidgets.QLineEdit()
        forenameLabel.setBuddy(self.forenameLineEdit)
        surnameLabel = QtWidgets.QLabel("&Surname:")
        self.surnameLineEdit = QtWidgets.QLineEdit()
        surnameLabel.setBuddy(self.surnameLineEdit)
        invoiceLabel = QtWidgets.QLabel("&Invoice No.:")
        self.invoiceSpinBox = QtWidgets.QSpinBox()
        invoiceLabel.setBuddy(self.invoiceSpinBox)
        self.invoiceSpinBox.setRange(1, 10000000)
        self.invoiceSpinBox.setValue(100000)
        self.invoiceSpinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        amountLabel = QtWidgets.QLabel("&Amount:")
        self.amountSpinBox = QtWidgets.QDoubleSpinBox()
        amountLabel.setBuddy(self.amountSpinBox)
        self.amountSpinBox.setRange(0, 5000.0)
        self.amountSpinBox.setPrefix("$ ")
        self.amountSpinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.paidCheckBox = QtWidgets.QCheckBox("&Paid")
        checkNumLabel = QtWidgets.QLabel("Check &No.:")
        self.checkNumLineEdit = QtWidgets.QLineEdit()
        checkNumLabel.setBuddy(self.checkNumLineEdit)
        bankLabel = QtWidgets.QLabel("&Bank:")
        self.bankLineEdit = QtWidgets.QLineEdit()
        bankLabel.setBuddy(self.bankLineEdit)
        accountNumLabel = QtWidgets.QLabel("Acco&unt No.:")
        self.accountNumLineEdit = QtWidgets.QLineEdit()
        accountNumLabel.setBuddy(self.accountNumLineEdit)
        sortCodeLabel = QtWidgets.QLabel("Sort &Code:")
        self.sortCodeLineEdit = QtWidgets.QLineEdit()
        sortCodeLabel.setBuddy(self.sortCodeLineEdit)
        creditCardLabel = QtWidgets.QLabel("&Number:")
        self.creditCardLineEdit = QtWidgets.QLineEdit()
        creditCardLabel.setBuddy(self.creditCardLineEdit)
        validFromLabel = QtWidgets.QLabel("&Valid From:")
        self.validFromDateEdit = QtWidgets.QDateEdit()
        validFromLabel.setBuddy(self.validFromDateEdit)
        self.validFromDateEdit.setDisplayFormat("MMM yyyy")
        self.validFromDateEdit.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        expiryLabel = QtWidgets.QLabel("E&xpiry Date:")
        self.expiryDateEdit = QtWidgets.QDateEdit()
        expiryLabel.setBuddy(self.expiryDateEdit)
        self.expiryDateEdit.setDisplayFormat("MMM yyyy")
        self.expiryDateEdit.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        tabWidget = QtWidgets.QTabWidget()

        cashWidget = QtWidgets.QWidget()
        cashLayout = QtWidgets.QHBoxLayout()
        cashLayout.addWidget(self.paidCheckBox)
        cashWidget.setLayout(cashLayout)
        tabWidget.addTab(cashWidget, "Cas&h")

        checkWidget = QtWidgets.QWidget()
        checkLayout = QtWidgets.QGridLayout()
        checkLayout.addWidget(checkNumLabel, 0, 0)
        checkLayout.addWidget(self.checkNumLineEdit, 0, 1)
        checkLayout.addWidget(bankLabel, 0, 2)
        checkLayout.addWidget(self.bankLineEdit, 0, 3)
        checkLayout.addWidget(accountNumLabel, 1, 0)
        checkLayout.addWidget(self.accountNumLineEdit, 1, 1)
        checkLayout.addWidget(sortCodeLabel, 1, 2)
        checkLayout.addWidget(self.sortCodeLineEdit, 1, 3)
        checkWidget.setLayout(checkLayout)
        tabWidget.addTab(checkWidget, "Chec&k")

        creditWidget = QtWidgets.QWidget()
        creditLayout = QtWidgets.QGridLayout()
        creditLayout.addWidget(creditCardLabel, 0, 0)
        creditLayout.addWidget(self.creditCardLineEdit, 0, 1, 1, 3)
        creditLayout.addWidget(validFromLabel, 1, 0)
        creditLayout.addWidget(self.validFromDateEdit, 1, 1)
        creditLayout.addWidget(expiryLabel, 1, 2)
        creditLayout.addWidget(self.expiryDateEdit, 1, 3)
        creditWidget.setLayout(creditLayout)
        tabWidget.addTab(creditWidget, "Credit Car&d")

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(forenameLabel, 0, 0)
        gridLayout.addWidget(self.forenameLineEdit, 0, 1)
        gridLayout.addWidget(surnameLabel, 0, 2)
        gridLayout.addWidget(self.surnameLineEdit, 0, 3)
        gridLayout.addWidget(invoiceLabel, 1, 0)
        gridLayout.addWidget(self.invoiceSpinBox, 1, 1)
        gridLayout.addWidget(amountLabel, 1, 2)
        gridLayout.addWidget(self.amountSpinBox, 1, 3)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addWidget(tabWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        for lineEdit in (
            self.forenameLineEdit,
            self.surnameLineEdit,
            self.checkNumLineEdit,
            self.accountNumLineEdit,
            self.bankLineEdit,
            self.sortCodeLineEdit,
            self.creditCardLineEdit,
        ):
            self.connect(lineEdit, QtCore.SIGNAL("textEdited(QString)"), self.updateUi)
        for dateEdit in (self.validFromDateEdit, self.expiryDateEdit):
            self.connect(dateEdit, QtCore.SIGNAL("dateChanged(QDate)"), self.updateUi)
        self.connect(self.paidCheckBox, QtCore.SIGNAL("clicked()"), self.updateUi)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)

        self.updateUi()
        self.setWindowTitle("Payment Form")

    def updateUi(self):
        today = QtCore.QDate.currentDate()
        enable = bool(self.forenameLineEdit.text()) or bool(self.surnameLineEdit.text())
        if enable:  ### TODO CHECK THE LOGIC!!!
            enable = (
                self.paidCheckBox.isChecked()
                or (
                    bool(self.checkNumLineEdit.text())
                    and bool(self.accountNumLineEdit.text())
                    and bool(self.bankLineEdit.text())
                    and bool(self.sortCodeLineEdit.text())
                )
                or (
                    bool(self.creditCardLineEdit.text())
                    and self.validFromDateEdit.date() <= today
                    and self.expiryDateEdit.date() >= today
                )
            )
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(enable)


app = QtWidgets.QApplication(sys.argv)
form = PaymentDlg()
form.show()
app.exec_()
