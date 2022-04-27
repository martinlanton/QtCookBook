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
from PySide6 import QtWidgets, QtCore, QtGui

CODEC = QtCore.QStringConverter.Utf8

#  Since pyrcc is no longer provided with PyQt or PySide, we
#  need to change resources location using the information from this thread :
#  https://stackoverflow.com/questions/66099225/how-can-resources-be-provided-in-pyqt6-which-has-no-pyrcc
# import qrc_resources  # this means this needs to go, and we need to adjust all the resources calls
QtCore.QDir.addSearchPath("resources", "images/")


__version__ = "1.0.0"


class MainWindow(QtWidgets.QMainWindow):

    NextId = 1
    Instances = set()

    def __init__(self, filename="", parent=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        MainWindow.Instances.add(self)

        self.editor = QtWidgets.QTextEdit()
        self.setCentralWidget(self.editor)

        fileNewAction = self.createAction(
            "&New",
            self.fileNew,
            QtGui.QKeySequence.New,
            "filenew",
            "Create a text file",
        )
        fileOpenAction = self.createAction(
            "&Open...",
            self.fileOpen,
            QtGui.QKeySequence.Open,
            "fileopen",
            "Open an existing text file",
        )
        fileSaveAction = self.createAction(
            "&Save", self.fileSave, QtGui.QKeySequence.Save, "filesave", "Save the text"
        )
        fileSaveAsAction = self.createAction(
            "Save &As...",
            self.fileSaveAs,
            icon="filesaveas",
            tip="Save the text using a new filename",
        )
        fileSaveAllAction = self.createAction(
            "Save A&ll", self.fileSaveAll, icon="filesave", tip="Save all the files"
        )
        fileCloseAction = self.createAction(
            "&Close",
            self.close,
            QtGui.QKeySequence.Close,
            "fileclose",
            "Close this text editor",
        )
        fileQuitAction = self.createAction(
            "&Quit", self.fileQuit, "Ctrl+Q", "filequit", "Close the application"
        )
        editCopyAction = self.createAction(
            "&Copy",
            self.editor.copy,
            QtGui.QKeySequence.Copy,
            "editcopy",
            "Copy text to the clipboard",
        )
        editCutAction = self.createAction(
            "Cu&t",
            self.editor.cut,
            QtGui.QKeySequence.Cut,
            "editcut",
            "Cut text to the clipboard",
        )
        editPasteAction = self.createAction(
            "&Paste",
            self.editor.paste,
            QtGui.QKeySequence.Paste,
            "editpaste",
            "Paste in the clipboard's text",
        )

        fileMenu = self.menuBar().addMenu("&File")
        self.addActionsToTarget(
            fileMenu,
            (
                fileNewAction,
                fileOpenAction,
                fileSaveAction,
                fileSaveAsAction,
                fileSaveAllAction,
                None,
                fileCloseAction,
                fileQuitAction,
            ),
        )
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActionsToTarget(editMenu, (editCopyAction, editCutAction, editPasteAction))

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.connect(
            self.windowMenu, QtCore.SIGNAL("aboutToShow()"), self.updateWindowMenu
        )

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActionsToTarget(fileToolbar, (fileNewAction, fileOpenAction, fileSaveAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        self.addActionsToTarget(editToolbar, (editCopyAction, editCutAction, editPasteAction))

        self.connect(
            self, QtCore.SIGNAL("destroyed(QObject*)"), MainWindow.updateInstances
        )

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        self.resize(500, 600)

        self.filename = filename
        if not self.filename:
            self.filename = "Unnamed-{}.txt".format(MainWindow.NextId)
            MainWindow.NextId += 1
            self.editor.document().setModified(False)
            self.setWindowTitle("SDI Text Editor - {}".format(self.filename))
        else:
            self.loadFile()

    @staticmethod
    def updateInstances(qobj):
        MainWindow.Instances = set(
            [window for window in MainWindow.Instances if isAlive(window)]
        )

    def createAction(
        self,
        text,
        slot=None,
        shortcut=None,
        icon=None,
        tip=None,
        checkable=False,
        signal="triggered()",
    ):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon("resources:{}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, QtCore.SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActionsToTarget(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def closeEvent(self, event):
        if (
            self.editor.document().isModified()
            and QtWidgets.QMessageBox.question(
                self,
                "SDI Text Editor - Unsaved Changes",
                "Save unsaved changes in {}?".format(self.filename),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.Yes
        ):
            self.fileSave()

    def fileQuit(self):
        QtWidgets.QApplication.closeAllWindows()

    def fileNew(self):
        MainWindow().show()

    def fileOpen(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(
            self, "SDI Text Editor -- Open File"
        )
        if filename:
            if not self.editor.document().isModified() and self.filename.startswith(
                "Unnamed"
            ):
                self.filename = filename
                self.loadFile()
            else:
                MainWindow(filename).show()

    def loadFile(self):
        fh = None
        try:
            fh = QtCore.QFile(self.filename)
            if not fh.open(QtCore.QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setEncoding(CODEC)
            self.editor.setPlainText(stream.readAll())
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QtWidgets.QMessageBox.warning(
                self,
                "SDI Text Editor -- Load Error",
                "Failed to load {}: {}".format(self.filename, e),
            )
        finally:
            if fh is not None:
                fh.close()
        self.editor.document().setModified(False)
        self.setWindowTitle(
            "SDI Text Editor - {}".format(QtCore.QFileInfo(self.filename).fileName())
        )

    def fileSave(self):
        if self.filename.startswith("Unnamed"):
            return self.fileSaveAs()
        fh = None
        try:
            fh = QtCore.QFile(self.filename)
            if not fh.open(QtCore.QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setEncoding(CODEC)
            stream << self.editor.toPlainText()
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QtWidgets.QMessageBox.warning(
                self,
                "SDI Text Editor -- Save Error",
                "Failed to save {}: {}".format(self.filename, e),
            )
            return False
        finally:
            if fh is not None:
                fh.close()
        return True

    def fileSaveAs(self):
        filename, filter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "SDI Text Editor -- Save File As",
            self.filename,
            "SDI Text files (*.txt *.*)",
        )
        if filename:
            self.filename = filename
            self.setWindowTitle(
                "SDI Text Editor - {}".format(
                    QtCore.QFileInfo(self.filename).fileName()
                )
            )
            return self.fileSave()
        return False

    def fileSaveAll(self):
        count = 0
        for window in MainWindow.Instances:
            if isAlive(window) and window.editor.document().isModified():
                if window.fileSave():
                    count += 1
        self.statusBar().showMessage(
            "Saved {} of {} files".format(count, len(MainWindow.Instances)), 5000
        )

    def updateWindowMenu(self):
        self.windowMenu.clear()
        for window in MainWindow.Instances:
            if isAlive(window):
                self.windowMenu.addAction(window.windowTitle(), self.raiseWindow)

    def raiseWindow(self):
        action = self.sender()
        if not isinstance(action, QtGui.QAction):
            return
        for window in MainWindow.Instances:
            if isAlive(window) and window.windowTitle() == action.text():
                window.activateWindow()
                window.raise_()
                break


def isAlive(qobj):
    import shiboken6

    try:
        shiboken6.getCppPointer(qobj)
    except RuntimeError:
        return False
    return True


app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon("resources:icon.png"))
MainWindow().show()
app.exec()
