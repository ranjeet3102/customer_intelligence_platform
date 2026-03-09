from fastapi import APIRouter
import pandas as pd
from pathlib import Path

router = APIRouter(prefix="/snapshots", tags=["snapshots"])

DECISIONS_PATH = Path("data/decisions/retention_decisions.parquet")


@router.get("")
def list_snapshots():
    df = pd.read_parquet(DECISIONS_PATH, columns=["snapshot_date"])
    snapshots = (
        df["snapshot_date"]
        .drop_duplicates()
        .sort_values()
        .astype(str)
        .tolist()
    )
    return {"snapshots": snapshots}