from pathlib import Path
from src.training.train_logistic import train_logistic_regression

def main():
    feature_path = Path("data/features/churn_features_v1.parquet")
    model_output_dir = Path("artifacts/models/logistic")

    metrics = train_logistic_regression(feature_path=feature_path, model_output_dir=model_output_dir)

    print("Logistic Regression Training Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")


if __name__=="__main__":
    main()