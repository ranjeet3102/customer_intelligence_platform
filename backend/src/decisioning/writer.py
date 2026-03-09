from pathlib import Path
import pandas as pd

DECISIONS_PATH = Path("data/decisions/retention_decisions.parquet")


def write_decisions(df: pd.DataFrame) -> None:
    """
    Persist validated retention decisions.
    """

    DECISIONS_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DECISIONS_PATH.exists():
        existing = pd.read_parquet(DECISIONS_PATH)

        existing = existing[
            ~existing.set_index(["customerid", "snapshot_date"]).index.isin(
                df.set_index(["customerid", "snapshot_date"]).index
            )
        ]

        df = pd.concat([existing, df], ignore_index=True)

    df.to_parquet(DECISIONS_PATH, index=False)