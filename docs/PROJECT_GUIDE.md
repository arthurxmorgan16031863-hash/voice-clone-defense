# Voice Clone Defense — Project Guide

## 1. Project Overview

Voice Clone Defense is a backend and frontend project for detecting and preventing voice-cloning impersonation attacks.

The project is being developed in stages. The current backend provides audio upload validation and audio feature extraction. Heuristic detection, ML detection, and risk-analysis components are being developed separately.

Do not assume that an audio file is AI-generated or authentic unless the corresponding detection modules are actually implemented and integrated.

---

## 2. Project Architecture

### Frontend
- React
- TypeScript
- Vite
- Provides the user interface for interacting with the system.

### Backend
- Python
- FastAPI
- Audio processing using the project's analysis modules.
- Provides API endpoints for health checking, file upload, and audio analysis.

### Detection Pipeline

The planned detection flow is:

1. User uploads an audio file.
2. Backend validates the file.
3. Audio features are extracted.
4. Heuristic detection can analyse relevant audio characteristics.
5. ML detection can provide a model-based assessment.
6. Risk engine can combine available evidence.
7. Frontend displays the result.

The heuristic, ML, and risk components should only be treated as complete when their actual implementations are integrated and tested.

---

## 3. Backend Setup

### Requirements

- Python 3.12
- Git
- VS Code

Backend dependencies are installed from:

`backend/requirements.txt`

### Create Virtual Environment

From the repository root:

```powershell
cd backend
py -3.12 -m venv venv