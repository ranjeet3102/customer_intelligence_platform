import logging
import pandas as pd

from src.features.builders.churn_features import build_churn_features
from src.features.store.writer import write_feature_store
from src.features.store.encoder_store import save_encoders
from src.features.store.metadata_writer import write_feature_metadata


logger=logging.getLogger(__name__)

def run_feature_pipeline(df:pd.DataFrame,
                        snapshot_date: str,
                        feature_version:str ="v1"):
    
    logger.info("=== phase 2 Feature Pipeline started ===")

    features_df, encoders = build_churn_features(
        df,
        snapshot_date=snapshot_date,
        feature_version=feature_version
    )

    save_encoders(encoders,feature_version)

    feature_path=write_feature_store(features_df,feature_version)
    meta_path = write_feature_metadata(
                features_df,
                feature_version,
                feature_path
    )

    logger.info(f"[MetaData] written -> {meta_path}")
    logger.info("=== Phase 2 Feature Pipeline Completed ===")

    return feature_path