import json

import sounddevice as sd
import soundfile as sf


class SampleInfo:
    headers = ["file_name", "bandwidth_average", "centroid_average", "spectral_contrast", "spectral_flatness", "samples", "sample-rate"]

    def __init__(self):
        self.uid = -1
        self.sample_rate = 0
        self.samples = 0
        self.file_name = None
        self.bandwidth_average = None
        self.spectral_contrast = None
        self.spectral_flatness = None
        self.centroid_average = None

    def from_json(sample_info):
        with open(sample_info, "r") as f:
            i = json.load(f)
            si = SampleInfo()
            si.uid = i["uid"]
            si.sample_rate = i["sample-rate"]
            si.samples = i["samples"]
            si.file_name = i["file_name"]
            si.bandwidth_average = i["bandwidth_average"]
            si.spectral_contrast = i["spectral_contrast"]
            si.spectral_flatness = i["spectral_flatness"]
            si.centroid_average = i["centroid_average"]
            return si

    def get_column_data(self, idx):
        if idx == 0:
            return self.file_name
        elif idx == 1:
            return self.bandwidth_average
        elif idx == 2:
            return self.centroid_average
        elif idx == 3:
            if isinstance(self.spectral_contrast, list):
                return ",".join([f"{i:.2f}" for i in self.spectral_contrast])
            else:
                return self.spectral_contrast
        elif idx == 4:
            return self.spectral_flatness
        elif idx == 5:
            return self.samples
        elif idx == 6:
            return self.sample_rate

class SoundManager:
    def __init__(self):
        self.device = None
        self.samples = {}
        self.root = "output/test/"
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
        file_name = f"{self.root}/{file_name}.wav"
        data, fs = sf.read(file_name, dtype='float32')
        sd.play(data, fs, device=self.device, loop=True)

    def clear_samples(self):
        self.samples = {}

    def add_sample(self, sample_info) -> SampleInfo:
        si = SampleInfo.from_json(sample_info)
        self.samples[si.uid] = si
        return si
