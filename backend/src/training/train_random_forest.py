import json
import yaml
import pandas as pd
from pathlib import Path
from typing import Dict
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score, recall_score, roc_auc_score
from src.training.data_loader import load_training_data
from src.training.evaluate.threshold_selection import select_threshold_by_recall

def train_random_forest(feature_path: Path, model_output_dir: Path,test_size:float=0.2, random_state: int=42) -> Dict[str, float]:

    X,y = load_training_data(feature_path)

    X_train ,X_val,y_train, y_val = train_test_split(X,y,test_size=test_size, random_state=random_state,stratify=y)

    model = RandomForestClassifier(n_estimators=300, max_depth=None, min_samples_split=20, min_samples_leaf=10, class_weight="balanced", random_state=random_state, n_jobs=1)

    model.fit(X_train ,y_train)

    y_pred= model.predict(X_val)
    y_prob=model.predict_proba(X_val)[:,1]

    # import numpy as np

    # print("Min prob:", y_prob.min())
    # print("Max prob:", y_prob.max())
    # print("Mean prob:", y_prob.mean())
    # print("90th pct:", np.percentile(y_prob, 90))
    # print("95th pct:", np.percentile(y_prob, 95))
    # print("99th pct:", np.percentile(y_prob, 99))

    # print(y.value_counts(normalize=True))


    TARGET = 0.7
    metrics = {
        "accuracy": accuracy_score(y_val, y_pred),
        "precision": precision_score(y_val, y_pred),
        "recall": recall_score(y_val, y_pred),
        "roc_auc": roc_auc_score(y_val, y_prob)
    }

    model_output_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_output_dir/"random_forest.json"
    metrics_path=model_output_dir/"random_forest_metrics.json"
    pd.to_pickle(model, model_path)

    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    
    threshold_info = select_threshold_by_recall(
    y_true=y_val,
    y_pred_proba=y_prob,
    target_recall=TARGET
)
    inference_config ={
        "churn":{
            "threshold":  round(threshold_info["threshold"],3),
            "recall": threshold_info["recall"],
            "objective": f"recall >= {TARGET}",
            "decided_in": "phase_3_validation"
        }
    }

    inference_config_path = Path("src/inference/config/inference.yaml")
    inference_config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(inference_config_path, "w") as f:
        yaml.safe_dump(inference_config, f, sort_keys=False)

    return metrics

