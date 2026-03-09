import json
from pathlib import Path
from src.model_registry.register import register_model

def main():

    model_dir  = Path("artifacts/models/random_forest")
    model_path = model_dir/"random_forest.pkl"
    metrics_path = model_dir/"random_forest_metrics.json"

    with open(metrics_path, "r") as f:
        metrics = json.load(f)

    feature_meta_path = Path("data/features/churn_features_v1.metadata.json")

    with open(feature_meta_path, "r") as f:
        feature_meta=json.load(f)

    dataset_hash = feature_meta["dataset_hash"]

    entry = register_model(
        model_name="churn_random_forest_v1",
        model_type="random_forest",
        model_path=model_path,
        metrics=metrics,
        feature_version="v1",
        dataset_hash=dataset_hash,
        status="production"
    )

    print("Model registered successfully:")
    print(entry)

if __name__ == "__main__":
    main()
