"""
test_audio_analyzer.py

Tests for backend/analysis/audio_analyzer.py.

Scope note: this file tests extract_features() as a raw feature
extractor. It does NOT test any authenticity/synthetic-speech
determination, because audio_analyzer.py does not produce one — that is
intentionally a separate, not-yet-built feature.

All audio fixtures used here are generated deterministically at test time
using numpy + soundfile. No external audio files are downloaded.

IMPORTANT LIMITATION — read before relying on this file as full coverage:
This project's testing rules call for coverage against "normal audio."
We do not have a genuine human speech recording available, and per
project instructions we are not downloading one automatically. The
"normal-ish audio" fixture below is a synthetic, frequency-varying
signal generated with numpy — it is useful for checking that the
extractor behaves sanely on non-silent, non-trivial audio (produces
finite numbers, correct duration, etc.), but it is NOT real speech and
must not be read as validating pitch-tracking accuracy on actual human
voices. A pure tone (constant single frequency) is kept as a strictly
separate, explicitly-labeled non-speech test case, per project
instructions — it is never used as a stand-in for speech.

If/when a genuine short speech recording becomes available, it should be
added as backend/tests/fixtures/sample_speech.wav and a dedicated test
added for it; that is out of scope for this file as currently written.

Run these tests from the `backend/` folder with the virtual environment
active:
    pytest
"""

import math

import numpy as np
import pytest
import soundfile as sf

from analysis.audio_analyzer import (
    extract_features,
    AudioLoadError,
    MINIMUM_RELIABLE_DURATION_SECONDS,
)


SAMPLE_RATE = 16000


# ---------------------------------------------------------------------
# Fixture generators
#
# Each of these writes a deterministic WAV file to a pytest-managed
# temporary directory (tmp_path) using numpy (to generate the samples)
# and soundfile (to write the WAV file) — no external audio is used.
# ---------------------------------------------------------------------

def _write_wav(path, samples: np.ndarray, sample_rate: int = SAMPLE_RATE):
    """Writes a mono float32 waveform to a WAV file using soundfile."""
    sf.write(path, samples.astype(np.float32), sample_rate)


@pytest.fixture
def silence_audio(tmp_path):
    """A 2-second file that is entirely digital silence (all zeros)."""
    duration_seconds = 2.0
    samples = np.zeros(int(SAMPLE_RATE * duration_seconds), dtype=np.float32)
    path = str(tmp_path / "silence.wav")
    _write_wav(path, samples)
    return path


@pytest.fixture
def tone_audio(tmp_path):
    """
    A 2-second pure 440Hz tone.

    This is a NON-SPEECH test case. It is intentionally simple and
    strictly non-varying in pitch, and must never be treated as a
    stand-in for real speech anywhere in this file.
    """
    duration_seconds = 2.0
    frequency_hz = 440.0
    t = np.arange(int(SAMPLE_RATE * duration_seconds)) / SAMPLE_RATE
    samples = 0.5 * np.sin(2 * math.pi * frequency_hz * t)
    path = str(tmp_path / "tone.wav")
    _write_wav(path, samples)
    return path


@pytest.fixture
def normal_ish_audio(tmp_path):
    """
    A 2-second SYNTHETIC signal with a frequency that varies over time
    (a linear chirp from 150Hz to 300Hz), used as a stand-in for
    "not silent, not a single fixed tone" audio.

    This is NOT real speech. It exists only to exercise the extractor on
    audio with changing pitch content, so we can sanity-check that
    duration/sample rate/silence/spectral-flatness values come back
    reasonable. It must not be used to assert speech-specific pitch
    accuracy — see the module docstring for why a real speech fixture is
    not included here.
    """
    duration_seconds = 2.0
    start_freq_hz = 150.0
    end_freq_hz = 300.0
    t = np.arange(int(SAMPLE_RATE * duration_seconds)) / SAMPLE_RATE
    # Linear chirp: instantaneous frequency moves from start to end.
    freq_sweep = start_freq_hz + (end_freq_hz - start_freq_hz) * (t / duration_seconds)
    samples = 0.5 * np.sin(2 * math.pi * freq_sweep * t)
    path = str(tmp_path / "normal_ish.wav")
    _write_wav(path, samples)
    return path


@pytest.fixture
def very_short_audio(tmp_path):
    """A 0.1-second tone — shorter than MINIMUM_RELIABLE_DURATION_SECONDS."""
    duration_seconds = 0.1
    frequency_hz = 440.0
    t = np.arange(int(SAMPLE_RATE * duration_seconds)) / SAMPLE_RATE
    samples = 0.5 * np.sin(2 * math.pi * frequency_hz * t)
    path = str(tmp_path / "very_short.wav")
    _write_wav(path, samples)
    return path


