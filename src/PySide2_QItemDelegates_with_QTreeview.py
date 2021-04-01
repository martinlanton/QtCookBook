import sys
from Qt import QtWidgets, QtGui, QtCore

_MODEL = QtGui.QStandardItemModel()


def startup():
    _DELEGATE = NewNodeDelegate()
    app = QtWidgets.QApplication(sys.argv)
    _MODEL.setHorizontalHeaderLabels(['component_name', 'component_type'])
    main_window = MainWindow()
    main_window.destination.setModel(_MODEL)
    main_window.destination.setItemDelegate(_DELEGATE)
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


class NewNodeDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(NewNodeDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        # new_node = NewNodeWidget(label=str(index.data()), parent=parent)
        new_node = QtWidgets.QPushButton(parent)

        # self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("currentIndexChanged()"))
        return new_node

    def setEditorData(self, editor, index):
        pass

    def setModelData(self, editor, model, index):
        pass

    def paint(self, painter, option, index):
        super(NewNodeDelegate, self).paint(painter, option, index)
        if index.model().hasChildren(index):
            return
        rect = option.rect
        btn = QtWidgets.QPushButton()
        btn.rect = QtCore.QRect(rect.left() + rect.width() - 30, rect.top(), 30, rect.height())
        btn.text = '...'
        QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_PushButton, btn, painter)


class NewNodeWidget(QtWidgets.QWidget):
    QMimeDataType = 'NewNodeQItem'

    def __init__(self, label=None, parent=None):
        super(NewNodeWidget, self).__init__(parent)

        self.drag_start_position = None
        self.label = label

        widgetLayout = QtWidgets.QHBoxLayout(self)
        widgetText = QtWidgets.QLabel(self.label)
        widgetLayout.addWidget(widgetText)
        widgetLayout.addStretch()

        widgetLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setLayout(widgetLayout)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        name = self.label
        print(name)
        drag = QtGui.QDrag(self)
        ba = bytearray(name, 'utf-8')
        drag_mime_data = QtCore.QMimeData()
        drag_mime_data.setData(self.QMimeDataType, QtCore.QByteArray(name))
        drag.setMimeData(drag_mime_data)
        drag.exec_(QtCore.Qt.MoveAction)


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
