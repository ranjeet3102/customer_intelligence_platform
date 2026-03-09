from pathlib import Path
import pandas as pd
import logging

logging=logging.getLogger(__name__)

FEATURE_STORE_DIR=Path("data/features")

def write_feature_store(df: pd.DataFrame,feature_version: str) -> Path:

    FEATURE_STORE_DIR.mkdir(parents=True, exist_ok=True)
    output_path=FEATURE_STORE_DIR/f"churn_features_{feature_version}.parquet"
    df.to_parquet(output_path,index=False)

    logging.info(f"[FeatureStore] written -> {output_path}")
    logging.info(f"[FeatureStore] Rows={len(df)} Cols={len(df.columns)}")

    return output_path
