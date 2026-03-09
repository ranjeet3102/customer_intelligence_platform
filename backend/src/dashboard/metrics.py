import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        raise ValueError("Dashboard dataframe is empty")

    total_customers = df["customerid"].nunique()

    high_risk_mask = df["risk_bucket"] == "high"
    high_risk_customers = high_risk_mask.sum()

    avg_churn_probability = df["churn_probability"].mean()

    total_clv = df["clv"].sum()

    clv_at_risk = (df["clv"] * df["churn_probability"]).sum()

    total_expected_savings = df["expected_savings"].sum()
    total_incentive_cost = df["incentive_cost"].sum()

    net_retained_value = total_expected_savings - total_incentive_cost

    roi = (
        total_expected_savings / total_incentive_cost
        if total_incentive_cost > 0
        else 0.0
    )

    return {
        "total_customers": int(total_customers),
        "high_risk_customers": int(high_risk_customers),
        "high_risk_pct": high_risk_customers / total_customers,
        "avg_churn_probability": avg_churn_probability,
        "total_clv": total_clv,
        "clv_at_risk": clv_at_risk,
        "total_expected_savings": total_expected_savings,
        "total_incentive_cost": total_incentive_cost,
        "net_retained_value": net_retained_value,
        "roi": roi,
    }