from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Import Member 5's Security Modules
from backend.security.file_security import validate_audio_file, save_temp_file_securely, securely_delete_file

# Import existing audio analyzer
from backend.analysis.audio_analyzer import extract_features

app = FastAPI(title="Voice Clone Defense API")

# Preserve existing CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "voice-clone-defense-backend"}

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    # Enforce full validation, including the 25MB stream limit
    validate_audio_file(file)
    temp_path = save_temp_file_securely(file)
    
    # Immediately delete since this endpoint is just for validation/upload checks
    securely_delete_file(temp_path)
    
    return {"status": "success", "message": "File uploaded and validated successfully."}

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    # 1. Security validation boundary
    validate_audio_file(file)
    
    # 2. Secure temp storage (Windows compatible, 25MB limit)
    temp_path = save_temp_file_securely(file)
    
    try:
        # 3. Preserve existing audio analysis
        features = extract_features(str(temp_path))
        
        # 4. Integration Placeholder for Members 3 & 4
        assessment_placeholder = {
            "engine_status": "PENDING",
            "risk_score": None,
            "risk_level": None,
            "confidence": None,
            "reasons": ["Awaiting integration of ML and Heuristic detection engines."],
            "recommendation": "Detection engines pending. Review raw audio features."
        }
        
        return {
            "status": "success",
            "filename": file.filename,
            "features": features,
            "assessment": assessment_placeholder
        }
        
    finally:
        # 5. Privacy enforcement: Securely delete biometric file
        securely_delete_file(temp_path)