from pathlib import Path
from src.training.train_xgboost import train_xgboost

def main():

    feature_path = Path("data/features/churn_features_v1.parquet")
    model_output_dir=Path("artifacts/models/xgboost")

    metrics = train_xgboost(feature_path=feature_path, model_output_dir=model_output_dir)

    print("xgboost Training Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")


    
if __name__ == "__main__":
    main()