from fastapi import APIRouter
from src.api.loaders.dashboard_loader import load_dashboard_df

router = APIRouter(prefix="/segments", tags=["segmentation"])


@router.get("/distribution")
def segment_distribution():
    df = load_dashboard_df()
    return df["segment_code"].value_counts().to_dict()