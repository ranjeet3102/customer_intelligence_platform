from pathlib import Path
import pandas as pd

DECISIONS_PATH = Path("data/decisions/retention_decisions.parquet")


def load_dashboard_df() -> pd.DataFrame:
    """Return all data across all snapshots."""
    if not DECISIONS_PATH.exists():
        raise FileNotFoundError(f"Missing artifact: {DECISIONS_PATH}")

    df = pd.read_parquet(DECISIONS_PATH)

    if df.empty:
        raise ValueError("No data found in retention_decisions store.")

    return df.reset_index(drop=True)