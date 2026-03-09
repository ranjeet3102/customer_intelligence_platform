import { useQuery } from "@tanstack/react-query";
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
    ResponsiveContainer, Cell
} from "recharts";
import { fetchKPIs, fetchRetentionActions } from "../api/client";
import KPICard from "../components/KPICard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorBanner from "../components/ErrorBanner";

function fmtGBP(n: number) {
    if (n >= 1_000_000) return `£${(n / 1_000_000).toFixed(2)}M`;
    if (n >= 1_000) return `£${(n / 1_000).toFixed(1)}K`;
    return `£${n.toFixed(0)}`;
}

const ACTION_COLORS: Record<string, string> = {
    discount: "#7c3aed",
    loyalty_bonus: "#10b981",
    no_action: "#475569",
    premium_offer: "#3b82f6",
    free_trial: "#f59e0b",
    retention_call: "#ec4899",
};

export default function RetentionPage() {
    const kpis = useQuery({ queryKey: ["kpis"], queryFn: fetchKPIs });
    const actions = useQuery({ queryKey: ["retentionActs"], queryFn: fetchRetentionActions });

    const actionData = actions.data
        ? Object.entries(actions.data)
            .map(([name, count]) => ({ name, count }))
            .sort((a, b) => b.count - a.count)
        : [];

    const totalActions = actionData.reduce((s, d) => s + d.count, 0);
    const activeActions = actionData.filter((d) => d.name !== "no_action").reduce((s, d) => s + d.count, 0);

    return (
        <div className="page-wrapper">
            {/* KPI Cards */}
            <div className="kpi-grid">
                {kpis.isLoading ? <LoadingSpinner /> : kpis.error ? <ErrorBanner /> : (
                    <>
                        <KPICard
                            label="Expected Savings"
                            value={fmtGBP(kpis.data!.total_expected_savings)}
                            icon="💰"
                            accentColor="var(--green)"
                            subtext="Revenue preserved by retention"
                        />
                        <KPICard
                            label="Incentive Cost"
                            value={fmtGBP(kpis.data!.total_incentive_cost)}
                            icon="💸"
                            accentColor="var(--orange)"
                            subtext="Total cost of retention offers"
                        />
                        <KPICard
                            label="Net Retained Value"
                            value={fmtGBP(kpis.data!.net_retained_value)}
                            icon="📈"
                            accentColor="var(--blue)"
                            subtext="Savings minus cost"
                        />
                        <KPICard
                            label="ROI"
                            value={`${kpis.data!.roi.toFixed(2)}×`}
                            icon="🎯"
                            accentColor="var(--accent)"
                            subtext="Return on retention investment"
                        />
                    </>
                )}
                {actions.data && (
                    <>
                        <KPICard
                            label="Active Interventions"
                            value={activeActions.toLocaleString()}
                            icon="⚡"
                            accentColor="var(--pink)"
                            subtext="Customers receiving an action"
                        />
                        <KPICard
                            label="No Action Needed"
                            value={(totalActions - activeActions).toLocaleString()}
                            icon="✅"
                            accentColor="var(--text-muted)"
                            subtext="Low-risk customers"
                        />
                    </>
                )}
            </div>

            {/* ROI Economics Panel */}
            {kpis.data && (
                <div className="chart-panel fade-in-up">
                    <div className="chart-panel-title">Retention Economics Overview</div>
                    <div className="chart-panel-sub">Visual comparison of savings, cost and net value</div>
                    <ResponsiveContainer width="100%" height={220}>
                        <BarChart
                            data={[
                                { name: "Expected Savings", value: kpis.data.total_expected_savings, fill: "#10b981" },
                                { name: "Incentive Cost", value: kpis.data.total_incentive_cost, fill: "#ef4444" },
                                { name: "Net Retained Value", value: kpis.data.net_retained_value, fill: "#7c3aed" },
                            ]}
                            margin={{ top: 4, right: 12, left: 20, bottom: 0 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
                            <XAxis dataKey="name" tick={{ fill: "var(--text-muted)", fontSize: 12 }} />
                            <YAxis tickFormatter={fmtGBP} tick={{ fill: "var(--text-muted)", fontSize: 11 }} />
                            <Tooltip
                                contentStyle={{ background: "var(--bg-elevated)", border: "1px solid var(--border)", borderRadius: 8, color: "var(--text-primary)" }}
                                formatter={(v: number) => [fmtGBP(v), ""]}
                            />
                            <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                                {[
                                    { fill: "#10b981" },
                                    { fill: "#ef4444" },
                                    { fill: "#7c3aed" },
                                ].map((entry, i) => (
                                    <Cell key={i} fill={entry.fill} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            )}

            {/* Action Distribution */}
            <div className="chart-grid">
                <div className="chart-panel fade-in-up">
                    <div className="chart-panel-title">Retention Action Distribution</div>
                    <div className="chart-panel-sub">Number of customers assigned each action type</div>
                    {actions.isLoading ? <LoadingSpinner /> : actions.error ? <ErrorBanner /> : (
                        <ResponsiveContainer width="100%" height={260}>
                            <BarChart data={actionData} margin={{ top: 4, right: 12, left: 0, bottom: 40 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
                                <XAxis dataKey="name" tick={{ fill: "var(--text-muted)", fontSize: 11 }} angle={-20} textAnchor="end" />
                                <YAxis tick={{ fill: "var(--text-muted)", fontSize: 11 }} />
                                <Tooltip
                                    contentStyle={{ background: "var(--bg-elevated)", border: "1px solid var(--border)", borderRadius: 8, color: "var(--text-primary)" }}
                                    formatter={(v: number) => [v.toLocaleString(), "Customers"]}
                                />
                                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                                    {actionData.map((entry, i) => (
                                        <Cell key={i} fill={ACTION_COLORS[entry.name] ?? "#7c3aed"} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    )}
                </div>

                {/* Action Table */}
                <div className="table-panel fade-in-up" style={{ borderRadius: "var(--radius-lg)" }}>
                    <div className="table-panel-header">
                        <div className="section-title">Action Breakdown</div>
                        <div className="section-sub">Count and share of each retention action</div>
                    </div>
                    {actions.isLoading ? <LoadingSpinner /> : actions.error ? <ErrorBanner /> : (
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>Action Type</th>
                                    <th>Customers</th>
                                    <th>Share</th>
                                </tr>
                            </thead>
                            <tbody>
                                {actionData.map((a, i) => (
                                    <tr key={a.name}>
                                        <td style={{ display: "flex", alignItems: "center", gap: 8 }}>
                                            <span style={{
                                                width: 10, height: 10, borderRadius: "50%",
                                                background: ACTION_COLORS[a.name] ?? "#7c3aed",
                                                display: "inline-block", flexShrink: 0
                                            }} />
                                            {a.name.replace(/_/g, " ")}
                                        </td>
                                        <td style={{ fontWeight: 600 }}>{a.count.toLocaleString()}</td>
                                        <td style={{ color: "var(--accent-light)" }}>
                                            {totalActions > 0 ? `${((a.count / totalActions) * 100).toFixed(1)}%` : "—"}
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
