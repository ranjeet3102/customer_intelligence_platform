from pathlib import Path
from src.training.train_random_forest import train_random_forest

def main():

    feature_path= Path("data/features/churn_features_v1.parquet")
    model_output_dir= Path("artifacts/models/random_forest")

    metrics = train_random_forest(feature_path=feature_path, model_output_dir=model_output_dir)

    print("Random forest training Metrics:")

    for k,v in metrics.items():
        print(f"{k}: {v:.4f}")

if __name__=="__main__":
    main()
    