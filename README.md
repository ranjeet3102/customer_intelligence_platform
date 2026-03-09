# Customer Intelligence Platform (CIP)

A comprehensive platform for customer insights, churn prediction, and retention decision-making. Built with a modern Light Premium UI and a robust Python-based data architecture.

## Architecture Overview

The project is divided into three main components:

- **[Frontend](./frontend)**: A React + Vite application featuring a premium light-mode dashboard.
- **[Backend](./backend)**: A FastAPI service providing endpoints for KPIs, predictions, and segmentation.
- **[Airflow](./airflow)**: An automation layer for data pipelines, model training, and batch inference.

## Prerequisites

- **Python**: 3.11+
- **Node.js**: 20.x+
- **Docker**: For running the Airflow pipelines.

## How to Run

### 1. Backend (API)
The backend provides the API layer for the dashboard.
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.api.main:app --reload
```

### 2. Frontend (Dashboard)
The dashboard provides the user interface.
```bash
cd frontend
npm install
npm run dev
```

### 3. Airflow (Pipelines)
Airflow handles data orchestration.
```bash
cd airflow
docker compose up -d
```

---

## 📁 Project Structure

```text
customer-intelligence-platform/
├── airflow/            # DAGs and Docker Compose
├── backend/
│   ├── src/            # Core Python modules
│   ├── scripts/        # Pipeline runners
│   └── data/           # Validated, Features, CLV, and Predictions
└── frontend/
    ├── src/            # React components and layouts
    └── public/         # Assets
```

---

*Refer to the individual component directories for more detailed documentation.*
