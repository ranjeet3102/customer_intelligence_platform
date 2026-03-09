from pathlib import Path
import pandas as pd
import logging
# from src.etl.distribution_analysis import compute_skew_kurtosis
from src.etl.preprocessing.missing_values import handle_missing_values

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s')

# numeric_cols = [
#     "tenure",
#     "monthlycharges",
#     "totalcharges",
# ]

INPUT_PATH=Path("data/validated/telco_customer_churn_validated.parquet")
OUTPUT_PATH=Path("data/processed/telco_customer_churn_processed.parquet")

def run_preprocessing():
    logging.info("Starting preprocessing...")

    df=pd.read_parquet(INPUT_PATH)

    # df1= pd.read_parquet("data/validated/telco_customer_churn_validated.parquet")

    # stats_df = compute_skew_kurtosis(df1, numeric_cols)

    # print(stats_df)

    logging.info("Running missing value handling")
    df=handle_missing_values(df)

    logging.info("Saving processed data")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    logging.info("Preprocessing completed.")

    return df

if __name__=="__main__":
    run_preprocessing()