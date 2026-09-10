from backend.risk.risk_models import EvidenceInput, RiskAssessmentOutput

class RiskEngine:
    def __init__(self, ml_weight: float = 0.6, heuristic_weight: float = 0.4):
        """
        Weights can be configured based on model evaluation data later.
        """
        self.ml_weight = ml_weight
        self.heuristic_weight = heuristic_weight

    def assess_risk(self, evidence: EvidenceInput) -> RiskAssessmentOutput:
        # 1. Handle Insufficient Evidence
        if evidence.insufficient_audio or evidence.audio_quality_score < 0.2:
            return RiskAssessmentOutput(
                risk_score=0.0,
                risk_level="INSUFFICIENT_EVIDENCE",
                confidence=0.0,
                reasons=["Audio quality or duration is insufficient for reliable assessment."],
                recommendation="Audio quality or duration is insufficient for reliable assessment. Request a clearer recording."
            )

        # 2. Calculate combined Risk Score (out of 100)
        base_score = (evidence.ml_probability * self.ml_weight) + (evidence.heuristic_score * self.heuristic_weight)
        risk_score = round(base_score * 100, 2)

        # 3. Determine Risk Level
        if risk_score >= 70:
            risk_level = "HIGH"
            recommendation = "High-risk indicators detected. Verify the caller through a trusted channel before authorizing sensitive actions."
        elif risk_score >= 40:
            risk_level = "MEDIUM"
            recommendation = "Potential anomaly detected. Perform additional verification."
        else:
            risk_level = "LOW"
            recommendation = "Audio appears low risk. Normal verification procedures may continue."

        # 4. Generate Explainable Reasons
        reasons = []
        if evidence.ml_probability >= 0.7:
            reasons.append("ML detector reported high synthetic-speech probability.")
        if evidence.heuristic_score >= 0.7:
            reasons.append("Heuristic analysis detected multiple signal-level anomalies.")
        
        # Append specific evidence from other modules if provided
        reasons.extend(evidence.ml_evidence)
        reasons.extend(evidence.heuristic_evidence)

        if not reasons and risk_level == "LOW":
            reasons.append("No significant anomalies detected in ML or Heuristic analysis.")

        # 5. Clarified Confidence Calculation:
        # Confidence reflects the reliability of the evidence based on acoustic quality.
        # It scales directly with audio_quality_score.
        confidence = round(evidence.audio_quality_score, 2)

        return RiskAssessmentOutput(
            risk_score=risk_score,
            risk_level=risk_level,
            confidence=confidence,
            reasons=reasons,
            recommendation=recommendation
        )