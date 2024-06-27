import streamlit as st
import requests
import pandas as pd
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

# Streamlit app layout
st.title("Singapore Wind Speed Data")

# Get current time in GMT+8
current_time_gmt8 = get_current_time_gmt8()
current_time_str = current_time_gmt8.strftime("%Y-%m-%dT%H:%M:%S")

# Date and time input
date_time_input = st.text_input("Enter date and time (YYYY-MM-DDTHH:mm:ss)", value=current_time_str)
date_input = st.text_input("Enter date (YYYY-MM-DD)", value=current_time_gmt8.strftime("%Y-%m-%d"))

# Fetch data button
if st.button("Fetch Wind Speed Data"):
    data = fetch_wind_speed(date_time=date_time_input, date=date_input)
    if data:
        st.success("Data fetched successfully")

        # Display API info
        st.subheader("API Info")
        st.json(data['api_info'])

        # Display metadata
        st.subheader("Metadata")
        st.json(data['metadata'])

        # Process and display items
        st.subheader("Wind Speed Readings")
        items = data['items']
        if items:
            for item in items:
                timestamp = item['timestamp']
                readings = item['readings']
                st.write(f"Timestamp: {timestamp}")
                for reading in readings:
                    station_id = reading['station_id']
                    value = reading['value']
                    st.write(f"Station ID: {station_id}, Wind Speed: {value} m/s")

            # Convert to DataFrame for better display
            readings_data = [
                {
                    "timestamp": item['timestamp'],
                    "station_id": reading['station_id'],
                    "wind_speed": reading['value']
                }
                for item in items for reading in item['readings']
            ]
            df = pd.DataFrame(readings_data)
            st.dataframe(df)
        else:
            st.write("No readings available for the specified date/time")
