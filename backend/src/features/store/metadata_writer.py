import json
import hashlib
from datetime import datetime,timezone
from pathlib import Path
import pandas as pd

def _dataframe_hash(df: pd.DataFrame) -> str:

    csv_bytes=df.to_csv(index=False).encode()
    return hashlib.md5(csv_bytes).hexdigest()

def write_feature_metadata(df: pd.DataFrame,feature_version: str,
                           feature_path: Path) -> Path:
    
    metadata={
        "feature_version": feature_version,
        "row_count": int(len(df)),
        "column_count":int(len(df.columns)),
        "columns": list(df.columns),
        "dataset_hash":_dataframe_hash(df),
        "snapshot_min":str(df["snapshot_date"].min()),
        "snapshot_max":str(df["snapshot_date"].max()),
        "source_values": sorted(df["source"].unique().tolist()),
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }

    meta_path=feature_path.with_suffix(".metadata.json")

    with open(meta_path, "w") as f:
        json.dump(metadata, f,indent=2)

    return meta_path