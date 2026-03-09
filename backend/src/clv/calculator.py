import pandas as pd

def calculate_clv(
        df: pd.DataFrame,
        margin_rate: float
)->pd.DataFrame:
    
    required_columns= {
        "monthlycharges",
        "expected_remaining_months"
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise KeyError(f"Missing required columns for clv: {missing}")
    

    if not (0< margin_rate <=1):
        raise ValueError(f"margin_rate must be in (0,1]")
    
    clv_df = df.copy()

    clv_df["expected_monthly_margin"] = (
        clv_df["monthlycharges"] * margin_rate
    )

    clv_df["clv"] = (
        clv_df["expected_monthly_margin"] * clv_df["expected_remaining_months"]
    )

    if(clv_df["clv"] < 0).any():
        raise ValueError("Negative CLV values detected")
    
    return clv_df