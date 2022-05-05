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


class ContactDlg(QtWidgets.QDialog):

    StyleSheet = """
QComboBox { color: darkblue; }
QLineEdit { color: darkgreen; }
QLineEdit[mandatory="1"] {
    background-color: rgb(255, 255, 127);
    color: darkblue;
}
"""

    def __init__(self, parent=None):
        super(ContactDlg, self).__init__(parent)

        forenameLabel = QtWidgets.QLabel("&Forename:")
        self.forenameEdit = QtWidgets.QLineEdit()
        forenameLabel.setBuddy(self.forenameEdit)
        surnameLabel = QtWidgets.QLabel("&Surname:")
        self.surnameEdit = QtWidgets.QLineEdit()
        surnameLabel.setBuddy(self.surnameEdit)
        categoryLabel = QtWidgets.QLabel("&Category:")
        self.categoryComboBox = QtWidgets.QComboBox()
        categoryLabel.setBuddy(self.categoryComboBox)
        self.categoryComboBox.addItems(["Business", "Domestic", "Personal"])
        companyLabel = QtWidgets.QLabel("C&ompany:")
        self.companyEdit = QtWidgets.QLineEdit()
        companyLabel.setBuddy(self.companyEdit)
        addressLabel = QtWidgets.QLabel("A&ddress:")
        self.addressEdit = QtWidgets.QLineEdit()
        addressLabel.setBuddy(self.addressEdit)
        phoneLabel = QtWidgets.QLabel("&Phone:")
        self.phoneEdit = QtWidgets.QLineEdit()
        phoneLabel.setBuddy(self.phoneEdit)
        mobileLabel = QtWidgets.QLabel("&Mobile:")
        self.mobileEdit = QtWidgets.QLineEdit()
        mobileLabel.setBuddy(self.mobileEdit)
        faxLabel = QtWidgets.QLabel("Fa&x:")
        self.faxEdit = QtWidgets.QLineEdit()
        faxLabel.setBuddy(self.faxEdit)
        emailLabel = QtWidgets.QLabel("&Email:")
        self.emailEdit = QtWidgets.QLineEdit()
        emailLabel.setBuddy(self.emailEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        addButton = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        addButton.setText("&Add")
        addButton.setEnabled(False)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(forenameLabel, 0, 0)
        grid.addWidget(self.forenameEdit, 0, 1)
        grid.addWidget(surnameLabel, 0, 2)
        grid.addWidget(self.surnameEdit, 0, 3)
        grid.addWidget(categoryLabel, 1, 0)
        grid.addWidget(self.categoryComboBox, 1, 1)
        grid.addWidget(companyLabel, 1, 2)
        grid.addWidget(self.companyEdit, 1, 3)
        grid.addWidget(addressLabel, 2, 0)
        grid.addWidget(self.addressEdit, 2, 1, 1, 3)
        grid.addWidget(phoneLabel, 3, 0)
        grid.addWidget(self.phoneEdit, 3, 1)
        grid.addWidget(mobileLabel, 3, 2)
        grid.addWidget(self.mobileEdit, 3, 3)
        grid.addWidget(faxLabel, 4, 0)
        grid.addWidget(self.faxEdit, 4, 1)
        grid.addWidget(emailLabel, 4, 2)
        grid.addWidget(self.emailEdit, 4, 3)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.lineedits = (
            self.forenameEdit,
            self.surnameEdit,
            self.companyEdit,
            self.phoneEdit,
            self.emailEdit,
        )
        for lineEdit in self.lineedits:
            lineEdit.setProperty("mandatory", 1)
            self.connect(lineEdit, QtCore.SIGNAL("textEdited(QString)"), self.updateUi)
        self.connect(
            self.categoryComboBox, QtCore.SIGNAL("activated(int)"), self.updateUi
        )

        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)

        self.setStyleSheet(ContactDlg.StyleSheet)
        self.setWindowTitle("Add Contact")

    def updateUi(self):
        mandatory = bool(int(self.companyEdit.property("mandatory")))
        if self.categoryComboBox.currentText() == "Business":
            if not mandatory:
                self.companyEdit.setProperty("mandatory", 1)
        elif mandatory:
            self.companyEdit.setProperty("mandatory", 0)
        if mandatory != bool(int(self.companyEdit.property("mandatory"))):
            self.setStyleSheet(ContactDlg.StyleSheet)
        enable = True
        for lineEdit in self.lineedits:
            if bool(int(lineEdit.property("mandatory"))) and not lineEdit.text():
                enable = False
                break
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(enable)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = ContactDlg()
    form.show()
    app.exec()
