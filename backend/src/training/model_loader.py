# import pandas as pd
# from pathlib import Path
# import pickle
# import json

# MODEL_REGISTRY_PATH = Path("artifacts/model_registry/registry.json")

# def load_production_model():

#     if not MODEL_REGISTRY_PATH.exists():
#             raise FileNotFoundError(f"Model registry not found at {MODEL_REGISTRY_PATH}")

#     with open(MODEL_REGISTRY_PATH, "r") as f:
#         registry = json.load(f)

#     production_model = [entry for entry in registry if entry.get("status")=="production"]

#     if not production_model:
#         raise ValueError("No production model found in registry")

# # if len(production_model) > 1:
# #     raise ValueError("Multiple production models found — registry invalid")


#     model_entry = production_model[-1]
# # model_entry = production_model[0]

#     model_path = Path(model_entry["model_path"])

#     if not model_path.exists():
#         raise FileNotFoundError(f"Model file not found at {model_path}")    

#     with open(model_path, "rb") as f:
#         model = pickle.load(f)

#     return model,model_entry

import json
import pickle
from pathlib import Path


MODEL_REGISTRY_PATH = Path("artifacts/model_registry/registry.json")


def load_production_model():

    # verify registry exists
    if not MODEL_REGISTRY_PATH.exists():
        raise FileNotFoundError(
            f"Model registry not found at {MODEL_REGISTRY_PATH}"
        )

    # load registry
    with open(MODEL_REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    # find production models
    production_models = [
        entry for entry in registry if entry.get("status") == "production"
    ]

    if not production_models:
        raise ValueError("No production model found in registry")

    # select latest production model
    model_entry = production_models[-1]

    # read model path from registry
    raw_model_path = model_entry["model_path"]

    # convert Windows path → Linux path
    model_rel_path = Path(raw_model_path.replace("\\", "/"))

    # backend root directory
    BASE_DIR = Path(__file__).resolve().parents[2]

    # final model path
    model_path = BASE_DIR / model_rel_path

    # validate path exists
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found at {model_path}"
        )

    # load model
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return model, model_entry