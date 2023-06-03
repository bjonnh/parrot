import librosa
import numpy as np


class ParrotFragment:
    def __init__(self, uid, data, begin, end, name, sr, container):
        if data is not None:
            self.data = data[begin:end]
        self.parameters = {"name": name,
                           "sample_rate": sr,
                           "uid": uid,
                           "container": container,
                           "begin": begin,
                           "end": end}

    @staticmethod
    def from_parameters(parameters):
        si = ParrotFragment(parameters["uid"], None, None, None, parameters["name"], parameters["sample_rate"],
                            parameters["container"])
        si.parameters.update(parameters)

        si.parameters["loaded"] = True
        return si

    @property
    def container(self):
        return self.parameters["container"]

    @property
    def uid(self):
        return self.parameters["uid"]

    @property
    def name(self):
        return self.parameters["name"]

    @property
    def file_name(self):
        return f"{self.uid:016d}_{self.name}"

    @property
    def sample_rate(self):
        return self.parameters["sample_rate"]

    def calculate_parameters(self):
        if "calculated" not in self.parameters:
            self.parameters["calculated"] = True
            self.parameters["samples"] = len(self.data)
            self.parameters["file_name"] = self.file_name
            self.parameters["centroid_average"] = self.centroid()
            self.parameters["bandwidth_average"] = self.bandwidth()
            self.parameters["spectral_contrast"] = self.spectral_contrast()
            self.parameters["spectral_flatness"] = self.spectral_flatness()

    def centroid(self):
        try:
            return np.average(librosa.feature.spectral_centroid(y=self.data, sr=self.sample_rate))
        except librosa.util.exceptions.ParameterError:
            return 0

    def bandwidth(self):
        try:
            return np.average(librosa.feature.spectral_bandwidth(y=self.data, sr=self.sample_rate))
        except librosa.util.exceptions.ParameterError:
            return 0

    def spectral_contrast(self):
        try:
            S = np.abs(librosa.stft(self.data))
            return list(np.average(librosa.feature.spectral_contrast(S=S, sr=self.sample_rate), axis=1))
        except librosa.util.exceptions.ParameterError:
            return 0

    def spectral_flatness(self):
        try:
            return float(np.average(librosa.feature.spectral_flatness(y=self.data)))
        except librosa.util.exceptions.ParameterError:
            return 0
