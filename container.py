import json
import os
import shutil

import librosa
import numpy as np
import soundfile as sf


class ParrotFragment:
    def __init__(self, uid, data, name, sr):
        self.uid = uid
        self.data = data
        self.name = name
        self.sr = sr
        self.parameters = {}

    def file_name(self):
        return f"{self.uid:016d}_{self.name}"

    def calculate_parameters(self):
        if "calculated" not in self.parameters:
            self.parameters["calculated"] = True
            self.parameters["uid"] = self.uid
            self.parameters["sample-rate"] = self.sr
            self.parameters["samples"] = len(self.data)
            self.parameters["file_name"] = self.file_name()
            self.parameters["centroid_average"] = self.centroid()
            self.parameters["bandwidth_average"] = self.bandwidth()
            self.parameters["spectral_contrast"] = self.spectral_contrast()
            self.parameters["spectral_flatness"] = self.spectral_flatness()

    def centroid(self):
        try:
            return np.average(librosa.feature.spectral_centroid(y=self.data, sr=self.sr))
        except librosa.util.exceptions.ParameterError:
            return 0

    def bandwidth(self):
        try:
            return np.average(librosa.feature.spectral_bandwidth(y=self.data, sr=self.sr))
        except librosa.util.exceptions.ParameterError:
            return 0

    def spectral_contrast(self):
        try:
            S = np.abs(librosa.stft(self.data))
            return list(np.average(librosa.feature.spectral_contrast(S=S, sr=self.sr), axis=1))
        except librosa.util.exceptions.ParameterError:
            return 0

    def spectral_flatness(self):
        try:
            return float(np.average(librosa.feature.spectral_flatness(y=self.data)))
        except librosa.util.exceptions.ParameterError:
            return 0


class ParrotContainer:
    def __init__(self, file_name, sr):
        self.file_name = file_name
        self.sr = sr
        self.fragments = []
        self.fragment_ids = 0
        self.container_output_dir = f"output/{self.file_name}/"

    def add_fragment(self, audio_arr, name):
        fragment = ParrotFragment(self.fragment_ids, audio_arr / np.max(audio_arr), name, self.sr)
        self.fragments.append(fragment)
        self.fragment_ids += 1
        fragment.calculate_parameters()

    def write_fragments(self):
        list_fragments = self.fragments
        for f in list_fragments:
            fragment_file_name = f.parameters["file_name"]
            self.write_audio(f.data, fragment_file_name)
            with open(f"{self.container_output_dir}/{fragment_file_name}.json", "w") as file:
                file.write(json.dumps(f.parameters))

    def write_audio(self, audio_arr, split_file_name):
        os.makedirs(self.container_output_dir, exist_ok=True)
        sf.write(f"output/{self.file_name}/{split_file_name}.wav", audio_arr, self.sr)

    def clear(self):
        shutil.rmtree(f"output/{self.file_name}/", ignore_errors=True)
