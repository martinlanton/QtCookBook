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
