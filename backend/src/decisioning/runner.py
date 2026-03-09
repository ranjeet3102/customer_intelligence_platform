from datetime import datetime, timezone

from src.decisioning.loader import load_decision_input
from src.decisioning.rules import apply_retention_rules
from src.decisioning.economics import apply_economics
from src.decisioning.validator import validate_decisions
from src.decisioning.writer import write_decisions


def run_retention_decisioning(snapshot_date: str | None = None) -> None:
    run_ts = datetime.now(timezone.utc)

    df = load_decision_input(snapshot_date)
   

    df = apply_retention_rules(df)
    df = apply_economics(df)

    df["decision_ts"] = run_ts

    validate_decisions(df)
    write_decisions(df)

if __name__ == "__main__":
    run_retention_decisioning()
