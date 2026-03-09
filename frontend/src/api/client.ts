import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 10000,
});

export interface KPIResponse {
  total_customers: number;
  high_risk_customers: number;
  high_risk_pct: number;
  avg_churn_probability: number;
  total_clv: number;
  clv_at_risk: number;
  total_expected_savings: number;
  total_incentive_cost: number;
  net_retained_value: number;
  roi: number;
}

export interface HighRiskCustomer {
  customerid: string;
  churn_probability: number;
  clv: number;
  segment_code: string;
  persona: string;
}

export interface ChurnDistribution {
  distribution: Record<string, number>;
}

export interface CLVStats {
  count: number;
  mean: number;
  std: number;
  min: number;
  "25%": number;
  "50%": number;
  "75%": number;
  max: number;
}

export interface SnapshotsResponse {
  snapshots: string[];
}



export const fetchKPIs = (): Promise<KPIResponse> =>
  api.get("/kpis").then((r) => r.data);

export const fetchChurnDistribution = (): Promise<ChurnDistribution> =>
  api.get("/churn/distribution").then((r) => r.data);

export const fetchRiskValue = (group: string = "hr-lv"): Promise<HighRiskCustomer[]> =>
  api.get(`/churn/risk-value?group=${group}`).then((r) => r.data);

export const fetchCLVDistribution = (): Promise<CLVStats> =>
  api.get("/clv/distribution").then((r) => r.data);

export const fetchSegmentDistribution = (): Promise<Record<string, number>> =>
  api.get("/segments/distribution").then((r) => r.data);

export const fetchRetentionActions = (): Promise<Record<string, number>> =>
  api.get("/retention/actions").then((r) => r.data);

export const fetchSnapshots = (): Promise<SnapshotsResponse> =>
  api.get("/snapshots").then((r) => r.data);
