# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'paymentdlg.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QCheckBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTabWidget,
    QWidget,
)


class Ui_PaymentDlg(object):
    def setupUi(self, PaymentDlg):
        if not PaymentDlg.objectName():
            PaymentDlg.setObjectName(u"PaymentDlg")
        PaymentDlg.resize(399, 276)
        self.gridLayout = QGridLayout(PaymentDlg)
        # ifndef Q_OS_MAC
        self.gridLayout.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        # endif
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(PaymentDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.NoButton | QDialogButtonBox.Ok
        )

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.spacerItem = QSpacerItem(
            381, 16, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout.addItem(self.spacerItem, 2, 0, 1, 1)

        self.tabWidget = QTabWidget(PaymentDlg)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.hboxLayout = QHBoxLayout(self.tab)
        # ifndef Q_OS_MAC
        self.hboxLayout.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.hboxLayout.setContentsMargins(9, 9, 9, 9)
        # endif
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.paidCheckBox = QCheckBox(self.tab)
        self.paidCheckBox.setObjectName(u"paidCheckBox")

        self.hboxLayout.addWidget(self.paidCheckBox)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout1 = QGridLayout(self.tab_2)
        # ifndef Q_OS_MAC
        self.gridLayout1.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.gridLayout1.setContentsMargins(9, 9, 9, 9)
        # endif
        self.gridLayout1.setObjectName(u"gridLayout1")
        self.sortCodeLineEdit = QLineEdit(self.tab_2)
        self.sortCodeLineEdit.setObjectName(u"sortCodeLineEdit")

        self.gridLayout1.addWidget(self.sortCodeLineEdit, 1, 3, 1, 1)

        self.label_8 = QLabel(self.tab_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout1.addWidget(self.label_8, 1, 2, 1, 1)

        self.bankLineEdit = QLineEdit(self.tab_2)
        self.bankLineEdit.setObjectName(u"bankLineEdit")

        self.gridLayout1.addWidget(self.bankLineEdit, 0, 3, 1, 1)

        self.label_7 = QLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout1.addWidget(self.label_7, 0, 2, 1, 1)

        self.accountNumLineEdit = QLineEdit(self.tab_2)
        self.accountNumLineEdit.setObjectName(u"accountNumLineEdit")

        self.gridLayout1.addWidget(self.accountNumLineEdit, 1, 1, 1, 1)

        self.label_6 = QLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout1.addWidget(self.label_6, 1, 0, 1, 1)

        self.checkNumLineEdit = QLineEdit(self.tab_2)
        self.checkNumLineEdit.setObjectName(u"checkNumLineEdit")

        self.gridLayout1.addWidget(self.checkNumLineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout1.addWidget(self.label_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout2 = QGridLayout(self.tab_3)
        # ifndef Q_OS_MAC
        self.gridLayout2.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.gridLayout2.setContentsMargins(9, 9, 9, 9)
        # endif
        self.gridLayout2.setObjectName(u"gridLayout2")
        self.creditCardLineEdit = QLineEdit(self.tab_3)
        self.creditCardLineEdit.setObjectName(u"creditCardLineEdit")

        self.gridLayout2.addWidget(self.creditCardLineEdit, 0, 1, 1, 3)

        self.label_11 = QLabel(self.tab_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout2.addWidget(self.label_11, 0, 0, 1, 1)

        self.expiryDateEdit = QDateEdit(self.tab_3)
        self.expiryDateEdit.setObjectName(u"expiryDateEdit")
        self.expiryDateEdit.setAlignment(Qt.AlignRight)

        self.gridLayout2.addWidget(self.expiryDateEdit, 1, 3, 1, 1)

        self.label_10 = QLabel(self.tab_3)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout2.addWidget(self.label_10, 1, 2, 1, 1)

        self.validFromDateEdit = QDateEdit(self.tab_3)
        self.validFromDateEdit.setObjectName(u"validFromDateEdit")
        self.validFromDateEdit.setAlignment(Qt.AlignRight)

        self.gridLayout2.addWidget(self.validFromDateEdit, 1, 1, 1, 1)

        self.label_9 = QLabel(self.tab_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout2.addWidget(self.label_9, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.gridLayout3 = QGridLayout()
        # ifndef Q_OS_MAC
        self.gridLayout3.setSpacing(6)
        # endif
        self.gridLayout3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout3.setObjectName(u"gridLayout3")
        self.label_3 = QLabel(PaymentDlg)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout3.addWidget(self.label_3, 0, 2, 1, 1)

        self.amountSpinBox = QDoubleSpinBox(PaymentDlg)
        self.amountSpinBox.setObjectName(u"amountSpinBox")
        self.amountSpinBox.setAlignment(Qt.AlignRight)
        self.amountSpinBox.setMaximum(999999.000000000000000)

        self.gridLayout3.addWidget(self.amountSpinBox, 1, 3, 1, 1)

        self.label = QLabel(PaymentDlg)
        self.label.setObjectName(u"label")

        self.gridLayout3.addWidget(self.label, 0, 0, 1, 1)

        self.label_5 = QLabel(PaymentDlg)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout3.addWidget(self.label_5, 1, 0, 1, 1)

        self.surnameLineEdit = QLineEdit(PaymentDlg)
        self.surnameLineEdit.setObjectName(u"surnameLineEdit")

        self.gridLayout3.addWidget(self.surnameLineEdit, 0, 3, 1, 1)

        self.forenameLineEdit = QLineEdit(PaymentDlg)
        self.forenameLineEdit.setObjectName(u"forenameLineEdit")

        self.gridLayout3.addWidget(self.forenameLineEdit, 0, 1, 1, 1)

        self.label_4 = QLabel(PaymentDlg)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout3.addWidget(self.label_4, 1, 2, 1, 1)

        self.invoiceNumSpinBox = QSpinBox(PaymentDlg)
        self.invoiceNumSpinBox.setObjectName(u"invoiceNumSpinBox")
        self.invoiceNumSpinBox.setAlignment(Qt.AlignRight)
        self.invoiceNumSpinBox.setMaximum(999999999)
        self.invoiceNumSpinBox.setMinimum(1000000)
        self.invoiceNumSpinBox.setValue(1000000)

        self.gridLayout3.addWidget(self.invoiceNumSpinBox, 1, 1, 1, 1)

        self.gridLayout.addLayout(self.gridLayout3, 0, 0, 1, 1)

        # if QT_CONFIG(shortcut)
        self.label_8.setBuddy(self.sortCodeLineEdit)
        self.label_7.setBuddy(self.bankLineEdit)
        self.label_6.setBuddy(self.accountNumLineEdit)
        self.label_2.setBuddy(self.checkNumLineEdit)
        self.label_11.setBuddy(self.creditCardLineEdit)
        self.label_10.setBuddy(self.expiryDateEdit)
        self.label_9.setBuddy(self.validFromDateEdit)
        self.label_3.setBuddy(self.surnameLineEdit)
        self.label.setBuddy(self.forenameLineEdit)
        self.label_5.setBuddy(self.invoiceNumSpinBox)
        self.label_4.setBuddy(self.amountSpinBox)
        # endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.forenameLineEdit, self.surnameLineEdit)
        QWidget.setTabOrder(self.surnameLineEdit, self.invoiceNumSpinBox)
        QWidget.setTabOrder(self.invoiceNumSpinBox, self.amountSpinBox)
        QWidget.setTabOrder(self.amountSpinBox, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.paidCheckBox)
        QWidget.setTabOrder(self.paidCheckBox, self.checkNumLineEdit)
        QWidget.setTabOrder(self.checkNumLineEdit, self.accountNumLineEdit)
        QWidget.setTabOrder(self.accountNumLineEdit, self.bankLineEdit)
        QWidget.setTabOrder(self.bankLineEdit, self.sortCodeLineEdit)
        QWidget.setTabOrder(self.sortCodeLineEdit, self.creditCardLineEdit)
        QWidget.setTabOrder(self.creditCardLineEdit, self.validFromDateEdit)
        QWidget.setTabOrder(self.validFromDateEdit, self.expiryDateEdit)

        self.retranslateUi(PaymentDlg)
        self.buttonBox.accepted.connect(PaymentDlg.accept)
        self.buttonBox.rejected.connect(PaymentDlg.reject)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(PaymentDlg)

    # setupUi

    def retranslateUi(self, PaymentDlg):
        PaymentDlg.setWindowTitle(
            QCoreApplication.translate("PaymentDlg", u"Payment Form", None)
        )
        self.paidCheckBox.setText(
            QCoreApplication.translate("PaymentDlg", u"&Paid", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            QCoreApplication.translate("PaymentDlg", u"Cas&h", None),
        )
        self.label_8.setText(
            QCoreApplication.translate("PaymentDlg", u"S&ort Code:", None)
        )
        self.label_7.setText(QCoreApplication.translate("PaymentDlg", u"&Bank:", None))
        self.label_6.setText(
            QCoreApplication.translate("PaymentDlg", u"A&ccount No.:", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("PaymentDlg", u"Check &No.:", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            QCoreApplication.translate("PaymentDlg", u"Chec&k", None),
        )
        self.label_11.setText(
            QCoreApplication.translate("PaymentDlg", u"&Number:", None)
        )
        self.expiryDateEdit.setDisplayFormat(
            QCoreApplication.translate("PaymentDlg", u"MMM yyyy", None)
        )
        self.label_10.setText(
            QCoreApplication.translate("PaymentDlg", u"E&xpiry Date", None)
        )
        self.validFromDateEdit.setDisplayFormat(
            QCoreApplication.translate("PaymentDlg", u"MMM yyyy", None)
        )
        self.label_9.setText(
            QCoreApplication.translate("PaymentDlg", u"&Valid From:", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_3),
            QCoreApplication.translate("PaymentDlg", u"Credit Car&d", None),
        )
        self.label_3.setText(
            QCoreApplication.translate("PaymentDlg", u"&Surname:", None)
        )
        self.amountSpinBox.setPrefix(
            QCoreApplication.translate("PaymentDlg", u"$ ", None)
        )
        self.label.setText(
            QCoreApplication.translate("PaymentDlg", u"&Forename:", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("PaymentDlg", u"&Invoice No.:", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("PaymentDlg", u"&Amount:", None)
        )

    # retranslateUi
