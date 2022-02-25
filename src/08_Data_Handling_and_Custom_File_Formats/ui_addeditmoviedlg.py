# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addeditmoviedlg.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PySide6 import QtWidgets, QtCore


class Ui_AddEditMovieDlg(object):
    def setupUi(self, AddEditMovieDlg):
        if not AddEditMovieDlg.objectName():
            AddEditMovieDlg.setObjectName(u"AddEditMovieDlg")
        AddEditMovieDlg.resize(484, 334)
        self.gridLayout = QtWidgets.QGridLayout(AddEditMovieDlg)
        # ifndef Q_OS_MAC
        self.gridLayout.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        # endif
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(AddEditMovieDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel
            | QtWidgets.QDialogButtonBox.NoButton
            | QtWidgets.QDialogButtonBox.Ok
        )

        self.gridLayout.addWidget(self.buttonBox, 4, 4, 1, 2)

        self.titleLineEdit = QtWidgets.QLineEdit(AddEditMovieDlg)
        self.titleLineEdit.setObjectName(u"titleLineEdit")

        self.gridLayout.addWidget(self.titleLineEdit, 0, 1, 1, 5)

        self.label_5 = QtWidgets.QLabel(AddEditMovieDlg)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 2)

        self.notesTextEdit = QtWidgets.QTextEdit(AddEditMovieDlg)
        self.notesTextEdit.setObjectName(u"notesTextEdit")
        self.notesTextEdit.setTabChangesFocus(True)
        self.notesTextEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.notesTextEdit.setAcceptRichText(False)

        self.gridLayout.addWidget(self.notesTextEdit, 3, 0, 1, 6)

        self.label_2 = QtWidgets.QLabel(AddEditMovieDlg)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.yearSpinBox = QtWidgets.QSpinBox(AddEditMovieDlg)
        self.yearSpinBox.setObjectName(u"yearSpinBox")
        self.yearSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.yearSpinBox.setMaximum(2100)
        self.yearSpinBox.setMinimum(1890)
        self.yearSpinBox.setValue(1890)

        self.gridLayout.addWidget(self.yearSpinBox, 1, 1, 1, 1)

        self.label_3 = QtWidgets.QLabel(AddEditMovieDlg)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)

        self.minutesSpinBox = QtWidgets.QSpinBox(AddEditMovieDlg)
        self.minutesSpinBox.setObjectName(u"minutesSpinBox")
        self.minutesSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.minutesSpinBox.setMaximum(720)

        self.gridLayout.addWidget(self.minutesSpinBox, 1, 3, 1, 1)

        self.label_4 = QtWidgets.QLabel(AddEditMovieDlg)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 4, 1, 1)

        self.acquiredDateEdit = QtWidgets.QDateEdit(AddEditMovieDlg)
        self.acquiredDateEdit.setObjectName(u"acquiredDateEdit")
        self.acquiredDateEdit.setAlignment(QtCore.Qt.AlignRight)

        self.gridLayout.addWidget(self.acquiredDateEdit, 1, 5, 1, 1)

        self.label = QtWidgets.QLabel(AddEditMovieDlg)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        # if QT_CONFIG(shortcut)
        self.label_5.setBuddy(self.notesTextEdit)
        self.label_2.setBuddy(self.yearSpinBox)
        self.label_3.setBuddy(self.minutesSpinBox)
        self.label_4.setBuddy(self.acquiredDateEdit)
        self.label.setBuddy(self.titleLineEdit)
        # endif // QT_CONFIG(shortcut)
        QtWidgets.QWidget.setTabOrder(self.titleLineEdit, self.yearSpinBox)
        QtWidgets.QWidget.setTabOrder(self.yearSpinBox, self.minutesSpinBox)
        QtWidgets.QWidget.setTabOrder(self.minutesSpinBox, self.acquiredDateEdit)
        QtWidgets.QWidget.setTabOrder(self.acquiredDateEdit, self.notesTextEdit)
        QtWidgets.QWidget.setTabOrder(self.notesTextEdit, self.buttonBox)

        self.retranslateUi(AddEditMovieDlg)
        self.buttonBox.accepted.connect(AddEditMovieDlg.accept)
        self.buttonBox.rejected.connect(AddEditMovieDlg.reject)

        QtCore.QMetaObject.connectSlotsByName(AddEditMovieDlg)
        # setupUi

    def retranslateUi(self, AddEditMovieDlg):
        AddEditMovieDlg.setWindowTitle(
            QtWidgets.QApplication.translate(
                "AddEditMovieDlg", u"My Movies - Add Movie", None
            )
        )
        self.label_5.setText(
            QtWidgets.QApplication.translate("AddEditMovieDlg", u"&Notes:", None)
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate("AddEditMovieDlg", u"&Year:", None)
        )
        self.yearSpinBox.setSpecialValueText(
            QtWidgets.QApplication.translate("AddEditMovieDlg", u"Unknown", None)
        )
        self.label_3.setText(
            QtWidgets.QApplication.translate("AddEditMovieDlg", u"&Minutes:", None)
        )
        self.minutesSpinBox.setSpecialValueText(
            QtWidgets.QApplication.translate("AddEditMovieDlg", u"Unknown", None)
        )
        self.label_4.setText(
            QtWidgets.QApplication.translate("AddEditMovieDlg", u"A&cquired:", None)
        )
        self.acquiredDateEdit.setDisplayFormat(
            QtWidgets.QApplication.translate(
                "AddEditMovieDlg", u"ddd MMM d, yyyy", None
            )
        )
        self.label.setText(
            QtWidgets.QApplication.translate("AddEditMovieDlg", u"&Title:", None)
        )
        # retranslateUi
