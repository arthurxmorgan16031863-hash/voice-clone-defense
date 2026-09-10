import os
import uuid
import tempfile
from pathlib import Path
from fastapi import UploadFile, HTTPException

# Updated Security Constants: 25 MB Limit
MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
ALLOWED_MIME_TYPES = {"audio/wav", "audio/mpeg", "audio/flac", "audio/ogg", "audio/mp4", "audio/x-m4a"}

def validate_audio_file(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename provided.")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file extension. Allowed: {ALLOWED_EXTENSIONS}")
    
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid MIME type: {file.content_type}")

    safe_filename = os.path.basename(file.filename)
    if safe_filename != file.filename:
        raise HTTPException(status_code=400, detail="Invalid filename format.")

def save_temp_file_securely(file: UploadFile) -> Path:
    # Windows-compatible temporary directory
    temp_dir = Path(tempfile.gettempdir()) / "voice_defense"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    ext = Path(file.filename).suffix.lower() if file.filename else ".wav"
    safe_name = f"{uuid.uuid4()}{ext}"
    file_path = temp_dir / safe_name

    size = 0
    with open(file_path, "wb") as buffer:
        while chunk := file.file.read(8192):
            size += len(chunk)
            if size > MAX_FILE_SIZE_BYTES:
                buffer.close()
                if file_path.exists():
                    file_path.unlink()
                raise HTTPException(status_code=413, detail="File too large. Max size is 25MB.")
            buffer.write(chunk)
            
    file.file.seek(0)
    return file_path

def securely_delete_file(file_path: Path) -> None:
    try:
        if file_path and Path(file_path).exists():
            Path(file_path).unlink()
    except Exception:
        pass