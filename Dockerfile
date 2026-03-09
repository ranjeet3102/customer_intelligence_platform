FROM apache/airflow:2.8.1-python3.11

USER airflow

COPY backend/requirements-airflow.txt /requirements-airflow.txt
COPY backend/requirements-api.txt /requirements-api.txt
COPY backend/requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /requirements.txt