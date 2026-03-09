from fastapi import APIRouter
from src.api.loaders.dashboard_loader import load_dashboard_df

router = APIRouter(prefix="/clv", tags=["clv"])


@router.get("/distribution")
def clv_distribution():
    df = load_dashboard_df()
    return df["clv"].describe().to_dict()