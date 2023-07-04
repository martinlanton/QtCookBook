import sys

from PySide6 import QtWidgets


class TestBase:
    def setup_class(self):
        self.app = QtWidgets.QApplication.instance()
        if not self.app:
            self.app = QtWidgets.QApplication(sys.argv)

        self.dialog = QtWidgets.QDialog()
        self.dialog.show()

    def teardown_method(self):
        """Cleaning up the content of the dialog in order to run consecutive tests in the same
        class. We wouldn't do that in regular tests as we wouldn't want to change the content of the
        main dialog at every test as we are doing here."""
        children = self.dialog.children()

        for child in children:
            child.setParent(None)  # We need to set the parent to none to make sure that the
            # instance is properly garbage collected when we deleted it at the next line, otherwise
            # the parent will keep a reference to it, preventing garbage collection
            del child