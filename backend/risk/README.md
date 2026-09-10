# Risk Assessment & Security Module

**Owner:** Member 5

## Purpose
This module acts as the final decision-making layer for the Voice Clone Defense system. It takes independent signals from the ML Engine and Heuristic Engine, evaluates them alongside audio quality metrics, and produces a final, explainable security recommendation.

## API Contract
Members 3 & 4 should format their outputs to match the `EvidenceInput` Pydantic model in `risk_models.py`. 
The final output to the frontend is governed by the `RiskAssessmentOutput` model.

## Risk Calculation
The current algorithm uses a weighted sum (Default: 60% ML, 40% Heuristic). 
*Note: These weights are initial placeholders and MUST be calibrated once Member 6 conducts testing on real evaluation data.*

## Categories
- **LOW:** (< 40 score) Normal procedures continue.
- **MEDIUM:** (40-69 score) Requires additional verification.
- **HIGH:** (70+ score) Strong AI presence; verify via secondary channel.
- **INSUFFICIENT_EVIDENCE:** Triggered if audio is too short or too noisy.

## Security Layer
The `security/` module ensures path traversal prevention, limits file sizes (10MB), validates MIME/extensions, and ensures secure deletion of temporary biometrics to comply with data privacy standards.