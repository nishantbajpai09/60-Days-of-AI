"""
app.py — Road Accident Insight Explorer
Interactive exploration of UK road accident data: no SQL, no BI tool, just filters.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

# ---------- Page config ----------
st.set_page_config(
    page_title="Road Accident Insight Explorer",
    page_icon="🚦",
    layout="wide",
)

DATA_PATH = "data/accidents_clean.parquet"


# ---------- Data loading ----------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        "Clean dataset not found. Run `python etl.py` first to generate "
        "`data/accidents_clean.parquet` from your raw CSV."
    )
    st.stop()

if df.empty:
    st.error("The dataset is empty after cleaning. Check your raw CSV.")
    st.stop()


# ---------- Insight engine ----------
def generate_insights(filtered: pd.DataFrame) -> list[str]:
    """
    Generates plain-language insights from the currently filtered dataset.

    Guards against misleading statements: if the selection is already
    ~100% severe (e.g. user filtered to Fatal only), the weather-severity
    insight is skipped since every weather condition would trivially show
    100% severity within that slice — a statistic, not an insight.
    """
    insights = []
    if filtered.empty:
        return ["No accidents match the current filters. Try widening your selection."]

    total = len(filtered)
    severe = filtered["accident_severity"].isin(["Fatal", "Serious"])
    severe_pct = severe.mean() * 100

    # Weather vs severity — skipped when selection is already near-100% severe
    if severe_pct < 95:
        severity_flag = filtered["accident_severity"].isin(["Fatal", "Serious"])
        weather_severity = (
            severity_flag.groupby(filtered["weather_conditions"])
            .mean()
            .sort_values(ascending=False)
        )
        weather_counts = filtered["weather_conditions"].value_counts()
        eligible = weather_severity[weather_counts.reindex(weather_severity.index) >= 10]
        if not eligible.empty:
            top_weather = eligible.index[0]
            top_pct = eligible.iloc[0] * 100
            insights.append(
                f"**{top_weather}** conditions are associated with the highest "
                f"proportion of severe accidents ({top_pct:.0f}% Fatal/Serious)."
            )
    else:
        insights.append(
            f"This selection is already filtered to mostly severe outcomes "
            f"({severe_pct:.0f}% Fatal/Serious) — weather comparison isn't "
            f"meaningful within an already-severe-only slice."
        )

    # Peak hour
    valid_hours = filtered[filtered["hour"] >= 0]
    if not valid_hours.empty:
        peak_hour = valid_hours["hour"].value_counts().idxmax()
        peak_count = valid_hours["hour"].value_counts().max()
        insights.append(
            f"**{peak_hour}:00–{peak_hour + 1}:00** is the peak hour for accidents "
            f"in this selection, with {peak_count:,} recorded incidents."
        )

    # Road surface
    surface_counts = filtered["road_surface_conditions"].value_counts()
    if not surface_counts.empty:
        top_surface = surface_counts.idxmax()
        top_surface_pct = (surface_counts.max() / total) * 100
        insights.append(
            f"**{top_surface}** road surface accounts for {top_surface_pct:.0f}% "
            f"of accidents in this selection."
        )

    # Day of week
    day_counts = filtered["day_of_week"].value_counts()
    if not day_counts.empty:
        top_day = day_counts.idxmax()
        insights.append(
            f"**{top_day}** sees the most accidents in this selection "
            f"({day_counts.max():,} incidents)."
        )

    return insights


# ---------- Sidebar filters ----------
st.sidebar.header("Filters")

severities = sorted(df["accident_severity"].unique())
selected_severity = st.sidebar.multiselect(
    "Severity", options=severities, default=severities
)

weathers = sorted(df["weather_conditions"].unique())
selected_weather = st.sidebar.multiselect(
    "Weather condition", options=weathers, default=weathers
)

min_date, max_date = df["date"].min().date(), df["date"].max().date()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# ---------- Apply filters ----------
mask = (
    df["accident_severity"].isin(selected_severity)
    & df["weather_conditions"].isin(selected_weather)
    & (df["date"].dt.date >= start_date)
    & (df["date"].dt.date <= end_date)
)
filtered = df[mask]


# ---------- Header ----------
st.title("🚦 Road Accident Insight Explorer")
st.caption(
    "Explore UK road accident data with plain filters — no SQL, no BI tool, "
    "no training required."
)

# ---------- KPI row ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total accidents", f"{len(filtered):,}")
col2.metric("Fatal", f"{(filtered['accident_severity'] == 'Fatal').sum():,}")
col3.metric("Serious", f"{(filtered['accident_severity'] == 'Serious').sum():,}")
col4.metric("Slight", f"{(filtered['accident_severity'] == 'Slight').sum():,}")

if filtered.empty:
    st.warning("No accidents match the current filters. Try widening your selection.")
    st.stop()

st.divider()

# ---------- Tabs ----------
tab_map, tab_trends, tab_insights = st.tabs(["🗺️ Hotspot Map", "📈 Trends", "💡 Insights"])

with tab_map:
    st.subheader("Accident hotspot density")
    fig_map = px.density_mapbox(
        filtered,
        lat="latitude",
        lon="longitude",
        radius=12,
        center=dict(lat=filtered["latitude"].mean(), lon=filtered["longitude"].mean()),
        zoom=8,
        mapbox_style="carto-positron",
        color_continuous_scale=["#FFEB3B", "#FF9800", "#F44336"],
        height=550,
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption(
        "Color intensity reflects accident density — yellow (lower) to red (higher)."
    )

with tab_trends:
    st.subheader("Accidents by hour of day")
    hourly = (
        filtered[filtered["hour"] >= 0]["hour"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    hourly.columns = ["hour", "count"]
    fig_hourly = px.bar(hourly, x="hour", y="count", labels={"hour": "Hour", "count": "Accidents"})
    st.plotly_chart(fig_hourly, use_container_width=True)

    st.subheader("Accidents by month")
    monthly = (
        filtered.groupby(["year", "month", "month_name"])
        .size()
        .reset_index(name="count")
        .sort_values(["year", "month"])
    )
    monthly["label"] = monthly["month_name"] + " " + monthly["year"].astype(str)
    fig_monthly = px.line(monthly, x="label", y="count", markers=True, labels={"label": "Month", "count": "Accidents"})
    st.plotly_chart(fig_monthly, use_container_width=True)

    st.subheader("Severity breakdown by weather condition")
    weather_severity_ct = (
        filtered.groupby(["weather_conditions", "accident_severity"])
        .size()
        .reset_index(name="count")
    )
    fig_weather = px.bar(
        weather_severity_ct,
        x="weather_conditions",
        y="count",
        color="accident_severity",
        labels={"weather_conditions": "Weather", "count": "Accidents", "accident_severity": "Severity"},
    )
    st.plotly_chart(fig_weather, use_container_width=True)

with tab_insights:
    st.subheader("Auto-generated insights")
    st.caption("Plain-language takeaways from the currently filtered data.")
    for point in generate_insights(filtered):
        st.markdown(f"- {point}")

st.divider()
st.caption(
    f"Data: UK STATS19 road safety data, Department for Transport (Open Government Licence). "
    f"Showing {len(filtered):,} of {len(df):,} total records."
)
