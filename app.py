"""
Road Accident Insight Explorer
Streamlit application.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Road Accident Insight Explorer", layout="wide")

DATA_PATH = "data/accidents_clean.parquet"


@st.cache_data
def load_data():
    return pd.read_parquet(DATA_PATH)


df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.title("Filters")
st.sidebar.caption("Leave a filter empty to include all values for that field.")

region = st.sidebar.multiselect("Police force area", sorted(df["police_force"].unique()))

min_date, max_date = df["date"].min(), df["date"].max()
date_range = st.sidebar.date_input(
    "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
)

severity = st.sidebar.multiselect("Severity", ["Fatal", "Serious", "Slight"])
weather = st.sidebar.multiselect("Weather condition", sorted(df["weather"].unique()))

if st.sidebar.button("Reset all filters"):
    st.rerun()

# ---------- Apply filters ----------
filtered = df.copy()
if region:
    filtered = filtered[filtered["police_force"].isin(region)]
if len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]
if severity:
    filtered = filtered[filtered["severity"].isin(severity)]
if weather:
    filtered = filtered[filtered["weather"].isin(weather)]

# ---------- Header ----------
st.title("Road Accident Insight Explorer")
st.write(
    "Explore road accident patterns by location, time, severity, and weather "
    "— no spreadsheets or SQL required."
)

# ---------- Key insights ----------
st.header("Key insights")
st.caption("Auto-generated in plain language based on your current filters.")

n = len(filtered)
total = len(df)

col1, col2 = st.columns(2)
if n == 0:
    st.warning("No accidents match the current filters.")
else:
    with col1:
        st.info(f"This selection contains **{n:,}** accidents.")
        peak_hour = filtered["hour"].mode()[0]
        peak_hour_pct = (filtered["hour"] == peak_hour).mean() * 100
        st.info(
            f"**{peak_hour_pct:.0f}%** of accidents in this selection occurred "
            f"around **{int(peak_hour)}:00**."
        )
        severe_pct = filtered["severity"].isin(["Fatal", "Serious"]).mean() * 100
        st.info(
            f"**{severe_pct:.0f}%** of accidents in this selection resulted in a "
            f"Fatal or Serious injury."
        )
    with col2:
        top_day = filtered["day_of_week_name"].value_counts()
        st.info(
            f"**{top_day.index[0]}** has the highest number of accidents in this "
            f"selection ({top_day.iloc[0]:,}, {top_day.iloc[0] / n * 100:.0f}% of the total)."
        )
        wx_severe = (
            filtered.assign(is_severe=filtered["severity"].isin(["Fatal", "Serious"]))
            .groupby("weather")["is_severe"]
            .mean()
            .sort_values(ascending=False)
        )
        if len(wx_severe):
            st.info(
                f"**{wx_severe.index[0]}** conditions are associated with the highest "
                f"proportion of severe accidents in this selection "
                f"({wx_severe.iloc[0] * 100:.0f}%)."
            )

st.divider()

c1, c2, c3 = st.columns(3)
c1.metric("Accidents in selection", f"{n:,}")
c2.metric("Of total dataset", f"{total:,}")
c3.metric("Percent of dataset", f"{n / total * 100:.1f}%" if total else "0%")

st.divider()

# ---------- Hotspot map ----------
st.header("Accident hotspot map")
st.write("Yellow to red indicates increasing concentration of accidents.")

MAX_MAP_POINTS = 15000
map_df = filtered.sample(min(len(filtered), MAX_MAP_POINTS), random_state=42) if n else filtered
if len(map_df):
    st.caption(f"Showing a random sample of {len(map_df):,} points for map performance (selection has {n:,} total).")
    fig_map = px.density_mapbox(
        map_df, lat="latitude", lon="longitude", radius=6, zoom=5,
        center=dict(lat=52.9, lon=-1.5), mapbox_style="carto-darkmatter",
        color_continuous_scale=["yellow", "orange", "red"],
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=500)
    st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# ---------- Trends over time ----------
st.header("Trends over time")

t1, t2 = st.columns(2)
with t1:
    st.subheader("Accidents by hour of day")
    hourly = filtered["hour"].value_counts().reindex(range(24), fill_value=0).sort_index()
    fig_hour = go.Figure(go.Bar(x=hourly.index, y=hourly.values, marker_color="#5b8cff"))
    fig_hour.update_layout(xaxis_title="Hour of day", yaxis_title="Number of accidents", height=350)
    st.plotly_chart(fig_hour, use_container_width=True)

with t2:
    st.subheader("Accidents by day of week")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    daily = filtered["day_of_week_name"].value_counts().reindex(day_order, fill_value=0)
    fig_day = go.Figure(go.Bar(x=daily.index, y=daily.values, marker_color="#5b8cff"))
    fig_day.update_layout(xaxis_title="Day of week", yaxis_title="Number of accidents", height=350)
    st.plotly_chart(fig_day, use_container_width=True)

st.divider()

# ---------- Severity breakdown ----------
st.header("Severity breakdown")
sev_order = ["Fatal", "Serious", "Slight"]
sev_counts = filtered["severity"].value_counts().reindex(sev_order, fill_value=0)
fig_sev = go.Figure(go.Bar(
    x=sev_order, y=sev_counts.values,
    marker_color=["#e0524f", "#e8a63c", "#3fae6d"],
))
fig_sev.update_layout(xaxis_title="Severity", yaxis_title="Number of accidents", height=350)
st.plotly_chart(fig_sev, use_container_width=True)

with st.expander("About this data"):
    st.write(
        "Source: [DfT road casualty statistics, collision data]"
        "(https://www.data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data), "
        "contains public sector information licensed under the Open Government Licence v3.0."
    )

st.caption("Built with Claude.")
