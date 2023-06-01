import os
import shutil

import audioflux as af
import librosa
import matplotlib.pyplot as plt
import matplotlib.transforms as mpt
import numpy as np
import soundfile as sf
from audioflux.display import fill_spec
from audioflux.type import SpectralFilterBankScaleType

from model.fragment import ParrotFragment


class ParrotContainer:
    def __init__(self, name, file_name):
        self.bft_obj = None
        self.spec_arr = None
        self.beat_times = None
        self.subseg_t = None
        self.audio_arr = None
        self.sr = None
        self.bound_times = None

        self.name = name
        self.file_name = file_name
        self.fragments = []
        self.fragment_ids = 0
        self.container_output_dir = f"output/{self.name}/"

    def add_fragment(self, audio_arr, name):
        fragment = ParrotFragment(self.fragment_ids, audio_arr / np.max(audio_arr), name, self.sr, self.name)
        self.fragments.append(fragment)
        self.fragment_ids += 1
        fragment.calculate_parameters()

    def write_fragments(self):
        list_fragments = self.fragments
        for f in list_fragments:
            fragment_file_name = f.parameters["file_name"]
            self.write_audio(f.data, fragment_file_name)
            with open(f"{self.container_output_dir}/{fragment_file_name}.json", "w") as file:
                file.write(f.as_json())

    def write_audio(self, audio_arr, split_file_name):
        os.makedirs(self.container_output_dir, exist_ok=True)
        sf.write(f"output/{self.name}/{split_file_name}.wav", audio_arr, self.sr)

    def clear(self):
        shutil.rmtree(f"output/{self.file_name}/", ignore_errors=True)

    def fragment(self):
        self.audio_arr, self.sr = librosa.load(self.file_name)
        # Create BFT object and extract mel spectrogram
        self.bft_obj = af.BFT(num=128, radix2_exp=12, samplate=int(self.sr),
                              scale_type=SpectralFilterBankScaleType.MEL)

        spec_arr = self.bft_obj.bft(self.audio_arr)
        spec_arr = np.abs(spec_arr)

        # Beat finding
        tempo, beats = librosa.beat.beat_track(y=self.audio_arr, sr=self.sr, hop_length=512)
        self.beat_times = librosa.frames_to_time(beats, sr=self.sr, hop_length=512)
        cqt = np.abs(librosa.cqt(self.audio_arr, sr=self.sr, hop_length=512))
        subseg = librosa.segment.subsegment(cqt, beats, n_segments=2)
        self.subseg_t = librosa.frames_to_time(subseg, sr=self.sr, hop_length=512)

        chroma = librosa.feature.chroma_cqt(y=self.audio_arr, sr=self.sr)
        bounds = librosa.segment.agglomerative(chroma, 800)
        self.bound_times = librosa.frames_to_time(bounds, sr=self.sr)

        self.clear()
        for bound in range(0, len(self.bound_times) - 1):
            b = int(self.bound_times[bound] * self.sr)
            e = int(self.bound_times[bound + 1] * self.sr)
            text = f"split_{b:016d}_{e:016d}"
            self.add_fragment(self.audio_arr[b:e], text)

        self.write_fragments()

    def graph(self):
        """Stored here for now"""
        # Display spectrogram
        audio_len = self.audio_arr.shape[-1]
        # set plot width to 1024px and height to 768px
        plt.rcParams["figure.figsize"] = (10.24, 7.68)
        fig, ax = plt.subplots()

        img = fill_spec(self.spec_arr, axes=ax,
                        x_coords=self.bft_obj.x_coords(audio_len),
                        y_coords=self.bft_obj.y_coords(),
                        x_axis='time', y_axis='log',
                        title='Mel Spectrogram')
        trans = mpt.blended_transform_factory(
            ax.transData, ax.transAxes)
        ax.vlines(self.bound_times, 0, 1, color='linen', linestyle='--',
                  linewidth=2, alpha=0.9, label='Segment boundaries',
                  transform=trans)
        lims = ax.get_ylim()
        ax.vlines(self.beat_times, lims[0], lims[1], color='lime', alpha=0.9,
                  linewidth=2, label='Beats')
        ax.vlines(self.subseg_t, lims[0], lims[1], color='linen', linestyle='--',
                  linewidth=1.5, alpha=0.5, label='Sub-beats')
        ax.legend()
        fig.colorbar(img, ax=ax)
        plt.show()
