import pandas as pd

SEGMENT_TO_PERSONA = {
    # High Risk
    "HR-HV": "At-Risk Champions",
    "HR-MV": "At-Risk Regulars",
    "HR-LV": "Fading Users",

    # Medium Risk
    "MR-HV": "Vulnerable High-Value",
    "MR-MV": "Neutral Core",
    "MR-LV": "Price-Sensitive",

    # Low Risk
    "LR-HV": "Loyal Gold",
    "LR-MV": "Stable Users",
    "LR-LV": "Passive Users",
}

def assign_persona(segment_code: pd.Series) -> pd.Series:

    personas = segment_code.map(SEGMENT_TO_PERSONA)

    if personas.isnull().any():
        unknown = segment_code[personas.isnull()].unique().tolist()
        raise ValueError(
            f"Unknown segment codes encountered: {unknown}"
        )

    return personas

