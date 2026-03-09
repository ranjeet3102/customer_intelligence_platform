# Customer Intelligence Platform (CIP)

## Overview

The **Customer Intelligence Platform (CIP)** is an end-to-end machine learning system designed to predict customer churn, estimate customer lifetime value (CLV), segment customers, and recommend retention strategies.

The platform simulates a production-grade analytics pipeline used in subscription businesses such as streaming services, SaaS platforms, and telecom providers.

It integrates **data engineering, machine learning, business analytics, and orchestration** into a unified system that runs automatically when new data arrives.

---

# Project Objectives

The system aims to answer critical business questions:

• Which customers are likely to churn?
• What is the predicted lifetime value of each customer?
• Which customer segments exist based on risk and value?
• What retention actions should the company take?
• What is the expected ROI of retention incentives?

---

# System Architecture

The platform follows a production-style ML architecture:

Data Sources
→ Raw Data Lake
→ Data Validation & Ingestion
→ Feature Engineering Pipeline
→ Feature Store
→ Model Training & Model Registry
→ Batch Inference Pipeline
→ CLV Engine
→ Customer Segmentation
→ Retention Decision Engine
→ Prediction Store
→ Dashboard & Reports
→ Monitoring & Orchestration

---

# Project Phases

## Phase 1 — Data Collection & Validation

Purpose:
Build a reliable ingestion pipeline and ensure schema correctness.

Key Components:

• Data ingestion pipeline
• Column normalization
• Schema validation using Pandera
• Data quality checks
• Outlier detection
• Profiling reports

Output:
Validated dataset stored in the **validated data layer**.

---

## Phase 2 — Feature Engineering Pipeline

Purpose:
Transform raw data into model-ready features.

Key Features Created:

• tenure_months
• revenue_per_tenure
• contract_type_encoding
• engagement indicators

Pipeline Responsibilities:

• preprocessing
• categorical encoding
• derived feature generation
• feature contract validation
• feature store writing

Output:
`data/features/churn_features_v1.parquet`

---

## Phase 3 — Model Training & Evaluation

Three models were trained:

1. Logistic Regression
2. Random Forest
3. XGBoost

Evaluation metrics:

• Accuracy
• Precision
• Recall
• ROC-AUC

Final model selected:

Random Forest
because it achieved the **best ROC-AUC (~0.84)** and balanced recall for churn detection.

Model artifacts are stored in the **Model Registry**.

---

## Phase 4 — Customer Lifetime Value (CLV)

The CLV engine estimates the expected future revenue of each customer.

Key formula:

Expected Remaining Months =
1 / churn_probability

CLV Calculation:

CLV =
expected_remaining_months
× monthly_revenue
× margin_rate

Where:

margin_rate = 0.7
(assumed business profit margin)

Outputs:

`data/clv/clv.parquet`

---

## Phase 5 — Customer Segmentation

Customers are segmented based on:

• Churn risk
• Customer value

Segments include:

Low Risk — High Value
Low Risk — Low Value
Medium Risk — High Value
High Risk — High Value
High Risk — Low Value

Each segment maps to a **customer persona** used by marketing teams.

Output:

`data/segmentation/segmentation.parquet`

---

## Phase 6 — Retention Decision Engine

The system recommends retention actions using rule-based policies.

Example rules:

High Risk + High Value
→ offer discount

Low Risk + High Value
→ no action

Economic constraints ensure incentives never exceed expected revenue savings.

Key formulas:

Expected Savings
= CLV × churn_probability

Maximum Incentive
= CLV × (1 − margin_rate)

Final incentive cost:

min(raw_incentive_cost, max_allowed_cost, expected_savings)

Output:

`data/decisions/retention_decisions.parquet`

---

## Phase 7 — Batch Inference Pipeline

Batch inference generates predictions for all customers.

Steps:

1. Load latest feature snapshot
2. Load production model from registry
3. Generate churn probabilities
4. Apply decision threshold
5. Store predictions

Output:

`data/predictions/churn_predictions.parquet`

---

# Pipeline Execution Strategy

The system runs **daily**.

However, the pipeline executes only when **new data arrives**.

Execution flow:

Feature Pipeline
→ Batch Inference
→ CLV Calculation
→ Segmentation
→ Decision Engine

This prevents unnecessary pipeline runs.

---

# Orchestration

The pipeline is orchestrated using:

**Apache Airflow**

DAG pipeline:

feature_pipeline
→ batch_inference
→ clv_pipeline
→ segmentation
→ decision_engine

Airflow runs inside Docker containers.

---

# Technologies Used

Python
Pandas
Scikit-Learn
XGBoost
Parquet
Pandera
Apache Airflow
Docker
Git

---

# Outputs Produced

The system produces several analytical outputs:

• churn_predictions.parquet
• clv.parquet
• segmentation.parquet
• retention_decisions.parquet

These outputs can power dashboards or reporting systems.

---

# Key Features

Production-style ML architecture
Feature store design
Model registry
Economic decision engine
Customer segmentation framework
Automated Airflow orchestration
Snapshot-based pipeline execution

---

# Future Improvements

Real-time inference API
Experiment tracking with MLflow
Monitoring & drift detection
Automated retraining pipelines
Customer recommendation engine

---

# Author

Ranjeet

Machine Learning & Data Engineering Project
