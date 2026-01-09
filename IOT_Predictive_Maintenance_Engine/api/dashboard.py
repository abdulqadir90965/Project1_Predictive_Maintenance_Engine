import streamlit as st
import requests

st.title("Predictive Maintenance Dashboard")

st.write("Enter sensor values to predict machine failure")

# User inputs
vibration = st.number_input("Vibration (m/s²)", value=3.0)
temperature = st.number_input("Temperature (°C)", value=80.0)

vib_lag = st.number_input("Vibration Lag 1", value=2.9)
temp_lag = st.number_input("Temperature Lag 1", value=79.5)

vib_roll = st.number_input("Vibration Rolling Mean 8", value=2.8)
temp_roll = st.number_input("Temperature Rolling Mean 8", value=78.5)

if st.button("Predict Failure"):
    payload = {
        "Vibration (m/s²)": vibration,
        "Temperature (°C)": temperature,
        "Vibration (m/s²)_lag_1": vib_lag,
        "Temperature (°C)_lag_1": temp_lag,
        "Vibration (m/s²)_roll_mean_8": vib_roll,
        "Temperature (°C)_roll_mean_8": temp_roll
    }

    response = requests.post(
        "http://127.0.0.1:5000/predict",
        json=payload
    )

    result = response.json()

    st.subheader("Prediction Result")
    st.write("Failure Probability:", result["failure_probability"])

    st.subheader("Top Risk Factors")
    st.table(result["top_risk_factors"])
