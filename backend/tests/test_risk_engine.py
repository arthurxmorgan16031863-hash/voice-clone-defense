import pytest

try:
    from backend.risk.risk_models import EvidenceInput
    from backend.risk.risk_engine import RiskEngine
except ModuleNotFoundError:  # pragma: no cover - supports running tests from backend/
    from risk.risk_models import EvidenceInput
    from risk.risk_engine import RiskEngine

@pytest.fixture
def engine():
    return RiskEngine()

def test_insufficient_evidence(engine):
    evidence = EvidenceInput(
        heuristic_score=0.9, ml_probability=0.9, 
        audio_quality_score=0.1, insufficient_audio=True
    )
    result = engine.assess_risk(evidence)
    assert result.risk_level == "INSUFFICIENT_EVIDENCE"
    assert result.risk_score == 0.0

def test_high_risk(engine):
    evidence = EvidenceInput(
        heuristic_score=0.8, ml_probability=0.9, 
        audio_quality_score=0.9, insufficient_audio=False
    )
    result = engine.assess_risk(evidence)
    assert result.risk_level == "HIGH"
    assert result.risk_score > 70.0

def test_low_risk(engine):
    evidence = EvidenceInput(
        heuristic_score=0.1, ml_probability=0.1, 
        audio_quality_score=0.95, insufficient_audio=False
    )
    result = engine.assess_risk(evidence)
    assert result.risk_level == "LOW"
    assert result.risk_score < 40.0