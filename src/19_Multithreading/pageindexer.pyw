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
import sys
from PySide6 import QtWidgets, QtCore
import walker


class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

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

        self.walker = walker.Walker(self.lock, self)
        self.connect(self.walker, QtCore.SIGNAL("indexed(QString)"), self.indexed)
        self.connect(self.walker, QtCore.SIGNAL("finished(bool)"), self.finished)
        self.connect(self.pathButton, QtCore.SIGNAL("clicked()"), self.setPath)
        self.connect(self.findEdit, QtCore.SIGNAL("returnPressed()"), self.find)
        self.setWindowTitle("Page Indexer")

    def setPath(self):
        self.pathButton.setEnabled(False)
        if self.walker.isRunning():
            self.walker.stop()
            self.walker.wait()
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Choose a Path to Index", self.path
        )
        if not path:
            self.statusLabel.setText("Click the 'Set Path' " "button to start indexing")
            self.pathButton.setEnabled(True)
            return
        self.path = QtCore.QDir.toNativeSeparators(path)
        self.findEdit.setFocus()
        self.pathLabel.setText(self.path)
        self.statusLabel.clear()
        self.filesListWidget.clear()
        self.fileCount = 0
        self.filenamesForWords = collections.defaultdict(set)
        self.commonWords = set()
        self.walker.initialize(self.path, self.filenamesForWords, self.commonWords)
        self.walker.start()

    def find(self):
        word = self.findEdit.text()
        if not word:
            self.statusLabel.setText("Enter a word to find in files")
            return
        self.statusLabel.clear()
        self.filesListWidget.clear()
        word = word.lower()
        if " " in word:
            word = word.split()[0]
        try:
            self.lock.lockForRead()
            found = word in self.commonWords
        finally:
            self.lock.unlock()
        if found:
            self.statusLabel.setText(
                "Common words like '{}' are " "not indexed".format(word)
            )
            return
        try:
            self.lock.lockForRead()
            files = self.filenamesForWords.get(word, set()).copy()
        finally:
            self.lock.unlock()
        if not files:
            self.statusLabel.setText(
                "No indexed file contains the word '{}'".format(word)
            )
            return
        files = [
            QtCore.QDir.toNativeSeparators(name)
            for name in sorted(files, key=str.lower)
        ]
        self.filesListWidget.addItems(files)
        self.statusLabel.setText(
            "{} indexed files contain the word '{}'".format(len(files), word)
        )

    def indexed(self, fname):
        self.statusLabel.setText(fname)
        self.fileCount += 1
        if self.fileCount % 25 == 0:
            self.filesIndexedLCD.display(self.fileCount)
            try:
                self.lock.lockForRead()
                indexedWordCount = len(self.filenamesForWords)
                commonWordCount = len(self.commonWords)
            finally:
                self.lock.unlock()
            self.wordsIndexedLCD.display(indexedWordCount)
            self.commonWordsLCD.display(commonWordCount)
        elif self.fileCount % 101 == 0:
            self.commonWordsListWidget.clear()
            try:
                self.lock.lockForRead()
                words = self.commonWords.copy()
            finally:
                self.lock.unlock()
            self.commonWordsListWidget.addItems(sorted(words))

    def finished(self, completed):
        self.statusLabel.setText("Indexing complete" if completed else "Stopped")
        self.finishedIndexing()

    def reject(self):
        if self.walker.isRunning():
            self.walker.stop()
            self.finishedIndexing()
        else:
            self.accept()

    def closeEvent(self, event=None):
        self.walker.stop()
        self.walker.wait()

    def finishedIndexing(self):
        self.walker.wait()
        self.filesIndexedLCD.display(self.fileCount)
        self.wordsIndexedLCD.display(len(self.filenamesForWords))
        self.commonWordsLCD.display(len(self.commonWords))
        self.pathButton.setEnabled(True)


app = QtWidgets.QApplication(sys.argv)
form = Form()
form.show()
app.exec()
