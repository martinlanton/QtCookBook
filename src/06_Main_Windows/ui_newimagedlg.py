# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newimagedlg.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6 import QtWidgets, QtCore, QtGui


class Ui_NewImageDlg(object):
    def setupUi(self, NewImageDlg):
        if not NewImageDlg.objectName():
            NewImageDlg.setObjectName(u"NewImageDlg")
        NewImageDlg.resize(287, 214)
        self.gridLayout = QtWidgets.QGridLayout(NewImageDlg)
        # ifndef Q_OS_MAC
        self.gridLayout.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        # endif
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(NewImageDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel
            | QtWidgets.QDialogButtonBox.NoButton
            | QtWidgets.QDialogButtonBox.Ok
        )

        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 2)

        self.spacerItem = QtWidgets.QSpacerItem(
            269, 16, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )

        self.gridLayout.addItem(self.spacerItem, 4, 0, 1, 3)

        self.colorLabel = QtWidgets.QLabel(NewImageDlg)
        self.colorLabel.setObjectName(u"colorLabel")
        self.colorLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.colorLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.colorLabel.setScaledContents(True)

        self.gridLayout.addWidget(self.colorLabel, 3, 1, 1, 1)

        self.label_3 = QtWidgets.QLabel(NewImageDlg)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.colorButton = QtWidgets.QPushButton(NewImageDlg)
        self.colorButton.setObjectName(u"colorButton")

        self.gridLayout.addWidget(self.colorButton, 3, 2, 1, 1)

        self.brushComboBox = QtWidgets.QComboBox(NewImageDlg)
        self.brushComboBox.setObjectName(u"brushComboBox")

        self.gridLayout.addWidget(self.brushComboBox, 2, 1, 1, 2)

        self.label_4 = QtWidgets.QLabel(NewImageDlg)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label = QtWidgets.QLabel(NewImageDlg)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QtWidgets.QLabel(NewImageDlg)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.heightSpinBox = QtWidgets.QSpinBox(NewImageDlg)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        self.heightSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.heightSpinBox.setMaximum(512)
        self.heightSpinBox.setMinimum(8)
        self.heightSpinBox.setSingleStep(4)
        self.heightSpinBox.setValue(64)

        self.gridLayout.addWidget(self.heightSpinBox, 1, 1, 1, 1)

        self.widthSpinBox = QtWidgets.QSpinBox(NewImageDlg)
        self.widthSpinBox.setObjectName(u"widthSpinBox")
        self.widthSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.widthSpinBox.setMaximum(512)
        self.widthSpinBox.setMinimum(8)
        self.widthSpinBox.setSingleStep(4)
        self.widthSpinBox.setValue(64)

        self.gridLayout.addWidget(self.widthSpinBox, 0, 1, 1, 1)

        # if QT_CONFIG(shortcut)
        self.label_4.setBuddy(self.brushComboBox)
        self.label.setBuddy(self.widthSpinBox)
        self.label_2.setBuddy(self.heightSpinBox)
        # endif // QT_CONFIG(shortcut)
        QtWidgets.QWidget.setTabOrder(self.widthSpinBox, self.heightSpinBox)
        QtWidgets.QWidget.setTabOrder(self.heightSpinBox, self.brushComboBox)
        QtWidgets.QWidget.setTabOrder(self.brushComboBox, self.colorButton)
        QtWidgets.QWidget.setTabOrder(self.colorButton, self.buttonBox)

        self.retranslateUi(NewImageDlg)
        self.buttonBox.accepted.connect(NewImageDlg.accept)
        self.buttonBox.rejected.connect(NewImageDlg.reject)

        QtCore.QMetaObject.connectSlotsByName(NewImageDlg)

    # setupUi

    def retranslateUi(self, NewImageDlg):
        NewImageDlg.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "NewImageDlg", u"Image Chooser - New Image", None
            )
        )
        self.colorLabel.setText("")
        self.label_3.setText(QtCore.QCoreApplication.translate("NewImageDlg", u"Color", None))
        self.colorButton.setText(
            QtCore.QCoreApplication.translate("NewImageDlg", u"&Color...", None)
        )
        self.label_4.setText(
            QtCore.QCoreApplication.translate("NewImageDlg", u"&Brush pattern:", None)
        )
        self.label.setText(QtCore.QCoreApplication.translate("NewImageDlg", u"&Width:", None))
        self.label_2.setText(
            QtCore.QCoreApplication.translate("NewImageDlg", u"&Height:", None)
        )
        self.heightSpinBox.setSuffix(
            QtCore.QCoreApplication.translate("NewImageDlg", u" px", None)
        )
        self.widthSpinBox.setSuffix(
            QtCore.QCoreApplication.translate("NewImageDlg", u" px", None)
        )

    # retranslateUi
