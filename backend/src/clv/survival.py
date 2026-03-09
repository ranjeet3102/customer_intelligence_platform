import pandas as pd
from typing import Tuple

def estimate_expected_lifetime(
        df:pd.DataFrame,
        epsilon: float,
    max_lifetime_months: int
) -> pd.DataFrame:
    
    if "churn_probability" not in df.columns:
        raise KeyError("churn_probability column missing")
    
    lifetime_df = df.copy()

    if (lifetime_df["churn_probability"] < 0).any() or \
       (lifetime_df["churn_probability"] > 1).any():
        raise ValueError("Invalid churn_probability values detected")
    
    lifetime_df["effective_churn_probability"] = lifetime_df[
        "churn_probability"
    ].clip(lower=epsilon)

    lifetime_df["expected_remaining_months"] = (
        1.0 / lifetime_df["effective_churn_probability"]
    )

    lifetime_df["expected_remaining_months"] = lifetime_df[
        "expected_remaining_months"
    ].clip(upper=max_lifetime_months)

    return lifetime_df