import streamlit as st

# ==========================================================
# SECTION TITLE
# ==========================================================

def section(title):
    st.markdown(
        f"""
        <div style="
            margin:30px 0 20px 0;
            border-left:5px solid #2563EB;
            padding-left:15px;
        ">
            <h2 style="
                color:#F8FAFC;
                margin:0;
                font-size:30px;
                font-weight:700;">
                {title}
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# GLASS CARD
# ==========================================================

def glass_card(title, content):

    st.markdown(
        f"""
        <div style="
            background: rgba(30,41,59,.88);
            border:1px solid rgba(255,255,255,.08);
            border-radius:20px;
            padding:24px;
            margin-bottom:18px;
            box-shadow:0 10px 30px rgba(0,0,0,.30);
        ">

            <h3 style="
                color:white;
                margin-top:0;
                margin-bottom:15px;
            ">
                {title}
            </h3>

            <p style="
                color:#CBD5E1;
                line-height:1.8;
                font-size:15px;
                margin:0;
            ">
                {content}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================================
# KPI CARD
# ==========================================================

def metric_card(
        title,
        value,
        subtitle,
        icon,
        color="#2563EB"
):

    st.markdown(
        f"""
<div style="
background:linear-gradient(145deg,#1E293B,#111827);
border-radius:18px;
padding:22px;
height:170px;
border:1px solid rgba(255,255,255,.08);
box-shadow:0 10px 25px rgba(0,0,0,.30);
transition:.3s;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
">

<div>

<div style="
font-size:15px;
color:#94A3B8;
font-weight:600;
">

{title}

</div>

<div style="
font-size:34px;
font-weight:700;
margin-top:12px;
color:white;
">

{value}

</div>

<div style="
margin-top:12px;
color:#22C55E;
font-weight:600;
">

{subtitle}

</div>

</div>

<div style="
font-size:46px;
color:{color};
">

{icon}

</div>

</div>

</div>
""",
        unsafe_allow_html=True
    )

# ==========================================================
# STATUS CARD
# ==========================================================

def status_card(
        title,
        value,
        color="#10B981"
):

    st.markdown(
        f"""
<div style="
background:#1E293B;
border-radius:16px;
padding:20px;
margin-bottom:18px;
border-left:6px solid {color};
">

<div style="
font-size:15px;
color:#94A3B8;
">

{title}

</div>

<div style="
font-size:30px;
font-weight:700;
margin-top:8px;
color:white;
">

{value}

</div>

</div>
""",
        unsafe_allow_html=True
    )
# ==========================================================
# SUMMARY BOX
# ==========================================================

def summary_box(content):

    st.markdown(
        f"""
<div style="
background:linear-gradient(135deg,#1E293B,#0F172A);
border-radius:22px;
padding:28px;
margin:15px 0;
border:1px solid rgba(255,255,255,.08);
box-shadow:0 12px 30px rgba(0,0,0,.35);
">

{content}

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# NAVIGATION CARD
# ==========================================================

def navigation_card(
        icon,
        title,
        description
):

    st.markdown(
        f"""
<div style="
background:linear-gradient(145deg,#1E293B,#111827);
padding:22px;
border-radius:18px;
border:1px solid rgba(255,255,255,.08);
margin-bottom:18px;
min-height:170px;
box-shadow:0 8px 20px rgba(0,0,0,.30);
">

<div style="
font-size:48px;
margin-bottom:12px;
">

{icon}

</div>

<div style="
font-size:22px;
font-weight:700;
color:white;
margin-bottom:10px;
">

{title}

</div>

<div style="
font-size:15px;
line-height:1.7;
color:#CBD5E1;
">

{description}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

def executive_insights(insights):

    html = ""

    for item in insights:

        html += f"""
<li style="
margin-bottom:14px;
line-height:1.8;
font-size:16px;
">

{item}

</li>
"""

    st.markdown(
        f"""
<div style="
background:linear-gradient(145deg,#1E293B,#111827);
border-left:6px solid #2563EB;
padding:25px;
border-radius:20px;
box-shadow:0 8px 25px rgba(0,0,0,.35);
">

<h3 style="
margin-top:0;
color:white;
">

🧠 AI Executive Insights

</h3>

<ul style="
padding-left:22px;
color:#CBD5E1;
">

{html}

</ul>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# INFO CARD
# ==========================================================

def info_card(
        title,
        value,
        color="#3B82F6"
):

    st.markdown(
        f"""
<div style="
background:#1E293B;
padding:18px;
border-radius:16px;
border-top:5px solid {color};
text-align:center;
">

<div style="
font-size:15px;
color:#94A3B8;
">

{title}

</div>

<div style="
font-size:32px;
font-weight:700;
margin-top:10px;
color:white;
">

{value}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# SUCCESS MESSAGE
# ==========================================================

def success_banner(message):

    st.markdown(
        f"""
<div style="
background:rgba(34,197,94,.15);
padding:18px;
border-radius:14px;
border-left:6px solid #22C55E;
margin:15px 0;
">

<span style="
font-size:16px;
font-weight:600;
color:#DCFCE7;
">

✅ {message}

</span>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# WARNING MESSAGE
# ==========================================================

def warning_banner(message):

    st.markdown(
        f"""
<div style="
background:rgba(245,158,11,.15);
padding:18px;
border-radius:14px;
border-left:6px solid #F59E0B;
margin:15px 0;
">

<span style="
font-size:16px;
font-weight:600;
color:#FDE68A;
">

⚠️ {message}

</span>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# DASHBOARD HEADER
# ==========================================================

def dashboard_header(
        title,
        subtitle
):

    st.markdown(
        f"""
<div style="
background:linear-gradient(135deg,#2563EB,#4F46E5);
padding:30px;
border-radius:22px;
margin-bottom:25px;
">

<h1 style="
margin:0;
color:white;
font-size:38px;
">

{title}

</h1>

<p style="
margin-top:10px;
color:#E2E8F0;
font-size:17px;
">

{subtitle}

</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# FOOTER
# ==========================================================
def footer():

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
<div style="
margin-top:40px;
padding:30px;
border-top:1px solid rgba(255,255,255,.08);
text-align:center;
">

<div style="
font-size:22px;
font-weight:700;
color:white;
">

📊 RetailPulse

</div>


<div style="
margin-top:10px;
font-size:15px;
color:#94A3B8;
">

Executive Retail Analytics Dashboard

</div>


<div style="
margin-top:15px;
font-size:14px;
color:#64748B;
">

Powered by Streamlit • Plotly • XGBoost • Prophet • PyTorch • SHAP

</div>


<div style="
margin-top:15px;
font-size:14px;
color:#3B82F6;
font-weight:600;
">

Created by Anil | 2026

</div>


</div>
""",
        unsafe_allow_html=True,
    )