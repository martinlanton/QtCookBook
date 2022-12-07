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

import bisect
import collections
import sys
from PySide6 import QtWidgets, QtCore, QtNetwork

PORT = 9407
SIZEOF_UINT16 = 2
MAX_BOOKINGS_PER_DAY = 5

# Key = date, value = list of room IDs
Bookings = collections.defaultdict(list)


def printBookings():
    for key in sorted(Bookings):
        print(key, Bookings[key])
    print()


class Thread(QtCore.QThread):

    lock = QtCore.QReadWriteLock()

    def __init__(self, socketId, parent):
        super(Thread, self).__init__(parent)
        self.socketId = socketId

    def run(self):
        socket = QtNetwork.QTcpSocket()
        if not socket.setSocketDescriptor(self.socketId):
            self.emit(QtCore.SIGNAL("error(int)"), socket.error())
            return
        while socket.state() == QtNetwork.QAbstractSocket.ConnectedState:
            nextBlockSize = 0
            stream = QtCore.QDataStream(socket)
            stream.setVersion(QtCore.QDataStream.Qt_4_2)
            if socket.waitForReadyRead() and socket.bytesAvailable() >= SIZEOF_UINT16:
                nextBlockSize = stream.readUInt16()
            else:
                self.sendError(socket, "Cannot read client request")
                return
            if socket.bytesAvailable() < nextBlockSize:
                if (
                    not socket.waitForReadyRead(60000)
                    or socket.bytesAvailable() < nextBlockSize
                ):
                    self.sendError(socket, "Cannot read client data")
                    return
            action = stream.readQString()
            date = QtCore.QDate()
            if action in ("BOOK", "UNBOOK"):
                room = stream.readQString()
                stream >> date
                try:
                    Thread.lock.lockForRead()
                    bookings = Bookings.get(date.toPython())
                finally:
                    Thread.lock.unlock()
                uroom = room
            if action == "BOOK":
                newlist = False
                try:
                    Thread.lock.lockForRead()
                    if bookings is None:
                        newlist = True
                finally:
                    Thread.lock.unlock()
                if newlist:
                    try:
                        Thread.lock.lockForWrite()
                        bookings = Bookings[date.toPython()]
                    finally:
                        Thread.lock.unlock()
                error = None
                insert = False
                try:
                    Thread.lock.lockForRead()
                    if len(bookings) < MAX_BOOKINGS_PER_DAY:
                        if uroom in bookings:
                            error = "Cannot accept duplicate booking"
                        else:
                            insert = True
                    else:
                        error = "{} is fully booked".format(
                            date.toString(QtCore.Qt.ISODate)
                        )
                finally:
                    Thread.lock.unlock()
                if insert:
                    try:
                        Thread.lock.lockForWrite()
                        bisect.insort(bookings, uroom)
                    finally:
                        Thread.lock.unlock()
                    self.sendReply(socket, action, room, date)
                else:
                    self.sendError(socket, error)
            elif action == "UNBOOK":
                error = None
                remove = False
                try:
                    Thread.lock.lockForRead()
                    if bookings is None or uroom not in bookings:
                        error = "Cannot unbook nonexistent booking"
                    else:
                        remove = True
                finally:
                    Thread.lock.unlock()
                if remove:
                    try:
                        Thread.lock.lockForWrite()
                        bookings.remove(uroom)
                    finally:
                        Thread.lock.unlock()
                    self.sendReply(socket, action, room, date)
                else:
                    self.sendError(socket, error)
            else:
                self.sendError(socket, "Unrecognized request")
            socket.waitForDisconnected()
            try:
                Thread.lock.lockForRead()
                printBookings()
            finally:
                Thread.lock.unlock()

    def sendError(self, socket, msg):
        reply = QtCore.QByteArray()
        stream = QtCore.QDataStream(reply, QtCore.QIODevice.WriteOnly)
        stream.setVersion(QtCore.QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream.writeQString("ERROR")
        stream.writeQString(msg)
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        socket.write(reply)

    def sendReply(self, socket, action, room, date):
        reply = QtCore.QByteArray()
        stream = QtCore.QDataStream(reply, QtCore.QIODevice.WriteOnly)
        stream.setVersion(QtCore.QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream.writeQString(action)
        stream.writeQString(room)
        stream << date
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        socket.write(reply)


class TcpServer(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        super(TcpServer, self).__init__(parent)

    def incomingConnection(self, socketId):
        thread = Thread(socketId, self)
        self.connect(
            thread, QtCore.SIGNAL("finished()"), thread, QtCore.SLOT("deleteLater()")
        )
        thread.start()


class BuildingServicesDlg(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(BuildingServicesDlg, self).__init__("&Close Server", parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.loadBookings()
        self.tcpServer = TcpServer(self)
        if not self.tcpServer.listen(QtNetwork.QHostAddress("0.0.0.0"), PORT):
            QtWidgets.QMessageBox.critical(
                self,
                "Building Services Server",
                "Failed to start server: {}".format(self.tcpServer.errorString()),
            )
            self.close()
            return

        self.connect(self, QtCore.SIGNAL("clicked()"), self.close)
        font = self.font()
        font.setPointSize(24)
        self.setFont(font)
        self.setWindowTitle("Building Services Server")

    def loadBookings(self):
        # Generate fake data
        import random

        today = QtCore.QDate.currentDate()
        for i in range(10):
            date = today.addDays(random.randint(7, 60))
            for j in range(random.randint(1, MAX_BOOKINGS_PER_DAY)):
                # Rooms are 001..534 excl. 100, 200, ..., 500
                floor = random.randint(0, 5)
                room = random.randint(1, 34)
                bookings = Bookings[date.toPython()]
                if len(bookings) >= MAX_BOOKINGS_PER_DAY:
                    continue
                bisect.insort(bookings, "{0:1d}{1:02d}".format(floor, room))
        printBookings()


app = QtWidgets.QApplication(sys.argv)
form = BuildingServicesDlg()
form.show()
form.move(0, 0)
app.exec_()
