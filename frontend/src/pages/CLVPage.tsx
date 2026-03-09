import { useQuery } from "@tanstack/react-query";
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
    ResponsiveContainer, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from "recharts";
import { fetchKPIs, fetchCLVDistribution } from "../api/client";
import KPICard from "../components/KPICard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorBanner from "../components/ErrorBanner";

function fmtGBP(n: number) {
    if (n >= 1_000_000) return `£${(n / 1_000_000).toFixed(2)}M`;
    if (n >= 1_000) return `£${(n / 1_000).toFixed(1)}K`;
    return `£${n.toFixed(0)}`;
}

export default function CLVPage() {
    const kpis = useQuery({ queryKey: ["kpis"], queryFn: fetchKPIs });
    const clvStats = useQuery({ queryKey: ["clvDist"], queryFn: fetchCLVDistribution });

    const percentileData = clvStats.data
        ? [
            { label: "Min", value: clvStats.data.min },
            { label: "P25", value: clvStats.data["25%"] },
            { label: "Median", value: clvStats.data["50%"] },
            { label: "Mean", value: clvStats.data.mean },
            { label: "P75", value: clvStats.data["75%"] },
            { label: "Max", value: clvStats.data.max },
        ]
        : [];

    const radarData = clvStats.data
        ? [
            { metric: "Mean CLV", value: Math.min((clvStats.data.mean / clvStats.data.max) * 100, 100) },
            { metric: "Spread", value: Math.min((clvStats.data.std / clvStats.data.max) * 100 * 2, 100) },
            { metric: "P75 %", value: (clvStats.data["75%"] / clvStats.data.max) * 100 },
            { metric: "Median %", value: (clvStats.data["50%"] / clvStats.data.max) * 100 },
            { metric: "P25 %", value: (clvStats.data["25%"] / clvStats.data.max) * 100 },
        ]
        : [];

    return (
        <div className="page-wrapper">
            {/* KPI Cards */}
            <div className="kpi-grid">
                {kpis.isLoading ? <LoadingSpinner /> : kpis.error ? <ErrorBanner /> : (
                    <>
                        <KPICard
                            label="Total CLV (Portfolio)"
                            value={fmtGBP(kpis.data!.total_clv)}
                            icon="💰"
                            accentColor="var(--green)"
                            subtext="Cumulative customer value"
                        />
                        <KPICard
                            label="CLV at Risk"
                            value={fmtGBP(kpis.data!.clv_at_risk)}
                            icon="⚠️"
                            accentColor="var(--orange)"
                            subtext="Weighted by churn probability"
                        />
                        {clvStats.data && (
                            <>
                                <KPICard
                                    label="Avg (Mean) CLV"
                                    value={fmtGBP(clvStats.data.mean)}
                                    icon="📊"
                                    accentColor="var(--accent)"
                                    subtext={`Std Dev: ${fmtGBP(clvStats.data.std)}`}
                                />
                                <KPICard
                                    label="Median CLV"
                                    value={fmtGBP(clvStats.data["50%"])}
                                    icon="📈"
                                    accentColor="var(--blue)"
                                    subtext={`Range: ${fmtGBP(clvStats.data.min)} – ${fmtGBP(clvStats.data.max)}`}
                                />
                            </>
                        )}
                    </>
                )}
            </div>

            {/* Charts */}
            <div className="chart-grid">
                <div className="chart-panel fade-in-up">
                    <div className="chart-panel-title">CLV Percentile Distribution</div>
                    <div className="chart-panel-sub">Customer value across statistical percentiles</div>
                    {clvStats.isLoading ? <LoadingSpinner /> : clvStats.error ? <ErrorBanner /> : (
                        <ResponsiveContainer width="100%" height={260}>
                            <BarChart data={percentileData} margin={{ top: 4, right: 12, left: 16, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="clvGrad" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="0%" stopColor="#10b981" stopOpacity={1} />
                                        <stop offset="100%" stopColor="#059669" stopOpacity={0.7} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
                                <XAxis dataKey="label" tick={{ fill: "var(--text-muted)", fontSize: 12 }} />
                                <YAxis tickFormatter={fmtGBP} tick={{ fill: "var(--text-muted)", fontSize: 11 }} />
                                <Tooltip
                                    contentStyle={{ background: "var(--bg-elevated)", border: "1px solid var(--border)", borderRadius: 8, color: "var(--text-primary)" }}
                                    formatter={(v: number) => [fmtGBP(v), "CLV"]}
                                />
                                <Bar dataKey="value" fill="url(#clvGrad)" radius={[6, 6, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    )}
                </div>

                <div className="chart-panel fade-in-up">
                    <div className="chart-panel-title">CLV Shape Profile</div>
                    <div className="chart-panel-sub">Radar view normalised to portfolio maximum CLV</div>
                    {clvStats.isLoading ? <LoadingSpinner /> : clvStats.error ? <ErrorBanner /> : (
                        <ResponsiveContainer width="100%" height={260}>
                            <RadarChart data={radarData}>
                                <PolarGrid stroke="var(--border-subtle)" />
                                <PolarAngleAxis dataKey="metric" tick={{ fill: "var(--text-secondary)", fontSize: 12 }} />
                                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: "var(--text-muted)", fontSize: 10 }} />
                                <Radar name="CLV" dataKey="value" stroke="#10b981" fill="#10b981" fillOpacity={0.25} strokeWidth={2} />
                                <Tooltip
                                    contentStyle={{ background: "var(--bg-elevated)", border: "1px solid var(--border)", borderRadius: 8, color: "var(--text-primary)" }}
                                    formatter={(v: number) => [`${v.toFixed(1)}%`, "Normalised"]}
                                />
                            </RadarChart>
                        </ResponsiveContainer>
                    )}
                </div>
            </div>

            {/* Stats Table */}
            {clvStats.data && (
                <div className="table-panel fade-in-up">
                    <div className="table-panel-header">
                        <div className="section-title">CLV Descriptive Statistics</div>
                        <div className="section-sub">Full statistical summary of customer lifetime value distribution</div>
                    </div>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Statistic</th>
                                <th>Value</th>
                                <th>Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            {[
                                { stat: "Count", value: clvStats.data.count.toLocaleString(), desc: "Total customers with CLV" },
                                { stat: "Mean", value: fmtGBP(clvStats.data.mean), desc: "Average customer lifetime value" },
                                { stat: "Std Dev", value: fmtGBP(clvStats.data.std), desc: "Spread / variability of CLV" },
                                { stat: "Min", value: fmtGBP(clvStats.data.min), desc: "Lowest CLV in portfolio" },
                                { stat: "25th Percentile", value: fmtGBP(clvStats.data["25%"]), desc: "75% of customers exceed this" },
                                { stat: "Median", value: fmtGBP(clvStats.data["50%"]), desc: "Midpoint — half above, half below" },
                                { stat: "75th Percentile", value: fmtGBP(clvStats.data["75%"]), desc: "Top quartile threshold" },
                                { stat: "Max", value: fmtGBP(clvStats.data.max), desc: "Highest CLV in portfolio" },
                            ].map((row) => (
                                <tr key={row.stat}>
                                    <td style={{ fontWeight: 600 }}>{row.stat}</td>
                                    <td className="text-green">{row.value}</td>
                                    <td style={{ color: "var(--text-secondary)" }}>{row.desc}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
