from pathlib import Path
from src.training.compare_models import load_metrics, compare_models


def main():

    base_dir = Path("artifacts/models")

    metrics = {
        "logistic": load_metrics(base_dir/"logistic","logistic_regression"),
        "random_forest": load_metrics(base_dir/"random_forest","random_forest"),
        "xgboost":load_metrics(base_dir/"xgboost","xgboost")
    }

    comparison_df = compare_models(metrics)

    print("\nModel Comparison:")
    print(comparison_df)

    comparison_df.to_csv("artifacts/model_comparison.csv") 

if __name__=="__main__":
    main()