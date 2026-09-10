import os
import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException

# Security Constants
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
ALLOWED_MIME_TYPES = {"audio/wav", "audio/mpeg", "audio/flac", "audio/ogg", "audio/mp4"}

def validate_audio_file(file: UploadFile) -> None:
    """
    Validates the uploaded file for security threats (size, type, path traversal).
    Raises HTTPException if validation fails.
    """
    # 1. Check file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file extension. Allowed: {ALLOWED_EXTENSIONS}")
    
    # 2. Check MIME type (Basic check, can be spoofed but adds a layer)
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid MIME type.")

    # 3. Path Traversal Prevention (ensure filename doesn't contain ../)
    safe_filename = os.path.basename(file.filename)
    if safe_filename != file.filename:
        raise HTTPException(status_code=400, detail="Invalid filename format.")

def save_temp_file_securely(file: UploadFile, temp_dir: str = "/tmp/voice_defense") -> Path:
    """
    Saves the file with a random UUID to prevent naming collisions and arbitrary code execution.
    """
    os.makedirs(temp_dir, exist_ok=True)
    
    ext = Path(file.filename).suffix.lower()
    safe_name = f"{uuid.uuid4()}{ext}"
    file_path = Path(temp_dir) / safe_name

    # Check file size while reading
    size = 0
    with open(file_path, "wb") as buffer:
        while chunk := file.file.read(8192):
            size += len(chunk)
            if size > MAX_FILE_SIZE_BYTES:
                buffer.close()
                os.remove(file_path)
                raise HTTPException(status_code=413, detail="File too large. Max size is 10MB.")
            buffer.write(chunk)
            
    file.file.seek(0) # Reset pointer
    return file_path

def securely_delete_file(file_path: Path) -> None:
    """
    Ensures the audio file is deleted to protect biometric privacy.
    """
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        # In a real app, log this securely. 
        pass