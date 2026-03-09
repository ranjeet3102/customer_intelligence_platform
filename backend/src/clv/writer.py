from pathlib import Path
import pandas as pd

CLV_STORE_PATH = Path("data/clv")

def write_clv_snapshot(df:pd.DataFrame,snapshot_date:str) ->None:

    required_columns = {
        "customerid",
        "snapshot_date",
        "clv",
        "model_version",
        "feature_version"
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise KeyError(f"Missing required CLV columns: {missing}")

    CLV_STORE_PATH.mkdir(parents=True, exist_ok=True)

    clv_path = CLV_STORE_PATH / "clv.parquet"

    if clv_path.exists():
        existing_df = pd.read_parquet(clv_path)

        existing_df = existing_df[
            existing_df["snapshot_date"] != snapshot_date
        ]

        final_df = pd.concat([existing_df, df], ignore_index=True)

    else:

        final_df =df

    final_df.to_parquet(clv_path,index=False)

    

    