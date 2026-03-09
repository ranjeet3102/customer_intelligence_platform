import json
from pathlib import Path
import pandas as pd


def load_metrics(model_dir: Path, model_name: str)-> dict:

    metrics_path = model_dir/f"{model_name}_metrics.json"
    if not metrics_path.exists():
        raise FileNotFoundError(f"Missing metrics for {model_name}")
    
    with open(metrics_path, "r") as f:
        return json.load(f)
    

def compare_models(metrics_by_models: dict) -> pd.DataFrame:

    df = pd.DataFrame.from_dict(metrics_by_models, orient="index")
    df = df.sort_values(by="roc_auc", ascending=False)

    return df



