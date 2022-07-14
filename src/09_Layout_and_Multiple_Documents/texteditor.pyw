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
import textedit

CODEC = QtCore.QStringConverter.Utf8

# Since pyrcc is no longer provided with PyQt or PySide, we
# need to change resources location using the information from this thread :
# https://stackoverflow.com/questions/66099225/how-can-resources-be-provided-in-pyqt6-which-has-no-pyrcc
# That said PySide6 does still provide an alternative : https://doc.qt.io/qtforpython-6/tutorials/basictutorial/qrcfiles.html
# import qrc_resources  # this means this needs to go, and we need to adjust all the resources calls
QtCore.QDir.addSearchPath("resources", "images/")

__version__ = "1.0.0"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.mdi = QtWidgets.QMdiArea()
        self.setCentralWidget(self.mdi)

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
            "&Save",
            self.fileSave,
            QtGui.QKeySequence.Save,
            "filesave",
            "Save the text",
        )
        fileSaveAsAction = self.createAction(
            "Save &As...",
            self.fileSaveAs,
            icon="filesaveas",
            tip="Save the text using a new filename",
        )
        fileSaveAllAction = self.createAction(
            "Save A&ll", self.fileSaveAll, "filesave", tip="Save all the files"
        )
        fileQuitAction = self.createAction(
            "&Quit", self.close, "Ctrl+Q", "filequit", "Close the application"
        )
        editCopyAction = self.createAction(
            "&Copy",
            self.editCopy,
            QtGui.QKeySequence.Copy,
            "editcopy",
            "Copy text to the clipboard",
        )
        editCutAction = self.createAction(
            "Cu&t",
            self.editCut,
            QtGui.QKeySequence.Cut,
            "editcut",
            "Cut text to the clipboard",
        )
        editPasteAction = self.createAction(
            "&Paste",
            self.editPaste,
            QtGui.QKeySequence.Paste,
            "editpaste",
            "Paste in the clipboard's text",
        )
        self.windowNextAction = self.createAction(
            "&Next", self.mdi.activateNextSubWindow, QtGui.QKeySequence.NextChild
        )
        self.windowPrevAction = self.createAction(
            "&Previous",
            self.mdi.activatePreviousSubWindow,
            QtGui.QKeySequence.PreviousChild,
        )
        self.windowCascadeAction = self.createAction(
            "Casca&de", self.mdi.cascadeSubWindows
        )
        self.windowTileAction = self.createAction("&Tile", self.mdi.tileSubWindows)
        self.windowRestoreAction = self.createAction(
            "&Restore All", self.windowRestoreAll
        )
        self.windowMinimizeAction = self.createAction(
            "&Iconize All", self.windowMinimizeAll
        )
        # self.windowArrangeIconsAction = self.createAction(  # it looks like this is not
        #     "&Arrange Icons", self.mdi.arrangeIcons         # available in the QMdiSubWindow class
        # )
        self.windowCloseAction = self.createAction(
            "&Close", self.mdi.closeActiveSubWindow, QtGui.QKeySequence.Close
        )

        self.windowMapper = QtCore.QSignalMapper(self)
        self.connect(
            self.windowMapper,
            QtCore.SIGNAL("mapped(QWidget*)"),
            self.mdi,
            QtCore.SLOT("setActiveWindow(QWidget*)"),
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
                fileQuitAction,
            ),
        )
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActionsToTarget(
            editMenu, (editCopyAction, editCutAction, editPasteAction)
        )
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.connect(
            self.windowMenu, QtCore.SIGNAL("aboutToShow()"), self.updateWindowMenu
        )

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActionsToTarget(
            fileToolbar, (fileNewAction, fileOpenAction, fileSaveAction)
        )
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        self.addActionsToTarget(
            editToolbar, (editCopyAction, editCutAction, editPasteAction)
        )

        settings = QtCore.QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry", QtCore.QByteArray()))
        self.restoreState(settings.value("MainWindow/State", QtCore.QByteArray()))

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        self.updateWindowMenu()
        self.setWindowTitle("Text Editor")
        QtCore.QTimer.singleShot(0, self.loadFiles)

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
        failures = []
        for subWindow in self.mdi.subWindowList():
            textEdit = subWindow.widget()
            if textEdit.isModified():
                try:
                    textEdit.save()
                except IOError as e:
                    failures.append(e)
        if (
            failures
            and QtWidgets.QMessageBox.warning(
                self,
                "Text Editor -- Save Error",
                "Failed to save{}\nQuit anyway?".format("\n\t".join(failures)),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.No
        ):
            event.ignore()
            return
        settings = QtCore.QSettings()
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())
        files = []
        for subWindow in self.mdi.subWindowList():
            textEdit = subWindow.widget()
            if not textEdit.filename.startswith("Unnamed"):
                files.append(textEdit.filename)
        settings.setValue("CurrentFiles", files)
        self.mdi.closeAllSubWindows()

    def loadFiles(self):
        if len(sys.argv) > 1:
            for filename in sys.argv[1:31]:  # Load at most 30 files
                if QtCore.QFileInfo(filename).isFile():
                    self.loadFile(filename)
                    QtWidgets.QApplication.processEvents()
        else:
            settings = QtCore.QSettings()
            files = settings.value("CurrentFiles") or []
            for filename in files:
                if QtCore.QFile.exists(filename):
                    self.loadFile(filename)
                    QtWidgets.QApplication.processEvents()

    def fileNew(self):
        textEdit = textedit.TextEdit()
        self.mdi.addSubWindow(textEdit)
        textEdit.show()

    def fileOpen(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(
            self, "Text Editor -- Open File"
        )
        if filename:
            for subWindow in self.mdi.subWindowList():
                textEdit = subWindow.widget()
                if textEdit.filename == filename:
                    self.mdi.setActiveSubWindow(textEdit)
                    break
            else:
                self.loadFile(filename)

    def loadFile(self, filename):
        textEdit = textedit.TextEdit(filename)
        try:
            textEdit.load()
        except EnvironmentError as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Text Editor -- Load Error",
                "Failed to load {}: {}".format(filename, e),
            )
            textEdit.close()
            del textEdit
        else:
            self.mdi.addSubWindow(textEdit)
            textEdit.show()

    def fileSave(self):
        textEdit = self.mdi.activeSubWindow()
        if textEdit is None or not isinstance(textEdit, QtWidgets.QTextEdit):
            return True
        try:
            textEdit.save()
            return True
        except EnvironmentError as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Text Editor -- Save Error",
                "Failed to save {}: {}".format(textEdit.filename, e),
            )
            return False

    def fileSaveAs(self):
        textEdit = self.mdi.activeSubWindow()
        if textEdit is None or not isinstance(textEdit, QtWidgets.QTextEdit):
            return
        filename, filter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Text Editor -- Save File As",
            textEdit.filename,
            "Text files (*.txt *.*)",
        )
        if filename:
            textEdit.filename = filename
            return self.fileSave()
        return True

    def fileSaveAll(self):
        errors = []
        for subWindow in self.mdi.subWindowList():
            textEdit = subWindow.widget()
            if textEdit.isModified():
                try:
                    textEdit.save()
                except EnvironmentError as e:
                    errors.append("{}: {}".format(textEdit.filename, e))
        if errors:
            QtWidgets.QMessageBox.warning(
                self,
                "Text Editor -- Save All Error",
                "Failed to save\n{}".format("\n".join(errors)),
            )

    def editCopy(self):
        textEdit = self.mdi.activeSubWindow()
        if textEdit is None or not isinstance(textEdit, QtWidgets.QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if text:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(text)

    def editCut(self):
        textEdit = self.mdi.activeSubWindow()
        if textEdit is None or not isinstance(textEdit, QtWidgets.QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if text:
            cursor.removeSelectedText()
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(text)

    def editPaste(self):
        textEdit = self.mdi.activeSubWindow()
        if textEdit is None or not isinstance(textEdit, QtWidgets.QTextEdit):
            return
        clipboard = QtWidgets.QApplication.clipboard()
        textEdit.insertPlainText(clipboard.text())

    def windowRestoreAll(self):
        for textEdit in self.mdi.subWindowList():
            textEdit.showNormal()

    def windowMinimizeAll(self):
        for textEdit in self.mdi.subWindowList():
            textEdit.showMinimized()

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.addActionsToTarget(
            self.windowMenu,
            (
                self.windowNextAction,
                self.windowPrevAction,
                self.windowCascadeAction,
                self.windowTileAction,
                self.windowRestoreAction,
                self.windowMinimizeAction,
                # self.windowArrangeIconsAction,
                None,
                self.windowCloseAction,
            ),
        )
        textEdits = self.mdi.subWindowList()
        if not textEdits:
            return
        self.windowMenu.addSeparator()
        i = 1
        menu = self.windowMenu
        for textEdit in textEdits:
            title = textEdit.windowTitle()
            if i == 10:
                self.windowMenu.addSeparator()
                menu = menu.addMenu("&More")
            accel = ""
            if i < 10:
                accel = "&{} ".format(i)
            elif i < 36:
                accel = "&{} ".format(chr(i + ord("@") - 9))
            action = menu.addAction("{}{}".format(accel, title))
            self.connect(
                action,
                QtCore.SIGNAL("triggered()"),
                self.windowMapper,
                QtCore.SLOT("map()"),
            )
            self.windowMapper.setMapping(action, textEdit)
            i += 1


app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon("resources:icon.png"))
app.setOrganizationName("Qtrac Ltd.")
app.setOrganizationDomain("qtrac.eu")
app.setApplicationName("Text Editor")
form = MainWindow()
form.show()
app.exec()
