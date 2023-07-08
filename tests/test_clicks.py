import logging
from PySide6 import QtTest, QtCore

from TwentyOne_QtTest import buttons
from tests.fixtures import TestBase


class TestMouseActions(TestBase):
    def test_mouse_clicks(self, caplog):
        layout = buttons.Layout()
        with caplog.at_level(logging.INFO):
            QtTest.QTest.mouseClick(layout.button_1, QtCore.Qt.LeftButton)
            QtTest.QTest.mouseClick(layout.button_2, QtCore.Qt.LeftButton)

        assert "Hello" in caplog.text
        assert "World" in caplog.text

    def test_mouse_pressed(self, caplog):
        layout = buttons.Layout()
        with caplog.at_level(logging.INFO):
            QtTest.QTest.mousePress(layout.button_1, QtCore.Qt.LeftButton)
            QtTest.QTest.mousePress(layout.button_2, QtCore.Qt.LeftButton)

        assert "Tralala" in caplog.text
        assert "Pouetpouet" in caplog.text

    def test_mouse_released(self, caplog):
        layout = buttons.Layout()
        QtTest.QTest.mousePress(layout.button_1, QtCore.Qt.LeftButton)
        with caplog.at_level(logging.INFO):
            QtTest.QTest.mouseRelease(layout.button_1, QtCore.Qt.LeftButton)

        assert "Releasing on button one" in caplog.text

