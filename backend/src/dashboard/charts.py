import pandas as pd
import plotly.express as px


def churn_probability_histogram(df: pd.DataFrame):
    return px.histogram(
        df,
        x="churn_probability",
        nbins=30,
        title="Churn Probability Distribution"
    )


def risk_bucket_bar(df: pd.DataFrame):
    counts = df["risk_bucket"].value_counts().reset_index()
    counts.columns = ["risk_bucket", "count"]

    return px.bar(
        counts,
        x="risk_bucket",
        y="count",
        title="Customers by Risk Bucket"
    )


def clv_vs_churn_scatter(df: pd.DataFrame):
    return px.scatter(
        df,
        x="churn_probability",
        y="clv",
        color="risk_bucket",
        title="CLV vs Churn Probability",
        hover_data=["customerid", "segment_code"]
    )


def risk_value_heatmap(df: pd.DataFrame):
    pivot = (
        df
        .pivot_table(
            index="risk_bucket",
            columns="value_bucket",
            values="customerid",
            aggfunc="count",
            fill_value=0
        )
        .reset_index()
        .melt(id_vars="risk_bucket", var_name="value_bucket", value_name="count")
    )

    return px.density_heatmap(
        pivot,
        x="value_bucket",
        y="risk_bucket",
        z="count",
        title="Risk vs Value Segmentation"
    )


def action_type_bar(df: pd.DataFrame):
    counts = df["action_type"].value_counts().reset_index()
    counts.columns = ["action_type", "count"]

    return px.bar(
        counts,
        x="action_type",
        y="count",
        title="Retention Actions Distribution"
    )


def cost_vs_savings_bar(df: pd.DataFrame):
    totals = pd.DataFrame({
        "metric": ["Expected Savings", "Incentive Cost"],
        "value": [
            df["expected_savings"].sum(),
            df["incentive_cost"].sum()
        ]
    })

    return px.bar(
        totals,
        x="metric",
        y="value",
        title="Retention Economics Overview"
    )


def segment_distribution(df: pd.DataFrame):
    counts = df["segment_code"].value_counts().reset_index()
    counts.columns = ["segment_code", "count"]

    return px.bar(
        counts,
        x="segment_code",
        y="count",
        title="Customer Segments Distribution"
    )