import yaml
from pathlib import Path

from src.segmentation.data_loader import load_segmentation_base
from src.segmentation.bucketing import apply_segmentation
from src.segmentation.personas import assign_persona
from src.segmentation.validator import run_segmentation_validation
from src.segmentation.writer import write_segmentation


CONFIG_PATH = Path("src/segmentation/config/segmentation.yaml")


def run_segmentation() -> None:
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    df = load_segmentation_base()

    df = apply_segmentation(df, config)

    df["persona"] = assign_persona(df["segment_code"])

    run_segmentation_validation(df, config)

    write_segmentation(
        df=df,
        segment_version=config["segment_version"],
    )


if __name__ == "__main__":
    run_segmentation()
