import pytest
from fastapi.testclient import TestClient
from fastapi import UploadFile, HTTPException
from io import BytesIO
from unittest.mock import patch
from backend.main import app
from backend.security.file_security import save_temp_file_securely

client = TestClient(app)

def test_health_check():
    # Verify the health endpoint was preserved
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
    # We use @patch to mock the audio analyzer in this isolated test
    # so it doesn't crash when we send fake "RIFF" bytes.
    mock_extract.return_value = {"audio_quality_score": 0.85, "duration_seconds": 5.0}
    
    audio_content = b"RIFF....WAVEfmt ..."
    
    # Send to the restored /analyze endpoint (not /api/v1/analyze)
    response = client.post(
        "/analyze",
        files={"file": ("test_sample.wav", audio_content, "audio/wav")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "assessment" in data
    
    # Verify it correctly shows PENDING_ENGINES instead of fabricating a LOW score
    assert data["assessment"]["risk_level"] == "PENDING_ENGINES"
    assert data["assessment"]["confidence"] == 0.85