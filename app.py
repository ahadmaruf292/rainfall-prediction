import streamlit as st
import numpy as np
import pickle


model = pickle.load(open('rainfall_model.pkl', 'rb'))

st.title("🌧️ Rainfall Prediction App")
st.markdown("This app predicts tomorrow rainfall using weather conditions.")

st.sidebar.header("🔧 Input Weather Features")

wind_dir_mapping = {
    "N (0)": 0, "NNE (1)": 1, "NE (2)": 2, "ENE (3)": 3,
    "E (4)": 4, "ESE (5)": 5, "SE (6)": 6, "SSE (7)": 7,
    "S (8)": 8, "SSW (9)": 9, "SW (10)": 10, "WSW (11)": 11,
    "W (12)": 12, "WNW (13)": 13, "NW (14)": 14, "NNW (15)": 15
}

MaxTemp = st.sidebar.number_input("Max Temperature (°C)", 10.0, 50.0, 30.0)
Rainfall = st.sidebar.number_input("Rainfall Today (mm)", 0.0, 100.0, 5.0)
Evaporation = st.sidebar.number_input("Evaporation (mm)", 0.0, 50.0, 5.0)
Sunshine = st.sidebar.number_input("Sunshine (hours)", 0.0, 15.0, 7.0)
WindGustDir_label = st.sidebar.selectbox("Wind Gust Direction", list(wind_dir_mapping.keys()))
WindGustDir = wind_dir_mapping[WindGustDir_label]
WindGustSpeed = st.sidebar.number_input("Wind Gust Speed (km/h)", 0, 100, 35)
Humidity9am = st.sidebar.slider("Humidity at 9am (%)", 0, 100, 85)
Humidity3pm = st.sidebar.slider("Humidity at 3pm (%)", 0, 100, 65)
Pressure9am = st.sidebar.number_input("Pressure at 9am (hPa)", 980.0, 1040.0, 1012.0)
Pressure3pm = st.sidebar.number_input("Pressure at 3pm (hPa)", 980.0, 1040.0, 1010.0)
Cloud9am = st.sidebar.slider("Cloud at 9am (oktas)", 0, 8, 4)
Cloud3pm = st.sidebar.slider("Cloud at 3pm (oktas)", 0, 8, 4)
Temp3pm = st.sidebar.number_input("Temperature at 3pm (°C)", 10.0, 50.0, 29.0)
RainToday = st.sidebar.selectbox("Did it rain today?", ['No', 'Yes'])
RainToday_encoded = 1 if RainToday == 'Yes' else 0
RISK_MM = st.sidebar.number_input("Manual RISK_MM value (optional, use 0 if unknown)", 0.0, 100.0, 0.0)


input_data = np.array([[
    MaxTemp, Rainfall, Evaporation, Sunshine, WindGustDir,
    WindGustSpeed, Humidity9am, Humidity3pm, Pressure9am,
    Pressure3pm, Cloud9am, Cloud3pm, Temp3pm, RainToday_encoded, RISK_MM
]])


if st.button("🔍 Predict Tomorrow Rainfall"):
    prediction = model.predict(input_data)[0]
    st.subheader(f"🌧️ Tomorrow Rainfall Predictions:")
    if prediction > 10:
        st.warning("☔ High risk of heavy rainfall.")
    elif prediction > 0:
        st.info("🌦️ Light rain likely.")
    else:
        st.success("🌞 No rain expected.")

st.markdown("---")
st.markdown("Built by **Ahad Maruf** using Streamlit & Machine Learning.")
