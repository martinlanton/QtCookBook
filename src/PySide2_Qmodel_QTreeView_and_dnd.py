import sys
from Qt import QtWidgets, QtGui, QtCore


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


class CustomModel(QtGui.QStandardItemModel):
    def mimeData(self, indexes):
        data = super(CustomModel, self).mimeData(indexes)

    def mimeTypes(self):
        return ["my_custom_type"]

    def dropMimeData(self, data, action, row, column, parent):
        if action != QtCore.Qt.DropAction.MoveAction:
            return False

        print("Now in dropMimeData")
        print(data)
        print(action)
        print(row)
        print(column)
        print(parent)

    def flags(self, index):
        return (
                QtCore.Qt.ItemIsSelectable
                | QtCore.Qt.ItemIsDragEnabled
                | QtCore.Qt.ItemIsDropEnabled
                | QtCore.Qt.ItemIsEditable
                | QtCore.Qt.ItemIsEnabled
        )

    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction


def add_item():
    number = NumberTracker.instance()
    number.number += 1
    name = 'test{}'.format(number)
    print(name)
    name_item = QtGui.QStandardItem(name)
    type_item = QtGui.QStandardItem(name)
    print(model, name_item, type_item)
    model.appendRow([name_item, type_item])
    # pprint(dir(_MODEL))


def startup():
    app = QtWidgets.QApplication(sys.argv)
    model.setHorizontalHeaderLabels(['component_name', 'component_type'])
    main_window = MainWindow()
    main_window.destination.setModel(model)
    main_window.show()
    sys.exit(app.exec_())


class DestinationTree(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(DestinationTree, self).__init__(parent)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        # self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, drag_event):
        mime_data = drag_event.mimeData()
        print(drag_event, mime_data)


class NumberTracker(object):
    _instance = None

    def __init__(self):
        self._number = 0

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = NumberTracker()

        return cls._instance

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    def __repr__(self):
        return str(self._number)


if __name__ == '__main__':
    model = CustomModel()
    startup()
