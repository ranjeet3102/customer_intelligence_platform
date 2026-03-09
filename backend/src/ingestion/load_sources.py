from pathlib import Path
import pandas as pd
import logging

from src.ingestion.schema import TELCO_SCHEMA



# Configuration
RAW_PATH = Path("data/raw/telecom.csv")
VALIDATED_PATH = Path("data/validated/telco_customer_churn_validated.parquet")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)



# Load Raw Data
def load_raw_data() -> pd.DataFrame:
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw file not found: {RAW_PATH}")

    logging.info("Loading raw dataset...")
    df = pd.read_csv(RAW_PATH)

    logging.info(f"Raw shape: {df.shape}")
    return df


# Column Name Normalization
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
   
    logging.info("Normalizing column names...")

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    column_aliases = {
        "customerID":"customerid",
        "SeniorCitizen":"seniorcitizen",
        "Partner":"partner",
        "Dependents":"dependents",
        "PhoneService":"phoneservice",
        "MultipleLines":"multiplelines",
        "InternetService":"internetservice",
        "OnlineSecurity":"onlinesecurity",
        "OnlineBackup":"onlinebackup",
        "DeviceProtection":"deviceprotection",
        "TechSupport":"techsupport",
        "StreamingTV":"streamingtv",
        "StreamingMovies":"streamingmovies",
        "Contract":"contract",
        "PaperlessBilling":"paperlessbilling",
        "PaymentMethod":"paymentmethod",
        "MonthlyCharges":"monthlycharges",
        "TotalCharges":"totalcharges",
        "Churn":"churn",

    }

    df = df.rename(columns=column_aliases)

    logging.info(f"Normalized columns: {list(df.columns)}")

    return df



# Value Normalization
def normalize_values(df: pd.DataFrame) -> pd.DataFrame:

    logging.info("Normalizing categorical values...")

    df = df.copy()

    yes_no_columns = [
        "partner",
        "dependents",
        "phoneservice",
        "paperlessbilling",
        "churn",
    ]

    for col in yes_no_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .map({
                    "yes": "Yes",
                    "no": "No",
                })
            )

    service_columns = [
        "multiplelines",
        "onlinesecurity",
        "onlinebackup",
        "deviceprotection",
        "techsupport",
        "streamingtv",
        "streamingmovies",
    ]

    for col in service_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .replace({
                    "yes": "Yes",
                    "no": "No",
                    "no internet service": "No internet service",
                    "no phone service": "No phone service",
                })
                
            )

    if "gender" in df.columns:
        df["gender"] = (
            df["gender"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "male": "Male",
                "female": "Female",
            })
        )

    if "contract" in df.columns:
        df["contract"] = (
            df["contract"]
            .astype(str)
            .str.strip()
            .str.lower()
            .replace({
                "month-to-month": "Month-to-Month",
                "one year": "One year",
                "two year": "Two year",
            })
        )

    if "internetservice" in df.columns:
        df["internetservice"] = (
            df["internetservice"]
            .astype(str)
            .str.strip()
            .str.lower()
            .replace({
                "dsl": "DSL",
                "fiber optic": "Fiber optic",
                "no": "No",
            })
        )

    if "paymentmethod" in df.columns:
        df["paymentmethod"] = (
            df["paymentmethod"]
            .astype(str)
            .str.strip()
            .str.lower()
            .replace({
                "electronic check": "Other",
                "mailed check": "Mailed check",
                "bank transfer (automatic)": "Bank transfer (automatic)",
                "credit card (automatic)": "Credit card (automatic)",
            })
        )
    

    return df



# Type Cleaning
def clean_types(df: pd.DataFrame) -> pd.DataFrame:

    logging.info("Cleaning column types...")

    df = df.copy()

    if "totalcharges" in df.columns:
        df["totalcharges"] = pd.to_numeric(
            df["totalcharges"],
            errors="coerce"
        )
        
   
    if "monthlycharges" in df.columns:
        df["monthlycharges"] = df["monthlycharges"].astype(float)

    
    if "seniorcitizen" in df.columns:
        df["seniorcitizen"] = df["seniorcitizen"].astype(int)

    if "tenure" in df.columns:
        df["tenure"] = df["tenure"].astype(int)
    
    return df



# Schema Validation
def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Validating dataframe schema...")
    validated_df = TELCO_SCHEMA.validate(df)
    logging.info("Schema validation passed ")
    return validated_df



# Save Validated Data
def save_validated(df: pd.DataFrame) -> None:
    VALIDATED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(VALIDATED_PATH, index=False)
    logging.info(f"Validated data written to: {VALIDATED_PATH}")




# Orchestration
def run_ingestion_pipeline() -> None:
    logging.info("Starting ingestion pipeline...")

    df_raw = load_raw_data()
    df_cols = normalize_columns(df_raw)
    df_vals = normalize_values(df_cols)
    df_clean = clean_types(df_vals)
    df_validated = validate_schema(df_clean)
    save_validated(df_validated)

    logging.info("Ingestion pipeline completed successfully.")


if __name__ == "__main__":
    run_ingestion_pipeline()
