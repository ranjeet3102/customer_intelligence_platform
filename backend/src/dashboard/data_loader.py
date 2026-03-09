from pathlib import Path
import pandas as pd

DECISIONS_PATH = Path("data/decisions/retention_decisions.parquet")


def _load_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing artifact: {path}")
    return pd.read_parquet(path)


def load_dashboard_snapshot(snapshot_date: str | None = None) -> pd.DataFrame:
    """
    Phase 8 dashboard loader.

    Source of truth:
    - retention_decisions.parquet (Phase 6 output)

    This file already contains:
    predictions + CLV + segmentation + decisioning
    """

    df = _load_parquet(DECISIONS_PATH)

    # --------------------------------------------------
    # Resolve snapshot_date
    # --------------------------------------------------
    if snapshot_date is None:
        snapshot_date = df["snapshot_date"].max()

    snapshot_date = pd.to_datetime(snapshot_date)
    df = df[df["snapshot_date"] == snapshot_date]

    if df.empty:
        raise ValueError(f"No data found for snapshot_date={snapshot_date}")

    # --------------------------------------------------
    # Enforce uniqueness
    # --------------------------------------------------
    if df.duplicated(subset=["customerid", "snapshot_date"]).any():
        raise ValueError("Duplicate dashboard rows per customer per snapshot")

    # --------------------------------------------------
    # Select canonical dashboard columns
    # --------------------------------------------------
    dashboard_columns = [
        "customerid",
        "snapshot_date",
        "churn_probability",
        "churn_label",
        "clv",
        "risk_bucket",
        "value_bucket",
        "segment_code",
        "persona",
        "action_type",
        "discount_pct",
        "incentive_cost",
        "expected_savings",
    ]

    missing = set(dashboard_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Dashboard missing required columns: {missing}")

    return df[dashboard_columns].reset_index(drop=True)