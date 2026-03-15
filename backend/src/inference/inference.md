Inference Layer:

Overview:
The Inference Layer generates churn predictions for all customers using the production model stored in the model registry.

This module loads the latest feature snapshot from the feature store, applies the trained model, and produces churn probability predictions for each customer. These predictions are then stored in the prediction store, which serves as input for downstream modules such as CLV estimation, customer segmentation, and retention decisioning.

The inference pipeline is designed to be deterministic, reproducible, and production-ready.
---------------------------------------------------------
Pipeline Position:

Feature Store
      │
      ▼
  Inference
      │
      ▼
Prediction Store
      │
      ├── CLV Engine
      ├── Customer Segmentation
      └── Retention Decision Engine
==============================================================
Objectives:

The batch inference layer performs the following responsibilities:
* Load the latest feature snapshot from the feature store
* Load the production model from the model registry
* Generate churn probability predictions
* Apply the churn classification threshold
* Store predictions in the prediction store
* Attach metadata for reproducibility
  
=============================================================
Pipeline Components

The batch inference module is composed of several subcomponents.

Component	    Responsibility
data_loader	    loads the feature snapshot
predictor	    generates churn probabilities
postprocess	    applies classification threshold
writer	stores  predictions
batch_runner	orchestrates the inference pipeline

==============================================================
Input Data:

The inference pipeline consumes features produced by the feature engineering layer.

Input location:
"data/features/churn_features_v1.parquet"

The dataset includes:
* engineered features
* customer identifiers
* snapshot metadata

Before inference, non-feature columns are removed to ensure feature parity with the training dataset.
===============================================================
Model Loading:

The inference pipeline dynamically loads the production model from the model registry.

This prevents hardcoded model paths and ensures that the pipeline always uses the latest approved model.

Model artifact location:
"artifacts/models/ "

The model loader retrieves:
* model artifact
* model metadata
* feature version information
===========================================================
Prediction Generation:

The model generates churn probability predictions for each customer.
==========================================================
Output Dataset:
The final prediction dataset is stored in the prediction store.

Output location:
"data/predictions/churn_predictions.parquet"
