from fastapi import APIRouter
from src.api.loaders.dashboard_loader import load_dashboard_df
from src.api.schemas.dashboard import KPIResponse

router = APIRouter(prefix="/kpis", tags=["kpis"])


@router.get("", response_model=KPIResponse)
def get_kpis():
    df = load_dashboard_df()

    total_customers = df["customerid"].nunique()
    high_risk = (df["risk_bucket"] == "high").sum()

    total_expected_savings = df["expected_savings"].sum()
    total_incentive_cost = df["incentive_cost"].sum()

    roi = (
        total_expected_savings / total_incentive_cost
        if total_incentive_cost > 0
        else 0.0
    )

    return KPIResponse(
        total_customers=total_customers,
        high_risk_customers=high_risk,
        high_risk_pct=high_risk / total_customers,
        avg_churn_probability=df["churn_probability"].mean(),
        total_clv=df["clv"].sum(),
        clv_at_risk=(df["clv"] * df["churn_probability"]).sum(),
        total_expected_savings=total_expected_savings,
        total_incentive_cost=total_incentive_cost,
        net_retained_value=total_expected_savings - total_incentive_cost,
        roi=roi,
    )