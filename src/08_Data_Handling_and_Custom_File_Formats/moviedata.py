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
import pickle
import gzip
from PySide6 import QtCore, QtXml

CODEC = QtCore.QStringConverter.Utf8
NEWPARA = chr(0x2029)
NEWLINE = chr(0x2028)
DATEFORMAT = "ddd MMM d, yyyy"


def encodedNewlines(text):
    return text.replace("\n\n", NEWPARA).replace("\n", NEWLINE)


def decodedNewlines(text):
    return text.replace(NEWPARA, "\n\n").replace(NEWLINE, "\n")


class Movie(object):
    """A Movie object holds the details of a movie.
    
    The data held are the title, year, minutes length, date acquired,
    and notes. If the year is unknown it is set to 1890. If the minutes
    is unknown it is set to 0. The title and notes are held as strings,
    and the notes may contain embedded newlines. Both are plain text,
    and can contain any Unicode characters. The title cannot contain
    newlines or tabs, but the notes can contain both. The date acquired
    is held as a QDate.
    """

    UNKNOWNYEAR = 1890
    UNKNOWNMINUTES = 0

    def __init__(
        self,
        title=None,
        year=UNKNOWNYEAR,
        minutes=UNKNOWNMINUTES,
        acquired=None,
        notes=None,
    ):
        self.title = title
        self.year = year
        self.minutes = minutes
        self.acquired = acquired if acquired is not None else QtCore.QDate.currentDate()
        self.notes = notes


