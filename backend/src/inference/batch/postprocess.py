from datetime import datetime
import pandas as pd
import yaml
from pathlib import Path

CONFIG_PATH = Path("src/inference/config/inference.yaml")

def load_churn_threshold() -> float:

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
    
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    try:

        return float(config["churn"]["threshold"])
    
    except KeyError:

        raise ValueError("Churn threshold not defined in inference config")
    

def apply_threshold_and_metadata(predictions_df: pd.DataFrame, snapshot_date: str,
                                 inference_ts: datetime,) -> pd.DataFrame:
    
    if "churn_probability" not in predictions_df.columns:
        raise ValueError("Missing churn_probability column")
    
    df = predictions_df.copy()

    churn_threshold = load_churn_threshold()

    df["churn_label"] = (df["churn_probability"] >= churn_threshold).astype(int)

    df["snapshot_date"] = pd.to_datetime(snapshot_date)

    df["inference_ts"] = inference_ts

    df["churn_threshold"] = churn_threshold

    return df