from PySide6 import QtTest

from TwentyOne_QtTest import line_edits
from tests.fixtures import TestBase


class TestKeyActions(TestBase):
    def test_key_clicks(self):
        layout = line_edits.Layout()
        QtTest.QTest.keyClicks(layout.line_edit_1, "Hello")
        QtTest.QTest.keyClicks(layout.line_edit_2, "World")

        assert layout.line_edit_1.text() == "Hello"
        assert layout.line_edit_2.text() == "World"
