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

import collections
import os
import sys
from PySide6 import QtWidgets, QtCore
import walker_ans as walker


def isAlive(qobj):
    # TODO : remove call to sip.unwrapinstance and find a better alternative
    #  here : https://realpython.com/python-pyqt-qthread/
    import sip

    try:
        sip.unwrapinstance(qobj)
    except RuntimeError:
        return False
    return True


class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.mutex = QtCore.QMutex()
        self.fileCount = 0
        self.filenamesForWords = collections.defaultdict(set)
        self.commonWords = set()
        self.lock = QtCore.QReadWriteLock()
        self.path = QtCore.QDir.homePath()
        pathLabel = QtWidgets.QLabel("Indexing path:")
        self.pathLabel = QtWidgets.QLabel()
        self.pathLabel.setFrameStyle(
            QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken
        )
        self.pathButton = QtWidgets.QPushButton("Set &Path...")
        self.pathButton.setAutoDefault(False)
        findLabel = QtWidgets.QLabel("&Find word:")
        self.findEdit = QtWidgets.QLineEdit()
        findLabel.setBuddy(self.findEdit)
        commonWordsLabel = QtWidgets.QLabel("&Common words:")
        self.commonWordsListWidget = QtWidgets.QListWidget()
        commonWordsLabel.setBuddy(self.commonWordsListWidget)
        filesLabel = QtWidgets.QLabel("Files containing the &word:")
        self.filesListWidget = QtWidgets.QListWidget()
        filesLabel.setBuddy(self.filesListWidget)
        filesIndexedLabel = QtWidgets.QLabel("Files indexed")
        self.filesIndexedLCD = QtWidgets.QLCDNumber()
        self.filesIndexedLCD.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        wordsIndexedLabel = QtWidgets.QLabel("Words indexed")
        self.wordsIndexedLCD = QtWidgets.QLCDNumber()
        self.wordsIndexedLCD.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        commonWordsLCDLabel = QtWidgets.QLabel("Common words")
        self.commonWordsLCD = QtWidgets.QLCDNumber()
        self.commonWordsLCD.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.statusLabel = QtWidgets.QLabel(
            "Click the 'Set Path' " "button to start indexing"
        )
        self.statusLabel.setFrameStyle(
            QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken
        )

        topLayout = QtWidgets.QHBoxLayout()
        topLayout.addWidget(pathLabel)
        topLayout.addWidget(self.pathLabel, 1)
        topLayout.addWidget(self.pathButton)
        topLayout.addWidget(findLabel)
        topLayout.addWidget(self.findEdit, 1)
        leftLayout = QtWidgets.QVBoxLayout()
        leftLayout.addWidget(filesLabel)
        leftLayout.addWidget(self.filesListWidget)
        rightLayout = QtWidgets.QVBoxLayout()
        rightLayout.addWidget(commonWordsLabel)
        rightLayout.addWidget(self.commonWordsListWidget)
        middleLayout = QtWidgets.QHBoxLayout()
        middleLayout.addLayout(leftLayout, 1)
        middleLayout.addLayout(rightLayout)
        bottomLayout = QtWidgets.QHBoxLayout()
        bottomLayout.addWidget(filesIndexedLabel)
        bottomLayout.addWidget(self.filesIndexedLCD)
        bottomLayout.addWidget(wordsIndexedLabel)
        bottomLayout.addWidget(self.wordsIndexedLCD)
        bottomLayout.addWidget(commonWordsLCDLabel)
        bottomLayout.addWidget(self.commonWordsLCD)
        bottomLayout.addStretch()
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addLayout(middleLayout)
        layout.addLayout(bottomLayout)
        layout.addWidget(self.statusLabel)
        self.setLayout(layout)

        self.walkers = []
        self.completed = []
        self.connect(self.pathButton, QtCore.SIGNAL("clicked()"), self.setPath)
        self.connect(self.findEdit, QtCore.SIGNAL("returnPressed()"), self.find)
        self.setWindowTitle("Page Indexer")

    def stopWalkers(self):
        for walker in self.walkers:
            if isAlive(walker) and walker.isRunning():
                walker.stop()
        for walker in self.walkers:
            if isAlive(walker) and walker.isRunning():
                walker.wait()
        self.walkers = []
        self.completed = []

    def setPath(self):
        self.stopWalkers()
        self.pathButton.setEnabled(False)
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Choose a Path to Index", self.path
        )
        if not path:
            self.statusLabel.setText("Click the 'Set Path' " "button to start indexing")
            self.pathButton.setEnabled(True)
            return
        self.statusLabel.setText("Scanning directories...")
        QtWidgets.QApplication.processEvents()  # Needed for Windows
        self.path = QtCore.QDir.toNativeSeparators(path)
        self.findEdit.setFocus()
        self.pathLabel.setText(self.path)
        self.statusLabel.clear()
        self.filesListWidget.clear()
        self.fileCount = 0
        self.filenamesForWords = collections.defaultdict(set)
        self.commonWords = set()
        nofilesfound = True
        files = []
        index = 0
        for root, dirs, fnames in os.walk(self.path):
            for name in [name for name in fnames if name.endswith((".htm", ".html"))]:
                files.append(os.path.join(root, name))
                if len(files) == 1000:
                    self.processFiles(index, files[:])
                    files = []
                    index += 1
                    nofilesfound = False
        if files:
            self.processFiles(index, files[:])
            nofilesfound = False
        if nofilesfound:
            self.finishedIndexing()
            self.statusLabel.setText("No HTML files found in the given path")

    def processFiles(self, index, files):
        thread = walker.Walker(
            index, self.lock, files, self.filenamesForWords, self.commonWords, self
        )
        self.connect(thread, QtCore.SIGNAL("indexed(QString,int)"), self.indexed)
        self.connect(thread, QtCore.SIGNAL("finished(bool,int)"), self.finished)
        self.connect(
            thread, QtCore.SIGNAL("finished()"), thread, QtCore.SLOT("deleteLater()")
        )
        self.walkers.append(thread)
        self.completed.append(False)
        thread.start()
        thread.wait(300)  # Needed for Windows

    def find(self):
        word = self.findEdit.text()
        if not word:
            try:
                self.mutex.lock()
                self.statusLabel.setText("Enter a word to find in files")
            finally:
                self.mutex.unlock()
            return
        try:
            self.mutex.lock()
            self.statusLabel.clear()
            self.filesListWidget.clear()
        finally:
            self.mutex.unlock()
        word = word.lower()
        if " " in word:
            word = word.split()[0]
        try:
            self.lock.lockForRead()
            found = word in self.commonWords
        finally:
            self.lock.unlock()
        if found:
            try:
                self.mutex.lock()
                self.statusLabel.setText(
                    "Common words like '{}' " "are not indexed".format(word)
                )
            finally:
                self.mutex.unlock()
            return
        try:
            self.lock.lockForRead()
            files = self.filenamesForWords.get(word, set()).copy()
        finally:
            self.lock.unlock()
        if not files:
            try:
                self.mutex.lock()
                self.statusLabel.setText(
                    "No indexed file contains " "the word '{}'".format(word)
                )
            finally:
                self.mutex.unlock()
            return
        files = [
            QtCore.QDir.toNativeSeparators(name)
            for name in sorted(files, key=str.lower)
        ]
        try:
            self.mutex.lock()
            self.filesListWidget.addItems(files)
            self.statusLabel.setText(
                "{} indexed files contain the word '{}'".format(len(files), word)
            )
        finally:
            self.mutex.unlock()

    def indexed(self, fname, index):
        try:
            self.mutex.lock()
            self.statusLabel.setText(fname)
            self.fileCount += 1
            count = self.fileCount
        finally:
            self.mutex.unlock()
        if count % 25 == 0:
            try:
                self.lock.lockForRead()
                indexedWordCount = len(self.filenamesForWords)
                commonWordCount = len(self.commonWords)
            finally:
                self.lock.unlock()
            try:
                self.mutex.lock()
                self.filesIndexedLCD.display(count)
                self.wordsIndexedLCD.display(indexedWordCount)
                self.commonWordsLCD.display(commonWordCount)
            finally:
                self.mutex.unlock()
        elif count % 101 == 0:
            try:
                self.lock.lockForRead()
                words = self.commonWords.copy()
            finally:
                self.lock.unlock()
            try:
                self.mutex.lock()
                self.commonWordsListWidget.clear()
                self.commonWordsListWidget.addItems(sorted(words))
            finally:
                self.mutex.unlock()

    def finished(self, completed, index):
        done = False
        if self.walkers:
            self.completed[index] = True
            if all(self.completed):
                try:
                    self.mutex.lock()
                    self.statusLabel.setText("Finished")
                    done = True
                finally:
                    self.mutex.unlock()
        else:
            try:
                self.mutex.lock()
                self.statusLabel.setText("Finished")
                done = True
            finally:
                self.mutex.unlock()
        if done:
            self.finishedIndexing()

    def reject(self):
        if not all(self.completed):
            self.stopWalkers()
            self.finishedIndexing()
        else:
            self.accept()

    def closeEvent(self, event=None):
        self.stopWalkers()

    def finishedIndexing(self):
        self.filesIndexedLCD.display(self.fileCount)
        self.wordsIndexedLCD.display(len(self.filenamesForWords))
        self.commonWordsLCD.display(len(self.commonWords))
        self.pathButton.setEnabled(True)
        QtWidgets.QApplication.processEvents()  # Needed for Windows


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec()
