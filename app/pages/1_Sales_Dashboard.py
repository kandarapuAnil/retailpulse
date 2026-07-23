import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    load_monthly,
    load_country,
    load_products,
    format_currency,
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# PROFESSIONAL DARK UI STYLE
# ==================================================

st.markdown("""
<style>

.main {
    background-color:#0F172A;
}


/* Main title */

h1 {
    color:white;
    font-size:42px;
    font-weight:800;
}


h2,h3 {
    color:#E2E8F0;
}


/* KPI Cards */

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

    font-size:15px;

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


/* Divider */

hr {

    border:1px solid #334155;

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


/* Dataframe */

[data-testid="stDataFrame"] {

    border-radius:15px;

}


</style>
""",
unsafe_allow_html=True)



# ==================================================
# HEADER
# ==================================================

st.markdown("""
<h1>
📊 Sales Dashboard
</h1>

<p style="
color:#94A3B8;
font-size:18px;
">
Executive Sales Intelligence | Revenue Analytics | Market Insights
</p>

""",
unsafe_allow_html=True)



# ==================================================
# LOAD DATA
# ==================================================

monthly = load_monthly()

country = load_country()

products = load_products()



# ==================================================
# STANDARDIZE REVENUE COLUMN
# ==================================================

def standardize_revenue(df):

    if df.empty:
        return df


    if "Revenue" in df.columns:
        return df


    if "TotalPrice" in df.columns:

        return df.rename(
            columns={
                "TotalPrice":"Revenue"
            }
        )


    numeric_cols = (
        df
        .select_dtypes(include="number")
        .columns
    )


    if len(numeric_cols)>0:

        df = df.rename(
            columns={
                numeric_cols[-1]:"Revenue"
            }
        )


    return df



monthly = standardize_revenue(monthly)

country = standardize_revenue(country)

products = standardize_revenue(products)



# ==================================================
# DATE FORMAT
# ==================================================

if "InvoiceDate" in monthly.columns:

    monthly["InvoiceDate"] = pd.to_datetime(
        monthly["InvoiceDate"],
        errors="coerce"
    )



# ==================================================
# SIDEBAR FILTER
# ==================================================

if (
    not monthly.empty
    and "InvoiceDate" in monthly.columns
):

    st.sidebar.header(
        "📅 Filters"
    )


    min_date = (
        monthly["InvoiceDate"]
        .min()
        .date()
    )


    max_date = (
        monthly["InvoiceDate"]
        .max()
        .date()
    )


    date_range = st.sidebar.date_input(
        "Date Range",
        value=(
            min_date,
            max_date
        )
    )


    if isinstance(
        date_range,
        (tuple,list)
    ):

        if len(date_range)==2:

            start_date,end_date=date_range

        else:

            start_date=end_date=date_range[0]


    else:

        start_date=end_date=date_range



    monthly = monthly[
        (
            monthly["InvoiceDate"]
            >=
            pd.to_datetime(start_date)
        )
        &
        (
            monthly["InvoiceDate"]
            <=
            pd.to_datetime(end_date)
        )
    ]



# ==================================================
# KPI CALCULATION
# ==================================================

if monthly.empty:

    total_revenue=0

    avg_revenue=0

    transactions=0

    best_month="-"



else:

    total_revenue = (
        monthly["Revenue"]
        .sum()
    )


    avg_revenue = (
        monthly["Revenue"]
        .mean()
    )


    transactions=len(monthly)


    best_month = (
        monthly.loc[
            monthly["Revenue"].idxmax(),
            "InvoiceDate"
        ]
        .strftime("%b %Y")
    )



# ==================================================
# KPI CARDS
# ==================================================

st.markdown(
    "<hr>",
    unsafe_allow_html=True
)


st.markdown(
"""
<h2>
📌 Sales Performance Overview
</h2>
""",
unsafe_allow_html=True
)


c1,c2,c3,c4 = st.columns(4)



c1.metric(
    "💰 Revenue",
    format_currency(total_revenue)
)


c2.metric(
    "📈 Average Revenue",
    format_currency(avg_revenue)
)


c3.metric(
    "🏆 Best Month",
    best_month
)


c4.metric(
    "🧾 Records",
    f"{transactions:,}"
)

# ==================================================
# REVENUE TREND
# ==================================================

st.markdown(
    "<hr>",
    unsafe_allow_html=True
)


st.markdown(
"""
<h2>
📈 Revenue Trend Analysis
</h2>
""",
unsafe_allow_html=True
)


if not monthly.empty:

    fig = px.area(
        monthly,
        x="InvoiceDate",
        y="Revenue",
        markers=True,
        template="plotly_dark",
        title=None
    )


    fig.update_layout(

        height=420,

        paper_bgcolor="#0F172A",

        plot_bgcolor="#0F172A",

        font=dict(
            color="white"
        ),

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ==================================================
# MARKET & PRODUCT ANALYSIS
# ==================================================

st.markdown(
    "<hr>",
    unsafe_allow_html=True
)


st.markdown(
"""
<h2>
🌍 Market & Product Insights
</h2>
""",
unsafe_allow_html=True
)


left,right = st.columns(2)



# -------------------------------
# TOP COUNTRIES
# -------------------------------

with left:


    if (
        not country.empty
        and "Country" in country.columns
        and "Revenue" in country.columns
    ):


        fig = px.bar(

            country
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(10),

            x="Revenue",

            y="Country",

            orientation="h",

            template="plotly_dark",

            title="Top Revenue Countries"

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



# -------------------------------
# TOP PRODUCTS
# -------------------------------

with right:


    if (
        not products.empty
        and "Revenue" in products.columns
    ):


        if "Description" in products.columns:

            product_col="Description"


        elif "Product" in products.columns:

            product_col="Product"


        elif "StockCode" in products.columns:

            product_col="StockCode"


        else:

            product_col=products.columns[0]



        fig = px.bar(

            products
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(10),

            x="Revenue",

            y=product_col,

            orientation="h",

            template="plotly_dark",

            title="Top Selling Products"

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
# REVENUE DISTRIBUTION
# ==================================================

st.markdown(
    "<hr>",
    unsafe_allow_html=True
)



st.markdown(
"""
<h2>
📊 Revenue Distribution
</h2>
""",
unsafe_allow_html=True
)



if not monthly.empty:


    hist = px.histogram(

        monthly,

        x="Revenue",

        nbins=30,

        template="plotly_dark",

        title=None

    )


    hist.update_layout(

        height=400,

        paper_bgcolor="#0F172A",

        plot_bgcolor="#0F172A",

        font=dict(
            color="white"
        )

    )



    st.plotly_chart(

        hist,

        use_container_width=True

    )




# ==================================================
# MONTHLY SALES TABLE
# ==================================================

st.markdown(
    "<hr>",
    unsafe_allow_html=True
)



st.markdown(
"""
<h2>
📅 Monthly Sales Records
</h2>
""",
unsafe_allow_html=True
)



st.dataframe(

    monthly,

    use_container_width=True,

    height=420

)




# ==================================================
# DOWNLOAD
# ==================================================

csv = (
    monthly
    .to_csv(index=False)
    .encode("utf-8")
)



st.download_button(

    label="⬇ Download Monthly Sales Report",

    data=csv,

    file_name="monthly_sales.csv",

    mime="text/csv"

)



# ==================================================
# FOOTER
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.caption(
"RetailPulse AI | Executive Sales Analytics Dashboard"
)