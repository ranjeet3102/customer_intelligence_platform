from pathlib import Path
import pandas as pd

PREDICTION_STORE_PATH = Path("data/predictions/churn_predictions.parquet")


def write_predictions(predictions_df: pd.DataFrame) -> None:

    required_cols = {
        "customerid",
        "snapshot_date",
        "churn_probability",
        "churn_label",
        "model_version",
        "inference_ts",
    }

    missing = required_cols - set(predictions_df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    PREDICTION_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)

    if PREDICTION_STORE_PATH.exists():
        existing_df = pd.read_parquet(PREDICTION_STORE_PATH)

        snapshot_date = predictions_df["snapshot_date"].iloc[0]
        existing_df = existing_df[existing_df["snapshot_date"] != snapshot_date]

        final_df = pd.concat([existing_df, predictions_df], ignore_index=True)

    else:

        final_df = predictions_df.copy()

    final_df.to_parquet(PREDICTION_STORE_PATH, index=False)