import pandas as pd

def compute_skew_kurtosis(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame:
    summary = []

    for col in numeric_cols:
        summary.append({
            "feature": col,
            "skewness": df[col].skew(),
            "kurtosis": df[col].kurt(), 
        })

    return pd.DataFrame(summary)
