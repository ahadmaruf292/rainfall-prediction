import streamlit as st
import numpy as np
import pickle

# বাংলা ফন্ট ও কাস্টম স্টাইল inject করা
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Siyam+Rupali&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Siyam Rupali', serif;
        background-color: #E0F7FA;
    }
    .stButton>button {
        background-color: #00838F;
        color: white;
        font-weight: bold;
    }
    .stSelectbox>div>div>div>select {
        color: #004D40;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Model লোড
model = pickle.load(open('rainfall_model.pkl', 'rb'))

# Language select
lang = st.sidebar.selectbox("Select Language / ভাষা নির্বাচন করুন", ["English", "বাংলা"])

if lang == "English":
    wind_dir_map = {
        'N': 0, 'NNE': 1, 'NE': 2, 'ENE': 3, 'E': 4, 'ESE': 5,
        'SE': 6, 'SSE': 7, 'S': 8, 'SSW': 9, 'SW': 10, 'WSW': 11,
        'W': 12, 'WNW': 13, 'NW': 14, 'NNW': 15
    }
    rain_today_map = {'Yes': 1, 'No': 0}

    title = "🌧️ Rainfall Prediction App"
    subtitle = "Enter today's weather data to predict if it will rain tomorrow."
    inputs = {
        "Max Temperature (°C)": 30.0,
        "Rainfall (mm)": 0.0,
        "Evaporation (mm)": 5.0,
        "Sunshine (hours)": 7.0,
        "Wind Gust Direction": list(wind_dir_map.keys()),
        "Wind Gust Speed (km/h)": 35.0,
        "Humidity at 9AM (%)": (0, 100, 70),
        "Humidity at 3PM (%)": (0, 100, 50),
        "Pressure at 9AM (hPa)": 1010.0,
        "Pressure at 3PM (hPa)": 1008.0,
        "Cloud at 9AM (oktas)": (0, 8, 4),
        "Cloud at 3PM (oktas)": (0, 8, 4),
        "Temperature at 3PM (°C)": 29.0,
        "Did it rain today?": ['Yes', 'No'],
        "RISK_MM (Risk of rain in mm)": 0.0
    }
    predict_btn = "📊 Predict Rainfall Tomorrow"
    rain_yes = "🌧️ Rain Expected Tomorrow!"
    rain_no = "☀️ No Rain Expected Tomorrow."
    error_msg = "Prediction failed: "
else:
    wind_dir_map = {
        'উত্তর': 0, 'উত্তর-উত্তর-পূর্ব': 1, 'উত্তর-পূর্ব': 2, 'পূর্ব-উত্তর-পূর্ব': 3,
        'পূর্ব': 4, 'পূর্ব-দক্ষিণ-পূর্ব': 5, 'দক্ষিণ-পূর্ব': 6, 'দক্ষিণ-দক্ষিণ-পূর্ব': 7,
        'দক্ষিণ': 8, 'দক্ষিণ-দক্ষিণ-পশ্চিম': 9, 'দক্ষিণ-পশ্চিম': 10, 'পশ্চিম-দক্ষিণ-পশ্চিম': 11,
        'পশ্চিম': 12, 'পশ্চিম-উত্তর-পশ্চিম': 13, 'উত্তর-পশ্চিম': 14, 'উত্তর-উত্তর-পশ্চিম': 15
    }
    rain_today_map = {'হ্যাঁ': 1, 'না': 0}

    title = "🌧️ বৃষ্টির পূর্বাভাস অ্যাপ"
    subtitle = "আগাম বৃষ্টির পূর্বাভাস পেতে আজকের আবহাওয়ার তথ্য দিন।"
    inputs = {
        "সর্বোচ্চ তাপমাত্রা (°C)": 30.0,
        "বৃষ্টির পরিমাণ (মিমি)": 0.0,
        "বাষ্পীভবন (মিমি)": 5.0,
        "সূর্যালোক (ঘন্টা)": 7.0,
        "দমকা বাতাসের দিক": list(wind_dir_map.keys()),
        "দমকা বাতাসের গতি (কিমি/ঘণ্টা)": 35.0,
        "সকাল ৯টায় আর্দ্রতা (%)": (0, 100, 70),
        "বিকাল ৩টায় আর্দ্রতা (%)": (0, 100, 50),
        "সকাল ৯টায় চাপ (hPa)": 1010.0,
        "বিকাল ৩টায় চাপ (hPa)": 1008.0,
        "সকাল ৯টায় মেঘ (০-৮)": (0, 8, 4),
        "বিকাল ৩টায় মেঘ (০-৮)": (0, 8, 4),
        "বিকাল ৩টায় তাপমাত্রা (°C)": 29.0,
        "আজ কি বৃষ্টি হয়েছে?": ['হ্যাঁ', 'না'],
        "বৃষ্টির ঝুঁকি (RISK_MM)": 0.0
    }
    predict_btn = "📊 বৃষ্টির পূর্বাভাস দেখুন"
    rain_yes = "🌧️ আগামীকাল বৃষ্টি হতে পারে!"
    rain_no = "☀️ আগামীকাল বৃষ্টি হওয়ার সম্ভাবনা কম।"
    error_msg = "পূর্বাভাসে সমস্যা হয়েছে: "

st.title(title)
st.markdown(subtitle)

max_temp = st.number_input(list(inputs.keys())[0], value=inputs[list(inputs.keys())[0]])
rainfall = st.number_input(list(inputs.keys())[1], value=inputs[list(inputs.keys())[1]])
evaporation = st.number_input(list(inputs.keys())[2], value=inputs[list(inputs.keys())[2]])
sunshine = st.number_input(list(inputs.keys())[3], value=inputs[list(inputs.keys())[3]])

wind_gust_dir_label = st.selectbox(list(inputs.keys())[4], inputs[list(inputs.keys())[4]])
wind_gust_dir = wind_dir_map[wind_gust_dir_label]

wind_gust_speed = st.number_input(list(inputs.keys())[5], value=inputs[list(inputs.keys())[5]])

humidity_9am = st.slider(list(inputs.keys())[6], *inputs[list(inputs.keys())[6]])
humidity_3pm = st.slider(list(inputs.keys())[7], *inputs[list(inputs.keys())[7]])

pressure_9am = st.number_input(list(inputs.keys())[8], value=inputs[list(inputs.keys())[8]])
pressure_3pm = st.number_input(list(inputs.keys())[9], value=inputs[list(inputs.keys())[9]])

cloud_9am = st.slider(list(inputs.keys())[10], *inputs[list(inputs.keys())[10]])
cloud_3pm = st.slider(list(inputs.keys())[11], *inputs[list(inputs.keys())[11]])

temp_3pm = st.number_input(list(inputs.keys())[12], value=inputs[list(inputs.keys())[12]])

rain_today_label = st.selectbox(list(inputs.keys())[13], list(rain_today_map.keys()))
rain_today = rain_today_map[rain_today_label]

risk_mm = st.number_input(list(inputs.keys())[14], value=inputs[list(inputs.keys())[14]])

input_data = np.array([[
    max_temp, rainfall, evaporation, sunshine,
    wind_gust_dir, wind_gust_speed,
    humidity_9am, humidity_3pm, pressure_9am, pressure_3pm,
    cloud_9am, cloud_3pm, temp_3pm,
    rain_today, risk_mm
]])

if st.button(predict_btn):
    try:
        prediction = model.predict(input_data)[0]
        if prediction == 1:
            st.success(rain_yes)
        else:
            st.info(rain_no)
    except Exception as e:
        st.error(error_msg + str(e))
