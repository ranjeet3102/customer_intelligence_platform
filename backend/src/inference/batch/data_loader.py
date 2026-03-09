from pathlib import Path
import pandas as pd

FEATURE_STORE_PATH = Path("data/features/churn_features_v1.parquet")

def load_feature_snapshot(snapshot_date: str) -> pd.DataFrame:

    if not FEATURE_STORE_PATH.exists():
        raise FileNotFoundError(
            f"Feature store not found at {FEATURE_STORE_PATH}."
        )
    
    df = pd.read_parquet(FEATURE_STORE_PATH)

    if "snapshot_date" not in df.columns:
        raise ValueError(
            "Feature store missing required column: snapshot_date"
        )
    
    snapshot_date =pd.to_datetime(snapshot_date)
    snapshot_df = df[df["snapshot_date"] == snapshot_date]

    if snapshot_df.empty:
        raise ValueError(
            f"No features found for snapshot_date={snapshot_date.date()}"
        )

    return snapshot_df.reset_index(drop=True)