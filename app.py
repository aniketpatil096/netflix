from html import escape
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Netflix & Chill | Viewing Insights",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path(__file__).with_name("netflix.csv")


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data["Watch_Date"] = pd.to_datetime(data["Watch_Date"], errors="coerce")
    return data


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700&display=swap');

    :root {
        --netflix-red: #e50914;
        --ink: #090909;
        --panel: #151515;
        --paper: #f5f2ed;
        --muted: #a7a19d;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background-image:
            linear-gradient(180deg, rgba(8,8,8,.62) 0%, rgba(8,8,8,.77) 48%, rgba(8,8,8,.87) 100%),
            url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=2200&q=85');
        background-position: center, center top;
        background-size: cover, cover;
        background-attachment: scroll, fixed;
        color: var(--paper);
    }

    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10,10,10,.98), rgba(18,12,12,.97));
        border-right: 1px solid #302323;
    }
    .sidebar-brand {
        align-items: center;
        border-bottom: 1px solid #302727;
        display: flex;
        gap: 12px;
        margin-bottom: 18px;
        padding: 8px 0 18px;
    }
    .sidebar-mark {
        align-items: center;
        background: var(--netflix-red);
        color: #fff;
        display: flex;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 27px;
        height: 40px;
        justify-content: center;
        width: 34px;
    }
    .sidebar-name {
        color: #fff;
        font-size: 15px;
        font-weight: 700;
    }
    .sidebar-caption {
        color: var(--muted);
        font-size: 10px;
        letter-spacing: 1px;
        margin-top: 2px;
    }
    [data-testid="stSidebar"] .stButton button {
        border-color: #514040;
        color: #f5f2ed;
    }
    [data-testid="stMainBlockContainer"] {
        max-width: 1440px;
        padding: 1.25rem 2.5rem 3rem;
    }

    .hero {
        min-height: 340px;
        display: flex;
        align-items: flex-end;
        padding: 42px 52px;
        margin: 0 0 28px;
        overflow: hidden;
        position: relative;
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 5px;
        background-image:
            linear-gradient(90deg, rgba(5,5,5,.96) 0%, rgba(5,5,5,.76) 43%, rgba(5,5,5,.18) 100%),
            linear-gradient(0deg, rgba(5,5,5,.72), transparent 70%),
            url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=2200&q=85');
        background-position: center, center, center 45%;
        background-size: cover;
        animation: reveal .7s ease-out both;
    }

    .hero-copy { max-width: 720px; position: relative; z-index: 1; }
    .brand {
        color: var(--netflix-red);
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 11px;
    }
    .hero h1 {
        color: #fff;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 76px;
        font-weight: 400;
        line-height: .92;
        letter-spacing: 0;
        margin: 0;
    }
    .hero h1 span { color: var(--netflix-red); }
    .hero p {
        color: #dedbd7;
        font-size: 15px;
        margin: 16px 0 0;
        max-width: 530px;
    }

    .section-heading {
        align-items: center;
        border-bottom: 1px solid #292727;
        display: flex;
        gap: 12px;
        margin: 0 0 16px;
        padding: 0 0 12px;
    }
    .section-heading h2 {
        color: var(--paper);
        font-family: 'Bebas Neue', sans-serif;
        font-size: 27px;
        font-weight: 400;
        letter-spacing: 0;
        margin: 0;
    }
    .section-heading span {
        background: var(--netflix-red);
        height: 19px;
        width: 3px;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(145deg, rgba(12,12,12,.88), rgba(12,12,12,.82));
        border: 1px solid #2a2828;
        border-radius: 5px;
        padding: 15px 16px 7px;
        transition: border-color .2s ease, transform .2s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(229,9,20,.55);
        transform: translateY(-2px);
    }
    [data-testid="stMetric"] {
        background: #141313;
        border-left: 2px solid var(--netflix-red);
        padding: 15px 18px;
    }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: #fff; }
    .insight-kicker {
        color: var(--netflix-red);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .insight-value {
        color: #fff;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 28px;
        line-height: 1.05;
        overflow-wrap: anywhere;
    }
    .insight-detail {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.5;
        margin-top: 8px;
    }
    .footer {
        color: #77716e;
        font-size: 12px;
        margin-top: 30px;
        padding-top: 14px;
        border-top: 1px solid #252323;
    }
    @keyframes reveal {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @media (max-width: 700px) {
        [data-testid="stMainBlockContainer"] { padding: .75rem 1rem 2rem; }
        .hero { min-height: 285px; padding: 26px 22px; }
        .hero h1 { font-size: 58px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

try:
    netflix = load_data()
except (OSError, pd.errors.ParserError) as error:
    st.error(f"Couldn't load the dataset: {error}")
    st.stop()

required_columns = {
    "Region",
    "Subscription_Plan",
    "Rating",
    "Category",
    "Monthly_Revenue",
}
missing_columns = required_columns.difference(netflix.columns)
if missing_columns:
    st.error(f"The dataset is missing required columns: {', '.join(sorted(missing_columns))}")
    st.stop()

regions = sorted(netflix["Region"].dropna().unique().tolist())
plans = sorted(netflix["Subscription_Plan"].dropna().unique().tolist())
rating_min = int(netflix["Rating"].min())
rating_max = int(netflix["Rating"].max())


def reset_filters() -> None:
    st.session_state["region_filter"] = regions
    st.session_state["plan_filter"] = plans
    st.session_state["rating_filter"] = (rating_min, rating_max)


with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand"><div class="sidebar-mark">N</div>'
        '<div><div class="sidebar-name">NETFLIX</div>'
        '<div class="sidebar-caption">INSIGHTS STUDIO</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Refine the view")
    selected_regions = st.multiselect("Region", regions, default=regions, key="region_filter")
    selected_plans = st.multiselect("Subscription plan", plans, default=plans, key="plan_filter")
    selected_ratings = st.slider(
        "Rating range",
        min_value=rating_min,
        max_value=rating_max,
        value=(rating_min, rating_max),
        key="rating_filter",
    )
    st.button("Reset filters", on_click=reset_filters, use_container_width=True)
    st.caption("Filters apply to every chart and insight.")

filtered_netflix = netflix.loc[
    netflix["Region"].isin(selected_regions)
    & netflix["Subscription_Plan"].isin(selected_plans)
    & netflix["Rating"].between(*selected_ratings)
].copy()

with st.sidebar:
    st.divider()
    st.caption(f"{len(filtered_netflix):,} of {len(netflix):,} records in view")

if filtered_netflix.empty:
    st.warning("No records match these filters. Adjust the selections in the sidebar.")
    st.stop()

netflix = filtered_netflix

st.markdown(
    """
    <section class="hero">
      <div class="hero-copy">
        <div class="brand">Netflix data analysis</div>
        <h1>NETFLIX <span>&amp; CHILL</span></h1>
        <p>A closer look at what people watch, how they rate it, and where the revenue comes from.</p>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-heading"><span></span><h2>Inside the stream</h2></div>',
    unsafe_allow_html=True,
)

region_revenue = netflix.groupby("Region")["Monthly_Revenue"].sum().rename_axis("Region").reset_index()
plan_rating = netflix.groupby("Subscription_Plan")["Rating"].sum().rename_axis("Subscription plan").reset_index()
rating_counts = netflix["Rating"].value_counts().sort_index().rename_axis("Rating").reset_index(name="Count")
category_revenue = netflix.groupby("Category")["Monthly_Revenue"].sum().rename_axis("Category").reset_index()
device_minutes = (
    netflix.groupby("Device", as_index=False)["Watch_Time_Minutes"]
    .sum()
    .sort_values("Watch_Time_Minutes", ascending=True)
)
top_title_counts = (
    netflix.groupby("Title", as_index=False)["Watch_Count"]
    .sum()
    .nlargest(8, "Watch_Count")
    .sort_values("Watch_Count", ascending=True)
)
monthly_watch_count = (
    netflix.dropna(subset=["Watch_Date"])
    .assign(Watch_Month=lambda data: data["Watch_Date"].dt.to_period("M").dt.to_timestamp())
    .groupby("Watch_Month", as_index=False)["Watch_Count"]
    .sum()
)
language_watch_count = (
    netflix.groupby("Language", as_index=False)["Watch_Count"]
    .sum()
    .sort_values("Watch_Count", ascending=False)
)

palette = ["#e50914", "#f5f2ed", "#a7a19d", "#6c6664", "#7b1018", "#d44b50", "#383434", "#bd9a96"]
chart_layout = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "DM Sans, sans-serif", "color": "#dedbd7", "size": 12},
    "margin": {"l": 12, "r": 12, "t": 16, "b": 12},
    "legend": {"orientation": "h", "yanchor": "bottom", "y": -0.12, "xanchor": "center", "x": 0.5},
}

region_chart = px.bar(
    region_revenue,
    x="Region",
    y="Monthly_Revenue",
    color="Monthly_Revenue",
    color_continuous_scale=["#641016", "#e50914", "#ff646a"],
    labels={"Monthly_Revenue": "Monthly revenue"},
)
region_chart.update_layout(**chart_layout, coloraxis_showscale=False, xaxis_title=None, yaxis_title="Revenue")
region_chart.update_traces(marker_line_width=0, hovertemplate="%{x}<br>Revenue: %{y:,.0f}<extra></extra>")

plan_chart = px.pie(
    plan_rating,
    names="Subscription plan",
    values="Rating",
    hole=0.62,
    color_discrete_sequence=palette,
)
plan_chart.update_layout(**chart_layout)
plan_chart.update_traces(textposition="inside", textinfo="percent+label", hole=0.62, marker_line_color="#151515", marker_line_width=2)

rating_chart = px.bar(
    rating_counts,
    x="Rating",
    y="Count",
    color="Rating",
    color_continuous_scale=["#641016", "#e50914", "#ff646a"],
    labels={"Count": "Number of ratings"},
)
rating_chart.update_layout(**chart_layout, coloraxis_showscale=False, xaxis_title=None, yaxis_title="Viewers")
rating_chart.update_xaxes(dtick=1)
rating_chart.update_traces(marker_line_width=0, hovertemplate="Rating %{x}<br>Viewers: %{y}<extra></extra>")

category_chart = px.pie(
    category_revenue,
    names="Category",
    values="Monthly_Revenue",
    hole=0.62,
    color_discrete_sequence=palette,
)
category_chart.update_layout(**chart_layout)
category_chart.update_traces(textposition="inside", textinfo="percent+label", hole=0.62, marker_line_color="#151515", marker_line_width=2)

device_chart = px.bar(
    device_minutes,
    x="Watch_Time_Minutes",
    y="Device",
    orientation="h",
    color="Watch_Time_Minutes",
    color_continuous_scale=["#641016", "#e50914", "#ff646a"],
    labels={"Watch_Time_Minutes": "Viewing minutes"},
)
device_chart.update_layout(**chart_layout, coloraxis_showscale=False, xaxis_title="Minutes watched", yaxis_title=None)
device_chart.update_yaxes(categoryorder="total ascending")
device_chart.update_traces(marker_line_width=0, hovertemplate="%{y}<br>%{x:,.0f} minutes<extra></extra>")

title_chart = px.bar(
    top_title_counts,
    x="Watch_Count",
    y="Title",
    orientation="h",
    color="Watch_Count",
    color_continuous_scale=["#641016", "#e50914", "#ff646a"],
    labels={"Watch_Count": "Watch count"},
)
title_chart.update_layout(**chart_layout, coloraxis_showscale=False, xaxis_title="Total watch count", yaxis_title=None)
title_chart.update_yaxes(categoryorder="total ascending")
title_chart.update_traces(marker_line_width=0, hovertemplate="%{y}<br>%{x:,.0f} watches<extra></extra>")

monthly_watch_chart = px.line(
    monthly_watch_count,
    x="Watch_Month",
    y="Watch_Count",
    markers=True,
    labels={"Watch_Count": "Watch count"},
)
monthly_watch_chart.update_layout(**chart_layout, xaxis_title=None, yaxis_title="Total watch count")
monthly_watch_chart.update_xaxes(tickformat="%b %Y")
monthly_watch_chart.update_traces(
    line={"color": "#e50914", "width": 3},
    marker={"color": "#f5f2ed", "size": 8, "line": {"color": "#e50914", "width": 2}},
    hovertemplate="%{x|%B %Y}<br>%{y:,.0f} watches<extra></extra>",
)

language_chart = px.bar(
    language_watch_count,
    x="Language",
    y="Watch_Count",
    color="Watch_Count",
    color_continuous_scale=["#641016", "#e50914", "#ff646a"],
    labels={"Watch_Count": "Watch count"},
)
language_chart.update_layout(**chart_layout, coloraxis_showscale=False, xaxis_title=None, yaxis_title="Total watch count")
language_chart.update_traces(marker_line_width=0, hovertemplate="%{x}<br>%{y:,.0f} watches<extra></extra>")

left, right = st.columns(2, gap="medium")
with left:
    with st.container(border=True):
        st.markdown("#### Revenue by region")
        st.plotly_chart(region_chart, use_container_width=True, config={"displayModeBar": False})
    with st.container(border=True):
        st.markdown("#### Ratings by subscription plan")
        st.plotly_chart(plan_chart, use_container_width=True, config={"displayModeBar": False})
with right:
    with st.container(border=True):
        st.markdown("#### Viewer rating count")
        st.plotly_chart(rating_chart, use_container_width=True, config={"displayModeBar": False})
    with st.container(border=True):
        st.markdown("#### Revenue by category")
        st.plotly_chart(category_chart, use_container_width=True, config={"displayModeBar": False})

st.markdown(
    '<div class="section-heading"><span></span><h2>Viewing patterns</h2></div>',
    unsafe_allow_html=True,
)

patterns_left, patterns_right = st.columns(2, gap="medium")
with patterns_left:
    with st.container(border=True):
        st.markdown("#### Viewing minutes by device")
        st.plotly_chart(device_chart, use_container_width=True, config={"displayModeBar": False})
    with st.container(border=True):
        st.markdown("#### Most-watched titles")
        st.plotly_chart(title_chart, use_container_width=True, config={"displayModeBar": False})
with patterns_right:
    with st.container(border=True):
        st.markdown("#### Monthly watch count")
        st.plotly_chart(monthly_watch_chart, use_container_width=True, config={"displayModeBar": False})
    with st.container(border=True):
        st.markdown("#### Watch count by language")
        st.plotly_chart(language_chart, use_container_width=True, config={"displayModeBar": False})

st.markdown(
    '<div class="section-heading"><span></span><h2>What stands out</h2></div>',
    unsafe_allow_html=True,
)


def show_insight(label: str, value: str, detail: str) -> None:
    with st.container(border=True):
        st.markdown(
            f'<div class="insight-kicker">{escape(label)}</div>'
            f'<div class="insight-value">{escape(value)}</div>'
            f'<div class="insight-detail">{escape(detail)}</div>',
            unsafe_allow_html=True,
        )


total_revenue = netflix["Monthly_Revenue"].sum()
top_region = region_revenue.nlargest(2, "Monthly_Revenue")
top_region_name = top_region.iloc[0]["Region"]
top_region_revenue = top_region.iloc[0]["Monthly_Revenue"]
region_revenue_gap = top_region_revenue - top_region.iloc[1]["Monthly_Revenue"]

top_category = category_revenue.loc[category_revenue["Monthly_Revenue"].idxmax()]
top_category_share = top_category["Monthly_Revenue"] / total_revenue * 100 if total_revenue else 0

rating_distribution = netflix["Rating"].value_counts()
most_common_rating = rating_distribution.idxmax()
most_common_rating_share = rating_distribution.max() / len(netflix) * 100
high_rating_share = netflix["Rating"].isin([4, 5]).mean() * 100

plan_summary = netflix.groupby("Subscription_Plan").agg(
    revenue=("Monthly_Revenue", "sum"),
    average_rating=("Rating", "mean"),
)
top_revenue_plan = plan_summary["revenue"].idxmax()
top_rated_plan = plan_summary["average_rating"].idxmax()
top_plan_revenue_share = plan_summary.loc[top_revenue_plan, "revenue"] / total_revenue * 100 if total_revenue else 0
top_plan_average_rating = plan_summary.loc[top_rated_plan, "average_rating"]

monthly_records = (
    netflix.dropna(subset=["Watch_Date"])
    .assign(Watch_Month=lambda data: data["Watch_Date"].dt.to_period("M"))
    .groupby("Watch_Month")
    .size()
    .sort_index()
)

insight_columns = st.columns(3, gap="medium")
with insight_columns[0]:
    show_insight(
        "Regional race",
        f"{top_region_name} · ₹{top_region_revenue:,.0f}",
        f"The top region leads the runner-up by just ₹{region_revenue_gap:,.0f}.",
    )
with insight_columns[1]:
    show_insight(
        "Category leader",
        f"{top_category['Category']} · {top_category_share:.1f}%",
        f"It generated ₹{top_category['Monthly_Revenue']:,.0f} in monthly revenue, the largest category total.",
    )
with insight_columns[2]:
    show_insight(
        "Ratings pulse",
        f"{most_common_rating}-star · {most_common_rating_share:.0f}%",
        f"The most common score is {most_common_rating} stars; {high_rating_share:.0f}% of records are rated 4 or 5.",
    )

insight_columns = st.columns(2, gap="medium")
with insight_columns[0]:
    show_insight(
        "Plan contrast",
        f"{top_revenue_plan} leads revenue · {top_rated_plan} leads ratings",
        f"{top_revenue_plan} contributes {top_plan_revenue_share:.1f}% of revenue; "
        f"{top_rated_plan} has the strongest average rating at {top_plan_average_rating:.2f}/5.",
    )
with insight_columns[1]:
    if len(monthly_records) > 1:
        first_month = monthly_records.index[0]
        peak_month = monthly_records.idxmax()
        first_month_count = monthly_records.iloc[0]
        peak_month_count = monthly_records.max()
        peak_months = monthly_records[monthly_records == peak_month_count].index
        peak_month_labels = ", ".join(month.strftime("%b %Y") for month in peak_months)
        change = (peak_month_count - first_month_count) / first_month_count * 100 if first_month_count else 0
        show_insight(
            "Viewing rhythm",
            f"{change:+.0f}% to {peak_month_count} records",
            f"Monthly records rose from {first_month_count} in {first_month.strftime('%b')} "
            f"to a peak in {peak_month_labels}.",
        )
    else:
        show_insight("Viewing rhythm", "Not enough date coverage", "More than one month of valid watch dates is needed for a trend comparison.")

st.markdown(
    '<div class="footer">NETFLIX VIEWING INSIGHTS <span style="color:#e50914">/</span> '
    f'{len(netflix):,} records <span style="color:#e50914">/</span> '
    f'₹{netflix["Monthly_Revenue"].sum():,.0f} total monthly revenue</div>',
    unsafe_allow_html=True,
)
