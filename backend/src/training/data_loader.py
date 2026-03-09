import pandas as pd
import pathlib as Path
from typing import Tuple,List


IDENTITY_COLUMNs: List[str] =[
    "customerid",
    "snapshot_date",
    "feature_version",
    "source",
]

TARGET_COLUMN = "churn"

def load_training_data(feature_path: Path) -> Tuple[pd.DataFrame, pd.Series]:
    
    df=pd.read_parquet(feature_path)

    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in data.")
    
    y=df[TARGET_COLUMN]

    drop_cols=IDENTITY_COLUMNs + [TARGET_COLUMN]
    X=df.drop(columns=drop_cols, errors="ignore")

    if X.empty:
        raise ValueError("Feature matrix x is empty after column filtering")

    return X,y