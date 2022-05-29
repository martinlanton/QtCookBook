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

import os
import sys
from PySide6 import QtWidgets, QtCore, QtGui

#  Since pyrcc is no longer provided with PyQt or PySide, we
#  need to change resources location using the information from this thread :
#  https://stackoverflow.com/questions/66099225/how-can-resources-be-provided-in-pyqt6-which-has-no-pyrcc
# import qrc_resources  # this means this needs to go, and we need to adjust all the resources calls
QtCore.QDir.addSearchPath("resources", "images/")

CODEC = QtCore.QStringConverter.Utf8


__version__ = "1.0.1"


class PythonHighlighter(QtGui.QSyntaxHighlighter):

    Rules = []

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.darkBlue)
        keywordFormat.setFontWeight(QtGui.QFont.Bold)
        for pattern in (
            r"\band\b",
            r"\bas\b",
            r"\bassert\b",
            r"\bbreak\b",
            r"\bclass\b",
            r"\bcontinue\b",
            r"\bdef\b",
            r"\bdel\b",
            r"\belif\b",
            r"\belse\b",
            r"\bexcept\b",
            r"\bexec\b",
            r"\bfinally\b",
            r"\bfor\b",
            r"\bfrom\b",
            r"\bglobal\b",
            r"\bif\b",
            r"\bimport\b",
            r"\bin\b",
            r"\bis\b",
            r"\blambda\b",
            r"\bnot\b",
            r"\bor\b",
            r"\bpass\b",
            r"\bprint\b",
            r"\braise\b",
            r"\breturn\b",
            r"\btry\b",
            r"\bwhile\b",
            r"\bwith\b",
            r"\byield\b",
        ):
            PythonHighlighter.Rules.append((QtCore.QRegularExpression(pattern), keywordFormat))
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor(0, 127, 0))
        comment_format.setFontItalic(True)
        PythonHighlighter.Rules.append((QtCore.QRegularExpression(r"#.*"), comment_format))
        self.stringFormat = QtGui.QTextCharFormat()
        self.stringFormat.setForeground(QtCore.Qt.darkYellow)
        string_re = QtCore.QRegularExpression(r"""(?:'[^']*?'|"[^"]*?")""")
        PythonHighlighter.Rules.append((string_re, self.stringFormat))
        self.stringRe = QtCore.QRegularExpression(r"""(:?"["]".*?"["]"|'''.*?''')""")
        PythonHighlighter.Rules.append((self.stringRe, self.stringFormat))
        self.tripleSingleRe = QtCore.QRegularExpression(r"""'''(?!")""")
        self.tripleDoubleRe = QtCore.QRegularExpression(r'''"""(?!')''')

    def highlightBlock(self, text):
        normal, triplesingle, tripledouble = range(3)

        for regex, formatting in PythonHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, formatting)
                i = regex.indexIn(text, i + length)

        self.setCurrentBlockState(normal)
        # TODO : fix the indexIn call
        if self.stringRe.indexIn(text) != -1:
            return
        for i, state in (
            (self.tripleSingleRe.indexIn(text), triplesingle),
            (self.tripleDoubleRe.indexIn(text), tripledouble),
        ):
            if self.previousBlockState() == state:
                if i == -1:
                    i = text.length()
                    self.setCurrentBlockState(state)
                self.setFormat(0, i + 3, self.stringFormat)
            elif i > -1:
                self.setCurrentBlockState(state)
                self.setFormat(i, text.length(), self.stringFormat)


