from pathlib import Path
import pandas as pd

FEATURES_PATH = Path("data/features/churn_features_v1.parquet")
PREDICTIONS_PATH = Path("data/predictions/churn_predictions.parquet")
CLV_PATH = Path("data/clv/clv.parquet")


def _load_latest_snapshot(path: Path) -> pd.DataFrame:

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    df = pd.read_parquet(path)

    if "snapshot_date" not in df.columns:
        raise ValueError(f"`snapshot_date` missing in {path.name}")

    df = df.copy()
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"])

    latest_snapshot = df["snapshot_date"].max()
    df_latest = df[df["snapshot_date"] == latest_snapshot]

    if df_latest.empty:
        raise ValueError(f"No rows found for latest snapshot in {path.name}")

    return df_latest


def load_segmentation_base() -> pd.DataFrame:

    features = _load_latest_snapshot(FEATURES_PATH)
    predictions = _load_latest_snapshot(PREDICTIONS_PATH)
    clv = _load_latest_snapshot(CLV_PATH)

    snapshot_dates = {
        features["snapshot_date"].iloc[0],
        predictions["snapshot_date"].iloc[0],
        clv["snapshot_date"].iloc[0],
    }

    if len(snapshot_dates) != 1:
        raise ValueError(
            f"Snapshot mismatch detected across stores: {snapshot_dates}"
        )

    base = (
        features
        .merge(
            predictions[["customerid", "churn_probability"]],
            on="customerid",
            how="inner",
        )
        .merge(
            clv[["customerid", "clv"]],
            on="customerid",
            how="inner",
        )
    )

    if base.empty:
        raise ValueError("Segmentation base dataframe is empty after joins")

    return base

