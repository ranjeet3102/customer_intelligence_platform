import { useQuery } from "@tanstack/react-query";
import {
    RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
    Tooltip, ResponsiveContainer, ComposedChart, Bar, Line, XAxis,
    YAxis, CartesianGrid, Cell
} from "recharts";
import { fetchKPIs, fetchSnapshots } from "../api/client";
import KPICard from "../components/KPICard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorBanner from "../components/ErrorBanner";

function fmtGBP(n: number) {
    if (n >= 1_000_000) return `£${(n / 1_000_000).toFixed(2)}M`;
    if (n >= 1_000) return `£${(n / 1_000).toFixed(1)}K`;
    return `£${n.toFixed(0)}`;
}
function fmtPct(n: number) { return `${(n * 100).toFixed(1)}%`; }

function healthScore(kpis: {
    avg_churn_probability: number;
    high_risk_pct: number;
    roi: number;
}): number {
    const churnScore = (1 - kpis.avg_churn_probability) * 40;
    const riskScore = (1 - kpis.high_risk_pct) * 35;
    const roiScore = Math.min(kpis.roi / 5, 1) * 25;
    return Math.round(churnScore + riskScore + roiScore);
}

function scoreColor(score: number) {
    if (score >= 75) return "var(--green)";
    if (score >= 50) return "var(--orange)";
    return "var(--red)";
}

function scoreLabel(score: number) {
    if (score >= 75) return "Healthy";
    if (score >= 50) return "Moderate";
    return "At Risk";
}

