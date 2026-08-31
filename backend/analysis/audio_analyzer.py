"""
audio_analyzer.py

Stage 1 audio feature extraction for Voice Clone Defense (SIH V1).

This module extracts raw, measurable properties of an audio file. It does
NOT determine whether audio is authentic or synthetic. There is no
authenticity label, verdict, or confidence score produced anywhere in this
file. This is a feature extractor, not a voice-clone detector.

Interpretation of these measurements belongs to a separate, later
heuristic-scoring feature, which has not been implemented yet.

Approved dependencies only: librosa, soundfile, numpy.
"""

from dataclasses import dataclass, asdict
from typing import Optional

import numpy as np
import librosa
from librosa.util.exceptions import ParameterError
import soundfile as sf


# Minimum duration (seconds) below which pitch analysis is considered
# unreliable. Below this, pitch extraction is not attempted at all.
MINIMUM_RELIABLE_DURATION_SECONDS = 0.5

# Amplitude threshold (relative to the clip's own peak amplitude) below
# which a sample is counted as "silent" when computing silence_ratio.
SILENCE_AMPLITUDE_THRESHOLD_RATIO = 0.02

# A clip whose silence_ratio is at or above this value is treated as
# effectively silent for the purposes of skipping pitch analysis.
EFFECTIVELY_SILENT_RATIO_THRESHOLD = 0.99


class AudioLoadError(Exception):
    """Raised when a file cannot be read/decoded as audio at all."""
    pass


@dataclass
class AudioFeatures:
    """
    Raw audio measurements only. This is NOT an authenticity verdict,
    label, or confidence score.

    duration_seconds:
        Length of the audio in seconds.

    sample_rate:
        Number of audio samples per second (Hz), as read from the file.

    pitch_mean_hz:
        Average detected pitch (fundamental frequency, F0) across the
        voiced parts of the clip, in Hertz. None if no reliable pitch
        could be measured (e.g. silence, non-tonal audio, or a clip too
        short to analyze).

    pitch_variability:
        Standard deviation of the detected pitch across the voiced parts
        of the clip, in Hertz. Higher values mean the pitch moved around
        more; lower values mean it stayed flatter. None under the same
        conditions as pitch_mean_hz.

    spectral_flatness_mean:
        Average spectral flatness of the clip (0.0-1.0). This measures
        how "noise-like" vs. "tone-like" the sound's frequency content is
        — values near 1.0 are closer to flat/noise-like spectra, values
        near 0.0 are closer to peaky/tonal spectra. This is a raw
        signal-processing measurement, not an indicator of authenticity
        by itself.

    silence_ratio:
        Proportion (0.0-1.0) of the clip that is at or below a small
        amplitude threshold, i.e. how much of the clip is effectively
        silent.

    insufficient_audio:
        True if the clip is too short (below
        MINIMUM_RELIABLE_DURATION_SECONDS) for pitch analysis to be
        considered reliable.

    notes:
        Plain-language notes explaining any fields that could not be
        computed and why.
    """
    duration_seconds: float
    sample_rate: int
    pitch_mean_hz: Optional[float]
    pitch_variability: Optional[float]
    spectral_flatness_mean: float
    silence_ratio: float
    insufficient_audio: bool
    notes: list


def _load_audio(file_path: str):
    """
    Loads an audio file and converts it to a mono waveform.

    Returns:
        (waveform, sample_rate) as (numpy array of float32, int)

    Raises:
        AudioLoadError if the file cannot be read/decoded as audio.

    Note on exception handling: we catch RuntimeError, ValueError, and
    soundfile.LibsndfileError specifically, since these are the exception
    types soundfile is documented to raise for unreadable/corrupted/
    invalid audio data. We deliberately do NOT catch a bare Exception
    here, so that an unrelated programming bug (e.g. a typo causing an
    AttributeError) surfaces normally instead of being silently
    reinterpreted as "corrupted audio."
    """
    try:
        waveform, sample_rate = sf.read(file_path, always_2d=False)
    except (RuntimeError, ValueError, sf.LibsndfileError) as exc:
        raise AudioLoadError(f"Could not read audio file: {exc}") from exc

    # If the file has more than one channel (e.g. stereo), average the
    # channels together to get a single mono waveform. Mono is simpler
    # and sufficient for the measurements we compute here.
    if waveform.ndim > 1:
        waveform = np.mean(waveform, axis=1)

    waveform = waveform.astype(np.float32)
    return waveform, sample_rate


def _compute_duration(waveform: np.ndarray, sample_rate: int) -> float:
    """Returns the duration of the waveform in seconds."""
    if sample_rate <= 0:
        return 0.0
    return len(waveform) / float(sample_rate)


def _compute_silence_ratio(waveform: np.ndarray) -> float:
    """
    Returns the proportion (0.0-1.0) of samples whose absolute amplitude
    is below a small threshold relative to the clip's own peak amplitude.
    A fully silent (all-zero) clip returns 1.0.
    """
    if len(waveform) == 0:
        return 1.0

    peak = np.max(np.abs(waveform))
    if peak == 0.0:
        return 1.0  # The entire clip is digital silence.

    threshold = peak * SILENCE_AMPLITUDE_THRESHOLD_RATIO
    silent_sample_count = np.sum(np.abs(waveform) < threshold)
    return float(silent_sample_count) / float(len(waveform))


