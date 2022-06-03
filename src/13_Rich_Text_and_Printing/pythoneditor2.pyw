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


__version__ = "1.1.0"


class PythonHighlighter(QtGui.QSyntaxHighlighter):

    Rules = []
    Formats = {}

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.initializeFormats()

        KEYWORDS = [
            "and",
            "as",
            "assert",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "exec",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "not",
            "or",
            "pass",
            "print",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield",
        ]
        BUILTINS = [
            "abs",
            "all",
            "any",
            "basestring",
            "bool",
            "callable",
            "chr",
            "classmethod",
            "cmp",
            "compile",
            "complex",
            "delattr",
            "dict",
            "dir",
            "divmod",
            "enumerate",
            "eval",
            "execfile",
            "exit",
            "file",
            "filter",
            "float",
            "frozenset",
            "getattr",
            "globals",
            "hasattr",
            "hex",
            "id",
            "int",
            "isinstance",
            "issubclass",
            "iter",
            "len",
            "list",
            "locals",
            "map",
            "max",
            "min",
            "object",
            "oct",
            "open",
            "ord",
            "pow",
            "property",
            "range",
            "reduce",
            "repr",
            "reversed",
            "round",
            "set",
            "setattr",
            "slice",
            "sorted",
            "staticmethod",
            "str",
            "sum",
            "super",
            "tuple",
            "type",
            "vars",
            "zip",
        ]
        CONSTANTS = ["False", "True", "None", "NotImplemented", "Ellipsis"]

        PythonHighlighter.Rules.append(
            (
                QtCore.QRegularExpression("|".join([r"\b%s\b" % keyword for keyword in KEYWORDS])),
                "keyword",
            )
        )
        PythonHighlighter.Rules.append(
            (
                QtCore.QRegularExpression("|".join([r"\b%s\b" % builtin for builtin in BUILTINS])),
                "builtin",
            )
        )
        PythonHighlighter.Rules.append(
            (
                QtCore.QRegularExpression("|".join([r"\b%s\b" % constant for constant in CONSTANTS])),
                "constant",
            )
        )
        PythonHighlighter.Rules.append(
            (
                QtCore.QRegularExpression(
                    r"\b[+-]?[0-9]+[lL]?\b"
                    r"|\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b"
                    r"|\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b"
                ),
                "number",
            )
        )
        PythonHighlighter.Rules.append(
            (QtCore.QRegularExpression(r"\bPyQt4\b|\bQt?[A-Z][a-z]\w+\b"), "pyqt")
        )
        PythonHighlighter.Rules.append((QtCore.QRegularExpression(r"\b@\w+\b"), "decorator"))
        stringRe = QtCore.QRegularExpression(r"""(?:'[^']*?'|"[^"]*?")""")
        PythonHighlighter.Rules.append((stringRe, "string"))
        self.stringRe = QtCore.QRegularExpression(r"""(:?"["]".*?"["]"|'''.*?''')""")
        PythonHighlighter.Rules.append((self.stringRe, "string"))
        self.tripleSingleRe = QtCore.QRegularExpression(r"""'''(?!")""")
        self.tripleDoubleRe = QtCore.QRegularExpression(r'''"""(?!')''')

    @staticmethod
    def initializeFormats():
        baseFormat = QtGui.QTextCharFormat()
        baseFormat.setFontFamily("courier")
        baseFormat.setFontPointSize(12)
        for name, color in (
            ("normal", QtCore.Qt.black),
            ("keyword", QtCore.Qt.darkBlue),
            ("builtin", QtCore.Qt.darkRed),
            ("constant", QtCore.Qt.darkGreen),
            ("decorator", QtCore.Qt.darkBlue),
            ("comment", QtCore.Qt.darkGreen),
            ("string", QtCore.Qt.darkYellow),
            ("number", QtCore.Qt.darkMagenta),
            ("error", QtCore.Qt.darkRed),
            ("pyqt", QtCore.Qt.darkCyan),
        ):
            format = QtGui.QTextCharFormat(baseFormat)
            format.setForeground(QtGui.QColor(color))
            if name in ("keyword", "decorator"):
                format.setFontWeight(QtGui.QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            PythonHighlighter.Formats[name] = format

    def highlightBlock(self, text):
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE, ERROR = range(4)

        textLength = len(text)
        prevState = self.previousBlockState()

        self.setFormat(0, textLength, PythonHighlighter.Formats["normal"])

        if text.startswith("Traceback") or text.startswith("Error: "):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength, PythonHighlighter.Formats["error"])
            return
        if prevState == ERROR and not (
            text.startswith(sys.ps1) or text.startswith("#")
        ):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength, PythonHighlighter.Formats["error"])
            return

        for regex, formatting in PythonHighlighter.Rules:
            match = regex.match(text)

            for i in range(match.lastCapturedIndex() + 1):
                start = match.capturedStart(i)
                end = match.capturedEnd(i)
                self.setFormat(start, end - start, PythonHighlighter.Formats[formatting])

        # Slow but good quality highlighting for comments. For more
        # speed, comment this out and add the following to __init__:
        # PythonHighlighter.Rules.append((QtCore.QRegularExpression(r"#.*"), "comment"))
        if not text:
            pass
        elif text[0] == "#":
            self.setFormat(0, len(text), PythonHighlighter.Formats["comment"])
        else:
            stack = []
            for i, c in enumerate(text):
                if c in ('"', "'"):
                    if stack and stack[-1] == c:
                        stack.pop()
                    else:
                        stack.append(c)
                elif c == "#" and len(stack) == 0:
                    self.setFormat(i, len(text), PythonHighlighter.Formats["comment"])
                    break

        self.setCurrentBlockState(NORMAL)

        if self.stringRe.match(text).hasMatch():
            return
        # This is fooled by triple quotes inside single quoted strings
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
                self.setFormat(0, i + 3, PythonHighlighter.Formats["string"])
            elif match.hasMatch():
                start = match.capturedStart(0)
                self.setCurrentBlockState(state)
                self.setFormat(start, len(text), PythonHighlighter.Formats["string"])

    def rehighlight(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        QtGui.QSyntaxHighlighter.rehighlight(self)
        QtWidgets.QApplication.restoreOverrideCursor()


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

        fileNewAction = self.createAction(
            "&New...", self.fileNew, QtGui.QKeySequence.New, "filenew", "Create a Python file"
        )
        fileOpenAction = self.createAction(
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
        fileQuitAction = self.createAction(
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

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(
            fileMenu,
            (
                fileNewAction,
                fileOpenAction,
                self.fileSaveAction,
                self.fileSaveAsAction,
                None,
                fileQuitAction,
            ),
        )
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(
            editMenu,
            (
                self.editCopyAction,
                self.editCutAction,
                self.editPasteAction,
                None,
                self.editIndentAction,
                self.editUnindentAction,
            ),
        )
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(
            fileToolbar, (fileNewAction, fileOpenAction, self.fileSaveAction)
        )
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(
            editToolbar,
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
        dir = os.path.dirname(self.filename) if self.filename is not None else "."
        fname, filtering = QtWidgets.QFileDialog.getOpenFileName(
            self, "Python Editor - Choose File", dir, "Python files (*.py *.pyw)"
        )
        if fname:
            self.filename = fname
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
        filename, filtering = QtWidgets.QFileDialog.getSaveFileName(
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
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            while pos <= end:
                cursor.insertText("    ")
                cursor.movePosition(QtGui.QTextCursor.Down)
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                pos = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(
                QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor, end - start
            )
        else:
            pos = cursor.position()
            cursor.movePosition(QtGui.QTextCursor.StartOfBlock)
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
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            while pos <= end:
                cursor.clearSelection()
                cursor.movePosition(
                    QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor, 4
                )
                if cursor.selectedText() == "    ":
                    cursor.removeSelectedText()
                cursor.movePosition(QtGui.QTextCursor.Down)
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                pos = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(
                QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor, end - start
            )
        else:
            cursor.clearSelection()
            cursor.movePosition(QtGui.QTextCursor.StartOfBlock)
            cursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor, 4)
            if cursor.selectedText() == "    ":
                cursor.removeSelectedText()
        cursor.endEditBlock()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))
    fname = None
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    form = MainWindow(fname)
    form.show()
    app.exec()


main()
