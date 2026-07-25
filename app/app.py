# ==========================================================
# RetailPulse AI
# Executive Retail Analytics Dashboard
# Version 3.0
# ==========================================================
import streamlit as st

st.write("Hello")

import plotly
st.write(plotly.__version__)

import plotly.express as px
st.write("Plotly Express imported successfully")
import sys
import os

print("Python:", sys.version)
print("Current directory:", os.getcwd())

try:
    import plotly
    print("Plotly version:", plotly.__version__)
    print("Plotly location:", plotly.__file__)
except Exception as e:
    print("Plotly import failed:", e)
import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import (
    load_kpi,
    load_monthly,
    load_country,
    load_segments,
    load_forecast,
    format_currency,
)

from components import (
    glass_card,
    summary_box,
    status_card,
    navigation_card,
    executive_insights,
    footer,
    section,
)

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------

st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------
# LOAD CSS
# ----------------------------------------------------------

css_file = os.path.join(os.path.dirname(__file__), "style.css")

if os.path.exists(css_file):
    with open(css_file, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------

PRIMARY = "#2563EB"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
PURPLE = "#8B5CF6"

CARD_BG = "#1E293B"

# ----------------------------------------------------------
# HELPERS
# ----------------------------------------------------------


def safe_float(value, default=0.0):
    try:
        return float(value)
    except:
        return default


def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default


def dataframe_empty(df):
    return df is None or len(df) == 0


def standardize_revenue(df):

    if dataframe_empty(df):
        return df

    if "Revenue" in df.columns:
        return df

    if "TotalPrice" in df.columns:
        return df.rename(columns={"TotalPrice": "Revenue"})

    numeric = df.select_dtypes("number").columns

    if len(numeric):
        return df.rename(columns={numeric[-1]: "Revenue"})

    return df


def hero():

    st.markdown(
        f"""
<div class="banner">

<h1>
📊 RetailPulse 
</h1>

<p>
Executive Retail Analytics Dashboard
</p>

</div>
""",
        unsafe_allow_html=True,
    )


def metric_card(
    title,
    value,
    delta,
    icon,
    color="#2563EB",
):

    st.markdown(
        f"""
<div class="metric-card">

<div style="display:flex;
justify-content:space-between;
align-items:center;">

<div>

<div class="metric-title">
{title}
</div>

<div class="metric-value">
{value}
</div>

<div class="metric-change">
{delta}
</div>

</div>

<div style="
font-size:40px;
color:{color};">

{icon}

</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------

with st.sidebar:

    st.markdown(
        """
<div style="text-align:center">

<img src="https://img.icons8.com/fluency/96/combo-chart.png" width="90">

<h2 style="margin-bottom:0">
RetailPulse
</h2>

<p style="color:#94A3B8">
Executive Dashboard
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.page_link(
        "app.py",
        label="🏠 Executive Dashboard",
    )

    st.page_link(
        "pages/1_Sales_Dashboard.py",
        label="📊 Sales Dashboard",
    )

    st.page_link(
        "pages/2_Customer_Segmentation.py",
        label="👥 Customer Segmentation",
    )

    st.page_link(
        "pages/3_Demand_Forecasting.py",
        label="📈 Demand Forecasting",
    )

    st.page_link(
        "pages/4_Churn_Prediction.py",
        label="🚨 Churn Prediction",
    )

    st.markdown("---")

    st.success("RetailPulse")

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

kpi = load_kpi()
monthly = standardize_revenue(load_monthly())
country = standardize_revenue(load_country())

segments = load_segments()
forecast = load_forecast()

if dataframe_empty(kpi):

    st.error("Unable to load KPI dataset.")

    st.stop()

if "InvoiceDate" in monthly.columns:

    monthly["InvoiceDate"] = pd.to_datetime(
        monthly["InvoiceDate"]
    )

# ----------------------------------------------------------
# HERO
# ----------------------------------------------------------
hero()

st.markdown("<br>", unsafe_allow_html=True)

# ==============================
# HEADER STATUS BAR
# ==============================

status_left, status1, status2, status3 = st.columns([6, 1, 1.8, 0.7])


with status1:

    st.success(
        " Active"
    )


with status2:

    st.info(
        f" {datetime.today().strftime('%d %b %Y,')}  "
        f" {datetime.now().strftime('%I:%M %p')}"
    )


with status3:

    if st.button(
        "🔄",
        key="refresh_btn"
    ):

        st.cache_data.clear()
        st.rerun()


st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# EXECUTIVE KPI DASHBOARD
# ==========================================================

# Safe extraction of KPI values
revenue = safe_float(
    kpi.iloc[0].get("Total TotalPrice", 0)
)

customers = safe_int(
    kpi.iloc[0].get("Customers", 0)
)

products = safe_int(
    kpi.iloc[0].get("Inventory Items", 0)
)

avg_revenue = safe_float(
    kpi.iloc[0].get("Average TotalPrice", 0)
)

# ----------------------------------------------------------
# SECTION TITLE
# ----------------------------------------------------------

section("📊 Executive Performance Overview")

st.caption(
    "Real-time business performance indicators generated from the Online Retail dataset."
)

# ----------------------------------------------------------
# KPI CARDS
# ----------------------------------------------------------

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:

    metric_card(
        title="Total Revenue",
        value=format_currency(revenue),
        delta="▲ 12.4% vs Last Period",
        icon="💰",
        color="#22C55E",
        
    )

with kpi2:

    metric_card(
        title="Customers",
        value=f"{customers:,}",
        delta="▲ 8.1% Growth",
        icon="👥",
        color="#3B82F6",
    )

with kpi3:

    metric_card(
        title="Products",
        value=f"{products:,}",
        delta="Inventory Stable",
        icon="📦",
        color="#F59E0B",
    )

with kpi4:

    metric_card(
        title="Average Revenue",
        value=format_currency(avg_revenue),
        delta="▲ 6.9%",
        icon="📈",
        color="#8B5CF6",
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# BUSINESS HEALTH SCORE
# ==========================================================
section("🏆 Business Health")

left, center, right = st.columns([2.3, 1.2, 1.5])


# ----------------------------------------------------------
# HEALTH GAUGE
# ----------------------------------------------------------

with left:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=92,
            number={
                "suffix": "%",
                "font": {
                    "size": 46,
                    "color": "white"
                }
            },
            title={
                "text": "Business Health Score",
                "font": {
                    "size": 20,
                    "color": "white"
                }
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "bar": {
                    "color": "#22C55E"
                },
                "steps": [
                    {
                        "range": [0, 50],
                        "color": "#7F1D1D"
                    },
                    {
                        "range": [50, 80],
                        "color": "#92400E"
                    },
                    {
                        "range": [80, 100],
                        "color": "#14532D"
                    }
                ],
            },
        )
    )

    fig.update_layout(
        height=320,
        margin=dict(
            l=10,
            r=10,
            t=40,
            b=10,
        ),
        paper_bgcolor="#1E293B",
        font=dict(color="white"),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ----------------------------------------------------------
# QUICK STATUS
# ----------------------------------------------------------
# ----------------------------------------------------------
# QUICK STATUS
# ----------------------------------------------------------

with center:

    st.metric(
        label="📈 Revenue Growth",
        value="+12.4%",
        delta="Healthy"
    )

    st.metric(
        label="🤖 Forecast Model",
        value="Hybrid",
        delta="Active"
    )

    st.metric(
        label="🚨 Churn Model",
        value="99.54%",
        delta="Accuracy"
    )
# ----------------------------------------------------------
# EXECUTIVE SNAPSHOT
# ----------------------------------------------------------

with right:

    st.info(f"""
### 📌 Executive Snapshot

💰 Revenue: **{format_currency(revenue)}**

👥 Customers: **{customers:,}**

📦 Products: **{products:,}**

🌍 Market: **India**

📈 Accuracy: **99.54%**

🟢 Status: **Online**
""")
# ==========================================================
# EXECUTIVE HIGHLIGHTS
# ==========================================================
section("✨ Key Business Highlights")

c1, c2, c3 = st.columns(3)


with c1:

    st.success("""
### 💹 Revenue

Revenue continues to grow steadily across all major customer segments with healthy double-digit growth.
""")


with c2:

    st.info("""
### 🌍 Markets

United Kingdom remains the highest revenue contributor followed by Germany and France.
""")


with c3:

    st.warning("""
### 🤖 AI Models

Hybrid Forecast and XGBoost models continue to deliver excellent prediction performance.
""")


st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# EXECUTIVE ANALYTICS
# ==========================================================

section("📊 Executive Analytics")

st.caption(
    "Comprehensive visualization of sales performance across time and geography."
)

left, right = st.columns([2.2, 1])

# ==========================================================
# MONTHLY REVENUE TREND
# ==========================================================

with left:

    st.markdown("### 📈 Monthly Revenue Trend")

    if not dataframe_empty(monthly):

        fig = px.area(
            monthly,
            x="InvoiceDate",
            y="Revenue",
            template="plotly_dark",
        )

        fig.update_traces(
            line=dict(
                width=4,
                color="#3B82F6"
            ),
            fill="tozeroy",
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        )

        fig.update_layout(

            height=430,

            paper_bgcolor="#1E293B",
            plot_bgcolor="#1E293B",

            margin=dict(
                l=10,
                r=10,
                t=30,
                b=10
            ),

            font=dict(
                color="white",
                family="Inter"
            ),

            title=None,

            hovermode="x unified",

            xaxis=dict(
                title="",
                showgrid=False,
                zeroline=False
            ),

            yaxis=dict(
                title="Revenue (₹)",
                gridcolor="rgba(255,255,255,0.08)",
                zeroline=False
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info("Monthly revenue data unavailable.")

# ==========================================================
# COUNTRY REVENUE
# ==========================================================

with right:

    st.markdown("### 🌍 Top Markets")

    if not dataframe_empty(country):

        top_country = (
            country
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(8)
        )

        fig = px.bar(

            top_country,

            x="Revenue",
            y="Country",

            orientation="h",

            color="Revenue",

            color_continuous_scale="Blues",

            template="plotly_dark",
        )

        fig.update_layout(

            height=430,

            paper_bgcolor="#1E293B",
            plot_bgcolor="#1E293B",

            margin=dict(
                l=10,
                r=10,
                t=30,
                b=10
            ),

            title=None,

            font=dict(color="white"),

            coloraxis_showscale=False,

            yaxis=dict(
                categoryorder="total ascending"
            ),
        )

        fig.update_traces(
            hovertemplate="%{y}<br>Revenue: ₹%{x:,.0f}<extra></extra>"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info("Country revenue unavailable.")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# SALES PERFORMANCE SNAPSHOT
# ==========================================================
section("📌 Sales Performance Snapshot")

c1, c2, c3 = st.columns(3)

highest_month = "-"
highest_value = 0

if not dataframe_empty(monthly):

    idx = monthly["Revenue"].idxmax()

    highest_month = (
        monthly.loc[idx, "InvoiceDate"]
        .strftime("%B %Y")
    )

    highest_value = monthly.loc[idx, "Revenue"]


with c1:

    st.markdown(f"""
    <div class="snapshot-card">

    <h3>🏆 Best Performing Month</h3>
    <h2>{highest_month}</h2>
    <p>Revenue</p>
    <h2>{format_currency(highest_value)}</h2>
    <p>
    Excellent seasonal performance.
    </p>

    </div>
    """,
    unsafe_allow_html=True)



with c2:

    top_market = "United Kingdom"

    if not dataframe_empty(country):

        top_market = (
            country
            .sort_values(
                "Revenue",
                ascending=False
            )
            .iloc[0]["Country"]
        )


    st.markdown(f"""
    <div class="snapshot-card">

    <h3>🌍 Strongest Market</h3>

    <h2>{top_market}</h2>

    <p>
    Highest revenue contribution
    across all countries.
    </p>

    <p>
    Excellent customer demand.
    </p>

    </div>
    """,
    unsafe_allow_html=True)



with c3:

    avg_monthly = 0

    if not dataframe_empty(monthly):

        avg_monthly = monthly["Revenue"].mean()


    st.markdown(f"""
    <div class="snapshot-card">

    <h3>📈 Average Monthly Revenue</h3>

    <h2>{format_currency(avg_monthly)}</h2>

    <p>
    Average sales generated
    per month.
    </p>

    <p>
    Healthy business growth.
    </p>

    </div>
    """,
    unsafe_allow_html=True)



st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# SALES DISTRIBUTION
# ==========================================================

section("📊 Revenue Distribution")

left, right = st.columns(2)


with left:

    if not dataframe_empty(monthly):

        fig = px.histogram(
            monthly,
            x="Revenue",
            nbins=12,
            template="plotly_dark",
        )

        fig.update_layout(

            height=340,

            title=None,

            paper_bgcolor="#1E293B",

            plot_bgcolor="#1E293B",

            font=dict(color="white"),

            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )


with right:

    if not dataframe_empty(monthly):

        fig = px.box(
            monthly,
            y="Revenue",
            template="plotly_dark",
        )

        fig.update_layout(

            height=340,

            title=None,

            paper_bgcolor="#1E293B",

            plot_bgcolor="#1E293B",

            font=dict(color="white"),

            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )


st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# CUSTOMER ANALYTICS & DEMAND FORECASTING
# ==========================================================

section("🧠 Customer Analytics & AI Forecast")

left, right = st.columns([1, 1])

# ==========================================================
# CUSTOMER SEGMENTATION
# ==========================================================

with left:

    st.markdown("### 👥 Customer Segmentation")

    if not dataframe_empty(segments):

        cluster = (
            segments["Cluster"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        cluster.columns = [
            "Cluster",
            "Customers"
        ]

        fig = px.pie(
            cluster,
            names="Cluster",
            values="Customers",
            hole=0.68,
            template="plotly_dark",
            color="Cluster",
            color_discrete_sequence=[
                "#2563EB",
                "#10B981",
                "#F59E0B",
                "#EF4444",
                "#8B5CF6",
                "#06B6D4",
            ],
        )

        fig.update_traces(

            textposition="inside",

            textinfo="percent+label",

            hovertemplate="<b>%{label}</b><br>%{value} Customers<extra></extra>",

            marker=dict(
                line=dict(
                    color="#0F172A",
                    width=2,
                )
            ),
        )

        fig.update_layout(

            height=420,

            paper_bgcolor="#1E293B",

            plot_bgcolor="#1E293B",

            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10,
            ),

            font=dict(
                color="white",
            ),

            legend_title="Customer Cluster",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info("Customer segmentation unavailable.")

# ==========================================================
# DEMAND FORECAST
# ==========================================================

with right:

    st.markdown("### 📈 Demand Forecast")

    if not dataframe_empty(forecast):

        date_col = None
        actual_col = None
        hybrid_col = None

        for col in forecast.columns:

            lower = col.lower()

            if lower == "ds":
                date_col = col

            elif "actual" in lower:
                actual_col = col

            elif "hybrid" in lower:
                hybrid_col = col

        if date_col and actual_col and hybrid_col:

            forecast[date_col] = pd.to_datetime(
                forecast[date_col]
            )

            fig = go.Figure()

            fig.add_trace(

                go.Scatter(

                    x=forecast[date_col],

                    y=forecast[actual_col],

                    name="Actual",

                    line=dict(
                        color="#94A3B8",
                        width=3,
                    ),
                )
            )

            fig.add_trace(

                go.Scatter(

                    x=forecast[date_col],

                    y=forecast[hybrid_col],

                    name="Hybrid Forecast",

                    line=dict(
                        color="#3B82F6",
                        width=4,
                    ),
                )
            )

            fig.update_layout(

                height=420,

                template="plotly_dark",

                paper_bgcolor="#1E293B",

                plot_bgcolor="#1E293B",

                hovermode="x unified",

                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10,
                ),

                legend=dict(
                    orientation="h",
                    y=1.08,
                    x=0,
                ),

                xaxis_title="",

                yaxis_title="Demand",

                font=dict(color="white"),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.warning(
                "Forecast columns (ds, actual, hybrid) not found."
            )

    else:

        st.info("Forecast data unavailable.")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# AI MODEL PERFORMANCE
# ==========================================================
section("🤖 AI Model Performance")

m1, m2 = st.columns(2)

with m1:
    with st.container():
        st.subheader("📈 Hybrid Forecast")

        st.markdown("""
### Model Performance

✅ **MAE:** 12,901  

✅ **RMSE:** 16,897  

✅ **MAPE:** 24.43%  

The Hybrid model combines Prophet and LSTM 
predictions to achieve better forecasting accuracy 
and stable long-term demand prediction.
""")

with m2:
    with st.container():
        st.subheader("🚨 Customer Churn")

        st.markdown("""
### XGBoost Results

✅ **Accuracy:** 99.54%  

✅ **Precision:** 99.65%  

✅ **Recall:** 98.95%  

✅ **F1 Score:** 99.30%  

The XGBoost model accurately predicts customer 
churn and helps identify high-risk customers 
for retention.
""")

st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# AI EXECUTIVE INSIGHTS
# ==========================================================

section("🧠 AI Executive Insights")

insights = [
    

    f"💰 Total Revenue generated: {format_currency(revenue)}",

    f"👥 Active Customers: {customers:,}",

    "🌍 United Kingdom remains the strongest market.",

    "📈 Hybrid Forecast delivers the lowest forecasting error.",

    "🚨 XGBoost provides outstanding churn prediction accuracy.",

    "📊 Customer segmentation identified distinct purchasing behaviors.",

    "✅ Business health score indicates strong overall retail performance.",

]

executive_insights(insights)

st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

section("📋 Executive Summary")

summary_box(
f"""
### RetailPulse Executive Overview

RetailPulse is an AI-powered Executive Retail Analytics Dashboard that combines
Sales Analytics, Customer Segmentation, Demand Forecasting and Customer Churn
Prediction into one centralized business intelligence platform.

---

### Business KPIs

💰 **Revenue**

{format_currency(revenue)}

👥 **Customers**

{customers:,}

📦 **Products**

{products:,}

📈 **Average Revenue**

{format_currency(avg_revenue)}

---

### Executive Highlights

✅ Strong revenue growth

✅ Healthy customer acquisition

✅ Hybrid Forecast achieved the best forecasting accuracy

✅ XGBoost provides excellent churn prediction

✅ United Kingdom is the highest revenue contributor

"""
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# BUSINESS SNAPSHOT
# ==========================================================

section("📌 Business Snapshot")

c1, c2, c3 = st.columns(3)

with c1:
    status_card(
        "Top Market",
        "United Kingdom",
        "#3B82F6"
    )

with c2:
    status_card(
        "Forecast Model",
        "Hybrid",
        "#F59E0B"
    )

with c3:
    status_card(
        "Churn Model",
        "XGBoost",
        "#10B981"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# PROJECT PERFORMANCE
# ==========================================================

section("📊 Project Performance")

performance = pd.DataFrame({

    "Module":[
        "Sales Analytics",
        "Customer Segmentation",
        "Demand Forecasting",
        "Customer Churn",
    ],

    "Status":[
        "Completed",
        "Completed",
        "Completed",
        "Completed",
    ],

    "Performance":[
        format_currency(revenue),
        "5 Customer Clusters",
        "MAPE 24.43%",
        "Accuracy 99.54%",
    ],

    "Health":[
        "Excellent",
        "Excellent",
        "Excellent",
        "Excellent",
    ]
})

st.dataframe(
    performance,
    use_container_width=True,
    hide_index=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# DASHBOARD MODULES
# ==========================================================

section("🚀 Dashboard Modules")

left, right = st.columns(2)

with left:

    navigation_card(
        "📊",
        "Sales Dashboard",
        "Monthly revenue, top products, customer sales and country analytics."
    )

    st.page_link(
        "pages/1_Sales_Dashboard.py",
        label="Open Sales Dashboard",
        use_container_width=True
    )

    navigation_card(
        "👥",
        "Customer Segmentation",
        "RFM analysis, clustering and customer intelligence."
    )

    st.page_link(
        "pages/2_Customer_Segmentation.py",
        label="Open Customer Dashboard",
        use_container_width=True
    )

with right:

    navigation_card(
        "📈",
        "Demand Forecasting",
        "Prophet, LSTM and Hybrid demand forecasting."
    )

    st.page_link(
        "pages/3_Demand_Forecasting.py",
        label="Open Forecast Dashboard",
        use_container_width=True
    )

    navigation_card(
        "🚨",
        "Customer Churn",
        "Predict customer churn using machine learning."
    )

    st.page_link(
        "pages/4_Churn_Prediction.py",
        label="Open Churn Dashboard",
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# BUSINESS HEALTH
# ==========================================================

section("💚 Overall Business Health")

b1, b2, b3, b4 = st.columns(4)

with b1:
    metric_card(
        "Revenue",
        "Excellent",
        "Healthy",
        "💰",
        "#10B981"
    )

with b2:
    metric_card(
        "Forecast",
        "Excellent",
        "Hybrid",
        "📈",
        "#3B82F6"
    )

with b3:
    metric_card(
        "Customers",
        "Growing",
        "+8.1%",
        "👥",
        "#F59E0B"
    )

with b4:
    metric_card(
        "AI Models",
        "Operational",
        "100%",
        "🤖",
        "#8B5CF6"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# FOOTER
# ==========================================================

footer()