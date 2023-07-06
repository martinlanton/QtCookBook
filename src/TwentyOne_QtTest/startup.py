import sys
from PySide6 import QtWidgets

from buttons import Layout

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def startup():
    log.info("Something")
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    layout = Layout(dialog)
    dialog.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    startup()
