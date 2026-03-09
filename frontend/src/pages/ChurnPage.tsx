import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
    ResponsiveContainer, BarChart, Bar
} from "recharts";
import { fetchKPIs, fetchChurnDistribution, fetchRiskValue } from "../api/client";
import KPICard from "../components/KPICard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorBanner from "../components/ErrorBanner";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

const GROUP_OPTIONS = [
    { value: "hr-hv", label: "High Risk – High Value (hr-hv)" },
    { value: "hr-mv", label: "High Risk – Medium Value (hr-mv)" },
    { value: "hr-lv", label: "High Risk – Low Value (hr-lv)" },
    { value: "mr-hv", label: "Medium Risk – High Value (mr-hv)" },
    { value: "mr-mv", label: "Medium Risk – Medium Value (mr-mv)" },
    { value: "mr-lv", label: "Medium Risk – Low Value (mr-lv)" },
    { value: "lr-hv", label: "Low Risk – High Value (lr-hv)" },
    { value: "lr-mv", label: "Low Risk – Medium Value (lr-mv)" },
    { value: "lr-lv", label: "Low Risk – Low Value (lr-lv)" },
];

function fmt(n: number, decimals = 2) {
    return n.toLocaleString("en-GB", { maximumFractionDigits: decimals });
}
function fmtPct(n: number) { return `${(n * 100).toFixed(1)}%`; }
function fmtGBP(n: number) {
    if (n >= 1_000_000) return `£${(n / 1_000_000).toFixed(2)}M`;
    if (n >= 1_000) return `£${(n / 1_000).toFixed(1)}K`;
    return `£${n.toFixed(0)}`;
}

