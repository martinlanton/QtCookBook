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
import moviedata
import ui_addeditmoviedlg


class AddEditMovieDlg(QtWidgets.QDialog, ui_addeditmoviedlg.Ui_AddEditMovieDlg):
    def __init__(self, movies, movie=None, parent=None):
        super(AddEditMovieDlg, self).__init__(parent)
        self.setupUi(self)

        self.movies = movies
        self.movie = movie
        self.acquiredDateEdit.setDisplayFormat(moviedata.DATEFORMAT)
        if movie is not None:
            self.titleLineEdit.setText(movie.title)
            self.yearSpinBox.setValue(movie.year)
            self.minutesSpinBox.setValue(movie.minutes)
            self.acquiredDateEdit.setDate(movie.acquired)
            self.acquiredDateEdit.setEnabled(False)
            self.notesTextEdit.setPlainText(movie.notes)
            self.notesTextEdit.setFocus()
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("&Accept")
            self.setWindowTitle("My Movies - Edit Movie")
        else:
            today = QtCore.QDate.currentDate()
            self.acquiredDateEdit.setDateRange(today.addDays(-5), today)
            self.acquiredDateEdit.setDate(today)
            self.titleLineEdit.setFocus()
        self.on_titleLineEdit_textEdited("")

    @QtCore.Slot("QString")
    def on_titleLineEdit_textEdited(self, text):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(
            bool(self.titleLineEdit.text())
        )

    def accept(self):
        title = self.titleLineEdit.text()
        year = self.yearSpinBox.value()
        minutes = self.minutesSpinBox.value()
        notes = self.notesTextEdit.toPlainText()
        if self.movie is None:
            acquired = self.acquiredDateEdit.date()
            self.movie = moviedata.Movie(title, year, minutes, acquired, notes)
            self.movies.add(self.movie)
        else:
            self.movies.updateMovie(self.movie, title, year, minutes, notes)
        QtWidgets.QDialog.accept(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    form = AddEditMovieDlg(0)
    form.show()
    app.exec()
