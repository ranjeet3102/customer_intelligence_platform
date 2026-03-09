import pandas as pd
import logging

logger = logging.getLogger(__name__)

NUMERIC_COLUMNS = [
    "tenure",
    "monthlycharges",
    "totalcharges",
    "seniorcitizen",
]


YES_NO_COLUMNS = [
    "partner",
    "dependents",
    "phoneservice",
    "multiplelines",
    "onlinesecurity",
    "onlinebackup",
    "deviceprotection",
    "techsupport",
    "streamingtv",
    "streamingmovies",
    "paperlessbilling",
]

CATEGORICAL_COLUMNS = [
    "contract",
    "paymentmethod",
    "internetservice",
]

TARGET_COLUMN = "churn"



#numeric missing handler
def handle_numeric_missing(df: pd.DataFrame) -> pd.DataFrame:

    df=df.copy()
    for col in NUMERIC_COLUMNS:
        if col not in df.columns:
            continue
        
        df[col]=pd.to_numeric(df[col],errors="coerce")
        missing_before=df[col].isna().sum()

        if missing_before>0:
            median_value=df[col].median()
            df[col]=df[col].fillna(median_value)

            logging.info(f"[Missing] Filled {missing_before} NaNs in {col} with median={median_value}")
    
    return df


#Yes/No Missing Handler
def handle_yesno_missing(df: pd.DataFrame) -> pd.DataFrame:

    df=df.copy()
    for col in YES_NO_COLUMNS:
        if col not in df.columns:
            continue
            
        missing_before=df[col].isna().sum()

        if missing_before>0:
            df[col]=df[col].fillna("No")
            logging.info(f"[Missing] Filled {missing_before} NaNs in {col} with 'No'")

    return df


#categorical missing handler
def handle_categorical_missing(df: pd.DataFrame) -> pd.DataFrame:

    df=df.copy()
    for col in CATEGORICAL_COLUMNS:
        if col not in df.columns:
            continue
            
        missing_before=df[col].isna().sum()

        if missing_before>0:
            df[col]=df[col].fillna("Unknown")
            logging.info(f"[Missing] Filled {missing_before} NaNs in {col} with 'Unknown'")

    return df



#Target missing handler
def handle_target_missing(df: pd.DataFrame) -> pd.DataFrame:

    df=df.copy()
    if TARGET_COLUMN in df.columns:
        missing_before=df[TARGET_COLUMN].isna().sum()

        if missing_before>0:
            df=df.dropna(subset=[TARGET_COLUMN])
            logging.info(f"[Missing] Dropped {missing_before} rows with NaNs in target column '{TARGET_COLUMN}'")

    return df


#missing value pipeline
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:

    logger.info("Starting missing value handling pipeline")
    df=df.copy()

    df=handle_numeric_missing(df)
    df=handle_yesno_missing(df)
    df=handle_categorical_missing(df)
    df=handle_target_missing(df)

    total_remaining_missing=df.isna().sum().sum()

    if total_remaining_missing>0:
        logger.warning(f"Remaining missing values after handling: {total_remaining_missing}")
    else:
        logger.info("No remaining missing values after handling")
        
    return df
