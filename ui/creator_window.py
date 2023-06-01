from PyQt5.QtWidgets import QDialog, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

from model import ParrotContainer
from sound_manager import SoundManager


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
