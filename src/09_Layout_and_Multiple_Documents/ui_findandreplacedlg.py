# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'findandreplacedlg.ui'
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
    QApplication,
    QCheckBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_FindAndReplaceDlg(object):
    def setupUi(self, FindAndReplaceDlg):
        if not FindAndReplaceDlg.objectName():
            FindAndReplaceDlg.setObjectName(u"FindAndReplaceDlg")
        FindAndReplaceDlg.resize(355, 274)
        self.hboxLayout = QHBoxLayout(FindAndReplaceDlg)
        # ifndef Q_OS_MAC
        self.hboxLayout.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.hboxLayout.setContentsMargins(9, 9, 9, 9)
        # endif
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.vboxLayout = QVBoxLayout()
        # ifndef Q_OS_MAC
        self.vboxLayout.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)
        # endif
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.gridLayout = QGridLayout()
        # ifndef Q_OS_MAC
        self.gridLayout.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        # endif
        self.gridLayout.setObjectName(u"gridLayout")
        self.replaceLineEdit = QLineEdit(FindAndReplaceDlg)
        self.replaceLineEdit.setObjectName(u"replaceLineEdit")

        self.gridLayout.addWidget(self.replaceLineEdit, 1, 1, 1, 1)

        self.findLineEdit = QLineEdit(FindAndReplaceDlg)
        self.findLineEdit.setObjectName(u"findLineEdit")

        self.gridLayout.addWidget(self.findLineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(FindAndReplaceDlg)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(FindAndReplaceDlg)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.vboxLayout.addLayout(self.gridLayout)

        self.vboxLayout1 = QVBoxLayout()
        # ifndef Q_OS_MAC
        self.vboxLayout1.setSpacing(6)
        # endif
        self.vboxLayout1.setContentsMargins(0, 0, 0, 0)
        self.vboxLayout1.setObjectName(u"vboxLayout1")
        self.caseCheckBox = QCheckBox(FindAndReplaceDlg)
        self.caseCheckBox.setObjectName(u"caseCheckBox")

        self.vboxLayout1.addWidget(self.caseCheckBox)

        self.wholeCheckBox = QCheckBox(FindAndReplaceDlg)
        self.wholeCheckBox.setObjectName(u"wholeCheckBox")
        self.wholeCheckBox.setChecked(True)

        self.vboxLayout1.addWidget(self.wholeCheckBox)

        self.vboxLayout.addLayout(self.vboxLayout1)

        self.spacerItem = QSpacerItem(
            231, 16, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.vboxLayout.addItem(self.spacerItem)

        self.moreFrame = QFrame(FindAndReplaceDlg)
        self.moreFrame.setObjectName(u"moreFrame")
        self.moreFrame.setFrameShape(QFrame.StyledPanel)
        self.moreFrame.setFrameShadow(QFrame.Raised)
        self.vboxLayout2 = QVBoxLayout(self.moreFrame)
        # ifndef Q_OS_MAC
        self.vboxLayout2.setSpacing(6)
        # endif
        # ifndef Q_OS_MAC
        self.vboxLayout2.setContentsMargins(9, 9, 9, 9)
        # endif
        self.vboxLayout2.setObjectName(u"vboxLayout2")
        self.backwardsCheckBox = QCheckBox(self.moreFrame)
        self.backwardsCheckBox.setObjectName(u"backwardsCheckBox")

        self.vboxLayout2.addWidget(self.backwardsCheckBox)

        self.regexCheckBox = QCheckBox(self.moreFrame)
        self.regexCheckBox.setObjectName(u"regexCheckBox")

        self.vboxLayout2.addWidget(self.regexCheckBox)

        self.ignoreNotesCheckBox = QCheckBox(self.moreFrame)
        self.ignoreNotesCheckBox.setObjectName(u"ignoreNotesCheckBox")

        self.vboxLayout2.addWidget(self.ignoreNotesCheckBox)

        self.vboxLayout.addWidget(self.moreFrame)

        self.hboxLayout.addLayout(self.vboxLayout)

        self.line = QFrame(FindAndReplaceDlg)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.hboxLayout.addWidget(self.line)

        self.vboxLayout3 = QVBoxLayout()
        # ifndef Q_OS_MAC
        self.vboxLayout3.setSpacing(6)
        # endif
        self.vboxLayout3.setContentsMargins(0, 0, 0, 0)
        self.vboxLayout3.setObjectName(u"vboxLayout3")
        self.findButton = QPushButton(FindAndReplaceDlg)
        self.findButton.setObjectName(u"findButton")
        self.findButton.setFocusPolicy(Qt.NoFocus)

        self.vboxLayout3.addWidget(self.findButton)

        self.replaceButton = QPushButton(FindAndReplaceDlg)
        self.replaceButton.setObjectName(u"replaceButton")
        self.replaceButton.setFocusPolicy(Qt.NoFocus)

        self.vboxLayout3.addWidget(self.replaceButton)

        self.closeButton = QPushButton(FindAndReplaceDlg)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setFocusPolicy(Qt.NoFocus)

        self.vboxLayout3.addWidget(self.closeButton)

        self.moreButton = QPushButton(FindAndReplaceDlg)
        self.moreButton.setObjectName(u"moreButton")
        self.moreButton.setFocusPolicy(Qt.NoFocus)
        self.moreButton.setCheckable(True)

        self.vboxLayout3.addWidget(self.moreButton)

        self.spacerItem1 = QSpacerItem(
            21, 16, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.vboxLayout3.addItem(self.spacerItem1)

        self.hboxLayout.addLayout(self.vboxLayout3)

        # if QT_CONFIG(shortcut)
        self.label_2.setBuddy(self.replaceLineEdit)
        self.label.setBuddy(self.findLineEdit)
        # endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.findLineEdit, self.replaceLineEdit)
        QWidget.setTabOrder(self.replaceLineEdit, self.caseCheckBox)
        QWidget.setTabOrder(self.caseCheckBox, self.wholeCheckBox)
        QWidget.setTabOrder(self.wholeCheckBox, self.backwardsCheckBox)
        QWidget.setTabOrder(self.backwardsCheckBox, self.regexCheckBox)
        QWidget.setTabOrder(self.regexCheckBox, self.ignoreNotesCheckBox)

        self.retranslateUi(FindAndReplaceDlg)
        self.closeButton.clicked.connect(FindAndReplaceDlg.reject)
        self.moreButton.toggled.connect(self.moreFrame.setVisible)

        QMetaObject.connectSlotsByName(FindAndReplaceDlg)

    # setupUi

    def retranslateUi(self, FindAndReplaceDlg):
        FindAndReplaceDlg.setWindowTitle(
            QCoreApplication.translate("FindAndReplaceDlg", u"Find and Replace", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("FindAndReplaceDlg", u"Replace w&ith:", None)
        )
        self.label.setText(
            QCoreApplication.translate("FindAndReplaceDlg", u"Find &what:", None)
        )
        self.caseCheckBox.setText(
            QCoreApplication.translate("FindAndReplaceDlg", u"&Case sensitive", None)
        )
        self.wholeCheckBox.setText(
            QCoreApplication.translate("FindAndReplaceDlg", u"Wh&ole words", None)
        )
        self.backwardsCheckBox.setText(
            QCoreApplication.translate("FindAndReplaceDlg", u"Search &Backwards", None)
        )
        self.regexCheckBox.setText(
            QCoreApplication.translate(
                "FindAndReplaceDlg", u"Regular E&xpression", None
            )
        )
        self.ignoreNotesCheckBox.setText(
            QCoreApplication.translate(
                "FindAndReplaceDlg", u"Ignore foot&notes and endnotes", None
            )
        )
        self.findButton.setText(
            QCoreApplication.translate("FindAndReplaceDlg", u"&Find", None)
        )
        self.replaceButton.setText(
            QCoreApplication.translate("FindAndReplaceDlg", u"&Replace", None)
        )
        self.closeButton.setText(
            QCoreApplication.translate("FindAndReplaceDlg", u"Close", None)
        )
        self.moreButton.setText(
            QCoreApplication.translate("FindAndReplaceDlg", u"&More", None)
        )

    # retranslateUi
