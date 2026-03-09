from fastapi import APIRouter
from src.api.loaders.dashboard_loader import load_dashboard_df

router = APIRouter(prefix="/churn", tags=["churn"])


@router.get("/distribution")
def churn_distribution():
    df = load_dashboard_df()

    hist = (
        df["churn_probability"]
        .round(2)
        .value_counts()
        .sort_index()
        .to_dict()
    )

    return {"distribution": hist}


@router.get("/risk-value")
def risk_value_customers(group: str = "hr-lv"):
    df = load_dashboard_df()
    
    risk_map = {"hr": "high", "mr": "medium", "lr": "low"}
    value_map = {"hv": "high", "mv": "medium", "lv": "low"}
    
    parts = group.split("-")
    if len(parts) != 2 or parts[0] not in risk_map or parts[1] not in value_map:
        return []
        
    risk_bucket = risk_map[parts[0]]
    value_bucket = value_map[parts[1]]
    
    filtered = df[(df["risk_bucket"] == risk_bucket) & (df["value_bucket"] == value_bucket)]

    return filtered[
        [
            "customerid",
            "churn_probability",
            "clv",
            "segment_code",
            "persona",
        ]
    ].to_dict(orient="records")