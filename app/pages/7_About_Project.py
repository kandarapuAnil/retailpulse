import streamlit as st


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="About RetailPulse",
    page_icon="ℹ️",
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

    font-size:44px;

    font-weight:800;

}



h2 {

    color:#E2E8F0;

}



p, li {

    color:#CBD5E1;

    font-size:18px;

}



/* CONTENT CARDS */

.about-card {

    background:

    linear-gradient(
        135deg,
        #1E293B,
        #334155
    );

    padding:30px;

    border-radius:20px;

    border:1px solid #475569;

    margin-bottom:25px;

    box-shadow:

    0px 8px 20px rgba(0,0,0,0.25);

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
ℹ️ About RetailPulse
</h1>

<p style="
color:#94A3B8;
font-size:20px;
">
AI Powered Retail Intelligence Platform
</p>

""",
unsafe_allow_html=True)




# ==================================================
# ABOUT CONTENT
# ==================================================

st.markdown("""

<div class="about-card">

<h2>
🚀 RetailPulse
</h2>


<p>
RetailPulse is an AI-powered Retail Analytics Dashboard
designed to transform retail data into actionable business
insights using Machine Learning and Data Analytics.
</p>


</div>


<div class="about-card">


<h2>
✨ Features
</h2>


<ul>

<li>👥 Customer Segmentation</li>

<li>📈 Demand Forecasting</li>

<li>🤖 Hybrid Forecast Model</li>

<li>🚨 Churn Prediction</li>

<li>📦 Inventory Optimization</li>

<li>🧠 Model Explainability</li>

</ul>


</div>



<div class="about-card">


<h2>
🧠 Machine Learning Models
</h2>


<ul>

<li>KMeans Clustering</li>

<li>Prophet Forecasting</li>

<li>LSTM Deep Learning</li>

<li>XGBoost Classification</li>

<li>Random Forest</li>

</ul>


</div>



<div class="about-card">


<h2>
⚙️ Technologies
</h2>


<ul>

<li>🐍 Python</li>

<li>📊 Streamlit</li>

<li>📈 Plotly</li>

<li>🤖 Scikit-Learn</li>

<li>🔥 PyTorch</li>

<li>📅 Prophet</li>

<li>🚀 XGBoost</li>

</ul>


</div>



<div class="about-card">


<h2>
👨‍💻 Developed By
</h2>


<h3>
Anil
</h3>


<p>
2026
</p>


</div>


""",
unsafe_allow_html=True)




# ==================================================
# FOOTER
# ==================================================

st.markdown(
"<hr>",
unsafe_allow_html=True
)


st.caption(
"RetailPulse AI | Executive Retail Analytics Platform"
)