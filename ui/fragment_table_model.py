from PyQt5.QtCore import QAbstractTableModel, Qt

from ui.parrot_fragment_ui import ParrotFragmentUI


class FragmentTableModel(QAbstractTableModel):
    def __init__(self, data):
        super(FragmentTableModel, self).__init__()
        self._data: list[ParrotFragmentUI] = data
        self._headers = ParrotFragmentUI.headers

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()].get_column_data(index.column())

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            if self._data[section]:
                return self._data[section].uid

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._headers)

    def append(self, sound_manager):
        self._data += list(sound_manager.samples.values())
        topLeft = self.index(0, 0)
        bottomRight = self.index(len(self._data), len(self._headers))
        self.dataChanged.emit(topLeft, bottomRight)
        self.layoutChanged.emit()

    def sort(self, ncol, order):
        """Sort table by given column number.
        """
        if ncol == 4:
            return

        self.layoutAboutToBeChanged.emit()

        self._data = sorted(self._data, key=lambda x: x.get_column_data(ncol))
        if order == Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()

    def getRowData(self, row):
        return self._data[row]