from pathlib import Path
import joblib
import logging

logger=logging.getLogger(__name__)
ENCODER_DIR=Path("artifacts/encoders")

def save_encoders(encoders: dict,features_version: str) -> None:

    ENCODER_DIR.mkdir(parents=True,exist_ok=True)

    for column,encoder in encoders.items():
        path=ENCODER_DIR/f"{column}_encoder_{features_version}.joblib"
        joblib.dump(encoder,path)
        logger.info(f"[Encoder] saved -> {path}")