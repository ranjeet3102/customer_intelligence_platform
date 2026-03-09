import yaml
import pandas as pd
from pathlib import Path

POLICY_PATH = Path("src/decisioning/config/retention.yaml")


def load_policy() -> dict:
    with open(POLICY_PATH, "r") as f:
        return yaml.safe_load(f)


def apply_retention_rules(df: pd.DataFrame) -> pd.DataFrame:
    

    policy = load_policy()
    policy_version = policy["policy"]["policy_version"]
    actions = policy["actions"]

    df = df.copy()

    def resolve_action(row):
        risk = f"{row['risk_bucket']}_risk"
        value = f"{row['value_bucket']}_value"

        rule = actions.get(risk, {}).get(value)

        if rule is None:
            raise ValueError(
                f"No retention rule defined for risk={risk}, value={value}"
            )

        return (
            rule["action_type"],
            rule["discount_pct"],
            rule["reason"]
        )

    resolved = df.apply(resolve_action, axis=1, result_type="expand")
    resolved.columns = ["action_type", "discount_pct", "decision_reason"]

    df = pd.concat([df, resolved], axis=1)
    df["policy_version"] = policy_version

    return df
