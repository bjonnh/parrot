import os

from PyQt5.QtWidgets import QAbstractItemView, QDialog, QFileDialog, QHBoxLayout, QPushButton, QTableView, QVBoxLayout, \
    QWidget

from model import ParrotContainer, ParrotFragment
from sound_manager import SoundManager
from ui.fragment_table_model import FragmentTableModel
from ui.parrot_fragment_ui import ParrotFragmentUI


class SelectorWindow(QDialog):
    def __init__(self, sound_manager: SoundManager):
        super().__init__()
        self.root = None
        self.sound_manager = sound_manager
        self.setGeometry(0, 0, 1024, 768)
        self.data = []
        self.selected_value = None
        self.setWindowTitle("Selector")

        self.table = QTableView()

        self.model = FragmentTableModel([])
        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)

        self.table.selectionModel().selectionChanged.connect(self.play)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.btn_load = QPushButton("Load container")
        self.btn_stop = QPushButton("Stop")
        self.btn_clear = QPushButton("Clear")
        self.btn_quit = QPushButton("Quit")

        self.btn_load.clicked.connect(self.load)
        self.btn_clear.clicked.connect(self.clear)
        self.btn_quit.clicked.connect(self.accept)
        self.btn_stop.clicked.connect(self.sound_manager.stop)

        self.sound_manager.event_system.cleared.connect(self.post_clear)
        self.sound_manager.event_system.loaded.connect(self.post_load)

        self.layout = QVBoxLayout()
        self.hlayoutw = QWidget()
        self.hlayout = QHBoxLayout(self.hlayoutw)
        self.layout.addWidget(self.hlayoutw)
        self.hlayout.addWidget(self.table)
        self.layout.addWidget(self.btn_load)
        self.layout.addWidget(self.btn_stop)
        self.layout.addWidget(self.btn_clear)
        self.layout.addWidget(self.btn_quit)
        self.setLayout(self.layout)

    def accept(self) -> None:
        self.sound_manager.stop()
        super().accept()

    def show(self) -> None:
        super().show()

    def load(self) -> None:
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilters(["Container file (container.json)", "All files (*)"])
        file_dialog.selectNameFilter("Container file (container.json)")
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            if len(filenames) == 1:
                file_name = filenames[0]
                self.root = os.path.dirname(file_name)

                self.sound_manager.load_from_container(self.root, file_name)

    def clear(self) -> None:
        self.sound_manager.clear_samples()

    def post_clear(self) -> None:
        self.table.selectionModel().clear()
        self.model.clear()

    def update(self) -> None:
        self.model.append(self.sound_manager)

    def post_load(self) -> None:
        self.update()

    def play(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if len(selected_rows) == 1:
            row_index = selected_rows[0].row()
            data: ParrotFragmentUI = self.table.model().getRowData(row_index)
            self.sound_manager.play_from_container(data.parrot_container, data.parrot_fragment)
