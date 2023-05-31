import glob
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QDialog, QFileDialog, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, \
    QTableView, QVBoxLayout, QWidget

from model import ParrotContainer
from sound_manager import SoundManager
from ui.device_selection import DeviceSelectionDialog
from ui.fragment_table_model import FragmentTableModel
from ui.parrot_fragment_ui import ParrotFragmentUI


class CreatorWindow(QDialog):
    def __init__(self, sound_manager: SoundManager):
        super().__init__()
        self.sound_manager = sound_manager
        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle("Creator")

        self.btn_file = QPushButton("Choose audio file")
        self.file_name = QLabel("No file chosen")
        self.name = QLineEdit("Name")
        self.btn_process = QPushButton("Process")
        self.okButton = QPushButton("Quit")

        self.btn_file.clicked.connect(self.get_file)
        self.btn_process.clicked.connect(self.process)
        self.okButton.clicked.connect(self.accept)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn_file)
        self.layout.addWidget(self.file_name)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.btn_process)
        self.layout.addWidget(self.okButton)
        self.setLayout(self.layout)

    def get_file(self):
        file_dialog = QFileDialog(self)
        # the name filters must be a list
        file_dialog.setNameFilters(["MP3 files (*.mp3)", "WAV files (*.wav)"])
        file_dialog.selectNameFilter("Supported audio files (*.mp3 *.wav)")
        # show the dialog
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            if len(filenames) == 1:
                self.file_name.setText(filenames[0])

    def process(self):
        ParrotContainer(self.name.text(), self.file_name.text()).fragment()


class SelectorWindow(QDialog):
    def __init__(self, sound_manager: SoundManager):
        super().__init__()
        self.root = "output/mb/"
        self.sound_manager = sound_manager
        self.setGeometry(0, 0, 1024, 768)
        self.data = []
        self.selected_value = None
        self.setWindowTitle("Selector")

        self.table = QTableView()

        self.model = FragmentTableModel([ParrotFragmentUI()])
        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)

        self.table.selectionModel().selectionChanged.connect(self.play)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.btn_quit = QPushButton("Quit")

        self.btn_quit.clicked.connect(self.accept)

        self.layout = QVBoxLayout()
        self.hlayoutw = QWidget()
        self.hlayout = QHBoxLayout(self.hlayoutw)
        self.layout.addWidget(self.hlayoutw)
        self.hlayout.addWidget(self.table)
        self.layout.addWidget(self.btn_quit)
        self.setLayout(self.layout)

    def show(self):
        self.sound_manager.clear_samples()
        for i in list(glob.glob(f"{self.root}/*.json")):
            self.sound_manager.add_sample(i)
        self.model.update_all_data(self.sound_manager)
        super().show()

    def play(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if len(selected_rows) == 1:
            file_name = self.table.model().data(selected_rows[0], Qt.DisplayRole)
            self.sound_manager.play(f"{self.root}/{file_name}")


def window(sound_manager: SoundManager):
    app = QApplication(sys.argv)
    w = QWidget()

    layout = QHBoxLayout(w)

    b = QLabel()
    b.setText("Parrot")

    btn_setup_audio = QPushButton("Setup audio device")

    btn_creator = QPushButton("Creator")

    btn_selector = QPushButton("Selector")

    btn_quit = QPushButton("Quit")

    device_dialog = DeviceSelectionDialog(sound_manager)
    creator_window = CreatorWindow(sound_manager)
    selector_window = SelectorWindow(sound_manager)

    btn_creator.clicked.connect(creator_window.show)
    btn_setup_audio.clicked.connect(device_dialog.show)
    btn_selector.clicked.connect(selector_window.show)

    layout.addWidget(b)
    layout.addWidget(btn_setup_audio)
    layout.addWidget(btn_creator)
    layout.addWidget(btn_selector)
    layout.addWidget(btn_quit)

    w.setWindowTitle("Parrot")
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window(SoundManager())
