from pathlib import Path
import pandas as pd
import numpy as np
import logging

VALIDATED_PATH=Path("data/validated/telco_customer_churn_validated.parquet")
REPORT_DIR=Path("reports/mertics")

REPORT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s'
                    )

#load data
def load_validated_data() -> pd.DataFrame:
    
    if not VALIDATED_PATH.exists():
        raise FileNotFoundError(f"Validated data file not found at {VALIDATED_PATH}")
    
    logging.info(f"Loading validated datasets...")
    df=pd.read_parquet(VALIDATED_PATH)
    logging.info(f"Dataset shape: {df.shape}")
    return df

#profiling function
def missing_values_report(df: pd.DataFrame) -> pd.DataFrame:

    logging.info("Generating missing values report...")
    report=pd.DataFrame({
        "missing_count":df.isna().sum(),
        "missing_percentage":(df.isna().mean()*100).round(2)
    }).sort_values('missing_percentage', ascending=False)

    return report

def dtype_report(df: pd.DataFrame) -> pd.DataFrame:

    return pd.DataFrame({
        "dtype":df.dtypes.astype(str)
    })

def cardinality_report(df: pd.DataFrame) -> pd.DataFrame:

    return pd.DataFrame({
        "unique_values(cardinality)": df.nunique()
    }).sort_values('unique_values(cardinality)', ascending=False)

def numeric_summary_report(df: pd.DataFrame) -> pd.DataFrame:

    numeric_cols=df.select_dtypes(include=["int64","float64"])
    return numeric_cols.describe().T


def outlier_report(df: pd.DataFrame) -> pd.DataFrame:

    numeric_cols=df.select_dtypes(include=["int64","float64"])
    rows=[]

    for col in numeric_cols.columns:

        Excluded_columns = {"seniorcitizen", "tenure"}
        if col in Excluded_columns:
            continue
        q1=numeric_cols[col].quantile(0.25)
        q3=numeric_cols[col].quantile(0.75)

        iqr=q3-q1

        lower= q1 - 1.5 * iqr
        upper= q3 + 1.5 * iqr

        outliers = ((numeric_cols[col]<lower) | (numeric_cols[col]>upper)).sum()

        rows.append({
            "columns":col,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "lower_bound": lower,
            "upper_bound": upper,
            "outlier_count": outliers,
            "outlier_percentile": round(outliers/len(df)*100, 2)
        })
        
    return pd.DataFrame(rows).sort_values("outlier_percentile", ascending=False)
    

#save reports
def save_report(df: pd.DataFrame, name: str):

    path= REPORT_DIR/ f"{name}.csv"
    df.to_csv(path)
    logging.info(f"Saved report: {path}")


#Orchestration
def run_profiling_pipeline():

    logging.info("Staring data profiling pipeline...")

    df = load_validated_data()

    missing = missing_values_report(df)
    dtypes = dtype_report(df)
    cardinality = cardinality_report(df)
    numeric_summary = numeric_summary_report(df)
    outliers = outlier_report(df)

    save_report(missing, "missing_values_report")
    save_report(dtypes,"dtype_report")
    save_report(cardinality,"cardinality_report")
    save_report(numeric_summary,"numeric_summary_report")
    save_report(outliers,"outlier_report")

    logging.info("Data profiling completed successfully.")


if __name__=="__main__":
    run_profiling_pipeline()