export default function ChurnPage() {
    const [group, setGroup] = useState("hr-lv");
    const kpis = useQuery({ queryKey: ["kpis"], queryFn: fetchKPIs });
    const distribution = useQuery({ queryKey: ["churnDist"], queryFn: fetchChurnDistribution });
    const riskValueQuery = useQuery({ queryKey: ["riskValue", group], queryFn: () => fetchRiskValue(group) });

    const distData = distribution.data
        ? Object.entries(distribution.data.distribution)
            .map(([prob, count]) => ({ prob: parseFloat(prob), count }))
            .sort((a, b) => a.prob - b.prob)
        : [];

    const downloadPDF = () => {
        if (!riskValueQuery.data) return;

        const doc = new jsPDF();
        const tableData = riskValueQuery.data.map(c => [
            c.customerid,
            fmtPct(c.churn_probability),
            fmtGBP(c.clv),
            c.segment_code,
            c.persona
        ]);

        doc.setFontSize(18);
        doc.text(`Churn Prediction Report - ${group.toUpperCase()}`, 14, 22);
        doc.setFontSize(11);
        doc.setTextColor(100);
        doc.text(`Generated on: ${new Date().toLocaleString()}`, 14, 30);
        doc.text(`Total Customers in Cohort: ${riskValueQuery.data.length}`, 14, 36);

        autoTable(doc, {
            startY: 45,
            head: [['Customer ID', 'Churn Prob.', 'CLV', 'Segment', 'Persona']],
            body: tableData,
            theme: 'grid',
            headStyles: { fillColor: [124, 58, 237] }, // #7c3aed
        });

        doc.save(`churn_report_${group}_${new Date().toISOString().split('T')[0]}.pdf`);
    };

    return (
        <div className="page-wrapper">
            {/* KPI Cards */}
            <div className="kpi-grid">
                {kpis.isLoading ? <LoadingSpinner /> : kpis.error ? <ErrorBanner /> : (
                    <>
                        <KPICard
                            label="Avg Churn Probability"
                            value={fmtPct(kpis.data!.avg_churn_probability)}
                            icon="⚡"
                            accentColor="var(--red)"
                            subtext="Across all customers"
                        />
                        <KPICard
                            label="High-Risk Customers"
                            value={fmt(kpis.data!.high_risk_customers, 0)}
                            icon="🔴"
                            accentColor="#ef4444"
                            subtext={`${fmtPct(kpis.data!.high_risk_pct)} of base`}
                        />
                        <KPICard
                            label="Total Customers"
                            value={fmt(kpis.data!.total_customers, 0)}
                            icon="👥"
                            accentColor="var(--blue)"
                            subtext="In active snapshot"
                        />
                        <KPICard
                            label="CLV at Risk"
                            value={fmtGBP(kpis.data!.clv_at_risk)}
                            icon="💸"
                            accentColor="var(--orange)"
                            subtext="Expected revenue loss"
                        />
                    </>
                )}
            </div>

            {/* Charts */}
            <div className="chart-grid">
                {/* Churn Distribution */}
                <div className="chart-panel fade-in-up">
                    <div className="chart-panel-title">Churn Probability Distribution</div>
                    <div className="chart-panel-sub">Number of customers at each probability threshold</div>
                    {distribution.isLoading ? <LoadingSpinner /> : distribution.error ? <ErrorBanner /> : (
                        <ResponsiveContainer width="100%" height={260}>
                            <AreaChart data={distData} margin={{ top: 4, right: 12, left: 0, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="churnGrad" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#ef4444" stopOpacity={0.35} />
                                        <stop offset="95%" stopColor="#ef4444" stopOpacity={0.02} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
                                <XAxis dataKey="prob" tickFormatter={(v) => `${Math.round(v * 100)}%`} tick={{ fill: "var(--text-muted)", fontSize: 11 }} />
                                <YAxis tick={{ fill: "var(--text-muted)", fontSize: 11 }} />
                                <Tooltip
                                    contentStyle={{ background: "#fff", border: "1px solid var(--border)", borderRadius: 8, color: "var(--text-primary)", boxShadow: "var(--shadow)" }}
                                    formatter={(v: any) => [v, "Customers"]}
                                    labelFormatter={(l) => `Probability: ${Math.round(Number(l) * 100)}%`}
                                />
                                <Area type="monotone" dataKey="count" stroke="#ef4444" strokeWidth={2} fill="url(#churnGrad)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    )}
                </div>

                {/* High Risk Bar Chart */}
                <div className="chart-panel fade-in-up">
                    <div className="chart-panel-title">Top Customers by Churn vs CLV</div>
                    <div className="chart-panel-sub">Top 10 customers in selected group by churn probability</div>
                    {riskValueQuery.isLoading ? <LoadingSpinner /> : riskValueQuery.error ? <ErrorBanner /> : (
                        <ResponsiveContainer width="100%" height={260}>
                            <BarChart
                                data={riskValueQuery.data!.slice(0, 10).map(c => ({
                                    id: c.customerid.slice(-6),
                                    prob: +(c.churn_probability * 100).toFixed(1),
                                    clv: +c.clv.toFixed(0),
                                }))}
                                margin={{ top: 4, right: 12, left: 0, bottom: 0 }}
                            >
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
                                <XAxis dataKey="id" tick={{ fill: "var(--text-muted)", fontSize: 10 }} />
                                <YAxis yAxisId="left" tick={{ fill: "var(--text-muted)", fontSize: 11 }} unit="%" />
                                <YAxis yAxisId="right" orientation="right" tick={{ fill: "var(--text-muted)", fontSize: 11 }} unit="£" />
                                <Tooltip
                                    contentStyle={{ background: "#fff", border: "1px solid var(--border)", borderRadius: 8, color: "var(--text-primary)", boxShadow: "var(--shadow)" }}
                                />
                                <Bar yAxisId="left" dataKey="prob" name="Churn %" fill="#ef4444" radius={[4, 4, 0, 0]} />
                                <Bar yAxisId="right" dataKey="clv" name="CLV £" fill="#a78bfa" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    )}
                </div>
            </div>

            {/* High risk table */}
            <div className="table-panel fade-in-up">
                <div className="table-panel-header" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div>
                        <div className="section-title">Risk-Value Cohort</div>
                        <div className="section-sub">Customers in the selected risk and value buckets</div>
                    </div>
                    <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                        <select
                            value={group}
                            onChange={(e) => setGroup(e.target.value)}
                            style={{
                                background: "var(--bg-surface)", color: "var(--text-primary)",
                                border: "1px solid var(--border)", padding: "8px 12px",
                                borderRadius: "var(--radius)", outline: "none", cursor: "pointer",
                                fontSize: 13, fontWeight: 500,
                            }}
                        >
                            {GROUP_OPTIONS.map(opt => (
                                <option key={opt.value} value={opt.value}>{opt.label}</option>
                            ))}
                        </select>
                        <button
                            onClick={downloadPDF}
                            disabled={!riskValueQuery.data || riskValueQuery.data.length === 0}
                            style={{
                                background: "var(--accent)", color: "white",
                                border: "none", padding: "8px 16px",
                                borderRadius: "var(--radius)", fontWeight: 600,
                                cursor: riskValueQuery.data?.length ? "pointer" : "not-allowed",
                                opacity: riskValueQuery.data?.length ? 1 : 0.5,
                                transition: "all 0.2s"
                            }}
                        >
                            Export PDF
                        </button>
                    </div>
                </div>
                {riskValueQuery.isLoading ? <LoadingSpinner /> : riskValueQuery.error ? <ErrorBanner /> : (
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Customer ID</th>
                                <th>Churn Probability</th>
                                <th>CLV</th>
                                <th>Segment</th>
                                <th>Persona</th>
                            </tr>
                        </thead>
                        <tbody>
                            {riskValueQuery.data!
                                .sort((a, b) => b.churn_probability - a.churn_probability)
                                .slice(0, 20)
                                .map((c, i) => (
                                    <tr key={i}>
                                        <td style={{ fontFamily: "monospace", color: "var(--accent-light)" }}>{c.customerid}</td>
                                        <td>
                                            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                                                <div style={{
                                                    width: 60, height: 5, background: "var(--border)", borderRadius: 99, overflow: "hidden"
                                                }}>
                                                    <div style={{
                                                        width: `${(c.churn_probability * 100).toFixed(0)}%`,
                                                        height: "100%",
                                                        background: `hsl(${(1 - c.churn_probability) * 120}, 80%, 50%)`,
                                                        borderRadius: 99,
                                                    }} />
                                                </div>
                                                <span>{fmtPct(c.churn_probability)}</span>
                                            </div>
                                        </td>
                                        <td className="text-green">{fmtGBP(c.clv)}</td>
                                        <td>
                                            <span style={{ background: "var(--bg-elevated)", color: "var(--text-secondary)", padding: "3px 9px", borderRadius: 99, fontSize: 11, fontWeight: 600, border: "1px solid var(--border)" }}>
                                                {c.segment_code}
                                            </span>
                                        </td>
                                        <td style={{ color: "var(--text-secondary)" }}>{c.persona}</td>
                                    </tr>
                                ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
}
