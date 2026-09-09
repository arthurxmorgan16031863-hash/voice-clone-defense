from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from analysis.audio_analyzer import AudioLoadError, extract_features

# This is the main FastAPI application.
app = FastAPI(title="Voice Clone Defense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Maximum upload size: 25 MB
MAX_FILE_SIZE = 25 * 1024 * 1024

# Audio formats allowed for V1.
ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".flac",
}


@app.get("/health")
def health_check():
    """
    Checks whether the backend is running.
    """
    return {
        "status": "ok",
        "service": "voice-clone-defense-backend"
    }


@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """
    Receives an audio file and performs basic validation.
    """
    filename = file.filename or ""

    # Get the file extension.
    extension = ""
    if "." in filename:
        extension = "." + filename.rsplit(".", 1)[1].lower()

    # Check whether the file type is supported.
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format."
        )

    # Read the uploaded file.
    contents = await file.read()

    # Check whether the file is empty.
    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded audio file is empty."
        )

    # Check the file size.
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Audio file is too large. Maximum size is 25 MB."
        )

    return {
        "status": "success",
        "filename": filename,
        "message": "Audio file uploaded and basic validation passed."
    }


@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    """
    Receives an audio file, validates it, and extracts
    Stage 1 raw audio features.

    This endpoint does NOT determine whether the audio is
    human or AI-generated.
    """
    filename = file.filename or ""

    # Get the file extension.
    extension = ""
    if "." in filename:
        extension = "." + filename.rsplit(".", 1)[1].lower()

    # Check whether the file type is supported.
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format."
        )

    # Read the uploaded file.
    contents = await file.read()

    # Check whether the file is empty.
    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded audio file is empty."
        )

    # Check the file size.
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Audio file is too large. Maximum size is 25 MB."
        )

    # Save the uploaded audio temporarily.
    import tempfile
    import os

    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False
        ) as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name

        # Run the existing Stage 1 feature extractor.
        features = extract_features(temp_file_path)

    except AudioLoadError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    finally:
        if temp_file_path is not None and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return {
        "status": "success",
        "filename": filename,
        "features": features
    }