import logging
from PySide6 import QtTest, QtCore

from TwentyOne_QtTest import buttons
from tests.fixtures import TestBase


class TestMouseActions(TestBase):
    gui_to_test = buttons.Layout

    def test_mouse_clicks(self, caplog):
        with caplog.at_level(logging.INFO):
            QtTest.QTest.mouseClick(self.layout.button_1, QtCore.Qt.LeftButton)
            QtTest.QTest.mouseClick(self.layout.button_2, QtCore.Qt.LeftButton)

        assert "Hello" in caplog.text
        assert "World" in caplog.text

    def test_mouse_pressed(self, caplog):
        with caplog.at_level(logging.INFO):
            QtTest.QTest.mousePress(self.layout.button_1, QtCore.Qt.LeftButton)
            QtTest.QTest.mousePress(self.layout.button_2, QtCore.Qt.LeftButton)

        assert "Tralala" in caplog.text
        assert "Pouetpouet" in caplog.text

    def test_mouse_released(self, caplog):
        QtTest.QTest.mousePress(self.layout.button_1, QtCore.Qt.LeftButton)
        with caplog.at_level(logging.INFO):
            QtTest.QTest.mouseRelease(self.layout.button_1, QtCore.Qt.LeftButton)

        assert "Releasing on button one" in caplog.text

