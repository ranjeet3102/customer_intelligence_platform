import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "./Sidebar";

const PAGE_META: Record<string, { title: string; sub: string; badge: string }> = {
    "/": { title: "Customer Health", sub: "Unified KPI overview and health scoring across your customer base", badge: "Overview" },
    "/churn": { title: "Churn Prediction", sub: "ML-powered churn probability, high-risk identification and distribution analysis", badge: "Predictive AI" },
    "/clv": { title: "Customer Lifetime Value", sub: "CLV distribution, at-risk value analysis, and percentile breakdown", badge: "Revenue" },
    "/segmentation": { title: "Segmentation", sub: "Customer segment breakdown and persona distribution", badge: "Behavioural" },
    "/retention": { title: "Retention Actions", sub: "Recommended retention actions, ROI and economics of each incentive tier", badge: "Decisioning" },
};

export default function DashboardLayout() {
    const { pathname } = useLocation();
    const meta = PAGE_META[pathname] ?? PAGE_META["/"];

    return (
        <div className="dashboard-shell">
            <Sidebar />
            <div className="main-content">
                <header className="topbar">
                    <div>
                        <div className="topbar-title">{meta.title}</div>
                        <div className="topbar-sub">{meta.sub}</div>
                    </div>
                    <span className="topbar-badge">{meta.badge}</span>
                </header>
                <Outlet />
            </div>
        </div>
    );
}
