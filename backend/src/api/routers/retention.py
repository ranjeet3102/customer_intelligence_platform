from fastapi import APIRouter
from src.api.loaders.dashboard_loader import load_dashboard_df

router = APIRouter(prefix="/retention", tags=["retention"])


@router.get("/actions")
def action_distribution():
    df = load_dashboard_df()
    return df["action_type"].value_counts().to_dict()