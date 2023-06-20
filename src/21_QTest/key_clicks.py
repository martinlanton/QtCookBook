from PySide6 import QtTest, QtWidgets, QtCore
import sys
import unittest


# TODO : setup this properly
class TestKeyClicks(unittest.TestCase):
    def setupClass(self):
        self.app = QtWidgets.QApplication.instance()
        if not self.app:
            self.app = QtWidgets.QApplication(sys.argv)

    def test_key_clicks(self):
        dialog = QtWidgets.QDialog()
        lineEdit = QtWidgets.QLineEdit(dialog)
        dialog.show()
        QtTest.QTest.keyClicks(lineEdit, "hello world")
        QtTest.QCOMPARE(lineEdit.text(), QtCore.QString("hello world"))


if __name__ == '__main__':
    unittest.main()
