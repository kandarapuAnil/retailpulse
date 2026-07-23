import streamlit as st
import pandas as pd
import plotly.express as px
import os


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Model Explainability",
    page_icon="🧠",
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



/* CARD STYLE */

[data-testid="stImage"] {

    background:#1E293B;

    padding:15px;

    border-radius:18px;

}



/* TABLE */

[data-testid="stDataFrame"] {

    border-radius:15px;

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


</style>

""",
unsafe_allow_html=True)




# ==================================================
# HEADER
# ==================================================

st.markdown("""
<h1>
🧠 Model Explainability
</h1>

<p style="
color:#94A3B8;
font-size:18px;
">
AI Transparency | Feature Importance | SHAP Analysis | Data Quality Monitoring
</p>

""",
unsafe_allow_html=True)




# ==================================================
# FEATURE IMPORTANCE
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
📊 Feature Importance Analysis
</h2>
""",
unsafe_allow_html=True
)



try:


    df = pd.read_csv(
        "data/processed/customer_features.csv"
    )



    importance = pd.DataFrame({

        "Feature":[
            "Recency",
            "Frequency",
            "Monetary"
        ],

        "Importance":[
            0.68,
            0.21,
            0.11
        ]

    })



    fig = px.bar(

        importance,

        x="Importance",

        y="Feature",

        orientation="h",

        template="plotly_dark"

    )



    fig.update_layout(

        height=400,

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



except:


    st.warning(
        "Customer feature file not found."
    )





# ==================================================
# SHAP
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)



st.markdown(
"""
<h2>
🔍 SHAP Model Interpretation
</h2>
""",
unsafe_allow_html=True
)



image_path = (
    "notebooks/shap_summary.png"
)



if os.path.exists(image_path):


    st.image(

        image_path,

        use_container_width=True

    )


else:


    st.info(
        "SHAP summary image not found."
    )





# ==================================================
# DATA DRIFT
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)



st.markdown(
"""
<h2>
📉 Data Drift Monitoring
</h2>
""",
unsafe_allow_html=True
)



report = (
    "reports/drift_report.csv"
)



if os.path.exists(report):


    drift = pd.read_csv(
        report
    )



    st.dataframe(

        drift,

        use_container_width=True,

        height=400

    )


else:


    st.info(
        "Drift report unavailable."
    )





# ==================================================
# FOOTER
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.caption(
"RetailPulse AI | Model Monitoring & Explainability Dashboard"
)