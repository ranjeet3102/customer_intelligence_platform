import { useQuery } from "@tanstack/react-query";
import {
    PieChart, Pie, Cell, Tooltip, Legend,
    BarChart, Bar, XAxis, YAxis, CartesianGrid,
    ResponsiveContainer
} from "recharts";
import { fetchSegmentDistribution } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorBanner from "../components/ErrorBanner";
import KPICard from "../components/KPICard";

const PALETTE = ["#7c3aed", "#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#06b6d4", "#ec4899", "#8b5cf6"];

const RADIAN = Math.PI / 180;
const renderLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, name }: any) => {
    if (percent < 0.05) return null;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);
    return (
        <text x={x} y={y} fill="white" textAnchor="middle" dominantBaseline="central" fontSize={11} fontWeight={600}>
            {`${(percent * 100).toFixed(0)}%`}
        </text>
    );
};

export default function SegmentationPage() {
    const segments = useQuery({ queryKey: ["segments"], queryFn: fetchSegmentDistribution });

    const pieData = segments.data
        ? Object.entries(segments.data).map(([name, value]) => ({ name, value }))
        : [];

    const barData = [...pieData].sort((a, b) => b.value - a.value);
    const total = pieData.reduce((s, d) => s + d.value, 0);

    return (
        <div className="page-wrapper">
            {/* KPI Cards */}
            {segments.isLoading ? <LoadingSpinner /> : segments.error ? <ErrorBanner /> : (
                <div className="kpi-grid">
                    <KPICard
                        label="Total Segments"
                        value={pieData.length}
                        icon="🗂️"
                        accentColor="var(--accent)"
                        subtext="Distinct customer segments"
                    />
                    <KPICard
                        label="Largest Segment"
                        value={barData[0]?.name ?? "—"}
                        icon="🏆"
                        accentColor="var(--blue)"
                        subtext={`${barData[0]?.value.toLocaleString()} customers`}
                    />
                    <KPICard
                        label="Smallest Segment"
                        value={barData[barData.length - 1]?.name ?? "—"}
                        icon="🔍"
                        accentColor="var(--cyan)"
                        subtext={`${barData[barData.length - 1]?.value.toLocaleString()} customers`}
                    />
                    <KPICard
                        label="Total Customers"
                        value={total.toLocaleString()}
                        icon="👥"
                        accentColor="var(--green)"
                        subtext="Across all segments"
                    />
                </div>
            )}

            {/* Charts */}
            <div className="chart-grid">
                <div className="chart-panel fade-in-up">
                    <div className="chart-panel-title">Segment Share — Pie Chart</div>
                    <div className="chart-panel-sub">Proportional breakdown of customers per segment</div>
                    {segments.isLoading ? <LoadingSpinner /> : segments.error ? <ErrorBanner /> : (
                        <ResponsiveContainer width="100%" height={280}>
                            <PieChart>
                                <Pie
                                    data={pieData}
                                    cx="50%"
                                    cy="50%"
                                    outerRadius={110}
                                    innerRadius={50}
                                    dataKey="value"
                                    labelLine={false}
                                    label={renderLabel}
                                >
                                    {pieData.map((_, i) => (
                                        <Cell key={i} fill={PALETTE[i % PALETTE.length]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ background: "var(--bg-elevated)", border: "1px solid var(--border)", borderRadius: 8, color: "var(--text-primary)" }}
                                    formatter={(v: number) => [v.toLocaleString(), "Customers"]}
                                />
                                <Legend wrapperStyle={{ color: "var(--text-secondary)", fontSize: 12 }} />
                            </PieChart>
                        </ResponsiveContainer>
                    )}
                </div>

                <div className="chart-panel fade-in-up">
                    <div className="chart-panel-title">Segment Size — Bar Chart</div>
                    <div className="chart-panel-sub">Absolute customer count per segment, sorted by size</div>
                    {segments.isLoading ? <LoadingSpinner /> : segments.error ? <ErrorBanner /> : (
                        <ResponsiveContainer width="100%" height={280}>
                            <BarChart data={barData} layout="vertical" margin={{ top: 4, right: 16, left: 60, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" horizontal={false} />
                                <XAxis type="number" tick={{ fill: "var(--text-muted)", fontSize: 11 }} />
                                <YAxis type="category" dataKey="name" tick={{ fill: "var(--text-secondary)", fontSize: 12 }} width={58} />
                                <Tooltip
                                    contentStyle={{ background: "var(--bg-elevated)", border: "1px solid var(--border)", borderRadius: 8, color: "var(--text-primary)" }}
                                    formatter={(v: number) => [v.toLocaleString(), "Customers"]}
                                />
                                <Bar dataKey="value" radius={[0, 6, 6, 0]}>
                                    {barData.map((_, i) => (
                                        <Cell key={i} fill={PALETTE[i % PALETTE.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    )}
                </div>
            </div>

            {/* Segment Detail Table */}
            {segments.data && (
                <div className="table-panel fade-in-up">
                    <div className="table-panel-header">
                        <div className="section-title">Segment Breakdown</div>
                        <div className="section-sub">Detailed count and share for every customer segment</div>
                    </div>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Segment Code</th>
                                <th>Customers</th>
                                <th>Share</th>
                                <th>Distribution</th>
                            </tr>
                        </thead>
                        <tbody>
                            {barData.map((seg, i) => (
                                <tr key={seg.name}>
                                    <td style={{ color: "var(--text-muted)" }}>{i + 1}</td>
                                    <td>
                                        <span style={{
                                            display: "inline-flex", alignItems: "center", gap: 8
                                        }}>
                                            <span style={{
                                                width: 10, height: 10, borderRadius: "50%",
                                                background: PALETTE[i % PALETTE.length],
                                                display: "inline-block", flexShrink: 0
                                            }} />
                                            <strong>{seg.name}</strong>
                                        </span>
                                    </td>
                                    <td>{seg.value.toLocaleString()}</td>
                                    <td style={{ color: "var(--accent-light)" }}>
                                        {total > 0 ? `${((seg.value / total) * 100).toFixed(1)}%` : "—"}
                                    </td>
                                    <td>
                                        <div style={{ width: 140, height: 6, background: "var(--border)", borderRadius: 99, overflow: "hidden" }}>
                                            <div style={{
                                                width: `${total > 0 ? (seg.value / total) * 100 : 0}%`,
                                                height: "100%",
                                                background: PALETTE[i % PALETTE.length],
                                                borderRadius: 99,
                                                transition: "width 0.6s ease",
                                            }} />
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
