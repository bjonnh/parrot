from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout

from sound_manager import SoundManager


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
        self.data = self.sound_manager.list_devices()
