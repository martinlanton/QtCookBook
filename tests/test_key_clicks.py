from PySide6 import QtTest

from TwentyOne_QtTest import line_edits
from tests.fixtures import TestBase


class TestKeyActions(TestBase):
    gui_to_test = line_edits.Layout

    def test_key_clicks(self):
        QtTest.QTest.keyClicks(self.layout.line_edit_1, "Hello")
        QtTest.QTest.keyClicks(self.layout.line_edit_2, "World")

        assert self.layout.line_edit_1.text() == "Hello"
        assert self.layout.line_edit_2.text() == "World"
