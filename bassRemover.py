from pydub import AudioSegment
from pydub.scipy_effects import _mk_butter_filter
import os.path


# custom band cut filter
def band_cut_filter(seg, low_cutoff_freq, high_cutoff_freq, order=10):
    filter_fn = _mk_butter_filter([low_cutoff_freq, high_cutoff_freq], type='bandstop', order=order)
    return seg.apply_mono_filter_to_each_channel(filter_fn)


def remove_bass(audiofile):
    # Read in audio file and get the two mono tracks
    extension = os.path.splitext(audiofile.filename)[1]

    if extension == ".mp3":
        sound_stereo = AudioSegment.from_mp3(audiofile).apply_gain(-4)
    else:
        sound_stereo = AudioSegment.from_wav(audiofile).apply_gain(-4)

    sound_mono = sound_stereo.split_to_mono()
    sound_monoL = sound_mono[0]
    sound_monoR = sound_mono[1]

    # Invert phase of the Right audio file
    sound_monoR_inv = sound_monoR.invert_phase()

    # Filtering with high pass filter
    filtered_stereo = band_cut_filter(sound_stereo, 55, 310)
    # finished = filtered_stereo

    # Merge all three sound files together one on top of the other
    merged = sound_monoL.overlay(sound_monoR_inv)
    merged = merged.overlay(filtered_stereo)
    return merged
