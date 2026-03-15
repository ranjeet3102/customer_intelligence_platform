System Architecture

Data Sources
      │
      ▼
Ingestion Pipeline
      │
      ▼
Data Validation & Profiling
      │
      ▼
Feature Engineering Pipeline
      │
      ▼
Feature Store
      │
      ▼
Model Training Pipeline
      │
      ▼
Model Registry
      │
      ▼
Batch Inference Pipeline
      │
      ▼
CLV Engine
      │
      ▼
Customer Segmentation
      │
      ▼
Retention Decision Engine
      │
      ▼
Prediction Store
      │
      ▼
Dashboard / Reporting


==========================================================================
# CIP Backend

The backend service for the Customer Intelligence Platform, built with FastAPI. It handles data processing, model inference, and serves as the API for the frontend dashboard.

## Setup

1. **Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   The project uses modular requirements files.
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the FastAPI server using `uvicorn`:
```bash
python -m uvicorn src.api.main:app --reload --port 8000
```
The API will be available at `http://127.0.0.1:8000`.

## Directory Structure
- `src/api`: FastAPI routers and schemas.
- `src/features`: Feature engineering logic and builders.
- `src/training`: Model training scripts (Random Forest, XGBoost, etc.).
- `src/inference`: Batch and real-time prediction logic.
- `requirements-airflow.txt`: Dependencies for Airflow pipelines.
- `requirements-api.txt`: Dependencies for the FastAPI server.
====================================================================================
