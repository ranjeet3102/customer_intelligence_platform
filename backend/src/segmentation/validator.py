import pandas as pd
from typing import Dict


def validate_structure(df: pd.DataFrame) -> None:
    required_cols = [
        "customerid",
        "risk_bucket",
        "value_bucket",
        "segment_code",
        "persona",
        "churn_probability",
        "clv",
    ]

    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df["customerid"].duplicated().any():
        raise ValueError("Duplicate customerid detected")

    null_cols = df[required_cols].isnull().any()
    if null_cols.any():
        raise ValueError(
            f"Null values found in columns: "
            f"{null_cols[null_cols].index.tolist()}"
        )


def validate_logic(df: pd.DataFrame) -> None:
   
    risk_means = (
        df.groupby("risk_bucket")["churn_probability"]
        .mean()
        .to_dict()
    )

    if not (
        risk_means.get("high", 0)
        > risk_means.get("medium", 0)
        > risk_means.get("low", 0)
    ):
        raise ValueError(
            f"Invalid churn ordering by risk bucket: {risk_means}"
        )
        

    value_means = (
        df.groupby("value_bucket")["clv"]
        .mean()
        .to_dict()
    )

    if not (
        value_means.get("high", 0)
        > value_means.get("medium", 0)
        > value_means.get("low", 0)
    ):
        raise ValueError(
            f"Invalid CLV ordering by value bucket: {value_means}"
        )


def validate_distribution(
    df: pd.DataFrame,
    config: Dict,
) -> None:
    min_pct = config["validation"]["min_segment_pct"]

    segment_dist = (
        df["segment_code"]
        .value_counts(normalize=True)
        .to_dict()
    )

    small_segments = {
        seg: pct
        for seg, pct in segment_dist.items()
        if pct < min_pct
    }

    if small_segments:
        raise ValueError(
            f"Segments below minimum size {min_pct}: "
            f"{small_segments}"
        )


def run_segmentation_validation(
    df: pd.DataFrame,
    config: Dict,
) -> None:
    validate_structure(df)
    validate_logic(df)
    validate_distribution(df, config)
