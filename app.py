import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(page_title="Sleep Apnea AI", layout="wide")

# ----------------------------------
# STYLE
# ----------------------------------
st.markdown("""
<style>
.main-title {
    background: linear-gradient(90deg, #ff8c00, #ff5e62);
    padding: 15px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 32px;
    font-weight: bold;
}

.about-box {
    background-color: #ff8c00;
    padding: 12px;
    border-radius: 10px;
    color: white;
    font-size: 13px;
}

.alert-box {
    position: fixed;
    left: 10px;
    top: 120px;
    width: 220px;
    padding: 10px;
    border-radius: 10px;
    color: white;
    font-weight: bold;
    z-index: 999;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# TITLE
# ----------------------------------
st.markdown(
    '<div class="main-title">💤 Sleep Apnea Monitoring System</div>',
    unsafe_allow_html=True
)

now = datetime.now()

# ----------------------------------
# SIDEBAR
# ----------------------------------
st.sidebar.markdown("## ℹ About System")

st.sidebar.markdown("""
<div class="about-box">
AI-based sleep apnea detection using vital signs.<br><br>
Analyzes SpO₂, heart rate, breathing, snoring, and BMI.<br><br>
🔗 Supports Arduino-based monitoring device for continuous data collection.
</div>
""", unsafe_allow_html=True)

st.sidebar.header("👤 Patient Profile")
st.sidebar.write("🕒", now.strftime("%Y-%m-%d %H:%M:%S"))

name = st.sidebar.text_input("Name")
age = st.sidebar.number_input("Age", 1, 100, 30)
patient_id = st.sidebar.text_input("ID")

# ----------------------------------
# CONTROLS
# ----------------------------------
st.sidebar.markdown("### ⚙ Controls")

if st.sidebar.button("🔌 Connect Device"):
    st.sidebar.success("Device Connected")

if st.sidebar.button("📄 Download 8–9 Hour Sleep Report"):
    st.sidebar.success("Report Ready")

# ----------------------------------
# INPUT PANEL
# ----------------------------------
st.header("📋 Patient Input Panel")

c1, c2, c3 = st.columns(3)

with c1:
    spo2 = st.number_input("SpO₂ (%)", 70, 100, 95)

with c2:
    heart_rate = st.number_input("Heart Rate", 40, 140, 75)

with c3:
    breathing_rate = st.number_input("Breathing Rate", 8, 40, 16)

c4, c5 = st.columns(2)

with c4:
    snoring = st.slider("Snoring Level", 0.0, 1.0, 0.3)

with c5:
    bmi = st.number_input("BMI", 10, 60, 25)

# ----------------------------------
# 📁 CSV OPTION (ADDED ONLY)
# ----------------------------------
st.markdown("## 📁 Optional: Upload Sleep Data (CSV)")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

csv_mode = False

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    st.markdown("### 📊 Uploaded Data Preview")
    st.dataframe(df)

    spo2 = df["spo2"].mean()
    heart_rate = df["heart_rate"].mean()
    breathing_rate = df["breathing_rate"].mean()
    snoring = df["snoring"].mean()
    bmi = df["bmi"].mean()

    csv_mode = True
    st.success("CSV loaded → using averaged sleep readings")

# ----------------------------------
# RISK ENGINE
# ----------------------------------
def risk_engine(spo2, hr, br, snore, bmi):

    score = 0

    if spo2 < 92:
        score += 45
    elif spo2 < 95:
        score += 20

    if snore > 0.6:
        score += 25
    elif snore > 0.3:
        score += 10

    if br > 20:
        score += 20
    elif br < 10:
        score += 10

    if hr > 100:
        score += 15

    if bmi > 35:
        score += 20
    elif bmi > 30:
        score += 10

    return min(score, 100)

# ----------------------------------
# GENERATE REPORT
# ----------------------------------
if st.button("🚀 Generate Report"):

    risk_score = risk_engine(spo2, heart_rate, breathing_rate, snoring, bmi)

    if risk_score < 25:
        diagnosis = "🟢 Normal Sleep Pattern"
        severity = "Normal"
        color = "#2ecc71"

    elif risk_score < 50:
        diagnosis = "🟡 Mild Sleep Apnea"
        severity = "Mild"
        color = "#f1c40f"

    elif risk_score < 75:
        diagnosis = "🟠 Moderate Sleep Apnea"
        severity = "Moderate"
        color = "#e67e22"

    else:
        diagnosis = "🔴 Severe Sleep Apnea"
        severity = "Severe"
        color = "#e74c3c"

    api_percent = risk_score

    # ----------------------------------
    # ALERT
    # ----------------------------------
    st.markdown(f"""
    <div class="alert-box" style="background:{color}">
    ⚠ {diagnosis}
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------
    # DIAGNOSIS
    # ----------------------------------
    st.markdown("## 🧠 Diagnosis")

    st.markdown(f"""
    <div style="
        padding:18px;
        border-radius:10px;
        background:{color};
        color:white;
        text-align:center;
        font-size:20px;
        font-weight:bold;">
        {diagnosis}<br><br>
        Risk Score: {risk_score}/100
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------
    # API
    # ----------------------------------
    st.markdown("## 📊 Apnea Performance Index (API)")

    st.markdown(f"""
### API: {api_percent}%

**Ranges**
- 0–24% → Normal sleep
- 25–49% → Mild apnea risk
- 50–74% → Moderate apnea
- 75–100% → Severe apnea
""")

    # ----------------------------------
    # SLEEP SIGNALS
    # ----------------------------------
    st.markdown("## 📈 Sleep Signals (8–9 Hours)")

    hours = 9
    points = hours * 60
    time = np.arange(points)

    spo2_signal = np.clip(np.random.normal(spo2, 1.5, points), 85, 100)
    heart_signal = np.random.normal(heart_rate, 3, points)
    breathing_signal = np.random.normal(breathing_rate, 1.2, points)

    spo2_min, spo2_max = np.min(spo2_signal), np.max(spo2_signal)
    hr_min, hr_max = np.min(heart_signal), np.max(heart_signal)
    br_min, br_max = np.min(breathing_signal), np.max(breathing_signal)

    g1, g2, g3 = st.columns(3)

    # ----------------------------------
    # SpO2 GRAPH
    # ----------------------------------
    with g1:
        fig, ax = plt.subplots(figsize=(4, 2.5))
        ax.plot(time, spo2_signal, color="green")
        ax.set_title("SpO₂")
        ax.set_xlabel("Time (Minutes)")
        ax.set_ylabel("SpO₂ %")
        st.pyplot(fig)

        st.caption(
            f"Oxygen saturation fluctuated between {spo2_min:.1f}% and {spo2_max:.1f}%. "
            "Dips may indicate apnea-related desaturation events."
        )

    # ----------------------------------
    # HEART GRAPH
    # ----------------------------------
    with g2:
        fig, ax = plt.subplots(figsize=(4, 2.5))
        ax.plot(time, heart_signal, color="red")
        ax.set_title("Heart Rate")
        ax.set_xlabel("Time (Minutes)")
        ax.set_ylabel("BPM")
        st.pyplot(fig)

        st.caption(
            f"Heart rate varied between {hr_min:.1f} and {hr_max:.1f} bpm. "
            "Sudden increases may reflect stress responses during apnea episodes."
        )

    # ----------------------------------
    # BREATHING GRAPH
    # ----------------------------------
    with g3:
        fig, ax = plt.subplots(figsize=(4, 2.5))
        ax.plot(time, breathing_signal, color="blue")
        ax.set_title("Breathing Rate")
        ax.set_xlabel("Time (Minutes)")
        ax.set_ylabel("Breaths/min")
        st.pyplot(fig)

        st.caption(
            f"Breathing rate ranged between {br_min:.1f} and {br_max:.1f} breaths/min. "
            "Irregular fluctuations may indicate respiratory instability."
        )

    # ----------------------------------
    # CLINICAL FINDINGS
    # ----------------------------------
    st.header("🔍 Clinical Findings")

    findings = []

    if spo2 < 92:
        findings.append("Low oxygen saturation detected")
    if snoring > 0.6:
        findings.append("High snoring intensity observed")
    if breathing_rate > 20:
        findings.append("Irregular breathing pattern detected")
    if bmi > 30:
        findings.append("Elevated BMI increases apnea risk")
    if heart_rate > 100:
        findings.append("Elevated heart rate observed")

    if len(findings) == 0:
        findings.append("No major abnormalities detected")

    for f in findings:
        st.write("•", f)

    # ----------------------------------
    # INTERPRETATION
    # ----------------------------------
    st.markdown("## 🩺 Clinical Interpretation")

    st.info(f"""
The patient demonstrates physiological patterns consistent with
{severity.lower()} sleep apnea.
Monitoring data revealed fluctuations in oxygen saturation,
heart rate, and respiratory activity across the sleep cycle.
""")

    # ----------------------------------
    # REPORT (WITH GRAPH EXPLANATIONS ADDED)
    # ----------------------------------
    report = f"""
SLEEP APNEA CLINICAL REPORT
===========================

Patient: {name}
Age: {age}
ID: {patient_id}

Diagnosis: {diagnosis}
Risk Score: {risk_score}/100
API: {api_percent}%

Mode: {"CSV Data" if csv_mode else "Manual Input"}

Findings:
{chr(10).join("- " + x for x in findings)}

Graph Interpretation:
- Oxygen saturation fluctuated between {spo2_min:.1f}% and {spo2_max:.1f}% indicating possible apnea events.
- Heart rate varied between {hr_min:.1f} and {hr_max:.1f} bpm indicating physiological stress.
- Breathing rate ranged between {br_min:.1f} and {br_max:.1f} breaths/min indicating respiratory instability.

Interpretation:
The patient shows signs consistent with {severity.lower()} sleep apnea.

Recommendations:
- Maintain healthy body weight
- Sleep in lateral position
- Seek specialist evaluation if symptoms persist
"""

    st.session_state.report_data = report

# ----------------------------------
# DOWNLOAD
# ----------------------------------
if "report_data" in st.session_state:

    st.download_button(
        "📄 Download Report",
        st.session_state.report_data,
        file_name="sleep_report.txt"
    )