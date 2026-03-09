import pandas as pd
from typing import Dict


def assign_risk_bucket(
    df: pd.DataFrame,
    risk_config: Dict[str, float],
) -> pd.Series:


    low_thr = risk_config["low"]
    high_thr = risk_config["high"]

    if not (0 < low_thr < high_thr < 1):
        raise ValueError("Invalid risk bucket thresholds")
    

    def _bucket(p):
        if p < low_thr:
            return "low"
        elif p < high_thr:
            return "medium"
        else:
            return "high"

    return df["churn_probability"].apply(_bucket)


def assign_value_bucket(
    df: pd.DataFrame,
    value_config: Dict[str, float],
) -> pd.Series:
    
    if value_config["method"] != "quantile":
        raise NotImplementedError("Only quantile-based bucketing supported")

    low_q = value_config["low"]
    high_q = value_config["high"]

    if not (0 < low_q < high_q < 1):
        raise ValueError("Invalid value bucket quantiles")

    clv_low = df["clv"].quantile(low_q)
    clv_high = df["clv"].quantile(high_q)


    def _bucket(v):
        if v < clv_low:
            return "low"
        elif v < clv_high:
            return "medium"
        else:
            return "high"

    return df["clv"].apply(_bucket)

def build_segment_code(
    risk_bucket: pd.Series,
    value_bucket: pd.Series,
) -> pd.Series:
   

    risk_map = {
        "low": "LR",
        "medium": "MR",
        "high": "HR",
    }

    value_map = {
        "low": "LV",
        "medium": "MV",
        "high": "HV",
    }

    return (
        risk_bucket.map(risk_map)
        + "-"
        + value_bucket.map(value_map)
    )

def apply_segmentation(
    df: pd.DataFrame,
    config: Dict,
) -> pd.DataFrame:
    
    df = df.copy()

    df["risk_bucket"] = assign_risk_bucket(
        df, config["risk_buckets"]
    )

    df["value_bucket"] = assign_value_bucket(
        df, config["value_buckets"]
    )

    df["segment_code"] = build_segment_code(
        df["risk_bucket"],
        df["value_bucket"],
    )

    return df

