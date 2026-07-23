import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_segments


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# PROFESSIONAL DARK STYLE
# ==================================================

st.markdown("""
<style>

.main {
    background-color:#0F172A;
}


h1 {
    color:white;
    font-size:42px;
    font-weight:800;
}


h2,h3 {
    color:#E2E8F0;
}


/* KPI CARDS */

[data-testid="metric-container"] {

    background:
    linear-gradient(
        135deg,
        #1E293B,
        #334155
    );

    padding:20px;

    border-radius:18px;

    border:1px solid #475569;

    box-shadow:
    0px 8px 20px rgba(0,0,0,0.25);

}


[data-testid="metric-container"] label {

    color:#94A3B8;

}


[data-testid="metric-container"] div {

    color:white;

    font-size:30px;

    font-weight:700;

}



/* Sidebar */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
        180deg,
        #020617,
        #1E293B
    );

}


section[data-testid="stSidebar"] * {

    color:white;

}



/* Dataframes */

[data-testid="stDataFrame"] {

    border-radius:15px;

}



/* Download Button */

.stDownloadButton button {

    background:#2563EB;

    color:white;

    border-radius:12px;

    padding:12px 25px;

    font-weight:600;

}


.stDownloadButton button:hover {

    background:#1D4ED8;

}

</style>
""",
unsafe_allow_html=True)



# ==================================================
# HEADER
# ==================================================

st.markdown("""
<h1>
👥 Customer Segmentation
</h1>

<p style="
color:#94A3B8;
font-size:18px;
">
AI Driven RFM Analysis | Customer Behavior Intelligence | Cluster Insights
</p>

""",
unsafe_allow_html=True)



# ==================================================
# LOAD DATA
# ==================================================

segments = load_segments()


if segments.empty:

    st.error(
        "customer_segments.csv not found."
    )

    st.stop()



# ==================================================
# SIDEBAR FILTER
# ==================================================

cluster_col = None


for col in [
    "Cluster",
    "cluster",
    "Segment",
    "segment"
]:

    if col in segments.columns:

        cluster_col = col

        break



if cluster_col:

    clusters = sorted(
        segments[cluster_col]
        .unique()
    )


    selected = st.sidebar.multiselect(

        "🎯 Select Cluster",

        clusters,

        default=clusters

    )


    segments = segments[
        segments[cluster_col]
        .isin(selected)
    ]



# ==================================================
# KPI SECTION
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
📌 Customer Intelligence Overview
</h2>
""",
unsafe_allow_html=True
)



total_customers = len(segments)


avg_recency = (
    segments["Recency"]
    .mean()
)


avg_frequency = (
    segments["Frequency"]
    .mean()
)


avg_monetary = (
    segments["Monetary"]
    .mean()
)



c1,c2,c3,c4 = st.columns(4)



c1.metric(
    "👥 Customers",
    f"{total_customers:,}"
)


c2.metric(
    "⏳ Avg Recency",
    f"{avg_recency:.1f}"
)


c3.metric(
    "🔁 Avg Frequency",
    f"{avg_frequency:.1f}"
)


c4.metric(
    "💰 Avg Monetary",
    f"${avg_monetary:,.0f}"
)



# ==================================================
# CLUSTER DISTRIBUTION
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
📊 Customer Cluster Distribution
</h2>
""",
unsafe_allow_html=True
)



if cluster_col:


    fig = px.histogram(

        segments,

        x=cluster_col,

        color=cluster_col,

        template="plotly_dark"

    )


    fig.update_layout(

        height=420,

        paper_bgcolor="#0F172A",

        plot_bgcolor="#0F172A",

        font=dict(
            color="white"
        )

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



# ==================================================
# RFM ANALYSIS
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
📈 Customer Value Analysis
</h2>
""",
unsafe_allow_html=True
)



fig = px.scatter(

    segments,

    x="Frequency",

    y="Monetary",

    color=cluster_col if cluster_col else None,

    size="Recency",

    hover_data=segments.columns,

    template="plotly_dark"

)



fig.update_layout(

    height=500,

    paper_bgcolor="#0F172A",

    plot_bgcolor="#0F172A",

    font=dict(
        color="white"
    )

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ==================================================
# CLUSTER STATISTICS
# ==================================================

if cluster_col:


    st.markdown(
    "<hr>",
    unsafe_allow_html=True
    )


    st.markdown(
    """
    <h2>
    📋 Cluster Performance Summary
    </h2>
    """,
    unsafe_allow_html=True
    )


    summary = (

        segments

        .groupby(cluster_col)[
            [
                "Recency",
                "Frequency",
                "Monetary"
            ]
        ]

        .mean()

        .round(2)

    )


    st.dataframe(

        summary,

        use_container_width=True,

        height=350

    )



# ==================================================
# TOP CUSTOMERS
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
🏆 High Value Customers
</h2>
""",
unsafe_allow_html=True
)



top = (

    segments

    .sort_values(
        "Monetary",
        ascending=False
    )

    .head(20)

)



st.dataframe(

    top,

    use_container_width=True,

    height=400

)



# ==================================================
# DOWNLOAD
# ==================================================

csv = segments.to_csv(
    index=False
)


st.download_button(

    "⬇ Download Customer Segments",

    csv,

    file_name="customer_segments.csv",

    mime="text/csv"

)