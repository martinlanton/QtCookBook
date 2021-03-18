import sys
from Qt import QtWidgets, QtGui, QtCore
from pprint import pprint

_MODEL = QtGui.QStandardItemModel()


def startup():
    app = QtWidgets.QApplication(sys.argv)
    _MODEL.setHorizontalHeaderLabels(['component_name', 'component_type'])
    main_window = MainWindow()
    main_window.destination.setModel(_MODEL)
    main_window.show()
    sys.exit(app.exec_())


class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        main_layout = QtWidgets.QHBoxLayout(self)

        self._destination = DestinationTree()
        main_layout.addWidget(self.destination)

        self.add_item_button = QtWidgets.QPushButton('Add Item')
        main_layout.addWidget(self.add_item_button)

        self.add_item_button.clicked.connect(add_item)

    @property
    def destination(self):
        return self._destination

    def item_count(self):
        number_of_items = 0
        iterator = QtWidgets.QTreeWidgetItemIterator(self)
        while iterator.value():
            number_of_items += 1
            iterator += 1

        return number_of_items


def add_item():
    name = 'test'
    print(name)
    print(_MODEL)
    name_item = QtGui.QStandardItem(name)
    type_item = QtGui.QStandardItem(name)
    print(name_item)
    print(type_item)
    _MODEL.appendRow([name_item, type_item])
    # pprint(dir(_MODEL))


class DestinationTree(QtWidgets.QTreeView):
    pass


if __name__ == '__main__':
    startup()
