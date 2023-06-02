from model import ParrotContainer
from model.fragment import ParrotFragment


class ParrotFragmentUI:
    headers = ["container", "file_name", "bandwidth_average", "centroid_average", "spectral_contrast",
               "spectral_flatness", "samples", "sample-rate"]

    def __init__(self, parrot_container: ParrotContainer = None, parrot_fragment: ParrotFragment = None):
        self.parrot_container: ParrotContainer = parrot_container
        self.parrot_fragment: ParrotFragment = parrot_fragment
        self.root: str | None = None

    @property
    def uid(self) -> str:
        if self.parrot_fragment is None:
            return ""
        return self.parrot_fragment.uid

    def get_column_data(self, idx):
        if self.parrot_fragment is None:
            return ""
        if idx == 0:
            return self.parrot_fragment.parameters["container"]
        elif idx == 1:
            return self.parrot_fragment.parameters["file_name"]
        elif idx == 2:
            return self.parrot_fragment.parameters["bandwidth_average"]
        elif idx == 3:
            return self.parrot_fragment.parameters["centroid_average"]
        elif idx == 4:
            sc = self.parrot_fragment.parameters["spectral_contrast"]
            if isinstance(sc, list):
                return ",".join([f"{i:.2f}" for i in sc])
            else:
                return sc
        elif idx == 5:
            return self.parrot_fragment.parameters["spectral_flatness"]
        elif idx == 6:
            return self.parrot_fragment.parameters["samples"]
        elif idx == 7:
            return self.parrot_fragment.parameters["sample_rate"]
