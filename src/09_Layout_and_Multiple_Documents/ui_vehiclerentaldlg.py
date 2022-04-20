# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'vehiclerentaldlg.ui'
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
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QStackedWidget,
    QWidget,
)


class Ui_VehicleRentalDlg(object):
    def setupUi(self, VehicleRentalDlg):
        if not VehicleRentalDlg.objectName():
            VehicleRentalDlg.setObjectName(u"VehicleRentalDlg")
        VehicleRentalDlg.resize(206, 246)
        self.gridLayout = QGridLayout(VehicleRentalDlg)
        # ifndef Q_OS_MAC
        self.gridLayout.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        # endif
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(VehicleRentalDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)

        self.spacerItem = QSpacerItem(
            188, 16, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout.addItem(self.spacerItem, 3, 0, 1, 1)

        self.hboxLayout = QHBoxLayout()
        # ifndef Q_OS_MAC
        self.hboxLayout.setSpacing(6)
        # endif
        self.hboxLayout.setContentsMargins(0, 0, 0, 0)
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.label_6 = QLabel(VehicleRentalDlg)
        self.label_6.setObjectName(u"label_6")

        self.hboxLayout.addWidget(self.label_6)

        self.mileageLabel = QLabel(VehicleRentalDlg)
        self.mileageLabel.setObjectName(u"mileageLabel")
        self.mileageLabel.setFrameShape(QFrame.StyledPanel)
        self.mileageLabel.setFrameShadow(QFrame.Sunken)
        self.mileageLabel.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )

        self.hboxLayout.addWidget(self.mileageLabel)

        self.gridLayout.addLayout(self.hboxLayout, 2, 0, 1, 1)

        self.stackedWidget = QStackedWidget(VehicleRentalDlg)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout1 = QGridLayout(self.page_2)
        # ifndef Q_OS_MAC
        self.gridLayout1.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.gridLayout1.setContentsMargins(9, 9, 9, 9)
        # endif
        self.gridLayout1.setObjectName(u"gridLayout1")
        self.colorComboBox = QComboBox(self.page_2)
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.setObjectName(u"colorComboBox")

        self.gridLayout1.addWidget(self.colorComboBox, 0, 1, 1, 1)

        self.label_4 = QLabel(self.page_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout1.addWidget(self.label_4, 0, 0, 1, 1)

        self.label_5 = QLabel(self.page_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout1.addWidget(self.label_5, 1, 0, 1, 1)

        self.seatsSpinBox = QSpinBox(self.page_2)
        self.seatsSpinBox.setObjectName(u"seatsSpinBox")
        self.seatsSpinBox.setAlignment(Qt.AlignRight)
        self.seatsSpinBox.setMinimum(2)
        self.seatsSpinBox.setMaximum(12)
        self.seatsSpinBox.setValue(4)

        self.gridLayout1.addWidget(self.seatsSpinBox, 1, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_2)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout2 = QGridLayout(self.page)
        # ifndef Q_OS_MAC
        self.gridLayout2.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.gridLayout2.setContentsMargins(9, 9, 9, 9)
        # endif
        self.gridLayout2.setObjectName(u"gridLayout2")
        self.weightSpinBox = QSpinBox(self.page)
        self.weightSpinBox.setObjectName(u"weightSpinBox")
        self.weightSpinBox.setAlignment(Qt.AlignRight)
        self.weightSpinBox.setMinimum(1)
        self.weightSpinBox.setMaximum(8)

        self.gridLayout2.addWidget(self.weightSpinBox, 0, 1, 1, 1)

        self.label_3 = QLabel(self.page)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout2.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout2.addWidget(self.label_2, 0, 0, 1, 1)

        self.volumeSpinBox = QSpinBox(self.page)
        self.volumeSpinBox.setObjectName(u"volumeSpinBox")
        self.volumeSpinBox.setAlignment(Qt.AlignRight)
        self.volumeSpinBox.setMinimum(4)
        self.volumeSpinBox.setMaximum(22)
        self.volumeSpinBox.setValue(10)

        self.gridLayout2.addWidget(self.volumeSpinBox, 1, 1, 1, 1)

        self.stackedWidget.addWidget(self.page)

        self.gridLayout.addWidget(self.stackedWidget, 1, 0, 1, 1)

        self.hboxLayout1 = QHBoxLayout()
        # ifndef Q_OS_MAC
        self.hboxLayout1.setSpacing(6)
        # endif
        self.hboxLayout1.setContentsMargins(0, 0, 0, 0)
        self.hboxLayout1.setObjectName(u"hboxLayout1")
        self.label = QLabel(VehicleRentalDlg)
        self.label.setObjectName(u"label")

        self.hboxLayout1.addWidget(self.label)

        self.vehicleComboBox = QComboBox(VehicleRentalDlg)
        self.vehicleComboBox.addItem("")
        self.vehicleComboBox.addItem("")
        self.vehicleComboBox.setObjectName(u"vehicleComboBox")

        self.hboxLayout1.addWidget(self.vehicleComboBox)

        self.gridLayout.addLayout(self.hboxLayout1, 0, 0, 1, 1)

        # if QT_CONFIG(shortcut)
        self.label_4.setBuddy(self.colorComboBox)
        self.label_5.setBuddy(self.seatsSpinBox)
        self.label_3.setBuddy(self.volumeSpinBox)
        self.label_2.setBuddy(self.seatsSpinBox)
        self.label.setBuddy(self.vehicleComboBox)
        # endif // QT_CONFIG(shortcut)

        self.retranslateUi(VehicleRentalDlg)
        self.vehicleComboBox.currentIndexChanged.connect(
            self.stackedWidget.setCurrentIndex
        )
        self.buttonBox.accepted.connect(VehicleRentalDlg.accept)
        self.buttonBox.rejected.connect(VehicleRentalDlg.reject)

        self.stackedWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(VehicleRentalDlg)

    # setupUi

    def retranslateUi(self, VehicleRentalDlg):
        VehicleRentalDlg.setWindowTitle(
            QCoreApplication.translate("VehicleRentalDlg", u"Vehicle Rental", None)
        )
        self.label_6.setText(
            QCoreApplication.translate("VehicleRentalDlg", u"Max. Mileage:", None)
        )
        self.mileageLabel.setText(
            QCoreApplication.translate("VehicleRentalDlg", u"1000 miles", None)
        )
        self.colorComboBox.setItemText(
            0, QCoreApplication.translate("VehicleRentalDlg", u"Black", None)
        )
        self.colorComboBox.setItemText(
            1, QCoreApplication.translate("VehicleRentalDlg", u"Blue", None)
        )
        self.colorComboBox.setItemText(
            2, QCoreApplication.translate("VehicleRentalDlg", u"Green", None)
        )
        self.colorComboBox.setItemText(
            3, QCoreApplication.translate("VehicleRentalDlg", u"Red", None)
        )
        self.colorComboBox.setItemText(
            4, QCoreApplication.translate("VehicleRentalDlg", u"Silver", None)
        )
        self.colorComboBox.setItemText(
            5, QCoreApplication.translate("VehicleRentalDlg", u"White", None)
        )
        self.colorComboBox.setItemText(
            6, QCoreApplication.translate("VehicleRentalDlg", u"Yellow", None)
        )

        self.label_4.setText(
            QCoreApplication.translate("VehicleRentalDlg", u"Co&lor:", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("VehicleRentalDlg", u"&Seats:", None)
        )
        self.weightSpinBox.setSuffix(
            QCoreApplication.translate("VehicleRentalDlg", u" tons", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("VehicleRentalDlg", u"Volu&me:", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("VehicleRentalDlg", u"&Weight:", None)
        )
        self.volumeSpinBox.setSuffix(
            QCoreApplication.translate("VehicleRentalDlg", u" cu m", None)
        )
        self.label.setText(
            QCoreApplication.translate("VehicleRentalDlg", u"&Vehicle Type:", None)
        )
        self.vehicleComboBox.setItemText(
            0, QCoreApplication.translate("VehicleRentalDlg", u"Car", None)
        )
        self.vehicleComboBox.setItemText(
            1, QCoreApplication.translate("VehicleRentalDlg", u"Van", None)
        )

    # retranslateUi
