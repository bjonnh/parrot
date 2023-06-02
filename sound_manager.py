import sounddevice as sd
import soundfile as sf
from PyQt5.QtCore import QObject, pyqtSignal

from model import ParrotContainer, ParrotFragment
from ui.parrot_fragment_ui import ParrotFragmentUI


class EventSystem(QObject):
    cleared = pyqtSignal()
    loaded = pyqtSignal()


class SoundManager:
    def __init__(self):
        self.device = None
        self.event_system: EventSystem = EventSystem()
        self.samples = {}
        data = self.list_devices()
        for idx, info in enumerate(data):
            if info['max_output_channels'] > 0:
                if info["name"] == "pipewire":
                    self.device = idx

    def list_devices(self):
        return sd.query_devices()

    def set_device(self, device):
        self.device = device

    def play(self, file_name):
        file_name = f"{file_name}.wav"
        data, fs = sf.read(file_name, dtype='float32')
        sd.play(data, fs, device=self.device, loop=True)

    def stop(self) -> None:
        sd.stop()

    def clear_samples(self):
        self.stop()
        self.samples = {}
        self.event_system.cleared.emit()

    def load_from_container(self, root: str, pc: ParrotContainer) -> None:
        for pf in pc.fragments:
            si = ParrotFragmentUI(pc, pf)
            self.samples[si.uid] = si
            si.root = root
        self.event_system.loaded.emit()

    def play_from_container(self, parrot_container: ParrotContainer, parrot_fragment: ParrotFragment):
        self.play(f"{parrot_container.container_output_dir}/{parrot_fragment.file_name}")
