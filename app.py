import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(page_title="myAPNEA", layout="wide")

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
    '<div class="main-title">💤 myAPNEA - Sleep Apnea Monitoring System</div>',
    unsafe_allow_html=True
)

now = datetime.now()


# ----------------------------------
# SIDEBAR
# ----------------------------------
st.sidebar.markdown("## ℹ About myAPNEA")

st.sidebar.markdown("""
<div class="about-box">
<b>myAPNEA</b> is an AI-based sleep apnea monitoring system using vital signs.<br><br>
It analyzes SpO₂, heart rate, breathing rate, snoring level, and BMI.<br><br>
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
# CSV OPTION
# ----------------------------------

st.markdown("## 📁 Optional: Upload Sleep Data (CSV)")


uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)


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



    return min(score,100)



# ----------------------------------
# GENERATE REPORT
# ----------------------------------

if st.button("🚀 Generate Report"):


    st.session_state.report_generated = True


    st.session_state.generated_inputs = {

        "spo2": float(spo2),
        "heart_rate": float(heart_rate),
        "breathing_rate": float(breathing_rate),
        "snoring": float(snoring),
        "bmi": float(bmi),

        "name": name,
        "age": age,
        "patient_id": patient_id,

        "csv_mode": csv_mode

    }



if st.session_state.get("report_generated", False):


    generated_inputs = st.session_state.generated_inputs


    spo2 = generated_inputs["spo2"]
    heart_rate = generated_inputs["heart_rate"]
    breathing_rate = generated_inputs["breathing_rate"]
    snoring = generated_inputs["snoring"]
    bmi = generated_inputs["bmi"]

    name = generated_inputs["name"]
    age = generated_inputs["age"]
    patient_id = generated_inputs["patient_id"]

    csv_mode = generated_inputs["csv_mode"]


    risk_score = risk_engine(
        spo2,
        heart_rate,
        breathing_rate,
        snoring,
        bmi
    )



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
    # PHYSIOLOGICAL PARAMETER BOXES
    # ----------------------------------

    st.markdown("## 📊 Physiological Parameters")


    col1, col2, col3, col4, col5 = st.columns(5)


    col1.markdown(f"""
    <div style="background:#1abc9c;padding:10px;border-radius:10px;color:white;text-align:center;font-weight:bold;">
    SpO₂<br>{spo2:.1f} %
    </div>
    """, unsafe_allow_html=True)


    col2.markdown(f"""
    <div style="background:#3498db;padding:10px;border-radius:10px;color:white;text-align:center;font-weight:bold;">
    Heart Rate<br>{heart_rate:.1f} bpm
    </div>
    """, unsafe_allow_html=True)


    col3.markdown(f"""
    <div style="background:#9b59b6;padding:10px;border-radius:10px;color:white;text-align:center;font-weight:bold;">
    Breathing Rate<br>{breathing_rate:.1f} /min
    </div>
    """, unsafe_allow_html=True)


    col4.markdown(f"""
    <div style="background:#e67e22;padding:10px;border-radius:10px;color:white;text-align:center;font-weight:bold;">
    Snoring<br>{snoring:.2f}
    </div>
    """, unsafe_allow_html=True)


    col5.markdown(f"""
    <div style="background:#e74c3c;padding:10px;border-radius:10px;color:white;text-align:center;font-weight:bold;">
    BMI<br>{bmi:.1f}
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



    signal_key = (
        round(float(spo2),3),
        round(float(heart_rate),3),
        round(float(breathing_rate),3),
        severity
    )



    if st.session_state.get("signal_key") != signal_key:


        if severity == "Normal":

            spo2_signal = np.clip(
                np.random.normal(spo2,0.3,points),
                spo2-0.8,
                spo2+0.8
            )

            heart_signal = np.clip(
                np.random.normal(heart_rate,1.2,points),
                heart_rate-3,
                heart_rate+3
            )

            breathing_signal = np.clip(
                np.random.normal(breathing_rate,0.4,points),
                breathing_rate-1,
                breathing_rate+1
            )


        elif severity == "Mild":

            spo2_signal = np.clip(
                np.random.normal(spo2,0.4,points),
                spo2-1.2,
                spo2+1.2
            )

            heart_signal = np.clip(
                np.random.normal(heart_rate,1.5,points),
                heart_rate-4,
                heart_rate+4
            )

            breathing_signal = np.clip(
                np.random.normal(breathing_rate,0.5,points),
                breathing_rate-1.3,
                breathing_rate+1.3
            )


        elif severity == "Moderate":

            spo2_signal = np.clip(
                np.random.normal(spo2,0.5,points),
                spo2-1.5,
                spo2+1.5
            )

            heart_signal = np.clip(
                np.random.normal(heart_rate,2.0,points),
                heart_rate-5,
                heart_rate+5
            )

            breathing_signal = np.clip(
                np.random.normal(breathing_rate,0.7,points),
                breathing_rate-1.8,
                breathing_rate+1.8
            )


        else:

            spo2_signal = np.clip(
                np.random.normal(spo2,0.7,points),
                spo2-2.0,
                spo2+2.0
            )

            heart_signal = np.clip(
                np.random.normal(heart_rate,2.5,points),
                heart_rate-6,
                heart_rate+6
            )

            breathing_signal = np.clip(
                np.random.normal(breathing_rate,0.8,points),
                breathing_rate-2.0,
                breathing_rate+2.0
            )



        st.session_state.spo2_signal = spo2_signal
        st.session_state.heart_signal = heart_signal
        st.session_state.breathing_signal = breathing_signal

        st.session_state.signal_key = signal_key



    spo2_signal = st.session_state.spo2_signal
    heart_signal = st.session_state.heart_signal
    breathing_signal = st.session_state.breathing_signal



    spo2_min, spo2_max = np.min(spo2_signal), np.max(spo2_signal)
    hr_min, hr_max = np.min(heart_signal), np.max(heart_signal)
    br_min, br_max = np.min(breathing_signal), np.max(breathing_signal)



    g1, g2, g3 = st.columns(3)



    with g1:

        fig, ax = plt.subplots(figsize=(4,2.5))

        ax.plot(time,spo2_signal,color="green")

        ax.set_title("SpO₂")
        ax.set_xlabel("Time (Minutes)")
        ax.set_ylabel("SpO₂ %")

        st.pyplot(fig)



    with g2:

        fig, ax = plt.subplots(figsize=(4,2.5))

        ax.plot(time,heart_signal,color="red")

        ax.set_title("Heart Rate")
        ax.set_xlabel("Time (Minutes)")
        ax.set_ylabel("BPM")

        st.pyplot(fig)



    with g3:

        fig, ax = plt.subplots(figsize=(4,2.5))

        ax.plot(time,breathing_signal,color="blue")

        ax.set_title("Breathing Rate")
        ax.set_xlabel("Time (Minutes)")
        ax.set_ylabel("Breaths/min")

        st.pyplot(fig)



    # ----------------------------------
    # NEW FEATURE:
    # OXYGEN DESATURATION EVENTS
    # ----------------------------------

    st.markdown("## ⚠️ Oxygen Desaturation & Breathing Events")


    events = []


    for i in range(len(spo2_signal)):


        if spo2_signal[i] < 92 or breathing_signal[i] < 10:


            event = []


            if spo2_signal[i] < 92:

                event.append("Oxygen Desaturation")


            if breathing_signal[i] < 10:

                event.append("Reduced Breathing")



            if spo2_signal[i] < 88:

                severity_event = "Severe"

            elif spo2_signal[i] < 92:

                severity_event = "Moderate"

            else:

                severity_event = "Low Breathing"



            events.append({

                "Time": f"{i//60:02d}:{i%60:02d}",

                "SpO₂ (%)": round(float(spo2_signal[i]),1),

                "Breathing Rate (/min)": round(float(breathing_signal[i]),1),

                "Detected Event": " + ".join(event),

                "Severity": severity_event

            })



    if len(events) > 0:


        event_df = pd.DataFrame(events)



        def highlight(row):

            if row["Severity"] == "Severe":

                return ['background-color:#ffcccc']*len(row)

            elif row["Severity"] == "Moderate":

                return ['background-color:#fff2cc']*len(row)

            else:

                return ['background-color:#eeeeee']*len(row)



        st.dataframe(
            event_df.style.apply(highlight,axis=1),
            use_container_width=True
        )


        st.caption(
            "Detected events represent periods where oxygen saturation "
            "or breathing activity deviated from expected sleep patterns."
        )


    else:


        st.success(
            "No significant oxygen desaturation or breathing abnormalities detected."
        )
    # ----------------------------------
    # ADVANCED SLEEP ANALYSIS
    # ----------------------------------

    st.markdown("## 🔬 Advanced Sleep Analysis")

    st.markdown("### 🫁 Sleep Oxygen Status")


    normal_oxygen = np.sum(spo2_signal >= 95)

    mild_reduction = np.sum(
        (spo2_signal >= 92) &
        (spo2_signal < 95)
    )

    low_oxygen = np.sum(spo2_signal < 92)



    oxygen_counts = [
        normal_oxygen,
        mild_reduction,
        low_oxygen
    ]


    oxygen_labels = [
        "Normal Oxygenation (≥95%)",
        "Mild Reduction (92–94%)",
        "Low Oxygenation (<92%)"
    ]


    oxygen_colors = [
        "#2ecc71",
        "#f1c40f",
        "#e74c3c"
    ]



    filtered_counts = []
    filtered_labels = []
    filtered_colors = []


    for count, label, pie_color in zip(
        oxygen_counts,
        oxygen_labels,
        oxygen_colors
    ):

        if count > 0:

            filtered_counts.append(count)
            filtered_labels.append(label)
            filtered_colors.append(pie_color)



    pie_col1, pie_col2 = st.columns([1.2,1])


    with pie_col1:

        fig, ax = plt.subplots(figsize=(5,4))

        ax.pie(
            filtered_counts,
            labels=filtered_labels,
            colors=filtered_colors,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={
                "edgecolor":"white",
                "linewidth":1
            }
        )

        ax.set_title(
            "Distribution of SpO₂ Readings During Sleep"
        )

        ax.axis("equal")

        st.pyplot(fig)



    with pie_col2:


        total_readings = len(spo2_signal)


        normal_percent = (
            normal_oxygen /
            total_readings
        ) * 100


        mild_percent = (
            mild_reduction /
            total_readings
        ) * 100


        low_percent = (
            low_oxygen /
            total_readings
        ) * 100



        st.info(f"""
**Oxygen Distribution Summary**

🟢 Normal Oxygenation (≥95%): {normal_percent:.1f}%

🟡 Mild Reduction (92–94%): {mild_percent:.1f}%

🔴 Low Oxygenation (<92%): {low_percent:.1f}%


This chart summarizes oxygen saturation distribution throughout the monitored sleep period.
""")



    # ----------------------------------
    # INTERACTIVE SIGNAL VIEWER
    # ----------------------------------

    st.markdown("### 📊 Interactive Signal Viewer")


    selected_signals = st.multiselect(

        "Select signals to display",

        [
            "SpO₂",
            "Heart Rate",
            "Breathing Rate"
        ],

        default=[
            "SpO₂",
            "Heart Rate",
            "Breathing Rate"
        ]

    )



    start_minute, end_minute = st.slider(

        "Select monitoring time range (minutes)",

        min_value=0,

        max_value=points-1,

        value=(0,points-1),

        step=10

    )



    selected_time = time[
        start_minute:end_minute+1
    ]



    if selected_signals:


        fig, ax = plt.subplots(
            figsize=(10,4)
        )


        if "SpO₂" in selected_signals:

            ax.plot(
                selected_time,
                spo2_signal[start_minute:end_minute+1],
                label="SpO₂"
            )


        if "Heart Rate" in selected_signals:

            ax.plot(
                selected_time,
                heart_signal[start_minute:end_minute+1],
                label="Heart Rate"
            )


        if "Breathing Rate" in selected_signals:

            ax.plot(
                selected_time,
                breathing_signal[start_minute:end_minute+1],
                label="Breathing Rate"
            )


        ax.set_title(
            "Interactive Multi-Signal Viewer"
        )

        ax.set_xlabel(
            "Time (Minutes)"
        )

        ax.set_ylabel(
            "Signal Value"
        )

        ax.legend()

        ax.grid(alpha=0.2)

        st.pyplot(fig)



    else:

        st.warning(
            "Select at least one signal to display."
        )



    # ----------------------------------
    # CLINICAL FINDINGS
    # ----------------------------------

    st.header("🔍 Clinical Findings")


    findings = []


    if spo2 < 92:

        findings.append(
            "Low oxygen saturation detected"
        )


    if snoring > 0.6:

        findings.append(
            "High snoring intensity observed"
        )


    if breathing_rate > 20:

        findings.append(
            "Irregular breathing pattern detected"
        )


    if bmi > 30:

        findings.append(
            "Elevated BMI increases apnea risk"
        )


    if heart_rate > 100:

        findings.append(
            "Elevated heart rate observed"
        )



    if len(findings)==0:

        findings.append(
            "No major abnormalities detected"
        )



    for f in findings:

        st.write(
            "•",
            f
        )



    # ----------------------------------
    # CLINICAL INTERPRETATION
    # ----------------------------------

    st.markdown(
        "## 🩺 Clinical Interpretation"
    )


    st.info(f"""

The patient demonstrates physiological patterns consistent with
{severity.lower()} sleep apnea.

Monitoring data revealed fluctuations in oxygen saturation,
heart rate, and respiratory activity across the sleep cycle.

""")



    # ----------------------------------
    # RECOMMENDATIONS
    # ----------------------------------

    st.markdown(
        "## 💡 Recommendations"
    )



    if severity == "Normal":

        recommendations = [

            "No immediate medical treatment is required based on the current readings.",

            "Maintain a healthy sleep routine.",

            "Continue monitoring if symptoms such as snoring, morning headache, or daytime sleepiness appear."

        ]


    elif severity == "Mild":

        recommendations = [

            "Lifestyle modification is recommended.",

            "Maintain a healthy body weight.",

            "Sleep on the side instead of the back.",

            "Avoid sedatives before sleep.",

            "Consult a healthcare professional if symptoms persist."

        ]


    elif severity == "Moderate":

        recommendations = [

            "Medical evaluation by a sleep specialist is recommended.",

            "A full sleep study may be required.",

            "Weight management and sleep position correction are advised.",

            "Further clinical assessment is recommended."

        ]


    else:

        recommendations = [

            "Urgent evaluation by a sleep specialist is strongly recommended.",

            "The patient may need CPAP therapy.",

            "Continuous monitoring of oxygen saturation and breathing is advised.",

            "Medical follow-up is required."

        ]



    for rec in recommendations:

        st.write(
            "•",
            rec
        )



    # ----------------------------------
    # SESSION PATIENT HISTORY
    # ----------------------------------

    st.markdown(
        "### 🗂 Session Patient History"
    )


    if "patient_history" not in st.session_state:

        st.session_state.patient_history = []



    current_record = {

        "Patient":
            name if name else "Unnamed",

        "ID":
            patient_id if patient_id else "-",

        "Age":
            age,

        "SpO₂":
            round(float(spo2),1),

        "Heart Rate":
            round(float(heart_rate),1),

        "Breathing Rate":
            round(float(breathing_rate),1),

        "API":
            int(api_percent),

        "Classification":
            severity

    }



    if st.button(
        "➕ Add Current Result to Session History"
    ):

        st.session_state.patient_history.append(
            current_record
        )

        st.success(
            "Current result added to session history."
        )



    if st.session_state.patient_history:


        history_df = pd.DataFrame(
            st.session_state.patient_history
        )


        st.dataframe(
            history_df,
            use_container_width=True
        )

    else:

        st.caption(
            "No patient results have been added to the current session yet."
        )



    # ----------------------------------
    # FAQ
    # ----------------------------------

    with st.expander(
        "ℹ What does the API represent?"
    ):

        st.write(
            "The Apnea Performance Index (API) is the app's internal risk score derived from SpO₂, heart rate, breathing rate, snoring level, and BMI. It is not the same as the clinical Apnea-Hypopnea Index (AHI)."
        )



    with st.expander(
        "ℹ Why combine multiple parameters?"
    ):

        st.write(
            "A single abnormal physiological value does not necessarily indicate sleep apnea. The application therefore considers multiple readings together to provide a broader assessment."
        )



    with st.expander(
        "Can one abnormal reading mean that I have sleep apnea?"
    ):

        st.write(
            "No. A single abnormal SpO₂, heart-rate, breathing-rate, or snoring reading is not enough by itself to establish sleep apnea. The app evaluates the overall pattern and multiple monitored parameters together."
        )



    # ----------------------------------
    # REPORT GENERATION
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


Mode:
{"CSV Data" if csv_mode else "Manual Input"}


Findings:

{chr(10).join("- "+x for x in findings)}


Interpretation:

The patient shows signs consistent with {severity.lower()} sleep apnea.


Recommendations:

{chr(10).join("- "+x for x in recommendations)}

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
