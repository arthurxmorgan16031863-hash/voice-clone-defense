import pytest
from fastapi.testclient import TestClient
from fastapi import UploadFile, HTTPException
from io import BytesIO
from backend.main import app
from backend.security.file_security import save_temp_file_securely

client = TestClient(app)

def test_file_size_boundary_25mb():
    # Test that a file exceeding 25MB raises HTTP 413
    large_stream = BytesIO(b"0" * (26 * 1024 * 1024))
    large_file = UploadFile(filename="huge.wav", file=large_stream)

    
    with pytest.raises(HTTPException) as exc:
        save_temp_file_securely(large_file)
    assert exc.value.status_code == 413

def test_security_and_risk_integration_flow():
    # Test an allowed audio file upload through the FastAPI endpoint
    audio_content = b"RIFF....WAVEfmt ..."
    response = client.post(
        "/api/v1/analyze",
        files={"file": ("test_sample.wav", audio_content, "audio/wav")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "assessment" in data
    assert data["assessment"]["risk_level"] == "LOW"