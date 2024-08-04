import streamlit as st
import requests
from datetime import datetime

def get_wind_speed(station_id, station_name, date_time):
    url = "https://api-open.data.gov.sg/v2/real-time/api/wind-speed"
    params = {
        "date": date_time
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        readings = data.get('data', {}).get('readings', [])
        for reading in readings:
            for station_data in reading.get('data', []):
                if station_data.get('stationId') == station_id:
                    return {
                        "station_name": station_name,
                        "timestamp": reading.get("timestamp"),
                        "wind_speed": station_data.get("value"),
                        "unit": data.get('data', {}).get('readingUnit')
                    }
    return None

st.title("Real-time Wind Speed Data")

station_id = "S107"
station_name = "East Coast Parkway"
date_time = st.text_input("Enter the date and time (YYYY-MM-DDTHH:MM:SS)", value=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

if st.button("Get Wind Speed"):
    wind_speed_data = get_wind_speed(station_id, station_name, date_time)
    if wind_speed_data:
        st.write(f"**Wind speed at {wind_speed_data['station_name']} (Station ID: {station_id})**")
        st.write(f"**Timestamp:** {wind_speed_data['timestamp']}")
        st.write(f"**Wind Speed:** {wind_speed_data['wind_speed']} {wind_speed_data['unit']}")
    else:
        st.write("No data found for the specified station and time.")
