import sys

from PySide6 import QtWidgets


class TestBase:
    gui_to_test = None
    app = None
    dialog = None
    layout = None

    @classmethod
    def setup_class(cls):
        cls.app = QtWidgets.QApplication.instance()
        if not cls.app:
            cls.app = QtWidgets.QApplication(sys.argv)

        cls.dialog = QtWidgets.QDialog()
        cls.layout = cls.gui_to_test(cls.dialog)
        cls.dialog.show()

    @classmethod
    def teardown_class(cls):
        """Cleaning up the content of the dialog in order to run consecutive tests in the same
        class. We wouldn't do that in regular tests as we wouldn't want to change the content of the
        main dialog at every test as we are doing here."""
        children = cls.dialog.children()

        for child in children:
            child.setParent(None)  # We need to set the parent to None to make sure that the
            # instance is properly garbage collected when we deleted it at the next line, otherwise
            # the parent will keep a reference to it, preventing garbage collection
            del child
