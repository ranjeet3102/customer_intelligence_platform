Feature Engineering Layer:

Overview:

The Feature Engineering Layer transforms validated raw customer data into structured machine-learning features used for churn prediction and downstream analytics.

This layer standardizes transformations, enforces feature contracts, and writes the resulting dataset to the feature store, ensuring that training and inference pipelines use the same feature definitions.

The goal of this module is to create consistent, reproducible, and model-ready features from the validated dataset produced by the ingestion layer.
----------------------------------------------

Raw Data
   │
   ▼
Ingestion & Validation
   │
   ▼
Feature Engineering   ← (this module)
   │
   ▼
Feature Store
   │
   ▼
Model Training / Inference
-------------------------------------------

The feature pipeline performs the following responsibilities:

Convert validated raw data into machine learning features

Standardize feature transformations

Normalize binary variables

Encode categorical variables

Generate derived features

Inject snapshot metadata

Validate the feature schema before storing

This layer guarantees that all models receive a consistent feature representation.
=====================================================
Input Dataset:
The feature pipeline consumes the validated dataset produced by the ingestion stage.

Input location:
"data/validated/telco_customer_churn_validated.parquet"

This dataset has already passed:

* schema validation
* type cleaning
* categorical normalization
======================================================
Feature Engineering Steps:
The pipeline performs a sequence of transformations to prepare the dataset for machine learning.

1. Binary Normalization
Binary categorical variables are converted into numeric values.

2. Categorical Encoding
Categorical variables with multiple categories are converted into numeric representations using label encoding.

3. Derived Feature Creation
Additional features are derived to improve model performance.

4. Snapshot Metadata Injection
Each record receives metadata fields used for pipeline tracking and reproducibility.
===========================================================
Feature Contract Validation:
Before writing features to the feature store, the pipeline validates a feature contract.

The contract ensures:
* required features exist
* correct data types
* no unexpected schema changes

If validation fails, the pipeline stops to prevent inconsistent features from entering the system.
=================================================================
Output Dataset (Feature Store):
The generated feature dataset is written to the feature store as a Parquet file.

Output location:
"data/features/churn_features_v1.parquet"

This dataset becomes the single source of truth for machine learning features used in:
* model training
* batch inference
* analytics
===============================================================
Feature Store Design

The feature store provides several benefits:

Benefit	        Description
Consistency	     Training and inference use identical features
Reproducibility  Feature snapshots are immutable
Performance	     Parquet format enables efficient queries
Versioning	     Feature versions allow schema evolution