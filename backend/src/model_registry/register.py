import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict

REGISTRY_PATH = Path("artifacts/model_registry/registry.json")

def register_model(
        model_name: str,
        model_type: str,
        model_path: Path,
        metrics: Dict[str, float],
        feature_version: str,
        dataset_hash: str,
        status: str =  "candidate",
) -> Dict:
    

    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

    if REGISTRY_PATH.exists():

        with open(REGISTRY_PATH, "r") as f:
            registry = json.load(f)

    else:
        registry = []

    entry = {
        "model_name": model_name,
        "model_type": model_type,
        "model_path": str(model_path),
        "feature_version": feature_version,
        "datset_hash": dataset_hash,
        "metrics": metrics,
        "status": status,
        "registered_utc": datetime.now(timezone.utc).isoformat()
                }
    
    registry.append(entry)

    with open(REGISTRY_PATH,"w") as f:
        json.dump(registry, f, indent=2)

    return entry
