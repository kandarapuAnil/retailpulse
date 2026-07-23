import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

from utils import (
    load_prophet_forecast,
    load_lstm_forecast,
    load_hybrid_forecast,
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Demand Forecasting",
    page_icon="📈",
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



/* Table */

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
📈 Demand Forecasting
</h1>

<p style="
color:#94A3B8;
font-size:18px;
">
AI Forecast Intelligence | Prophet | LSTM | Hybrid Model Comparison
</p>

""",
unsafe_allow_html=True)



# ==================================================
# LOAD DATA
# ==================================================

try:

    prophet = load_prophet_forecast()

    lstm = load_lstm_forecast()

    hybrid = load_hybrid_forecast()


except Exception as e:

    st.error(
        f"Error loading forecast files:\n{e}"
    )

    st.stop()



# ==================================================
# PREDICTION EXTRACTION
# ==================================================

if "yhat" in prophet.columns:

    prophet_pred = (
        prophet["yhat"]
        .reset_index(drop=True)
    )


elif "Prediction" in prophet.columns:

    prophet_pred = (
        prophet["Prediction"]
        .reset_index(drop=True)
    )


else:

    prophet_pred = (
        prophet.iloc[:,-1]
        .reset_index(drop=True)
    )



if "Prediction" in lstm.columns:

    lstm_pred = (
        lstm["Prediction"]
        .reset_index(drop=True)
    )


elif "LSTM" in lstm.columns:

    lstm_pred = (
        lstm["LSTM"]
        .reset_index(drop=True)
    )


else:

    lstm_pred = (
        lstm.iloc[:,-1]
        .reset_index(drop=True)
    )



if "Actual" in hybrid.columns:

    actual = (
        hybrid["Actual"]
        .reset_index(drop=True)
    )


else:

    actual = (
        hybrid.iloc[:,0]
        .reset_index(drop=True)
    )



if "Hybrid" in hybrid.columns:

    hybrid_pred = (
        hybrid["Hybrid"]
        .reset_index(drop=True)
    )


elif "Prediction" in hybrid.columns:

    hybrid_pred = (
        hybrid["Prediction"]
        .reset_index(drop=True)
    )


else:

    hybrid_pred = (
        hybrid.iloc[:,-1]
        .reset_index(drop=True)
    )



# ==================================================
# ALIGN LENGTH
# ==================================================

n = min(
    len(actual),
    len(prophet_pred),
    len(lstm_pred),
    len(hybrid_pred)
)


actual = actual.tail(n).reset_index(drop=True)

prophet_pred = prophet_pred.tail(n).reset_index(drop=True)

lstm_pred = lstm_pred.tail(n).reset_index(drop=True)

hybrid_pred = hybrid_pred.tail(n).reset_index(drop=True)



# ==================================================
# METRICS
# ==================================================

def metrics(y_true,y_pred):

    mae = mean_absolute_error(
        y_true,
        y_pred
    )


    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )


    mask = y_true != 0


    if mask.sum()==0:

        mape=0

    else:

        mape = (
            np.mean(
                np.abs(
                    (
                        y_true[mask]
                        -
                        y_pred[mask]
                    )
                    /
                    y_true[mask]
                )
            )
            *
            100
        )


    return mae,rmse,mape



prophet_mae,prophet_rmse,prophet_mape = metrics(
    actual,
    prophet_pred
)


lstm_mae,lstm_rmse,lstm_mape = metrics(
    actual,
    lstm_pred
)


hybrid_mae,hybrid_rmse,hybrid_mape = metrics(
    actual,
    hybrid_pred
)



# ==================================================
# MODEL PERFORMANCE
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



c1,c2,c3 = st.columns(3)


c1.metric(
    "🔵 Prophet MAPE",
    f"{prophet_mape:.2f}%"
)


c2.metric(
    "🟣 LSTM MAPE",
    f"{lstm_mape:.2f}%"
)


c3.metric(
    "🟢 Hybrid MAPE",
    f"{hybrid_mape:.2f}%"
)



# ==================================================
# FORECAST GRAPH
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
📊 Forecast Comparison
</h2>
""",
unsafe_allow_html=True
)



fig = go.Figure()



fig.add_trace(
    go.Scatter(
        y=actual,
        mode="lines",
        name="Actual",
        line=dict(width=4)
    )
)


fig.add_trace(
    go.Scatter(
        y=prophet_pred,
        mode="lines",
        name="Prophet"
    )
)


fig.add_trace(
    go.Scatter(
        y=lstm_pred,
        mode="lines",
        name="LSTM"
    )
)


fig.add_trace(
    go.Scatter(
        y=hybrid_pred,
        mode="lines",
        name="Hybrid",
        line=dict(width=4)
    )
)



fig.update_layout(

    template="plotly_dark",

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
# PERFORMANCE TABLE
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.markdown(
"""
<h2>
📋 Model Accuracy Comparison
</h2>
""",
unsafe_allow_html=True
)



comparison = pd.DataFrame(
{
"Model":[
"Prophet",
"LSTM",
"Hybrid"
],

"MAE":[
prophet_mae,
lstm_mae,
hybrid_mae
],

"RMSE":[
prophet_rmse,
lstm_rmse,
hybrid_rmse
],

"MAPE":[
prophet_mape,
lstm_mape,
hybrid_mape
]
}
)



st.dataframe(
    comparison,
    use_container_width=True,
    height=350
)



# ==================================================
# DOWNLOAD
# ==================================================

csv = comparison.to_csv(
    index=False
).encode("utf-8")



st.download_button(

    "⬇ Download Forecast Metrics",

    data=csv,

    file_name="forecast_metrics.csv",

    mime="text/csv"

)