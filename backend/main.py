from fastapi import FastAPI

# This is the main FastAPI application.
app = FastAPI(title="Voice Clone Defense API")


@app.get("/health")
def health_check():
    """
    Checks whether the backend is running.
    """
    return {
        "status": "ok",
        "service": "voice-clone-defense-backend"
    }