from datetime import datetime, timezone
import pandas as pd
from pathlib import Path
from src.inference.batch.data_loader import load_feature_snapshot
from src.inference.batch.predictor import generate_predictions
from src.inference.batch.postprocess import apply_threshold_and_metadata
from src.inference.batch.writer import write_predictions


def run_batch_inference(snapshot_date: str) -> None:

    inference_ts = datetime.now(timezone.utc)

    feature_df = load_feature_snapshot(snapshot_date=snapshot_date)

    predictions_df = generate_predictions(feature_df)

    final_df = apply_threshold_and_metadata(predictions_df = predictions_df,
                                            snapshot_date = snapshot_date,
                                            inference_ts = inference_ts)
    
    write_predictions(final_df)


if __name__ == "__main__":

    df = pd.read_parquet("data/features/churn_features_v1.parquet")
    latest_snapshot = df["snapshot_date"].max().strftime("%Y-%m-%d")

    run_batch_inference(latest_snapshot)