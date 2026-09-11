import io
import math

import numpy as np
import soundfile as sf
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)

SAMPLE_RATE = 16000


def make_wav_bytes(duration_seconds=1.0, frequency_hz=220.0):
    samples = np.sin(
        2 * math.pi * frequency_hz
        * np.arange(int(SAMPLE_RATE * duration_seconds))
        / SAMPLE_RATE
    ).astype(np.float32)

    buffer = io.BytesIO()
    sf.write(buffer, samples, SAMPLE_RATE, format="WAV")
    return buffer.getvalue()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_upload_rejects_invalid_extension():
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 400


def test_upload_accepts_wav():
    response = client.post(
        "/upload",
        files={
            "file": (
                "test.wav",
                make_wav_bytes(),
                "audio/wav",
            )
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_analyze_rejects_invalid_extension():
    response = client.post(
        "/analyze",
        files={"file": ("test.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 400


def test_analyze_accepts_valid_wav():
    response = client.post(
        "/analyze",
        files={
            "file": (
                "test.wav",
                make_wav_bytes(),
                "audio/wav",
            )
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "success"
    assert body["filename"] == "test.wav"
    assert "features" in body
    assert "assessment" in body
    assert body["assessment"]["engine_status"] == "PENDING"
