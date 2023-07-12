import logging
from PySide6 import QtTest, QtCore

from TwentyOne_QtTest import buttons
from tests.fixtures import TestBase


# TODO : uncomment this and fix it
# class TestMouseActions(TestBase):
#     def test_mouse_move(self, caplog):
#         layout = buttons.Layout()
#         QtTest.QTest.mousePress(layout.button_1, QtCore.Qt.LeftButton)
#
#         with caplog.at_level(logging.INFO):
#             QtTest.QTest.mouseMove(layout.button_2, layout.button_2.mapToGlobal(layout.button_2.rect().center()))
#             QtTest.QTest.mouseRelease(layout.button_2, QtCore.Qt.LeftButton)
#
#         assert "Moving from button one" in caplog.text
#         assert "Moving to button two" in caplog.text
#         assert "Releasing on button two" in caplog.text
