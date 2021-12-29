import os
import platform
import sys

from PySide6 import QtWidgets, QtCore, QtGui

import helpform
import newimagedlg
import qrc_resources

__version__ = "1.0.0"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.image = QtGui.QImage()
        self.dirty = False
        self.filename = None
        self.mirroredvertically = False
        self.mirroredhorizontally = False

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.setCentralWidget(self.imageLabel)

        logDockWidget = QtWidgets.QDockWidget("Log", self)
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        )
        self.listWidget = QtWidgets.QListWidget()
        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, logDockWidget)

        self.printer = None

        self.sizeLabel = QtWidgets.QLabel()
        self.sizeLabel.setFrameStyle(
            QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken
        )
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)
