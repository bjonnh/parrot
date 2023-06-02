from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QDialog, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider, \
    QVBoxLayout

from model import ParrotContainer
from sound_manager import SoundManager


class CreatorWindow(QDialog):
    def __init__(self, sound_manager: SoundManager):
        super().__init__()
        self.sound_manager : SoundManager = sound_manager
        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle("Creator")

        self.btn_file = QPushButton("Choose audio file")
        self.file_name = QLabel("No file chosen")
        self.name = QLineEdit("Name")

        self.hbox_segments = QHBoxLayout()
        self.segments_label = QLabel("Number of segments")
        self.segments_number = QSlider(Qt.Horizontal)
        self.segments_number.setMinimum(10)
        self.segments_number.setMaximum(2048)
        self.segments_number.setValue(666)
        self.segments_value = QLabel("666")
        self.segments_number.valueChanged.connect(self.segments_value.setNum)
        self.hbox_segments.addWidget(self.segments_label)
        self.hbox_segments.addWidget(self.segments_number)
        self.hbox_segments.addWidget(self.segments_value)


        self.autoload_label = QLabel("Autoload in selector (clears existing)")
        self.cbx_autoload = QCheckBox("Autoload")
        self.cbx_autoload.setChecked(True)
        self.hbox_autoload = QHBoxLayout()
        self.hbox_autoload.addWidget(self.autoload_label)
        self.hbox_autoload.addWidget(self.cbx_autoload)

        self.btn_process = QPushButton("Process")
        self.okButton = QPushButton("Quit")

        self.btn_file.clicked.connect(self.get_file)
        self.btn_process.clicked.connect(self.process)
        self.okButton.clicked.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn_file)
        self.layout.addWidget(self.file_name)
        self.layout.addWidget(self.name)
        self.layout.addLayout(self.hbox_segments)
        self.layout.addLayout(self.hbox_autoload)
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
        pc: ParrotContainer = ParrotContainer(self.name.text(), self.file_name.text())
        pc.fragment(segments=int(self.segments_number.value()))

        if self.cbx_autoload.isChecked():
            self.sound_manager.clear_samples()
            self.sound_manager.load_from_container(pc.container_output_dir, f"{pc.container_output_dir}/container.json")
