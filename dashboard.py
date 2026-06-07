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
                st.error(f"🚨 **DANGER: Anomaly Detected!** The API flagged this traffic as suspicious.")
            else:
                st.success(f"✅ **SAFE: Normal Traffic.** No anomalies detected.")

            st.info(f"**AI Confidence Score (Anomaly Score):** {result['anomaly_score']}")
        
        else:
            st.warning("API responded, but there was an error processing the request.")
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the API. Is your Docker container running?")