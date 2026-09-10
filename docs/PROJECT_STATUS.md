# Voice Clone Defense — Project Status

This document records the repository state at the time of documentation work. It is intentionally conservative: code currently present in the repository is separated from modules that are still being integrated.

## Implemented in the Repository

| Area | Current state |
|---|---|
| Frontend | React + TypeScript + Vite application with audio upload and analysis states |
| Backend | FastAPI application with `POST /api/v1/analyze` |
| Audio analysis | Raw feature extraction for duration, sample rate, pitch statistics, spectral flatness, and silence ratio |
| Upload validation | Extension/MIME allow-list checks, filename validation, and 25 MB size limit |
| Temporary-file handling | Generated temporary filenames and cleanup after processing |
| Risk engine | Risk calculation and `LOW`, `MEDIUM`, `HIGH`, `INSUFFICIENT_EVIDENCE` output model |
| Tests | Audio analyzer, risk engine, and integration/security tests are present |
| CI | GitHub Actions workflow runs backend dependency installation and the audio-analyzer test suite on pushes/PRs to `main` |
| Documentation rules | `CLAUDE.md` defines V1 scope, security rules, testing expectations, and development workflow |

## In Development / Integration Pending

- Real heuristic voice-cloning detection.
- Real ML-based synthetic-speech detection.
- Wiring real detector evidence into the risk engine through the existing evidence model.
- Final user-facing authenticity result based on the real detection pipeline.
- Final model-backed confidence and explanation behavior.

## Important Current Limitation

`backend/main.py` currently uses placeholder heuristic and ML values when constructing the risk-engine input. The risk engine itself is implemented, but its current API integration does not yet represent a real ML/heuristic detector result.

Similarly, `backend/analysis/audio_analyzer.py` is a feature extractor. Its measurements must not be interpreted as proof that audio is authentic or synthetic.

## Testing Status

The repository contains tests, but testing is still evolving with the project. The presence of a test file does not by itself mean the final V1 detector is validated.

When the real heuristic and ML modules are integrated, the team should add tests for:

- normal valid audio
- unsupported file types
- corrupted audio
- empty/invalid input
- short or insufficient audio
- large files
- detector outputs at boundary conditions
- risk-level transitions
- end-to-end API behavior using real detector evidence

## Documentation Maintenance

Update this file whenever a major module moves from planned/in-development to implemented. Keep the status factual and avoid adding unverified accuracy or benchmark claims.
