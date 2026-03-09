import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.training.model_loader import load_production_model

NON_FEATURE_COLUMNS = {
    "customerid",
    "snapshot_date",
    "feature_version",
    "source",
    "churn"
}

def generate_predictions(feature_df: pd.DataFrame) -> pd.DataFrame:

    model, model_metadata = load_production_model()

    feature_cols = [col for col in feature_df.columns if col not in NON_FEATURE_COLUMNS]

    X = feature_df[feature_cols]

    churn_probs = model.predict_proba(X)[:, 1]

    predictions_df = pd.DataFrame({
        "customerid": feature_df["customerid"],
        "churn_probability":  churn_probs,
        "model_version": model_metadata["feature_version"]
    })

    return predictions_df


