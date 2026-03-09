from pathlib import Path
from datetime import datetime, timezone
import pandas as pd


SEGMENTATION_PATH = Path("data/segmentation/segmentation.parquet")


def write_segmentation(
    df: pd.DataFrame,
    segment_version: str,
) -> None:
    

    df = df.copy()

    if "snapshot_date" not in df.columns:
        raise ValueError("snapshot_date missing from segmentation dataframe")

    snapshot_date = df["snapshot_date"].iloc[0]

    df["segment_version"] = segment_version
    df["created_at"] = datetime.now(timezone.utc)

    if SEGMENTATION_PATH.exists():
        existing = pd.read_parquet(SEGMENTATION_PATH)

        existing = existing[
            existing["snapshot_date"] != snapshot_date
        ]

        df = pd.concat([existing, df], ignore_index=True)

    SEGMENTATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(SEGMENTATION_PATH, index=False)
