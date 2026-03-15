Retention Decision Engine:
Overview:

The Retention Decision Engine determines the optimal retention strategy for each customer predicted to churn.

It combines information from the churn prediction model, customer lifetime value (CLV), and customer segmentation results to decide whether a retention action should be applied and how much incentive should be offered.

The goal of this module is to ensure that retention strategies maximize business value while maintaining positive return on investment (ROI).
==============================================================
Objectives

The decision engine performs the following responsibilities:
* Load churn predictions
* Load customer lifetime value (CLV)
* Load segmentation results
* Determine retention strategies based on customer segments
* Calculate retention incentives
* Enforce economic constraints to avoid negative ROI
* Store final retention decisions
================================================================

Input Data

The decision engine consumes three datasets.

1. Churn Predictions:

Location:
"data/predictions/churn_predictions.parquet"

Contains:
* customerid
* churn_probability
-------------------------------------------------------------
2. CLV Store

Location:
"data/clv/clv.parquet"

Contains:
* customerid
* clv
-------------------------------------------------------------
3. Segmentation Store

Location:
"data/segmentation/segmentation.parquet"

Contains:
* customerid
* risk_bucket
* value_bucket
* segment_code
---------------------------------------------------------------
Decision Strategy

Retention decisions are determined using a rule-based policy based on the customer segment.

Example decision policy:

Risk Level	  Value Level	 Retention Strategy
High Risk	  High Value	 Offer discount
High Risk	  Low Value	     Minimal retention effort
Medium Risk	  High Value     Targeted engagement
Low Risk	  High Value     No action
