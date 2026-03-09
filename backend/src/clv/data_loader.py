from pathlib import Path
import pandas as pd


def load_clv_inputs(snapshot_date: str) -> pd.DataFrame:

    features_df = pd.read_parquet("data/features/churn_features_v1.parquet")
    predictions_df = pd.read_parquet("data/predictions/churn_predictions.parquet")

    features_df = features_df[
        features_df["snapshot_date"] == snapshot_date
    ]

    predictions_df = predictions_df[
        predictions_df["snapshot_date"] == snapshot_date
    ]

    if features_df.empty:
        raise ValueError(f"No feature data for snapshot_date={snapshot_date}")

    if predictions_df.empty:
        raise ValueError(f"No prediction data for snapshot_date={snapshot_date}")

    clv_df = features_df.merge(
        predictions_df[
            ["customerid", "churn_probability", "model_version", "snapshot_date"]
        ],
        on=["customerid", "snapshot_date"],
        how="inner",
        validate="one_to_one"
    )

    if clv_df.empty:
        raise ValueError("CLV input dataframe empty after join")

    return clv_df
