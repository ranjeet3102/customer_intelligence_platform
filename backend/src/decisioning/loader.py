from pathlib import Path
import pandas as pd

PREDICTIONS_PATH = Path("data/predictions/churn_predictions.parquet")
CLV_PATH = Path("data/clv/clv.parquet")
SEGMENTATION_PATH = Path("data/segmentation/segmentation.parquet")





def load_decision_input(snapshot_date: str | None = None) -> pd.DataFrame:
  

    preds = pd.read_parquet(PREDICTIONS_PATH)
    clv = pd.read_parquet(CLV_PATH)
    seg = pd.read_parquet(SEGMENTATION_PATH)

    if "clv" in seg.columns:
        seg = seg.drop(columns=["clv"])


    if "customerid" in preds.columns:
        preds = preds.rename(columns={"customerid": "customerid"})

    if snapshot_date is not None:
        snapshot_date = pd.to_datetime(snapshot_date)
        preds = preds[preds["snapshot_date"] == snapshot_date]
        clv = clv[clv["snapshot_date"] == snapshot_date]
        seg = seg[seg["snapshot_date"] == snapshot_date]
    else:
        common_snapshots = (
            set(preds["snapshot_date"])
            & set(clv["snapshot_date"])
            & set(seg["snapshot_date"])
        )

        if not common_snapshots:
            raise ValueError("No common snapshot_date across decision inputs")

        snapshot_date = max(common_snapshots)
        preds = preds[preds["snapshot_date"] == snapshot_date]
        clv = clv[clv["snapshot_date"] == snapshot_date]
        seg = seg[seg["snapshot_date"] == snapshot_date]

    df = (
        preds
        .merge(clv, on=["customerid", "snapshot_date"], how="inner")
        .merge(seg, on=["customerid", "snapshot_date"], how="inner")
    )

    if df.empty:
        raise ValueError("Decision input dataframe is empty after joins")

    return df
