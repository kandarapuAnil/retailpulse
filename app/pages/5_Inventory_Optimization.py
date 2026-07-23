import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Inventory Optimization",
    page_icon="📦",
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



/* SIDEBAR */

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



/* TABLE */

[data-testid="stDataFrame"] {

    border-radius:15px;

}



/* BUTTON */

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
📦 Inventory Optimization
</h1>

<p style="
color:#94A3B8;
font-size:18px;
">
Smart Stock Monitoring | Reorder Intelligence | Inventory Analytics
</p>

""",
unsafe_allow_html=True)



# ==================================================
# LOAD INVENTORY DATA
# ==================================================

try:

    inventory = pd.read_csv(
        "data/processed/inventory_recommendations.csv"
    )


except Exception as e:

    st.error(
        f"Unable to load inventory data.\n{e}"
    )

    st.stop()



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
📌 Inventory Overview
</h2>
""",
unsafe_allow_html=True
)



total_products = len(inventory)


reorder_products = (
    inventory["Status"]
    ==
    "Reorder"
).sum()


avg_stock = (
    inventory["Current_Stock"]
    .mean()
)


avg_reorder = (
    inventory["Reorder_Point"]
    .mean()
)



c1,c2,c3,c4 = st.columns(4)



c1.metric(
    "📦 Products",
    f"{total_products:,}"
)


c2.metric(
    "🚨 Reorder Items",
    reorder_products
)


c3.metric(
    "📊 Avg Stock",
    f"{avg_stock:.1f}"
)


c4.metric(
    "🎯 Avg Reorder Point",
    f"{avg_reorder:.1f}"
)




# ==================================================
# INVENTORY ANALYSIS
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
📊 Inventory Analytics
</h2>
""",
unsafe_allow_html=True
)



left,right = st.columns(2)



# -------------------------
# STATUS PIE
# -------------------------

with left:


    fig = px.pie(

        inventory,

        names="Status",

        template="plotly_dark",

        hole=0.45

    )


    fig.update_layout(

        height=420,

        paper_bgcolor="#0F172A",

        font=dict(
            color="white"
        )

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )




# -------------------------
# STOCK DISTRIBUTION
# -------------------------

with right:


    fig = px.histogram(

        inventory,

        x="Current_Stock",

        nbins=30,

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
# STOCK VS REORDER
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
📦 Stock Level vs Reorder Point
</h2>
""",
unsafe_allow_html=True
)



fig = go.Figure()



fig.add_trace(

    go.Bar(

        x=inventory["Description"].head(20),

        y=inventory["Current_Stock"].head(20),

        name="Current Stock"

    )

)



fig.add_trace(

    go.Bar(

        x=inventory["Description"].head(20),

        y=inventory["Reorder_Point"].head(20),

        name="Reorder Point"

    )

)



fig.update_layout(

    template="plotly_dark",

    barmode="group",

    height=550,

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
# REORDER RECOMMENDATIONS
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
🚨 Top Products to Reorder
</h2>
""",
unsafe_allow_html=True
)



top = (

    inventory

    .sort_values(

        "Reorder_Quantity",

        ascending=False

    )

    .head(20)

)



st.dataframe(

    top[

        [

            "StockCode",

            "Description",

            "Current_Stock",

            "Reorder_Point",

            "Reorder_Quantity",

            "Status"

        ]

    ],

    use_container_width=True,

    height=400

)




# ==================================================
# SEARCH
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
🔍 Product Search
</h2>
""",
unsafe_allow_html=True
)



search = st.text_input(
    "Search Product"
)



if search:


    result = inventory[

        inventory["Description"]

        .str.contains(
            search,
            case=False,
            na=False
        )

    ]


    st.dataframe(

        result,

        use_container_width=True

    )




# ==================================================
# DOWNLOAD
# ==================================================

csv = inventory.to_csv(
    index=False
)



st.download_button(

    "⬇ Download Inventory Report",

    csv,

    file_name="inventory_report.csv",

    mime="text/csv"

)