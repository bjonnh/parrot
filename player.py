import glob
import sys

from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QDialog, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, \
    QPushButton, \
    QTableView, QVBoxLayout, QWidget

from sound_manager import SampleInfo, SoundManager


class DeviceSelectionDialog(QDialog):
    def __init__(self, sound_manager: SoundManager):
        super().__init__()
        self.sound_manager = sound_manager

        self.data = []
        self.selected_value = None
        self.setWindowTitle("Select a device")

        self.list = QListWidget()

        self.okButton = QPushButton("Ok")
        self.cancelButton = QPushButton("Cancel")

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.okButton)
        self.layout.addWidget(self.cancelButton)
        self.setLayout(self.layout)

    def show(self):
        self.list.clear()
        self.update_devices()
        for idx, info in enumerate(self.data):
            if info['max_output_channels'] > 0:
                item = QListWidgetItem()
                item.setText(info["name"])
                item.setData(Qt.UserRole, idx)
                self.list.addItem(item)
        super().show()

    def accept(self):
        self.sound_manager.set_device(self.list.currentItem().data(Qt.UserRole))
        self.selected_value = self.list.currentItem().text()
        super().accept()

    def update_devices(self):
        self.data = sound_manager.list_devices()


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data: list[SampleInfo] = data
        self._headers = SampleInfo.headers

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()].get_column_data(index.column())

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            if self._data[section] != []:
                return self._data[section].uid

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._headers)

    def update_all_data(self, sound_manager):
        self._data = list(sound_manager.samples.values())
        topLeft = self.index(0, 0)
        bottomRight = self.index(len(self._data), len(self._headers))
        self.dataChanged.emit(topLeft, bottomRight)
        self.layoutChanged.emit()

    def sort(self, ncol, order):
        """Sort table by given column number.
        """
        if ncol == 3:
            return

        self.layoutAboutToBeChanged.emit()

        self._data = sorted(self._data, key=lambda x: x.get_column_data(ncol))
        if order == Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()

class SelectorWindow(QDialog):
    def __init__(self, sound_manager: SoundManager):
        super().__init__()
        self.sound_manager = sound_manager
        self.setGeometry(0, 0, 1024, 768)
        self.data = []
        self.selected_value = None
        self.setWindowTitle("Selector")

        self.table = QTableView()

        self.model = TableModel([SampleInfo()])
        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)

        self.table.selectionModel().selectionChanged.connect(self.play)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.okButton = QPushButton("Quit")

        self.okButton.clicked.connect(self.accept)

        self.layout = QVBoxLayout()
        self.hlayoutw = QWidget()
        self.hlayout = QHBoxLayout(self.hlayoutw)
        self.layout.addWidget(self.hlayoutw)
        self.hlayout.addWidget(self.table)
        self.layout.addWidget(self.okButton)
        self.setLayout(self.layout)

    def show(self):
        sound_manager.clear_samples()
        for i in list(glob.glob('output/test/*.json')):
            sound_manager.add_sample(i)
        self.model.update_all_data(sound_manager)
        super().show()

    def play(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if len(selected_rows) == 1:
            self.sound_manager.play(self.table.model().data(selected_rows[0], Qt.DisplayRole))


def window(sound_manager: SoundManager):
    app = QApplication(sys.argv)
    w = QWidget()

    layout = QHBoxLayout(w)

    b = QLabel()
    b.setText("Parrot")

    btn_setup_audio = QPushButton()
    btn_setup_audio.setText("Setup audio device")

    btn_selector = QPushButton()
    btn_selector.setText("Selector")

    device_dialog = DeviceSelectionDialog(sound_manager)
    selector_window = SelectorWindow(sound_manager)

    btn_setup_audio.clicked.connect(device_dialog.show)
    btn_selector.clicked.connect(selector_window.show)

    layout.addWidget(b)
    layout.addWidget(btn_setup_audio)
    layout.addWidget(btn_selector)

    w.setWindowTitle("Parrot")
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sound_manager = SoundManager()
    window(sound_manager)