class MovieContainer(object):
    """A MovieContainer holds a set of Movie objects.

    The movies are held in a canonicalized order based on their title
    and year, so if either of these fields is changed the movies must be
    re-sorted. For this reason (and to maintain the dirty flag), all
    updates to movies should be made through this class's updateMovie()
    method.
    """

    MAGIC_NUMBER = 0x3051E
    FILE_VERSION = 100

    def __init__(self):
        self.__fname = ""
        self.__movies = []
        self.__movieFromId = {}
        self.__dirty = False

    def key(self, title, year):
        text = title.lower()
        if text.startswith("a "):
            text = text[2:]
        elif text.startswith("an "):
            text = text[3:]
        elif text.startswith("the "):
            text = text[4:]
        parts = text.split(" ", 1)
        if parts[0].isdigit():
            text = "{0:08d} ".format(int(parts[0]))
            if len(parts) > 1:
                text += parts[1]
        return "{}\t{}".format(text.replace(" ", ""), year)

    def isDirty(self):
        return self.__dirty

    def setDirty(self, dirty=True):
        self.__dirty = dirty

    def clear(self, clearFilename=True):
        self.__movies = []
        self.__movieFromId = {}
        if clearFilename:
            self.__fname = ""
        self.__dirty = False

    def movieFromId(self, id):
        """Returns the movie with the given Python ID."""
        return self.__movieFromId[id]

    def movieAtIndex(self, index):
        """Returns the index-th movie."""
        return self.__movies[index][1]

    def add(self, movie):
        """Adds the given movie to the list if it isn't already
        present. Returns True if added; otherwise returns False."""
        if id(movie) in self.__movieFromId:
            return False
        key = self.key(movie.title, movie.year)
        bisect.insort_left(self.__movies, [key, movie])
        self.__movieFromId[id(movie)] = movie
        self.__dirty = True
        return True

    def delete(self, movie):
        """Deletes the given movie from the list and returns True;
        returns False if the movie isn't in the list."""
        if id(movie) not in self.__movieFromId:
            return False
        key = self.key(movie.title, movie.year)
        i = bisect.bisect_left(self.__movies, [key, movie])
        del self.__movies[i]
        del self.__movieFromId[id(movie)]
        self.__dirty = True
        return True

    def updateMovie(self, movie, title, year, minutes=None, notes=None):
        if minutes is not None:
            movie.minutes = minutes
        if notes is not None:
            movie.notes = notes
        if title != movie.title or year != movie.year:
            key = self.key(movie.title, movie.year)
            i = bisect.bisect_left(self.__movies, [key, movie])
            self.__movies[i][0] = self.key(title, year)
            movie.title = title
            movie.year = year
            self.__movies.sort()
        self.__dirty = True

    def __iter__(self):
        for pair in iter(self.__movies):
            yield pair[1]

    def __len__(self):
        return len(self.__movies)

    def setFilename(self, fname):
        self.__fname = fname

    def filename(self):
        return self.__fname

    @staticmethod
    def formats():
        return "*.mqb *.mpb *.mqt *.mpt"

    def save(self, fname=""):
        if fname:
            self.__fname = fname
        if self.__fname.endswith(".mqb"):
            return self.saveQDataStream()
        elif self.__fname.endswith(".mpb"):
            return self.savePickle()
        elif self.__fname.endswith(".mqt"):
            return self.saveQTextStream()
        elif self.__fname.endswith(".mpt"):
            return self.saveText()
        return False, "Failed to save: invalid file extension"

    def load(self, fname=""):
        if fname:
            self.__fname = fname
        if self.__fname.endswith(".mqb"):
            return self.loadQDataStream()
        elif self.__fname.endswith(".mpb"):
            return self.loadPickle()
        elif self.__fname.endswith(".mqt"):
            return self.loadQTextStream()
        elif self.__fname.endswith(".mpt"):
            return self.loadText()
        return False, "Failed to load: invalid file extension"

    def saveQDataStream(self):
        error = None
        file = None
        try:
            file = QtCore.QFile(self.__fname)
            if not file.open(QtCore.QIODevice.WriteOnly):
                raise IOError(file.errorString())
            stream = QtCore.QDataStream(file)
            stream.writeInt32(MovieContainer.MAGIC_NUMBER)
            stream.writeInt32(MovieContainer.FILE_VERSION)
            stream.setVersion(QtCore.QDataStream.Qt_4_2)
            for key, movie in self.__movies:
                stream.writeQString(movie.title)
                stream.writeInt16(movie.year)
                stream.writeInt16(movie.minutes)
                stream.writeQString(movie.acquired.toString(QtCore.Qt.ISODate))
                stream.writeQString(movie.notes)
        except EnvironmentError as e:
            error = "Failed to save: {}".format(e)
        finally:
            if file is not None:
                file.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return (
                True,
                "Saved {} movie records to {}".format(
                    len(self.__movies), QtCore.QFileInfo(self.__fname).fileName()
                ),
            )

    def loadQDataStream(self):
        error = None
        file = None
        try:
            file = QtCore.QFile(self.__fname)
            if not file.open(QtCore.QIODevice.ReadOnly):
                raise IOError(file.errorString())
            stream = QtCore.QDataStream(file)
            magic = stream.readInt32()
            if magic != MovieContainer.MAGIC_NUMBER:
                raise IOError("unrecognized file type")
            version = stream.readInt32()
            if version < MovieContainer.FILE_VERSION:
                raise IOError("old and unreadable file format")
            elif version > MovieContainer.FILE_VERSION:
                raise IOError("new and unreadable file format")
            stream.setVersion(QtCore.QDataStream.Qt_4_2)
            self.clear(False)
            while not stream.atEnd():
                title = stream.readQString()
                year = stream.readInt16()
                minutes = stream.readInt16()
                acquired = QtCore.QDate.fromString(stream.readQString(), QtCore.Qt.ISODate)
                notes = stream.readQString()
                self.add(Movie(title, year, minutes, acquired, notes))
        except EnvironmentError as e:
            error = "Failed to load: {}".format(e)
        finally:
            if file is not None:
                file.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return (
                True,
                "Loaded {} movie records from {}".format(
                    len(self.__movies), QtCore.QFileInfo(self.__fname).fileName()
                ),
            )

    def savePickle(self):
        error = None
        fh = None
        try:
            fh = gzip.open(self.__fname, "wb")
            pickle.dump(self.__movies, fh, 2)
        except EnvironmentError as e:
            error = "Failed to save: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return (
                True,
                "Saved {} movie records to {}".format(
                    len(self.__movies), QtCore.QFileInfo(self.__fname).fileName()
                ),
            )

    def loadPickle(self):
        error = None
        fh = None
        try:
            fh = gzip.open(self.__fname, "rb")
            self.clear(False)
            self.__movies = pickle.load(fh)
            for key, movie in self.__movies:
                self.__movieFromId[id(movie)] = movie
        except EnvironmentError as e:
            error = "Failed to load: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return (
                True,
                "Loaded {} movie records from {}".format(
                    len(self.__movies), QtCore.QFileInfo(self.__fname).fileName()
                ),
            )

    def saveQTextStream(self):
        error = None
        fh = None
        try:
            fh = QtCore.QFile(self.__fname)
            if not fh.open(QtCore.QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setEncoding(CODEC)
            for key, movie in self.__movies:
                stream << "{{MOVIE}} " << movie.title << "\n" << movie.year << " " << movie.minutes << " " << movie.acquired.toString(
                    QtCore.Qt.ISODate
                ) << "\n{NOTES}"
                if movie.notes:
                    stream << "\n" << movie.notes
                stream << "\n{{ENDMOVIE}}\n"
        except EnvironmentError as e:
            error = "Failed to save: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return (
                True,
                "Saved {} movie records to {}".format(
                    len(self.__movies), QtCore.QFileInfo(self.__fname).fileName()
                ),
            )

    def loadQTextStream(self):
        error = None
        fh = None
        try:
            fh = QtCore.QFile(self.__fname)
            if not fh.open(QtCore.QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setEncoding(CODEC)
            self.clear(False)
            lino = 0
            while not stream.atEnd():
                title = year = minutes = acquired = notes = None
                line = stream.readLine()
                lino += 1
                if not line.startswith("{{MOVIE}}"):
                    raise ValueError("no movie record found")
                else:
                    title = line[len("{{MOVIE}}") :].strip()
                if stream.atEnd():
                    raise ValueError("premature end of file")
                line = stream.readLine()
                lino += 1
                parts = line.split(" ")
                if len(parts) != 3:
                    raise ValueError("invalid numeric data")
                year = int(parts[0])
                minutes = int(parts[1])
                ymd = parts[2].split("-")
                if len(ymd) != 3:
                    raise ValueError("invalid acquired date")
                acquired = QtCore.QDate(int(ymd[0]), int(ymd[1]), int(ymd[2]))
                if stream.atEnd():
                    raise ValueError("premature end of file")
                line = stream.readLine()
                lino += 1
                if line != "{NOTES}":
                    raise ValueError("notes expected")
                notes = ""
                while not stream.atEnd():
                    line = stream.readLine()
                    lino += 1
                    if line == "{{ENDMOVIE}}":
                        if (
                            title is None
                            or year is None
                            or minutes is None
                            or acquired is None
                            or notes is None
                        ):
                            raise ValueError("incomplete record")
                        self.add(Movie(title, year, minutes, acquired, notes.strip()))
                        break
                    else:
                        notes += line + "\n"
                else:
                    raise ValueError("missing endmovie marker")
        except (IOError, OSError, ValueError) as e:
            error = "Failed to load: {} on line {}".format(e, lino)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return (
                True,
                "Loaded {} movie records from {}".format(
                    len(self.__movies), QtCore.QFileInfo(self.__fname).fileName()
                ),
            )

    def saveText(self):
        error = None
        fh = None
        try:
            fh = open(self.__fname, "w", encoding=CODEC)
            for key, movie in self.__movies:
                fh.write("{{{{MOVIE}}}} {}\n".format(movie.title))
                fh.write(
                    "{} {} {}\n".format(
                        movie.year, movie.minutes, movie.acquired.toString(QtCore.Qt.ISODate)
                    )
                )
                fh.write("{NOTES}")
                if movie.notes:
                    fh.write("\n{}".format(movie.notes))
                fh.write("\n{{ENDMOVIE}}\n")
        except EnvironmentError as e:
            error = "Failed to save: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return (
                True,
                "Saved {} movie records to {}".format(
                    len(self.__movies), QtCore.QFileInfo(self.__fname).fileName()
                ),
            )

    def loadText(self):
        error = None
        fh = None
        try:
            fh = open(self.__fname, "rU", encoding=CODEC)
            self.clear(False)
            lino = 0
            while True:
                title = year = minutes = acquired = notes = None
                line = fh.readline()
                if not line:
                    break
                lino += 1
                if not line.startswith("{{MOVIE}}"):
                    raise ValueError("no movie record found")
                else:
                    title = line[len("{{MOVIE}}") :].strip()
                line = fh.readline()
                if not line:
                    raise ValueError("premature end of file")
                lino += 1
                parts = line.split(" ")
                if len(parts) != 3:
                    raise ValueError("invalid numeric data")
                year = int(parts[0])
                minutes = int(parts[1])
                ymd = parts[2].split("-")
                if len(ymd) != 3:
                    raise ValueError("invalid acquired date")
                acquired = QtCore.QDate(int(ymd[0]), int(ymd[1]), int(ymd[2]))
                line = fh.readline()
                if not line:
                    raise ValueError("premature end of file")
                lino += 1
                if line != "{NOTES}\n":
                    raise ValueError("notes expected")
                notes = ""
                while True:
                    line = fh.readline()
                    if not line:
                        raise ValueError("missing endmovie marker")
                    lino += 1
                    if line == "{{ENDMOVIE}}\n":
                        if (
                            title is None
                            or year is None
                            or minutes is None
                            or acquired is None
                            or notes is None
                        ):
                            raise ValueError("incomplete record")
                        self.add(Movie(title, year, minutes, acquired, notes.strip()))
                        break
                    else:
                        notes += line
        except (IOError, OSError, ValueError) as e:
            error = "Failed to load: {} on line {}".format(e, lino)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return (
                True,
                "Loaded {} movie records from {}".format(
                    len(self.__movies), QtCore.QFileInfo(self.__fname).fileName()
                ),
            )

    def exportXml(self, fname):
        error = None
        fh = None
        try:
            fh = QtCore.QFile(fname)
            if not fh.open(QtCore.QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setEncoding(CODEC)
            stream << (
                "<?xml version='1.0' encoding='UTF-8'?>\n"
                "<!DOCTYPE MOVIES>\n"
                "<MOVIES VERSION='{}'>\n".format(MovieContainer.FILE_VERSION)
            )
            for key, movie in self.__movies:
                stream << (
                    "<MOVIE YEAR='{}' MINUTES='{}' "
                    "ACQUIRED='{}'>\n".format(
                        movie.year, movie.minutes, movie.acquired.toString(QtCore.Qt.ISODate)
                    )
                ) << "<TITLE>" << movie.title.replace("&", "&amp;") << "</TITLE>\n<NOTES>"
                if movie.notes:
                    stream << "\n" << encodedNewlines(movie.notes).replace("&", "&amp;")
                stream << "\n</NOTES>\n</MOVIE>\n"
            stream << "</MOVIES>\n"
        except EnvironmentError as e:
            error = "Failed to export: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return (
                True,
                "Exported {} movie records to {}".format(
                    len(self.__movies), QtCore.QFileInfo(fname).fileName()
                ),
            )

    def importDOM(self, fname):
        dom = QtXml.QDomDocument()
        error = None
        fh = None
        try:
            fh = QtCore.QFile(fname)
            if not fh.open(QtCore.QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            if not dom.setContent(fh):
                raise ValueError("could not parse XML")
        except (IOError, OSError, ValueError) as e:
            error = "Failed to import: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
        try:
            self.populateFromDOM(dom)
        except ValueError as e:
            return False, "Failed to import: {}".format(e)
        self.__fname = ""
        self.__dirty = True
        return (
            True,
            "Imported {} movie records from {}".format(
                len(self.__movies), QtCore.QFileInfo(fname).fileName()
            ),
        )

    def populateFromDOM(self, dom):
        root = dom.documentElement()
        if root.tagName() != "MOVIES":
            raise ValueError("not a Movies XML file")
        self.clear(False)
        node = root.firstChild()
        while not node.isNull():
            if node.toElement().tagName() == "MOVIE":
                self.readMovieNode(node.toElement())
            node = node.nextSibling()

    def readMovieNode(self, element):
        def getText(node):
            child = node.firstChild()
            text = ""
            while not child.isNull():
                if child.nodeType() == QtXml.QDomNode.TextNode:
                    text += child.toText().data()
                child = child.nextSibling()
            return text.strip()

        year = int(element.attribute("YEAR"))
        minutes = int(element.attribute("MINUTES"))
        ymd = element.attribute("ACQUIRED").split("-")
        if len(ymd) != 3:
            raise ValueError(
                "invalid acquired date {}".format(element.attribute("ACQUIRED"))
            )
        acquired = QtCore.QDate(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        title = notes = None
        node = element.firstChild()
        while title is None or notes is None:
            if node.isNull():
                raise ValueError("missing title or notes")
            if node.toElement().tagName() == "TITLE":
                title = getText(node)
            elif node.toElement().tagName() == "NOTES":
                notes = getText(node)
            node = node.nextSibling()
        if not title:
            raise ValueError("missing title")
        self.add(Movie(title, year, minutes, acquired, decodedNewlines(notes)))

    def importSAX(self, fname):
        print(fname)
        error = None
        fh = None
        try:
            fh = QtCore.QFile(fname)
            if not fh.open(QtCore.QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QXmlStreamReader(fh)

            # Get to document start
            stream.readNext()
            print("StartDocument : %s" % stream.isStartDocument())

            # Get to DTD
            stream.readNext()
            file_type = stream.dtdName()
            if file_type != "MOVIES":
                raise IOError("unrecognized file type")

            # Get to MOVIES start
            stream.readNext()
            version = int(stream.attributes().value("VERSION"))
            print("Version is : %s, %s\n\n" % (type(version), version))
            if version < MovieContainer.FILE_VERSION:
                raise IOError("old and unreadable file format")
            elif version > MovieContainer.FILE_VERSION:
                raise IOError("new and unreadable file format")

            # Get to MOVIES start character
            stream.readNext()

            self.clear(False)

            while not stream.atEnd():
                # Get to movie start
                stream.readNext()
                # Check if we encountered an end element
                # if yes, that means it's the end of the file
                if stream.tokenString() == "EndElement":
                    print("At end")
                    break
                attr = stream.attributes()
                year = int(attr.value("YEAR"))
                minutes = int(attr.value("MINUTES"))
                acquired = QtCore.QDate.fromString(attr.value("ACQUIRED"), QtCore.Qt.ISODate)
                # Get to movie start character
                stream.readNext()

                # Get to title start
                stream.readNext()

                # Get to title start character
                stream.readNext()
                title = stream.text()

                # Get to title end
                stream.readNext()

                # Get to title end character
                stream.readNext()

                # Get to notes start
                stream.readNext()

                # Get to notes start character
                stream.readNext()
                # using strip to remove white spaces added at export for xml formatting
                notes = stream.text().strip()

                # Get to nodes end
                stream.readNext()

                # Get to nodes end characters
                stream.readNext()

                # Get to movie end
                stream.readNext()

                # Get to movie end characters
                stream.readNext()

                self.add(Movie(title, year, minutes, acquired, notes))

        except (IOError, OSError, ValueError) as e:
            error = "Failed to import: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__fname = ""
            self.__dirty = True
            return (
                True,
                "Imported {} movie records from {}".format(
                    len(self.__movies), QtCore.QFileInfo(fname).fileName()
                ),
            )
