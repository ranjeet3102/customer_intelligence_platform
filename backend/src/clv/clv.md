Customer Lifetime Value (CLV) Engine:

Overview:
The Customer Lifetime Value (CLV) Engine estimates the expected future monetary value that each customer will generate for the business.

It uses churn probability predictions from the inference pipeline and combines them with revenue information to estimate how long a customer is likely to remain subscribed and how much profit they are expected to generate.

This module helps the system understand which customers are the most valuable, allowing downstream components such as segmentation and retention decisioning to make economically optimal decisions.

-------------------------------------------------------
Pipeline Position:

Feature Store
      │
      ▼
Batch Inference
      │
      ▼
CLV Engine
      │
      ▼
Customer Segmentation
      │
      ▼
Retention Decision Engine
=========================================================
Objectives

The CLV engine performs the following tasks:
* Load churn prediction outputs
* Estimate expected customer lifetime
* Calculate expected future revenue
* Compute customer lifetime value
* Store CLV results for downstream modules

This allows the platform to identify high-value customers worth retaining.
=========================================================
Input Data

The CLV engine consumes data from two sources:

1. Prediction Store:
"data/predictions/churn_predictions.parquet"

Contains:
* customerid
* churn_probability
* snapshot_date
---------------------------------------------------------
2. Feature Store
"data/features/churn_features_v1.parquet"

Contains:
* monthlycharges
* tenure
* customer metadata

These features are required to calculate revenue-related metrics.

==========================================================