@pytest.fixture
def corrupted_audio(tmp_path):
    """A file with a .wav extension but content that is not valid audio."""
    path = str(tmp_path / "corrupted.wav")
    with open(path, "wb") as f:
        f.write(b"this is not a valid wav file at all")
    return path


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

def test_normal_ish_audio_returns_sane_values(normal_ish_audio):
    """
    Checks that a non-silent, non-trivial synthetic signal produces
    well-formed, finite measurements. This does NOT assert speech-like
    pitch behavior, since this fixture is not real speech (see module
    docstring).
    """
    result = extract_features(normal_ish_audio)

    assert result["duration_seconds"] == pytest.approx(2.0, abs=0.05)
    assert result["sample_rate"] == SAMPLE_RATE
    assert 0.0 <= result["silence_ratio"] <= 1.0
    assert math.isfinite(result["spectral_flatness_mean"])
    assert 0.0 <= result["spectral_flatness_mean"] <= 1.0
    assert result["insufficient_audio"] is False

    # Pitch is either None or a finite number — never NaN/inf, never a
    # fabricated placeholder.
    if result["pitch_mean_hz"] is not None:
        assert math.isfinite(result["pitch_mean_hz"])
    if result["pitch_variability"] is not None:
        assert math.isfinite(result["pitch_variability"])


def test_silence_does_not_fabricate_pitch(silence_audio):
    """Silence-only audio must report a high silence_ratio and no pitch."""
    result = extract_features(silence_audio)

    assert result["duration_seconds"] == pytest.approx(2.0, abs=0.05)
    assert result["sample_rate"] == SAMPLE_RATE
    assert result["silence_ratio"] > 0.99
    assert result["pitch_mean_hz"] is None
    assert result["pitch_variability"] is None
    assert result["insufficient_audio"] is False  # duration is fine; it's just silent
    assert len(result["notes"]) > 0  # should explain why pitch wasn't computed


def test_very_short_audio_is_flagged_and_skips_pitch(very_short_audio):
    """
    Audio shorter than MINIMUM_RELIABLE_DURATION_SECONDS must be flagged
    via insufficient_audio, and must not attempt pitch extraction.
    """
    result = extract_features(very_short_audio)

    assert result["duration_seconds"] < MINIMUM_RELIABLE_DURATION_SECONDS
    assert result["insufficient_audio"] is True
    assert result["pitch_mean_hz"] is None
    assert result["pitch_variability"] is None
    assert len(result["notes"]) > 0


def test_tone_is_non_speech_and_does_not_crash(tone_audio):
    """
    A pure tone is a NON-SPEECH test case. This test only checks that
    extraction completes and returns well-formed values — it makes no
    claim about speech-like behavior, since a tone is not speech.
    """
    result = extract_features(tone_audio)

    assert result["duration_seconds"] == pytest.approx(2.0, abs=0.05)
    assert result["sample_rate"] == SAMPLE_RATE
    assert 0.0 <= result["silence_ratio"] <= 1.0
    assert math.isfinite(result["spectral_flatness_mean"])
    assert result["insufficient_audio"] is False

    if result["pitch_mean_hz"] is not None:
        assert math.isfinite(result["pitch_mean_hz"])
    if result["pitch_variability"] is not None:
        assert math.isfinite(result["pitch_variability"])


def test_corrupted_audio_raises_audio_load_error(corrupted_audio):
    """
    A file that cannot be decoded as audio must raise AudioLoadError,
    not return fabricated/placeholder measurements.
    """
    with pytest.raises(AudioLoadError):
        extract_features(corrupted_audio)


def test_result_never_contains_authenticity_claims(normal_ish_audio):
    """
    Guards against scope creep: extract_features() must never return an
    authenticity label, verdict, confidence score, or risk score. This
    function is a feature extractor, not a voice-clone detector.
    """
    result = extract_features(normal_ish_audio)

    forbidden_keys = {
        "label",
        "verdict",
        "confidence",
        "confidence_score",
        "authenticity",
        "authenticity_score",
        "is_synthetic",
        "is_authentic",
        "risk_score",
    }
    assert forbidden_keys.isdisjoint(result.keys())


def test_result_has_exactly_the_expected_fields(silence_audio):
    """
    Confirms the result dict's keys match exactly what this stage is
    approved to return — nothing extra, nothing missing.
    """
    result = extract_features(silence_audio)

    expected_keys = {
        "duration_seconds",
        "sample_rate",
        "pitch_mean_hz",
        "pitch_variability",
        "spectral_flatness_mean",
        "silence_ratio",
        "insufficient_audio",
        "notes",
    }
    assert set(result.keys()) == expected_keys