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

from PySide6 import QtWidgets, QtCore

CODEC = QtCore.QStringConverter.Utf8


class TextEdit(QtWidgets.QTextEdit):

    NextId = 1

    def __init__(self, filename="", parent=None):
        super(TextEdit, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.filename = filename
        if not self.filename:
            self.filename = "Unnamed-{}.txt".format(TextEdit.NextId)
            TextEdit.NextId += 1
        self.document().setModified(False)
        self.setWindowTitle(QtCore.QFileInfo(self.filename).fileName())

    def closeEvent(self, event):
        if (
            self.document().isModified()
            and QtWidgets.QMessageBox.question(
                self,
                "Text Editor - Unsaved Changes",
                "Save unsaved changes in {}?".format(self.filename),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            == QtWidgets.QMessageBox.Yes
        ):
            try:
                self.save()
            except EnvironmentError as e:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Text Editor -- Save Error",
                    "Failed to save {}: {}".format(self.filename, e),
                )

    def isModified(self):
        return self.document().isModified()

    def save(self):
        if self.filename.startswith("Unnamed"):
            filename, filter = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Text Editor -- Save File As",
                self.filename,
                "Text files (*.txt *.*)",
            )
            if not filename:
                return
            self.filename = filename
        self.setWindowTitle(QtCore.QFileInfo(self.filename).fileName())
        exception = None
        fh = None
        try:
            fh = QtCore.QFile(self.filename)
            if not fh.open(QtCore.QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setEncoding(CODEC)
            stream << self.toPlainText()
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception

    def load(self):
        exception = None
        fh = None
        try:
            fh = QtCore.QFile(self.filename)
            if not fh.open(QtCore.QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setEncoding(CODEC)
            self.setPlainText(stream.readAll())
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception
