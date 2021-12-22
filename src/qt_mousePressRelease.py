from Qt import QtWidgets, QtCore, QtGui, QtTest
import sys


class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.var = None

        widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(widget)
        self.widget = QtWidgets.QPushButton("Check this")
        layout.addWidget(self.widget)

        self.widget.clicked.connect(self.set_var)

    def set_var(self):
        print("setting var")
        self.var = "Var has been set"


class DraggableWidget(QtWidgets.QWidget):
    QMimeDataType = "text/plain"

    def __init__(self, label=None):
        super(DraggableWidget, self).__init__()

        self._label = label

        widgetLayout = QtWidgets.QHBoxLayout(self)
        self.widgetText = QtWidgets.QLabel(self._label)
        widgetLayout.addWidget(self.widgetText)
        widgetLayout.addStretch()

        widgetLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setLayout(widgetLayout)

    def label(self):
        return self._label

    def mouseMoveEvent(self, event):
        name = self._label
        print(name)
        drag = QtGui.QDrag(self)
        # ba = bytearray(name, 'utf-8')
        drag_mime_data = QtCore.QMimeData()
        drag_mime_data.setData(self.QMimeDataType, QtCore.QByteArray(name))
        drag.setMimeData(drag_mime_data)
        drag.exec_(QtCore.Qt.MoveAction)


class TestGUIAvailableComponents:
    def setup_method(self):
        # Setup QApplication
        self.app = QtWidgets.QApplication.instance()
        if not self.app:
            self.app = QtWidgets.QApplication(sys.argv)

        self.main_window = Window()
        self.main_window.show()

    def teardown_method(self):
        self.main_window.close()
        del self.main_window

    def test_shouldAddOneWidgetToTheTree_whenDragingFromAvailableComponentToTree(self):
        source_widget = self.main_window.widget
        # destination_widget = self.main_window.line_edit

        # print(source_widget.text())
        print(source_widget)
        # print(destination_widget)
        QtTest.QTest.mousePress(source_widget, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(source_widget, QtCore.Qt.LeftButton)
        # QtTest.QTest.mouseMove(destination_widget)
        # QtTest.QTest.mouseRelease(destination_widget, QtCore.Qt.LeftButton)

        text = self.main_window.var
        assert text == "Var has been set"


def startup():
    app = QtWidgets.QApplication(sys.argv)
    main_window = Window()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    startup()
