import audioflux as af
import librosa
import numpy as np
import matplotlib.transforms as mpt
from audioflux.type import SpectralFilterBankScaleType

from container import ParrotContainer

print("Loading example")
#librosa.ex(
example_name = "db.mp3"
#example_name = "pb.mp3"
#example_name = "mb.mp3"
audio_arr, sr = librosa.load(example_name)


print("Spectrogram")
# Create BFT object and extract mel spectrogram
bft_obj = af.BFT(num=128, radix2_exp=12, samplate=int(sr),
                 scale_type=SpectralFilterBankScaleType.MEL)

spec_arr = bft_obj.bft(audio_arr)
spec_arr = np.abs(spec_arr)

print("Beat finding")
# Beat finding
tempo, beats = librosa.beat.beat_track(y=audio_arr, sr=sr, hop_length=512)
beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=512)
cqt = np.abs(librosa.cqt(audio_arr, sr=sr, hop_length=512))
subseg = librosa.segment.subsegment(cqt, beats, n_segments=2)
subseg_t = librosa.frames_to_time(subseg, sr=sr, hop_length=512)

print("Chroma CQT")
# Split
chroma = librosa.feature.chroma_cqt(y=audio_arr, sr=sr)
bounds = librosa.segment.agglomerative(chroma, 800)
bound_times = librosa.frames_to_time(bounds, sr=sr)

print("Writing splits")
pc = ParrotContainer("test", sr)
pc.clear()
for bound in range(0, len(bound_times)-1):
    b = int(bound_times[bound]*sr)
    e = int(bound_times[bound+1]*sr)
    text = f"split_{b:016d}_{e:016d}"
    pc.add_fragment(audio_arr[b:e], text)

pc.write_fragments()
print("Generate graph")

# Display spectrogram

import matplotlib.pyplot as plt
from audioflux.display import fill_spec

audio_len = audio_arr.shape[-1]
# set plot width to 1024px and height to 768px
plt.rcParams["figure.figsize"] = (10.24, 7.68)
fig, ax = plt.subplots()

img = fill_spec(spec_arr, axes=ax,
                x_coords=bft_obj.x_coords(audio_len),
                y_coords=bft_obj.y_coords(),
                x_axis='time', y_axis='log',
                title='Mel Spectrogram')
trans = mpt.blended_transform_factory(
    ax.transData, ax.transAxes)
ax.vlines(bound_times, 0, 1, color='linen', linestyle='--',
          linewidth=2, alpha=0.9, label='Segment boundaries',
          transform=trans)
lims = ax.get_ylim()
ax.vlines(beat_times, lims[0], lims[1], color='lime', alpha=0.9,
           linewidth=2, label='Beats')
ax.vlines(subseg_t, lims[0], lims[1], color='linen', linestyle='--',
           linewidth=1.5, alpha=0.5, label='Sub-beats')
ax.legend()
fig.colorbar(img, ax=ax)
plt.show()
