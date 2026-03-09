interface KPICardProps {
    label: string;
    value: string | number;
    subtext?: string;
    icon?: string;
    accentColor?: string;
}

export default function KPICard({ label, value, subtext, accentColor = "var(--accent)" }: KPICardProps) {
    return (
        <div className="kpi-card fade-in-up" style={{ "--card-accent": accentColor } as React.CSSProperties}>
            <div className="kpi-icon" style={{ background: `${accentColor}18` }}>
                {/* <span style={{ fontSize: 18 }}>{icon}</span> */}
            </div>
            <div className="kpi-label">{label}</div>
            <div className="kpi-value">{value}</div>
            {subtext && <div className="kpi-sub">{subtext}</div>}
        </div>
    );
}
