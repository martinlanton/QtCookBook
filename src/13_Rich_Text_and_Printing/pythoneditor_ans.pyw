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

# Since pyrcc is no longer provided with PyQt or PySide, we
# need to change resources location using the information from this thread :
# https://stackoverflow.com/questions/66099225/how-can-resources-be-provided-in-pyqt6-which-has-no-pyrcc
# That said PySide6 does still provide an alternative : https://doc.qt.io/qtforpython-6/tutorials/basictutorial/qrcfiles.html
# import qrc_resources  # this means this needs to go, and we need to adjust all the resources calls
QtCore.QDir.addSearchPath("resources", "images/")

CODEC = QtCore.QStringConverter.Utf8


__version__ = "1.0.1"


class PythonHighlighter(QtGui.QSyntaxHighlighter):

    Rules = []

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtCore.Qt.darkBlue)
        keyword_format.setFontWeight(QtGui.QFont.Bold)
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
            PythonHighlighter.Rules.append(
                (QtCore.QRegularExpression(pattern), keyword_format)
            )
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor(0, 127, 0))
        comment_format.setFontItalic(True)
        PythonHighlighter.Rules.append(
            (QtCore.QRegularExpression(r"#.*"), comment_format)
        )
        self.stringFormat = QtGui.QTextCharFormat()
        self.stringFormat.setForeground(QtCore.Qt.darkYellow)
        string_re = QtCore.QRegularExpression(r"""(?:'[^']*?'|"[^"]*?")""")
        PythonHighlighter.Rules.append((string_re, self.stringFormat))
        self.stringRe = QtCore.QRegularExpression(r"""(:?"["]".*?"["]"|'''.*?''')""")
        PythonHighlighter.Rules.append((self.stringRe, self.stringFormat))
        self.tripleSingleRe = QtCore.QRegularExpression(r"""'''(?!")""")
        self.tripleDoubleRe = QtCore.QRegularExpression(r'''"""(?!')''')

    def highlightBlock(self, text):
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE = range(3)

        for regex, formatting in PythonHighlighter.Rules:
            match = regex.match(text)

            for i in range(match.lastCapturedIndex() + 1):
                start = match.capturedStart(i)
                end = match.capturedEnd(i)
                self.setFormat(start, end - start, formatting)

        self.setCurrentBlockState(NORMAL)
        if self.stringRe.match(text).hasMatch():
            return
        for match, state in (
            (self.tripleSingleRe.match(text), TRIPLESINGLE),
            (self.tripleDoubleRe.match(text), TRIPLEDOUBLE),
        ):
            if self.previousBlockState() == state:
                if not match.hasMatch():
                    i = len(text)
                    self.setCurrentBlockState(state)
                else:
                    i = match.capturedStart(0)
                self.setFormat(0, i + 3, self.stringFormat)
            elif match.hasMatch():
                start = match.capturedStart(0)
                self.setCurrentBlockState(state)
                self.setFormat(start, len(text), self.stringFormat)


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
            "&New...",
            self.fileNew,
            QtGui.QKeySequence.New,
            "filenew",
            "Create a Python file",
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
        self.editIndentAction = self.createAction(
            "&Indent",
            self.editIndent,
            "Ctrl+]",
            "editindent",
            "Indent the current line or selection",
        )
        self.editUnindentAction = self.createAction(
            "&Unindent",
            self.editUnindent,
            "Ctrl+[",
            "editunindent",
            "Unindent the current line or selection",
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
            edit_menu,
            (
                self.editCopyAction,
                self.editCutAction,
                self.editPasteAction,
                None,
                self.editIndentAction,
                self.editUnindentAction,
            ),
        )
        file_toolbar = self.addToolBar("File")
        file_toolbar.setObjectName("FileToolBar")
        self.addActions(
            file_toolbar, (file_new_action, file_open_action, self.fileSaveAction)
        )
        edit_toolbar = self.addToolBar("Edit")
        edit_toolbar.setObjectName("EditToolBar")
        self.addActions(
            edit_toolbar,
            (
                self.editCopyAction,
                self.editCutAction,
                self.editPasteAction,
                None,
                self.editIndentAction,
                self.editUnindentAction,
            ),
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
        enable = not self.editor.document().isEmpty()
        self.fileSaveAsAction.setEnabled(enable)
        self.editIndentAction.setEnabled(enable)
        self.editUnindentAction.setEnabled(enable)
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
                QtWidgets.QMessageBox.Yes
                | QtWidgets.QMessageBox.No
                | QtWidgets.QMessageBox.Cancel,
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
        except EnvironmentError as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Python Editor -- Load Error",
                "Failed to load {}: {}".format(self.filename, e),
            )
        finally:
            if fh is not None:
                fh.close()
        self.setWindowTitle(
            "Python Editor - {}".format(QtCore.QFileInfo(self.filename).fileName())
        )

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

    def editIndent(self):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            end = cursor.position()
            if start > end:
                start, end = end, start
                pos = start
            cursor.clearSelection()
            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.StartOfLine)
            while pos <= end:
                cursor.insertText("    ")
                cursor.movePosition(QTextCursor.Down)
                cursor.movePosition(QTextCursor.StartOfLine)
                pos = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(
                QTextCursor.NextCharacter, QTextCursor.KeepAnchor, end - start
            )
        else:
            pos = cursor.position()
            cursor.movePosition(QTextCursor.StartOfBlock)
            cursor.insertText("    ")
            cursor.setPosition(pos + 4)
        cursor.endEditBlock()

    def editUnindent(self):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            end = cursor.position()
            if start > end:
                start, end = end, start
                pos = start
            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.StartOfLine)
            while pos <= end:
                cursor.clearSelection()
                cursor.movePosition(
                    QTextCursor.NextCharacter, QTextCursor.KeepAnchor, 4
                )
                if cursor.selectedText() == "    ":
                    cursor.removeSelectedText()
                cursor.movePosition(QTextCursor.Down)
                cursor.movePosition(QTextCursor.StartOfLine)
                pos = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(
                QTextCursor.NextCharacter, QTextCursor.KeepAnchor, end - start
            )
        else:
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.StartOfBlock)
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, 4)
            if cursor.selectedText() == "    ":
                cursor.removeSelectedText()
        cursor.endEditBlock()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("resources:icon.png"))
    f_name = None
    if len(sys.argv) > 1:
        f_name = sys.argv[1]
    form = MainWindow(f_name)
    form.show()
    app.exec()


main()
