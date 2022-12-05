#!/usr/bin/env python3
# Copyright (c) 2007-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import sys
from PySide6 import QtWidgets, QtCore, QtGui, QtNetwork

MAC = "qt_mac_set_native_menubar" in dir()

PORT = 9407
SIZEOF_UINT16 = 2


class BuildingServicesClient(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BuildingServicesClient, self).__init__(parent)

        self.socket = QtNetwork.QTcpSocket()
        self.nextBlockSize = 0
        self.request = None

        roomLabel = QtWidgets.QLabel("&Room")
        self.roomEdit = QtWidgets.QLineEdit()
        roomLabel.setBuddy(self.roomEdit)
        regex = QtCore.QRegularExpression(r"[0-9](?:0[1-9]|[12][0-9]|3[0-4])")
        self.roomEdit.setValidator(QtGui.QRegularExpressionValidator(regex, self))
        self.roomEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        dateLabel = QtWidgets.QLabel("&Date")
        self.dateEdit = QtWidgets.QDateEdit()
        dateLabel.setBuddy(self.dateEdit)
        self.dateEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.dateEdit.setDate(QtCore.QDate.currentDate().addDays(1))
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        responseLabel = QtWidgets.QLabel("Response")
        self.responseLabel = QtWidgets.QLabel()
        self.responseLabel.setFrameStyle(
            QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken
        )

        self.bookButton = QtWidgets.QPushButton("&Book")
        self.bookButton.setEnabled(False)
        self.unBookButton = QtWidgets.QPushButton("&Unbook")
        self.unBookButton.setEnabled(False)
        quitButton = QtWidgets.QPushButton("&Quit")
        if not MAC:
            self.bookButton.setFocusPolicy(QtCore.Qt.NoFocus)
            self.unBookButton.setFocusPolicy(QtCore.Qt.NoFocus)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(self.bookButton)
        buttonLayout.addWidget(self.unBookButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(roomLabel, 0, 0)
        layout.addWidget(self.roomEdit, 0, 1)
        layout.addWidget(dateLabel, 0, 2)
        layout.addWidget(self.dateEdit, 0, 3)
        layout.addWidget(responseLabel, 1, 0)
        layout.addWidget(self.responseLabel, 1, 1, 1, 3)
        layout.addLayout(buttonLayout, 2, 1, 1, 4)
        self.setLayout(layout)

        self.connect(self.socket, QtCore.SIGNAL("connected()"), self.sendRequest)
        self.connect(self.socket, QtCore.SIGNAL("readyRead()"), self.readResponse)
        self.connect(
            self.socket, QtCore.SIGNAL("disconnected()"), self.serverHasStopped
        )
        self.connect(
            self.socket,
            QtCore.SIGNAL("error(QAbstractSocket::SocketError)"),
            self.serverHasError,
        )
        self.connect(self.roomEdit, QtCore.SIGNAL("textEdited(QString)"), self.updateUi)
        self.connect(
            self.dateEdit, QtCore.SIGNAL("dateChanged(QtCore.QDate)"), self.updateUi
        )
        self.connect(self.bookButton, QtCore.SIGNAL("clicked()"), self.book)
        self.connect(self.unBookButton, QtCore.SIGNAL("clicked()"), self.unBook)
        self.connect(quitButton, QtCore.SIGNAL("clicked()"), self.close)

        self.setWindowTitle("Building Services")

    def updateUi(self):
        enabled = False
        if self.roomEdit.text() and self.dateEdit.date() > QtCore.QDate.currentDate():
            enabled = True
        if self.request is not None:
            enabled = False
        self.bookButton.setEnabled(enabled)
        self.unBookButton.setEnabled(enabled)

    def closeEvent(self, event):
        self.socket.close()
        event.accept()

    def book(self):
        self.issueRequest("BOOK", self.roomEdit.text(), self.dateEdit.date())

    def unBook(self):
        self.issueRequest("UNBOOK", self.roomEdit.text(), self.dateEdit.date())

    def issueRequest(self, action, room, date):
        self.request = QtCore.QByteArray()
        stream = QtCore.QDataStream(self.request, QtCore.QIODevice.WriteOnly)
        stream.setVersion(QtCore.QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream.writeQString(action)
        stream.writeQString(room)
        stream << date
        stream.device().seek(0)
        stream.writeUInt16(self.request.size() - SIZEOF_UINT16)
        self.updateUi()
        if self.socket.isOpen():
            self.socket.close()
        self.responseLabel.setText("Connecting to server...")
        self.socket.connectToHost("localhost", PORT)

    def sendRequest(self):
        self.responseLabel.setText("Sending request...")
        self.nextBlockSize = 0
        self.socket.write(self.request)
        self.request = None

    def readResponse(self):
        stream = QtCore.QDataStream(self.socket)
        stream.setVersion(QtCore.QDataStream.Qt_4_2)

        while True:
            if self.nextBlockSize == 0:
                if self.socket.bytesAvailable() < SIZEOF_UINT16:
                    break
                self.nextBlockSize = stream.readUInt16()
            if self.socket.bytesAvailable() < self.nextBlockSize:
                break
            action = stream.readQString()
            room = stream.readQString()
            date = QtCore.QDate()
            if action != "ERROR":
                stream >> date
            if action == "ERROR":
                msg = "Error: {}".format(room)
            elif action == "BOOK":
                msg = "Booked room {} for {}".format(
                    room, date.toString(QtCore.Qt.ISODate)
                )
            elif action == "UNBOOK":
                msg = "Unbooked room {} for {}".format(
                    room, date.toString(QtCore.Qt.ISODate)
                )
            self.responseLabel.setText(msg)
            self.updateUi()
            self.nextBlockSize = 0

    def serverHasStopped(self):
        self.responseLabel.setText("Error: Connection closed by server")
        self.socket.close()

    def serverHasError(self, error):
        self.responseLabel.setText("Error: {}".format(self.socket.errorString()))
        self.socket.close()


app = QtWidgets.QApplication(sys.argv)
form = BuildingServicesClient()
form.show()
app.exec()
