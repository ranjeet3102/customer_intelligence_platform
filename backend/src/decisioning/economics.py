import pandas as pd


def apply_economics(
    df: pd.DataFrame,
    margin_rate: float = 0.7
) -> pd.DataFrame:
  
    df = df.copy()

    df["max_allowed_cost"] = df["clv"] * (1 - margin_rate)

    df["raw_incentive_cost"] = df["discount_pct"] * df["clv"]

    df["expected_savings"] = df["clv"] * df["churn_probability"]

    df["incentive_cost"] = df[
        ["raw_incentive_cost", "max_allowed_cost", "expected_savings"]
    ].min(axis=1)

    return df
