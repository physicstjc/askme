import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time
from datetime import datetime, timedelta, timezone

# Function to fetch wind speed data
def fetch_wind_speed(date_time=None, date=None):
    base_url = "https://api.data.gov.sg/v1/environment/wind-direction"
    params = {}
    if date_time:
        params['date_time'] = date_time
    if date:
        params['date'] = date
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API")
        return None

# Function to get the current time in GMT+8
def get_current_time_gmt8():
    gmt8 = timezone(timedelta(hours=8))
    return datetime.now(gmt8)

# Initialize an empty DataFrame to store wind speed data
if 'wind_speed_data' not in st.session_state:
    st.session_state.wind_speed_data = pd.DataFrame(columns=['timestamp', 'wind_speed'])

# Function to log wind speed data for station "S107"
def log_wind_speed():
    current_time_gmt8 = get_current_time_gmt8()
    date_time_str = current_time_gmt8.strftime("%Y-%m-%dT%H:%M:%S")
    data = fetch_wind_speed(date_time=date_time_str)
    if data:
        for item in data['items']:
            for reading in item['readings']:
                if reading['station_id'] == "S107":
                    new_data = {
                        'timestamp': item['timestamp'],
                        'wind_speed': reading['value']
                    }
                    st.session_state.wind_speed_data = st.session_state.wind_speed_data.append(new_data, ignore_index=True)

# Streamlit app layout
st.title("Singapore Wind Speed Data Logger")

# Start and stop logging buttons
if st.button('Start Logging'):
    st.session_state.logging = True
elif st.button('Stop Logging'):
    st.session_state.logging = False

# Periodically log data if logging is enabled
if 'logging' not in st.session_state:
    st.session_state.logging = False

if st.session_state.logging:
    log_wind_speed()
    time.sleep(600)  # Sleep for 10 minutes

# Display the logged data
st.subheader("Logged Wind Speed Data for Station S107")
st.dataframe(st.session_state.wind_speed_data)

# Display the data in a graph
if not st.session_state.wind_speed_data.empty:
    fig = px.line(st.session_state.wind_speed_data, x='timestamp', y='wind_speed', title='Wind Speed at Station S107 Over Time')
    st.plotly_chart(fig)
