from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


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
        files={"file": ("test.wav", b"fake audio data", "audio/wav")},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_analyze_rejects_invalid_extension():
    response = client.post(
        "/analyze",
        files={"file": ("test.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 400