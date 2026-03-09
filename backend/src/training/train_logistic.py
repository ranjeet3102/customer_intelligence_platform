import json
from pathlib import Path
from typing import Dict
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score,recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from src.training.data_loader import load_training_data

def train_logistic_regression(feature_path: Path,model_output_dir:Path,test_size: float=0.2,random_state: int=42,) -> Dict[str,float]: 

    X,y=load_training_data(feature_path)

    X_train, X_val, y_train, y_val = train_test_split(X,y,test_size=test_size,random_state=random_state,stratify=y)

    model=LogisticRegression(max_iter=1000,class_weight="balanced",n_jobs=1,random_state=random_state)

    model.fit(X_train,y_train)


    y_pred = model.predict(X_val)
    y_prob = model.predict_proba(X_val)[:,1]
    print(y_prob)

    mertics={
        "accuracy": accuracy_score(y_val, y_pred),
        "precision": precision_score(y_val, y_pred),
        "recall": recall_score(y_val, y_pred),
        "roc_auc": roc_auc_score(y_val, y_prob)
    }

    model_output_dir.mkdir(parents=True,exist_ok=True)

    model_path=model_output_dir/"logistic_regression.pkl"
    metrics_path=model_output_dir/"logistic_regression_metrics.json"

    pd.to_pickle(model,model_path)

    with open(metrics_path, "w") as f:
        json.dump(mertics,f,indent=2)

    return mertics