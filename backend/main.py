from fastapi import FastAPI, UploadFile, File
from backend.security.file_security import validate_audio_file, save_temp_file_securely, securely_delete_file
from backend.risk.risk_engine import RiskEngine
from backend.risk.risk_models import EvidenceInput

app = FastAPI(title="Voice Clone Defense API")
risk_engine = RiskEngine()

@app.post("/api/v1/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    # 1. Security validation boundary
    validate_audio_file(file)
    
    # 2. Secure temp storage (Windows compatible)
    temp_path = save_temp_file_securely(file)
    
    try:
        # Placeholder stubs for Members 3 & 4 (until their engines plug in)
        mock_heuristic_score = 0.1
        mock_ml_probability = 0.15
        mock_audio_quality = 0.95
        
        evidence = EvidenceInput(
            heuristic_score=mock_heuristic_score,
            ml_probability=mock_ml_probability,
            audio_quality_score=mock_audio_quality,
            insufficient_audio=False
        )
        
        # 3. Run Risk Assessment Engine
        assessment = risk_engine.assess_risk(evidence)
        
        return {
            "filename": file.filename,
            "assessment": assessment.model_dump()
        }
        
    finally:
        # 4. Privacy enforcement: Securely delete biometric file
        securely_delete_file(temp_path)