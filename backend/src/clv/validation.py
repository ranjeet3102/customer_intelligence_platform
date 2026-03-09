import pandas as pd
import numpy as np


def validate_clv(df: pd.DataFrame) -> None:

    required_columns = {
        "customerid",
        "snapshot_date",
        "churn_probability",
        "expected_remaining_months",
        "monthlycharges",
        "clv"
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise KeyError(f"Missing CLV validation columns: {missing}")
    
    if df.isnull().any().any():
        raise ValueError("Null values detected in CLV output")

    if df.duplicated(subset=["customerid", "snapshot_date"]).any():
        raise ValueError("Duplicate customerid + snapshot_date rows found")

    if df["snapshot_date"].nunique() != 1:
        raise ValueError("Multiple snapshot_dates found in CLV validation run")
    

    if (df["churn_probability"] <= 0).any() or (df["churn_probability"] > 1).any():
        raise ValueError("Invalid churn_probability values detected")

    if (df["expected_remaining_months"] <= 0).any():
        raise ValueError("Non-positive expected_remaining_months detected")

    if (df["clv"] < 0).any():
        raise ValueError("Negative CLV values detected")

    if not np.isfinite(df["clv"]).all():
        raise ValueError("Non-finite CLV values detected")
    
    churn_lifetime_corr = df["churn_probability"].corr(
        df["expected_remaining_months"]
    )

    churn_clv_corr = df["churn_probability"].corr(df["clv"])

    if churn_lifetime_corr >= 0:
        raise ValueError(
            f"Expected negative correlation between churn and lifetime, got {churn_lifetime_corr:.3f}"
        )

    if churn_clv_corr >= 0:
        raise ValueError(
            f"Expected negative correlation between churn and CLV, got {churn_clv_corr:.3f}"
        )
    
    clv_quantiles = df["clv"].quantile([0.5, 0.9, 0.99])

    if clv_quantiles.loc[0.99] > 10 * clv_quantiles.loc[0.9]:
        raise ValueError("Extreme CLV tail detected (possible cap or epsilon issue)")

    high_churn_top_clv = df[
        (df["churn_probability"] > 0.8)
        & (df["clv"] > clv_quantiles.loc[0.9])
    ]

    if not high_churn_top_clv.empty:
        raise ValueError(
            "High churn customers appearing in top CLV segment"
        )
    