export default function CustomerHealthPage() {
    const kpis = useQuery({ queryKey: ["kpis"], queryFn: fetchKPIs });
    const snapshots = useQuery({ queryKey: ["snapshots"], queryFn: fetchSnapshots });

    const score = kpis.data ? healthScore(kpis.data) : null;

    const radarData = kpis.data
        ? [
            { metric: "Low Churn Risk", A: Math.round((1 - kpis.data.avg_churn_probability) * 100) },
            { metric: "Low High-Risk %", A: Math.round((1 - kpis.data.high_risk_pct) * 100) },
            { metric: "CLV Health", A: Math.min(Math.round((kpis.data.total_clv / (kpis.data.total_customers * 1000)) * 100), 100) },
            { metric: "ROI", A: Math.min(Math.round((kpis.data.roi / 5) * 100), 100) },
            { metric: "Net Value", A: kpis.data.net_retained_value > 0 ? Math.min(Math.round((kpis.data.net_retained_value / kpis.data.total_expected_savings) * 100), 100) : 0 },
        ]
        : [];

    const metricsTable = kpis.data
        ? [
            { name: "Total Customers", value: kpis.data.total_customers.toLocaleString(), status: "info" },
            { name: "High-Risk Customers", value: kpis.data.high_risk_customers.toLocaleString(), status: kpis.data.high_risk_pct > 0.2 ? "bad" : "ok" },
            { name: "High-Risk %", value: fmtPct(kpis.data.high_risk_pct), status: kpis.data.high_risk_pct > 0.2 ? "bad" : "ok" },
            { name: "Avg Churn Probability", value: fmtPct(kpis.data.avg_churn_probability), status: kpis.data.avg_churn_probability > 0.4 ? "bad" : "ok" },
            { name: "Total CLV", value: fmtGBP(kpis.data.total_clv), status: "good" },
            { name: "CLV at Risk", value: fmtGBP(kpis.data.clv_at_risk), status: kpis.data.clv_at_risk / kpis.data.total_clv > 0.3 ? "bad" : "ok" },
            { name: "Expected Savings", value: fmtGBP(kpis.data.total_expected_savings), status: "good" },
            { name: "Incentive Cost", value: fmtGBP(kpis.data.total_incentive_cost), status: "info" },
            { name: "Net Retained Value", value: fmtGBP(kpis.data.net_retained_value), status: kpis.data.net_retained_value > 0 ? "good" : "bad" },
            { name: "ROI", value: `${kpis.data.roi.toFixed(2)}×`, status: kpis.data.roi > 2 ? "good" : kpis.data.roi > 1 ? "ok" : "bad" },
        ]
        : [];

    const statusColor: Record<string, string> = {
        good: "var(--green)",
        ok: "var(--orange)",
        bad: "var(--red)",
        info: "var(--accent-light)",
    };

    return (
        <div className="page-wrapper">
            {/* Health Score Hero */}
            {kpis.isLoading ? <LoadingSpinner /> : kpis.error ? <ErrorBanner /> : (
                <div style={{
                    display: "flex", alignItems: "stretch", gap: 20,
                }}>
                    {/* Score Card */}
                    <div className="chart-panel fade-in-up" style={{ flex: "0 0 260px", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "32px 24px" }}>
                        <div style={{ fontSize: 12, fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 16 }}>
                            Portfolio Health Score
                        </div>
                        <div style={{
                            width: 140, height: 140, borderRadius: "50%",
                            border: `6px solid ${scoreColor(score!)}`,
                            boxShadow: `0 0 40px ${scoreColor(score!)}40`,
                            display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
                            marginBottom: 16,
                        }}>
                            <span style={{ fontSize: 42, fontWeight: 800, color: scoreColor(score!), lineHeight: 1 }}>
                                {score}
                            </span>
                            <span style={{ fontSize: 12, color: "var(--text-secondary)", marginTop: 4 }}>/ 100</span>
                        </div>
                        <div style={{ fontSize: 18, fontWeight: 700, color: scoreColor(score!) }}>{scoreLabel(score!)}</div>
                        <div style={{ fontSize: 12, color: "var(--text-muted)", marginTop: 6, textAlign: "center" }}>
                            Composite score: churn risk, high-risk %, and ROI
                        </div>
                    </div>

                    {/* KPI Overview Radar */}
                    <div className="chart-panel fade-in-up" style={{ flex: 1 }}>
                        <div className="chart-panel-title">Health Dimensions</div>
                        <div className="chart-panel-sub">Multi-dimensional view of portfolio health (higher = better)</div>
                        <ResponsiveContainer width="100%" height={240}>
                            <RadarChart data={radarData}>
                                <PolarGrid stroke="var(--border-subtle)" />
                                <PolarAngleAxis dataKey="metric" tick={{ fill: "var(--text-secondary)", fontSize: 12 }} />
                                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: "var(--text-muted)", fontSize: 10 }} />
                                <Radar name="Health" dataKey="A" stroke={scoreColor(score!)} fill={scoreColor(score!)} fillOpacity={0.2} strokeWidth={2} />
                                <Tooltip
                                    contentStyle={{ background: "var(--bg-elevated)", border: "1px solid var(--border)", borderRadius: 8, color: "var(--text-primary)" }}
                                    formatter={(v: number) => [`${v}/100`, "Score"]}
                                />
                            </RadarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            )}

            {/* Quick KPI Row */}
            {kpis.data && (
                <div className="kpi-grid">
                    <KPICard label="Total Customers" value={kpis.data.total_customers.toLocaleString()} accentColor="var(--blue)" />
                    <KPICard label="High Risk %" value={fmtPct(kpis.data.high_risk_pct)}  accentColor="var(--red)" />
                    <KPICard label="Total CLV" value={fmtGBP(kpis.data.total_clv)}  accentColor="var(--green)" />
                    <KPICard label="ROI" value={`${kpis.data.roi.toFixed(2)}×`}  accentColor="var(--accent)" />
                </div>
            )}

            {/* Full Metrics Table */}
            <div className="chart-grid">
                <div className="table-panel fade-in-up">
                    <div className="table-panel-header">
                        <div className="section-title">All KPI Metrics</div>
                        <div className="section-sub">Complete health picture across all 10 indicators</div>
                    </div>
                    {kpis.isLoading ? <LoadingSpinner /> : kpis.error ? <ErrorBanner /> : (
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>Metric</th>
                                    <th>Value</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {metricsTable.map((row) => (
                                    <tr key={row.name}>
                                        <td style={{ display: "flex", alignItems: "center", gap: 8 }}>
                                            <span>{row.icon}</span> {row.name}
                                        </td>
                                        <td style={{ fontWeight: 600, color: "var(--text-primary)" }}>{row.value}</td>
                                        <td>
                                            <span className="badge" style={{
                                                background: `${statusColor[row.status]}18`,
                                                color: statusColor[row.status],
                                            }}>
                                                {row.status === "good" ? "✓ Good" : row.status === "ok" ? "~ Fair" : row.status === "bad" ? "✗ Alert" : "ℹ Info"}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>

                {/* Snapshots */}
                <div className="table-panel fade-in-up">
                    <div className="table-panel-header">
                        <div className="section-title">Available Snapshots</div>
                        <div className="section-sub">Historical data snapshots in the retention decisions store</div>
                    </div>
                    {snapshots.isLoading ? <LoadingSpinner /> : snapshots.error ? <ErrorBanner /> : (
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Snapshot Date</th>
                                    <th>Tag</th>
                                </tr>
                            </thead>
                            <tbody>
                                {snapshots.data!.snapshots.map((s, i, arr) => (
                                    <tr key={s}>
                                        <td style={{ color: "var(--text-muted)" }}>{i + 1}</td>
                                        <td style={{ fontFamily: "monospace", color: "var(--accent-light)" }}>{s}</td>
                                        <td>
                                            {i === arr.length - 1
                                                ? <span className="badge" style={{ background: "rgba(16,185,129,0.15)", color: "var(--green)" }}>Latest</span>
                                                : <span style={{ color: "var(--text-muted)", fontSize: 12 }}>Historical</span>
                                            }
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>
            </div>
        </div>
    );
}
