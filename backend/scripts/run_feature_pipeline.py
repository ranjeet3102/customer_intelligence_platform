from src.ingestion.load_sources import run_ingestion_pipeline
from src.etl.data_profiling import run_profiling_pipeline
from src.etl.run_preprocessing import run_preprocessing
from src.pipelines.feature_pipeline import run_feature_pipeline


import pandas as pd
from datetime import date

snapshot_date = date.today().isoformat()

def main():

    run_ingestion_pipeline()
    run_profiling_pipeline()
    run_preprocessing()

    df=pd.read_parquet("data/processed/telco_customer_churn_processed.parquet")
    run_feature_pipeline(df, snapshot_date=snapshot_date,feature_version="v1")



if __name__ == "__main__":
    main()