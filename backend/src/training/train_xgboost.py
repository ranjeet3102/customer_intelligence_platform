import json 
import pandas as pd
from pathlib import Path
from typing import Dict
import  xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from src.training.data_loader import load_training_data

def train_xgboost(feature_path: Path, model_output_dir: Path, test_size: float=0.2, random_state: int=42) -> Dict[str, float]:

    X,y =load_training_data(feature_path)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=random_state)

    model=xgb.XGBClassifier(n_estimators=400, max_depths=6,
                            learning_rate=0.05, subsample=0.8,
                            colsample_bytree=0.8,objective="binary:logistic",
                             eval_metric="auc", scale_pos_weight=(y_train == 0).sum()/(y_train==1).sum(),
                              random_state=random_state, n_jobs=-1)
    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)
    y_prob = model.predict_proba(X_val)[:,1]

    metrics = {
        "accuracy": accuracy_score(y_val, y_pred),
        "precision": precision_score(y_val, y_pred),
        "recall": recall_score(y_val, y_pred),
        "roc_auc": roc_auc_score(y_val, y_prob)
    }

    model_output_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_output_dir/"xgboost.pkl"
   
    metrics_path = model_output_dir/"xgboost_metrics.json"

    pd.to_pickle(model,model_path)   

    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics


    