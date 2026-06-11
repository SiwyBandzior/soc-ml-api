import streamlit as st
import requests

st.set_page_config(page_title="SOC Anomaly Dashboard", layout="centered")

st.title("🛡️ SOC Network Traffic Analyzer")
st.markdown("Enter network packet details below to run real-time AI anomaly detection.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    packet_size = st.number_input("Packet Size (Bytes)", min_value=1.0, value=500.0, step=10.0)
with col2:
    session_duration = st.number_input("Session Duration (ms)", min_value=0.1, value=30.0, step=1.0)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Analyze Traffic", type="primary", use_container_width=True):
    payload = {
        "packet_size_bytes": packet_size,
        "session_duration_ms": session_duration
    }
    try:
        response = requests.post("http://127.0.0.1:8000/analyze/", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.divider()
            if result["status"] == "DANGER":
                st.error(f"🚨 **DANGER: Anomaly Detected!** The AI flagged this traffic as suspicious.")
            else:
                st.success(f"✅ **SAFE: Normal Traffic.** No anomalies detected.")
            st.info(f"**AI Confidence Score (Anomaly Score):** {result['anomaly_score']}")
        else:
            st.warning("API responded, but there was an error processing the request.")
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the API. Is your Docker container running?")

st.divider()

# --- ADMIN SECTION (RETRAINING) ---
st.markdown("### ⚙️ SOC Administration")
st.markdown("Force the AI to learn from the newly collected network traffic history.")

if st.button("🔄 Retrain AI Model", type="secondary"):
    try:
        retrain_response = requests.post("http://127.0.0.1:8000/retrain/")
        if retrain_response.status_code == 200:
            res_data = retrain_response.json()
            if res_data["status"] == "success":
                st.toast("🧠 AI Model successfully updated!", icon="✅")
                st.success(res_data["message"])
            elif res_data["status"] == "warning":
                st.warning(res_data["message"])
            else:
                st.error(res_data["message"])
        else:
            st.error(f"❌ API Error ({retrain_response.status_code}): {retrain_response.text}")
    except requests.exceptions.ConnectionError:
        st.error("❌ API Offline.")