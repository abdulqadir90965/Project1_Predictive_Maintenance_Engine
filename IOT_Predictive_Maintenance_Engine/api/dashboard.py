import streamlit as st
import requests

st.title("Predictive Maintenance Dashboard")
st.write("Enter sensor values to predict machine failure")

# API URL
url = "http://127.0.0.1:5000/predict"

# --- User Inputs ---
vibration = st.number_input("Vibration (m/s²)", value=3.2)
temperature = st.number_input("Temperature (°C)", value=82.5)

vib_lag_1 = st.number_input("Vibration Lag 1", value=3.0)
temp_lag_1 = st.number_input("Temperature Lag 1", value=81.9)

vib_roll_4 = st.number_input("Vibration Rolling Mean (4h)", value=2.9)
temp_roll_4 = st.number_input("Temperature Rolling Mean (4h)", value=80.8)

vib_roll_8 = st.number_input("Vibration Rolling Mean (8h)", value=2.7)
temp_roll_8 = st.number_input("Temperature Rolling Mean (8h)", value=79.6)

# --- Build Payload ---
def build_payload():
    return {
        "Vibration (m/s²)": vibration,
        "Temperature (°C)": temperature,
        "Vibration (m/s²)_lag_1": vib_lag_1,
        "Temperature (°C)_lag_1": temp_lag_1,
        "Vibration (m/s²)_roll_mean_4": vib_roll_4,
        "Temperature (°C)_roll_mean_4": temp_roll_4,
        "Vibration (m/s²)_roll_mean_8": vib_roll_8,
        "Temperature (°C)_roll_mean_8": temp_roll_8
    }

# --- Predict Button ---
if st.button("Predict Failure"):
    payload = build_payload()
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        result = response.json()

        st.subheader("Prediction Result")

        failure_prob = result["failure_probability"]

        st.write("Failure Probability:", round(failure_prob, 3))

# --- Color-coded Risk Indicator ---
        if failure_prob < 0.30:
            st.success("🟢 Low Risk: Machine is operating normally.")
        elif failure_prob < 0.60:
            st.warning("🟠 Medium Risk: Monitor the machine closely.")
        else:
            st.error("🔴 High Risk: Maintenance required within 24 hours.")

        st.subheader("Top Risk Factors")
        st.table(result["top_risk_factors"])
    else:
        st.error("API Error: Unable to get prediction")