class TextEdit(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText("    ")
            return True
        return QtWidgets.QTextEdit.event(self, event)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, filename=None, parent=None):
        super(MainWindow, self).__init__(parent)

        font = QtGui.QFont("Courier", 11)
        font.setFixedPitch(True)
        self.editor = TextEdit()
        self.editor.setFont(font)
        self.highlighter = PythonHighlighter(self.editor.document())
        self.setCentralWidget(self.editor)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        file_new_action = self.createAction(
            "&New...", self.fileNew, QtGui.QKeySequence.New, "filenew", "Create a Python file"
        )
        file_open_action = self.createAction(
            "&Open...",
            self.fileOpen,
            QtGui.QKeySequence.Open,
            "fileopen",
            "Open an existing Python file",
        )
        self.fileSaveAction = self.createAction(
            "&Save", self.fileSave, QtGui.QKeySequence.Save, "filesave", "Save the file"
        )
        self.fileSaveAsAction = self.createAction(
            "Save &As...",
            self.fileSaveAs,
            icon="filesaveas",
            tip="Save the file using a new name",
        )
        file_quit_action = self.createAction(
            "&Quit", self.close, "Ctrl+Q", "filequit", "Close the application"
        )
        self.editCopyAction = self.createAction(
            "&Copy",
            self.editor.copy,
            QtGui.QKeySequence.Copy,
            "editcopy",
            "Copy text to the clipboard",
        )
        self.editCutAction = self.createAction(
            "Cu&t",
            self.editor.cut,
            QtGui.QKeySequence.Cut,
            "editcut",
            "Cut text to the clipboard",
        )
        self.editPasteAction = self.createAction(
            "&Paste",
            self.editor.paste,
            QtGui.QKeySequence.Paste,
            "editpaste",
            "Paste in the clipboard's text",
        )

        file_menu = self.menuBar().addMenu("&File")
        self.addActions(
            file_menu,
            (
                file_new_action,
                file_open_action,
                self.fileSaveAction,
                self.fileSaveAsAction,
                None,
                file_quit_action,
            ),
        )
        edit_menu = self.menuBar().addMenu("&Edit")
        self.addActions(
            edit_menu, (self.editCopyAction, self.editCutAction, self.editPasteAction)
        )
        file_toolbar = self.addToolBar("File")
        file_toolbar.setObjectName("FileToolBar")
        self.addActions(
            file_toolbar, (file_new_action, file_open_action, self.fileSaveAction)
        )
        edit_toolbar = self.addToolBar("Edit")
        edit_toolbar.setObjectName("EditToolBar")
        self.addActions(
            edit_toolbar, (self.editCopyAction, self.editCutAction, self.editPasteAction)
        )

        self.connect(self.editor, QtCore.SIGNAL("selectionChanged()"), self.updateUi)
        self.connect(
            self.editor.document(), QtCore.SIGNAL("modificationChanged(bool)"), self.updateUi
        )
        self.connect(QtWidgets.QApplication.clipboard(), QtCore.SIGNAL("dataChanged()"), self.updateUi)

        self.resize(800, 600)
        self.setWindowTitle("Python Editor")
        self.filename = filename
        if self.filename is not None:
            self.loadFile()
        self.updateUi()

    def updateUi(self, arg=None):
        self.fileSaveAction.setEnabled(self.editor.document().isModified())
        self.fileSaveAsAction.setEnabled(not self.editor.document().isEmpty())
        enable = self.editor.textCursor().hasSelection()
        self.editCopyAction.setEnabled(enable)
        self.editCutAction.setEnabled(enable)
        self.editPasteAction.setEnabled(self.editor.canPaste())

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

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def closeEvent(self, event):
        if not self.okToContinue():
            event.ignore()

    def okToContinue(self):
        if self.editor.document().isModified():
            reply = QtWidgets.QMessageBox.question(
                self,
                "Python Editor - Unsaved Changes",
                "Save unsaved changes?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
            )
            if reply == QtWidgets.QMessageBox.Cancel:
                return False
            elif reply == QtWidgets.QMessageBox.Yes:
                return self.fileSave()
        return True

    def fileNew(self):
        if not self.okToContinue():
            return
        document = self.editor.document()
        document.clear()
        document.setModified(False)
        self.filename = None
        self.setWindowTitle("Python Editor - Unnamed")
        self.updateUi()

    def fileOpen(self):
        if not self.okToContinue():
            return
        dir_ = os.path.dirname(self.filename) if self.filename is not None else "."
        filename, filter_str = QtWidgets.QFileDialog.getOpenFileName(
            self, "Python Editor - Choose File", dir_, "Python files (*.py *.pyw)"
        )
        if filename:
            self.filename = filename
            self.loadFile()

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
            self.setWindowTitle(
                "Python Editor - {}".format(QtCore.QFileInfo(self.filename).fileName())
            )
        except EnvironmentError as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Python Editor -- Load Error",
                "Failed to load {}: {}".format(self.filename, e),
            )
        finally:
            if fh is not None:
                fh.close()

    def fileSave(self):
        if self.filename is None:
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
                "Python Editor -- Save Error",
                "Failed to save {}: {}".format(self.filename, e),
            )
            return False
        finally:
            if fh is not None:
                fh.close()
        return True

    def fileSaveAs(self):
        filename = self.filename if self.filename is not None else "."
        filename, filter_str = QtWidgets.QFileDialog.getSaveFileName(
            self, "Python Editor -- Save File As", filename, "Python files (*.py *.pyw)"
        )
        if filename:
            self.filename = filename
            self.setWindowTitle(
                "Python Editor - {}".format(QtCore.QFileInfo(self.filename).fileName())
            )
            return self.fileSave()
        return False


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("resources:icon.png"))
    fname = None
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    form = MainWindow(fname)
    form.show()
    app.exec()


main()
