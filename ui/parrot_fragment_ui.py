import json
from argparse import ArgumentError

from model.fragment import ParrotFragment


class ParrotFragmentUI:
    headers = ["file_name", "bandwidth_average", "centroid_average", "spectral_contrast", "spectral_flatness", "samples", "sample-rate"]

    def __init__(self, parrot_fragment: ParrotFragment = None):
        self.parrot_fragment = parrot_fragment

    @staticmethod
    def from_json(sample_info):
        return ParrotFragmentUI(ParrotFragment.from_json(sample_info))

    @property
    def uid(self):
        if self.parrot_fragment is None:
            return ""
        return self.parrot_fragment.uid

    def get_column_data(self, idx):
        if self.parrot_fragment is None:
            return ""
        if idx == 0:
            return self.parrot_fragment.parameters["file_name"]
        elif idx == 1:
            return self.parrot_fragment.parameters["bandwidth_average"]
        elif idx == 2:
            return self.parrot_fragment.parameters["centroid_average"]
        elif idx == 3:
            sc = self.parrot_fragment.parameters["spectral_contrast"]
            if isinstance(sc, list):
                return ",".join([f"{i:.2f}" for i in sc])
            else:
                return sc
        elif idx == 4:
            return self.parrot_fragment.parameters["spectral_flatness"]
        elif idx == 5:
            return self.parrot_fragment.parameters["samples"]
        elif idx == 6:
            return self.parrot_fragment.parameters["sample_rate"]
