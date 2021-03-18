import sys
from Qt import QtWidgets, QtGui, QtCore


def startup():
    app = QtWidgets.QApplication(sys.argv)
    tree_model = QtGui.QStandardItemModel()
    tree_model.setHorizontalHeaderLabels(['component_name', 'component_type'])
    main_window = MainWindow()
    main_window.destination.setModel(tree_model)
    main_window.show()
    sys.exit(app.exec_())


class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        main_layout = QtWidgets.QHBoxLayout(self)
        self.source = SourceList()

        main_layout.addWidget(self.source)

        self._destination = DestinationTree()
        main_layout.addWidget(self.destination)

        add_items_to_list(self.source)

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


class SourceList(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(SourceList, self).__init__(parent)


class QListWidgetItemWidget(QtWidgets.QWidget):
    QMimeDataType = 'AddComponentQItem'

    def __init__(self, label=None):
        super(QListWidgetItemWidget, self).__init__()

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


class QTreeViewItemWidget(QListWidgetItemWidget):
    QMimeDataType = 'MoveComponentQItem'


class DestinationTree(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(DestinationTree, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, drag_event):
        mime_data = drag_event.mimeData()
        if mime_data.hasFormat(QListWidgetItemWidget.QMimeDataType):
            drag_event.acceptProposedAction()

    def dragMoveEvent(self, drag_event):
        return

    def dragLeaveEvent(self, drag_event):
        return

    def dropEvent(self, drop_event):
        print('Entering Drop event')
        byte_array = drop_event.mimeData().data(QListWidgetItemWidget.QMimeDataType)
        name = byte_array.data().decode('utf8')

        add_item_to_model(self.model(), name)


def add_items_to_list(list_widget):
    """

    :param list_widget:
    :type list_widget: QtWidget.QListWidget
    :return:
    """
    names = ['model', 'skin', 'arm', 'spine', 'pelvis', 'torso', 'leg']

    for name in names:
        list_widget_item = QtWidgets.QListWidgetItem()
        # Create widget
        widget = QListWidgetItemWidget(name)
        list_widget_item.setSizeHint(widget.sizeHint())

        # Add widget to QListWidget funList
        list_widget.addItem(list_widget_item)
        list_widget.setItemWidget(list_widget_item, widget)


def add_item_to_model(model, name):
    print(name)
    print(model)
    name_item = QtGui.QStandardItem(name)
    type_item = QtGui.QStandardItem(name)
    model.appendRow([name_item, type_item])


if __name__ == '__main__':
    startup()
