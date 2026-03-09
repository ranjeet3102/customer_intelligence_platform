from datetime import datetime, timezone
import yaml
import pandas as pd

from src.clv.data_loader import load_clv_inputs
from src.clv.survival import estimate_expected_lifetime
from src.clv.calculator import calculate_clv
from src.clv.writer import write_clv_snapshot
from src.clv.validation import validate_clv


def get_latest_snapshot_date() -> str:
    predictions_df = pd.read_parquet("data/predictions/churn_predictions.parquet")

    if predictions_df.empty:
        raise ValueError("Prediction store is empty, cannot infer snapshot_date")

    latest_snapshot = predictions_df["snapshot_date"].max()
    return str(latest_snapshot.date())


def run_clv() -> None:
    run_ts = datetime.now(timezone.utc)

    snapshot_date = get_latest_snapshot_date()

    with open("src/clv/config/clv.yaml", "r") as f:
        config = yaml.safe_load(f)["clv"]

    clv_df = load_clv_inputs(snapshot_date=snapshot_date)

    clv_df = estimate_expected_lifetime(
        df=clv_df,
        epsilon=config["epsilon"],
        max_lifetime_months=config["max_lifetime_months"],
    )

    clv_df = calculate_clv(
        df=clv_df,
        margin_rate=config["margin_rate"],
    )

    clv_df["clv_run_ts"] = run_ts

    write_clv_snapshot(
        df=clv_df,
        snapshot_date=snapshot_date,
    )

    validate_clv(clv_df)

    print(
        f"CLV pipeline completed successfully "
        f"for inferred snapshot_date={snapshot_date}"
    )


if __name__ == "__main__":
    run_clv()
