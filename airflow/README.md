# CIP Airflow

Data orchestration and pipeline automation for the Customer Intelligence Platform using Apache Airflow.

## Setup & Execution

1. **Prerequisites**:
   Ensure you have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed.

2. **Start Airflow Containers**:
   ```bash
   cd airflow
   docker compose up -d
   ```

3. **Access the Webserver**:
   Once the containers are healthy, access the Airflow UI at `http://localhost:8080`.
   - **Username**: `admin`
   - **Password**: `admin`

## Pipelines
- **Ingestion**: Automated ingestion of customer health and usage data.
- **Profiling**: Auto-EDA for identifying data quality issues and insights.
- **Training**: Scheduled retraining of churn and CLV models.
- **Inference**: Batch prediction pipelines for risk scoring.
