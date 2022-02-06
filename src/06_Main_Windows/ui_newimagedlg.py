# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newimagedlg.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox)


class Ui_NewImageDlg(object):
    def setupUi(self, NewImageDlg):
        if not NewImageDlg.objectName():
            NewImageDlg.setObjectName(u"NewImageDlg")
        NewImageDlg.resize(287, 214)
        self.gridLayout = QGridLayout(NewImageDlg)
#ifndef Q_OS_MAC
        self.gridLayout.setSpacing(6)
#endif
#ifndef Q_OS_MAC
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
#endif
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(NewImageDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.NoButton|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 2)

        self.spacerItem = QSpacerItem(269, 16, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.spacerItem, 4, 0, 1, 3)

        self.colorLabel = QLabel(NewImageDlg)
        self.colorLabel.setObjectName(u"colorLabel")
        self.colorLabel.setFrameShape(QFrame.StyledPanel)
        self.colorLabel.setFrameShadow(QFrame.Raised)
        self.colorLabel.setScaledContents(True)

        self.gridLayout.addWidget(self.colorLabel, 3, 1, 1, 1)

        self.label_3 = QLabel(NewImageDlg)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.colorButton = QPushButton(NewImageDlg)
        self.colorButton.setObjectName(u"colorButton")

        self.gridLayout.addWidget(self.colorButton, 3, 2, 1, 1)

        self.brushComboBox = QComboBox(NewImageDlg)
        self.brushComboBox.setObjectName(u"brushComboBox")

        self.gridLayout.addWidget(self.brushComboBox, 2, 1, 1, 2)

        self.label_4 = QLabel(NewImageDlg)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label = QLabel(NewImageDlg)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(NewImageDlg)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.heightSpinBox = QSpinBox(NewImageDlg)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        self.heightSpinBox.setAlignment(Qt.AlignRight)
        self.heightSpinBox.setMaximum(512)
        self.heightSpinBox.setMinimum(8)
        self.heightSpinBox.setSingleStep(4)
        self.heightSpinBox.setValue(64)

        self.gridLayout.addWidget(self.heightSpinBox, 1, 1, 1, 1)

        self.widthSpinBox = QSpinBox(NewImageDlg)
        self.widthSpinBox.setObjectName(u"widthSpinBox")
        self.widthSpinBox.setAlignment(Qt.AlignRight)
        self.widthSpinBox.setMaximum(512)
        self.widthSpinBox.setMinimum(8)
        self.widthSpinBox.setSingleStep(4)
        self.widthSpinBox.setValue(64)

        self.gridLayout.addWidget(self.widthSpinBox, 0, 1, 1, 1)

#if QT_CONFIG(shortcut)
        self.label_4.setBuddy(self.brushComboBox)
        self.label.setBuddy(self.widthSpinBox)
        self.label_2.setBuddy(self.heightSpinBox)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.widthSpinBox, self.heightSpinBox)
        QWidget.setTabOrder(self.heightSpinBox, self.brushComboBox)
        QWidget.setTabOrder(self.brushComboBox, self.colorButton)
        QWidget.setTabOrder(self.colorButton, self.buttonBox)

        self.retranslateUi(NewImageDlg)
        self.buttonBox.accepted.connect(NewImageDlg.accept)
        self.buttonBox.rejected.connect(NewImageDlg.reject)

        QMetaObject.connectSlotsByName(NewImageDlg)
    # setupUi

    def retranslateUi(self, NewImageDlg):
        NewImageDlg.setWindowTitle(QCoreApplication.translate("NewImageDlg", u"Image Chooser - New Image", None))
        self.colorLabel.setText("")
        self.label_3.setText(QCoreApplication.translate("NewImageDlg", u"Color", None))
        self.colorButton.setText(QCoreApplication.translate("NewImageDlg", u"&Color...", None))
        self.label_4.setText(QCoreApplication.translate("NewImageDlg", u"&Brush pattern:", None))
        self.label.setText(QCoreApplication.translate("NewImageDlg", u"&Width:", None))
        self.label_2.setText(QCoreApplication.translate("NewImageDlg", u"&Height:", None))
        self.heightSpinBox.setSuffix(QCoreApplication.translate("NewImageDlg", u" px", None))
        self.widthSpinBox.setSuffix(QCoreApplication.translate("NewImageDlg", u" px", None))
    # retranslateUi
