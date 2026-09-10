from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Import Member 5's Security & Risk Modules
from backend.security.file_security import validate_audio_file, save_temp_file_securely, securely_delete_file
from backend.risk.risk_engine import RiskEngine
from backend.risk.risk_models import EvidenceInput

# Import existing audio analyzer
from backend.analysis.audio_analyzer import extract_features

app = FastAPI(title="Voice Clone Defense API")
risk_engine = RiskEngine()

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
    validate_audio_file(file)
    return {"status": "success", "message": "File uploaded and validated successfully."}

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    # 1. Security validation boundary
    validate_audio_file(file)
    
    # 2. Secure temp storage (Windows compatible)
    temp_path = save_temp_file_securely(file)
    
    try:
        # 3. Preserve existing audio analysis (DO NOT BYPASS)
        features = extract_features(str(temp_path))
        
        # 4. Integration Placeholder for Members 3 & 4
        # We are NOT fabricating ML/Heuristic scores here. 
        # Using Option B to communicate the pending integration state.
        assessment_placeholder = {
            "risk_score": None,
            "risk_level": "PENDING_ENGINES",
            "confidence": features.get("audio_quality_score", 0.0) if features else 0.0,
            "reasons": ["Awaiting integration of ML and Heuristic detection engines."],
            "recommendation": "Detection engines pending. Review raw audio features."
        }
        
        # 5. Maintain the exact expected response contract for the frontend
        return {
            "status": "success",
            "filename": file.filename,
            "features": features,
            "assessment": assessment_placeholder
        }
        
    finally:
        # 6. Privacy enforcement: Securely delete biometric file
        securely_delete_file(temp_path)