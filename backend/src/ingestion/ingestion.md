Raw Data Source
      │
      ▼
Load Raw Dataset
      │
      ▼
Column Normalization
      │
      ▼
Categorical Value Normalization
      │
      ▼
Data Type Cleaning
      │
      ▼
Schema Validation (Pandera)
      │
      ▼
Validated Dataset

=================================================
Input Data:

The ingestion layer reads the raw dataset from:

"data/raw/telecom.csv"

the dataset contains customer information including:
* customer demographics
* subscription details
* billing information
* service usage
* churn labels

This dataset is commonly used for churn prediction modeling.

========================================================
Data Standardlization:
Before validation, the ingestion pipeline performs several normaliation steps to ensure consistency.
---------------------------------------------
Column Name Normaliation:
All column names are converted to lowercase to maintain a consistent naming convention across the entire platform.
----------------------------------------------
Categorical Value Normaliation:
Categorical values are standardized to avoid inconsistencies across datasets.
----------------------------------------------
Schema validation:
The ingestion layer uses Pandera to enforce strict data contracts.

Schema validation checks:
* column presence
* data types
* categorical constraints
* null value restrictions
* numeric bounds

=======================================================
Output Data:
After validation, the dataset is stored as a Parquet file.

Output location:
"data/validation/telco_customer_churn_validation.parquet"

========================================================
Error Handling:
The ingestion pipeline follows a fail-fast strategy.

if validation fails:
* the pipeline stops
* an error is raised
* the invalid dataset is rejected

This ensured that the downstream ML pipelines never operate on corrupted data.






