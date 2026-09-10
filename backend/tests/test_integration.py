import pytest
from fastapi.testclient import TestClient
from fastapi import UploadFile, HTTPException
from io import BytesIO
from unittest.mock import patch
import tempfile
from pathlib import Path

from backend.main import app
from backend.security.file_security import save_temp_file_securely

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "voice-clone-defense-backend"}

def test_file_size_boundary_25mb():
    # Test that a file exceeding 25MB raises HTTP 413
    large_stream = BytesIO(b"0" * (26 * 1024 * 1024))
    large_file = UploadFile(filename="huge.wav", file=large_stream)
    
    with pytest.raises(HTTPException) as exc:
        save_temp_file_securely(large_file)
    assert exc.value.status_code == 413

@patch("backend.main.extract_features")
def test_security_and_risk_integration_flow(mock_extract):
    mock_extract.return_value = {"duration_seconds": 5.0}
    
    audio_content = b"RIFF....WAVEfmt ..."
    response = client.post(
        "/analyze",
        files={"file": ("test_sample.wav", audio_content, "audio/wav")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "assessment" in data
    
    # Verify separated engine status and null values
    assert data["assessment"]["engine_status"] == "PENDING"
    assert data["assessment"]["risk_level"] is None
    assert data["assessment"]["confidence"] is None

@patch("backend.security.file_security.uuid.uuid4")
@patch("backend.main.extract_features")
def test_temp_file_cleanup_on_success(mock_extract, mock_uuid):
    # Mock the UUID so we know exactly what path to check
    mock_uuid.return_value = "1234-test-success"
    mock_extract.return_value = {"duration_seconds": 5.0}
    
    audio_content = b"RIFF....WAVEfmt ..."
    client.post(
        "/analyze",
        files={"file": ("test_sample.wav", audio_content, "audio/wav")}
    )
    
    expected_path = Path(tempfile.gettempdir()) / "voice_defense" / "1234-test-success.wav"
    assert not expected_path.exists()

@patch("backend.security.file_security.uuid.uuid4")
@patch("backend.main.extract_features")
def test_temp_file_cleanup_on_exception(mock_extract, mock_uuid):
    mock_uuid.return_value = "5678-test-fail"
    mock_extract.side_effect = Exception("Simulated extraction failure")
    
    audio_content = b"RIFF....WAVEfmt ..."
    
    with pytest.raises(Exception, match="Simulated extraction failure"):
        client.post(
            "/analyze",
            files={"file": ("test_sample.wav", audio_content, "audio/wav")}
        )
    
    expected_path = Path(tempfile.gettempdir()) / "voice_defense" / "5678-test-fail.wav"
    assert not expected_path.exists()