def _compute_spectral_flatness(waveform: np.ndarray) -> float:
    """
    Returns the mean spectral flatness of the waveform using librosa.
    See the AudioFeatures docstring for what this measurement means.
    """
    if len(waveform) == 0:
        return 0.0

    flatness_over_time = librosa.feature.spectral_flatness(y=waveform)
    return float(np.mean(flatness_over_time))


def _compute_pitch_stats(waveform: np.ndarray, sample_rate: int):
    """
    Estimates pitch (F0) over time using librosa's pyin pitch tracker,
    then returns the mean and standard deviation of the pitch across the
    voiced (non-silent, tonal) portions of the clip.

    This function assumes the caller has already confirmed the audio
    meets MINIMUM_RELIABLE_DURATION_SECONDS. As a defensive safeguard
    (in case this function is ever called directly, e.g. from a test),
    it re-checks duration itself and refuses to run pitch extraction on
    audio that's too short, since librosa.pyin can behave unreliably or
    raise errors on very short input.

    Returns:
        (pitch_mean_hz, pitch_variability) as (float, float), or
        (None, None) if no reliable voiced pitch could be found, or if
        the audio is too short to analyze.

    Note on exception handling: we catch ValueError and librosa's
    ParameterError specifically, since these are the documented cases
    where librosa.pyin rejects input it cannot process (e.g. malformed
    parameters relative to signal length). We do NOT catch a bare
    Exception here, so unrelated programming bugs are not hidden.
    """
    duration_seconds = _compute_duration(waveform, sample_rate)
    if duration_seconds < MINIMUM_RELIABLE_DURATION_SECONDS:
        return None, None

    try:
        f0, _voiced_flag, _voiced_probability = librosa.pyin(
            waveform,
            fmin=librosa.note_to_hz("C2"),
            fmax=librosa.note_to_hz("C7"),
            sr=sample_rate,
        )
    except (ValueError, ParameterError):
        # librosa could not process this signal for pitch tracking
        # (e.g. still too short relative to its internal frame/window
        # requirements despite passing our duration check above).
        return None, None

    if f0 is None:
        return None, None

    # pyin marks unvoiced frames as NaN; keep only the voiced ones.
    voiced_f0_values = f0[~np.isnan(f0)]
    if len(voiced_f0_values) == 0:
        return None, None

    return float(np.mean(voiced_f0_values)), float(np.std(voiced_f0_values))


def extract_features(file_path: str) -> dict:
    """
    Extracts raw Stage 1 audio features from an audio file.

    IMPORTANT: This function is a feature extractor, not a voice-clone
    detector. It returns raw measurements only — duration, sample rate,
    pitch statistics, spectral flatness, and silence ratio. It does NOT
    determine or claim whether the audio is authentic or synthetic, and
    it does NOT produce any label, verdict, or confidence score.

    Args:
        file_path: Path to an audio file that has already passed upload
            validation (format/size checks are assumed to have happened
            before this function is called).

    Returns:
        A dict matching the AudioFeatures fields (see that class's
        docstring for what each field means).

    Raises:
        AudioLoadError if the file cannot be decoded as audio at all
        (e.g. it is corrupted or not actually audio data).
    """
    waveform, sample_rate = _load_audio(file_path)

    notes = []
    duration_seconds = _compute_duration(waveform, sample_rate)
    silence_ratio = _compute_silence_ratio(waveform)
    spectral_flatness_mean = _compute_spectral_flatness(waveform)

    insufficient_audio = duration_seconds < MINIMUM_RELIABLE_DURATION_SECONDS

    # Pitch extraction is only ever attempted when the audio is long
    # enough AND not effectively silent. This check happens BEFORE
    # _compute_pitch_stats is called, in addition to that function's own
    # internal safeguard, per the requirement to avoid calling
    # librosa.pyin on unreliable input.
    if insufficient_audio:
        notes.append(
            f"Audio duration ({duration_seconds:.2f}s) is below the "
            f"minimum reliable duration "
            f"({MINIMUM_RELIABLE_DURATION_SECONDS}s); pitch statistics "
            f"were not computed."
        )
        pitch_mean_hz, pitch_variability = None, None

    elif silence_ratio >= EFFECTIVELY_SILENT_RATIO_THRESHOLD:
        notes.append(
            "Audio is effectively silent; pitch statistics are not "
            "meaningful and were not computed."
        )
        pitch_mean_hz, pitch_variability = None, None

    else:
        pitch_mean_hz, pitch_variability = _compute_pitch_stats(
            waveform, sample_rate
        )
        if pitch_mean_hz is None:
            notes.append(
                "No reliable pitch could be detected in this audio "
                "(for example, non-tonal or non-speech content)."
            )

    features = AudioFeatures(
        duration_seconds=duration_seconds,
        sample_rate=sample_rate,
        pitch_mean_hz=pitch_mean_hz,
        pitch_variability=pitch_variability,
        spectral_flatness_mean=spectral_flatness_mean,
        silence_ratio=silence_ratio,
        insufficient_audio=insufficient_audio,
        notes=notes,
    )

    return asdict(features)