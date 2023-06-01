import sys

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, \
    QWidget

from sound_manager import SoundManager
from ui.creator_window import CreatorWindow
from ui.device_selection import DeviceSelectionDialog
from ui.selector_window import SelectorWindow


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
    btn_quit.clicked.connect(lambda: sys.exit(app.exec_()))

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
