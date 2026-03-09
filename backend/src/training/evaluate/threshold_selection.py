import pandas as pd
from sklearn.metrics import precision_recall_curve

def select_threshold_by_recall(y_true, y_pred_proba, target_recall: float)->dict:

    precision, recall, thresholds = precision_recall_curve(
        y_true,
        y_pred_proba
    )

    pr_df = pd.DataFrame({
        "threshold": thresholds,
        "precision": precision[:-1],
        "recall":recall[:-1]
    })

    candidates = pr_df[pr_df["recall"] >= target_recall]

    if candidates.empty:
        raise ValueError(f"No threshold achieves recall >= {target_recall}")
    
    chosen = candidates.sort_values("threshold",ascending=False).iloc[0]

    return {
        "threshold": float(chosen["threshold"]),
        "precision": float(chosen["precision"]),
        "recall": float(chosen["recall"])
    }