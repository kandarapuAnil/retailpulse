import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Churn Prediction",
    page_icon="🚨",
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



/* DOWNLOAD BUTTON */

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
🚨 Customer Churn Prediction
</h1>

<p style="
color:#94A3B8;
font-size:18px;
">
AI Customer Retention Intelligence | XGBoost Risk Analysis
</p>

""",
unsafe_allow_html=True)




# ==================================================
# LOAD DATA
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "processed"


try:

    df = pd.read_csv(
        DATA_DIR / "customer_features.csv"
    )


except Exception as e:

    st.error(
        f"Error loading file:\n{e}"
    )

    st.stop()



# ==================================================
# CREATE CHURN LABEL
# ==================================================

df["Churn"] = (
    df["Recency"] > 90
).astype(int)



# ==================================================
# LOAD MODEL
# ==================================================

MODEL_PATH = (
    BASE_DIR /
    "models" /
    "churn_model.pkl"
)


if not MODEL_PATH.exists():

    st.error(
        f"Model not found:\n{MODEL_PATH}"
    )

    st.stop()



model = joblib.load(
    MODEL_PATH
)




# ==================================================
# PREDICTION
# ==================================================

X = df[
    [
        "Recency",
        "Frequency",
        "Monetary"
    ]
]


y = df["Churn"]


prediction = model.predict(X)


probability = (
    model.predict_proba(X)[:,1]
)


df["Prediction"] = prediction

df["Probability"] = probability




# ==================================================
# METRICS
# ==================================================

accuracy = accuracy_score(
    y,
    prediction
)


precision = precision_score(
    y,
    prediction
)


recall = recall_score(
    y,
    prediction
)


f1 = f1_score(
    y,
    prediction
)


churn_rate = y.mean()*100




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
🤖 Model Performance Overview
</h2>
""",
unsafe_allow_html=True
)



c1,c2,c3,c4 = st.columns(4)



c1.metric(
    "🎯 Accuracy",
    f"{accuracy:.2%}"
)


c2.metric(
    "✅ Precision",
    f"{precision:.2%}"
)


c3.metric(
    "📌 Recall",
    f"{recall:.2%}"
)


c4.metric(
    "⭐ F1 Score",
    f"{f1:.2%}"
)




# ==================================================
# CHURN GAUGE
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)



st.markdown(
"""
<h2>
🚨 Customer Risk Overview
</h2>
""",
unsafe_allow_html=True
)




fig = go.Figure(
    go.Indicator(

        mode="gauge+number",

        value=churn_rate,

        title={
            "text":
            "Churn Rate (%)"
        },


        gauge={

            "axis":{
                "range":[0,100]
            },

            "bar":{
                "color":"red"
            }

        }

    )
)



fig.update_layout(

    template="plotly_dark",

    height=350,

    paper_bgcolor="#0F172A",

    font={
        "color":"white"
    }

)



st.plotly_chart(

    fig,

    use_container_width=True

)




# ==================================================
# FEATURE IMPORTANCE
# ==================================================

if hasattr(
    model,
    "feature_importances_"
):


    st.markdown(
    "<hr>",
    unsafe_allow_html=True
    )


    st.markdown(
    """
    <h2>
    🔍 Important Churn Factors
    </h2>
    """,
    unsafe_allow_html=True
    )



    importance = pd.DataFrame({

        "Feature":
        X.columns,

        "Importance":
        model.feature_importances_

    })



    fig = px.bar(

        importance.sort_values(

            "Importance",

            ascending=True

        ),


        x="Importance",

        y="Feature",

        orientation="h",

        template="plotly_dark"

    )


    fig.update_layout(

        height=350,

        paper_bgcolor="#0F172A",

        plot_bgcolor="#0F172A"

    )



    st.plotly_chart(

        fig,

        use_container_width=True

    )




# ==================================================
# CONFUSION MATRIX
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
📊 Confusion Matrix
</h2>
""",
unsafe_allow_html=True
)



cm = confusion_matrix(
    y,
    prediction
)


cm_df = pd.DataFrame(

    cm,

    index=[
        "Actual No",
        "Actual Yes"
    ],

    columns=[
        "Pred No",
        "Pred Yes"
    ]

)



st.dataframe(

    cm_df,

    use_container_width=True

)




# ==================================================
# HIGH RISK CUSTOMERS
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
⚠️ High Risk Customers
</h2>
""",
unsafe_allow_html=True
)



risk = (

    df

    .sort_values(

        "Probability",

        ascending=False

    )

    .head(20)

)


customer_col = "Customer ID" if "Customer ID" in risk.columns else "CustomerID"

st.dataframe(
    risk[
        [
            customer_col,
            "Recency",
            "Frequency",
            "Monetary",
            "Probability"
        ]
    ],
    use_container_width=True,
    height=400
)




# ==================================================
# DOWNLOAD
# ==================================================

csv = risk.to_csv(
    index=False
)



st.download_button(

    "⬇ Download High Risk Customers",

    csv,

    file_name="high_risk_customers.csv",

    mime="text/csv"

)