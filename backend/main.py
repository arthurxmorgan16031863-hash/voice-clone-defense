from fastapi import FastAPI, File, UploadFile, HTTPException


# This is the main FastAPI application.
app = FastAPI(title="Voice Clone Defense API")


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

    # Get the file extension.
    filename = file.filename or ""
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