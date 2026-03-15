import { NavLink } from "react-router-dom";

const navItems = [
    {
        to: "/",
        label: "Customer Health",
        icon: (
            <svg className="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
        ),
    },
    {
        to: "/churn",
        label: "Churn Prediction",
        icon: (
            <svg className="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
            </svg>
        ),
    },
    {
        to: "/clv",
        label: "Customer LTV",
        icon: (
            <svg className="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        ),
    },
    {
        to: "/segmentation",
        label: "Segmentation",
        icon: (
            <svg className="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
            </svg>
        ),
    },
    {
        to: "/retention",
        label: "Retention",
        icon: (
            <svg className="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
        ),
    },
];

export default function Sidebar() {
    return (
        <aside className="sidebar">
            <div className="sidebar-brand">
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
                    <div style={{
                        width: 34, height: 34, borderRadius: 10,
                        background: "linear-gradient(135deg, #6d28d9, #8b5cf6)",
                        display: "flex", alignItems: "center", justifyContent: "center",
                        flexShrink: 0,
                        boxShadow: "0 2px 8px rgba(109,40,217,0.3)",
                    }}>
                        <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="white" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18" />
                        </svg>
                    </div>
                    <div>
                        <div className="sidebar-brand-title">CIP</div>
                        <div className="sidebar-brand-sub">Intelligence Platform</div>
                    </div>
                </div>
            </div>

            <div className="sidebar-section-label">Navigation</div>

            <nav style={{ flex: 1 }}>
                {navItems.map((item) => (
                    <NavLink
                        key={item.to}
                        to={item.to}
                        end={item.to === "/"}
                        className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}
                    >
                        {item.icon}
                        {item.label}
                    </NavLink>
                ))}
            </nav>

            <div style={{
                margin: "0 10px",
                padding: "12px 14px",
                borderRadius: 10,
                background: "rgba(109,40,217,0.05)",
                border: "1px solid rgba(109,40,217,0.14)",
            }}>
                <div style={{ fontSize: 11, fontWeight: 700, color: "var(--accent)", marginBottom: 4, letterSpacing: "0.04em", textTransform: "uppercase" }}>
                    Data Source
                </div>
                {/* <div style={{ fontSize: 11, color: "var(--text-secondary)", lineHeight: 1.5, fontFamily: "monospace" }}>
                    retention_decisions.parquet
                </div> */}
                <div style={{
                    marginTop: 8, display: "flex", alignItems: "center", gap: 5,
                    fontSize: 11, color: "var(--green)", fontWeight: 600,
                }}>
                    <span style={{ width: 6, height: 6, borderRadius: "50%", background: "var(--green)", display: "inline-block", boxShadow: "0 0 0 2px rgba(5,150,105,0.2)" }} />
                    Live API
                </div>
            </div>
        </aside>
    );
}
