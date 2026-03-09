from pydantic import BaseModel
from typing import List
from datetime import datetime


class KPIResponse(BaseModel):
    total_customers: int
    high_risk_customers: int
    high_risk_pct: float
    avg_churn_probability: float
    total_clv: float
    clv_at_risk: float
    total_expected_savings: float
    total_incentive_cost: float
    net_retained_value: float
    roi: float


class DistributionItem(BaseModel):
    key: str
    value: float