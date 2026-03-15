Customer Segmentation Layer:

Overview:

The Customer Segmentation Layer groups customers into meaningful categories based on their churn risk and customer lifetime value (CLV).

The purpose of segmentation is to help the system understand which customers are valuable and which customers are likely to churn, allowing the retention engine to apply appropriate strategies.

By combining churn probability and customer lifetime value, the platform can prioritize retention efforts toward high-value customers who are at risk of leaving.
--------------------------------------------------------
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
=======================================================
Objectives:

The segmentation module performs the following responsibilities:
* Load churn prediction results
* Load customer lifetime value (CLV) estimates
* Combine customer risk and value metrics
* Assign risk buckets based on churn probability
* Assign value buckets based on CLV
* Generate customer segments
* Store segmentation results for downstream decisioning

This segmentation allows the system to differentiate between low-value churners and high-value churners, which require different retention strategies.
=======================================================
Input Data:

The segmentation pipeline consumes two datasets.

1. Prediction Store

Location:
"data/predictions/churn_predictions.parquet"

Contains:
* customerid
* churn_probability
* snapshot_date
-------------------------------------------------------
2. CLV Store

Location:
"data/clv/clv.parquet"

Contains:
* customerid
* clv
* expected_remaining_months
=========================================================
Segmentation Strategy:
Customers are segmented using two dimensions:
* Churn Risk
* Customer Value

Combining these two factors provides a comprehensive view of customer behavior.
---------------------------------------------------------
Risk Segmentation:

Customers are assigned a risk bucket based on their churn probability.
---------------------------------------------------------
Value Segmentation:

Customers are assigned a value bucket based on their CLV.
--------------------------------------------------------
Segment Generation:

The final customer segment is created by combining the risk bucket and value bucket.
------------------------------------------------------
Personas Mapping:

Segments can also be mapped to customer personas to simplify interpretation.
------------------------------------------------------
Output Dataset:

Segmentation results are stored in the segmentation store.

Output location:
"data/segmentation/segmentation.parquet"