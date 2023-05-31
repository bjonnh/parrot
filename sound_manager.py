import sounddevice as sd
import soundfile as sf

from ui.parrot_fragment_ui import ParrotFragmentUI


class SoundManager:
    def __init__(self):
        self.device = None
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

    def clear_samples(self):
        self.samples = {}

    def add_sample(self, sample_info) -> ParrotFragmentUI:
        si = ParrotFragmentUI.from_json(sample_info)
        self.samples[si.uid] = si
        return si
