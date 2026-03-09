import json
import pickle
from pathlib import Path
from typing import Dict, Any

REGISTRY_PATH = Path("artifacts/model_registry/registry.json")

def load_production_model() -> Dict[str, Any]:

    if not REGISTRY_PATH.exists():
        raise FileNotFoundError("model registry not found")
    
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    production_models = [entry for entry in registry if entry["status"] == "production"]
    
    if not production_models:
        raise RuntimeError("No production model registered")
    
    production_entry = production_models[-1]
    
    model_path = Path(production_entry["model_path"])

    
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return {
        "model": model,
        "model_name": production_entry["model_name"],
        "model_type": production_entry["model_type"],
        "feature_version": production_entry["feature_version"],
        "metrics": production_entry["metrics"],
    }

