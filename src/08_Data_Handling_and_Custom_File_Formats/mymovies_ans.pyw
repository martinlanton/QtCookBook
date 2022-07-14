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

import platform
import sys
from PySide6 import QtWidgets, QtCore, QtGui
import PySide6
import addeditmoviedlg_ans as addeditmoviedlg
import moviedata_ans as moviedata

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

        self.movies = moviedata.MovieContainer()
        self.table = QtWidgets.QTableWidget()
        self.setCentralWidget(self.table)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        fileNewAction = self.createAction(
            "&New...",
            self.fileNew,
            QtGui.QKeySequence.New,
            "filenew",
            "Create a movie data file",
        )
        fileOpenAction = self.createAction(
            "&Open...",
            self.fileOpen,
            QtGui.QKeySequence.Open,
            "fileopen",
            "Open an existing  movie data file",
        )
        fileSaveAction = self.createAction(
            "&Save",
            self.fileSave,
            QtGui.QKeySequence.Save,
            "filesave",
            "Save the movie data",
        )
        fileSaveAsAction = self.createAction(
            "Save &As...",
            self.fileSaveAs,
            icon="filesaveas",
            tip="Save the movie data using a new name",
        )
        fileImportDOMAction = self.createAction(
            "&Import from XML (DOM)...",
            self.fileImportDOM,
            tip="Import the movie data from an XML file",
        )
        fileImportSAXAction = self.createAction(
            "I&mport from XML (SAX)...",
            self.fileImportSAX,
            tip="Import the movie data from an XML file",
        )
        fileExportXmlAction = self.createAction(
            "E&xport as XML...",
            self.fileExportXml,
            tip="Export the movie data to an XML file",
        )
        fileQuitAction = self.createAction(
            "&Quit", self.close, "Ctrl+Q", "filequit", "Close the application"
        )
        editAddAction = self.createAction(
            "&Add...", self.editAdd, "Ctrl+A", "editadd", "Add data about a movie"
        )
        editEditAction = self.createAction(
            "&Edit...",
            self.editEdit,
            "Ctrl+E",
            "editedit",
            "Edit the current movie's data",
        )
        editRemoveAction = self.createAction(
            "&Remove...", self.editRemove, "Del", "editdelete", "Remove a movie's data"
        )
        helpAboutAction = self.createAction(
            "&About", self.helpAbout, tip="About the application"
        )

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(
            fileMenu,
            (
                fileNewAction,
                fileOpenAction,
                fileSaveAction,
                fileSaveAsAction,
                None,
                fileImportDOMAction,
                fileImportSAXAction,
                fileExportXmlAction,
                None,
                fileQuitAction,
            ),
        )
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editAddAction, editEditAction, editRemoveAction))
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpAboutAction,))

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction, fileSaveAsAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (editAddAction, editEditAction, editRemoveAction))

        self.connect(
            self.table,
            QtCore.SIGNAL("itemDoubleClicked(QtWidgets.QTableWidgetItem*)"),
            self.editEdit,
        )
        QtGui.QShortcut(QtGui.QKeySequence("Return"), self.table, self.editEdit)

        settings = QtCore.QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry", QtCore.QByteArray()))
        self.restoreState(settings.value("MainWindow/State", QtCore.QByteArray()))

        self.setWindowTitle("My Movies")
        QtCore.QTimer.singleShot(0, self.loadInitialFile)

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
            action.setIcon(QtGui.QIcon(":/{}.png".format(icon)))
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
        if self.okToContinue():
            settings = QtCore.QSettings()
            settings.setValue("LastFile", self.movies.filename())
            settings.setValue("MainWindow/Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())
        else:
            event.ignore()

    def okToContinue(self):
        if self.movies.isDirty():
            reply = QtWidgets.QMessageBox.question(
                self,
                "My Movies - Unsaved Changes",
                "Save unsaved changes?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
            )
            if reply == QtWidgets.QMessageBox.Cancel:
                return False
            elif reply == QtWidgets.QMessageBox.Yes:
                return self.fileSave()
        return True

    def loadInitialFile(self):
        settings = QtCore.QSettings()
        fname = settings.value("LastFile")
        if fname and QtCore.QFile.exists(fname):
            ok, msg = self.movies.load(fname)
            self.statusBar().showMessage(msg, 5000)
        self.updateTable()

    def updateTable(self, current=None):
        self.table.clear()
        self.table.setRowCount(len(self.movies))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Title", "Year", "Mins", "Acquired", "Location", "Notes"]
        )
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.table.setSelectionMode(QtWidgets.QTableWidget.SingleSelection)
        selected = None
        for row, movie in enumerate(self.movies):
            item = QtWidgets.QTableWidgetItem(movie.title)
            if current is not None and current == id(movie):
                selected = item
            item.setData(QtCore.Qt.UserRole, int(id(movie)))
            self.table.setItem(row, 0, item)
            year = movie.year
            if year != movie.UNKNOWNYEAR:
                item = QtWidgets.QTableWidgetItem("{}".format(year))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 1, item)
            minutes = movie.minutes
            if minutes != movie.UNKNOWNMINUTES:
                item = QtWidgets.QTableWidgetItem("{}".format(minutes))
                item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.table.setItem(row, 2, item)
            item = QtWidgets.QTableWidgetItem(movie.acquired.toString(moviedata.DATEFORMAT))
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.table.setItem(row, 3, item)
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(movie.location))
            notes = movie.notes
            if len(notes) > 40:
                notes = notes[:39] + "..."
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(notes))
        self.table.resizeColumnsToContents()
        if selected is not None:
            selected.setSelected(True)
            self.table.setCurrentItem(selected)
            self.table.scrollToItem(selected)

    def fileNew(self):
        if not self.okToContinue():
            return
        self.movies.clear()
        self.statusBar().clearMessage()
        self.updateTable()

    def fileOpen(self):
        if not self.okToContinue():
            return
        path = (
            QtCore.QFileInfo(self.movies.filename()).path() if self.movies.filename() else "."
        )
        fname = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "My Movies - Load Movie Data",
            path,
            "My Movies data files ({})".format(self.movies.formats()),
        )
        if fname:
            ok, msg = self.movies.load(fname)
            self.statusBar().showMessage(msg, 5000)
            self.updateTable()

    def fileSave(self):
        if not self.movies.filename():
            return self.fileSaveAs()
        else:
            ok, msg = self.movies.save()
            self.statusBar().showMessage(msg, 5000)
            return ok

    def fileSaveAs(self):
        fname = self.movies.filename() if self.movies.filename() else "."
        fname = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "My Movies - Save Movie Data",
            fname,
            "My Movies data files ({})".format(self.movies.formats()),
        )
        if fname:
            if "." not in fname:
                fname += ".mqb"
            ok, msg = self.movies.save(fname)
            self.statusBar().showMessage(msg, 5000)
            return ok
        return False

    def fileImportDOM(self):
        self.fileImport("dom")

    def fileImportSAX(self):
        self.fileImport("sax")

    def fileImport(self, format):
        if not self.okToContinue():
            return
        path = (
            QtCore.QFileInfo(self.movies.filename()).path() if self.movies.filename() else "."
        )
        fname = QtWidgets.QFileDialog.getOpenFileName(
            self, "My Movies - Import Movie Data", path, "My Movies XML files (*.xml)"
        )
        if fname:
            if format == "dom":
                ok, msg = self.movies.importDOM(fname)
            else:
                ok, msg = self.movies.importSAX(fname)
            self.statusBar().showMessage(msg, 5000)
            self.updateTable()

    def fileExportXml(self):
        fname = self.movies.filename()
        if not fname:
            fname = "."
        else:
            i = fname.rfind(".")
            if i > 0:
                fname = fname[:i]
            fname += ".xml"
        fname = QtWidgets.QFileDialog.getSaveFileName(
            self, "My Movies - Export Movie Data", fname, "My Movies XML files (*.xml)"
        )
        if fname:
            if "." not in fname:
                fname += ".xml"
            ok, msg = self.movies.exportXml(fname)
            self.statusBar().showMessage(msg, 5000)

    def editAdd(self):
        form = addeditmoviedlg.AddEditMovieDlg(self.movies, None, self)
        if form.exec_():
            self.updateTable(id(form.movie))

    def editEdit(self):
        movie = self.currentMovie()
        if movie is not None:
            form = addeditmoviedlg.AddEditMovieDlg(self.movies, movie, self)
            if form.exec_():
                self.updateTable(id(movie))

    def editRemove(self):
        movie = self.currentMovie()
        if movie is not None:
            year = " {}".format(movie.year) if movie.year != movie.UNKNOWNYEAR else ""
            if (
                QtWidgets.QMessageBox.question(
                    self,
                    "My Movies - Delete Movie",
                    "Delete Movie `{}' {}?".format(movie.title, year),
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                )
                == QtWidgets.QMessageBox.Yes
            ):
                self.movies.delete(movie)
                self.updateTable()

    def currentMovie(self):
        row = self.table.currentRow()
        if row > -1:
            item = self.table.item(row, 0)
            id = int(item.data(QtCore.Qt.UserRole))
            return self.movies.movieFromId(id)
        return None

    def helpAbout(self):
        QtWidgets.QMessageBox.about(
            self,
            "My Movies - About",
            """<b>My Movies</b> v {0}
                <p>Copyright &copy; 2008-10 Qtrac Ltd. 
                All rights reserved.
                <p>This application can be used to view some basic
                information about movies and to load and save the 
                movie data in a variety of custom file formats.
                <p>Python {1} - QtCore.Qt {2} - PyQt {3} on {4}""".format(
                __version__,
                platform.python_version(),
                PySide6.QtCore.__version__,
                PySide6.__version__,
                platform.system(),
            ),
        )


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("My Movies")
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()


main()
