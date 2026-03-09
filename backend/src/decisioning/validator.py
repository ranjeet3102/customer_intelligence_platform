import pandas as pd


REQUIRED_COLUMNS = {
    "customerid",
    "snapshot_date",
    "action_type",
    "discount_pct",
    "incentive_cost",
    "expected_savings",
    "policy_version",
}


def validate_decisions(df: pd.DataFrame) -> None:
    
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df.duplicated(subset=["customerid", "snapshot_date"]).any():
        raise ValueError("Duplicate decisions for customer and snapshot")

    required_cols = list(REQUIRED_COLUMNS)

    if df[required_cols].isnull().any().any():
        raise ValueError("Null values detected in required decision fields")

    

    if (df["discount_pct"] < 0).any():
        raise ValueError("Negative discount percentage detected")

    if (df["incentive_cost"] < 0).any():
        raise ValueError("Negative incentive cost detected")

    violations = df["incentive_cost"] > df["expected_savings"]
    if violations.any():
        bad_rows = df.loc[violations, ["customerid", "incentive_cost", "expected_savings"]]
        raise ValueError(
            f"Negative ROI decisions detected:\n{bad_rows.head()}"
        )
