import sys
from pathlib import Path

# --- PYTHONPATH FIX (REQUIRED FOR STREAMLIT) ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
import streamlit as st

from src.dashboard.data_loader import load_dashboard_snapshot
from src.dashboard.metrics import compute_kpis
from src.dashboard import charts


st.set_page_config(
    page_title="Customer Intelligence Dashboard",
    layout="wide"
)

st.title("📊 Customer Intelligence Platform")
st.caption("Churn · CLV · Segmentation · Retention Decisions")


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Controls")

snapshot_date = st.sidebar.text_input(
    "Snapshot date (YYYY-MM-DD)",
    value=""
)

load_latest = st.sidebar.checkbox("Use latest snapshot", value=True)

# -----------------------------
# Data Load
# -----------------------------
with st.spinner("Loading dashboard data..."):
    df = load_dashboard_snapshot(
        snapshot_date=None if load_latest else snapshot_date
    )

kpis = compute_kpis(df)

st.success(f"Snapshot loaded: {df['snapshot_date'].iloc[0].date()}")


# -----------------------------
# KPI Section
# -----------------------------
st.subheader("Executive Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{kpis['total_customers']:,}")
col2.metric("High Risk Customers", f"{kpis['high_risk_customers']:,}")
col3.metric("Avg Churn Probability", f"{kpis['avg_churn_probability']:.2%}")
col4.metric("ROI", f"{kpis['roi']:.2f}")

col5, col6, col7 = st.columns(3)

col5.metric("Total CLV", f"{kpis['total_clv']:,.0f}")
col6.metric("CLV at Risk", f"{kpis['clv_at_risk']:,.0f}")
col7.metric("Net Retained Value", f"{kpis['net_retained_value']:,.0f}")


# -----------------------------
# Charts
# -----------------------------
st.subheader("Risk Distribution")

c1, c2 = st.columns(2)
c1.plotly_chart(charts.churn_probability_histogram(df), use_container_width=True)
c2.plotly_chart(charts.risk_bucket_bar(df), use_container_width=True)


st.subheader("Value vs Risk")

c3, c4 = st.columns(2)
c3.plotly_chart(charts.clv_vs_churn_scatter(df), use_container_width=True)
c4.plotly_chart(charts.risk_value_heatmap(df), use_container_width=True)


st.subheader("Retention Decisions")

c5, c6 = st.columns(2)
c5.plotly_chart(charts.action_type_bar(df), use_container_width=True)
c6.plotly_chart(charts.cost_vs_savings_bar(df), use_container_width=True)


st.subheader("Segments & Personas")
st.plotly_chart(charts.segment_distribution(df), use_container_width=True)


# -----------------------------
# Data Table (optional)
# -----------------------------
with st.expander("View underlying data"):
    st.dataframe(
        df.sort_values("churn_probability", ascending=False),
        use_container_width=True
    )